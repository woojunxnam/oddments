"""Reusable freeze and blind-package generation for any authored tranche.

Generalizes the one-off Pre-Batch3 T3 freeze so Batch 3 tranches do not re-implement it.
Given a tranche config it emits, from the exact frozen authoring candidate:

  * a sanitized blind package containing only question ID, type, stem and choices;
  * separate LEGAL and REALISM frozen audit contracts;
  * a clean-freeze manifest with question hashes, file blobs and dependency snapshots;
  * a sealed post-lock dependency reveal;
  * a governance Phase-0 attestation.

All published sha256 values are computed over LF-normalized bytes so they reproduce on
every platform and equal `git show <sha>:<path> | sha256sum`.

    python scripts/freeze_tranche.py --config audits/remediation/2026-08-19/B3A-FREEZE-CONFIG.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, load_json, load_records, question_audit_hash, write_json


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
BLIND_ALLOWED_KEYS = {"question_id", "question_type", "stem", "choices"}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def file_sha256(path: Path) -> str:
    """Hash LF-normalized bytes so the value is platform-independent."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def blob_sha(sha: str, path: str) -> str:
    line = git("ls-tree", sha, "--", path)
    if not line:
        raise SystemExit(f"{path} not found at {sha}")
    return line.split()[2]


def dependency_snapshots(questions: dict) -> dict:
    rules = {r["rule_id"]: r for _, r in load_records(DATA / "rules")}
    drugs = {d["drug_id"]: d for _, d in load_records(DATA / "drugs")}
    blueprint = load_json(DATA / "blueprint.json")
    profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    used_rules, used_drugs = set(), set()
    for question in questions.values():
        used_rules.update(question.get("rule_ids", []))
        used_drugs.update(question.get("drug_ids", []))
    return {
        "rules": {r: {"content_version": rules[r]["content_version"], "content_hash": rules[r]["content_hash"]}
                  for r in sorted(used_rules)},
        "drugs": {d: {"content_version": drugs[d]["content_version"], "content_hash": drugs[d]["content_hash"]}
                  for d in sorted(used_drugs)},
        "blueprint": {"blueprint_id": blueprint["blueprint_id"], "content_version": blueprint["content_version"],
                      "content_hash": blueprint["content_hash"]},
        "style_profile": {"profile_id": profile["profile_id"], "content_version": profile["content_version"],
                          "content_hash": profile["content_hash"]},
    }


