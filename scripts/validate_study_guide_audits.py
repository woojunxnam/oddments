from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from qa_common import DATA, ROOT, SCHEMAS, QAReport, load_json, load_records, question_audit_hash, validate_schema_records
from study_guide_common import study_guide_content_hash


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validate_study_guide_audits() -> tuple[QAReport, dict[str, dict[str, Any]]]:
    report = QAReport()
    root = ROOT / "audits" / "study_guide"
    records = [
        (path, load_json(path))
        for path in sorted(root.glob("**/*-AUDIT.json"))
        if path.is_file()
    ]
    validate_schema_records(records, SCHEMAS / "study_guide_audit.schema.json", report)
    audits: dict[str, dict[str, Any]] = {}
    instances: dict[str, str] = {}
    sections = {item["section_id"]: item for _, item in load_records(DATA / "study_guide" / "sections")}
    rules = {item["rule_id"]: item for _, item in load_records(DATA / "rules")}
    questions = {item["question_id"]: item for _, item in load_records(DATA / "questions")}

    for path, audit in records:
        audit_id = audit.get("audit_id")
        if audit_id in audits:
            report.error(f"{path}: duplicate audit_id {audit_id}")
        audits[audit_id] = audit
        instance = audit.get("auditor_instance")
        if instance in instances:
            report.error(f"{path}: duplicate auditor_instance also used by {instances[instance]}")
        instances[instance] = str(path)

        package_path = ROOT / audit.get("audit_package_path", "")
        if not package_path.is_file():
            report.error(f"{path}: missing audit package {package_path}")
            continue
        package = load_json(package_path)
        if normalized_sha256(package_path) != audit.get("audit_package_sha256"):
            report.error(f"{path}: audit package hash mismatch")
        if audit.get("auditor_instance") != package.get("auditor_instance_reserved"):
            report.error(f"{path}: auditor_instance does not match reserved identity")

        expected_ids = package.get("section_ids", [])
        if audit.get("section_ids") != expected_ids:
            report.error(f"{path}: section_ids do not exactly match frozen package order")
        frozen_by_id = {item["section_id"]: item for item in package.get("sections", [])}
        expected_hashes = {section_id: frozen_by_id[section_id]["content_hash"] for section_id in expected_ids}
        if audit.get("section_hashes") != expected_hashes:
            report.error(f"{path}: section_hashes do not exactly match frozen package")
        results = {item.get("section_id"): item for item in audit.get("results", [])}
        if len(results) != len(audit.get("results", [])) or set(results) != set(expected_ids):
            report.error(f"{path}: results must adjudicate each frozen section exactly once")

        for section_id in expected_ids:
            frozen = frozen_by_id[section_id]
            frozen_section = frozen.get("full_prose_under_review", {})
            if study_guide_content_hash(frozen_section) != frozen["content_hash"]:
                report.error(f"{path}: frozen semantic hash mismatch for {section_id}")
            current = sections.get(section_id)
            if current and current.get("content_hash") == frozen["content_hash"]:
                if study_guide_content_hash(current) != frozen["content_hash"]:
                    report.error(f"{path}: current semantic hash mismatch for {section_id}")
            elif current and current.get("independent_audit_id") == audit_id:
                # This audit certifies the section, but the prose has moved since. A section
                # verified by a LATER audit is not drift for this one: an earlier audit of a
                # since-repaired section is ordinary history. The section-level loop below
                # still requires every VERIFIED section to hold a KEEP from its own audit at
                # its exact current hash.
                report.error(f"{path}: current verified section drift for {section_id}")
            result = results.get(section_id, {})
            if result.get("section_hash") != frozen["content_hash"]:
                report.error(f"{path}: result hash mismatch for {section_id}")
            failed = [name for name, verdict in result.get("criteria", {}).items() if verdict != "PASS"]
            if result.get("disposition") == "KEEP" and (failed or result.get("practice_mapping_verdict") != "PASS"):
                report.error(f"{path}: KEEP section {section_id} has failed criteria")

            for dependency in frozen.get("rule_dependencies", []):
                current_rule = rules.get(dependency["rule_id"])
                if not current_rule or (
                    current_rule.get("content_version") != dependency["content_version"]
                    or current_rule.get("content_hash") != dependency["content_hash"]
                ):
                    report.error(f"{path}: stale rule dependency {dependency['rule_id']} for {section_id}")
            for dependency in frozen.get("practice_question_dependencies", []):
                current_question = questions.get(dependency["question_id"])
                if not current_question or question_audit_hash(current_question) != dependency["question_hash"]:
                    report.error(f"{path}: stale practice question {dependency['question_id']} for {section_id}")

    for section_id, section in sections.items():
        if section.get("verification_status") != "VERIFIED":
            continue
        audit_id = section.get("independent_audit_id")
        audit = audits.get(audit_id)
        if not audit:
            report.error(f"{section_id}: VERIFIED section has no canonical independent audit record {audit_id}")
            continue
        result = next(
            (item for item in audit.get("results", []) if item.get("section_id") == section_id),
            None,
        )
        if not result or result.get("disposition") != "KEEP":
            report.error(f"{section_id}: VERIFIED section lacks an independent KEEP disposition")
        elif result.get("section_hash") != section.get("content_hash"):
            report.error(f"{section_id}: VERIFIED section audit is stale")

    return report, audits


if __name__ == "__main__":
    from qa_common import print_report

    result, _ = validate_study_guide_audits()
    raise SystemExit(print_report("study guide audits", result))
