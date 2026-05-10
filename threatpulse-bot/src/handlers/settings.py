"""
/settings — opens inline menu to re-run onboarding or tweak preferences.
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.storage import get_profile


async def settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 עדכן הגדרות", callback_data="settings_restart")],
        [InlineKeyboardButton("📊 סטטוס נוכחי",  callback_data="settings_status")],
    ])
    await update.message.reply_text(
        "⚙️ *הגדרות ThreatPulse*\n\nמה תרצה לעדכן?",
        parse_mode="Markdown",
        reply_markup=kb,
    )


async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "settings_restart":
        await query.edit_message_text("שלח /start כדי לעדכן את ההגדרות שלך.")

    elif query.data == "settings_status":
        chat_id = str(update.effective_chat.id)
        profile = get_profile(chat_id)
        if not profile:
            await query.edit_message_text("עדיין לא הגדרת פרופיל. שלח /start.")
            return
        atk = ", ".join(profile.get("attack_types", [])) or "—"
        ctr = ", ".join(profile.get("countries", [])) or "—"
        os_ = ", ".join(profile.get("os", [])) or "—"
        blk = str(len(profile.get("blocked_sources", [])))
        await query.edit_message_text(
            f"📊 *הפרופיל שלך*\n\n"
            f"🔒 התקפות: `{atk}`\n"
            f"🌍 מדינות: `{ctr}`\n"
            f"💻 OS: `{os_}`\n"
            f"🚫 מקורות חסומים: {blk}",
            parse_mode="Markdown",
        )
