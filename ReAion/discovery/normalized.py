from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import CalendarInterview, PrepDocument, RecruiterMessage


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_normalized(path: str | Path) -> tuple[CalendarInterview, list[RecruiterMessage]]:
    """Load an offline normalized discovery export.

    This is the contract future Google OAuth adapters must produce. It performs
    no network access and rejects malformed or incomplete event records.
    """
    payload: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    event = payload.get("event")
    if not isinstance(event, dict):
        raise ValueError("normalized export must contain an event object")
    for key in ("title", "start"):
        if not event.get(key):
            raise ValueError(f"event missing {key}")
    messages: list[RecruiterMessage] = []
    for raw in payload.get("messages", []):
        if not isinstance(raw, dict) or not raw.get("subject") or not raw.get("received_at"):
            raise ValueError("message requires subject and received_at")
        attachments = tuple(
            PrepDocument(
                name=item["name"], text=item.get("text", ""),
                source=item.get("source", "gmail"), path=item.get("path")
            )
            for item in raw.get("attachments", [])
            if isinstance(item, dict) and item.get("name")
        )
        messages.append(RecruiterMessage(
            subject=raw["subject"], received_at=_dt(raw["received_at"]),
            sender=raw.get("sender"), body=raw.get("body", ""),
            attachments=attachments,
        ))
    return CalendarInterview(
        title=event["title"], start=_dt(event["start"]),
        end=_dt(event["end"]) if event.get("end") else None,
        organizer=event.get("organizer"), company=event.get("company"),
        role=event.get("role"), meeting_url=event.get("meeting_url"),
        timezone=event.get("timezone"),
    ), messages
