"""One-time deterministic source enrollment. Never writes a public bank or queue.

The immutable registry is a code-reviewed enrollment, not an automatic draft importer.
Re-running requires identical source outputs; extending scope requires a separate batch.
"""

import copy
import json
from pathlib import Path
import subprocess
import sys
import remediation_batch_registry as b

BASE_COMMIT = "4e5f150cc60908386d52fdbaeaae33351a1a5144"


def write_once(root, path, value):
    raw = b.encoded(value)
    p = root / path
    if p.exists():
        b.require(
            p.read_bytes() == raw, "Enrollment would rewrite immutable file: " + path
        )
    else:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(raw)
    return b.sha(raw)


def enroll(root=b.ROOT):
    root = Path(root)
    scan = b.scan_reservations(root, BASE_COMMIT)
    ids = b.next_ids(scan["reserved_ids"], 10)
    bank = b.read(root, b.BASE + "/questions.json")
    selection = b.read(root, b.BASE + "/selection.json")
    parents = b.parent_records(root)
    rows = []
    for pid, qid in zip(b.PARENTS, ids):
        v2 = pid in {"MA-EXP-0515", "MA-EXP-0827"}
        prefix = b.G2 if v2 else b.G1
        draft_path = (
            prefix
            + "/drafts/P9-REPAIR-"
            + pid.removeprefix("MA-")
            + ("-v2.json" if v2 else "-v1.json")
        )
        draft = b.read(root, draft_path)
        hold = next(
            h
            for h in selection["safety_holds" if pid.startswith("MA-REV-") else "holds"]
            if h.get("question_id", h.get("legacy_question_id")) == pid
        )
        report = b.F2 if v2 else b.F1
        rows.append(
            dict(
                question_id=qid,
                original_question_id=pid,
                original_record_sha256=b.digest(parents[pid]),
                parent_hold=copy.deepcopy(hold),
                draft_key=draft["draft_key"],
                draft_path=draft_path,
                draft_raw_sha256=b.sha((root / draft_path).read_bytes()),
                visible_content_sha256=draft["visible_content_sha256"],
                author_commit=b.G2_COMMIT if v2 else b.G1_COMMIT,
                independent_commit=b.F2_COMMIT if v2 else b.F1_COMMIT,
                independent_report_path=report,
                independent_report_sha256=b.sha((root / report).read_bytes()),
            )
        )
    # Actual existing delivery from the unchanged base is captured before adding authoring.
    from publish_practice import build_payload

    published = build_payload()
    b.require(
        len(published["questions"]) == 2349,
        "Enrollment base must be actual2349 delivery",
    )
    delivered = dict(
        schema_version="remediation-published-baseline/1",
        base_commit=BASE_COMMIT,
        record_hashes={q["question_id"]: b.digest(q) for q in published["questions"]},
        source_hashes={sid: b.digest(s) for sid, s in published["sources"].items()},
        public_activation=False,
        canonical_release_credit=0,
    )
    published_sha = write_once(root, b.PUBLISHED_BASELINE, delivered)
    protected = [
        *b.PUBLIC_BANKS[:3],
        b.OLD_ALLOCATION,
        "docs/RELEASE_POLICY.md",
        "docs/AUDIT_WORKFLOW.md",
        "docs/SOURCE_USE_POLICY.md",
        "docs/QUESTION_AUTHORING_STANDARD.md",
        "reports/representative-rewrite/sata-remediation/author-review-consumer-baseline.json",
        "reports/full-corpus-review/sata-remediation-current-id-author-sources.json",
    ]
    protected += [
        str(p.relative_to(root))
        for p in sorted((root / b.BASE / "authoring").glob("*.json"))
        if p.name != "11_phase9_remediation10.json"
    ]
    # Every retained original native-author53 report and independent29 report stays byte-bound.
    for registry in [
        "reports/full-corpus-review/sata-remediation-current-id-author-sources.json"
    ]:
        protected += [x["report_path"] for x in b.read(root, registry)["sources"]]
    independent = b.read(
        root, "reports/full-corpus-review/independent-legacy-work-queue.json"
    )
    old29 = next(j for j in independent["jobs"] if j["sequence"] == 29)
    protected += [r["evidence_path"] for r in old29["result"]["results"]]
    a = dict(
        schema_version="remediation-batch-allocation/1",
        batch_id=b.BATCH_ID,
        base_commit=BASE_COMMIT,
        reservation_scan=scan,
        allocations=rows,
        retention_sha256=b.sha((root / b.RETENTION).read_bytes()),
        protected_file_sha256s={
            p: b.sha((root / p).read_bytes()) for p in sorted(set(protected))
        },
        prior_representative_question_hashes={
            q["question_id"]: b.digest(q) for q in bank["questions"]
        },
        prior_representative_source_hashes={
            sid: b.digest(s) for sid, s in bank["sources"].items()
        },
        published2349_baseline_sha256=published_sha,
        archive_only=True,
        current_id_author_sequence=54,
        original_parent_holds_preserved=True,
        author_review_credit=0,
        independent_review_credit=0,
        canonical_release_credit=0,
    )
    allocation_sha = write_once(root, b.ALLOCATION, a)
    payload = b._authoring_from_allocation(root, a)
    authoring_sha = write_once(root, b.AUTHORING, payload)
    from build_representative_rewrites import compile_authored_items

    guide = b.read(root, "notes/guide.json")
    sources = {
        sid: dict(
            copy.deepcopy(s),
            id=sid,
            url=s["official_url"],
            source_class="PUBLIC_OFFICIAL",
        )
        for sid, s in payload["sources"].items()
    }
    compiled = compile_authored_items(
        payload["questions"],
        {
            q["question_id"]: (payload["authored_at"], payload["edition"])
            for q in payload["questions"]
        },
        sources,
        guide,
        parents,
        root,
    )
    state = b.read(root, "reports/full-corpus-review/work-queue.json")
    b.require(
        len(state["jobs"]) == 53
        and all(j["status"] == "INTEGRATED" for j in state["jobs"]),
        "Enrollment requires exact completed nativeauthor53 parent",
    )
    old_native = b.read(
        root,
        "reports/representative-rewrite/sata-remediation/author-review-consumer-baseline.json",
    )
    baseline = dict(
        schema_version="remediation-batch-current-id-baseline/1",
        batch_id=b.BATCH_ID,
        base_commit=BASE_COMMIT,
        candidate_question_hashes={q["question_id"]: b.digest(q) for q in compiled},
        new_source_hashes={sid: b.digest(s) for sid, s in sources.items()},
        required_author_provenance=b.canonical_actor(
            b.read(root, rows[0]["draft_path"])["author_provenance"]
        ),
        required_native_author_sequence=54,
        original_53_job_hashes=[b.digest(j) for j in state["jobs"]],
        original_event_hashes=[b.digest(e) for e in state["events"]],
        static_review_files=old_native["static_review_files"],
        static_source_sha256=old_native["static_source_sha256"],
        original_independent_job29_sha256=b.digest(old29),
        native_author_review_credit=0,
        native_independent_review_credit=0,
        canonical_release_credit=0,
    )
    baseline_sha = write_once(root, b.CURRENT_BASELINE, baseline)
    registry = dict(
        schema_version="immutable-remediation-batches/1",
        batches=[
            dict(
                batch_id="original-sata-three",
                allocation_path=b.OLD_ALLOCATION,
                allocation_sha256=b.OLD_ALLOCATION_SHA,
                native_author_sequence=53,
                current_id_count=3,
            ),
            dict(
                batch_id=b.BATCH_ID,
                allocation_path=b.ALLOCATION,
                allocation_sha256=allocation_sha,
                authoring_path=b.AUTHORING,
                authoring_sha256=authoring_sha,
                current_id_baseline_path=b.CURRENT_BASELINE,
                current_id_baseline_sha256=baseline_sha,
                native_author_sequence=54,
                current_id_count=10,
            ),
        ],
    )
    registry_sha = write_once(root, b.REGISTRY, registry)
    print(
        json.dumps(
            dict(
                ids=ids,
                reservation_max=scan["reserved_ids"][-1],
                allocation_sha256=allocation_sha,
                authoring_sha256=authoring_sha,
                current_baseline_sha256=baseline_sha,
                registry_sha256=registry_sha,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    enroll()
