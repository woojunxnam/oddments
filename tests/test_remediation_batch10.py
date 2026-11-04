"""Append-only source boundaries and synthetic native54 lifecycle (not legal reviews)."""

import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import remediation_batch_registry as batch
import remediation_batch_author_reviews as native
import build_representative_rewrites as compiler
import review_queue as queue

NOW = "2026-11-04T12:00:00+00:00"


def write(root, path, value):
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(batch.encoded(value))


def git(root, *args):
    return subprocess.check_output(
        ["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL
    ).strip()


def commit(root):
    git(root, "add", ".")
    git(root, "commit", "-qm", "synthetic engineering fixture; no legal credit")
    return git(root, "rev-parse", "HEAD")


@pytest.fixture(scope="module")
def compiled():
    result = compiler.build()
    return (
        result[compiler.BASE / "questions.json"],
        result[compiler.BASE / "selection.json"],
    )


def test_deterministic_real_reservations_and_exact_two_batch_registry():
    a = batch.allocation()
    scan = a["reservation_scan"]
    assert len(batch.load_registry()["batches"]) == 2
    assert [r["question_id"] for r in a["allocations"]] == batch.next_ids(
        scan["reserved_ids"], 10
    )
    assert max(scan["reserved_ids"]) == "MA-RW-0083"
    assert any(
        "MA-RW-9999" in r["ids"] and r["allocation_effect"] == "NONALLOCATING_REFERENCE"
        for p, r in scan["all_textual_mentions"].items()
        if p.startswith("tests/")
    )
    assert batch.next_ids(["MA-RW-0090"], 2) == ["MA-RW-0091", "MA-RW-0092"]
    with pytest.raises(ValueError, match="exhausted"):
        batch.next_ids(["MA-RW-9999"], 1)
    with pytest.raises(ValueError, match="Invalid"):
        batch.next_ids(["MA-RW-10000"], 1)


def test_full_compiler_old2349_77_90_and_all40_final_characters(compiled):
    bank, selection = compiled
    a = batch.allocation()
    baseline = batch.current_baseline()
    batch.validate_compiled_bank(bank)
    assert len(bank["questions"]) == 87 and len(bank["sources"]) == 152
    assert len(selection["archive_only_replacements"]) == 13
    assert (
        selection["recommended_ids"]
        == batch.read(ROOT, batch.BASE + "/selection.json")["recommended_ids"]
    )
    assert len(selection["recommended_ids"]) == 202
    old = {
        q["question_id"]: q
        for p in batch.PUBLIC_BANKS
        for q in batch.read(ROOT, p)["questions"]
    }
    assert len(old) == 2349
    assert all(
        batch.digest(q) == a["prior_representative_question_hashes"][q["question_id"]]
        for q in batch.legacy_projection(bank)["questions"]
    )
    checked = 0
    for row, draft, f, report, parent in batch.draft_rows(ROOT, a):
        q = next(q for q in bank["questions"] if q["question_id"] == row["question_id"])
        for k in ("stem", "choices", "correct_choice_ids", "question_type"):
            assert q[k] == draft[k]
        for k, v in draft["explanation"].items():
            assert q["explanation"][k] == v
        assert q["stem"] == q["scenario"] + "\n\n" + q["lead_in"]
        assert (
            batch.digest(q) == baseline["candidate_question_hashes"][q["question_id"]]
        )
        assert q["verification_status"] == "NOT_INDEPENDENTLY_REVIEWED"
        assert (
            q["remediation_candidate"]["independent_draft_review"][
                "current_public_id_assessed"
            ]
            is False
        )
        for c in q["choices"]:
            proof = next(p for p in draft["option_proofs"] if p["choice_id"] == c["id"])
            for actual, original in zip(
                q["explanation"]["choice_authorities"][c["id"]],
                proof["authorities"],
                strict=True,
            ):
                assert {k: v for k, v in actual.items() if k != "source_id"} == {
                    k: v for k, v in original.items() if k != "source_id"
                }
                assert actual["source_id"].startswith("rm-p9-ten-")
            checked += 1
    assert checked == 40
    assert sum("/v2/" in r["draft_path"] for r in a["allocations"]) == 2
    assert not set(baseline["candidate_question_hashes"]) & set(
        selection["recommended_ids"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        "old_question",
        "old_source",
        "new_key",
        "new_Korean",
        "new_primary",
        "unknown_ID",
        "parent_mapping",
        "release",
    ],
)
def test_compiler_refuses_any_old_or_new_binding_drift(compiled, mutation):
    bank = copy.deepcopy(compiled[0])
    new = next(q for q in bank["questions"] if q["question_id"] == "MA-RW-0084")
    if mutation == "old_question":
        bank["questions"][0]["history_policy"] = "MIGRATE"
    elif mutation == "old_source":
        bank["sources"][next(iter(bank["sources"]))]["changed"] = True
    elif mutation == "new_key":
        new["correct_choice_ids"] = ["D"]
    elif mutation == "new_Korean":
        new["explanation"]["core_reasoning"] += " "
    elif mutation == "new_primary":
        bank["sources"][new["source_ids"][0]]["raw_sha256"] = "0" * 64
    elif mutation == "unknown_ID":
        bank["questions"].append(dict(new, question_id="MA-RW-0094"))
    elif mutation == "parent_mapping":
        new["revision_of"] = "MA-REV-0001"
    elif mutation == "release":
        new["publication_status"] = "RELEASED"
    with pytest.raises(ValueError):
        batch.validate_compiled_bank(bank)


@pytest.fixture(scope="module")
def template(tmp_path_factory, compiled):
    root = tmp_path_factory.mktemp("batch10-native-template")
    a = batch.allocation()
    baseline = batch.current_baseline()
    paths = set(a["protected_file_sha256s"]) | set(baseline["static_source_sha256"])
    paths |= {x["path"] for x in batch.read(ROOT, batch.RETENTION)["files"]}
    paths |= {
        batch.REGISTRY,
        batch.ALLOCATION,
        batch.CURRENT_BASELINE,
        batch.RETENTION,
        batch.AUTHORING,
        batch.PUBLISHED_BASELINE,
        native.QUEUE,
        batch.BASE + "/selection.json",
        "site/practice-expansion/publication.json",
    }
    for r in a["allocations"]:
        h = r["parent_hold"]
        paths.add(h.get("review_source", h.get("evidence_report")))
    for p in paths:
        dest = root / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / p, dest)
    write(root, batch.BASE + "/questions.json", compiled[0])
    write(root, batch.BASE + "/selection.json", compiled[1])
    config = batch.read(root, "site/practice-expansion/publication.json")
    config["representative_selection"]["sha256"] = batch.sha(
        (root / batch.BASE / "selection.json").read_bytes()
    )
    write(root, "site/practice-expansion/publication.json", config)
    git(root, "init", "-q")
    git(root, "config", "user.name", "Synthetic fixture")
    git(root, "config", "user.email", "fixture@example.test")
    commit(root)
    return root


