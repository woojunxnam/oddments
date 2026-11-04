"""Exact native author54 consumer for the registered ten-candidate batch.

Draft G/F reviews and compilation never create credit. Runtime uses HEAD-retained
sources and native queue events, and never fetches an old worker Git object.
"""

from __future__ import annotations
import copy
import json
from pathlib import Path
import re
from datetime import datetime
import remediation_author_reviews as old
import remediation_batch_registry as batch

ROOT = batch.ROOT
REGISTRY = (
    "reports/full-corpus-review/remediation-batch-p9-ten-current-id-author-sources.json"
)
PREFIX = "reports/full-corpus-review/remediation-batch-p9-ten-current-id-author/"
SCHEMA = "remediation-batch-current-id-author-review/1"
QUEUE = old.QUEUE
require = old.require
sha = old.sha
digest = old.digest
read_head = old.read_head
expected_actor = old.expected_actor


def read_baseline(root):
    return batch.current_baseline(root)


def candidate_records(root):
    root = Path(root)
    baseline = read_baseline(root)
    authored = batch.authoring_payload(root)
    bank = batch.read(root, batch.BASE + "/questions.json")
    result = {
        q["question_id"]: q
        for q in bank["questions"]
        if q["question_id"] in baseline["candidate_question_hashes"]
    }
    require(
        len(result) == 10
        and {qid: digest(q) for qid, q in result.items()}
        == baseline["candidate_question_hashes"],
        "New batch requires exactly ten frozen current-ID records; regenerate inventory",
    )
    authored_by_id = {q["question_id"]: q for q in authored["questions"]}
    require(
        all(
            q.get("archive_only_candidate") is True
            and q["remediation_candidate"]
            == authored_by_id[qid]["remediation_candidate"]
            for qid, q in result.items()
        ),
        "Unbound batch author candidate",
    )
    require(
        expected_actor(result) == baseline["required_author_provenance"],
        "Changed batch content author",
    )
    return result


def validate_submission(job, result):
    require(
        job.get("current_id_author_batch_id") == batch.BATCH_ID
        and job.get("sequence") == 54
        and job.get("required_author_actor_id") == batch.G_ACTOR,
        "Only registered native author54 may review the ten candidates",
    )
    old._validate_submission(job, result, count=10, prefix=PREFIX)


def validate_report(root, job, result, raw, questions):
    validate_submission(job, result)
    require(
        set(questions) == set(read_baseline(root)["candidate_question_hashes"]),
        "Unregistered native author report IDs",
    )
    return old._validate_report(
        root, job, result, raw, questions, count=10, schema=SCHEMA
    )


def validate_parent(root, baseline, static_review_files=None):
    if static_review_files is not None:
        require(
            list(static_review_files) == baseline["static_review_files"],
            "Original static author source set changed",
        )
    for path, h in baseline["static_source_sha256"].items():
        require(
            sha((root / path).read_bytes()) == h,
            "Original63 author source bytes changed: " + path,
        )
    state = batch.read(root, QUEUE)
    from review_queue import state_stage

    require(state_stage(state) == "author", "Wrong native author queue stage")
    require(
        [digest(j) for j in state["jobs"][:53]] == baseline["original_53_job_hashes"]
        and [
            digest(e) for e in state["events"][: len(baseline["original_event_hashes"])]
        ]
        == baseline["original_event_hashes"],
        "Original53 author jobs/events changed",
    )
    return state


