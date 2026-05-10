"""
Polling engine — fetches RSS feeds, filters per user profile, sends alerts.
"""
import hashlib
import logging
import aiohttp
import feedparser
from datetime import datetime, timezone

from utils.storage import get_all_profiles, is_seen, mark_seen
from utils.data import SOURCES, ATTACK_KEYWORDS, OS_KEYWORDS
from utils.formatters import format_alert

logger = logging.getLogger(__name__)


def _article_id(entry) -> str:
    raw = getattr(entry, "id", None) or getattr(entry, "link", "") or getattr(entry, "title", "")
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _matches_profile(text: str, source: dict, profile: dict) -> tuple[bool, list]:
    """
    Returns (matched, list_of_matched_attack_types).
    An article matches if:
      - Its source is not blocked by the user
      - At least one attack type keyword matches the user's selected attack types
      - (Optional) OS keyword matches if user has OS filter set
    """
    blocked = set(profile.get("blocked_sources", []))
    if source["id"] in blocked:
        return False, []

    user_attacks = set(profile.get("attack_types", []))
    user_os      = set(profile.get("os", []))
    text_low     = text.lower()

    # Check attack types
    matched_attacks = []
    for atk_id in user_attacks:
        keywords = ATTACK_KEYWORDS.get(atk_id, [])
        if any(kw in text_low for kw in keywords):
            matched_attacks.append(atk_id)

    if not matched_attacks:
        return False, []

    # If user selected specific OS, at least one must match
    if user_os:
        os_matched = any(
            any(kw in text_low for kw in OS_KEYWORDS.get(os_id, []))
            for os_id in user_os
        )
        if not os_matched:
            return False, []

    return True, matched_attacks


async def _fetch_rss(url: str) -> list:
    """Parse RSS feed, return list of entries."""
    try:
        parsed = feedparser.parse(url)
        return parsed.entries[:30]
    except Exception as e:
        logger.error(f"RSS parse error {url}: {e}")
        return []


async def _fetch_otx(api_key: str = "") -> list:
    """
    Fetch OTX AlienVault public pulses (free, no key = limited to 5 pulses).
    Returns list of fake 'entries' matching RSS structure.
    """
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {}
    if api_key:
        headers["X-OTX-API-KEY"] = api_key

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return []
                data = await resp.json()
                results = []
                for pulse in data.get("results", [])[:20]:
                    results.append({
                        "id":       pulse.get("id", ""),
                        "title":    pulse.get("name", ""),
                        "link":     f"https://otx.alienvault.com/pulse/{pulse.get('id','')}",
                        "summary":  pulse.get("description", ""),
                        "published": pulse.get("created", "")[:10],
                    })
                return results
    except Exception as e:
        logger.error(f"OTX fetch error: {e}")
        return []


def _entry_text(entry) -> str:
    if isinstance(entry, dict):
        return f"{entry.get('title','')} {entry.get('summary','')}"
    return f"{getattr(entry,'title','')} {getattr(entry,'summary','')}"


def _entry_fields(entry):
    if isinstance(entry, dict):
        return entry.get("id",""), entry.get("title",""), entry.get("link",""), entry.get("summary",""), entry.get("published","")
    return (
        getattr(entry,"id",""),
        getattr(entry,"title",""),
        getattr(entry,"link",""),
        getattr(entry,"summary",""),
        getattr(entry,"published","") or getattr(entry,"updated",""),
    )


async def run_poll(bot, config: dict) -> int:
    """
    Main poll: fetch all sources, match against all user profiles, send alerts.
    Returns total number of messages sent.
    """
    profiles = get_all_profiles()
    if not profiles:
        logger.info("No registered users yet.")
        return 0

    otx_key = config.get("OTX_API_KEY", "")
    total_sent = 0

    for source in SOURCES:
        # Fetch entries
        if source["type"] == "rss":
            entries = await _fetch_rss(source["url"])
        elif source["type"] == "api_otx":
            entries = await _fetch_otx(otx_key)
        else:
            # rss_scrape or unsupported — try as RSS anyway
            entries = await _fetch_rss(source["url"])

        for entry in entries:
            raw_id, title, link, summary, published = _entry_fields(entry)
            article_id = hashlib.sha256((raw_id or link or title).encode()).hexdigest()[:16]

            if is_seen(article_id):
                continue

            full_text = f"{title} {summary}"

            # Send to each user whose profile matches
            for chat_id, profile in profiles.items():
                matched, attack_types = _matches_profile(full_text, source, profile)
                if not matched:
                    continue

                message = format_alert(
                    title=title,
                    link=link,
                    source=source["name"],
                    summary=summary,
                    matched_types=attack_types,
                    published=published,
                )
                try:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=message,
                        parse_mode="HTML",
                        disable_web_page_preview=True,
                    )
                    total_sent += 1
                except Exception as e:
                    logger.error(f"Send failed to {chat_id}: {e}")

            mark_seen(article_id)

    logger.info(f"Poll complete. {total_sent} alerts sent.")
    return total_sent
