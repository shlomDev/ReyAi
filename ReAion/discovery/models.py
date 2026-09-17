from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class PrepDocument:
    name: str
    text: str
    source: str = "local"
    path: str | None = None


@dataclass(frozen=True)
class CalendarInterview:
    title: str
    start: datetime
    end: datetime | None = None
    organizer: str | None = None
    company: str | None = None
    role: str | None = None
    meeting_url: str | None = None
    timezone: str | None = None


@dataclass(frozen=True)
class RecruiterMessage:
    subject: str
    received_at: datetime
    sender: str | None = None
    body: str = ""
    attachments: tuple[PrepDocument, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class InterviewBrief:
    title: str
    company: str | None
    role: str | None
    start: datetime
    meeting_url: str | None
    sources: tuple[str, ...]
    prep_documents: tuple[str, ...]
    recruiter_notes: tuple[str, ...]
    missing: tuple[str, ...]
