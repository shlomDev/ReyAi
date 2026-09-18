import json
from discovery.normalized import load_normalized

def test_load_normalized_export(tmp_path):
    path = tmp_path / "export.json"
    path.write_text(json.dumps({
        "event": {
            "title": "Interview", "start": "2026-09-20T10:00:00Z",
            "company": "Example Corp", "role": "Infrastructure Engineer"
        },
        "messages": [{
            "subject": "Prep", "received_at": "2026-09-18T10:00:00Z",
            "body": "Join https://teams.microsoft.com/l/meetup-join/x",
            "attachments": [{"name": "prep.pdf", "text": "STAR examples"}]
        }]
    }), encoding="utf-8")
    event, messages = load_normalized(path)
    assert event.company == "Example Corp"
    assert messages[0].attachments[0].name == "prep.pdf"

def test_load_normalized_rejects_missing_event(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{}", encoding="utf-8")
    try:
        load_normalized(path)
    except ValueError as exc:
        assert "event object" in str(exc)
    else:
        raise AssertionError("expected ValueError")
