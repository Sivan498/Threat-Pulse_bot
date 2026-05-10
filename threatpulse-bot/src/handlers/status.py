from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import get_profile
from modules.scheduler import last_poll


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    profile = get_profile(chat_id)
    if not profile:
        await update.message.reply_text("לא הגדרת פרופיל עדיין. שלח /start")
        return

    await update.message.reply_text(
        f"🛡️ *ThreatPulse — סטטוס*\n\n"
        f"⏱️ סריקה אחרונה: `{last_poll['time']}`\n"
        f"📬 התראות נשלחו היום: `{last_poll['sent_today']}`\n\n"
        f"הפרופיל שלך:\n"
        f"🔒 `{', '.join(profile.get('attack_types', []))}`\n"
        f"🌍 `{', '.join(profile.get('countries', []))}`\n"
        f"💻 `{', '.join(profile.get('os', []))}`",
        parse_mode="Markdown",
    )
