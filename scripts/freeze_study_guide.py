"""Build an immutable, full-prose audit package for Study Guide sections.

The package intentionally contains no controller verdicts or repair suggestions.  It binds every
section to its semantic hash, canonical rule versions/hashes and official authority metadata, and
RELEASED practice-question audit hashes at one represented candidate commit.

Usage:
    python scripts/freeze_study_guide.py --config <freeze-config.json>
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
from study_guide_common import study_guide_content_hash


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def blob_sha(commit: str, relative_path: str) -> str:
    line = git("ls-tree", commit, "--", relative_path)
    if not line:
        raise SystemExit(f"{relative_path} not found at {commit}")
    return line.split()[2]


def record_index(directory: Path, key: str) -> tuple[dict[str, dict], dict[str, str]]:
    records: dict[str, dict] = {}
    paths: dict[str, str] = {}
    for path, record in load_records(directory):
        record_id = record[key]
        records[record_id] = record
        paths[record_id] = path.relative_to(ROOT).as_posix()
    return records, paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = ROOT / config_path
    config = load_json(config_path)

    candidate_sha = config["represented_candidate_sha"]
    subprocess.check_call(["git", "merge-base", "--is-ancestor", candidate_sha, "HEAD"], cwd=ROOT)
    drift = git(
        "diff",
        "--name-only",
        candidate_sha,
        "HEAD",
        "--",
        "data/study_guide",
        "data/rules",
        "data/questions",
        "schemas/study_guide_section.schema.json",
    )
    if drift:
        raise SystemExit(f"canonical audit inputs drifted from {candidate_sha}: {drift.splitlines()}")

    sections, section_paths = record_index(DATA / "study_guide" / "sections", "section_id")
    rules, rule_paths = record_index(DATA / "rules", "rule_id")
    questions, question_paths = record_index(DATA / "questions", "question_id")
    section_ids = config["section_ids"]
    if not section_ids or len(section_ids) != len(set(section_ids)):
        raise SystemExit("freeze config must name a non-empty unique Study Guide section set")
    missing_section_ids = sorted(set(section_ids) - set(sections))
    if missing_section_ids:
        raise SystemExit(f"freeze config names unknown Study Guide sections: {missing_section_ids}")

    frozen_sections = []
    all_rule_ids: set[str] = set()
    all_question_ids: set[str] = set()
    for section_id in section_ids:
        section = sections[section_id]
        if section["verification_status"] != "AUDIT_PENDING":
            raise SystemExit(f"{section_id} is not AUDIT_PENDING")
        if section["content_hash"] != study_guide_content_hash(section):
            raise SystemExit(f"{section_id} content_hash is stale")
        all_rule_ids.update(section["rule_ids"])
        all_question_ids.update(section["practice_question_ids"])
        frozen_sections.append(
            {
                "section_id": section_id,
                "content_version": section["content_version"],
                "content_hash": section["content_hash"],
                "canonical_path": section_paths[section_id],
                "canonical_blob": blob_sha(candidate_sha, section_paths[section_id]),
                "full_prose_under_review": section,
                "rule_dependencies": [
                    {
                        "rule_id": rule_id,
                        "content_version": rules[rule_id]["content_version"],
                        "content_hash": rules[rule_id]["content_hash"],
                        "status": rules[rule_id]["status"],
                        "verification_status": rules[rule_id]["verification_status"],
                        "last_verified": rules[rule_id]["last_verified"],
                        "authority": rules[rule_id]["authority"],
                        "rule_summary": rules[rule_id]["rule_summary"],
                        "exceptions": rules[rule_id]["exceptions"],
                        "canonical_path": rule_paths[rule_id],
                        "canonical_blob": blob_sha(candidate_sha, rule_paths[rule_id]),
                    }
                    for rule_id in section["rule_ids"]
                ],
                "practice_question_dependencies": [
                    {
                        "question_id": question_id,
                        "question_hash": question_audit_hash(questions[question_id]),
                        "verification_status": questions[question_id]["verification_status"],
                        "lifecycle_status": questions[question_id]["lifecycle_status"],
                        "canonical_path": question_paths[question_id],
                        "canonical_blob": blob_sha(candidate_sha, question_paths[question_id]),
                    }
                    for question_id in section["practice_question_ids"]
                ],
            }
        )

    output_dir = ROOT / config["output_dir"]
    prefix = config["file_prefix"]
    package_path = output_dir / f"{prefix}-AUDIT-PACKAGE.json"
    manifest_path = output_dir / f"{prefix}-FREEZE-MANIFEST.json"
    package = {
        "package_type": "STUDY_GUIDE_FULL_PROSE_INDEPENDENT_AUDIT",
        "freeze_date": config["freeze_date"],
        "authorizing_issue": config["authorizing_issue"],
        "represented_candidate_branch": config["represented_candidate_branch"],
        "represented_candidate_sha": candidate_sha,
        "auditor_instance_reserved": config["auditor_instance_reserved"],
        "independent": True,
        "author_is_not_auditor": True,
        "section_ids": section_ids,
        "permitted_dispositions": ["KEEP", "MINOR_EDIT", "MAJOR_REWRITE", "HOLD"],
        "review_criteria": [
            "paraphrase_fidelity",
            "material_exceptions",
            "ma_vs_federal_distinctions",
            "actor_and_scope",
            "deadlines",
            "forms",
            "decision_logic",
            "overgeneralization",
            "unsupported_propositions",
            "practice_question_mapping",
            "study_usefulness_without_legal_distortion",
        ],
        "release_rule": (
            "정확히 동결된 current section hash에 대해 독립 auditor가 KEEP을 부여하고 모든 "
            "dependency hash가 current일 때만 공개할 수 있다. 다른 disposition은 비공개로 유지한다."
        ),
        "auditor_instruction": (
            "각 section을 현재 공식 authority와 독립적으로 대조하고, controller의 예상 결론 없이 평가한다. "
            "각 disposition과 finding을 section content_hash 및 모든 dependency hash에 결속한다."
        ),
        "sections": frozen_sections,
    }
    write_json(package_path, package)
    prior_audit_reference = config.get("prior_audit_reference")
    if prior_audit_reference is not None:
        prior_path = ROOT / prior_audit_reference["path"]
        if not prior_path.is_file():
            raise SystemExit(f"prior_audit_reference names a missing audit: {prior_path}")
        prior_audit_reference = {
            **prior_audit_reference,
            "sha256": file_sha256(prior_path),
            "reuse_for_repaired_hashes": False,
        }
    write_json(
        manifest_path,
        {
            "manifest_type": config.get("manifest_type", "STUDY_GUIDE_PILOT_CLEAN_FREEZE"),
            "freeze_date": config["freeze_date"],
            "authorizing_issue": config["authorizing_issue"],
            "represented_candidate_branch": config["represented_candidate_branch"],
            "represented_candidate_sha": candidate_sha,
            "auditor_instance_reserved": config["auditor_instance_reserved"],
            "author_is_not_auditor": True,
            "section_count": len(section_ids),
            "section_hashes": {sid: sections[sid]["content_hash"] for sid in section_ids},
            "section_file_blobs": {sid: blob_sha(candidate_sha, section_paths[sid]) for sid in section_ids},
            "rule_dependencies": {
                rule_id: {
                    "content_version": rules[rule_id]["content_version"],
                    "content_hash": rules[rule_id]["content_hash"],
                    "canonical_blob": blob_sha(candidate_sha, rule_paths[rule_id]),
                }
                for rule_id in sorted(all_rule_ids)
            },
            "practice_question_hashes": {
                question_id: question_audit_hash(questions[question_id])
                for question_id in sorted(all_question_ids)
            },
            "practice_question_blobs": {
                question_id: blob_sha(candidate_sha, question_paths[question_id])
                for question_id in sorted(all_question_ids)
            },
            "audit_package_path": package_path.relative_to(ROOT).as_posix(),
            "audit_package_sha256": file_sha256(package_path),
            "expected_audit_output_path": config["expected_audit_output_path"],
            **({"prior_audit_reference": prior_audit_reference} if prior_audit_reference else {}),
            "safe_content_statement": (
                "이 freeze에는 full Study Guide prose와 공식 dependency metadata가 포함되지만 "
                "controller expected verdict 또는 repair hint는 포함되지 않는다."
            ),
        },
    )
    print(f"wrote {package_path.relative_to(ROOT).as_posix()} sha256={file_sha256(package_path)}")
    print(f"wrote {manifest_path.relative_to(ROOT).as_posix()} sha256={file_sha256(manifest_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
