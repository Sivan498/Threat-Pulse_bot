"""
Storage — persists user profiles and seen-article tracking to JSON files.
"""
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)
_data_dir: Path = None


def init_storage(data_dir: str):
    global _data_dir
    _data_dir = Path(data_dir)
    _data_dir.mkdir(parents=True, exist_ok=True)


def _path(filename: str) -> Path:
    return _data_dir / filename


def _read(path: Path, default) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write(path: Path, data: Any):
    try:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        logger.error(f"Write error {path}: {e}")


# ── User Profiles ────────────────────────────────────────────────────────────

def get_profile(chat_id: str) -> dict | None:
    profiles = _read(_path("profiles.json"), {})
    return profiles.get(str(chat_id))


def save_profile(chat_id: str, profile: dict):
    profiles = _read(_path("profiles.json"), {})
    profiles[str(chat_id)] = profile
    _write(_path("profiles.json"), profiles)


def get_all_profiles() -> dict:
    return _read(_path("profiles.json"), {})


def get_registered_chat_ids() -> list:
    return list(get_all_profiles().keys())


# ── Seen Articles ────────────────────────────────────────────────────────────

def is_seen(article_id: str) -> bool:
    seen = _read(_path("seen.json"), [])
    return article_id in seen


def mark_seen(article_id: str):
    seen = _read(_path("seen.json"), [])
    seen.append(article_id)
    _write(_path("seen.json"), seen[-3000:])  # keep last 3000
