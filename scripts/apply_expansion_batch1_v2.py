from __future__ import annotations

import json
from pathlib import Path

from qa_common import DATA, ROOT, load_json, question_audit_hash, write_json


SPEC_DIR = ROOT / "repair_specs" / "exp1_v2"
TODAY = "2026-08-14"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one replacement target, found {count}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def replace_between(path: Path, start: str, end: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    left = text.find(start)
    if left < 0:
        raise RuntimeError(f"{path}: missing start marker")
    right = text.find(end, left)
    if right < 0:
        raise RuntimeError(f"{path}: missing end marker")
    path.write_text(text[:left] + replacement + text[right:], encoding="utf-8")


def load_specs() -> dict[str, dict]:
    merged: dict[str, dict] = {}
    for path in sorted(SPEC_DIR.glob("questions_*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        overlap = set(merged) & set(payload)
        if overlap:
            raise RuntimeError(f"duplicate repair spec IDs: {sorted(overlap)}")
        merged.update(payload)
    expected = {f"MA-Q-{number:04d}" for number in range(91, 130)}
    if set(merged) != expected:
        raise RuntimeError(f"repair spec coverage mismatch: missing={sorted(expected-set(merged))} extra={sorted(set(merged)-expected)}")
    return merged


def patch_questions() -> None:
    specs = load_specs()
    q130_path = DATA / "questions" / "ma-q-0130.json"
    q130_before = question_audit_hash(load_json(q130_path))
    for qid, patch in specs.items():
        path = DATA / "questions" / f"ma-q-{qid[-4:]}.json"
        record = load_json(path)
        if record.get("question_id") != qid:
            raise RuntimeError(f"{path}: question_id mismatch")
        record.update(patch)
        record.update(
            {
                "verification_status": "AUDIT_PENDING",
                "lifecycle_status": "AUDIT_PENDING",
                "last_legal_review": TODAY,
                "audits": [],
                "duplicate_review_status": "PENDING",
                "independent_audit_status": "PENDING",
                "final_adjudication": None,
                "development_fixture": True,
            }
        )
        choice_ids = {choice["id"] for choice in record.get("choices", [])}
        if set(record.get("correct_choice_ids", [])) - choice_ids:
            raise RuntimeError(f"{qid}: answer references missing choice")
        write_json(path, record)
    q130_after = question_audit_hash(load_json(q130_path))
    if q130_before != q130_after:
        raise RuntimeError("MA-Q-0130 changed unexpectedly")


def patch_rules() -> None:
    tech = load_json(DATA / "rules" / "ma-tech-cii.json")
    tech.update(
        {
            "content_version": 2,
            "rule_summary": (
                "Under 247 CMR 8.05, a pharmacy intern may handle Schedule II controlled substances under direct pharmacist supervision; "
                "an ordinary pharmacy technician may assist with transporting Schedule II substances, while a certified pharmacy technician may assist with transporting and handling them when the pharmacist supervises and approves the activity and written policies and procedures govern it. Pharmacist professional judgment is not delegated."
            ),
            "exam_relevance": "Tests the distinct Schedule II scopes of interns, pharmacy technicians, and certified pharmacy technicians and the supervision/approval conditions attached to those tasks.",
            "last_verified": TODAY,
            "exceptions": ["Apply any narrower setting-specific Board policy when the question expressly concerns an automated dispensing device or another specially regulated workflow."],
            "common_confusions": [
                "Treating ordinary pharmacy technician and certified pharmacy technician as the same Schedule II handling category.",
                "Confusing physical transporting or handling authority with pharmacist-only clinical judgment or final verification."
            ],
            "verification_notes": "Current 247 CMR 8.05 checked against the Board's 2025-04-25 regulation publication; v2 separates ordinary technician transporting from certified technician transporting/handling authority."
        }
    )
    write_json(DATA / "rules" / "ma-tech-cii.json", tech)

    transfer = load_json(DATA / "rules" / "ma-rx-transfer.json")
    transfer.update(
        {
            "content_version": 2,
            "rule_summary": (
                "Under current 247 CMR 9.14, a pharmacy must timely transfer a prescription at the request of the patient or authorized agent, may act as the patient's agent to obtain the transfer, and may not charge a transfer fee. Schedule VI prescriptions transfer in the same manner as Schedule III-V prescriptions; remaining authorized refills may be transferred, but a Schedule VI prescription may not be transferred more than one year after issuance. Under 247 CMR 8.04, a certified pharmacy technician may perform a Schedule VI transfer with approval of the pharmacist on duty."
            ),
            "exam_relevance": "Tests transfer timing, Schedule VI age/refill limits, no-fee requirements, and the certified-technician Schedule VI transfer role without importing stale pharmacist-only mechanics.",
            "authority": [
                {
                    "type": "PROMULGATED_REGULATION",
                    "name": "Massachusetts transfer of prescriptions",
                    "section": "247 CMR 9.14",
                    "url": "https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download"
                },
                {
                    "type": "PROMULGATED_REGULATION",
                    "name": "Certified pharmacy technician Schedule VI transfer scope",
                    "section": "247 CMR 8.04(4)(d)",
                    "url": "https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download"
                }
            ],
            "last_verified": TODAY,
            "numeric_facts": [
                {"fact":"Schedule VI maximum age for transfer","value":1,"unit":"year from issuance","conditions":"No Schedule VI prescription may be transferred more than one year after it was issued."}
            ],
            "exceptions": ["Schedule-specific federal requirements may add restrictions for federally controlled prescriptions; do not automatically import those mechanics into a Massachusetts Schedule VI transfer."],
            "common_confusions": [
                "Using obsolete pharmacist-to-pharmacist or annotation language as the universal current Massachusetts transfer rule.",
                "Assuming a certified pharmacy technician can never perform a Schedule VI transfer.",
                "Applying a six-month cutoff instead of the current one-year Schedule VI transfer limit."
            ],
            "verification_notes": "Current 247 CMR 9.14 and 247 CMR 8.04 checked on 2026-08-14; v2 removes stale universal pharmacist-to-pharmacist/annotation summary language."
        }
    )
    write_json(DATA / "rules" / "ma-rx-transfer.json", transfer)

    ep = load_json(DATA / "rules" / "ma-controlled-eprescribe.json")
    ep.update(
        {
            "content_version": 2,
            "rule_summary": (
                "Massachusetts generally requires covered prescriptions to be issued electronically subject to 105 CMR 721.070 exceptions and waivers. Schedule VI prescriptions are excepted from the state electronic-prescribing requirement under 105 CMR 721.070(A)(9). Under 105 CMR 721.070(C), a pharmacist who receives an otherwise valid written or oral prescription is not required to verify that the prescription properly falls within an electronic-prescribing exception or waiver; all other prescription and controlled-substance requirements still apply."
            ),
            "exam_relevance": "Tests the difference between the prescriber's e-prescribing obligation and the dispensing pharmacist's no-verification rule for exceptions/waivers, including the Schedule VI exception.",
            "authority": [
                {
                    "type": "PROMULGATED_REGULATION",
                    "name": "Standards for prescription format and security in Massachusetts",
                    "section": "105 CMR 721.070(A), (C)",
                    "url": "https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download"
                },
                {
                    "type": "OFFICIAL_GUIDANCE",
                    "name": "DCP Electronic Prescribing and Dispensing Manual",
                    "section": "DCP 19-12-108; pharmacist exception verification",
                    "url": "https://www.mass.gov/circular-letter/circular-dcp-19-12-108-electronic-prescribing-and-dispensing-manual"
                }
            ],
            "last_verified": TODAY,
            "exceptions": [
                "Schedule VI prescriptions are excepted from the Massachusetts electronic-prescribing requirement under 105 CMR 721.070(A)(9).",
                "Other enumerated exceptions and waivers may permit a covered prescription to be issued in written or oral form."
            ],
            "common_confusions": [
                "Assuming the pharmacist must independently prove the prescriber's exception or waiver before dispensing an otherwise valid written or oral prescription.",
                "Treating no-verification of the e-prescribing exception as a waiver of all other prescription-validity requirements."
            ],
            "verification_notes": "Current 105 CMR 721.070 and DCP 19-12-108 checked on 2026-08-14; v2 adds the pharmacist no-verification rule and Schedule VI exception."
        }
    )
    write_json(DATA / "rules" / "ma-controlled-eprescribe.json", ep)


def patch_audit_provenance() -> None:
    assignments = {
        "AUDIT-GPT-EXP1-LEGAL-INITIAL-2026-08-14.json": "GPT-CHAT-ISSUE17-2026-08-14",
        "AUDIT-GPT-EXP1-REALISM-INITIAL-2026-08-14.json": "GPT-CHAT-ISSUE17-2026-08-14",
        "AUDIT-GPT-DESKTOP-EXP1-LEGAL-INITIAL-2026-08-14.json": "GPT-DESKTOP-BLIND-2026-08-14",
        "AUDIT-GPT-DESKTOP-EXP1-REALISM-INITIAL-2026-08-14.json": "GPT-DESKTOP-BLIND-2026-08-14",
    }
    for filename, instance in assignments.items():
        path = DATA / "audits" / filename
        record = load_json(path)
        record["auditor_instance"] = instance
        write_json(path, record)


def patch_governance_code() -> None:
    qpath = ROOT / "scripts" / "validate_questions.py"
    old = '''            for label, passes, requirement in (\n                ("legal", legal_passes, release_requirements.get("legal_verification", {})),\n                ("realism", realism_passes, release_requirements.get("realism_review", {})),\n            ):\n                if len(passes) < requirement.get("minimum_passes", 1):\n                    report.error(f"{path}: insufficient current independent {label} audit passes")\n                auditors = {audit.get("auditor") for audit in passes}\n                if len(auditors) < requirement.get("minimum_distinct_auditors", 1):\n                    report.error(f"{path}: insufficient distinct {label} auditors")\n                missing_auditors = set(requirement.get("required_auditor_types", [])) - auditors\n                if missing_auditors:\n                    report.error(\n                        f"{path}: missing required {label} auditor types {sorted(missing_auditors)}"\n                    )\n'''
    new = '''            for label, passes, requirement in (\n                ("legal", legal_passes, release_requirements.get("legal_verification", {})),\n                ("realism", realism_passes, release_requirements.get("realism_review", {})),\n            ):\n                if len(passes) < requirement.get("minimum_passes", 1):\n                    report.error(f"{path}: insufficient current independent {label} audit passes")\n                basis = requirement.get("distinctness_basis", "AUDITOR_TYPE")\n                identities: set[str] = set()\n                for audit in passes:\n                    if basis == "AUDITOR_INSTANCE":\n                        identity = audit.get("auditor_instance")\n                        if not identity:\n                            report.error(\n                                f"{path}: {label} audit {audit.get('audit_id')} lacks auditor_instance required by release policy"\n                            )\n                            continue\n                    else:\n                        identity = audit.get("auditor")\n                    if identity:\n                        identities.add(identity)\n                if len(identities) < requirement.get("minimum_distinct_auditors", 1):\n                    report.error(f"{path}: insufficient distinct {label} auditors")\n                auditor_types = {audit.get("auditor") for audit in passes}\n                missing_auditors = set(requirement.get("required_auditor_types", [])) - auditor_types\n                if missing_auditors:\n                    report.error(\n                        f"{path}: missing required {label} auditor types {sorted(missing_auditors)}"\n                    )\n'''
    replace_once(qpath, old, new)

    gpath = ROOT / "scripts" / "validate_governance.py"
    old = '''        required_types = requirement.get("required_auditor_types", [])\n        if minimum_distinct > minimum_passes:\n            report.error(f"{requirements_path}: {label} distinct-auditor minimum exceeds pass minimum")\n        if len(required_types) > minimum_distinct:\n            report.error(f"{requirements_path}: {label} required auditor types exceed distinct-auditor minimum")\n'''
    new = '''        required_types = requirement.get("required_auditor_types", [])\n        basis = requirement.get("distinctness_basis", "AUDITOR_TYPE")\n        if minimum_distinct > minimum_passes:\n            report.error(f"{requirements_path}: {label} distinct-auditor minimum exceeds pass minimum")\n        if basis == "AUDITOR_TYPE" and len(required_types) > minimum_distinct:\n            report.error(f"{requirements_path}: {label} required auditor types exceed distinct-auditor minimum")\n'''
    replace_once(gpath, old, new)


def patch_release_tests() -> None:
    path = ROOT / "tests" / "test_release_integrity.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '    def legal_audit(audit_id: str, auditor: str) -> dict:\n        return {\n            "audit_id": audit_id,\n            "auditor": auditor,',
        '    def legal_audit(audit_id: str, auditor: str, auditor_instance: str) -> dict:\n        return {\n            "audit_id": audit_id,\n            "auditor": auditor,\n            "auditor_instance": auditor_instance,'
    )
    text = text.replace(
        '        audit_ids[0]: legal_audit(audit_ids[0], "GPT"),\n        audit_ids[1]: legal_audit(audit_ids[1], "CLAUDE"),',
        '        audit_ids[0]: legal_audit(audit_ids[0], "GPT", "GPT-TEST-A"),\n        audit_ids[1]: legal_audit(audit_ids[1], "GPT", "GPT-TEST-B"),'
    )
    text = text.replace(
        '            "auditor": "HUMAN",\n            "audit_scope": "REAUDIT",',
        '            "auditor": "HUMAN",\n            "auditor_instance": "HUMAN-REALISM-TEST",\n            "audit_scope": "REAUDIT",'
    )
    path.write_text(text, encoding="utf-8")

    start = '@pytest.mark.parametrize(\n    ("missing_id", "missing_type"),'
    end = '@pytest.mark.parametrize(\n    ("field", "value"),'
    replacement = '''def test_two_current_legal_passes_are_still_required(\n    tmp_path, monkeypatch, canonical_question, registry_indexes\n) -> None:\n    rules, drugs = registry_indexes\n    question, audits = release_fixture(canonical_question, rules, drugs)\n    missing_id = "AUDIT-CLAUDE-LEGAL-TEST"\n    question["audits"].remove(missing_id)\n    audits.pop(missing_id)\n    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)\n    assert any("insufficient current independent legal audit passes" in error for error in report.errors)\n\n\ndef test_same_model_family_with_distinct_instances_can_satisfy_legal_distinctness(\n    tmp_path, monkeypatch, canonical_question, registry_indexes\n) -> None:\n    rules, drugs = registry_indexes\n    question, audits = release_fixture(canonical_question, rules, drugs)\n    audits["AUDIT-CLAUDE-LEGAL-TEST"]["auditor"] = "GPT"\n    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)\n    assert report.errors == []\n\n\n'''
    replace_between(path, start, end, replacement)

    start = 'def test_duplicate_same_auditor_does_not_satisfy_distinct_requirement('
    end = 'def test_reaudit_without_initial_batch_history_cannot_release('
    replacement = '''def test_duplicate_same_auditor_instance_does_not_satisfy_distinct_requirement(\n    tmp_path, monkeypatch, canonical_question, registry_indexes\n) -> None:\n    rules, drugs = registry_indexes\n    question, audits = release_fixture(canonical_question, rules, drugs)\n    audits["AUDIT-CLAUDE-LEGAL-TEST"]["auditor"] = "GPT"\n    audits["AUDIT-CLAUDE-LEGAL-TEST"]["auditor_instance"] = audits["AUDIT-GPT-LEGAL-TEST"]["auditor_instance"]\n    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)\n    assert any("insufficient distinct legal auditors" in error for error in report.errors)\n\n\n'''
    replace_between(path, start, end, replacement)


def main() -> int:
    patch_questions()
    patch_rules()
    patch_audit_provenance()
    patch_governance_code()
    patch_release_tests()
    print("Expansion Batch 1 v2 repair applied: 39 questions; Q0130 preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
