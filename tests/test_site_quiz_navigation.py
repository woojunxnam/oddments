from pathlib import Path


def test_quiz_modes_refresh_session_seed_and_keep_shuffle_stable_within_session(root: Path) -> None:
    app = (root / "site" / "app.js").read_text(encoding="utf-8")

    assert 'const requestedSeed = new URLSearchParams(window.location.search).get("seed");' in app
    assert "function createSessionSeed(mode)" in app
    assert "state.sessionSeed = createSessionSeed(mode);" in app
    assert 'if (["random", "mock", "drug"].includes(mode))' in app
    assert "questions = MpjeShuffle.seededShuffle(questions, state.sessionSeed);" in app
    assert "state.question = MpjeShuffle.shuffleQuestionChoices(canonical, state.sessionSeed);" in app
    assert "new Date().toISOString().slice(0, 10)" not in app


def test_previous_question_button_preserves_session_response_state(root: Path) -> None:
    app = (root / "site" / "app.js").read_text(encoding="utf-8")
    html = (root / "site" / "index.html").read_text(encoding="utf-8")

    assert 'id="previous-question"' in html
    assert 'previousQuestion: document.querySelector("#previous-question")' in app
    assert "responses: []" in app
    assert "function saveCurrentResponse()" in app
    assert "const response = state.responses[state.index];" in app
    assert 'elements.previousQuestion.addEventListener("click"' in app
    assert "saveCurrentResponse();\n  state.index -= 1;" in app
