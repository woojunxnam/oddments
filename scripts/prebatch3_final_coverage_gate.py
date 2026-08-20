"""Final Pre-Batch3 competency coverage gate — full Issue #40 rerun from the exact post-T2 SHA.

Issue #83 PHASE F. Nothing here is projected: every atomic competency, every family,
every area count and the 120-question mock are recomputed from the current canonical
tree, and each piece of evidence is re-verified against current-hash audit records.

The frozen 46-row semantic baseline matrix (immutable git blob) supplies the atomic
definitions and the prior semantic evidence. Evidence is then recomputed as:

  * baseline selected evidence, carried forward only while still release-usable;
  * baseline legacy-salvage candidates, promoted only once actually released;
  * the Pre-Batch3 T2 tranche mappings;
  * explicit from-scratch corrections, each of which must state its justification.

A promotion is accepted only when the exact question is RELEASED, duplicate-clear,
final-KEEP and carries current-hash independent legal KEEP/YES plus realism KEEP/PASS.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, deterministic_hash, load_json, load_records, question_audit_hash, write_json
from release_context import style_profile_snapshot
from validate_audits import validate_audits


GATE_ID = "PRE_BATCH3_FULL_COMPETENCY_COVERAGE_DEBT_POST_T3"
CONTROLLER_ISSUE = 83
GATE_ISSUE = 40
NABP_PROFILE = "MPJE competency statements applicable before 2027-03-01"

BASELINE_MATRIX_BLOB = "e2490c406b14a540a0b259be8986c90119e760f1"
BASELINE_MATRIX_PATH = "audits/coverage/2026-08-17/FINAL-PRE-BATCH3-COVERAGE-MATRIX.json"
BASELINE_MATRIX_COMMIT = "b3a2e0d8b7b9f04b13ccfe0da2642948a7adf829"
POST_T1_MATRIX_SOURCE_SHA = "516771a93f939c843ba4c2be7ef745718606f448"

REQUIRED_AREA_ALLOCATION = {1: 26, 2: 40, 3: 29, 4: 25}
MOCK_SIZE = 120
FAMILY_DIVERSITY_MINIMUM = 2

# Promotions accepted by the post-T1 gate rerun (PR #67 analysis), re-verified here.
POST_T1_PROMOTIONS = {
    "2.1e": ["MA-Q-0032"],
    "2.4": ["MA-Q-0088"],
    "3.2": ["MA-Q-0030", "MA-Q-0036"],
    "3.3a": ["MA-Q-0085"],
    "4.2e": ["MA-Q-0059", "MA-Q-0060"],
    "4.4": ["MA-Q-0087"],
}

# Pre-Batch3 Coverage T2 tranche, mapped to the atomic each item was authored against.
T2_PROMOTIONS = {
    "1.1a": ["MA-Q-0224"],
    "1.2b": ["MA-Q-0211"],
    "1.2c": ["MA-Q-0212"],
    "2.3a": ["MA-Q-0213"],
    "2.4": ["MA-Q-0225"],
    "4.2c": ["MA-Q-0214"],
    "4.3": ["MA-Q-0215"],
    "4.4": ["MA-Q-0226"],
    "4.5a": ["MA-Q-0216"],
    "4.5b": ["MA-Q-0217"],
    "4.5c": ["MA-Q-0218"],
    "4.5d": ["MA-Q-0219"],
    "4.6": ["MA-Q-0220"],
    "4.7b": ["MA-Q-0221"],
    "4.7c": ["MA-Q-0222"],
    "4.7d": ["MA-Q-0223"],
}

# Pre-Batch3 T3 diversity tranche (Issue #86). These two items do not open a new atomic
# competency: they add a second scenario family to two headlines that already had direct
# atomic coverage but rested on a single family after T2.
T3_PROMOTIONS = {
    "4.3": ["MA-Q-0227"],
    "4.6": ["MA-Q-0228"],
}

# Batch 3 diversity promotion (Issue #91). Headline 2.2 lost its second scenario family when
# MA-Q-0172 was contained pending an authority reaudit, leaving the headline resting on
# MA-Q-0145 alone. MA-Q-0174 is a released, independently audited SATA in a different family,
# B2_DRUG_TESTOSTERONE_INDICATION, and it adjudicates the same competency from a different
# angle: whether a pharmacist may administer a product turns on the INDICATION, so prescribed
# testosterone for gender-affirming care is within the statutory administration category while
# the same product for routine hypogonadism is not. That is a distinct scenario shape rather
# than a second pass over the category list, which is what the diversity rule is asking for.
# MA-Q-0171 was considered first and set aside: it is a near-twin of MA-Q-0145 in form and
# would satisfy the count without satisfying the point.
BATCH3_PROMOTIONS = {
    "2.2": ["MA-Q-0174"],
}

# From-scratch semantic corrections to the frozen baseline. Issue #40 requires the final
# gate to re-derive direct support rather than inherit a delta, so a baseline row that
# genuinely has direct current evidence is corrected here with an explicit justification.
FROM_SCRATCH_CORRECTIONS = {
    "2.3b": {
        "question_ids": ["MA-Q-0086"],
        "justification": (
            "MA-Q-0086 is a released SATA whose entire stem asks which Massachusetts "
            "documentation statements are correct after a patient declines the offer to "
            "counsel. Its keyed choices adjudicate recording the failure to accept the offer, "
            "the permitted record systems (patient profile, prescription signature log, or "
            "another system) and the statutory presumption when no refusal is recorded, and it "
            "carries the direct MA-COUNSELING-DOCUMENTATION rule. That is direct evidence for "
            "'Documentation of counseling/offer', not a peripheral mention. The frozen baseline "
            "listed MA-Q-0086 only as a 2.3a salvage candidate while it was still AUDIT_PENDING; "
            "the independent Auditor-A T2 realism finding separately confirmed that MA-Q-0086 "
            "'expressly tests the same permitted record locations'."
        ),
    }
}


def git_blob_json(blob_sha: str) -> dict:
    raw = subprocess.check_output(["git", "cat-file", "blob", blob_sha], cwd=ROOT)
    return json.loads(raw.decode("utf-8"))


def head_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def headline_of(atomic_id: str) -> str:
    return atomic_id[:-1] if atomic_id[-1].isalpha() else atomic_id


class Bank:
    def __init__(self) -> None:
        self.questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
        self.rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
        _, self.audits = validate_audits()
        self.style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
        self.blueprint = load_json(DATA / "blueprint.json")
        self._usable: dict[str, dict] = {}

    def released(self, question_id: str) -> bool:
        question = self.questions.get(question_id)
        return bool(
            question
            and question.get("verification_status") == "RELEASED"
            and question.get("lifecycle_status") == "RELEASED"
        )

    def release_usable(self, question_id: str) -> dict | None:
        """Return current-hash evidence for a question, or None with a recorded reason."""
        if question_id in self._usable:
            return self._usable[question_id] or None
        question = self.questions.get(question_id)
        if question is None or not self.released(question_id):
            self._usable[question_id] = {}
            return None
        problems: list[str] = []
        if question.get("duplicate_review_status") != "CLEAR":
            problems.append("duplicate review not CLEAR")
        if question.get("independent_audit_status") != "PASSED":
            problems.append("independent audit status not PASSED")
        if (question.get("final_adjudication") or {}).get("decision") != "KEEP":
            problems.append("final adjudication not KEEP")

        current_hash = question_audit_hash(question)
        legal, realism = None, None
        for audit_id in question.get("audits", []):
            audit = self.audits.get(audit_id)
            if audit is None or audit.get("question_hashes", {}).get(question_id) != current_hash:
                continue
            if not audit.get("independent") or audit.get("audit_status") != "FULLY_ADJUDICATED":
                continue
            result = next(
                (item for item in audit.get("results", []) if item.get("Question_ID") == question_id), None
            )
            if result is None:
                continue
            if audit.get("review_type") == "LEGAL_VERIFICATION":
                if result.get("Verdict") == "KEEP" and result.get("Existing_Answer_Correct") == "YES":
                    legal = audit_id
            elif audit.get("review_type") == "REALISM_REVIEW":
                if (
                    audit.get("style_profile") == style_profile_snapshot(self.style_profile)
                    and result.get("Verdict") == "KEEP"
                    and result.get("Realism_Verdict") == "PASS"
                ):
                    realism = audit_id
        if legal is None:
            problems.append("no current-hash independent legal KEEP/YES")
        if realism is None:
            problems.append("no current-hash independent realism KEEP/PASS")
        if problems:
            self._usable[question_id] = {}
            return None
        evidence = {
            "question_id": question_id,
            "family_id": question.get("family_id"),
            "area": question.get("area"),
            "question_hash": current_hash,
            "audit_legal": legal,
            "audit_realism": realism,
            "last_legal_review": question.get("last_legal_review"),
            "dependency_snapshot": (question.get("final_adjudication") or {}).get("verified_dependencies"),
        }
        self._usable[question_id] = evidence
        return evidence


def build_rows(bank: Bank, baseline: dict) -> list[dict]:
    rows = []
    for baseline_row in baseline["rows"]:
        atomic_id = baseline_row["atomic_id"]
        evidence: dict[str, dict] = {}
        origins: dict[str, str] = {}
        rejected: list[dict] = []

        def consider(question_id: str, origin: str) -> None:
            usable = bank.release_usable(question_id)
            if usable is None:
                rejected.append({"question_id": question_id, "origin": origin, "reason": "not release-usable"})
                return
            if question_id not in evidence:
                evidence[question_id] = usable
                origins[question_id] = origin

        for item in baseline_row["selected_release_evidence"]:
            consider(item if isinstance(item, str) else item["question_id"], "BASELINE_SELECTED")
        for item in baseline_row["legacy_salvage_candidates"]:
            consider(item if isinstance(item, str) else item["question_id"], "BASELINE_SALVAGE_PROMOTED")
        for question_id in POST_T1_PROMOTIONS.get(atomic_id, []):
            consider(question_id, "POST_T1_PROMOTION")
        for question_id in T2_PROMOTIONS.get(atomic_id, []):
            consider(question_id, "T2_PROMOTION")
        for question_id in T3_PROMOTIONS.get(atomic_id, []):
            consider(question_id, "T3_PROMOTION")
        for question_id in BATCH3_PROMOTIONS.get(atomic_id, []):
            consider(question_id, "BATCH3_DIVERSITY_PROMOTION")
        correction = FROM_SCRATCH_CORRECTIONS.get(atomic_id)
        if correction:
            for question_id in correction["question_ids"]:
                consider(question_id, "FROM_SCRATCH_CORRECTION")

        selected = [evidence[question_id] | {"origin": origins[question_id]} for question_id in sorted(evidence)]
        rows.append(
            {
                "atomic_id": atomic_id,
                "nabp_area": baseline_row["nabp_area"],
                "label": baseline_row["label"],
                "baseline_semantic_status": baseline_row["semantic_status"],
                "direct_release_usable_count": len(selected),
                "status": "PASS" if selected else "FAIL_NO_DIRECT_RELEASE_USABLE_EVIDENCE",
                "selected_release_evidence": selected,
                "rejected_candidates": rejected,
                "from_scratch_correction": correction["justification"] if correction else None,
            }
        )
    return rows


def build_headlines(rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[headline_of(row["atomic_id"])].append(row)

    headlines = []
    for headline in sorted(grouped, key=lambda item: (item.split(".")[0], int(item.split(".")[1]))):
        group = grouped[headline]
        families = sorted(
            {
                item["family_id"]
                for row in group
                for item in row["selected_release_evidence"]
            }
        )
        failed_atomics = [row["atomic_id"] for row in group if row["status"] != "PASS"]
        if failed_atomics:
            status = "FAIL_ATOMIC_COVERAGE"
        elif len(families) < FAMILY_DIVERSITY_MINIMUM:
            status = "FAIL_FAMILY_DIVERSITY"
        else:
            status = "PASS"
        headlines.append(
            {
                "headline": headline,
                "atomic_ids": [row["atomic_id"] for row in group],
                "failed_atomic_ids": failed_atomics,
                "distinct_families": families,
                "family_count": len(families),
                "status": status,
                "exception_justification": None,
            }
        )
    return headlines


def build_mock(bank: Bank) -> dict:
    """Construct one concrete blueprint-faithful 120-question mock with no reuse."""
    by_area: dict[int, list[dict]] = defaultdict(list)
    for question_id in sorted(bank.questions):
        usable = bank.release_usable(question_id)
        if usable:
            by_area[usable["area"]].append(usable)

    selection: dict[int, list[str]] = {}
    shortfalls: dict[int, int] = {}
    used: set[str] = set()
    for area, required in REQUIRED_AREA_ALLOCATION.items():
        pool = by_area.get(area, [])
        # Round-robin across families first so the mock is not family-saturated.
        by_family: dict[str, list[dict]] = defaultdict(list)
        for item in pool:
            by_family[item["family_id"]].append(item)
        ordered: list[dict] = []
        rank = 0
        while len(ordered) < len(pool):
            for family_id in sorted(by_family):
                bucket = by_family[family_id]
                if rank < len(bucket):
                    ordered.append(bucket[rank])
            rank += 1
        chosen = [item["question_id"] for item in ordered if item["question_id"] not in used][:required]
        used.update(chosen)
        selection[area] = chosen
        if len(chosen) < required:
            shortfalls[area] = required - len(chosen)

    all_selected = [question_id for area in sorted(selection) for question_id in selection[area]]
    family_counts = Counter(bank.questions[question_id]["family_id"] for question_id in all_selected)
    return {
        "required_area_allocation": {str(area): count for area, count in REQUIRED_AREA_ALLOCATION.items()},
        "release_usable_area_counts": {str(area): len(by_area.get(area, [])) for area in sorted(REQUIRED_AREA_ALLOCATION)},
        "release_usable_total": sum(len(items) for items in by_area.values()),
        "slack_by_area": {
            str(area): len(by_area.get(area, [])) - required
            for area, required in REQUIRED_AREA_ALLOCATION.items()
        },
        "shortfalls_by_area": {str(area): count for area, count in shortfalls.items()},
        "assembled_count": len(all_selected),
        "no_reuse_verified": len(all_selected) == len(set(all_selected)),
        "blueprint_faithful_120_without_reuse": not shortfalls and len(all_selected) == MOCK_SIZE,
        "max_family_repeat_in_mock": max(family_counts.values()) if family_counts else 0,
        "selection_by_area": {str(area): selection[area] for area in sorted(selection)},
    }


def build_taxonomy_gate(bank: Bank, baseline: dict) -> dict:
    known = {
        "MA-Q-0085": 3,
        "MA-Q-0087": 4,
        "MA-Q-0088": 2,
    }
    resolved = {}
    unresolved = []
    for question_id, required_area in known.items():
        current_area = bank.questions[question_id]["area"]
        status = "RESOLVED" if current_area == required_area else "UNRESOLVED"
        resolved[question_id] = {"required_area": required_area, "current_area": current_area, "status": status}
        if status == "UNRESOLVED":
            unresolved.append(question_id)
    return {
        "known_prior_mismatches": resolved,
        "unresolved_known_mismatches": unresolved,
        "formal_cross_area_mappings_retained": len(baseline["formal_taxonomy_mappings"]),
    }


def build_manifest(bank: Bank, matrix: dict, matrix_path: Path) -> dict:
    """Freeze the exact evidence this verdict rests on so the run is reproducible."""
    evidence_hashes: dict[str, str] = {}
    evidence_audits: dict[str, dict] = {}
    rule_hashes: dict[str, dict] = {}
    for row in matrix["rows"]:
        for item in row["selected_release_evidence"]:
            question_id = item["question_id"]
            evidence_hashes[question_id] = item["question_hash"]
            evidence_audits[question_id] = {
                "legal": item["audit_legal"],
                "realism": item["audit_realism"],
            }
            for rule_id, snapshot in ((item["dependency_snapshot"] or {}).get("rules") or {}).items():
                rule_hashes[rule_id] = snapshot

    return {
        "manifest_type": "POST_T3_PRE_BATCH3_FINAL_GATE_MANIFEST",
        "gate": GATE_ID,
        "gate_issue": GATE_ISSUE,
        "controller_issue": CONTROLLER_ISSUE,
        "verdict": matrix["verdict"],
        "batch3": matrix["batch3"],
        "frozen_source": {
            "branch": "remediation/pre-batch3-legacy-salvage-t1",
            "sha": matrix["source_sha"],
            "role": "final post-T3 canonical release state audited by this gate",
        },
        "frozen_baseline_matrix": matrix["frozen_baseline_matrix"],
        "artifact_sha256": {
            matrix_path.relative_to(ROOT).as_posix(): file_sha256(matrix_path),
            "scripts/prebatch3_final_coverage_gate.py": file_sha256(Path(__file__).resolve()),
        },
        "release_context_hashes": {
            "blueprint": {
                "id": bank.blueprint.get("blueprint_id"),
                "content_version": bank.blueprint.get("content_version"),
                "content_hash": bank.blueprint.get("content_hash"),
            },
            "style_profile": style_profile_snapshot(bank.style_profile),
        },
        "evidence_question_count": len(evidence_hashes),
        "evidence_question_hashes": dict(sorted(evidence_hashes.items())),
        "evidence_audit_ids": dict(sorted(evidence_audits.items())),
        "evidence_rule_hashes": dict(sorted(rule_hashes.items())),
        "mock_selection_hash": deterministic_hash(matrix["mock_capacity"]["selection_by_area"]),
        "gate_fail_reasons": matrix["gate_fail_reasons"],
        "reproduce": [
            "git checkout " + matrix["source_sha"],
            "python scripts/validate_all.py",
            "python -m pytest -q",
            "python scripts/generate_artifacts.py --write && git diff --exit-code",
            "python scripts/prebatch3_final_coverage_gate.py",
        ],
    }


def file_sha256(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    baseline = git_blob_json(BASELINE_MATRIX_BLOB)
    if baseline.get("atomic_count") != 46 or len(baseline["rows"]) != 46:
        raise SystemExit("frozen baseline matrix does not contain exactly 46 atomic rows")

    bank = Bank()
    rows = build_rows(bank, baseline)
    headlines = build_headlines(rows)
    mock = build_mock(bank)
    taxonomy = build_taxonomy_gate(bank, baseline)

    failed_atomics = [row["atomic_id"] for row in rows if row["status"] != "PASS"]
    diversity_debt = [item["headline"] for item in headlines if item["status"] == "FAIL_FAMILY_DIVERSITY"]

    fail_reasons: list[str] = []
    if failed_atomics:
        fail_reasons.append(
            f"{len(failed_atomics)} of 46 atomic competencies lack qualifying direct "
            f"release-usable coverage: {', '.join(failed_atomics)}"
        )
    for area, shortfall in mock["shortfalls_by_area"].items():
        fail_reasons.append(
            f"Area {area} release-usable count "
            f"{mock['release_usable_area_counts'][area]} is below required "
            f"{mock['required_area_allocation'][area]} by {shortfall}"
        )
    if not mock["blueprint_faithful_120_without_reuse"]:
        fail_reasons.append("no blueprint-faithful 120-question mock can be assembled without reuse")
    for headline in diversity_debt:
        fail_reasons.append(f"headline family-diversity debt: {headline}")
    if taxonomy["unresolved_known_mismatches"]:
        fail_reasons.append(f"unresolved taxonomy mismatches: {taxonomy['unresolved_known_mismatches']}")

    verdict = "PASS" if not fail_reasons else "FAIL"
    matrix = {
        "gate": GATE_ID,
        "gate_issue": GATE_ISSUE,
        "controller_issue": CONTROLLER_ISSUE,
        "representation": "FULL_FROM_SCRATCH_RECOMPUTATION_AT_EXACT_POST_T3_SHA",
        "audit_date": "2026-08-19",
        "source_sha": head_sha(),
        "nabp_profile": NABP_PROFILE,
        "frozen_baseline_matrix": {
            "path": BASELINE_MATRIX_PATH,
            "matrix_commit": BASELINE_MATRIX_COMMIT,
            "git_blob_sha": BASELINE_MATRIX_BLOB,
            "role": "immutable 46-atomic competency definitions and prior semantic evidence",
        },
        "prior_post_t1_gate_source_sha": POST_T1_MATRIX_SOURCE_SHA,
        "prior_post_t2_gate_source_sha": "860ec67308772ac63073ed62a7ebdcc565921183",
        "atomic_count": len(rows),
        "atomic_pass_count": len(rows) - len(failed_atomics),
        "atomic_fail_count": len(failed_atomics),
        "failed_atomic_ids": failed_atomics,
        "rows": rows,
        "headline_family_diversity": headlines,
        "headline_family_diversity_debt": diversity_debt,
        "taxonomy_gate": taxonomy,
        "mock_capacity": mock,
        "gate_fail_reasons": fail_reasons,
        "verdict": verdict,
        "batch3": "UNLOCKED" if verdict == "PASS" else "BLOCKED",
        "methodology": [
            "The immutable frozen 46-row baseline matrix supplies the atomic competency definitions.",
            "Every atomic row is recomputed: baseline evidence is carried forward only while the exact "
            "question is still release-usable, salvage candidates are promoted only once released, the "
            "T2 tranche is mapped to the atomic each item was authored against, and any from-scratch "
            "correction records an explicit written justification.",
            "Release-usable means RELEASED, duplicate-clear, final-KEEP, plus current-hash independent "
            "legal KEEP/YES and realism KEEP/PASS against the current style profile.",
            "Headline family diversity requires at least two distinct families unless a written narrow "
            "exception exists; no exception is claimed by this run.",
            "Mock capacity uses the current canonical area field and assembles one concrete 26/40/29/25 "
            "selection, verifying no question is reused.",
        ],
    }

    output = ROOT / "audits" / "coverage" / "2026-08-19" / "POST-T3-PRE-BATCH3-FINAL-COVERAGE-MATRIX.json"
    write_json(output, matrix)

    manifest_path = ROOT / "audits" / "coverage" / "2026-08-19" / "POST-T3-PRE-BATCH3-FINAL-GATE-MANIFEST.json"
    write_json(manifest_path, build_manifest(bank, matrix, output))

    print(f"source SHA: {matrix['source_sha']}")
    print(f"atomic: {matrix['atomic_pass_count']}/46 PASS, {matrix['atomic_fail_count']} FAIL")
    if failed_atomics:
        print(f"  failed atomics: {failed_atomics}")
    print(f"release-usable by area: {mock['release_usable_area_counts']} (required {mock['required_area_allocation']})")
    print(f"slack by area: {mock['slack_by_area']}")
    print(f"120-question mock without reuse: {mock['blueprint_faithful_120_without_reuse']}")
    print(f"headline family-diversity debt: {diversity_debt or 'none'}")
    print(f"taxonomy unresolved: {taxonomy['unresolved_known_mismatches'] or 'none'}")
    print()
    for reason in fail_reasons:
        print(f"FAIL REASON: {reason}")
    print(f"VERDICT: {verdict}  (Batch 3: {matrix['batch3']})")
    print(f"matrix: {output.relative_to(ROOT).as_posix()}")
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
