from datetime import datetime, timezone
from discovery.models import CalendarInterview, PrepDocument, RecruiterMessage
from discovery.prep import build_brief

def test_brief_matches_email_url_and_attachment():
    event = CalendarInterview(
        title="Hardware interview", start=datetime(2026, 9, 20, 10, tzinfo=timezone.utc),
        role="Infrastructure Engineer",
    )
    message = RecruiterMessage(
        subject="Interview preparation", received_at=event.start,
        body="Your interview with Example Corp: https://meet.google.com/abc-defg-hij",
        attachments=(PrepDocument("prep.pdf", "Troubleshooting topics", source="gmail"),),
    )
    brief = build_brief(event, [message])
    assert brief.company == "Example Corp"
    assert brief.meeting_url == "https://meet.google.com/abc-defg-hij"
    assert brief.prep_documents == ("prep.pdf",)
    assert brief.missing == ()

def test_brief_marks_unverified_fields_instead_of_inventing():
    event = CalendarInterview("Interview", datetime(2026, 9, 20, tzinfo=timezone.utc))
    brief = build_brief(event)
    assert brief.company is None
    assert "company" in brief.missing
    assert "role" in brief.missing
    assert "meeting_provider_url" in brief.missing
