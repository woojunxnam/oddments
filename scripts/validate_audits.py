from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

from qa_common import DATA, SCHEMAS, QAReport, index_records, load_records, print_report, validate_schema_records


TARGETED_INITIAL_BATCH_AUTHORIZATIONS = {
    "PRE-BATCH3-COVERAGE-T2": {
        "authorizing_issue": 68,
        "represented_candidate_sha": "b849159ef18d37618ca6badf886e465502436e1b",
        "question_ids": frozenset(f"MA-Q-{index:04d}" for index in range(211, 227)),
    },
    # Issue #86 governance amendment: the two new bank-admission candidates that close the
    # measured headline family-diversity debt for 4.3 and 4.6 take their first fresh
    # independent canonical audit as TARGETED_INITIAL_BATCH rather than REAUDIT.
    "PRE-BATCH3-COVERAGE-T3-DIVERSITY": {
        "authorizing_issue": 86,
        "represented_candidate_sha": "f13c91c2635ea153a1ea19d9dfb34bcbe12f30c2",
        "question_ids": frozenset({"MA-Q-0227", "MA-Q-0228"}),
    },
    # Issue #91 governance amendment: the 16-question B3-F top-up consists of new
    # bank-admission candidates but is below the ordinary 30-question INITIAL_BATCH minimum.
    "BATCH3-B3F": {
        "authorizing_issue": 91,
        "represented_candidate_sha": "1cc76f458f6584edc3dfad8387240ea968201b64",
        "question_ids": frozenset(f"MA-Q-{index:04d}" for index in range(391, 407)),
    },
    # Issue #196: exact focused11 source-lock and current hashes; scope only.
    "FOCUSED-MPJE336-FOCUSED11": {
        "authorizing_issue": 196,
        "represented_candidate_sha": "40905fc1b895e2254f0a979f6d87e2f7e474021c",
        "question_ids": frozenset({
            "MA-Q-0441",
            "MA-Q-0446",
            "MA-Q-0448",
            "MA-Q-0451",
            "MA-Q-0452",
            "MA-Q-0453",
            "MA-Q-0456",
            "MA-Q-0459",
            "MA-Q-0461",
            "MA-Q-0465",
            "MA-Q-0468",
        }),
        "question_hashes": {
            "MA-Q-0441": "4fc702e7e02938457b0af345e38c0162371cb8c528179be5425a7a95ee7e81ad",
            "MA-Q-0446": "b18989503ce0edd87ef3cd4b79b8f50cbfe566191a0a526f5427c266430093f0",
            "MA-Q-0448": "3c4c8135761b4e208a7140cef7708dde10856f64018f081db5f50c411c8b04d3",
            "MA-Q-0451": "34bda60837330705badc801838713229d646778ffeb6fe18be46fa99cc177be9",
            "MA-Q-0452": "835adcd1f23f0321039dae094234831105550a7a91fa3ad30be41df700a960a4",
            "MA-Q-0453": "5b677d3ac2d38b2fbdcde25b0d7c0737ca864888f0127e20fb7a67bd2471d3d8",
            "MA-Q-0456": "11131c31be205b22c34607ca84567245bd665c11169aaf430e9b98ff00473d63",
            "MA-Q-0459": "afc59770277751e2d4afa76f8a26737dc4b6a5a0d1af4cfbe29ede6d79ae8f95",
            "MA-Q-0461": "9d28d6e3aabf5416217d9e7a40efc4afee641a4932b79e9c0caa1c533ea1a95e",
            "MA-Q-0465": "1d05ea3862897d2cddff4e302ccd7ea447f66fbf51ba428dc954ca4aa670a894",
            "MA-Q-0468": "c121ac08b6232b2f5d3d4471cad3fb6232b920d98731aeecb3eedf6fa7f893f6",
        },
    },
}
GIT_SHA_PATTERN = re.compile(r"^[a-f0-9]{40}$")


