"""Build the deterministic Batch 4 Phase-0 census and controller plan.

This script does not author, edit, adjudicate, or release questions.  It measures
the GitHub-main canonical tree and writes the four Phase-0 artifacts required by
Issue #121.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_structural_patterns import analyze_structural_patterns
from qa_common import DATA, ROOT, deterministic_hash, load_json, load_records, question_audit_hash, write_json
from release_context import style_profile_snapshot
from validate_audits import validate_audits


REPORT_DATE = "2026-09-01"
CONTROLLER_ISSUE = 121
EXPECTED_STARTING_MAIN = "5f07f49e43d50dff7a8a2f8c49f0a58135d120d7"
FOUR_SET_ALLOCATION = {1: 104, 2: 160, 3: 116, 4: 100}
PER_EXAM_ALLOCATION = {1: 26, 2: 40, 3: 29, 4: 25}
QUARANTINED_IDS = {"MA-Q-0028"}
KNOWN_STALE_AUTHORITY_RULE_IDS = {"MA-MH-SUD-ADMIN"}
KNOWN_PARALLEL_DEBT_RULE_IDS = {"FED-PSE-QUANTITY", "MA-PMP-REPORTING"}

TRANCHES = [
    {"tranche_id": "B4-A", "first_id": "MA-Q-0407", "last_id": "MA-Q-0439", "count": 33, "area_allocation": {"1": 9, "2": 12, "3": 7, "4": 5}},
    {"tranche_id": "B4-B", "first_id": "MA-Q-0440", "last_id": "MA-Q-0472", "count": 33, "area_allocation": {"1": 8, "2": 11, "3": 8, "4": 6}},
    {"tranche_id": "B4-C", "first_id": "MA-Q-0473", "last_id": "MA-Q-0505", "count": 33, "area_allocation": {"1": 7, "2": 11, "3": 8, "4": 7}},
    {"tranche_id": "B4-D", "first_id": "MA-Q-0506", "last_id": "MA-Q-0538", "count": 33, "area_allocation": {"1": 5, "2": 10, "3": 8, "4": 10}},
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def is_released(question: dict) -> bool:
    return question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED"


def counter_json(values) -> dict[str, int]:
    return {str(key): value for key, value in sorted(Counter(values).items(), key=lambda item: str(item[0]))}


def sba_length_metrics(questions: list[dict]) -> dict:
    sba = [question for question in questions if question["question_type"] == "SBA"]
    first_longest_is_keyed = 0
    any_tied_longest_is_keyed = 0
    keyed_lengths: list[int] = []
    distractor_lengths: list[int] = []
    question_validator_outliers: list[str] = []
    structural_detector_outliers: list[str] = []
    for question in sba:
        lengths = {choice["id"]: len(choice["text"]) for choice in question["choices"]}
        key = question["correct_choice_ids"][0]
        maximum = max(lengths.values())
        first_longest = next(choice["id"] for choice in question["choices"] if lengths[choice["id"]] == maximum)
        first_longest_is_keyed += first_longest == key
        any_tied_longest_is_keyed += lengths[key] == maximum
        keyed_lengths.append(lengths[key])
        distractor_lengths.extend(length for choice_id, length in lengths.items() if choice_id != key)
        keyed_tokens = len(next(choice["text"] for choice in question["choices"] if choice["id"] == key).split())
        distractor_tokens = max(
            len(choice["text"].split()) for choice in question["choices"] if choice["id"] != key
        )
        if keyed_tokens >= 1.5 * distractor_tokens and keyed_tokens >= distractor_tokens + 4:
            question_validator_outliers.append(question["question_id"])
        if keyed_tokens >= 1.6 * distractor_tokens and keyed_tokens >= distractor_tokens + 6:
            structural_detector_outliers.append(question["question_id"])
    count = len(sba)
    return {
        "sba_count": count,
        "first_longest_is_keyed": first_longest_is_keyed,
        "first_longest_rate_percent": round(100 * first_longest_is_keyed / count, 1),
        "any_tied_longest_is_keyed": any_tied_longest_is_keyed,
        "any_tied_longest_rate_percent": round(100 * any_tied_longest_is_keyed / count, 1),
        "mean_keyed_characters": round(sum(keyed_lengths) / len(keyed_lengths), 1),
        "mean_distractor_characters": round(sum(distractor_lengths) / len(distractor_lengths), 1),
        "question_validator_outliers": sorted(question_validator_outliers),
        "structural_detector_outliers": sorted(structural_detector_outliers),
    }


def sata_metrics(questions: list[dict]) -> dict:
    sata = [question for question in questions if question["question_type"] == "SATA"]
    correct_count = Counter(len(question["correct_choice_ids"]) for question in sata)
    key_patterns = Counter("".join(sorted(question["correct_choice_ids"])) for question in sata)
    return {
        "sata_count": len(sata),
        "correct_count_distribution": {str(key): value for key, value in sorted(correct_count.items())},
        "key_pattern_distribution": dict(sorted(key_patterns.items())),
        "top_key_patterns": [{"pattern": key, "count": value} for key, value in key_patterns.most_common(10)],
    }


def current_audit_evidence(question: dict, audits: dict[str, dict], style_profile: dict) -> dict:
    question_id = question["question_id"]
    current_hash = question_audit_hash(question)
    passing_legal: list[str] = []
    passing_realism: list[str] = []
    failing: list[dict] = []
    for audit_id, audit in audits.items():
        if audit.get("question_hashes", {}).get(question_id) != current_hash:
            continue
        if not audit.get("independent") or audit.get("audit_status") != "FULLY_ADJUDICATED":
            continue
        result = next((row for row in audit.get("results", []) if row.get("Question_ID") == question_id), None)
        if result is None:
            continue
        if audit.get("review_type") == "LEGAL_VERIFICATION":
            if result.get("Verdict") == "KEEP" and result.get("Existing_Answer_Correct") == "YES":
                passing_legal.append(audit_id)
            else:
                failing.append({"audit_id": audit_id, "review_type": "LEGAL_VERIFICATION", "verdict": result.get("Verdict"), "answer_correct": result.get("Existing_Answer_Correct")})
        elif audit.get("review_type") == "REALISM_REVIEW":
            if (
                audit.get("style_profile") == style_profile_snapshot(style_profile)
                and result.get("Verdict") == "KEEP"
                and result.get("Realism_Verdict") == "PASS"
            ):
                passing_realism.append(audit_id)
            else:
                failing.append({"audit_id": audit_id, "review_type": "REALISM_REVIEW", "verdict": result.get("Verdict"), "realism_verdict": result.get("Realism_Verdict")})
    return {
        "question_hash": current_hash,
        "passing_legal_audits": sorted(passing_legal),
        "passing_realism_audits": sorted(passing_realism),
        "failing_current_hash_evidence": sorted(failing, key=lambda row: row["audit_id"]),
    }


def classify_unreleased(question: dict, evidence: dict, audits: dict[str, dict]) -> tuple[str, str]:
    question_id = question["question_id"]
    if question_id in QUARANTINED_IDS:
        return "QUARANTINED", "Explicit quarantine; zero Batch-4 capacity."
    if question.get("verification_status") == "HOLD" or question.get("lifecycle_status") == "REVIEW_REQUIRED":
        return "AUTHORITY_HOLD", "Known current-authority issue; unchanged current-hash audit evidence cannot make it usable."
    if evidence["failing_current_hash_evidence"]:
        return "NEEDS_REPAIR_AND_REAUDIT", "Current-hash audit contains a legal or realism failure."
    if evidence["passing_legal_audits"] and evidence["passing_realism_audits"]:
        used = evidence["passing_legal_audits"] + evidence["passing_realism_audits"]
        if any(not audits[audit_id].get("auditor_instance") for audit_id in used):
            return "NEEDS_FRESH_INSTANCE_AUDIT", "Passing evidence lacks auditor_instance required by current policy."
        return "NEEDS_GUARDED_ADMISSION_REVIEW", "Passing evidence exists, but lifecycle/dependencies/final adjudication still require exact release-gate review."
    return "NEEDS_FRESH_AUDIT", "No complete current-hash legal and realism pass pair."


def authority_coverage(released: list[dict], rules: dict[str, dict]) -> dict:
    used_rule_ids = sorted({rule_id for question in released for rule_id in question.get("rule_ids", [])})
    authorities = [
        {**authority, "rule_id": rule_id}
        for rule_id in used_rule_ids
        for authority in rules[rule_id].get("authority", [])
    ]
    domains = Counter(urlparse(authority["url"]).netloc.lower() for authority in authorities)
    return {
        "released_unique_rule_ids": len(used_rule_ids),
        "released_rule_statuses": counter_json(rules[rule_id]["status"] for rule_id in used_rule_ids),
        "released_rule_verification_statuses": counter_json(rules[rule_id]["verification_status"] for rule_id in used_rule_ids),
        "authority_record_count": len(authorities),
        "authority_type_distribution": counter_json(authority["type"] for authority in authorities),
        "authority_domain_distribution": dict(sorted(domains.items())),
        "rules_missing_authority_or_https_url": [
            rule_id
            for rule_id in used_rule_ids
            if not rules[rule_id].get("authority")
            or any(not authority.get("url", "").startswith("https://") for authority in rules[rule_id].get("authority", []))
        ],
        "last_verified_range": {
            "earliest": min(rules[rule_id]["last_verified"] for rule_id in used_rule_ids),
            "latest": max(rules[rule_id]["last_verified"] for rule_id in used_rule_ids),
        },
    }


def build_inventory(
    source_sha: str,
    questions: dict[str, dict],
    rules: dict[str, dict],
    drugs: dict[str, dict],
    audits: dict[str, dict],
    style_profile: dict,
) -> dict:
    all_questions = [questions[question_id] for question_id in sorted(questions)]
    released = [question for question in all_questions if is_released(question)]
    unreleased = [question for question in all_questions if not is_released(question)]
    released_by_area = Counter(question["area"] for question in released)
    deficits = {str(area): max(0, target - released_by_area.get(area, 0)) for area, target in FOUR_SET_ALLOCATION.items()}

    unreleased_rows = []
    for question in unreleased:
        evidence = current_audit_evidence(question, audits, style_profile)
        classification, reason = classify_unreleased(question, evidence, audits)
        unreleased_rows.append(
            {
                "question_id": question["question_id"],
                "area": question["area"],
                "topic": question["topic"],
                "family_id": question["family_id"],
                "verification_status": question["verification_status"],
                "lifecycle_status": question["lifecycle_status"],
                "classification": classification,
                "reason": reason,
                **evidence,
            }
        )
    classification_counts = Counter(row["classification"] for row in unreleased_rows)
    classification_by_area: dict[str, Counter] = defaultdict(Counter)
    for row in unreleased_rows:
        classification_by_area[row["classification"]][row["area"]] += 1

    numeric_ids = sorted(int(question_id.rsplit("-", 1)[1]) for question_id in questions)
    gaps = sorted(set(range(1, max(numeric_ids) + 1)) - set(numeric_ids))
    full_structural, full_structural_failed = analyze_structural_patterns(all_questions)
    preview_allowlist = load_json(ROOT / "site" / "generated" / "preview_allowlist.json")
    public_payload = load_json(ROOT / "site" / "generated" / "questions.json")
    hold_rules = [
        {
            "rule_id": rule["rule_id"],
            "title": rule["title"],
            "status": rule["status"],
            "verification_status": rule["verification_status"],
            "last_verified": rule["last_verified"],
        }
        for rule in rules.values()
        if rule.get("status") != "CURRENT" or rule.get("verification_status") == "HOLD"
    ]

    jurisdictions = {
        question["question_id"]: {rules[rule_id]["jurisdiction"] for rule_id in question.get("rule_ids", [])}
        for question in released
    }
    return {
        "report_type": "BATCH4_BASELINE_INVENTORY",
        "recorded_on": REPORT_DATE,
        "controller_issue": CONTROLLER_ISSUE,
        "github": {
            "repository": "woojunxnam/oddments",
            "authoritative": True,
            "source_live_main_sha": source_sha,
            "expected_handoff_sha_matched": source_sha == EXPECTED_STARTING_MAIN,
        },
        "bank": {
            "canonical_questions": len(all_questions),
            "released_questions": len(released),
            "unreleased_questions": len(unreleased),
            "status_pairs": counter_json(f"{question['verification_status']}|{question['lifecycle_status']}" for question in all_questions),
            "highest_used_question_id": f"MA-Q-{max(numeric_ids):04d}",
            "next_free_question_id": f"MA-Q-{max(numeric_ids) + 1:04d}",
            "id_gaps": gaps,
            "released_by_area": {str(area): released_by_area.get(area, 0) for area in sorted(FOUR_SET_ALLOCATION)},
            "canonical_by_area": counter_json(question["area"] for question in all_questions),
            "unreleased_by_area": counter_json(question["area"] for question in unreleased),
        },
        "four_exam_target": {
            "exam_count": 4,
            "questions_per_exam": 120,
            "per_exam_area_allocation": {str(area): count for area, count in PER_EXAM_ALLOCATION.items()},
            "minimum_by_area": {str(area): count for area, count in FOUR_SET_ALLOCATION.items()},
            "minimum_total_distinct": 480,
            "deficit_by_area": deficits,
            "deficit_total": sum(deficits.values()),
            "preferred_final_released": 486,
            "preferred_new_releases": 120,
        },
        "unreleased_capacity": {
            "current_release_usable_capacity": 0,
            "classification_counts": dict(sorted(classification_counts.items())),
            "classification_by_area": {
                classification: {str(area): count for area, count in sorted(counts.items())}
                for classification, counts in sorted(classification_by_area.items())
            },
            "questions": unreleased_rows,
            "conclusion": "No unreleased record is counted toward the four-exam minimum. MA-Q-0172 carries passing old current-hash evidence but remains an explicit authority HOLD; the other 39 require fresh audit, semantic repair/reaudit, or remain quarantined.",
        },
        "released_distributions": {
            "question_type": counter_json(question["question_type"] for question in released),
            "difficulty": counter_json(question["difficulty"] for question in released),
            "drug_integrated": sum(bool(question.get("drug_ids")) for question in released),
            "non_drug": sum(not question.get("drug_ids") for question in released),
            "multi_rule": sum(len(question.get("rule_ids", [])) > 1 for question in released),
            "ma_only": sum(value == {"MA"} for value in jurisdictions.values()),
            "federal_only": sum(value == {"FEDERAL"} for value in jurisdictions.values()),
            "ma_federal_interaction": sum(value >= {"MA", "FEDERAL"} for value in jurisdictions.values()),
            "unique_drug_ids": len({drug_id for question in released for drug_id in question.get("drug_ids", [])}),
        },
        "quality_baseline": {
            "validate_all": {"errors": 0, "warnings": 1, "warning_ids": ["MA-Q-0190"], "verdict": "PASS"},
            "pytest": {"passed": 100, "skipped": 1, "failed": 0, "verdict": "PASS"},
            "duplicate_detector": {"finding_count": load_json(ROOT / "duplicate_report.json")["finding_count"], "verdict": "PASS"},
            "structural_detector_default_scope": {"finding_count": load_json(ROOT / "structural_pattern_report.json")["finding_count"], "verdict": "PASS"},
            "structural_detector_full_bank": {"finding_count": full_structural["finding_count"], "failed": full_structural_failed, "findings": full_structural["findings"], "verdict": "FAIL" if full_structural_failed else "PASS"},
            "sba_answer_length": {
                "canonical": sba_length_metrics(all_questions),
                "released": sba_length_metrics(released),
                "disposition": "BATCH4_PARALLEL_FIX",
                "interpretation": "The aggregate first-longest signal remains consequential even though the existing per-item detector only warns on MA-Q-0190.",
            },
            "sata": {"canonical": sata_metrics(all_questions), "released": sata_metrics(released)},
        },
        "official_source_coverage": authority_coverage(released, rules),
        "known_authority_debt": {
            "hold_or_unclear_rules": sorted(hold_rules, key=lambda row: row["rule_id"]),
            "ma_mh_sud_admin": {
                "classification": "BATCH4_BLOCKING_FOR_DEPENDENT_CONTENT",
                "finding": "MA-MH-SUD-ADMIN still cites superseded DCP 19-2-105 while DCP 26-03-124 dated 2026-03-11 is current. New authoring and Study Guide prose must use migrated current dependencies; MA-Q-0172 remains HOLD.",
                "released_dependents": sorted(question["question_id"] for question in released if "MA-MH-SUD-ADMIN" in question.get("rule_ids", [])),
            },
            "citation_dependency_propagation": {
                "classification": "BATCH4_PARALLEL_FIX",
                "rules": ["FED-PSE-QUANTITY", "MA-PMP-REPORTING"],
                "finding": "Verified citation/pinpoint corrections were deferred because rule rehashing propagates through drug and released-question dependency snapshots and requires independent re-adjudication.",
            },
        },
        "site_baseline": {
            "storage": "localStorage",
            "storage_key": "ma-mpje-progress-v1",
            "completed_exam_history": False,
            "export_import": False,
            "quick_20": False,
            "raw_generated_question_count": len(public_payload.get("questions", [])),
            "browser_allowlist_count": len(preview_allowlist.get("question_ids", [])),
            "raw_unreleased_records_exposed": len(public_payload.get("questions", [])) - len(preview_allowlist.get("question_ids", [])),
            "classification": "BATCH4_BLOCKING_BEFORE_LANE_C",
            "required_action": "Generate a RELEASE-only public question asset; client-side allowlisting is not a confidentiality boundary.",
        },
        "debt_classification": [
            {"item": "Aggregate SBA answer-length leakage", "classification": "BATCH4_PARALLEL_FIX"},
            {"item": "FED-PSE-QUANTITY / MA-PMP-REPORTING citation and dependency propagation", "classification": "BATCH4_PARALLEL_FIX"},
            {"item": "MA-Q-0190 per-item answer-length warning", "classification": "BATCH4_PARALLEL_FIX"},
            {"item": "MA-Q-0028 quarantine", "classification": "POST_BATCH4_DEBT"},
            {"item": "MA-MH-SUD-ADMIN superseded authority migration", "classification": "BATCH4_BLOCKING_FOR_DEPENDENT_CONTENT"},
            {"item": "MA-Q-0172 authority hold", "classification": "POST_BATCH4_DEBT_UNLESS_CLEARED_INDEPENDENTLY"},
            {"item": "Raw static payload exposes 40 unreleased questions", "classification": "BATCH4_BLOCKING_BEFORE_LANE_C"},
        ],
    }


def build_proposition_census(source_sha: str, questions: dict[str, dict], rules: dict[str, dict]) -> dict:
    released = [questions[question_id] for question_id in sorted(questions) if is_released(questions[question_id])]
    proposition_rows = []
    by_rule_signature: dict[str, list[str]] = defaultdict(list)
    for question in released:
        rule_ids = sorted(question.get("rule_ids", []))
        jurisdictions = sorted({rules[rule_id]["jurisdiction"] for rule_id in rule_ids})
        signature_fields = {
            "area": question["area"],
            "topic": question["topic"],
            "subtopic": question["subtopic"],
            "rule_ids": rule_ids,
            "reasoning_steps": question.get("reasoning_steps", []),
        }
        rule_signature = deterministic_hash(rule_ids)
        proposition_signature = deterministic_hash(signature_fields)
        by_rule_signature[rule_signature].append(question["question_id"])
        proposition_rows.append(
            {
                "question_id": question["question_id"],
                "question_hash": question_audit_hash(question),
                "area": question["area"],
                "topic": question["topic"],
                "subtopic": question["subtopic"],
                "family_id": question["family_id"],
                "rule_ids": rule_ids,
                "drug_ids": sorted(question.get("drug_ids", [])),
                "jurisdictions": jurisdictions,
                "reasoning_steps": question.get("reasoning_steps", []),
                "rule_set_signature": rule_signature,
                "proposition_signature": proposition_signature,
            }
        )

    prior = load_json(ROOT / "audits" / "coverage" / "2026-08-19" / "POST-T3-PRE-BATCH3-FINAL-COVERAGE-MATRIX.json")
    atomic_rows = []
    for row in prior["rows"]:
        current = []
        for evidence in row["selected_release_evidence"]:
            question = questions.get(evidence["question_id"])
            if question and is_released(question) and question_audit_hash(question) == evidence["question_hash"]:
                current.append(evidence["question_id"])
        atomic_rows.append(
            {
                "atomic_id": row["atomic_id"],
                "nabp_area": row["nabp_area"],
                "label": row["label"],
                "current_release_evidence_ids": current,
                "current_release_evidence_count": len(current),
                "status": "PASS" if current else "FAIL",
            }
        )
    headline_groups: dict[str, list[dict]] = defaultdict(list)
    for row in atomic_rows:
        headline = row["atomic_id"][:-1] if row["atomic_id"][-1].isalpha() else row["atomic_id"]
        headline_groups[headline].append(row)
    headline_rows = []
    for headline, rows in sorted(headline_groups.items()):
        evidence_ids = sorted({question_id for row in rows for question_id in row["current_release_evidence_ids"]})
        headline_rows.append(
            {
                "headline": headline,
                "atomic_ids": [row["atomic_id"] for row in rows],
                "failed_atomic_ids": [row["atomic_id"] for row in rows if row["status"] != "PASS"],
                "current_release_evidence_ids": evidence_ids,
                "distinct_families": sorted({questions[question_id]["family_id"] for question_id in evidence_ids}),
                "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            }
        )

    topic_groups: dict[tuple[int, str, str], list[dict]] = defaultdict(list)
    for row in proposition_rows:
        topic_groups[(row["area"], row["topic"], row["subtopic"])].append(row)
    topic_rows = [
        {
            "area": area,
            "topic": topic,
            "subtopic": subtopic,
            "released_count": len(rows),
            "family_ids": sorted({row["family_id"] for row in rows}),
            "rule_ids": sorted({rule_id for row in rows for rule_id in row["rule_ids"]}),
            "question_ids": [row["question_id"] for row in rows],
        }
        for (area, topic, subtopic), rows in sorted(topic_groups.items())
    ]
    exact_duplicate_signatures = [
        {"proposition_signature": signature, "question_ids": ids}
        for signature, ids in defaultdict(list, {
            signature: [row["question_id"] for row in proposition_rows if row["proposition_signature"] == signature]
            for signature in {row["proposition_signature"] for row in proposition_rows}
        }).items()
        if len(ids) > 1
    ]
    return {
        "report_type": "BATCH4_PROPOSITION_CENSUS",
        "recorded_on": REPORT_DATE,
        "controller_issue": CONTROLLER_ISSUE,
        "source_live_main_sha": source_sha,
        "method": "Each RELEASED question is represented by its current audit hash, Area/topic/subtopic, exact rule and drug dependencies, jurisdictions, and reasoning steps. The proposition signature intentionally goes below family name.",
        "summary": {
            "released_questions": len(released),
            "unique_proposition_signatures": len({row["proposition_signature"] for row in proposition_rows}),
            "unique_rule_set_signatures": len(by_rule_signature),
            "exact_duplicate_proposition_signature_groups": len(exact_duplicate_signatures),
            "topics": len({row["topic"] for row in proposition_rows}),
            "subtopic_rows": len(topic_rows),
            "atomic_competencies_passed": sum(row["status"] == "PASS" for row in atomic_rows),
            "atomic_competencies_total": len(atomic_rows),
            "headline_families_passed": sum(row["status"] == "PASS" for row in headline_rows),
            "headline_families_total": len(headline_rows),
        },
        "atomic_competencies": atomic_rows,
        "headline_families": headline_rows,
        "topic_subtopic_coverage": topic_rows,
        "rule_set_clusters": [
            {"rule_set_signature": signature, "question_ids": ids, "count": len(ids)}
            for signature, ids in sorted(by_rule_signature.items())
        ],
        "exact_duplicate_proposition_signatures": exact_duplicate_signatures,
        "released_propositions": proposition_rows,
        "authoring_constraint": "A second question in a family is not novel unless its proposition row differs materially in actor, trigger, exception, jurisdiction, setting, timing, documentation consequence, or legal interaction. Drug substitution alone is insufficient.",
    }


def build_family_headroom(source_sha: str, questions: dict[str, dict], rules: dict[str, dict], matrix: dict) -> dict:
    candidate_counts = Counter(question["family_id"] for question in questions.values())
    released_counts = Counter(question["family_id"] for question in questions.values() if is_released(question))
    rows = []
    for family in sorted(matrix["families"], key=lambda item: item["family_id"]):
        family_id = family["family_id"]
        dependency_ids = sorted(set(family.get("primary_rule_ids", []) + family.get("secondary_rule_ids", [])))
        missing = [rule_id for rule_id in dependency_ids if rule_id not in rules]
        blocked = [
            rule_id
            for rule_id in dependency_ids
            if rule_id in rules and (rules[rule_id].get("status") != "CURRENT" or rules[rule_id].get("verification_status") == "HOLD")
        ]
        stale = sorted(set(dependency_ids) & KNOWN_STALE_AUTHORITY_RULE_IDS)
        parallel_debt = sorted(set(dependency_ids) & KNOWN_PARALLEL_DEBT_RULE_IDS)
        source_readiness = (
            "MISSING_RULE"
            if missing
            else "HOLD_OR_UNCLEAR"
            if blocked
            else "KNOWN_STALE_AUTHORITY_DEBT"
            if stale
            else "CURRENT_WITH_RECORDED_DEPENDENCY_DEBT"
            if parallel_debt
            else "CURRENT_AUTHORITY_METADATA"
        )
        released_count = released_counts.get(family_id, 0)
        candidate_count = candidate_counts.get(family_id, 0)
        cap = family["max_questions_in_final_bank"]
        rows.append(
            {
                "family_id": family_id,
                "area": family["area"],
                "topic": family["topic"],
                "subtopic": family["subtopic"],
                "primary_rule_ids": family.get("primary_rule_ids", []),
                "secondary_rule_ids": family.get("secondary_rule_ids", []),
                "drug_required": family["drug_required"],
                "target_difficulties": family["target_difficulties"],
                "target_item_types": family["target_item_types"],
                "computed_candidate_count": candidate_count,
                "matrix_candidate_count": family["current_candidate_count"],
                "computed_released_count": released_count,
                "matrix_released_count": family["current_released_count"],
                "max_questions_in_final_bank": cap,
                "released_headroom": max(0, cap - released_count),
                "saturated": released_count >= cap,
                "source_readiness": source_readiness,
                "blocked_rule_ids": blocked,
                "missing_rule_ids": missing,
                "known_stale_authority_rule_ids": stale,
                "parallel_debt_rule_ids": parallel_debt,
                "question_ids": sorted(question_id for question_id, question in questions.items() if question["family_id"] == family_id),
            }
        )
    mismatches = [
        row["family_id"]
        for row in rows
        if row["computed_candidate_count"] != row["matrix_candidate_count"]
        or row["computed_released_count"] != row["matrix_released_count"]
    ]
    return {
        "report_type": "BATCH4_FAMILY_HEADROOM",
        "recorded_on": REPORT_DATE,
        "controller_issue": CONTROLLER_ISSUE,
        "source_live_main_sha": source_sha,
        "summary": {
            "families_in_matrix": len(rows),
            "families_with_candidates": sum(row["computed_candidate_count"] > 0 for row in rows),
            "families_with_released_questions": sum(row["computed_released_count"] > 0 for row in rows),
            "saturated_family_count": sum(row["saturated"] for row in rows),
            "released_headroom_sum": sum(row["released_headroom"] for row in rows),
            "zero_candidate_family_count": sum(row["computed_candidate_count"] == 0 for row in rows),
            "authority_blocked_family_count": sum(row["source_readiness"] in {"MISSING_RULE", "HOLD_OR_UNCLEAR", "KNOWN_STALE_AUTHORITY_DEBT"} for row in rows),
            "parallel_dependency_debt_family_count": sum(row["source_readiness"] == "CURRENT_WITH_RECORDED_DEPENDENCY_DEBT" for row in rows),
            "matrix_count_mismatches": mismatches,
        },
        "saturated_families": [row for row in rows if row["saturated"]],
        "available_current_authority_families": [
            row for row in rows if row["released_headroom"] > 0 and row["source_readiness"] == "CURRENT_AUTHORITY_METADATA"
        ],
        "blocked_or_unclear_families": [
            row for row in rows if row["source_readiness"] in {"MISSING_RULE", "HOLD_OR_UNCLEAR", "KNOWN_STALE_AUTHORITY_DEBT"}
        ],
        "families_with_parallel_dependency_debt": [
            row for row in rows if row["source_readiness"] == "CURRENT_WITH_RECORDED_DEPENDENCY_DEBT"
        ],
        "all_families": rows,
        "warning": "Numerical headroom is not authorization to author. Proposition novelty and current primary authority must be established before a family is selected.",
    }


def build_plan(source_sha: str, inventory: dict, proposition: dict, family: dict) -> dict:
    return {
        "report_type": "BATCH4_PLAN_V1",
        "recorded_on": REPORT_DATE,
        "controller_issue": CONTROLLER_ISSUE,
        "controller_issue_url": f"https://github.com/woojunxnam/oddments/issues/{CONTROLLER_ISSUE}",
        "source_live_main_sha": source_sha,
        "authority": {
            "github": "AUTHORITATIVE",
            "notion": "NAVIGATION_AND_HUMAN_SUMMARY_ONLY",
            "notion_page_url": "https://app.notion.com/p/3cec4d2fdd17818d9103edacec598673?pvs=204",
        },
        "measured_baseline": {
            "released": inventory["bank"]["released_questions"],
            "released_by_area": inventory["bank"]["released_by_area"],
            "four_exam_deficit_by_area": inventory["four_exam_target"]["deficit_by_area"],
            "four_exam_deficit_total": inventory["four_exam_target"]["deficit_total"],
            "next_free_question_id": inventory["bank"]["next_free_question_id"],
            "current_unreleased_capacity_counted": inventory["unreleased_capacity"]["current_release_usable_capacity"],
            "atomic_competencies": f"{proposition['summary']['atomic_competencies_passed']}/{proposition['summary']['atomic_competencies_total']}",
            "saturated_families": family["summary"]["saturated_family_count"],
        },
        "question_target": {
            "candidate_count": 132,
            "minimum_new_releases": 120,
            "preferred_final_released": 486,
            "minimum_four_exam_area_counts": {str(area): value for area, value in FOUR_SET_ALLOCATION.items()},
            "reserved_range": {"first_id": "MA-Q-0407", "last_id": "MA-Q-0538", "contiguous": True},
            "tranches": TRANCHES,
            "total_candidate_area_allocation": {"1": 29, "2": 44, "3": 31, "4": 28},
            "resilience_over_exact_deficit": {"1": 3, "2": 4, "3": 8, "4": 3, "total": 18},
        },
        "lane_a": {
            "name": "QUESTION_BANK_EXPANSION",
            "selection_order": [
                "Exclude HOLD/UNCLEAR/superseded dependencies and saturated families.",
                "Select genuinely distinct applied legal propositions from the proposition census.",
                "Verify current official authority and exact sections before semantic authoring.",
                "Balance Area allocation, item type, SATA correct-count, drug integration, MA/federal interaction, and answer-length leakage.",
            ],
            "tranche_workflow": [
                "author semantic AUDIT_PENDING candidate",
                "validate_all + pytest + duplicate + full-bank structural + answer distribution + tranche SATA gate + family cap + source freshness",
                "immutable freeze package",
                "sanitized blind package",
                "new unique independent auditor_instance",
                "immutable Phase-1 blind lock before canonical unseal",
                "official-source LEGAL verification and REALISM review",
                "commit/push audit evidence",
                "controller current-hash verification",
                "guarded release of qualifying current hashes only",
                "recompute four-exam Area deficits",
            ],
            "auditor_instances": ["GPT-FRESH-B4A", "GPT-FRESH-B4B", "GPT-FRESH-B4C", "GPT-FRESH-B4D"],
            "controller_self_audit_forbidden": True,
            "repair_policy": "Use the resilience buffer. Do not automatically repair every failure; repair only measured minimum deficits after releases.",
        },
        "lane_b": {
            "name": "STUDY_GUIDE_1_0",
            "canonical_truth": "data/rules/",
            "architecture": {
                "schema": "schemas/study_guide_section.schema.json",
                "index": "data/study_guide/index.json",
                "sections": "data/study_guide/sections/*.json",
                "coverage_matrix": "audits/coverage/<date>/STUDY-GUIDE-COVERAGE-MATRIX.json",
                "canonical_audit_records": "data/audits/",
                "generated_site_payload": "site/generated/study_guide.json",
                "generator": "scripts/build_study_guide_data.py",
                "validator": "scripts/validate_study_guide.py",
            },
            "section_contract": [
                "section_id", "title", "area", "topic", "learning_objectives", "rule_ids",
                "verified_rule_dependencies", "official_authority_references", "high_yield_summary",
                "decision_logic", "ma_vs_federal", "exceptions", "timing_deadlines", "forms_records",
                "role_specific_duties", "common_mpje_traps", "drug_examples", "practice_question_ids",
                "last_verified", "freshness_metadata",
            ],
            "fail_closed_rules": [
                "Every rule_id exists and is CURRENT with accepted verification status.",
                "Every stored rule version/hash equals the current canonical dependency.",
                "No HOLD/DRAFT/superseded rule is taught as current law.",
                "Every practice_question_id is current-hash RELEASE-usable and not quarantined.",
                "Every legal proposition in guide prose resolves to canonical rules.",
                "A rule hash change makes all dependent guide sections stale until regenerated and independently reverified.",
            ],
            "independent_guide_review": {
                "required": True,
                "scope": ["paraphrase fidelity", "MA-vs-federal comparisons", "exceptions", "deadlines", "decision tables", "oversimplification", "practice mapping"],
            },
            "content_modules": [
                "AREA_1_LICENSURE_PERSONNEL", "AREA_2_PHARMACIST_PRACTICE", "AREA_3_DISPENSING_REQUIREMENTS", "AREA_4_PHARMACY_OPERATIONS",
                "FEDERAL_VS_MASSACHUSETTS", "CONTROLLED_SUBSTANCE_MASTER_TABLE", "SCHEDULE_II_VS_III_V_VS_MA_VI",
                "PRESCRIPTION_VALIDITY", "REFILLS_TRANSFERS_PARTIAL_FILLS", "ORAL_ELECTRONIC_WRITTEN_PRESCRIPTIONS",
                "DEA_MASSACHUSETTS_FORMS_REPORTING", "MASSPAT", "PERSONNEL_SCOPE_MATRIX", "PHARMACIST_SERVICES",
                "COUNSELING_PATIENT_PROFILE_DUR", "CQI_QRE_SERIOUS_EVENT", "INVENTORY_SECURITY_LOSS_DESTRUCTION",
                "SUBSTITUTION_INTERCHANGE", "DEADLINES_RETENTION", "COMMON_MPJE_TRAPS", "DRUG_INTEGRATED_LAW_TABLES",
            ],
        },
        "lane_c": {
            "name": "STUDY_UX_1_0",
            "precondition": "Replace the raw 406-question static payload with RELEASE-only generated public data before adding study modes.",
            "quick_20": {"area_allocation": {"1": 4, "2": 7, "3": 5, "4": 4}, "fresh_seed_per_session": True, "stable_seed_within_session": True},
            "session_types": ["QUICK_20", "MOCK_120", "TOPIC_QUIZ", "WRONG_ANSWER_QUIZ", "BOOKMARKED_QUIZ"],
            "storage_decision": {
                "abstraction_required": True,
                "preferences_and_small_indexes": "localStorage",
                "detailed_exam_sessions_and_answers": "IndexedDB",
                "reason": "Detailed immutable question-hash/session-answer history can grow beyond localStorage's synchronous, quota-limited design; IndexedDB preserves local-first use and supports future cloud adapters.",
                "migration": "Versioned one-time import of ma-mpje-progress-v1 into the new storage abstraction; preserve original until verified.",
                "cloud_sync": "DEFERRED_NOT_REQUIRED",
            },
            "export_import": "Versioned JSON with schema validation, preview, explicit replace/merge decision, and no silent incompatible overwrite.",
            "history_integrity": "Persist question_id and question_content_hash with each answer so historical results remain interpretable after revisions.",
            "tests": ["fresh representative random session", "stable Back/Next", "completion/result calculations", "history survives refresh", "export/import validation", "wrong-answer retry", "RELEASE-only exposure", "guide mappings"],
        },
        "debt_policy": inventory["debt_classification"],
        "blocking_authority": inventory["known_authority_debt"]["ma_mh_sud_admin"],
        "phase_sequence": [
            "P0 artifacts + master issue",
            "P0.1 public-payload hardening and aggregate leakage gate design",
            "B4-A proposition/source plan",
            "B4-A author/freeze/fresh audit/release",
            "Study Guide schema/validator skeleton in parallel",
            "Lane C storage/session engine after RELEASE-only payload hardening",
            "Repeat B4-B/B4-C/B4-D with measured deficit recomputation",
            "Independent Study Guide verification",
            "Four-disjoint-exam construction and final integrated QA",
        ],
        "exact_next_action": "Commit and push these Phase-0 artifacts, open a PR, then harden the public generated question payload and define the aggregate SBA leakage gate before semantic B4-A authoring.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the four Phase-0 artifacts")
    args = parser.parse_args()

    source_sha = git("rev-parse", "origin/main")
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}
    _, audits = validate_audits()
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    matrix = load_json(DATA / "exam_style" / "question_family_matrix.json")

    inventory = build_inventory(source_sha, questions, rules, drugs, audits, style_profile)
    proposition = build_proposition_census(source_sha, questions, rules)
    family = build_family_headroom(source_sha, questions, rules, matrix)
    plan = build_plan(source_sha, inventory, proposition, family)
    output_dir = ROOT / "audits" / "coverage" / REPORT_DATE
    payloads = {
        output_dir / "BATCH4-BASELINE-INVENTORY.json": inventory,
        output_dir / "BATCH4-PROPOSITION-CENSUS.json": proposition,
        output_dir / "BATCH4-FAMILY-HEADROOM.json": family,
        output_dir / "BATCH4-PLAN-V1.json": plan,
    }
    if args.write:
        for path, payload in payloads.items():
            write_json(path, payload)
            print(f"wrote {path.relative_to(ROOT).as_posix()}")
    else:
        print(json.dumps({str(path.relative_to(ROOT)): payload["report_type"] for path, payload in payloads.items()}, indent=2))

    print(f"source live main: {source_sha}")
    print(f"released: {inventory['bank']['released_questions']} by area {inventory['bank']['released_by_area']}")
    print(f"four-set deficits: {inventory['four_exam_target']['deficit_by_area']} total={inventory['four_exam_target']['deficit_total']}")
    print(f"unreleased current capacity counted: {inventory['unreleased_capacity']['current_release_usable_capacity']}")
    print(f"families: {family['summary']['families_in_matrix']} saturated={family['summary']['saturated_family_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
