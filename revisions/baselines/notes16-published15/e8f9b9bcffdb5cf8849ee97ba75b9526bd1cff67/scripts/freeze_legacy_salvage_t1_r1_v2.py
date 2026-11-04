from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qa_common import (
    DATA,
    dependency_snapshot,
    drug_consequence_rule_ids,
    load_json,
    load_records,
    question_audit_hash,
    semantic_content_hash,
    write_json,
)

CANDIDATE_SHA = "6035cd92939bc094d0077b87d93ef8ac0b784415"
AUDITOR_INSTANCE = "GPT-FRESH-COV-T1-D"
DATE = "2026-08-17"
OUT = Path("audits/remediation/2026-08-17")
FREEZE_BRANCH = "freeze/pre-batch3-legacy-salvage-t1-r1-v2"

QUESTION_IDS = ["MA-Q-0028", "MA-Q-0032", "MA-Q-0036"]

LEGAL_CONTRACT = {
    "required_fields": [
        "Question_ID",
        "Verdict",
        "Severity",
        "Existing_Answer_Correct",
        "authorities",
        "Problem",
        "Proposed_Answer",
        "Proposed_Rewrite",
        "Proposed_Explanation",
    ],
    "pass_condition": "Verdict=KEEP and Existing_Answer_Correct=YES for changed-item admission; any other result requires downstream adjudication.",
}

REALISM_CRITERIA = [
    "jurisprudence_reasoning",
    "practice_plausibility",
    "authentic_distractors",
    "wording_not_guessable",
    "reasoning_not_trivia",
    "natural_rule_combination",
    "appropriate_drug_context",
    "distinct_from_bank",
    "not_schedule_flashcard",
    "public_style_without_copying",
]


def index(directory: Path, id_field: str) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for _, record in load_records(directory):
        rid = record.get(id_field)
        if rid:
            result[rid] = record
    return result


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

    rule_snapshots = {}
    for rid in all_rule_ids:
        record = rules[rid]
        if record.get("content_hash") != semantic_content_hash(record, "rule"):
            raise SystemExit(f"rule semantic hash mismatch: {rid}")
        rule_snapshots[rid] = dependency_snapshot(record)

    drug_snapshots = {}
    for did in drug_ids:
        record = drugs[did]
        if record.get("content_hash") != semantic_content_hash(record, "drug"):
            raise SystemExit(f"drug semantic hash mismatch: {did}")
        drug_snapshots[did] = dependency_snapshot(record)

    style = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    if style.get("content_hash") != semantic_content_hash(style, "style_profile"):
        raise SystemExit("style semantic hash mismatch")
    style_snapshot = {"profile_id": style["profile_id"], **dependency_snapshot(style)}

    blueprint = load_json(DATA / "blueprint.json")
    if blueprint.get("content_hash") != semantic_content_hash(blueprint, "blueprint"):
        raise SystemExit("blueprint semantic hash mismatch")
    blueprint_snapshot = {"blueprint_id": blueprint["blueprint_id"], **dependency_snapshot(blueprint)}

    dependency_snapshots = {
        "rules": rule_snapshots,
        "drugs": drug_snapshots,
        "blueprint": blueprint_snapshot,
        "style_profile": style_snapshot,
    }

    blind = {
        "package_type": "BLIND_QUESTION_INPUT",
        "audit_date": DATE,
        "auditor_instance": AUDITOR_INSTANCE,
        "candidate_sha": CANDIDATE_SHA,
        "question_ids": QUESTION_IDS,
        "questions": [
            {
                "question_id": q["question_id"],
                "question_type": q.get("question_type"),
                "stem": q.get("stem"),
                "choices": q.get("choices"),
            }
            for q in selected
        ],
        "content_boundary": "Intentionally excludes keyed answers, explanations, rule/drug links, family metadata, lifecycle fields, and all prior-review classifications so the auditor can solve independently first.",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    blind_path = OUT / "GPT-D-BLIND-QUESTIONS-PRE-BATCH3-LEGACY-SALVAGE-T1-R1.json"
    blind_bytes = dump_bytes(blind)
    blind_path.write_bytes(blind_bytes)
    blind_sha = sha256_bytes(blind_bytes)

    common = {
        "package_type": "FROZEN_AUDIT_INPUT",
        "audit_date": DATE,
        "audit_scope": "REAUDIT",
        "auditor": "GPT",
        "auditor_instance": AUDITOR_INSTANCE,
        "independent": True,
        "candidate_sha": CANDIDATE_SHA,
        "tranche": "PRE_BATCH3_LEGACY_SALVAGE_T1_R1",
        "question_ids": QUESTION_IDS,
        "question_hashes": question_hashes,
        "dependency_snapshots": dependency_snapshots,
        "blind_question_package": {"path": str(blind_path), "sha256": blind_sha},
        "content_boundary": "No question text, keyed answers, explanations, family metadata, or prior-review classifications are embedded in this contract package. Use the blind question package for independent solving and verify canonical hashes mechanically.",
        "independence_note": "Independently solve all three questions before inspecting keyed answers, explanations, prior review material, repository conclusions, or repair history. Current-law decisions must be based on independently researched official sources.",
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
        "style_profile": style_snapshot,
        "result_contract": {
            "required_fields": [
                "Question_ID",
                "Verdict",
                "Severity",
                "Realism_Verdict",
                "Reviewed_Date",
                "Criteria",
                "Notes",
            ],
            "pass_condition": "All required realism criteria true and Realism_Verdict=PASS.",
        },
    }

    legal_path = OUT / "GPT-D-LEGAL-PRE-BATCH3-LEGACY-SALVAGE-T1-R1.json"
    realism_path = OUT / "GPT-D-REALISM-PRE-BATCH3-LEGACY-SALVAGE-T1-R1.json"
    legal_bytes = dump_bytes(legal)
    realism_bytes = dump_bytes(realism)
    legal_path.write_bytes(legal_bytes)
    realism_path.write_bytes(realism_bytes)

    manifest = {
        "manifest_type": "PRE_BATCH3_LEGACY_SALVAGE_T1_R1_CLEAN_FREEZE_V2",
        "created_date": DATE,
        "candidate_branch": "repair/pre-batch3-legacy-salvage-t1-r1",
        "candidate_sha": CANDIDATE_SHA,
        "freeze_branch": FREEZE_BRANCH,
        "auditor_instance_reserved": AUDITOR_INSTANCE,
        "question_count": len(QUESTION_IDS),
        "question_ids": QUESTION_IDS,
        "question_hashes": question_hashes,
        "dependency_snapshots": dependency_snapshots,
        "blind_question_package": {"path": str(blind_path), "sha256": blind_sha},
        "packages": {
            str(legal_path): {"sha256": sha256_bytes(legal_bytes)},
            str(realism_path): {"sha256": sha256_bytes(realism_bytes)},
        },
        "independence_sanitized": True,
        "supersedes_incomplete_audit_issue": 53,
        "locked_next_step": "Fresh independent REAUDIT LEGAL_VERIFICATION + REALISM_REVIEW of exactly MA-Q-0028, MA-Q-0032, and MA-Q-0036 from scratch before repair admission.",
    }

    manifest_path = OUT / "PRE-BATCH3-LEGACY-SALVAGE-T1-R1-CLEAN-FREEZE-V2-MANIFEST.json"
    write_json(manifest_path, manifest)

    print(f"frozen questions: {len(QUESTION_IDS)}")
    print(f"blind package sha256: {blind_sha}")
    print(f"legal package sha256: {manifest['packages'][str(legal_path)]['sha256']}")
    print(f"realism package sha256: {manifest['packages'][str(realism_path)]['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
