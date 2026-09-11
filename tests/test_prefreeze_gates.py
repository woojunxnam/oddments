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
    assert parent_citations("M.G.L. c. 94C, s. 18(d3/4), read with s. 18(d)") == {"mgl c 94c 18 d"}
    assert parent_citations("no citation here") == set()


def test_one_provision_written_four_ways_reaches_one_key() -> None:
    # The corpus spells the chapter as "M.G.L." or in full and the marker as "s." or "§",
    # and some records keep the chapter in the authority name and the subsection in the
    # section field. Every spelling has to collapse to one key or two rules citing the same
    # provision never register as neighbours -- the miss that cost this batch two audit
    # cycles on SG-CIII-V-REFILL-TRANSFER.
    expected = {"mgl c 94c 20 c"}
    assert parent_citations("M.G.L. c. 94C, s. 20(c)") == expected
    assert parent_citations("M.G.L. c. 94C, § 20(c)") == expected
    assert parent_citations("Massachusetts General Laws c. 94C § 20(c)") == expected
    # A range cites every subsection it spans.
    assert expected <= parent_citations("Massachusetts General Laws c. 94C § 20(a)-(c)")


def test_a_statute_section_is_keyed_by_subsection_family() -> None:
    # A CMR or CFR section addresses one subject, but M.G.L. c. 94C, s. 23 runs from
    # validity through refills, quantity limits and e-prescribing exceptions. Keying the
    # statute at section level would make almost every Massachusetts rule a neighbour of
    # every other, so unrelated subsections must stay apart while a subsection family joins.
    assert parent_citations("M.G.L. c. 94C, s. 23(a)") != parent_citations("M.G.L. c. 94C, §23(d)")
    assert parent_citations("M.G.L. c. 94C, s. 18(d3/4)") == parent_citations("M.G.L. c. 94C, § 18(d1/2)")
    assert parent_citations("M.G.L. c. 94C, § 18(c)") != parent_citations("M.G.L. c. 94C, § 18(d)")


def _unused_authority_rule_ids(rules: dict[str, Any], section: dict[str, Any]) -> set[str]:
    report = analyze_scope_coverage(sections={section["section_id"]: section}, rules=rules)
    return {
        finding["rule_id"]
        for row in report["sections"]
        for finding in row["findings"]
        if finding["code"] == "UNUSED_AUTHORITY"
    }


def test_unused_authority_reads_prose_not_just_citation_numbers() -> None:
    # The guide renders pinpoint citations separately, so the signal has to recognise a
    # provision the prose plainly teaches without quoting its number. Two authority-name
    # shapes have to work: a short specific name, and a name that describes the source
    # rather than the provision, where only the rule's own title says what it is about.
    rules = {
        "SHORT-NAME": _rule("SHORT-NAME", 3, "Prescription transfer", "105 CMR 721.010"),
        "SOURCE-NAME": _rule("SOURCE-NAME", 3, "Prescription transfer", "105 CMR 700.012(C)(8)"),
        "ABSENT": _rule("ABSENT", 3, "Prescription transfer", "247 CMR 9.99"),
    }
    rules["SHORT-NAME"]["authority"][0]["name"] = "Definition of Failover"
    rules["SOURCE-NAME"]["authority"][0]["name"] = "Massachusetts Department of Public Health regulations"
    rules["SOURCE-NAME"]["title"] = "Additional drug designation"
    rules["ABSENT"]["authority"][0]["name"] = "Central fill authorisation"
    rules["ABSENT"]["title"] = "Central fill authorisation"

    taught = _section(
        "SG-TAUGHT",
        ["SHORT-NAME", "SOURCE-NAME", "ABSENT"],
        "A Failover is a Schedule VI document converted to a computer generated facsimile. "
        "A drug the Department designates as an additional drug becomes reportable.",
    )
    # Both provisions the prose teaches stay quiet; the one it never mentions still fires.
    assert _unused_authority_rule_ids(rules, taught) == {"ABSENT"}

    silent = _section("SG-SILENT", ["SHORT-NAME"], "Refills are permitted for six months.")
    assert _unused_authority_rule_ids(rules, silent) == {"SHORT-NAME"}