def _valid_official_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def _targeted_initial_governance_errors(audit: dict) -> list[str]:
    if audit.get("audit_scope") != "TARGETED_INITIAL_BATCH":
        return []

    errors: list[str] = []
    authorization = audit.get("governance_authorization")
    if not isinstance(authorization, dict):
        return ["TARGETED_INITIAL_BATCH requires governance_authorization"]

    tranche_id = authorization.get("tranche_id")
    governed = TARGETED_INITIAL_BATCH_AUTHORIZATIONS.get(tranche_id)
    if governed is None:
        return [f"TARGETED_INITIAL_BATCH tranche {tranche_id!r} is not governance-authorized"]

    if authorization.get("authorizing_issue") != governed["authorizing_issue"]:
        errors.append(
            f"TARGETED_INITIAL_BATCH tranche {tranche_id} must be authorized by issue "
            f"{governed['authorizing_issue']}"
        )

    represented_candidate_sha = authorization.get("represented_candidate_sha")
    if not isinstance(represented_candidate_sha, str) or not GIT_SHA_PATTERN.fullmatch(represented_candidate_sha):
        errors.append("TARGETED_INITIAL_BATCH represented_candidate_sha must be a 40-character lowercase Git SHA")
    elif represented_candidate_sha != governed["represented_candidate_sha"]:
        errors.append(
            f"TARGETED_INITIAL_BATCH tranche {tranche_id} represented_candidate_sha does not match governance authorization"
        )

    authorization_question_ids = authorization.get("question_ids")
    if not isinstance(authorization_question_ids, list):
        errors.append("TARGETED_INITIAL_BATCH governance authorization question_ids must be an array")
    else:
        authorization_set = set(authorization_question_ids)
        if authorization_set != governed["question_ids"]:
            errors.append(
                f"TARGETED_INITIAL_BATCH tranche {tranche_id} governance authorization question_ids do not match the exact authorized set"
            )
        if authorization_set != set(audit.get("question_ids", [])):
            errors.append(
                "TARGETED_INITIAL_BATCH governance authorization question_ids must exactly match audit question_ids"
            )

    if "question_hashes" in governed and audit.get("question_hashes") != governed["question_hashes"]:
        errors.append(
            f"TARGETED_INITIAL_BATCH tranche {tranche_id} question_hashes do not match the exact authorized hashes"
        )

    return errors


def is_valid_targeted_initial_audit(audit: dict) -> bool:
    if audit.get("audit_scope") != "TARGETED_INITIAL_BATCH":
        return False
    if _targeted_initial_governance_errors(audit):
        return False
    if audit.get("independent") is not True or audit.get("audit_status") != "FULLY_ADJUDICATED":
        return False
    question_ids = audit.get("question_ids", [])
    if not isinstance(question_ids, list) or not 1 <= len(question_ids) < 30:
        return False
    question_id_set = set(question_ids)
    result_ids = [result.get("Question_ID") for result in audit.get("results", []) if isinstance(result, dict)]
    if len(result_ids) != len(set(result_ids)) or set(result_ids) != question_id_set:
        return False
    if set(audit.get("question_hashes", {})) != question_id_set:
        return False
    return True


def validate_audits(
    known_question_ids: set[str] | None = None,
    data_root: Path | None = None,
) -> tuple[QAReport, dict[str, dict]]:
    report = QAReport()
    records = load_records((data_root or DATA) / "audits")
    validate_schema_records(records, SCHEMAS / "audit.schema.json", report)
    audits = index_records(records, "audit_id", report)

    for path, audit in records:
        question_ids = audit.get("question_ids", [])
        result_ids = [result.get("Question_ID") for result in audit.get("results", [])]
        hash_ids = set(audit.get("question_hashes", {}))
        if len(result_ids) != len(set(result_ids)):
            report.error(f"{path}: duplicate Question_ID in results")
        if set(question_ids) != set(result_ids):
            report.error(f"{path}: question_ids and results Question_ID sets must match exactly")
        if set(question_ids) != hash_ids:
            report.error(f"{path}: question_ids and question_hashes keys must match exactly")
        if known_question_ids is not None:
            for question_id in sorted(set(question_ids) - known_question_ids):
                report.error(f"{path}: unknown question ID {question_id}")

        for message in _targeted_initial_governance_errors(audit):
            report.error(f"{path}: {message}")

        if audit.get("audit_status") != "FULLY_ADJUDICATED":
            continue
        for result in audit.get("results", []):
            question_id = result.get("Question_ID", "<missing>")
            if audit.get("review_type") == "LEGAL_VERIFICATION":
                if result.get("Existing_Answer_Correct") == "NOT_ASSESSED":
                    report.error(f"{path}: {question_id} is fully adjudicated but answer was not assessed")
                authorities = result.get("authorities", [])
                if not authorities:
                    report.error(f"{path}: {question_id} is fully adjudicated but lacks authorities")
                for index, authority in enumerate(authorities):
                    label = f"{question_id} authority[{index}]"
                    for field in ("authority", "source_type", "exact_section", "law_checked_date"):
                        value = authority.get(field)
                        if value is None or not str(value).strip():
                            report.error(f"{path}: {label} lacks {field}")
                    if not _valid_official_url(authority.get("official_url")):
                        report.error(f"{path}: {label} has invalid official_url")
            elif audit.get("review_type") == "REALISM_REVIEW":
                criteria = result.get("Criteria", {})
                if result.get("Realism_Verdict") == "PASS" and not all(criteria.values()):
                    report.error(f"{path}: {question_id} realism PASS requires every criterion to pass")
    return report, audits


def main() -> int:
    report, _ = validate_audits()
    return print_report("audits", report)


if __name__ == "__main__":
    raise SystemExit(main())