@pytest.fixture
def repo(template, tmp_path):
    root = tmp_path / "repo"
    subprocess.run(
        ["git", "clone", "-q", "--shared", str(template), str(root)], check=True
    )
    git(root, "config", "user.name", "Synthetic fixture")
    git(root, "config", "user.email", "fixture@example.test")
    state = batch.read(root, native.QUEUE)
    # All old53 assigned records remain credited; only new10 need an author job.
    ledger = {
        qid: dict(
            question_id=qid,
            content_sha256=h,
            collection=batch.BASE + "/questions.json",
            checked_at="2026-11-04",
            legal_review_status="AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT",
            independent_legacy_legal_assessment={
                "synthetic_fixture_ineligible_old_record": True
            },
        )
        for j in state["jobs"]
        for qid, h in j["question_hashes"].items()
    }
    questions = native.candidate_records(root)
    for qid, q in questions.items():
        row = dict(
            question_id=qid,
            content_sha256=batch.digest(q),
            collection=batch.BASE + "/questions.json",
        )
        native.bind_candidate_inventory_row(row, q, root)
        ledger[qid] = row
    p = root / "reports/full-corpus-review/question-ledger.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in ledger.values()) + "\n")
    primary = native.PREFIX + "evidence/synthetic-primary.txt"
    (root / primary).parent.mkdir(parents=True, exist_ok=True)
    (root / primary).write_text("SYNTHETIC ENGINEERING TEST ONLY; NOT LAW.\n")
    url = "https://www.mass.gov/doc/synthetic-engineering-fixture/download"
    metadata = native.PREFIX + "evidence/synthetic-retrieval.json"
    write(
        root,
        metadata,
        dict(
            official_url=url,
            raw_sha256=batch.sha((root / primary).read_bytes()),
            http_status=200,
        ),
    )
    authority = dict(
        official_url=url,
        exact_section="SYNTHETIC TEST SECTION NOT LEGAL PROOF",
        law_checked_date="2026-11-04",
        version_or_effective_date_status="SYNTHETIC FIXTURE",
        body_verified_current_primary=True,
        http_status=200,
        used_as_legal_proof=True,
        raw_path=primary,
        raw_sha256=batch.sha((root / primary).read_bytes()),
        retrieval_metadata_path=metadata,
        retrieval_metadata_sha256=batch.sha((root / metadata).read_bytes()),
    )
    commit(root)
    return root, state, ledger, questions, authority


