"""
Background scheduler — runs the poller at a fixed interval.
"""
import logging
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from modules.poller import run_poll

logger = logging.getLogger(__name__)

last_poll = {
    "time": "Never",
    "sent_today": 0,
}


async def _job(bot, config):
    sent = await run_poll(bot, config)
    last_poll["time"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    last_poll["sent_today"] = last_poll.get("sent_today", 0) + sent


def setup_scheduler(app, config):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        _job,
        trigger=IntervalTrigger(seconds=config["POLL_INTERVAL"]),
        args=[app.bot, config],
        id="main_poll",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(f"Scheduler started — polling every {config['POLL_INTERVAL']}s")
