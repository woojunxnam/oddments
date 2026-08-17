from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qa_common import (
    DATA,
    QUESTION_AUDIT_FIELDS,
    dependency_snapshot,
    drug_consequence_rule_ids,
    load_json,
    load_records,
    question_audit_hash,
    semantic_content_hash,
    write_json,
)

CANDIDATE_SHA = "c99161a7f3e50bb95491de98f895795989d22a16"
AUDITOR_INSTANCE = "GPT-FRESH-COV-T1-A"
DATE = "2026-08-17"
OUT = Path("audits/remediation/2026-08-17")

QUESTION_IDS = [
    "MA-Q-0004", "MA-Q-0009", "MA-Q-0013", "MA-Q-0015", "MA-Q-0016",
    "MA-Q-0017", "MA-Q-0020", "MA-Q-0027", "MA-Q-0028", "MA-Q-0030",
    "MA-Q-0032", "MA-Q-0034", "MA-Q-0036", "MA-Q-0040", "MA-Q-0059",
    "MA-Q-0060", "MA-Q-0075", "MA-Q-0076", "MA-Q-0077", "MA-Q-0078",
    "MA-Q-0079", "MA-Q-0080", "MA-Q-0081", "MA-Q-0082", "MA-Q-0083",
    "MA-Q-0084", "MA-Q-0085", "MA-Q-0086", "MA-Q-0087", "MA-Q-0088",
]

REPAIR_IDS = [
    "MA-Q-0009", "MA-Q-0015", "MA-Q-0016", "MA-Q-0017", "MA-Q-0040",
    "MA-Q-0075", "MA-Q-0076", "MA-Q-0078", "MA-Q-0081", "MA-Q-0085",
    "MA-Q-0086", "MA-Q-0087", "MA-Q-0088",
]
KEEP_IDS = sorted(set(QUESTION_IDS) - set(REPAIR_IDS))

LEGAL_CONTRACT = {
    "required_fields": [
        "Question_ID", "Verdict", "Severity", "Existing_Answer_Correct",
        "authorities", "Problem", "Proposed_Answer", "Proposed_Rewrite",
        "Proposed_Explanation",
    ],
    "pass_condition": "Verdict=KEEP and Existing_Answer_Correct=YES for release admission; any other result requires adjudication before release.",
}

REALISM_CRITERIA = [
    "jurisprudence_reasoning", "practice_plausibility", "authentic_distractors",
    "wording_not_guessable", "reasoning_not_trivia", "natural_rule_combination",
    "appropriate_drug_context", "distinct_from_bank", "not_schedule_flashcard",
    "public_style_without_copying",
]


def index(directory: Path, id_field: str) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for _, record in load_records(directory):
        rid = record.get(id_field)
        if rid:
            result[rid] = record
    return result


def canonical_question(q: dict) -> dict:
    return {field: q.get(field) for field in QUESTION_AUDIT_FIELDS}