def complete(repo, register=True):
    root, state, ledger, questions, authority = repo
    queue.plan(state, ledger, root, size=10, at=NOW)
    job = queue.claim(state, batch.G_ACTOR, at=NOW)
    actor = native.expected_actor(questions)
    records = [
        dict(
            question_id=qid,
            record_sha256=batch.digest(q),
            checked_at="2026-11-04",
            disposition="KEEP",
            legal_review_status="AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT",
            blocker="",
            current_ID_stem_all_choices_key_all_Korean_explanations_read=True,
            author_expected_choice_ids=q["correct_choice_ids"],
            reviewer_provenance=dict(actor, independent=False),
            choice_by_choice_findings={
                c["id"]: dict(
                    original_choice_text=c["text"],
                    expected_true=c["id"] in q["correct_choice_ids"],
                    finding_ko="실제 법률 판정이 아닌 합성 engineering fixture 검증이다.",
                    exact_authority="SYNTHETIC TEST SECTION",
                    authorities=[copy.deepcopy(authority)],
                )
                for c in q["choices"]
            },
        )
        for qid, q in questions.items()
    ]
    report = dict(
        schema_version=native.SCHEMA,
        stage="author",
        job_id=job["job_id"],
        actor_provenance=actor,
        canonical_audit=False,
        canonical_release_credit=0,
        independent_of_authors=False,
        independent_review_credit=0,
        records=records,
    )
    path = native.PREFIX + "synthetic-g-author54.json"
    write(root, path, report)
    worker = commit(root)
    h = batch.sha((root / path).read_bytes())
    result = dict(
        stage="author",
        job_id=job["job_id"],
        actor_provenance=actor,
        canonical_audit=False,
        canonical_release_credit=0,
        independent_review_credit=0,
        independent_of_authors=False,
        question_hashes=job["question_hashes"],
        worker_commit=worker,
        results=[
            dict(
                question_id=qid,
                disposition="AUTHOR_REVIEWED",
                evidence_path=path,
                evidence_sha256=h,
            )
            for qid in questions
        ],
    )
    queue.submit(state, job["job_id"], job["lease_token"], result, at=NOW)
    queue.integrate(state, job["job_id"], root, at=NOW)
    write(root, native.QUEUE, state)
    if register:
        write(
            root,
            native.REGISTRY,
            dict(
                schema_version="remediation-batch-native-author-sources/1",
                batch_id=batch.BATCH_ID,
                sources=[dict(job_id=job["job_id"], report_path=path, report_sha256=h)],
            ),
        )
    commit(root)
    return job, report, path


def test_pending_native54_all10_atomic_G_only_and_no_independent_or_credit(repo):
    root, state, ledger, questions, _ = repo
    assert native.load_sources(root) == {}
    for qid in questions:
        assert (
            ledger[qid]["author_review_increment"] == 0
            and ledger[qid]["checked_at"] is None
        )
    assert (
        queue.plan(
            queue.empty("independent-legacy"),
            {qid: ledger[qid] for qid in questions},
            root,
            size=10,
            at=NOW,
        )
        == []
    )
    with pytest.raises(ValueError, match="exactly all ten"):
        queue.plan(state, ledger, root, size=9, at=NOW)
    queue.plan(state, ledger, root, size=10, at=NOW)
    job = state["jobs"][-1]
    assert (
        job["sequence"] == 54
        and job["current_id_author_batch_id"] == batch.BATCH_ID
        and set(job["question_hashes"]) == set(questions)
    )
    assert queue.plan(state, ledger, root, size=10, at=NOW) == []
    for actor in (batch.E_ACTOR, batch.F_ACTOR, "/root"):
        with pytest.raises(ValueError, match="Required content author"):
            queue.claim(state, actor, at=NOW)
    assert (
        queue.claim(state, batch.G_ACTOR, at=NOW)["required_author_actor_id"]
        == batch.G_ACTOR
    )
    assert native.load_sources(root) == {}


