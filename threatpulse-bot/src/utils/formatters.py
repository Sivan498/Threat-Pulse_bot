"""
Formats alert messages for Telegram (HTML parse mode).
"""


def format_alert(title: str, link: str, source: str,
                 summary: str = "", matched_types: list = None,
                 published: str = "") -> str:
    type_badges = " ".join(_type_badge(t) for t in (matched_types or []))
    lines = [
        f"🛡️ <b>Threat Intel Alert</b>",
        f"━━━━━━━━━━━━━━━━━━━━",
        f"<b>{_esc(title)}</b>",
    ]
    if type_badges:
        lines.append(type_badges)
    lines.append(f"")
    lines.append(f"📰 <i>{_esc(source)}</i>")
    if published:
        lines.append(f"🕐 {_esc(published)}")
    if summary:
        short = _esc(_strip_html(summary)[:300])
        if len(summary) > 300:
            short += "…"
        lines += ["", short]
    lines += ["", f'🔗 <a href="{link}">Read more</a>']
    return "\n".join(lines)


def _type_badge(type_id: str) -> str:
    badges = {
        "ransomware":   "🔒 Ransomware",
        "phishing":     "🎣 Phishing",
        "apt":          "🕵️ APT",
        "zeroday":      "💣 Zero-day",
        "ddos":         "🌊 DDoS",
        "malware":      "🦠 Malware",
        "supply_chain": "⛓️ Supply Chain",
        "cve":          "📋 CVE",
        "data_breach":  "💾 Data Breach",
        "ics_scada":    "🏭 ICS/SCADA",
    }
    label = badges.get(type_id, type_id)
    return f"<code>{label}</code>"


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _strip_html(text: str) -> str:
    import re
    return re.sub(r"<[^>]+>", "", text).strip()
