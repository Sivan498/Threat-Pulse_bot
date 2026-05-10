import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent.parent / ".env")
except ImportError:
    pass


def load_config() -> dict:
    config = {
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN", ""),
        "POLL_INTERVAL":      int(os.getenv("POLL_INTERVAL", "3600")),
        "DATA_DIR":           os.getenv("DATA_DIR", str(Path(__file__).parent.parent.parent / "data")),
        "OTX_API_KEY":        os.getenv("OTX_API_KEY", ""),  # optional free key
    }
    if not config["TELEGRAM_BOT_TOKEN"]:
        raise ValueError("TELEGRAM_BOT_TOKEN not set")
    return config