def test_only_integrated_registered_G54_can_credit_and_next_priority_excludes_authors(
    repo,
):
    root, state, ledger, questions, _ = repo
    job, _, _ = complete(repo)
    assert len(native.load_sources(root)) == 1
    rows = {}
    for qid, q in questions.items():
        row = dict(
            question_id=qid,
            content_sha256=batch.digest(q),
            collection=batch.BASE + "/questions.json",
        )
        native.bind_candidate_inventory_row(row, q, root)
        native.bind_candidate_inventory_row(row, q, root)
        assert (
            row["author_review_increment"] == 1
            and row["current_id_author_review_required"] is False
        )
        assert row["independent_review_credit"] == row["canonical_release_credit"] == 0
        rows[qid] = row
    ledger.update(rows)
    assert queue.plan(state, ledger, root, size=10, at=NOW) == []
    # Priority reads all13 current source bindings but selects only eligible new10.
    allbank = batch.read(root, batch.BASE + "/questions.json")
    for q in allbank["questions"]:
        if q["question_id"] not in ledger:
            ledger[q["question_id"]] = dict(
                question_id=q["question_id"],
                content_sha256=batch.digest(q),
                collection=batch.BASE + "/questions.json",
                checked_at=None,
                legal_review_status="already independently assessed",
            )
    for qid in batch.read(root, batch.BASE + "/selection.json")["recommended_ids"]:
        ledger.setdefault(
            qid, dict(checked_at=None, legal_review_status="not eligible")
        )
    independent = queue.empty("independent-legacy")
    queue.plan(
        independent, ledger, root, size=10, at=NOW, prioritize_remediation_defaults=True
    )
    planned = independent["jobs"][0]
    assert (
        list(planned["question_hashes"]) == sorted(questions)
        and planned["selection_policy"]
        == "REMEDIATION_THEN_SOURCE_DEFAULT_THEN_LEXICAL"
    )
    assert batch.REGISTRY in planned["priority_source_sha256"]
    for actor in batch.EXCLUDED:
        with pytest.raises(
            ValueError, match="author/editor cannot independently claim"
        ):
            queue.claim(independent, actor, at=NOW)
    assert queue.claim(independent, "/root/actual-other-reviewer", at=NOW)
    assert queue.plan(independent, ledger, root, size=10, at=NOW) == []


def test_absent_registration_stays_zero_even_after_native_integration(repo):
    root, *_ = repo
    complete(repo, register=False)
    assert native.load_sources(root) == {}


@pytest.mark.parametrize(
    "mutation",
    [
        "no_IG",
        "no_CLAIM",
        "no_SUBMIT",
        "old53_changed",
        "actor",
        "draft_F_replay",
        "current_read_false",
        "source_changed",
        "source_missing",
        "wrong_batch",
    ],
)
def test_native54_refuses_fake_history_source_actor_and_draft_replay(repo, mutation):
    root, state, ledger, questions, _ = repo
    job, report, path = complete(repo)
    if mutation == "no_IG":
        job["status"] = "SUBMITTED"
    elif mutation == "no_CLAIM":
        state["events"] = [
            e
            for e in state["events"]
            if not (e["kind"] == "CLAIM" and e.get("job_id") == job["job_id"])
        ]
    elif mutation == "no_SUBMIT":
        state["events"] = [
            e
            for e in state["events"]
            if not (e["kind"] == "SUBMIT" and e.get("job_id") == job["job_id"])
        ]
    elif mutation == "old53_changed":
        state["jobs"][52]["worker"] = "invented"
    elif mutation == "actor":
        job["worker"] = batch.E_ACTOR
    elif mutation == "wrong_batch":
        job["current_id_author_batch_id"] = "invented"
    elif mutation in {"source_changed", "source_missing"}:
        p = (
            root
            / next(iter(report["records"][0]["choice_by_choice_findings"].values()))[
                "authorities"
            ][0]["raw_path"]
        )
        if mutation == "source_missing":
            p.unlink()
        else:
            p.write_text("tampered")
    else:
        if mutation == "draft_F_replay":
            report = batch.read(root, batch.F2)
        else:
            report["records"][0][
                "current_ID_stem_all_choices_key_all_Korean_explanations_read"
            ] = False
        write(root, path, report)
        h = batch.sha((root / path).read_bytes())
        for row in job["result"]["results"]:
            row["evidence_sha256"] = h
        for e in state["events"]:
            if e["kind"] == "SUBMIT" and e.get("job_id") == job["job_id"]:
                e["result_sha256"] = batch.digest(job["result"])
        reg = batch.read(root, native.REGISTRY)
        reg["sources"][0]["report_sha256"] = h
        write(root, native.REGISTRY, reg)
    write(root, native.QUEUE, state)
    commit(root)
    with pytest.raises((ValueError, FileNotFoundError, KeyError)):
        native.load_sources(root)