def load_sources(root=ROOT, static_review_files=None):
    root = Path(root)
    if batch.load_registry(root) is None:
        return {}
    baseline = read_baseline(root)
    state = validate_parent(root, baseline, static_review_files)
    if not (root / REGISTRY).exists():
        return {}  # absent or LEASED/SUBMITTED54 is pending, never credited
    read_head(root, batch.CURRENT_BASELINE)
    read_head(root, batch.REGISTRY)
    registry = json.loads(read_head(root, REGISTRY))
    require(
        registry.get("schema_version") == "remediation-batch-native-author-sources/1"
        and registry.get("batch_id") == batch.BATCH_ID
        and isinstance(registry.get("sources"), list)
        and len(registry["sources"]) == 1,
        "Only one exact native author54 source registration is allowed",
    )
    questions = candidate_records(root)
    read_head(root, batch.BASE + "/questions.json")
    read_head(root, QUEUE)
    source = registry["sources"][0]
    jobs = [j for j in state["jobs"] if j["job_id"] == source["job_id"]]
    require(len(jobs) == 1, "Unknown/duplicate batch native author job")
    job = jobs[0]
    require(
        job["sequence"] == 54
        and len(state["jobs"]) >= 54
        and state["jobs"][53] == job
        and job["status"] == "INTEGRATED"
        and all(j["status"] == "INTEGRATED" for j in state["jobs"][:53]),
        "Native54 credit requires sequential integration after original53",
    )
    require(
        job["question_hashes"] == {qid: digest(q) for qid, q in questions.items()}
        and job["job_id"] == "review-" + digest(job["question_hashes"])[:16],
        "Stale native54 current-record bindings",
    )
    require(
        job.get("selection_policy") == "CURRENT_ID_AUTHOR_REVIEW_REQUIRED",
        "Unmarked native54 author job",
    )
    result = job["result"]
    from review_queue import validate_result

    validate_result(job, result)
    validate_submission(job, result)
    require(
        all(
            r["evidence_path"] == source["report_path"]
            and r["evidence_sha256"] == source["report_sha256"]
            for r in result["results"]
        ),
        "Native54 registry differs from submitted evidence",
    )
    require(source["report_path"].startswith(PREFIX), "Unsafe native54 report path")
    raw = read_head(root, source["report_path"])
    require(sha(raw) == source["report_sha256"], "Native54 report raw SHA mismatch")
    events = state["events"]
    plan = [
        i
        for i, e in enumerate(events)
        if e["kind"] == "PLAN" and job["job_id"] in e.get("job_ids", [])
    ]
    claims = [
        i
        for i, e in enumerate(events)
        if e["kind"] == "CLAIM"
        and e.get("job_id") == job["job_id"]
        and e.get("worker") == job["worker"]
        and e.get("attempt") == job["attempt"]
    ]
    submits = [
        i
        for i, e in enumerate(events)
        if e["kind"] == "SUBMIT"
        and e.get("job_id") == job["job_id"]
        and e.get("result_sha256") == digest(result)
    ]
    integrations = [
        i
        for i, e in enumerate(events)
        if e["kind"] == "INTEGRATE"
        and e.get("job_id") == job["job_id"]
        and e.get("commit") == job.get("integrated_commit")
    ]
    require(
        len(plan) == len(claims) == len(submits) == len(integrations) == 1
        and plan[0] < claims[0] < submits[0] < integrations[0],
        "Missing/invalid native54 plan-claim-submit-integration chain",
    )
    require(
        type(job.get("attempt")) is int and job["attempt"] >= 1,
        "Invalid native54 attempt",
    )
    require(
        events[plan[0]].get("selection_policy")
        == "CURRENT_ID_AUTHOR_REVIEW_REQUIRED_THEN_LEXICAL",
        "Native54 PLAN policy missing",
    )
    require(
        job.get("lease_token")
        == digest(
            dict(
                job=job["job_id"],
                worker=job["worker"],
                attempt=job["attempt"],
                at=events[claims[0]]["at"],
            )
        )
        and job.get("worker_branch")
        == "mission/" + job["job_id"] + "-attempt-" + str(job["attempt"])
        and job.get("created_at") == events[plan[0]]["at"]
        and job.get("submitted_at") == events[submits[0]]["at"]
        and job.get("integrated_at") == events[integrations[0]]["at"],
        "Invalid native54 claim/lease/provenance binding",
    )
    require(
        datetime.fromisoformat(job["created_at"])
        <= datetime.fromisoformat(events[claims[0]]["at"])
        <= datetime.fromisoformat(job["submitted_at"])
        <= datetime.fromisoformat(job["integrated_at"])
        and datetime.fromisoformat(job["submitted_at"])
        <= datetime.fromisoformat(job["lease_until"]),
        "Invalid native54 chronology",
    )
    report = validate_report(root, job, result, raw, questions)
    by_id = {r["question_id"]: r for r in report["records"]}
    for row in result["results"]:
        require(
            row["disposition"]
            == (
                "AUTHOR_REVIEWED"
                if by_id[row["question_id"]]["disposition"] == "KEEP"
                else by_id[row["question_id"]]["disposition"]
            ),
            "Native54 result/report disposition differs",
        )
    return {source["report_path"].removeprefix("reports/full-corpus-review/"): report}