def test_a_repeated_section_reference_does_not_widen_the_key() -> None:
    # Records name the section twice, once bare in the authority name and once with the
    # subsection: "M.G.L. c.94C §18" + "§18(d), §18(d 1/2)". The bare half must not drag the
    # key back out to "every rule that mentions s. 18".
    assert parent_citations("M.G.L. c.94C §18 §18(d), §18(d 1/2)") == {"mgl c 94c 18 d"}


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


def test_a_published_section_cannot_outlive_a_corrected_rule() -> None:
    """Publication stays pinned to current law even though historical audits do not.

    validate_study_guide_audits no longer treats a moved rule as staling every audit that
    once froze it, because an audit is a record of what was reviewed. The guarantee that
    replaced it runs through the section: a published section's own dependency snapshot
    must match the current rules, and refreshing it moves the section's content hash away
    from the KEEP that published it.
    """
    from qa_common import DATA, dependency_snapshot, load_records
    from study_guide_common import study_guide_content_hash
    from validate_study_guide_audits import validate_study_guide_audits

    report, audits = validate_study_guide_audits()
    assert report.ok

    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    sections = {
        record["section_id"]: record
        for _, record in load_records(DATA / "study_guide" / "sections")
    }
    published = {
        section_id: section
        for section_id, section in sections.items()
        if section["verification_status"] == "VERIFIED"
    }
    # Empty while the guide moves between content models. The mechanism this test guards --
    # that moving a rule stales its dependent sections -- is pinned independently of the
    # corpus by test_rule_hash_change_makes_dependent_sections_stale, so the loop below
    # asserting it over live published sections may legitimately have nothing to iterate.
    for section_id, section in published.items():
        # Every dependency snapshot a published section carries is the current rule.
        for rule_id, snapshot in section["verified_rule_dependencies"].items():
            assert snapshot == dependency_snapshot(rules[rule_id]), section_id
        # And the hash those snapshots feed is the hash its audit gave a KEEP.
        audit = audits[section["independent_audit_id"]]
        result = next(item for item in audit["results"] if item["section_id"] == section_id)
        assert result["disposition"] == "KEEP"
        assert result["section_hash"] == study_guide_content_hash(section)


def test_rules_citing_one_provision_must_point_at_one_page() -> None:
    """A dead authority URL looks exactly like a live one to a presence check.

    MA-CDTM-QUALIFICATIONS pointed at .../Section24B1~2, which 404s, while sibling rules
    on the same statute pointed at .../Section24B%201~2, which loads. Nothing caught it,
    because the validator only asked whether a url field existed. Divergence between rules
    citing the same provision is the signal available without network access.
    """
    from validate_rules import _provision_key, _report_url_divergence, _url_identity
    from qa_common import QAReport

    # The two mass.gov forms of one chapter are equivalent and must not be flagged.
    assert _url_identity("https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download") == \
        _url_identity("https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards")
    assert _url_identity("https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download") == \
        _url_identity("https://www.mass.gov/regulations/105-CMR-70000-implementation-of-mgl-c94c")

    # Subsections of one section share a page, so they are compared together.
    assert _provision_key("M.G.L. c. 112, § 24B1/2(b)") == _provision_key("M.G.L. c. 112, § 24B1/2(c)(5)")
    # "s." and "§" name the same marker.
    assert _provision_key("M.G.L. c. 94C, s. 21A") == _provision_key("M.G.L. c. 94C, § 21A")
    # Different sections stay apart.
    assert _provision_key("M.G.L. c. 94C, s. 18") != _provision_key("M.G.L. c. 94C, s. 21")

    records = [
        (None, {"rule_id": "MAJORITY-A", "authority": [{"section": "M.G.L. c. 112, § 24B1/2(a)", "url": "https://x/Section24B%201~2"}]}),
        (None, {"rule_id": "MAJORITY-B", "authority": [{"section": "M.G.L. c. 112, § 24B1/2(b)", "url": "https://x/Section24B%201~2"}]}),
        (None, {"rule_id": "ODD-ONE", "authority": [{"section": "M.G.L. c. 112, § 24B1/2(c)", "url": "https://x/Section24B1~2"}]}),
    ]
    report = QAReport()
    _report_url_divergence(records, report)
    assert any("ODD-ONE" in warning for warning in report.warnings), report.warnings
    assert not any("MAJORITY" in warning.split("use")[0] for warning in report.warnings)