def test_head_only_native54_shallow_without_old_worker_objects(repo):
    root, *_ = repo
    job, _, _ = complete(repo)
    clone = root.parent / "shallow"
    subprocess.run(
        ["git", "clone", "-q", "--depth", "1", root.as_uri(), str(clone)], check=True
    )
    assert (
        subprocess.run(
            [
                "git",
                "-C",
                str(clone),
                "cat-file",
                "-e",
                job["result"]["worker_commit"] + "^{commit}",
            ],
            capture_output=True,
        ).returncode
        != 0
    )
    assert len(native.load_sources(clone)) == 1


@pytest.mark.parametrize(
    "mutation",
    [
        "unknown",
        "nonheld",
        "parent_changed",
        "source404",
        "wrong200",
        "registry_changed",
    ],
)
def test_exact_registered_parent_and_primary_retention_fail_closed(
    template, tmp_path, mutation
):
    root = tmp_path / "case"
    subprocess.run(
        ["git", "clone", "-q", "--shared", str(template), str(root)], check=True
    )
    a = batch.allocation(root)
    if mutation in {"unknown", "nonheld", "parent_changed"}:
        if mutation == "unknown":
            a["allocations"][0]["original_question_id"] = "MA-EXP-9999"
        elif mutation == "nonheld":
            s = batch.read(root, batch.BASE + "/selection.json")
            s["holds"] = [
                h
                for h in s["holds"]
                if h["legacy_question_id"]
                != a["allocations"][0]["original_question_id"]
            ]
            write(root, batch.BASE + "/selection.json", s)
        else:
            p = batch.PUBLIC_BANKS[0]
            s = batch.read(root, p)
            q = next(
                q
                for q in s["questions"]
                if q["question_id"] == a["allocations"][0]["original_question_id"]
            )
            q["stem"] += " "
            write(root, p, s)
        with pytest.raises(ValueError):
            batch.validate_parents(root, a)
    elif mutation == "registry_changed":
        reg = batch.read(root, batch.REGISTRY)
        reg["batches"][1]["current_id_count"] = 11
        write(root, batch.REGISTRY, reg)
        with pytest.raises(ValueError):
            batch.load_registry(root)
    else:
        d = batch.read(root, a["allocations"][0]["draft_path"])
        auth = copy.deepcopy(d["option_proofs"][0]["authorities"][0])
        if mutation == "source404":
            auth["http_status"] = 404
        else:
            auth["body_verified_current_primary"] = False
            auth["body_verification"] = "WRONG_DOCUMENT"
        with pytest.raises(ValueError):
            batch.validate_authority(root, auth, author=True)


def test_forged_checked_date_without_integrated_author54_cannot_schedule(repo):
    root, state, ledger, questions, _ = repo
    for qid in questions:
        ledger[qid].update(
            checked_at="2026-11-04",
            author_review_increment=1,
            current_id_author_review_required=False,
        )
    with pytest.raises(ValueError, match="author54 evidence must be integrated"):
        queue.plan(queue.empty("independent-legacy"), ledger, root, size=10, at=NOW)


def test_reservation_scanner_allocates_real_fields_not_test_sentinels(tmp_path):
    write(
        tmp_path,
        "bank/authoring/actual.json",
        {"questions": [{"question_id": "MA-RW-0097"}]},
    )
    write(tmp_path, "reports/real-allocation.json", {"reserved_ids": ["MA-RW-0099"]})
    write(tmp_path, "tests/sentinel.json", {"question_id": "MA-RW-9999"})
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "Synthetic fixture")
    git(tmp_path, "config", "user.email", "fixture@example.test")
    commit(tmp_path)
    scan = batch.scan_reservations(tmp_path, "HEAD")
    assert scan["reserved_ids"] == ["MA-RW-0097", "MA-RW-0099"]
    assert batch.next_ids(scan["reserved_ids"], 1) == ["MA-RW-0100"]
    write(tmp_path, "bank/drafts/invalid.json", {"question_id": "MA-RW-10000"})
    commit(tmp_path)
    with pytest.raises(ValueError, match="Unsupported reserved ID format"):
        batch.scan_reservations(tmp_path, "HEAD")
