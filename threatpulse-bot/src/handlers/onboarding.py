"""
Onboarding conversation — guides the user through 4 setup steps.
Uses multi-select inline keyboards (toggle on/off per item).
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from utils.storage import save_profile, get_profile
from utils.data import ATTACK_TYPES, COUNTRIES, OS_TYPES, SOURCES

logger = logging.getLogger(__name__)

# Conversation states
(
    STATE_ATTACK_TYPES,
    STATE_COUNTRIES,
    STATE_OS_TYPES,
    STATE_BLOCKED_SOURCES,
) = range(4)

# Context keys
_ATK  = "sel_attacks"
_CTR  = "sel_countries"
_OS   = "sel_os"
_BLK  = "sel_blocked"


# ── Helpers ──────────────────────────────────────────────────────────────────

def _toggle(selected: set, item_id: str) -> set:
    selected = set(selected)
    if item_id in selected:
        selected.discard(item_id)
    else:
        selected.add(item_id)
    return selected


def _multi_keyboard(items: list, selected: set,
                    prefix: str, done_label: str = "✅ אישור") -> InlineKeyboardMarkup:
    rows = []
    for item in items:
        tick = "✅ " if item["id"] in selected else "◻️ "
        rows.append([InlineKeyboardButton(
            tick + item["label"],
            callback_data=f"{prefix}:{item['id']}"
        )])
    rows.append([InlineKeyboardButton(done_label, callback_data=f"{prefix}:DONE")])
    return InlineKeyboardMarkup(rows)


def _source_keyboard(selected_blocked: set) -> InlineKeyboardMarkup:
    rows = []
    for src in SOURCES:
        tick = "🚫 " if src["id"] in selected_blocked else "✅ "
        rows.append([InlineKeyboardButton(
            tick + src["name"],
            callback_data=f"blk:{src['id']}"
        )])
    rows.append([InlineKeyboardButton("✅ סיום הגדרות", callback_data="blk:DONE")])
    return InlineKeyboardMarkup(rows)


# ── Step 0: /start ────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = str(update.effective_chat.id)
    existing = get_profile(chat_id)

    # Reset selections
    context.user_data[_ATK] = set(existing.get("attack_types", [])) if existing else set()
    context.user_data[_CTR] = set(existing.get("countries", [])) if existing else set()
    context.user_data[_OS]  = set(existing.get("os", [])) if existing else set()
    context.user_data[_BLK] = set(existing.get("blocked_sources", [])) if existing else set()

    greeting = (
        "👋 *ברוך הבא ל-ThreatPulse Bot!*\n\n"
        "אני אשלח לך התראות אבטחה מותאמות אישית.\n"
        "נגדיר יחד מה מעניין אותך — 4 שלבים קצרים.\n\n"
        "*שלב 1/4 — סוגי התקפות*\n"
        "בחר את הקטגוריות שרלוונטיות אליך:"
    ) if not existing else (
        "⚙️ *עדכון הגדרות*\n\n"
        "*שלב 1/4 — סוגי התקפות*\n"
        "הגדרות קיימות מסומנות — שנה לפי רצונך:"
    )

    kb = _multi_keyboard(
        ATTACK_TYPES,
        context.user_data[_ATK],
        prefix="atk",
        done_label="הבא ›",
    )
    await update.message.reply_text(greeting, parse_mode="Markdown", reply_markup=kb)
    return STATE_ATTACK_TYPES


# ── Step 1: Attack types ──────────────────────────────────────────────────────

async def choose_attack_types(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    _, value = query.data.split(":", 1)

    if value == "DONE":
        if not context.user_data[_ATK]:
            await query.answer("בחר לפחות סוג התקפה אחד ⚠️", show_alert=True)
            return STATE_ATTACK_TYPES

        kb = _multi_keyboard(
            COUNTRIES,
            context.user_data[_CTR],
            prefix="ctr",
            done_label="הבא ›",
        )
        await query.edit_message_text(
            "🌍 *שלב 2/4 — ארצות מושפעות*\n\n"
            "בחר את המדינות/אזורים שרלוונטיים אליך:",
            parse_mode="Markdown",
            reply_markup=kb,
        )
        return STATE_COUNTRIES

    context.user_data[_ATK] = _toggle(context.user_data[_ATK], value)
    kb = _multi_keyboard(ATTACK_TYPES, context.user_data[_ATK], prefix="atk", done_label="הבא ›")
    await query.edit_message_reply_markup(reply_markup=kb)
    return STATE_ATTACK_TYPES


# ── Step 2: Countries ─────────────────────────────────────────────────────────

async def choose_countries(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    _, value = query.data.split(":", 1)

    if value == "DONE":
        if not context.user_data[_CTR]:
            await query.answer("בחר לפחות מדינה אחת ⚠️", show_alert=True)
            return STATE_COUNTRIES

        kb = _multi_keyboard(
            OS_TYPES,
            context.user_data[_OS],
            prefix="os",
            done_label="הבא ›",
        )
        await query.edit_message_text(
            "💻 *שלב 3/4 — מערכות הפעלה*\n\n"
            "על אילו פלטפורמות תרצה להתריע?",
            parse_mode="Markdown",
            reply_markup=kb,
        )
        return STATE_OS_TYPES

    context.user_data[_CTR] = _toggle(context.user_data[_CTR], value)
    kb = _multi_keyboard(COUNTRIES, context.user_data[_CTR], prefix="ctr", done_label="הבא ›")
    await query.edit_message_reply_markup(reply_markup=kb)
    return STATE_COUNTRIES


# ── Step 3: OS ────────────────────────────────────────────────────────────────

async def choose_os(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    _, value = query.data.split(":", 1)

    if value == "DONE":
        if not context.user_data[_OS]:
            await query.answer("בחר לפחות מערכת הפעלה אחת ⚠️", show_alert=True)
            return STATE_OS_TYPES

        await query.edit_message_text(
            "🚫 *שלב 4/4 — מקורות לחסום*\n\n"
            "בחר מקורות שאת ההתראות מהם *לא* תרצה לקבל.\n"
            "מקורות ✅ = פעיל | מקורות 🚫 = חסום",
            parse_mode="Markdown",
            reply_markup=_source_keyboard(context.user_data[_BLK]),
        )
        return STATE_BLOCKED_SOURCES

    context.user_data[_OS] = _toggle(context.user_data[_OS], value)
    kb = _multi_keyboard(OS_TYPES, context.user_data[_OS], prefix="os", done_label="הבא ›")
    await query.edit_message_reply_markup(reply_markup=kb)
    return STATE_OS_TYPES


# ── Step 4: Blocked sources ───────────────────────────────────────────────────

async def choose_blocked_sources(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    _, value = query.data.split(":", 1)

    if value == "DONE":
        await finish_onboarding(update, context)
        return ConversationHandler.END

    context.user_data[_BLK] = _toggle(context.user_data[_BLK], value)
    await query.edit_message_reply_markup(
        reply_markup=_source_keyboard(context.user_data[_BLK])
    )
    return STATE_BLOCKED_SOURCES


# ── Finish ────────────────────────────────────────────────────────────────────

async def finish_onboarding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = str(update.effective_chat.id)

    profile = {
        "chat_id":        chat_id,
        "attack_types":   list(context.user_data[_ATK]),
        "countries":      list(context.user_data[_CTR]),
        "os":             list(context.user_data[_OS]),
        "blocked_sources": list(context.user_data[_BLK]),
    }
    save_profile(chat_id, profile)

    summary_attacks = ", ".join(context.user_data[_ATK]) or "—"
    summary_os      = ", ".join(context.user_data[_OS])  or "—"
    summary_blocked = str(len(context.user_data[_BLK])) + " מקורות חסומים"

    await query.edit_message_text(
        f"✅ *הגדרות נשמרו!*\n\n"
        f"🔒 התקפות: `{summary_attacks}`\n"
        f"💻 פלטפורמות: `{summary_os}`\n"
        f"🚫 {summary_blocked}\n\n"
        f"אני אשלח לך התראות בזמן אמת.\n"
        f"להגדרות חוזרות — /settings\n"
        f"לסטטוס — /status",
        parse_mode="Markdown",
    )
    logger.info(f"User {chat_id} onboarded: {profile}")
