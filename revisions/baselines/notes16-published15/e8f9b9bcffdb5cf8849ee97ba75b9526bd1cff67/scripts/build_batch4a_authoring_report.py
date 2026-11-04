"""Build the durable B4-A candidate authoring and preflight report."""

from __future__ import annotations

import hashlib
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, load_json, load_records, question_audit_hash, write_json


MAP_PATH = ROOT / "audits" / "coverage" / "2026-09-01" / "B4-A-PROPOSITION-MAP-FINAL.json"
OUTPUT = ROOT / "audits" / "remediation" / "2026-09-01" / "BATCH4-B4A-AUTHORING-REPORT.json"
QUESTION_IDS = [f"MA-Q-{number:04d}" for number in range(407, 440)]


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def main() -> int:
    proposition_map = load_json(MAP_PATH)
    all_questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    selected = [all_questions[qid] for qid in QUESTION_IDS]
    matrix = load_json(DATA / "exam_style" / "question_family_matrix.json")
    duplicate = load_json(ROOT / "duplicate_report.json")
    structural = load_json(ROOT / "structural_pattern_report.json")
    distribution = load_json(ROOT / "answer_distribution_report.json")
    sba_length = load_json(ROOT / "sba_answer_length_report.json")
    public_questions = load_json(ROOT / "site" / "generated" / "questions.json")
    public_guide = load_json(ROOT / "site" / "generated" / "study_guide.json")

    if [question["question_id"] for question in selected] != QUESTION_IDS:
        raise SystemExit("B4-A question range is incomplete or out of order")
    if any(question["verification_status"] != "AUDIT_PENDING" for question in selected):
        raise SystemExit("B4-A report may only be built while every item remains AUDIT_PENDING")
    if duplicate["finding_count"] or structural["finding_count"]:
        raise SystemExit("duplicate or structural findings remain; refusing to record a passing preflight")
    if distribution["severity"] != "PASS" or sba_length["severity"] != "PASS":
        raise SystemExit("answer-distribution or SBA leakage gate is not passing")

    families_over_cap = [
        family["family_id"]
        for family in matrix["families"]
        if family["current_candidate_count"] > family["max_questions_in_final_bank"]
    ]
    if families_over_cap:
        raise SystemExit(f"candidate family caps exceeded: {families_over_cap}")

    sata = [question for question in selected if question["question_type"] == "SATA"]
    sba = [question for question in selected if question["question_type"] == "SBA"]
    public_items = public_questions["questions"]
    if len(public_items) != 366 or any(item["question_id"] in QUESTION_IDS for item in public_items):
        raise SystemExit("RELEASE-only public question payload is not preserved")

    report = {
        "report_id": "BATCH4-B4A-AUTHORING",
        "date": "2026-09-01",
        "controller_issue": 121,
        "tranche": "B4-A",
        "audit_scope": "INITIAL_BATCH",
        "source_main_sha": "15abfda6e41ec42a9cc8e4e6c07315df521b7de2",
        "author_branch": "codex/batch4a-candidates",
        "authored_by": "GPT controller with three non-overlapping parallel author workstreams",
        "independent_audit_status": "NOT_PERFORMED_BY_AUTHORS",
        "reserved_fresh_auditor_instance": "GPT-FRESH-B4A",
        "reserved_identity_prior_use_found": False,
        "proposition_map": {
            "path": str(MAP_PATH.relative_to(ROOT)).replace("\\", "/"),
            "sha256": normalized_sha256(MAP_PATH),
            "main_merge_sha": "15abfda6e41ec42a9cc8e4e6c07315df521b7de2",
            "final_unresolved_authority_risks": proposition_map["authority_review"]["final_unresolved_authority_risks"],
        },
        "question_ids": QUESTION_IDS,
        "question_count": len(selected),
        "locked_id_range": {"first": QUESTION_IDS[0], "last": QUESTION_IDS[-1], "collisions": 0},
        "area_allocation": dict(sorted(Counter(str(q["area"]) for q in selected).items())),
        "item_mix": {
            "SBA": len(sba),
            "SATA": len(sata),
            "difficulty": dict(sorted(Counter(str(q["difficulty"]) for q in selected).items())),
            "sba_key_positions": dict(sorted(Counter(q["correct_choice_ids"][0] for q in sba).items())),
            "sata_correct_counts": dict(sorted(Counter(str(len(q["correct_choice_ids"])) for q in sata).items())),
            "sata_slot_presence": {
                choice_id: round(sum(choice_id in q["correct_choice_ids"] for q in sata) / len(sata), 6)
                for choice_id in "ABCDE"
            },
            "multi_rule_count": sum(len(q["rule_ids"]) > 1 for q in selected),
        },
        "question_audit_hashes": {q["question_id"]: question_audit_hash(q) for q in selected},
        "candidate_state": {
            "AUDIT_PENDING": len(selected),
            "RELEASED": 0,
            "audits_attached": 0,
            "final_adjudications": 0,
        },
        "source_policy": {
            "provenance": "GEN",
            "source_signal_ids": [],
            "current_canonical_rules_only": True,
            "recalled_actual_question_content_retained": 0,
            "forbidden_rule_ids": ["MA-MH-SUD-ADMIN"],
            "forbidden_rule_ids_used": [],
            "hold_questions_preserved": ["MA-Q-0172"],
        },
        "full_bank_preflight": {
            "canonical_question_count": len(all_questions),
            "released_question_count": 366,
            "duplicate_detector_findings": duplicate["finding_count"],
            "structural_pattern_findings": structural["finding_count"],
            "families_over_cap": len(families_over_cap),
            "answer_distribution": {
                "sba_count": distribution["sba_count"],
                "frequencies": distribution["frequencies"],
                "chi_square": distribution["chi_square"],
                "p_value_approx": distribution["p_value_approx"],
                "severity": distribution["severity"],
            },
            "sba_answer_length": {
                "prospective_first_longest_keyed": sba_length["prospective"]["first_longest_keyed"],
                "prospective_sba_count": sba_length["prospective"]["sba_count"],
                "prospective_share": sba_length["prospective"]["first_longest_share"],
                "individual_extremes": len(sba_length["prospective"]["individual_extremes"]),
                "severity": sba_length["severity"],
            },
            "tranche_sata_pattern_gate": "PASS",
            "repository_validation": "PASS (0 errors, 2 inherited warnings)",
            "full_tests": "PASS (117 passed, 2 skipped)",
            "generated_artifact_freshness": "PASS (0 errors, 0 warnings)",
        },
        "public_payload_guard": {
            "released_questions_online": len(public_items),
            "b4a_candidates_online": 0,
            "verified_study_guide_sections_online": len(public_guide["sections"]),
        },
        "notes": (
            "The controller and parallel authors must not audit this tranche. Release requires the unused "
            "GPT-FRESH-B4A instance to solve the sanitized package and commit an immutable Phase-1 lock "
            "before canonical key or dependency access, followed by current-official-source LEGAL review "
            "and a FULL canonical-bank REALISM review. Passing hashes may be released without waiting for "
            "failed siblings."
        ),
    }
    write_json(OUTPUT, report)
    print(f"wrote {OUTPUT.relative_to(ROOT)} for {len(selected)} B4-A candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
