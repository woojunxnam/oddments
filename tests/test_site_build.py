from __future__ import annotations

from build_site_data import build_site_payload


def test_release_site_data_excludes_audit_pending_fixtures() -> None:
    payload = build_site_payload(include_fixtures=False)
    assert payload["questions"] == []
    assert payload["meta"]["development_fixture_mode"] is False
    assert payload["meta"]["release_status"] == "NO_RELEASED_QUESTIONS"
    assert "safe_to_memorize" not in payload["meta"]


def test_development_site_data_is_explicitly_unsafe() -> None:
    payload = build_site_payload(include_fixtures=True)
    assert len(payload["questions"]) == 10
    assert payload["meta"]["development_fixture_mode"] is True
    assert payload["meta"]["release_status"] == "DEVELOPMENT_ONLY"