def dump_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def main() -> int:
    questions = index(DATA / "questions", "question_id")
    rules = index(DATA / "rules", "rule_id")
    drugs = index(DATA / "drugs", "drug_id")

    selected = [questions[qid] for qid in QUESTION_IDS]
    question_hashes = {qid: question_audit_hash(questions[qid]) for qid in QUESTION_IDS}

    direct_rule_ids = sorted({rid for q in selected for rid in q.get("rule_ids", [])})
    drug_ids = sorted({did for q in selected for did in q.get("drug_ids", [])})
    transitive_rule_ids = sorted({rid for did in drug_ids for rid in drug_consequence_rule_ids(drugs[did])})
    all_rule_ids = sorted(set(direct_rule_ids) | set(transitive_rule_ids))

    # Freeze dependency identities and prove stored semantic hashes are internally valid.
    rule_snapshots = {}
    for rid in all_rule_ids:
        record = rules[rid]
        calculated = semantic_content_hash(record, "rule")
        if record.get("content_hash") != calculated:
            raise SystemExit(f"rule semantic hash mismatch: {rid}")
        rule_snapshots[rid] = dependency_snapshot(record)

    drug_snapshots = {}
    for did in drug_ids:
        record = drugs[did]
        calculated = semantic_content_hash(record, "drug")
        if record.get("content_hash") != calculated:
            raise SystemExit(f"drug semantic hash mismatch: {did}")
        drug_snapshots[did] = dependency_snapshot(record)

    style = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    style_calculated = semantic_content_hash(style, "style_profile")
    if style.get("content_hash") != style_calculated:
        raise SystemExit("style semantic hash mismatch")
    style_snapshot = {
        "profile_id": style["profile_id"],
        **dependency_snapshot(style),
    }

    blueprint_path = DATA / "blueprint.json"
    if not blueprint_path.is_file():
        raise SystemExit("expected blueprint at data/blueprint.json")
    blueprint = load_json(blueprint_path)
    blueprint_calculated = semantic_content_hash(blueprint, "blueprint")
    if blueprint.get("content_hash") != blueprint_calculated:
        raise SystemExit("blueprint semantic hash mismatch")
    blueprint_snapshot = {
        "blueprint_id": blueprint["blueprint_id"],
        **dependency_snapshot(blueprint),
    }

    common = {
        "package_type": "FROZEN_AUDIT_INPUT",
        "audit_date": DATE,
        "audit_scope": "INITIAL_BATCH",
        "auditor": "GPT",
        "auditor_instance": AUDITOR_INSTANCE,
        "independent": True,
        "candidate_sha": CANDIDATE_SHA,
        "tranche": "PRE_BATCH3_LEGACY_SALVAGE_T1",
        "question_ids": QUESTION_IDS,
        "repair_ids": REPAIR_IDS,
        "unchanged_editor_keep_ids": KEEP_IDS,
        "question_hashes": question_hashes,
        "questions": [canonical_question(q) for q in selected],
        "dependency_snapshots": {
            "rules": rule_snapshots,
            "drugs": drug_snapshots,
            "blueprint": blueprint_snapshot,
            "style_profile": style_snapshot,
        },
        "independence_note": (
            "Independently solve each question before relying on the keyed answer, explanation, canonical rule summary, "
            "editor review, prior audit conclusion, or lifecycle status. Dependency artifacts may be used mechanically "
            "for frozen hash verification, but current-law decisions must be based on independently researched official sources."
        ),
    }

    legal = {
        **common,
        "review_type": "LEGAL_VERIFICATION",
        "source_policy": "Current official primary/official sources only.",
        "result_contract": LEGAL_CONTRACT,
    }
    realism = {
        **common,
        "review_type": "REALISM_REVIEW",
        "full_bank_comparison_required": True,
        "criteria_required": REALISM_CRITERIA,
        "result_contract": {
            "required_fields": [
                "Question_ID", "Verdict", "Severity", "Realism_Verdict",
                "Reviewed_Date", "Criteria", "Notes",
            ],
            "pass_condition": "All required realism criteria true and Realism_Verdict=PASS.",
        },
    }

    legal_path = OUT / "GPT-A-LEGAL-PRE-BATCH3-LEGACY-SALVAGE-T1.json"
    realism_path = OUT / "GPT-A-REALISM-PRE-BATCH3-LEGACY-SALVAGE-T1.json"
    OUT.mkdir(parents=True, exist_ok=True)
    legal_bytes = dump_bytes(legal)
    realism_bytes = dump_bytes(realism)
    legal_path.write_bytes(legal_bytes)
    realism_path.write_bytes(realism_bytes)

    manifest = {
        "manifest_type": "PRE_BATCH3_LEGACY_SALVAGE_T1_FREEZE",
        "created_date": DATE,
        "candidate_branch": "remediation/pre-batch3-legacy-salvage-t1",
        "candidate_sha": CANDIDATE_SHA,
        "freeze_branch": "freeze/pre-batch3-legacy-salvage-t1",
        "auditor_instance_reserved": AUDITOR_INSTANCE,
        "question_count": len(QUESTION_IDS),
        "question_ids": QUESTION_IDS,
        "repair_count": len(REPAIR_IDS),
        "repair_ids": REPAIR_IDS,
        "editor_keep_count": len(KEEP_IDS),
        "editor_keep_ids": KEEP_IDS,
        "question_hashes": question_hashes,
        "dependency_snapshots": common["dependency_snapshots"],
        "packages": {
            str(legal_path): {"sha256": sha256_bytes(legal_bytes)},
            str(realism_path): {"sha256": sha256_bytes(realism_bytes)},
        },
        "locked_next_step": "Fresh independent LEGAL_VERIFICATION + REALISM_REVIEW of exactly the 30 frozen questions before any release admission.",
    }
    write_json(OUT / "PRE-BATCH3-LEGACY-SALVAGE-T1-FREEZE-MANIFEST.json", manifest)

    print(f"frozen questions: {len(QUESTION_IDS)}")
    print(f"legal package sha256: {manifest['packages'][str(legal_path)]['sha256']}")
    print(f"realism package sha256: {manifest['packages'][str(realism_path)]['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
