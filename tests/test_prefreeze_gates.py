"""The two pre-freeze drafting gates.

Both were built from failure modes that independent auditors actually raised, so the
tests pin the shapes those auditors found rather than the current contents of the bank:

  scope coverage   Every Study Guide section audited so far failed on a controlling
                   provision missing from inside its own declared scope.
  answer cues      MA-Q-0426 failed wording_not_guessable twice, the second time because
                   the key was the only option carrying a prohibitive direction.

Detection is tested on synthetic records so the assertions stay true as content moves.
The live checks assert only structural invariants.
"""

from __future__ import annotations

from typing import Any

from check_answer_cue_patterns import analyze_answer_cues, answer_cue_report, option_polarity
from check_study_guide_scope_coverage import (
    analyze_scope_coverage,
    parent_citations,
    scope_coverage_report,
)
from qa_common import DATA, load_records


def _rule(rule_id: str, area: int, topic: str, section: str, summary: str = "Rule text.") -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "area": area,
        "topic": topic,
        "subtopic": "sub",
        "status": "CURRENT",
        "verification_status": "PRIMARY_VERIFIED",
        "rule_summary": summary,
        "authority": [{"section": section, "url": "https://example.invalid", "name": "n", "type": "STATUTE"}],
    }


def _section(section_id: str, rule_ids: list[str], prose: str, verified: bool = False) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "areas": [3],
        "topic": "Prescription transfer",
        "subtopic": "sub",
        "title": section_id,
        "learning_objectives": [],
        "rule_ids": rule_ids,
        "quick_review": [{"text": prose, "rule_ids": rule_ids}],
        "decision_logic": [],
        "ma_vs_federal": [],
        "exceptions": [],
        "timing_deadlines": [],
        "forms_records": [],
        "role_duties": [],
        "common_traps": [],
        "drug_examples": [],
        "verification_status": "VERIFIED" if verified else "AUDIT_PENDING",
    }


def _sba(question_id: str, choices: list[tuple[str, str]], key: str, rule_ids: list[str],
         released: bool = False) -> dict[str, Any]:
    return {
        "question_id": question_id,
        "question_type": "SBA",
        "choices": [{"id": cid, "text": text} for cid, text in choices],
        "correct_choice_ids": [key],
        "rule_ids": rule_ids,
        "lifecycle_status": "RELEASED" if released else "AUDIT_PENDING",
    }


def test_parent_citations_strips_pinpoints() -> None:
    assert parent_citations("247 CMR 9.04(13)") == parent_citations("247 CMR 9.04(12)")
    assert parent_citations("21 CFR 1306.13(b)(1)-(b)(2)") == parent_citations("21 CFR 1306.13(a)")
    assert parent_citations("M.G.L. c. 94C, s. 18(d3/4), read with s. 18(d)") == {"mgl c 94c s 18"}
    assert parent_citations("no citation here") == set()


def test_scope_gate_finds_the_shapes_auditors_raised() -> None:
    rules = {
        "CITED": _rule("CITED", 3, "Prescription transfer", "247 CMR 9.14(4)(c)"),
        # Same narrow topic as a dependency, never cited: the 21 CFR 1306.08(e) shape.
        "TOPIC-SIBLING": _rule("TOPIC-SIBLING", 3, "Prescription transfer", "21 CFR 1306.08(e)"),
        # Same parent provision as a dependency: the 247 CMR 9.04(12) beside 9.04(13) shape.
        "AUTH-SIBLING": _rule("AUTH-SIBLING", 3, "Prescription validity", "247 CMR 9.14(2)"),
        # Different area entirely, so out of the section's declared scope.
        "OUT-OF-SCOPE": _rule("OUT-OF-SCOPE", 1, "Licensure", "247 CMR 3.01"),
    }
    sections = {"SG-T": _section("SG-T", ["CITED"], "The rule in 247 CMR 9.14 applies.")}

    findings = analyze_scope_coverage(sections, rules)["sections"][0]["findings"]
    by_rule = {finding["rule_id"]: finding for finding in findings}

    assert by_rule["TOPIC-SIBLING"]["code"] == "TOPIC_NEIGHBOUR"
    assert by_rule["TOPIC-SIBLING"]["strength"] == "MEDIUM"
    assert by_rule["AUTH-SIBLING"]["code"] == "AUTHORITY_NEIGHBOUR"
    assert by_rule["AUTH-SIBLING"]["strength"] == "HIGH"
    assert "OUT-OF-SCOPE" not in by_rule


def test_scope_gate_flags_an_authority_the_prose_never_uses() -> None:
    rules = {
        "TWO-AUTHORITIES": {
            **_rule("TWO-AUTHORITIES", 3, "Prescription transfer", "247 CMR 9.14"),
            "authority": [
                {"section": "247 CMR 9.14", "url": "https://x.invalid", "name": "n", "type": "STATUTE"},
                {"section": "247 CMR 8.04(4)(d)", "url": "https://x.invalid", "name": "n", "type": "STATUTE"},
            ],
        }
    }
    sections = {"SG-T": _section("SG-T", ["TWO-AUTHORITIES"], "Transfers follow 247 CMR 9.14.")}

    findings = analyze_scope_coverage(sections, rules)["sections"][0]["findings"]
    unused = [f for f in findings if f["code"] == "UNUSED_AUTHORITY"]
    assert [f["authority"] for f in unused] == [["247 CMR 8.04(4)(d)"]]
    assert unused[0]["strength"] == "HIGH"