def build_contract(review_type: str, cfg: dict, questions: dict, snapshots: dict, hashes: dict, blobs: dict) -> dict:
    contract = {
        "package_type": "FROZEN_AUDIT_CONTRACT",
        "review_type": review_type,
        "audit_date": cfg["freeze_date"],
        "audit_scope": cfg["audit_scope"],
        "auditor": cfg["auditor_type"],
        "auditor_instance": cfg["auditor_instance"],
        "independent": True,
        "audit_status_required": "FULLY_ADJUDICATED",
        "tranche": cfg["tranche"],
        "authorizing_issue": cfg["authorizing_issue"],
        "represented_candidate_branch": cfg["candidate_branch"],
        "represented_candidate_sha": cfg["candidate_sha"],
        "freeze_branch": cfg["freeze_branch"],
        "source_branch": cfg["source_branch"],
        "source_sha": cfg["source_sha"],
        "question_ids": cfg["question_ids"],
        "question_hashes": hashes,
        "question_file_blobs": blobs,
        "dependency_snapshots": snapshots,
        "phase_order": [
            "PHASE_1_BLIND_SOLVE_AND_IMMUTABLE_LOCK",
            "PHASE_2_UNSEAL_CANONICAL_KEYS_AND_DEPENDENCIES",
            f"PHASE_3_{review_type}",
        ],
        "output_record": {
            "path": f"data/audits/{cfg['legal_audit_id'] if review_type == 'LEGAL_VERIFICATION' else cfg['realism_audit_id']}.json",
            "schema": "schemas/audit.schema.json",
            "audit_scope": cfg["audit_scope"],
            "independent": True,
            "audit_status": "FULLY_ADJUDICATED",
        },
    }
    if review_type == "LEGAL_VERIFICATION":
        contract["required_result_fields"] = [
            "Question_ID", "Verdict", "Severity", "Existing_Answer_Correct", "authorities",
            "Problem", "Proposed_Answer", "Proposed_Rewrite", "Proposed_Explanation",
        ]
        contract["authority_requirements"] = {
            "minimum_per_question": 1,
            "each_authority_requires": ["authority", "source_type", "exact_section", "official_url", "law_checked_date"],
            "official_url_scheme": "https",
            "source_policy": "current official primary or official government sources only",
        }
        contract["release_qualifying_result"] = {"Verdict": "KEEP", "Existing_Answer_Correct": "YES"}
    else:
        contract["style_profile"] = {
            "profile_id": snapshots["style_profile"]["profile_id"],
            "content_version": snapshots["style_profile"]["content_version"],
            "content_hash": snapshots["style_profile"]["content_hash"],
        }
        contract["required_result_fields"] = [
            "Question_ID", "Verdict", "Severity", "Realism_Verdict", "Reviewed_Date", "Criteria", "Notes",
        ]
        contract["required_criteria"] = list(REALISM_CRITERIA)
        contract["comparison_scope"] = {
            "scope": "FULL_CANONICAL_BANK",
            "question_directory": "data/questions",
            "expected_record_count_at_candidate": cfg["bank_size_at_candidate"],
            "requirement": (
                "Compare each reviewed item against the entire canonical bank, not a sample and not the "
                "existing duplicate report, and record the closest comparison question IDs in Notes."
            ),
        }
        contract["release_qualifying_result"] = {"Verdict": "KEEP", "Realism_Verdict": "PASS"}
    return contract


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_json(Path(args.config) if Path(args.config).is_absolute() else ROOT / args.config)

    head = git("rev-parse", "HEAD")
    if head != cfg["candidate_sha"]:
        subprocess.check_call(["git", "merge-base", "--is-ancestor", cfg["candidate_sha"], head], cwd=ROOT)
        drift = git("diff", "--name-only", cfg["candidate_sha"], head, "--", "data", "schemas", "site")
        if drift:
            raise SystemExit(f"canonical content drifted from {cfg['candidate_sha']}: {drift.splitlines()}")

    all_questions = {q["question_id"]: q for _, q in load_records(DATA / "questions")}
    questions = {qid: all_questions[qid] for qid in cfg["question_ids"]}
    snapshots = dependency_snapshots(questions)
    hashes = {qid: question_audit_hash(questions[qid]) for qid in cfg["question_ids"]}
    blobs = {qid: blob_sha(cfg["candidate_sha"], f"data/questions/{qid.lower()}.json") for qid in cfg["question_ids"]}

    out = ROOT / cfg["output_dir"]
    prefix = cfg["file_prefix"]
    paths = {
        "blind": out / f"{prefix}-BLIND-QUESTIONS.json",
        "legal": out / f"{prefix}-LEGAL-CONTRACT.json",
        "realism": out / f"{prefix}-REALISM-CONTRACT.json",
        "manifest": out / f"{prefix}-CLEAN-FREEZE-MANIFEST.json",
        "postlock": out / f"{prefix}-POSTLOCK-DEPENDENCIES.json",
        "attestation": out / f"{prefix}-GOVERNANCE-PHASE0-ATTESTATION.json",
    }

    write_json(paths["blind"], {
        "package_type": "BLIND_QUESTION_INPUT",
        "audit_date": cfg["freeze_date"],
        "tranche": cfg["tranche"],
        "authorizing_issue": cfg["authorizing_issue"],
        "auditor_instance_reserved": cfg["auditor_instance"],
        "represented_candidate_branch": cfg["candidate_branch"],
        "represented_candidate_sha": cfg["candidate_sha"],
        "question_ids": cfg["question_ids"],
        "questions": [
            {"question_id": qid, "question_type": questions[qid]["question_type"],
             "stem": questions[qid]["stem"],
             "choices": [{"id": c["id"], "text": c["text"]} for c in questions[qid]["choices"]]}
            for qid in cfg["question_ids"]
        ],
        "instruction": (
            "Solve each item independently from current official authority before reading anything else "
            "in the repository. Record your selected choice IDs and your reasoning, then commit the "
            "Phase-1 lock. Do not open data/questions/, data/rules/, the authoring report, the post-lock "
            "reveal, the generated site payload, the controller ledger, the plan issue or any git history "
            "for these questions before that lock is committed."
        ),
        "content_boundary": (
            "Contains only question ID, type, stem and choices plus non-substantive package identity "
            "metadata. Excludes keyed answers, explanations, choice analysis, rule and drug identifiers, "
            "area, topic, subtopic, difficulty, family, provenance and all author reasoning."
        ),
    })
    write_json(paths["legal"], build_contract("LEGAL_VERIFICATION", cfg, questions, snapshots, hashes, blobs))
    write_json(paths["realism"], build_contract("REALISM_REVIEW", cfg, questions, snapshots, hashes, blobs))
    write_json(paths["manifest"], {
        "manifest_type": f"{cfg['tranche']}_CLEAN_FREEZE",
        "created_date": cfg["freeze_date"],
        "tranche": cfg["tranche"],
        "audit_scope": cfg["audit_scope"],
        "authorizing_issue": cfg["authorizing_issue"],
        "controller_issue": cfg["controller_issue"],
        "source_branch": cfg["source_branch"],
        "source_sha": cfg["source_sha"],
        "represented_candidate_branch": cfg["candidate_branch"],
        "represented_candidate_sha": cfg["candidate_sha"],
        "freeze_branch": cfg["freeze_branch"],
        "auditor_instance_reserved": cfg["auditor_instance"],
        "author_is_not_auditor": True,
        "question_count": len(cfg["question_ids"]),
        "question_ids": cfg["question_ids"],
        "question_hashes": hashes,
        "question_file_blobs": blobs,
        "new_rule_file_blobs": {r: blob_sha(cfg["candidate_sha"], f"data/rules/{r.lower()}.json")
                                for r in sorted(snapshots["rules"])},
        "dependency_snapshots": snapshots,
        "quality_gates_at_freeze": cfg["quality_gates"],
    })
    write_json(paths["postlock"], {
        "package_type": "POSTLOCK_DEPENDENCY_REVEAL",
        "seal_condition": (
            "Do not open this file until the Phase-1 blind lock has been committed and pushed."
        ),
        "tranche": cfg["tranche"],
        "represented_candidate_sha": cfg["candidate_sha"],
        "question_rule_map": {qid: list(questions[qid].get("rule_ids", [])) for qid in cfg["question_ids"]},
        "question_drug_map": {qid: list(questions[qid].get("drug_ids", [])) for qid in cfg["question_ids"]},
        "question_taxonomy": {
            qid: {"area": questions[qid]["area"], "topic": questions[qid]["topic"],
                  "subtopic": questions[qid]["subtopic"], "difficulty": questions[qid]["difficulty"],
                  "family_id": questions[qid]["family_id"]}
            for qid in cfg["question_ids"]
        },
        "dependency_snapshots": snapshots,
        "canonical_paths": {qid: f"data/questions/{qid.lower()}.json" for qid in cfg["question_ids"]},
    })

    # Leakage check before the attestation records the package hashes.
    blind = load_json(paths["blind"])
    blind_text = json.dumps(blind, ensure_ascii=False)
    leaked = []
    for item in blind["questions"]:
        extra = set(item) - BLIND_ALLOWED_KEYS
        if extra:
            leaked.append(f"blind package exposes {sorted(extra)}")
    for qid, question in questions.items():
        if question["explanation"]["core_reasoning"] in blind_text:
            leaked.append(f"{qid}.explanation")
        if question["family_id"] in blind_text:
            leaked.append(f"{qid}.family_id")
        for rule_id in question.get("rule_ids", []):
            if rule_id in blind_text:
                leaked.append(f"{qid}.rule_ids")
    if leaked:
        raise SystemExit(f"blind package leakage: {sorted(set(leaked))}")

    write_json(paths["attestation"], {
        "attestation_type": "GOVERNANCE_PRECERTIFIED_PHASE0",
        "date": cfg["freeze_date"],
        "tranche": cfg["tranche"],
        "audit_scope": cfg["audit_scope"],
        "authorizing_issue": cfg["authorizing_issue"],
        "controller_issue": cfg["controller_issue"],
        "candidate_branch": cfg["candidate_branch"],
        "candidate_sha": cfg["candidate_sha"],
        "freeze_branch": cfg["freeze_branch"],
        "auditor_instance_reserved": cfg["auditor_instance"],
        "question_ids": cfg["question_ids"],
        "question_hashes": hashes,
        "dependency_snapshots": snapshots,
        "package_sha256": {p.relative_to(ROOT).as_posix(): file_sha256(p)
                           for k, p in paths.items() if k != "attestation"},
        "package_git_note": "sha256 values are LF-normalized and equal `git show <sha>:<path> | sha256sum`",
        "quality_gates": cfg["quality_gates"],
        "auditor_phase0_required": False,
        "auditor_start_phase": "PHASE_1_BLIND_SOLVE",
        "independence_statement": (
            f"{cfg['tranche']} was authored by the Claude Code controller session running Issue "
            f"#{cfg['controller_issue']}. That session must not audit it. The audit requires a separate "
            "session whose pre-lock inputs are the sanitized blind package and current official sources "
            "only, recorded under a distinct auditor_instance."
        ),
        "safe_content_statement": (
            "This attestation contains hashes, blob identifiers and dependency metadata only. It contains "
            "no canonical keyed answer, explanation or author reasoning."
        ),
    })

    for key, path in paths.items():
        print(f"wrote {path.relative_to(ROOT).as_posix()}  sha256={file_sha256(path)}")
    print("blind-package leakage check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
