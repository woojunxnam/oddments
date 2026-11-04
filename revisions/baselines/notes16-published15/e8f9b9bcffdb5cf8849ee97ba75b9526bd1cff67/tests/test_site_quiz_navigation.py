from pathlib import Path


def test_quiz_modes_refresh_session_seed_and_keep_shuffle_stable_within_session(root: Path) -> None:
    app = (root / "site" / "app.js").read_text(encoding="utf-8")

    assert 'const requestedSeed = new URLSearchParams(window.location.search).get("seed");' in app
    assert "function createSessionSeed(mode)" in app
    assert "state.sessionSeed = createSessionSeed(mode);" in app
    assert 'if (mode === "quick20") questions = MpjeSessions.createQuick20(questions, state.sessionSeed);' in app
    assert "MpjeShuffle.seededShuffle(questions, state.sessionSeed)" in app
    assert "state.question = MpjeShuffle.shuffleQuestionChoices(canonical, state.sessionSeed);" in app
    seed_function = app.split("function createSessionSeed(mode)", 1)[1].split("function createSessionId", 1)[0]
    assert "toISOString().slice(0, 10)" not in seed_function


def test_previous_question_button_preserves_session_response_state(root: Path) -> None:
    app = (root / "site" / "app.js").read_text(encoding="utf-8")
    html = (root / "site" / "index.html").read_text(encoding="utf-8")

    assert 'id="previous-question"' in html
    assert 'previousQuestion: document.querySelector("#previous-question")' in app
    assert "responses: []" in app
    assert "function saveCurrentResponse()" in app
    assert "const response = state.responses[state.index];" in app
    assert 'elements.previousQuestion.addEventListener("click"' in app
    assert "saveCurrentResponse(); state.index -= 1; renderCurrentQuestion();" in app


def test_quick20_history_and_local_export_controls_are_wired(root: Path) -> None:
    app = (root / "site" / "app.js").read_text(encoding="utf-8")
    html = (root / "site" / "index.html").read_text(encoding="utf-8")

    assert 'data-mode="quick20"' in html
    assert 'id="exam-results"' in html
    assert 'id="history-panel"' in html
    assert 'id="export-study-data"' in html
    assert 'id="import-study-data"' in html
    assert 'src="session.js"' in html
    assert 'src="storage.js"' in html
    assert "MpjeStorage.saveSession(record)" in app
    assert "question_content_hashes" in (root / "site" / "session.js").read_text(encoding="utf-8")
