"""Deterministic representation transform of the immutable Auditor-A T2 evidence.

Issue #83 PHASE A. This script is a *governance transformer only*: it converts the
already-accepted `GPT-FRESH-COV-T2-A` legal and full-bank realism artifacts (PR #71,
accepted head 5b5ca7b15fcdcca186d7b6758f7f8d180e613bc3) into the post-PR81 canonical
audit schema without making a new substantive judgment.

It never re-audits, never adds an authority, never changes a criterion and never
converts the historical pre-repair MA-Q-0213 realism failure into a pass. The source
artifacts are read straight from Git by their exact immutable blob SHAs so the
transform cannot silently drift onto different evidence.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, write_json


# ---------------------------------------------------------------------------
# Immutable Auditor-A source identities (Issue #83)
# ---------------------------------------------------------------------------
AUDITOR_INSTANCE = "GPT-FRESH-COV-T2-A"
ACCEPTED_AUDIT_PR = 71
ACCEPTED_AUDIT_HEAD = "5b5ca7b15fcdcca186d7b6758f7f8d180e613bc3"
REPRESENTED_CANDIDATE_SHA = "b849159ef18d37618ca6badf886e465502436e1b"
AUDIT_DATE = "2026-08-18"

PHASE1_LOCK_BLOB = "38e0da2165d42add508b65eed995f40447aa9b8f"
PHASE1_LOCK_SHA256 = "16071c19e5089ad08366f45a12c87fceea273ee327880437dfafe8448e3f715c"
PHASE1_LOCK_PATH = "audits/remediation/2026-08-18/GPT-FRESH-COV-T2-A-PHASE1-LOCK.json"
LEGAL_BLOB = "cc152b7b34f8f0dd5d2393700c855b4e9c44219c"
LEGAL_PATH = "audits/remediation/2026-08-18/GPT-FRESH-COV-T2-A-LEGAL-VERIFICATION.json"
REALISM_BLOB = "625a3944a47bfb38492be8d3a5b9342868c817ad"
REALISM_PATH = "audits/remediation/2026-08-18/GPT-FRESH-COV-T2-A-FULL-BANK-REALISM-REVIEW.json"

LEGAL_AUDIT_ID = "AUDIT-GPT-FRESH-COV-T2-A-LEGAL-TARGETED-INITIAL-2026-08-18"
REALISM_AUDIT_ID = "AUDIT-GPT-FRESH-COV-T2-A-REALISM-TARGETED-INITIAL-2026-08-18"

TRANCHE_ID = "PRE-BATCH3-COVERAGE-T2"
AUTHORIZING_ISSUE = 68
QUESTION_IDS = [f"MA-Q-{index:04d}" for index in range(211, 227)]

STYLE_PROFILE = {
    "profile_id": "MPJE-MA-PRE2027",
    "content_version": 1,
    "content_hash": "293be8fdcd39af2255a22a0423b7123d5cfcf7c0e6c561872eb0ef04e745015c",
}

# Exact original Auditor-A question hashes. MA-Q-0213 intentionally keeps the
# historical pre-repair hash so the accepted realism FAIL stays bound to the exact
# content that failed and can never be silently re-attached to repaired content.
ORIGINAL_QUESTION_HASHES = {
    "MA-Q-0211": "0e64b008982afd70481d5cbb98764c33333b9575abf880225d2c342b62e84b30",
    "MA-Q-0212": "804b1f109276192cd626f3d609fc627003e619aa1eed23c39b0d1945b4a20682",
    "MA-Q-0213": "993eee2f3d84d3532d757924fa22421c93a7cf16d69b26d40d5f660ca3624548",
    "MA-Q-0214": "35a7f054480e5c46f8aa3293f30e3ad3716e5f2786ecb6bc741d0068868c94c6",
    "MA-Q-0215": "60cacb955e6fef4d02699c6b3b80f869920551d484dbb9afe8bd1114b911f685",
    "MA-Q-0216": "a59cab0514d45b1e1d10f67e9c01c8d78fda5309abb469c156a37dbd8078f2e5",
    "MA-Q-0217": "e4a5cdd5a5189c56ec9946cfaed177350c425fddff1d17451ea0ceb73399cd66",
    "MA-Q-0218": "ad1ee83f096695440b0068e5989fd8997af7c92020a25fb5d4b6d40b10d036ab",
    "MA-Q-0219": "6caa187601ecc06d17efb4dfa295df327d9fd2f08e9ef60d0027ef215e3a98f3",
    "MA-Q-0220": "72dfe8a9eb2a34ebf251327d80bf8046eec880650ba3070160c8a37d999bc47e",
    "MA-Q-0221": "97d16d872b91e45425ccca675c25cd35bdd9bde85168a4d44c396c95610c6921",
    "MA-Q-0222": "ea4d8ab19e3e1e54132ca076842ce21d47779152c5e0652e6575892454baa571",
    "MA-Q-0223": "857eca7ddc6176091b9ab209244613cb80cb47ae03f10aea48299bab527e5a11",
    "MA-Q-0224": "b4fe81e97a7a555753af73ea9d9f65be6b8d889ddb074ee52ebfaadd66dd96d9",
    "MA-Q-0225": "1cacd9445f05b72dfb15015db5c9d26faee59649a5db714e1e0ec1e236e91444",
    "MA-Q-0226": "7afaf435fff0676352d13f668e5873e3376c902ba96ee0160a83c48d539b29d9",
}
HISTORICAL_Q0213_FAILURE_HASH = ORIGINAL_QUESTION_HASHES["MA-Q-0213"]

# Deterministic source-verdict/severity mapping. Nothing here re-scores an item:
# each entry only renames an already-recorded judgment into the canonical enum.
SEVERITY_MAP = {"NONE": "Low", "MINOR": "Low", "MODERATE": "Medium", "MAJOR": "High", "CRITICAL": "Critical"}
VERDICT_MAP = {
    "KEEP": "KEEP",
    "MINOR_EDIT": "MINOR_EDIT",
    "REWRITE": "MAJOR_REWRITE",
    "MAJOR_REWRITE": "MAJOR_REWRITE",
    "DELETE": "DELETE",
}
CRITERION_MAP = {"PASS": True, "FAIL": False}
PROVENANCE_NOTE = (
    "Deterministic canonical representation of immutable Auditor-A evidence "
    f"(instance {AUDITOR_INSTANCE}, accepted audit PR #{ACCEPTED_AUDIT_PR}, accepted head "
    f"{ACCEPTED_AUDIT_HEAD}). No new substantive audit judgment was made."
)


def git_blob(blob_sha: str) -> bytes:
    return subprocess.check_output(["git", "cat-file", "blob", blob_sha], cwd=ROOT)


def load_immutable_source(blob_sha: str, expected_sha256: str | None = None) -> dict:
    raw = git_blob(blob_sha)
    digest = hashlib.sha256(raw).hexdigest()
    if expected_sha256 is not None and digest != expected_sha256:
        raise SystemExit(f"immutable source {blob_sha} sha256 {digest} != expected {expected_sha256}")
    return json.loads(raw.decode("utf-8"))


def classify_source_type(title: str, url: str) -> str:
    """Classify an authority strictly from the title/URL Auditor A already recorded.

    Anything that cannot be classified without substantive interpretation falls back
    to OTHER_OFFICIAL rather than inventing or researching a replacement source.
    """
    host = (urlparse(url).netloc or "").casefold()
    path = (urlparse(url).path or "").casefold()
    if host.endswith("malegislature.gov"):
        return "MA_STATUTE"
    if host.endswith("mass.gov") and "/247-cmr-" in path:
        return "MA_PROMULGATED_REGULATION"
    if "policy 20" in title.casefold():
        return "MA_BOARD_POLICY"
    if "drug control program" in title.casefold():
        return "MA_DCP_GUIDANCE"
    return "OTHER_OFFICIAL"


def normalize_authority(source_authority: dict) -> dict:
    title = source_authority["title"]
    url = source_authority["url"]
    return {
        "authority": title,
        "source_type": classify_source_type(title, url),
        # No more granular section field exists in the immutable artifact, so the
        # exact recorded source title/section is carried through unchanged.
        "exact_section": title,
        "official_url": url,
        "law_checked_date": AUDIT_DATE,
    }


def join_proposed_answer(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ",".join(str(item) for item in value)
    return str(value)


def empty_if_absent(value: object) -> str:
    return "" if value is None else str(value)


def build_legal_audit(source: dict) -> dict:
    results = []
    for source_result in source["results"]:
        question_id = source_result["Question_ID"]
        results.append(
            {
                "Question_ID": question_id,
                "Verdict": VERDICT_MAP[source_result["Verdict"]],
                "Severity": SEVERITY_MAP[source_result["Severity"]],
                "Existing_Answer_Correct": source_result["Existing_Answer_Correct"],
                "authorities": [normalize_authority(item) for item in source_result["authorities"]],
                "Problem": source_result["Problem"],
                "Proposed_Answer": join_proposed_answer(source_result.get("Proposed_Answer")),
                "Proposed_Rewrite": empty_if_absent(source_result.get("Proposed_Rewrite")),
                "Proposed_Explanation": empty_if_absent(source_result.get("Proposed_Explanation")),
            }
        )
    return {
        "audit_id": LEGAL_AUDIT_ID,
        "auditor": "GPT",
        "auditor_instance": AUDITOR_INSTANCE,
        "audit_date": AUDIT_DATE,
        "audit_scope": "TARGETED_INITIAL_BATCH",
        "review_type": "LEGAL_VERIFICATION",
        "independent": True,
        "audit_status": "FULLY_ADJUDICATED",
        "governance_authorization": {
            "tranche_id": TRANCHE_ID,
            "authorizing_issue": AUTHORIZING_ISSUE,
            "represented_candidate_sha": REPRESENTED_CANDIDATE_SHA,
            "question_ids": list(QUESTION_IDS),
        },
        "question_ids": list(QUESTION_IDS),
        "question_hashes": {question_id: ORIGINAL_QUESTION_HASHES[question_id] for question_id in QUESTION_IDS},
        "results": results,
    }


def build_realism_notes(source_result: dict) -> str:
    notes = source_result["Notes"].strip()
    closest = source_result.get("closest_relevant_comparison_question_ids") or []
    if closest:
        notes = f"{notes} Closest canonical-bank comparison question IDs: {', '.join(closest)}."
    if source_result["Question_ID"] == "MA-Q-0213":
        notes = (
            f"{notes} HISTORICAL PRE-REPAIR EVIDENCE: this accepted Auditor-A finding is recorded "
            f"against the original MA-Q-0213 content hash {HISTORICAL_Q0213_FAILURE_HASH} only. It is "
            "deliberately retained as a valid failed-audit record and is not applied to the repaired "
            "current MA-Q-0213 content, which carries separate current-hash Auditor-B evidence."
        )
    return notes


def build_realism_audit(source: dict) -> dict:
    results = []
    for source_result in source["results"]:
        criteria = {key: CRITERION_MAP[value] for key, value in source_result["Criteria"].items()}
        results.append(
            {
                "Question_ID": source_result["Question_ID"],
                "Verdict": VERDICT_MAP[source_result["Verdict"]],
                "Severity": SEVERITY_MAP[source_result["Severity"]],
                "Realism_Verdict": source_result["Realism_Verdict"],
                "Reviewed_Date": source_result["Reviewed_Date"],
                "Criteria": criteria,
                "Notes": build_realism_notes(source_result),
            }
        )
    return {
        "audit_id": REALISM_AUDIT_ID,
        "auditor": "GPT",
        "auditor_instance": AUDITOR_INSTANCE,
        "audit_date": AUDIT_DATE,
        "audit_scope": "TARGETED_INITIAL_BATCH",
        "review_type": "REALISM_REVIEW",
        "independent": True,
        "audit_status": "FULLY_ADJUDICATED",
        "governance_authorization": {
            "tranche_id": TRANCHE_ID,
            "authorizing_issue": AUTHORIZING_ISSUE,
            "represented_candidate_sha": REPRESENTED_CANDIDATE_SHA,
            "question_ids": list(QUESTION_IDS),
        },
        "style_profile": dict(STYLE_PROFILE),
        "question_ids": list(QUESTION_IDS),
        "question_hashes": {question_id: ORIGINAL_QUESTION_HASHES[question_id] for question_id in QUESTION_IDS},
        "results": results,
    }


def assert_transform_is_faithful(legal_source: dict, realism_source: dict, legal: dict, realism: dict) -> None:
    """Fail closed if the transform ever changed a substantive judgment."""
    legal_by_id = {item["Question_ID"]: item for item in legal_source["results"]}
    realism_by_id = {item["Question_ID"]: item for item in realism_source["results"]}
    if sorted(legal_by_id) != QUESTION_IDS or sorted(realism_by_id) != QUESTION_IDS:
        raise SystemExit("immutable Auditor-A evidence does not cover exactly MA-Q-0211..MA-Q-0226")

    for result in legal["results"]:
        source_result = legal_by_id[result["Question_ID"]]
        if result["Verdict"] != VERDICT_MAP[source_result["Verdict"]]:
            raise SystemExit(f"{result['Question_ID']}: legal verdict drift")
        if result["Existing_Answer_Correct"] != source_result["Existing_Answer_Correct"]:
            raise SystemExit(f"{result['Question_ID']}: answer-correct drift")
        if result["Problem"] != source_result["Problem"]:
            raise SystemExit(f"{result['Question_ID']}: Problem text drift")
        source_urls = [item["url"] for item in source_result["authorities"]]
        if [item["official_url"] for item in result["authorities"]] != source_urls:
            raise SystemExit(f"{result['Question_ID']}: authority set drift")

    for result in realism["results"]:
        source_result = realism_by_id[result["Question_ID"]]
        if result["Realism_Verdict"] != source_result["Realism_Verdict"]:
            raise SystemExit(f"{result['Question_ID']}: realism verdict drift")
        expected = {key: CRITERION_MAP[value] for key, value in source_result["Criteria"].items()}
        if result["Criteria"] != expected:
            raise SystemExit(f"{result['Question_ID']}: realism criterion drift")
        if not source_result["Notes"].strip() or source_result["Notes"].strip() not in result["Notes"]:
            raise SystemExit(f"{result['Question_ID']}: realism note text was not preserved")

    q0213_legal = next(item for item in legal["results"] if item["Question_ID"] == "MA-Q-0213")
    q0213_realism = next(item for item in realism["results"] if item["Question_ID"] == "MA-Q-0213")
    if legal["question_hashes"]["MA-Q-0213"] != HISTORICAL_Q0213_FAILURE_HASH:
        raise SystemExit("MA-Q-0213 legal evidence must stay bound to the original pre-repair hash")
    if realism["question_hashes"]["MA-Q-0213"] != HISTORICAL_Q0213_FAILURE_HASH:
        raise SystemExit("MA-Q-0213 realism evidence must stay bound to the original pre-repair hash")
    if q0213_legal["Verdict"] != "KEEP" or q0213_legal["Existing_Answer_Correct"] != "YES":
        raise SystemExit("MA-Q-0213 legal judgment drift")
    if (
        q0213_realism["Verdict"] != "MAJOR_REWRITE"
        or q0213_realism["Severity"] != "High"
        or q0213_realism["Realism_Verdict"] != "FAIL"
        or q0213_realism["Criteria"]["distinct_from_bank"] is not False
    ):
        raise SystemExit("the historical MA-Q-0213 realism failure must be preserved exactly")
    other_criteria = {key: value for key, value in q0213_realism["Criteria"].items() if key != "distinct_from_bank"}
    if not all(other_criteria.values()):
        raise SystemExit("only distinct_from_bank failed in the original MA-Q-0213 realism evidence")

    passing = [item for item in realism["results"] if item["Question_ID"] != "MA-Q-0213"]
    if len(passing) != 15 or not all(
        item["Verdict"] == "KEEP" and item["Severity"] == "Low" and item["Realism_Verdict"] == "PASS"
        for item in passing
    ):
        raise SystemExit("the 15 original Auditor-A realism passes must map to KEEP / Low / PASS")


def build_provenance_report(legal: dict, realism: dict) -> dict:
    return {
        "report_type": "T2_AUDITOR_A_CANONICAL_REPRESENTATION_TRANSFORM",
        "controller_issue": 83,
        "superseded_issue_for_implementation_mechanics": 82,
        "transformer": "Claude Code governance controller",
        "transformer_is_auditor": False,
        "statement": (
            "This is a deterministic, non-substantive representation transform of immutable "
            "Auditor-A evidence into the post-PR81 canonical audit schema. The transformer made no "
            "new legal or realism judgment, added no authority, changed no criterion, and did not "
            "convert the historical pre-repair MA-Q-0213 realism failure into a pass."
        ),
        "auditor": "GPT",
        "auditor_instance": AUDITOR_INSTANCE,
        "accepted_audit_pr": ACCEPTED_AUDIT_PR,
        "accepted_audit_head": ACCEPTED_AUDIT_HEAD,
        "represented_candidate_sha": REPRESENTED_CANDIDATE_SHA,
        "immutable_sources": {
            PHASE1_LOCK_PATH: {"git_blob_sha": PHASE1_LOCK_BLOB, "sha256": PHASE1_LOCK_SHA256},
            LEGAL_PATH: {"git_blob_sha": LEGAL_BLOB},
            REALISM_PATH: {"git_blob_sha": REALISM_BLOB},
        },
        "canonical_records_written": {
            f"data/audits/{LEGAL_AUDIT_ID}.json": {
                "audit_id": LEGAL_AUDIT_ID,
                "audit_scope": "TARGETED_INITIAL_BATCH",
                "review_type": "LEGAL_VERIFICATION",
                "question_count": len(legal["question_ids"]),
            },
            f"data/audits/{REALISM_AUDIT_ID}.json": {
                "audit_id": REALISM_AUDIT_ID,
                "audit_scope": "TARGETED_INITIAL_BATCH",
                "review_type": "REALISM_REVIEW",
                "question_count": len(realism["question_ids"]),
            },
        },
        "governance_authorization": {
            "tranche_id": TRANCHE_ID,
            "authorizing_issue": AUTHORIZING_ISSUE,
            "represented_candidate_sha": REPRESENTED_CANDIDATE_SHA,
            "question_ids": list(QUESTION_IDS),
        },
        "deterministic_mappings": {
            "severity": SEVERITY_MAP,
            "verdict": VERDICT_MAP,
            "realism_criteria": {"PASS": True, "FAIL": False},
            "proposed_answer": 'array joined with "," in original order; null/absent -> ""',
            "authority_source_type": (
                "malegislature.gov -> MA_STATUTE; mass.gov 247 CMR regulation page -> "
                "MA_PROMULGATED_REGULATION; explicit numbered Board policy document -> MA_BOARD_POLICY; "
                "explicit Drug Control Program guidance -> MA_DCP_GUIDANCE; otherwise OTHER_OFFICIAL"
            ),
            "exact_section": "exact recorded source title (no more granular field exists in the source artifact)",
            "law_checked_date": AUDIT_DATE,
        },
        "historical_failure_preserved": {
            "question_id": "MA-Q-0213",
            "original_pre_repair_hash": HISTORICAL_Q0213_FAILURE_HASH,
            "realism_verdict": "FAIL",
            "verdict": "MAJOR_REWRITE",
            "severity": "High",
            "failed_criterion": "distinct_from_bank",
            "closest_comparison_question_ids": ["MA-Q-0086", "MA-Q-0092"],
            "deleted_or_hidden": False,
        },
        "authority_source_type_assignments": sorted(
            {
                (item["official_url"], item["source_type"])
                for result in legal["results"]
                for item in result["authorities"]
            }
        ),
    }


def main() -> int:
    legal_source = load_immutable_source(LEGAL_BLOB)
    realism_source = load_immutable_source(REALISM_BLOB)
    lock = load_immutable_source(PHASE1_LOCK_BLOB, PHASE1_LOCK_SHA256)

    for name, source in (("legal", legal_source), ("realism", realism_source), ("lock", lock)):
        if source.get("auditor") != AUDITOR_INSTANCE:
            raise SystemExit(f"{name} source auditor {source.get('auditor')!r} != {AUDITOR_INSTANCE}")
        if source.get("represented_candidate_sha") != REPRESENTED_CANDIDATE_SHA:
            raise SystemExit(f"{name} source represented_candidate_sha drift")
    if legal_source.get("phase1_lock_sha256") != PHASE1_LOCK_SHA256:
        raise SystemExit("legal source does not reference the accepted Phase-1 blind lock")
    if realism_source.get("phase1_lock_sha256") != PHASE1_LOCK_SHA256:
        raise SystemExit("realism source does not reference the accepted Phase-1 blind lock")

    legal = build_legal_audit(legal_source)
    realism = build_realism_audit(realism_source)
    assert_transform_is_faithful(legal_source, realism_source, legal, realism)

    write_json(DATA / "audits" / f"{LEGAL_AUDIT_ID}.json", legal)
    write_json(DATA / "audits" / f"{REALISM_AUDIT_ID}.json", realism)
    report_path = ROOT / "audits" / "remediation" / "2026-08-19" / "T2-AUDITOR-A-CANONICAL-TRANSFORM-PROVENANCE.json"
    write_json(report_path, build_provenance_report(legal, realism))

    print(f"wrote data/audits/{LEGAL_AUDIT_ID}.json ({len(legal['results'])} results)")
    print(f"wrote data/audits/{REALISM_AUDIT_ID}.json ({len(realism['results'])} results)")
    print(f"wrote {report_path.relative_to(ROOT).as_posix()}")
    print(PROVENANCE_NOTE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
