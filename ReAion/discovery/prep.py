from __future__ import annotations

import re
from .models import CalendarInterview, InterviewBrief, PrepDocument, RecruiterMessage

_MEETING_HOSTS = ("meet.google.com", "teams.microsoft.com", "teams.live.com",
                  "zoom.us", "webex.com", "app.chime.aws")

def _first_url(text: str) -> str | None:
    match = re.search(r"https?://[^\s<>]+", text or "")
    return match.group(0).rstrip(").,") if match else None

def _company(event: CalendarInterview, messages: list[RecruiterMessage]) -> str | None:
    if event.company:
        return event.company
    for message in messages:
        match = re.search(r"\b(?:at|with|from)\s+([A-Z][\w&.-]+(?:\s+[A-Z][\w&.-]+)?)", message.body)
        if match:
            return match.group(1)
    return None

def build_brief(event: CalendarInterview, messages: list[RecruiterMessage] | None = None,
                documents: list[PrepDocument] | None = None) -> InterviewBrief:
    """Build a deterministic, credential-free brief from normalized inputs.

    OAuth adapters deliberately live outside this module. No email/calendar access,
    secrets, or attachments are fetched here.
    """
    messages = messages or []
    documents = documents or [doc for message in messages for doc in message.attachments]
    notes = tuple(filter(None, (message.body.strip()[:500] for message in messages)))
    sources = ["calendar"]
    if messages:
        sources.append("recruiter_email")
    if documents:
        sources.append("prep_attachments")
    url = event.meeting_url or next((_first_url(message.body) for message in messages if _first_url(message.body)), None)
    missing = []
    if not event.company and not _company(event, messages):
        missing.append("company")
    if not event.role:
        missing.append("role")
    if not url or not any(host in url.lower() for host in _MEETING_HOSTS):
        missing.append("meeting_provider_url")
    return InterviewBrief(
        title=event.title, company=_company(event, messages), role=event.role,
        start=event.start, meeting_url=url, sources=tuple(sources),
        prep_documents=tuple(doc.name for doc in documents),
        recruiter_notes=notes, missing=tuple(missing),
    )