def test_scope_gate_stays_quiet_on_a_published_section() -> None:
    rules = {
        "CITED": _rule("CITED", 3, "Prescription transfer", "247 CMR 9.14"),
        "TOPIC-SIBLING": _rule("TOPIC-SIBLING", 3, "Prescription transfer", "21 CFR 1306.08(e)"),
    }
    published = {"SG-T": _section("SG-T", ["CITED"], "247 CMR 9.14 applies.", verified=True)}
    pending = {"SG-T": _section("SG-T", ["CITED"], "247 CMR 9.14 applies.", verified=False)}

    assert analyze_scope_coverage(published, rules)["actionable_count"] > 0
    # The signal is still computed, but a section that already survived a fresh auditor
    # at its exact hash is not re-litigated on every validate_all run.
    assert scope_coverage_report(analyze_scope_coverage(published, rules)).warnings == []
    assert scope_coverage_report(analyze_scope_coverage(pending, rules)).warnings != []


def test_option_polarity_reads_direction_not_sentiment() -> None:
    assert option_polarity("The protocol is impermissible, because it circumvents the limit.") == "PROHIBITIVE"
    assert option_polarity("The workflow is permissible because the step was documented.") == "PERMISSIVE"
    assert option_polarity("The patient rather than the pharmacist is the administering party.") == "NEUTRAL"


def test_answer_cue_gate_catches_the_lone_dissenting_key() -> None:
    """The MA-Q-0426 shape: one prohibitive key against options that validate or merely excuse.

    Two of the four distractors read as neutral rather than permissive, which is why the
    gate must key on 'no distractor shares the key's direction' rather than on every
    distractor stating the opposite.
    """
    question = _sba(
        "MA-Q-9001",
        [
            ("A", "The formal label controls, so no administration restriction is engaged."),
            ("B", "The patient rather than the pharmacist is the administering party."),
            ("C", "The protocol is impermissible, because the sequence circumvents the restriction."),
            ("D", "A valid prescription authorizes the pharmacist to administer the medication."),
            ("E", "Responsibility rests with whoever designed the protocol."),
        ],
        key="C",
        rule_ids=[],
    )
    findings = analyze_answer_cues({"MA-Q-9001": question}, {})["findings"]
    assert [f["code"] for f in findings] == ["POLARITY_SINGLETON"]

    balanced = _sba(
        "MA-Q-9002",
        [
            ("A", "The pharmacist may not dispense without the notation."),
            ("B", "The pharmacist is prohibited from transferring the prescription twice."),
            ("C", "The protocol is impermissible, because the sequence circumvents the restriction."),
            ("D", "A valid prescription authorizes the pharmacist to administer the medication."),
            ("E", "Responsibility rests with whoever designed the protocol."),
        ],
        key="C",
        rule_ids=[],
    )
    assert analyze_answer_cues({"MA-Q-9002": balanced}, {})["findings"] == []


def test_answer_cue_gate_stays_quiet_on_released_items() -> None:
    choices = [
        ("A", "The formal label controls, so no administration restriction is engaged."),
        ("B", "The patient rather than the pharmacist is the administering party."),
        ("C", "The protocol is impermissible, because the sequence circumvents the restriction."),
        ("D", "A valid prescription authorizes the pharmacist to administer the medication."),
        ("E", "Responsibility rests with whoever designed the protocol."),
    ]
    released = {"MA-Q-9003": _sba("MA-Q-9003", choices, "C", [], released=True)}
    pending = {"MA-Q-9004": _sba("MA-Q-9004", choices, "C", [], released=False)}

    assert answer_cue_report(analyze_answer_cues(released, {}), questions=released).warnings == []
    assert answer_cue_report(analyze_answer_cues(pending, {}), questions=pending).warnings != []


def test_gates_run_clean_against_the_live_bank() -> None:
    sections = {record["section_id"]: record for _, record in load_records(DATA / "study_guide" / "sections")}
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}

    scope = analyze_scope_coverage()
    assert {row["section_id"] for row in scope["sections"]} == set(sections)
    assert scope["actionable_count"] <= scope["finding_count"]
    for row in scope["sections"]:
        for finding in row["findings"]:
            assert finding["strength"] in {"HIGH", "MEDIUM", "LOW"}

    cues = analyze_answer_cues()
    assert cues["sba_count"] > 0
    for finding in cues["findings"]:
        assert finding["question_id"] in questions
        assert finding["code"] in {"POLARITY_SINGLETON", "KEY_RULE_ECHO"}
    # A drafting gate that fires on a large share of an audited bank is measuring noise.
    assert cues["flagged_question_count"] <= cues["sba_count"] * 0.10
