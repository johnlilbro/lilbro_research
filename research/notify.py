from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
NOTIFY_DIR = BASE_DIR / "notifications"
NOTIFY_DIR.mkdir(exist_ok=True)


def write_notification(timestamp: str, details: str) -> Path:
    path = NOTIFY_DIR / f"research_cycle_complete_{timestamp}.md"
    path.write_text(details)
    return path
