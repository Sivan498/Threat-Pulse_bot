"""
ThreatPulse Bot — Threat Intel Feeder for Security Analysts
Onboards users through a guided setup, then sends filtered alerts.
"""
import logging
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters
)
from handlers.onboarding import (
    start, choose_attack_types, choose_countries,
    choose_os, choose_blocked_sources, finish_onboarding,
    STATE_ATTACK_TYPES, STATE_COUNTRIES, STATE_OS_TYPES, STATE_BLOCKED_SOURCES,
)
from handlers.settings import settings_menu, settings_callback
from handlers.status import status_command
from modules.scheduler import setup_scheduler
from utils.config import load_config
from utils.storage import init_storage

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    config = load_config()
    init_storage(config["DATA_DIR"])

    app = Application.builder().token(config["TELEGRAM_BOT_TOKEN"]).build()
    app.bot_data["config"] = config

    # Onboarding conversation flow
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            STATE_ATTACK_TYPES:     [CallbackQueryHandler(choose_attack_types)],
            STATE_COUNTRIES:        [CallbackQueryHandler(choose_countries)],
            STATE_OS_TYPES:         [CallbackQueryHandler(choose_os)],
            STATE_BLOCKED_SOURCES:  [CallbackQueryHandler(choose_blocked_sources)],
        },
        fallbacks=[CommandHandler("start", start)],
        per_message=False,
    )
    app.add_handler(conv)

    # Settings & status (available after onboarding)
    app.add_handler(CommandHandler("settings", settings_menu))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CallbackQueryHandler(settings_callback, pattern="^settings_"))

    setup_scheduler(app, config)

    logger.info("🛡️  ThreatPulse Bot is running.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
