from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from phase2_realism_v3 import repair_scope
from qa_common import DATA, ROOT, load_json, load_records, question_audit_hash, write_json
from release_context import style_profile_snapshot


OUTPUT_DIR = ROOT / "audits" / "reaudit" / "2026-08-13"
AUDIT_DATE = "2026-08-13"
BATCHES = (("A", 0, 40), ("B", 40, 52))
REVIEW_TYPES = ("LEGAL_VERIFICATION", "REALISM_REVIEW")


def _pending_legal_result(qid: str) -> dict[str, Any]:
    return {
        "Question_ID": qid,
        "Verdict": "KEEP",
        "Severity": "Low",
        "Existing_Answer_Correct": "NOT_ASSESSED",
        "authorities": [],
        "Problem": "PENDING_INDEPENDENT_REAUDIT",
        "Proposed_Answer": "PENDING_INDEPENDENT_REAUDIT",
        "Proposed_Rewrite": "PENDING_INDEPENDENT_REAUDIT",
        "Proposed_Explanation": "PENDING_INDEPENDENT_REAUDIT",
    }


def _pending_realism_result(qid: str) -> dict[str, Any]:
    criteria = {
        "jurisprudence_reasoning": False,
        "practice_plausibility": False,
        "authentic_distractors": False,
        "wording_not_guessable": False,
        "reasoning_not_trivia": False,
        "natural_rule_combination": False,
        "appropriate_drug_context": False,
        "distinct_from_bank": False,
        "not_schedule_flashcard": False,
        "public_style_without_copying": False,
    }
    return {
        "Question_ID": qid,
        "Verdict": "MAJOR_REWRITE",
        "Severity": "High",
        "Realism_Verdict": "FAIL",
        "Reviewed_Date": AUDIT_DATE,
        "Criteria": criteria,
        "Notes": "PENDING_INDEPENDENT_REAUDIT",
    }


def _payload(
    review_type: str,
    batch_name: str,
    questions: dict[str, dict[str, Any]],
    qids: list[str],
) -> dict[str, Any]:
    review_code = "LEGAL" if review_type == "LEGAL_VERIFICATION" else "REALISM"
    payload: dict[str, Any] = {
        "audit_id": f"AUDIT-GPT-PHASE2-V3-{review_code}-REAUDIT-2026-08-13-{batch_name}",
        "auditor": "GPT",
        "audit_date": AUDIT_DATE,
        "audit_scope": "REAUDIT",
        "review_type": review_type,
        "independent": True,
        "audit_status": "STRUCTURAL_TRIAGE_ONLY",
        "question_ids": qids,
        "question_hashes": {qid: question_audit_hash(questions[qid]) for qid in qids},
        "results": [
            _pending_legal_result(qid)
            if review_type == "LEGAL_VERIFICATION"
            else _pending_realism_result(qid)
            for qid in qids
        ],
    }
    if review_type == "REALISM_REVIEW":
        payload["style_profile"] = style_profile_snapshot(
            load_json(DATA / "exam_style" / "mpje_style_profile.json")
        )
    return payload


def export_packages() -> list[Path]:
    scope = sorted(repair_scope())
    if len(scope) != 52:
        raise ValueError(f"expected 52 changed questions, found {len(scope)}")
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    schema = load_json(ROOT / "schemas" / "audit.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    outputs: list[Path] = []
    for review_type in REVIEW_TYPES:
        review_code = "LEGAL" if review_type == "LEGAL_VERIFICATION" else "REALISM"
        for batch_name, start, stop in BATCHES:
            qids = scope[start:stop]
            payload = _payload(review_type, batch_name, questions, qids)
            errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.absolute_path))
            if errors:
                details = "; ".join(error.message for error in errors)
                raise ValueError(f"invalid {review_code} batch {batch_name}: {details}")
            output = OUTPUT_DIR / f"GPT-V3-{review_code}-BATCH-{batch_name}.json"
            write_json(output, payload)
            outputs.append(output)
    covered = {
        review_type: {
            qid
            for path in outputs
            for payload in [load_json(path)]
            if payload["review_type"] == review_type
            for qid in payload["question_ids"]
        }
        for review_type in REVIEW_TYPES
    }
    for review_type, qids in covered.items():
        if qids != set(scope):
            raise ValueError(f"{review_type} packages do not exactly cover the changed scope")
    return outputs


def main() -> int:
    for output in export_packages():
        payload = load_json(output)
        print(f"exported {len(payload['question_ids'])} items to {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