def apply_review(row, question, root=ROOT):
    for path, source in load_sources(root).items():
        matches = [
            r for r in source["records"] if r["question_id"] == question["question_id"]
        ]
        if not matches:
            continue
        review = matches[0]
        for key in (
            "disposition",
            "legal_review_status",
            "choice_by_choice_findings",
            "reviewer_provenance",
            "checked_at",
            "blocker",
        ):
            row[key] = copy.deepcopy(review[key])
        row.update(
            current_id_author_review_required=False,
            author_review_increment=1,
            checked_at_scope="FORMAL_NATIVE_CURRENT_ID_AUTHOR_REVIEW",
            native_author_review_job_id=source["job_id"],
            review_evidence=dict(
                source_path="reports/full-corpus-review/" + path,
                source_sha256=sha(
                    (Path(root) / "reports/full-corpus-review" / path).read_bytes()
                ),
                native_author_job_id=source["job_id"],
                review_record_sha256=digest(review),
            ),
            answer_key_assessment=(
                "NOT_ASSESSED_SOURCE_BLOCKED"
                if review["author_expected_choice_ids"] is None
                else "FORMAL_CURRENT_ID_AUTHOR_EXPECTED_KEY_RECORDED"
            ),
            authority_clauses=[
                f["exact_authority"]
                for f in review["choice_by_choice_findings"].values()
            ],
            next_action="Different eligible actual session must audit compiled current IDs independently.",
            independent_review_credit=0,
            canonical_release_credit=0,
        )


def bind_candidate_inventory_row(row, question, root=ROOT):
    baseline = read_baseline(root)
    qid = question["question_id"]
    require(
        qid in baseline["candidate_question_hashes"]
        and digest(question) == baseline["candidate_question_hashes"][qid],
        "Stale/unallocated new remediation inventory",
    )
    # The registry has already verified authoring bytes and the complete current
    # record hash; reconstructing all ten drafts for every row adds no binding.
    a = batch.read(root, batch.AUTHORING)
    binding = question["remediation_candidate"]
    require(
        binding
        == next(
            q["remediation_candidate"]
            for q in a["questions"]
            if q["question_id"] == qid
        )
        and binding["current_id_independent_audit"] == "PENDING"
        and question["independent_legal_audit"]
        is question["independent_realism_audit"]
        is None,
        "New candidate cannot inherit compiled-ID audit",
    )
    row.update(
        disposition="AUDIT_PENDING",
        legal_review_status=old.STATUS,
        checked_at=None,
        checked_at_scope="FORMAL_CURRENT_ID_AUTHOR_REVIEW_REQUIRED",
        source_author_review_date=a["authored_at"],
        current_id_author_review_required=True,
        current_id_author_batch_id=batch.BATCH_ID,
        source_author_review_binding=copy.deepcopy(binding),
        known_author_editor_actor_ids=list(batch.EXCLUDED),
        reviewer_provenance=dict(
            author_session=batch.G_ACTOR,
            engineering_provenance=batch.ENGINEER,
            independent="NOT_RUN_FOR_COMPILED_ID",
        ),
        implementation_status="ARCHIVE_ONLY_REPLACEMENT_CANDIDATE",
        blocker="Native current-ID author54 and different actual-session independent review pending; parent HOLD/default unchanged.",
        next_action="Assign actual G a native author54 current-ID review first.",
        answer_key_assessment="EXACT_G_DRAFT_KEY_COPY_NOT_NEW_ENGINEERING_ASSESSMENT",
        author_review_increment=0,
        independent_review_credit=0,
        canonical_release_credit=0,
    )
    apply_review(row, question, root)


def validate_independent_candidates(root, ledger, candidates):
    """A forged checked_at/row flag is insufficient to schedule this source batch."""
    if batch.load_registry(root) is None:
        return
    new = set(read_baseline(root)["candidate_question_hashes"]) & set(candidates)
    if not new:
        return
    sources = load_sources(root)
    require(
        len(sources) == 1,
        "Native author54 evidence must be integrated before independent planning",
    )
    path, report = next(iter(sources.items()))
    by_id = {r["question_id"]: r for r in report["records"]}
    source_sha = sha((Path(root) / "reports/full-corpus-review" / path).read_bytes())
    for qid in new:
        row = ledger[qid]
        require(
            row.get("current_id_author_batch_id") == batch.BATCH_ID
            and row.get("current_id_author_review_required") is False
            and row.get("checked_at_scope") == "FORMAL_NATIVE_CURRENT_ID_AUTHOR_REVIEW"
            and row.get("native_author_review_job_id") == report["job_id"]
            and row.get("author_review_increment") == 1
            and row.get("checked_at") == by_id[qid]["checked_at"]
            and row.get("review_evidence", {}).get("source_sha256") == source_sha
            and row.get("review_evidence", {}).get("review_record_sha256")
            == digest(by_id[qid])
            and row.get("review_evidence", {}).get("native_author_job_id")
            == report["job_id"]
            and row.get("review_evidence", {}).get("source_path")
            == "reports/full-corpus-review/" + path
            and row.get("known_author_editor_actor_ids") == list(batch.EXCLUDED),
            "Unbound native54 ledger eligibility",
        )
