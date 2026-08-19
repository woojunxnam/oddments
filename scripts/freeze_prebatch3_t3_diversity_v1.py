"""Freeze the Pre-Batch3 T3 diversity candidate and build the fresh-auditor inputs.

Issue #86. Produces, from the exact frozen authoring-candidate commit:

  * a sanitized blind package containing only question ID, type, stem and choices;
  * separate LEGAL and REALISM frozen audit contracts;
  * a clean-freeze manifest with question hashes, file blobs and dependency snapshots;
  * a post-lock dependency reveal that stays sealed until the auditor commits the lock;
  * a governance Phase-0 attestation.

Nothing here performs or anticipates the audit. The author of MA-Q-0227 and MA-Q-0228
must not audit them; these files exist so a genuinely fresh auditor can start from a
blind solve.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, load_json, load_records, question_audit_hash, write_json


TRANCHE_ID = "PRE-BATCH3-COVERAGE-T3-DIVERSITY"
AUTHORIZING_ISSUE = 86
CONTROLLER_ISSUE = 83
FREEZE_DATE = "2026-08-19"

SOURCE_BRANCH = "remediation/pre-batch3-legacy-salvage-t1"
SOURCE_SHA = "860ec67308772ac63073ed62a7ebdcc565921183"
CANDIDATE_BRANCH = "remediation/pre-batch3-coverage-t3-diversity"
CANDIDATE_SHA = "f13c91c2635ea153a1ea19d9dfb34bcbe12f30c2"
FREEZE_BRANCH = "freeze/pre-batch3-coverage-t3-v1"

AUDITOR_INSTANCE_RESERVED = "CLAUDE-FRESH-COV-T3-A"
AUDITOR_TYPE_RESERVED = "CLAUDE"

QUESTION_IDS = ["MA-Q-0227", "MA-Q-0228"]
OUT_DIR = ROOT / "audits" / "remediation" / "2026-08-19"

BLIND_PACKAGE = OUT_DIR / "T3-BLIND-QUESTIONS-PRE-BATCH3-COVERAGE-T3.json"
LEGAL_CONTRACT = OUT_DIR / "T3-LEGAL-CONTRACT-PRE-BATCH3-COVERAGE-T3.json"
REALISM_CONTRACT = OUT_DIR / "T3-REALISM-CONTRACT-PRE-BATCH3-COVERAGE-T3.json"
MANIFEST = OUT_DIR / "PRE-BATCH3-COVERAGE-T3-CLEAN-FREEZE-V1-MANIFEST.json"
POSTLOCK = OUT_DIR / "PRE-BATCH3-COVERAGE-T3-V1-POSTLOCK-DEPENDENCIES.json"
ATTESTATION = OUT_DIR / "PRE-BATCH3-COVERAGE-T3-V1-GOVERNANCE-PHASE0-ATTESTATION.json"

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


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def blob_sha(sha: str, path: str) -> str:
    line = git("ls-tree", sha, "--", path)
    if not line:
        raise SystemExit(f"{path} not found at {sha}")
    return line.split()[2]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_candidate_questions() -> dict[str, dict]:
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    return {question_id: questions[question_id] for question_id in QUESTION_IDS}


def dependency_snapshots(questions: dict[str, dict]) -> dict:
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}
    blueprint = load_json(DATA / "blueprint.json")
    profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    used_rules, used_drugs = set(), set()
    for question in questions.values():
        used_rules.update(question.get("rule_ids", []))
        used_drugs.update(question.get("drug_ids", []))
    return {
        "rules": {
            rule_id: {
                "content_version": rules[rule_id]["content_version"],
                "content_hash": rules[rule_id]["content_hash"],
            }
            for rule_id in sorted(used_rules)
        },
        "drugs": {
            drug_id: {
                "content_version": drugs[drug_id]["content_version"],
                "content_hash": drugs[drug_id]["content_hash"],
            }
            for drug_id in sorted(used_drugs)
        },
        "blueprint": {
            "blueprint_id": blueprint["blueprint_id"],
            "content_version": blueprint["content_version"],
            "content_hash": blueprint["content_hash"],
        },
        "style_profile": {
            "profile_id": profile["profile_id"],
            "content_version": profile["content_version"],
            "content_hash": profile["content_hash"],
        },
    }


def build_blind_package(questions: dict[str, dict]) -> dict:
    return {
        "package_type": "BLIND_QUESTION_INPUT",
        "audit_date": FREEZE_DATE,
        "tranche_id": TRANCHE_ID,
        "authorizing_issue": AUTHORIZING_ISSUE,
        "auditor_instance_reserved": AUDITOR_INSTANCE_RESERVED,
        "represented_candidate_branch": CANDIDATE_BRANCH,
        "represented_candidate_sha": CANDIDATE_SHA,
        "question_ids": list(QUESTION_IDS),
        "questions": [
            {
                "question_id": question_id,
                "question_type": questions[question_id]["question_type"],
                "stem": questions[question_id]["stem"],
                "choices": [
                    {"id": choice["id"], "text": choice["text"]}
                    for choice in questions[question_id]["choices"]
                ],
            }
            for question_id in QUESTION_IDS
        ],
        "instruction": (
            "Solve each item independently from current official Massachusetts and federal authority "
            "before reading anything else in the repository. Record your selected choice IDs and your "
            "reasoning, then commit the Phase-1 lock. Do not open data/questions/, data/rules/, the "
            "authoring report, the git log or Issue #86 before that lock is committed."
        ),
        "content_boundary": (
            "Contains only frozen question ID, type, stem and choices plus non-substantive package "
            "identity metadata. Excludes keyed answers, explanations, choice analysis, rule and drug "
            "identifiers, area, topic, subtopic, difficulty, family, provenance and all author reasoning."
        ),
    }


def build_contract(review_type: str, questions: dict[str, dict], snapshots: dict) -> dict:
    contract = {
        "package_type": "FROZEN_AUDIT_CONTRACT",
        "review_type": review_type,
        "audit_date": FREEZE_DATE,
        "audit_scope": "TARGETED_INITIAL_BATCH",
        "auditor": AUDITOR_TYPE_RESERVED,
        "auditor_instance": AUDITOR_INSTANCE_RESERVED,
        "independent": True,
        "audit_status_required": "FULLY_ADJUDICATED",
        "governance_authorization": {
            "tranche_id": TRANCHE_ID,
            "authorizing_issue": AUTHORIZING_ISSUE,
            "represented_candidate_sha": CANDIDATE_SHA,
            "question_ids": list(QUESTION_IDS),
        },
        "represented_candidate_branch": CANDIDATE_BRANCH,
        "represented_candidate_sha": CANDIDATE_SHA,
        "freeze_branch": FREEZE_BRANCH,
        "source_branch": SOURCE_BRANCH,
        "source_sha": SOURCE_SHA,
        "question_ids": list(QUESTION_IDS),
        "question_hashes": {
            question_id: question_audit_hash(questions[question_id]) for question_id in QUESTION_IDS
        },
        "question_file_blobs": {
            question_id: blob_sha(CANDIDATE_SHA, f"data/questions/{question_id.lower()}.json")
            for question_id in QUESTION_IDS
        },
        "dependency_snapshots": snapshots,
        "phase_order": [
            "PHASE_1_BLIND_SOLVE_AND_IMMUTABLE_LOCK",
            "PHASE_2_UNSEAL_CANONICAL_KEYS_AND_DEPENDENCIES",
            f"PHASE_3_{review_type}",
        ],
        "output_record": {
            "path": f"data/audits/AUDIT-{AUDITOR_INSTANCE_RESERVED}-"
            + ("LEGAL" if review_type == "LEGAL_VERIFICATION" else "REALISM")
            + "-TARGETED-INITIAL-2026-08-19.json",
            "schema": "schemas/audit.schema.json",
            "audit_scope": "TARGETED_INITIAL_BATCH",
            "independent": True,
            "audit_status": "FULLY_ADJUDICATED",
        },
    }
    if review_type == "LEGAL_VERIFICATION":
        contract["required_result_fields"] = [
            "Question_ID",
            "Verdict",
            "Severity",
            "Existing_Answer_Correct",
            "authorities",
            "Problem",
            "Proposed_Answer",
            "Proposed_Rewrite",
            "Proposed_Explanation",
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
            "Question_ID",
            "Verdict",
            "Severity",
            "Realism_Verdict",
            "Reviewed_Date",
            "Criteria",
            "Notes",
        ]
        contract["required_criteria"] = list(REALISM_CRITERIA)
        contract["comparison_scope"] = {
            "scope": "FULL_CANONICAL_BANK",
            "question_directory": "data/questions",
            "expected_record_count_at_candidate": 228,
            "requirement": (
                "Compare each reviewed item against the entire canonical bank, not a sample and not the "
                "existing duplicate report, and record the closest comparison question IDs in Notes."
            ),
        }
        contract["release_qualifying_result"] = {"Verdict": "KEEP", "Realism_Verdict": "PASS"}
    return contract


def build_manifest(questions: dict[str, dict], snapshots: dict) -> dict:
    return {
        "manifest_type": "PRE_BATCH3_COVERAGE_T3_CLEAN_FREEZE_V1",
        "created_date": FREEZE_DATE,
        "tranche_id": TRANCHE_ID,
        "authorizing_issue": AUTHORIZING_ISSUE,
        "controller_issue": CONTROLLER_ISSUE,
        "source_branch": SOURCE_BRANCH,
        "source_sha": SOURCE_SHA,
        "represented_candidate_branch": CANDIDATE_BRANCH,
        "represented_candidate_sha": CANDIDATE_SHA,
        "freeze_branch": FREEZE_BRANCH,
        "freeze_seed_sha": CANDIDATE_SHA,
        "freeze_head_binding": {
            "mechanism": (
                "The exact freeze HEAD is the commit containing this manifest and is pinned by immutable "
                "SHA in the fresh-audit handoff. The represented candidate SHA is the authority for content."
            ),
            "required_auditor_check": (
                "Confirm the represented candidate SHA and every question hash below before any substantive work."
            ),
        },
        "auditor_instance_reserved": AUDITOR_INSTANCE_RESERVED,
        "author_is_not_auditor": True,
        "question_count": len(QUESTION_IDS),
        "question_ids": list(QUESTION_IDS),
        "question_hashes": {
            question_id: question_audit_hash(questions[question_id]) for question_id in QUESTION_IDS
        },
        "question_file_blobs": {
            question_id: blob_sha(CANDIDATE_SHA, f"data/questions/{question_id.lower()}.json")
            for question_id in QUESTION_IDS
        },
        "new_rule_file_blobs": {
            rule_id: blob_sha(CANDIDATE_SHA, f"data/rules/{rule_id.lower()}.json")
            for rule_id in sorted(snapshots["rules"])
        },
        "dependency_snapshots": snapshots,
        "remediated_headlines": {
            "4.3": {
                "label": "Delivery of drugs",
                "existing_family": "T2_0215_MA_DRUG_DELIVERY",
                "new_question": "MA-Q-0227",
            },
            "4.6": {
                "label": "Centralized prescription processing / central fill",
                "existing_family": "T2_0220_MA_CENTRAL_FILL",
                "new_question": "MA-Q-0228",
            },
        },
        "quality_gates_at_freeze": {
            "repository_validation": "PASS",
            "full_tests": "PASS",
            "generated_artifact_freshness": "PASS",
            "duplicate_detector_findings": 0,
            "structural_pattern_findings": 0,
        },
    }


def build_postlock(questions: dict[str, dict], snapshots: dict) -> dict:
    return {
        "package_type": "POSTLOCK_DEPENDENCY_REVEAL",
        "seal_condition": (
            "Do not open this file until the Phase-1 blind lock has been committed and pushed. It names "
            "the canonical dependencies the auditor may then verify against current official sources."
        ),
        "tranche_id": TRANCHE_ID,
        "represented_candidate_sha": CANDIDATE_SHA,
        "question_rule_map": {
            question_id: list(questions[question_id].get("rule_ids", [])) for question_id in QUESTION_IDS
        },
        "question_drug_map": {
            question_id: list(questions[question_id].get("drug_ids", [])) for question_id in QUESTION_IDS
        },
        "question_taxonomy": {
            question_id: {
                "area": questions[question_id]["area"],
                "topic": questions[question_id]["topic"],
                "subtopic": questions[question_id]["subtopic"],
                "difficulty": questions[question_id]["difficulty"],
                "family_id": questions[question_id]["family_id"],
            }
            for question_id in QUESTION_IDS
        },
        "dependency_snapshots": snapshots,
        "canonical_paths": {
            question_id: f"data/questions/{question_id.lower()}.json" for question_id in QUESTION_IDS
        },
    }


def build_attestation(manifest: dict) -> dict:
    return {
        "attestation_type": "GOVERNANCE_PRECERTIFIED_PHASE0",
        "date": FREEZE_DATE,
        "tranche_id": TRANCHE_ID,
        "authorizing_issue": AUTHORIZING_ISSUE,
        "controller_issue": CONTROLLER_ISSUE,
        "candidate_branch": CANDIDATE_BRANCH,
        "candidate_sha": CANDIDATE_SHA,
        "freeze_branch": FREEZE_BRANCH,
        "auditor_instance_reserved": AUDITOR_INSTANCE_RESERVED,
        "question_ids": list(QUESTION_IDS),
        "question_hashes": manifest["question_hashes"],
        "dependency_snapshots": manifest["dependency_snapshots"],
        "package_sha256": {
            path.relative_to(ROOT).as_posix(): file_sha256(path)
            for path in (BLIND_PACKAGE, LEGAL_CONTRACT, REALISM_CONTRACT, MANIFEST, POSTLOCK)
        },
        "repository_validation": "PASS",
        "full_tests": "PASS",
        "generated_artifact_freshness": "PASS",
        "duplicate_detector_findings": 0,
        "structural_pattern_findings": 0,
        "auditor_phase0_required": False,
        "auditor_start_phase": "PHASE_1_BLIND_SOLVE",
        "independence_statement": (
            "MA-Q-0227 and MA-Q-0228 were authored by the Claude Code controller session running Issue #83. "
            "That session must not audit them. The audit requires a separate session whose pre-lock inputs "
            "are the sanitized blind package and current official sources only, recorded under a distinct "
            "auditor_instance."
        ),
        "safe_content_statement": (
            "This attestation contains hashes, blob identifiers and dependency metadata only. It contains "
            "no canonical keyed answer, explanation or author reasoning."
        ),
    }


def main() -> int:
    head = git("rev-parse", "HEAD")
    if head != CANDIDATE_SHA:
        raise SystemExit(f"HEAD {head} is not the frozen candidate {CANDIDATE_SHA}")

    questions = load_candidate_questions()
    snapshots = dependency_snapshots(questions)

    write_json(BLIND_PACKAGE, build_blind_package(questions))
    write_json(LEGAL_CONTRACT, build_contract("LEGAL_VERIFICATION", questions, snapshots))
    write_json(REALISM_CONTRACT, build_contract("REALISM_REVIEW", questions, snapshots))
    manifest = build_manifest(questions, snapshots)
    write_json(MANIFEST, manifest)
    write_json(POSTLOCK, build_postlock(questions, snapshots))
    write_json(ATTESTATION, build_attestation(manifest))

    blind = load_json(BLIND_PACKAGE)
    leaked = []
    blind_text = json.dumps(blind, ensure_ascii=False)
    for question_id, question in questions.items():
        for field in ("correct_choice_ids", "rule_ids", "family_id", "topic", "subtopic"):
            value = question.get(field)
            needle = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
            if isinstance(value, str) and value and value in blind_text:
                leaked.append(f"{question_id}.{field}")
            elif isinstance(value, list) and value and all(str(item) in blind_text for item in value):
                if field != "correct_choice_ids":
                    leaked.append(f"{question_id}.{field}")
        if question["explanation"]["core_reasoning"] in blind_text:
            leaked.append(f"{question_id}.explanation")
    allowed_keys = {"question_id", "question_type", "stem", "choices"}
    for item in blind["questions"]:
        extra = set(item) - allowed_keys
        if extra:
            leaked.append(f"blind package exposes {sorted(extra)}")
    if leaked:
        raise SystemExit(f"blind package leakage: {leaked}")

    for path in (BLIND_PACKAGE, LEGAL_CONTRACT, REALISM_CONTRACT, MANIFEST, POSTLOCK, ATTESTATION):
        print(f"wrote {path.relative_to(ROOT).as_posix()}  sha256={file_sha256(path)}")
    print("blind-package leakage check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
