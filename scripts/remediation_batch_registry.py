"""Exact append-only remediation batches; source conversion is never current-ID audit credit."""

from __future__ import annotations
import copy
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = "practice_expansion/2026-10-28-representative"
PREFIX = "reports/representative-rewrite/remediation-batches"
REGISTRY = PREFIX + "/registry.json"
REGISTRY_SHA = "75fb8a049948ba2b41d8acccce39f6dcbc595158374f11d1828e9d355464b783"
BATCH_ID = "phase9-ten-final-v2"
ALLOCATION = PREFIX + "/p9-ten/allocation.json"
CURRENT_BASELINE = PREFIX + "/p9-ten/current-id-baseline.json"
RETENTION = PREFIX + "/p9-ten/source-retention.json"
AUTHORING = BASE + "/authoring/11_phase9_remediation10.json"
PUBLISHED_BASELINE = PREFIX + "/p9-ten/published2349-baseline.json"
OLD_ALLOCATION = "reports/representative-rewrite/sata-remediation/allocation.json"
OLD_ALLOCATION_SHA = "b4869303714843dc3f86d0de3984478fe94b375562fa84a8ebf8dde9e70ef938"
G1 = "reports/full-corpus-review/phase9-remediation-author-g"
G2 = G1 + "/v2"
F1 = "reports/full-corpus-review/phase9-remediation-final-f/final-f-review.json"
F2 = "reports/full-corpus-review/phase9-remediation-final-f/v2/final-f-v2-review.json"
G1_COMMIT = "b7e87d5f3086d77e33f9ac350eeaa2522c93f1fd"
G2_COMMIT = "359b8ee39a68e9eb224743d67f0e2e228a0c490d"
F1_COMMIT = "4c2987c3a28397a4d0da609baff092b6b13c5b98"
F2_COMMIT = "5ca4be14f6acbde72fe15a503f9bfbfe0756ccca"
PARENTS = tuple(
    sorted(
        [
            "MA-REV-0002",
            "MA-REV-0005",
            "MA-REV-0020",
            "MA-REV-0026",
            "MA-REV-0027",
            "MA-EXP-0515",
            "MA-EXP-0615",
            "MA-EXP-0735",
            "MA-EXP-0827",
            "MA-EXP-0851",
        ]
    )
)
G_ACTOR = "/root/independent_case_g"
F_ACTOR = "/root/independent_case_f"
E_ACTOR = "/root/independent_case_e"
EXCLUDED = (G_ACTOR, E_ACTOR, F_ACTOR, "/root")
ENGINEER = dict(
    actor_id=E_ACTOR,
    session_id=E_ACTOR,
    stable_instance="gpt-independent-session-root-independent_case_e-20261103",
    role="COMPILER_EDITOR_NOT_CURRENT_ID_INDEPENDENT_REVIEWER",
)
PUBLIC_BANKS = (
    "practice_expansion/2026-10-23/candidates/questions.json",
    "practice_expansion/2026-10-26-plus/questions.json",
    "practice_expansion/2026-10-27-quality/questions.json",
    BASE + "/questions.json",
)
VISIBLE = (
    "draft_key",
    "question_type",
    "stem",
    "choices",
    "correct_choice_ids",
    "explanation",
)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    return sha(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    )


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def read(root, path):
    return json.loads((Path(root) / path).read_bytes())


def safe(root, path):
    p = Path(path)
    resolved = (Path(root) / p).resolve()
    require(
        not p.is_absolute()
        and ".." not in p.parts
        and Path(root).resolve() in resolved.parents
        and not (Path(root) / p).is_symlink(),
        "Unsafe remediation source path",
    )
    return Path(root) / p


def verify_file(root, path, expected):
    raw = safe(root, path).read_bytes()
    require(sha(raw) == expected, "Remediation source bytes changed: " + path)
    return raw


def scan_reservations(root, commit):
    """Only real producer/allocation fields allocate; test/example text is a recorded mention."""
    stream = subprocess.check_output(["git", "-C", str(root), "archive", commit])
    reserved = set()
    files = {}
    mentions = {}
    keys = {
        "question_id",
        "replacement_question_id",
        "reserved_question_id",
        "allocated_question_id",
        "public_question_id",
    }
    lists = {"reserved_ids", "reserved_question_ids", "allocated_question_ids"}
    with tarfile.open(fileobj=io.BytesIO(stream)) as archive:
        for member in archive:
            if not member.isfile():
                continue
            path = member.name
            ext = Path(path).suffix
            if ext not in {".json", ".jsonl", ".py", ".js", ".md", ".txt", ".html"}:
                continue
            raw = archive.extractfile(member).read()
            text = raw.decode(errors="replace")
            ids = set(re.findall(r"\bMA-RW-\d+\b", text))
            if not ids:
                continue
            mentions[path] = dict(
                raw_sha256=sha(raw),
                ids=sorted(ids),
                allocation_effect="NONALLOCATING_REFERENCE",
            )
            producer = (
                path in PUBLIC_BANKS
                or "/authoring/" in path
                or "/drafts/" in path
                or (
                    ext == ".json"
                    and (
                        "allocation" in Path(path).name
                        or path.endswith("/registry.json")
                    )
                )
            )
            if not producer or path.startswith(("tests/", "test-results/")):
                continue
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                raise ValueError("Malformed authoritative ID reservation: " + path)
            found = set()

            def take(value):
                if isinstance(value, str) and value.startswith("MA-RW-"):
                    require(
                        re.fullmatch(r"MA-RW-\d{4}", value),
                        "Unsupported reserved ID format: " + path,
                    )
                    found.add(value)

            def walk(value):
                if isinstance(value, dict):
                    for k, v in value.items():
                        if k in keys:
                            take(v)
                        if k in lists and isinstance(v, list):
                            for q in v:
                                take(q)
                        walk(v)
                elif isinstance(value, list):
                    for v in value:
                        walk(v)

            walk(data)
            if found:
                reserved.update(found)
                files[path] = dict(raw_sha256=sha(raw), ids=sorted(found))
                mentions[path][
                    "allocation_effect"
                ] = "AUTHORITATIVE_PRODUCER_OR_ALLOCATION_FIELD"
    require(reserved, "No authoritative reservations found")
    return dict(
        rule="Maximum exact four-digit ID in tracked public banks, authoring/draft question fields and allocation/registry reservation fields; tests/comments/diagnostic mentions do not allocate.",
        reserved_ids=sorted(reserved),
        reservation_files=files,
        all_textual_mentions=mentions,
    )


def validate_current_reservation_ownership(root, a):
    """A later tracked draft may reserve other IDs, never this batch's IDs.

    Only HEAD/current tracked producer fields are read. No historical worker
    objects, test sentinel, comments or diagnostic text allocate public IDs.
    """
    owned = {r["question_id"] for r in a["allocations"]}
    allowed = {AUTHORING, ALLOCATION, REGISTRY, BASE + "/questions.json"}
    paths = (
        subprocess.check_output(
            ["git", "-C", str(root), "ls-files", "-z", "--", "*.json"]
        )
        .decode()
        .split("\0")
    )
    keys = {
        "question_id",
        "replacement_question_id",
        "reserved_question_id",
        "allocated_question_id",
        "public_question_id",
    }
    lists = {"reserved_ids", "reserved_question_ids", "allocated_question_ids"}
    for path in paths:
        if not path or path in allowed or path.startswith(("tests/", "test-results/")):
            continue
        producer = (
            path in PUBLIC_BANKS
            or "/authoring/" in path
            or "/drafts/" in path
            or "allocation" in Path(path).name
            or path.endswith("/registry.json")
        )
        if not producer:
            continue
        found = set()

        def take(v):
            if isinstance(v, str) and v.startswith("MA-RW-"):
                require(
                    re.fullmatch(r"MA-RW-\d{4}", v),
                    "Unsupported current reservation format: " + path,
                )
                found.add(v)

        def walk(value):
            if isinstance(value, dict):
                for k, v in value.items():
                    if k in keys:
                        take(v)
                    if k in lists and isinstance(v, list):
                        for item in v:
                            take(item)
                    walk(v)
            elif isinstance(value, list):
                for v in value:
                    walk(v)

        walk(read(root, path))
        require(
            not found & owned,
            "Current tracked reservation collides with enrolled batch: " + path,
        )


def next_ids(reserved, count):
    require(
        count > 0
        and reserved
        and all(re.fullmatch(r"MA-RW-\d{4}", q) for q in reserved),
        "Invalid reservation/count",
    )
    start = max(int(q.rsplit("-", 1)[1]) for q in reserved) + 1
    require(start + count <= 10000, "MA-RW four-digit space exhausted")
    return [f"MA-RW-{n:04d}" for n in range(start, start + count)]


def load_registry(root=ROOT):
    root = Path(root)
    path = root / REGISTRY
    if not path.exists():
        require(not (root / AUTHORING).exists(), "Missing registered remediation batch")
        return None
    raw = path.read_bytes()
    require(sha(raw) == REGISTRY_SHA, "Remediation batch registry raw SHA changed")
    data = json.loads(raw)
    require(
        data.get("schema_version") == "immutable-remediation-batches/1",
        "Unsupported batch registry",
    )
    require(
        len(data["batches"]) == 2
        and data["batches"][0]
        == dict(
            batch_id="original-sata-three",
            allocation_path=OLD_ALLOCATION,
            allocation_sha256=OLD_ALLOCATION_SHA,
            native_author_sequence=53,
            current_id_count=3,
        ),
        "Original three-candidate registration changed",
    )
    verify_file(root, OLD_ALLOCATION, OLD_ALLOCATION_SHA)
    entry = data["batches"][1]
    require(
        entry["batch_id"] == BATCH_ID
        and entry["allocation_path"] == ALLOCATION
        and entry["authoring_path"] == AUTHORING
        and entry["current_id_count"] == 10
        and entry["native_author_sequence"] == 54,
        "Unregistered remediation batch scope",
    )
    allocation = json.loads(verify_file(root, ALLOCATION, entry["allocation_sha256"]))
    require(
        allocation["batch_id"] == BATCH_ID
        and tuple(r["original_question_id"] for r in allocation["allocations"])
        == PARENTS,
        "Batch parent scope changed",
    )
    require(
        [r["question_id"] for r in allocation["allocations"]]
        == next_ids(allocation["reservation_scan"]["reserved_ids"], 10),
        "Non-deterministic remediation IDs",
    )
    verify_file(root, CURRENT_BASELINE, entry["current_id_baseline_sha256"])
    verify_file(root, AUTHORING, entry["authoring_sha256"])
    retention = json.loads(verify_file(root, RETENTION, allocation["retention_sha256"]))
    for item in retention["files"]:
        verify_file(root, item["path"], item["raw_sha256"])
    for p, h in allocation["protected_file_sha256s"].items():
        verify_file(root, p, h)
    return data


def allocation(root=ROOT):
    registry = load_registry(root)
    require(registry is not None, "No new remediation batch registered")
    return read(root, ALLOCATION)


def canonical_actor(value):
    return dict(
        actor_id=value.get("actor_id", value.get("actor")),
        session_id=value.get("session_id", value.get("session")),
        stable_instance=value.get(
            "stable_instance", value.get("stable_auditor_instance")
        ),
    )


def validate_authority(root, value, *, author=False):
    from build_representative_rewrites import OFFICIAL_HOSTS

    require(
        value.get("official_url", "").startswith("https://")
        and (urlparse(value["official_url"]).hostname or "").lower() in OFFICIAL_HOSTS
        and value.get("exact_section")
        and value.get("law_checked_date"),
        "Missing exact official draft authority",
    )
    require(
        value.get("source_type") != "PUBLIC_OFFICIAL_STYLE_ONLY"
        and value.get("not_legal_proof") is not True,
        "Style/copyright memo cannot be primary legal proof",
    )
    require(
        value.get("raw_path") and value.get("raw_sha256"),
        "Unavailable raw primary proof",
    )
    meta_path = value.get("retrieval_metadata_path")
    if not meta_path and not author:
        inferred = str(Path(value["raw_path"]).with_suffix("")) + "-retrieval.json"
        if (Path(root) / inferred).exists():
            meta_path = inferred
    status = value.get("http_status")
    if status is None and meta_path:
        status = read(root, meta_path).get("http_status")
    require(status == 200, "Unavailable raw primary HTTP proof")
    verify_file(root, value["raw_path"], value["raw_sha256"])
    if meta_path:
        meta_raw = safe(root, meta_path).read_bytes()
        if value.get("retrieval_metadata_path"):
            require(
                sha(meta_raw) == value["retrieval_metadata_sha256"],
                "Primary retrieval metadata raw changed",
            )
        meta = json.loads(meta_raw)
        require(
            meta.get("raw_sha256") == value["raw_sha256"]
            and meta.get("http_status") == 200,
            "Primary retrieval metadata differs",
        )
    if author:
        require(
            value.get("tls_verification") is True
            and value.get("used_as_legal_proof") is True
            and (
                value.get("body_verified_current_primary") is True
                or value.get("body_verification")
                == "CORRECT_DOCUMENT_CONTROLLING_SECTION_PERSONALLY_READ"
            ),
            "Unverified author primary body/TLS",
        )


def parent_records(root):
    return {
        q["question_id"]: q
        for path in PUBLIC_BANKS
        for q in read(root, path)["questions"]
    }


def validate_parents(root, a):
    selection = read(root, BASE + "/selection.json")
    by_id = parent_records(root)
    for row in a["allocations"]:
        pid = row["original_question_id"]
        require(
            pid in by_id and digest(by_id[pid]) == row["original_record_sha256"],
            "Changed/unknown remediation parent: " + pid,
        )
        field, key = (
            ("safety_holds", "question_id")
            if pid.startswith("MA-REV-")
            else ("holds", "legacy_question_id")
        )
        holds = [h for h in selection[field] if h[key] == pid]
        require(
            len(holds) == 1 and holds[0] == row["parent_hold"],
            "Unknown/nonheld/changed remediation parent: " + pid,
        )
        hold = holds[0]
        path = hold.get("review_source", hold.get("evidence_report"))
        expected = hold.get("review_source_sha256", hold.get("evidence_report_sha256"))
        require(path and expected, "Parent HOLD must have exact review source")
        report = json.loads(verify_file(root, path, expected))
        records = [r for r in report["records"] if r["question_id"] == pid]
        require(
            len(records) == 1
            and records[0]["record_sha256"] == row["original_record_sha256"],
            "Stale parent review record",
        )
        r = records[0]
        legal = r.get("legal_review", {})
        realism = r.get("realism_review", {})
        require(
            report.get("independent_of_authors") is True
            and report.get("canonical_audit") is False
            and report.get("canonical_release_credit") == 0
            and (
                legal.get("verdict") != "KEEP"
                or legal.get("existing_answer_correct") != "YES"
                or realism.get("verdict") != "PASS"
            ),
            "Parent HOLD lacks an actual current negative source",
        )
    return by_id


def draft_rows(root, a):
    by_id = validate_parents(root, a)
    rows = []
    for row in a["allocations"]:
        raw = verify_file(root, row["draft_path"], row["draft_raw_sha256"])
        draft = json.loads(raw)
        require(
            draft["original_question_id"] == row["original_question_id"]
            and draft["original_record_sha256"] == row["original_record_sha256"],
            "Draft parent binding changed",
        )
        vhash = digest({k: draft[k] for k in VISIBLE})
        require(
            vhash == draft["visible_content_sha256"] == row["visible_content_sha256"],
            "Draft visible bytes/hash changed",
        )
        report = json.loads(
            verify_file(
                root, row["independent_report_path"], row["independent_report_sha256"]
            )
        )
        matches = [r for r in report["records"] if r["draft_key"] == draft["draft_key"]]
        require(len(matches) == 1, "Draft review scope changed")
        f = matches[0]
        require(
            report["actor_provenance"]["actor_id"] == F_ACTOR
            and report["canonical_audit"] is False
            and report["canonical_release_credit"]
            == report["native_review_credit"]
            == 0,
            "Draft F source cannot become native/release credit",
        )
        require(
            f["final_author_draft_path"] == row["draft_path"]
            and f["final_author_draft_raw_sha256"] == sha(raw)
            and f["final_visible_content_sha256"] == vhash
            and f["legal_review"]["verdict"] == "KEEP"
            and f["legal_review"]["existing_answer_correct"] == "YES"
            and f["realism_review"]["verdict"] == "PASS"
            and f["legal_review"]["independently_expected_key"]
            == draft["correct_choice_ids"],
            "Wrong draft version/F key/status binding",
        )
        require(
            len(draft["choices"]) == 4
            and set(draft["explanation"]["choice_analysis"])
            == {c["id"] for c in draft["choices"]},
            "Incomplete four-option Korean input",
        )
        findings = f["legal_review"]["choice_by_choice_findings"]
        require(
            {x["choice_id"] for x in findings} == {c["id"] for c in draft["choices"]},
            "F option coverage changed",
        )
        for c in draft["choices"]:
            g = next(p for p in draft["option_proofs"] if p["choice_id"] == c["id"])
            ff = next(p for p in findings if p["choice_id"] == c["id"])
            rationale = draft["explanation"]["choice_analysis"][c["id"]]
            require(
                g["option_text_sha256"]
                == ff["option_text_sha256"]
                == sha(c["text"].encode())
                and ff["option_text"] == c["text"]
                and g["rationale_sha256"]
                == ff["rationale_sha256"]
                == sha(rationale.encode()),
                "Draft option/rationale/F byte drift",
            )
            require(
                (g["author_supported"] == "YES")
                == (c["id"] in draft["correct_choice_ids"])
                and ff["independently_assessed_truth"]
                is (c["id"] in draft["correct_choice_ids"]),
                "Draft option/key proof drift",
            )
            for authority in g["authorities"]:
                validate_authority(root, authority, author=True)
            for authority in ff["authorities"]:
                validate_authority(root, authority)
        rows.append((row, draft, f, report, by_id[row["original_question_id"]]))
    return rows


def _authoring_from_allocation(root, a):
    """Pure enrollment constructor; public authoring_payload additionally validates registration."""
    rows = draft_rows(root, a)
    sources = {}
    questions = []
    allocation_sha = sha(encoded(a))
    for row, draft, f, report, parent in rows:
        version = "v2" if "/v2/" in row["draft_path"] else "v1"
        prefix = "rm-p9-ten-" + version + "-"
        scenario, separator, lead = draft["stem"].rpartition("\n\n")
        require(
            separator and scenario + separator + lead == draft["stem"],
            "Lossless scenario split unavailable",
        )
        choices = []
        f_authority_bindings = {}
        for c in draft["choices"]:
            proof = next(p for p in draft["option_proofs"] if p["choice_id"] == c["id"])
            refs = []
            for authority in proof["authorities"]:
                sid = prefix + authority["source_id"] + "-" + digest(authority)[:12]
                source = dict(
                    source_id=sid,
                    title=authority["source_id"] + " — retained G primary",
                    official_url=authority["official_url"],
                    exact_sections=[authority["exact_section"]],
                    checked_at=authority["law_checked_date"],
                    access_status="READ_OFFICIAL",
                    retrieval_method=authority.get(
                        "retrieval_method", "Original retained G source"
                    )
                    + "; exact G capture, no new engineering legal read",
                    source_currency=authority.get("version_or_effective_date_status"),
                    verification_scope=authority.get(
                        "direct_read_scope",
                        authority.get(
                            "read_scope",
                            "Exact referenced option clauses from retained G proof",
                        ),
                    ),
                    original_source_id=authority["source_id"],
                    original_author_commit=row["author_commit"],
                )
                for k in (
                    "retrieved_at",
                    "tls_verification",
                    "http_status",
                    "effective_date",
                    "effective_date_status",
                    "raw_path",
                    "raw_sha256",
                    "text_path",
                    "text_sha256",
                    "retrieval_metadata_path",
                    "retrieval_metadata_sha256",
                ):
                    source[k] = copy.deepcopy(authority.get(k))
                if sid in sources:
                    old = sources[sid]
                    require(
                        all(
                            old[k] == source[k]
                            for k in source
                            if k not in ("exact_sections", "verification_scope")
                        ),
                        "Conflicting namespaced draft source",
                    )
                    old["exact_sections"] = sorted(
                        set(old["exact_sections"] + [authority["exact_section"]])
                    )
                    if source["verification_scope"] not in old["verification_scope"]:
                        old["verification_scope"] += "\n" + source["verification_scope"]
                else:
                    sources[sid] = source
                refs.append(dict(copy.deepcopy(authority), source_id=sid))
            choices.append(
                dict(
                    id=c["id"],
                    text=c["text"],
                    correct=c["id"] in draft["correct_choice_ids"],
                    rationale_ko=draft["explanation"]["choice_analysis"][c["id"]],
                    authority_refs=refs,
                )
            )
            ff = next(
                x
                for x in f["legal_review"]["choice_by_choice_findings"]
                if x["choice_id"] == c["id"]
            )
            f_authority_bindings[c["id"]] = dict(
                option_record_sha256=digest(ff),
                authority_record_sha256s=[digest(x) for x in ff["authorities"]],
            )
        actor = canonical_actor(draft["author_provenance"])
        require(
            actor["actor_id"] == actor["session_id"] == G_ACTOR
            and actor["stable_instance"],
            "Actual G author provenance required",
        )
        binding = dict(
            batch_id=BATCH_ID,
            batch_allocation_path=ALLOCATION,
            batch_allocation_sha256=allocation_sha,
            draft_key=draft["draft_key"],
            source_path=row["draft_path"],
            source_full_file_sha256=row["draft_raw_sha256"],
            visible_record_sha256=row["visible_content_sha256"],
            source_author_commit=row["author_commit"],
            original_author_provenance=actor,
            original_author_provenance_verbatim=draft["author_provenance"],
            engineering_provenance=ENGINEER,
            known_author_editor_actor_ids=list(EXCLUDED),
            prior_whole_key_assessor_actor_ids=[F_ACTOR],
            independent_draft_review=dict(
                commit=row["independent_commit"],
                path=row["independent_report_path"],
                report_sha256=row["independent_report_sha256"],
                record_sha256=digest(f),
                per_choice_authority_bindings=f_authority_bindings,
                canonical_audit=False,
                current_public_id_assessed=False,
            ),
            current_id_author_review_required=True,
            current_id_independent_audit="PENDING",
            additional_coverage_credit=0,
            question_audit_credit=0,
            author_review_credit=0,
            canonical_audit=False,
            canonical_release_credit=0,
            release_eligible=False,
            public_activation=False,
        )
        questions.append(
            dict(
                question_id=row["question_id"],
                legacy_question_id=row["original_question_id"],
                topic=parent["topic"],
                area=parent["area"],
                question_type=draft["question_type"],
                scenario=scenario,
                lead_in=lead,
                choices=choices,
                core_reasoning_ko=draft["explanation"]["core_reasoning"],
                learning_boundary_ko=draft["explanation"]["learning_boundary"],
                note_unit_ids=[x["unit_id"] for x in parent["note_evidence"]],
                decision_path=[
                    "Apply each exact retained final-draft option to its original primary-source clauses.",
                    "Keep the stated actor, clock, setting, exception and recommendation strength unchanged.",
                ],
                decision_signature="lossless-final-G-F-draft:" + draft["draft_key"],
                difference_from_legacy=draft["design_change_ko"],
                comparison_with_existing_quality=[
                    dict(
                        relationship="SOURCE_BOUND_REMEDIATION_NOT_NEW_COVERAGE_CERTIFICATION",
                        material_difference=f["realism_review"]["finding_ko"],
                        additional_coverage_credit=0,
                    )
                ],
                competency_codes=["2.1"],
                competency_rationale="Inherited parent area; metadata conversion only, no new legal judgment.",
                exam_outline="MPJE-MA-PRE2027",
                valid_for_exams_before="2027-03-01",
                archive_only_candidate=True,
                remediation_candidate=binding,
            )
        )
    return dict(
        scope="Exactly ten final G/F draft bindings, append-only archive candidates; old HOLD/default unchanged",
        edition="2026-11-04.representative8",
        authored_at="2026-11-04",
        base_commit=a["base_commit"],
        review_status="AUTHOR_SOURCE_REVIEW_NOT_INDEPENDENT_AUDIT",
        author_session=G_ACTOR,
        engineering_provenance=ENGINEER,
        source_limitations=[
            "Exact retained G/F drafts are source context, not new public/current-ID author or independent review.",
            "Actual native G author job54 and a different eligible current-ID independent session remain required.",
            "Original source retrieval/effective-date unknowns remain unchanged. No copyright-restricted private text is copied as legal proof.",
        ],
        sources=sources,
        questions=questions,
    )


def authoring_payload(root=ROOT):
    a = allocation(root)
    payload = _authoring_from_allocation(root, a)
    entry = load_registry(root)["batches"][1]
    require(
        sha(encoded(payload)) == entry["authoring_sha256"],
        "Registered authoring conversion changed",
    )
    return payload


def current_baseline(root=ROOT):
    registry = load_registry(root)
    require(registry is not None, "Missing batch registry")
    return json.loads(
        verify_file(
            root, CURRENT_BASELINE, registry["batches"][1]["current_id_baseline_sha256"]
        )
    )


def legacy_projection(bank, root=ROOT):
    a = allocation(root)
    ids = set(a["prior_representative_question_hashes"])
    sids = set(a["prior_representative_source_hashes"])
    result = copy.deepcopy(bank)
    result["questions"] = [q for q in bank["questions"] if q["question_id"] in ids]
    result["sources"] = {sid: s for sid, s in bank["sources"].items() if sid in sids}
    return result


def validate_compiled_bank(bank, root=ROOT):
    from build_sata_remediation_candidates import validate_preservation as old_validate

    if load_registry(root) is None:
        return old_validate(bank, root)
    a = allocation(root)
    validate_current_reservation_ownership(root, a)
    old_validate(legacy_projection(bank, root), root)
    q = {x["question_id"]: x for x in bank["questions"]}
    require(len(q) == len(bank["questions"]), "Duplicate representative ID")
    for qid, h in a["prior_representative_question_hashes"].items():
        require(
            qid in q and digest(q[qid]) == h,
            "Existing2349 representative object changed: " + qid,
        )
    for sid, h in a["prior_representative_source_hashes"].items():
        require(
            sid in bank["sources"] and digest(bank["sources"][sid]) == h,
            "Existing90 source object changed: " + sid,
        )
    baseline = current_baseline(root)
    new = set(baseline["candidate_question_hashes"])
    present = set(q) & new
    require(not present or present == new, "Partially compiled remediation batch")
    require(
        set(q) == set(a["prior_representative_question_hashes"]) | present,
        "Unallocated new representative ID",
    )
    if not present:
        require(
            set(bank["sources"]) == set(a["prior_representative_source_hashes"]),
            "Premature new batch sources in old stored bank",
        )
        return read(root, OLD_ALLOCATION)
    for qid, h in baseline["candidate_question_hashes"].items():
        require(digest(q[qid]) == h, "Compiled new candidate full-record drift: " + qid)
    for sid, h in baseline["new_source_hashes"].items():
        require(
            sid in bank["sources"] and digest(bank["sources"][sid]) == h,
            "New batch source proof drift: " + sid,
        )
    require(
        set(bank["sources"])
        == set(a["prior_representative_source_hashes"])
        | set(baseline["new_source_hashes"]),
        "Unregistered source namespace",
    )
    validate_parents(root, a)
    return dict(
        allocations=read(root, OLD_ALLOCATION)["allocations"] + a["allocations"]
    )


def validate_archive_links(links, by_id, root=ROOT):
    from build_sata_remediation_candidates import ALLOCATION as OLD

    rows = read(root, OLD)["allocations"]
    if load_registry(root) is not None:
        new = set(current_baseline(root)["candidate_question_hashes"])
        present = set(by_id) & new
        require(not present or present == new, "Partially compiled archive batch")
        if present:
            rows = rows + allocation(root)["allocations"]
            validate_parents(root, allocation(root))
    expected = {r["question_id"]: r["original_question_id"] for r in rows}
    require(
        len(links) == len(expected)
        and {r["replacement_question_id"]: r["legacy_question_id"] for r in links}
        == expected,
        "Archive-only allocation/held-parent mapping changed",
    )
    require(
        all(
            by_id[qid].get("archive_only_candidate") is True
            and by_id[qid]["revision_of"] == pid
            for qid, pid in expected.items()
        ),
        "Archive-only bank/parent binding changed",
    )
    return expected


def validate_published_preservation(data, root=ROOT):
    from build_sata_remediation_candidates import (
        validate_published_preservation as old_validate,
    )

    old_validate(data, root)
    if load_registry(root) is None:
        return
    a = allocation(root)
    baseline = json.loads(
        verify_file(root, PUBLISHED_BASELINE, a["published2349_baseline_sha256"])
    )
    by_id = {q["question_id"]: q for q in data["questions"]}
    require(len(by_id) == len(data["questions"]), "Duplicate delivered ID")
    for qid, h in baseline["record_hashes"].items():
        require(
            qid in by_id and digest(by_id[qid]) == h,
            "Old2349 delivered object changed: " + qid,
        )
    new = set(current_baseline(root)["candidate_question_hashes"])
    present = set(by_id) & new
    require(not present or present == new, "Partially delivered remediation batch")
    require(
        set(by_id) == set(baseline["record_hashes"]) | present,
        "Unallocated delivered question",
    )
    stored = read(root, BASE + "/questions.json")
    validate_compiled_bank(stored, root)
    originals = {q["question_id"]: q for q in stored["questions"]}
    for qid in present:
        require(
            qid in originals, "New delivered candidate lacks current compiled source"
        )
        expected = copy.deepcopy(originals[qid])
        expected["source_edition"] = expected["edition"]
        expected["edition"] = data["edition"]
        require(
            by_id[qid] == expected,
            "Delivered candidate wording/key/proof changed: " + qid,
        )
    expected_sources = dict(baseline["source_hashes"])
    if present:
        expected_sources.update(current_baseline(root)["new_source_hashes"])
    require(
        {sid: digest(s) for sid, s in data["sources"].items()} == expected_sources,
        "Delivered source namespace/old source proof changed",
    )


def registered_rows(root=ROOT):
    rows = read(root, OLD_ALLOCATION)["allocations"]
    if load_registry(root) is not None:
        rows = rows + allocation(root)["allocations"]
    return rows


def author_module(job):
    if "current_id_author_batch_id" not in job:
        import remediation_author_reviews as native
    else:
        require(
            job["current_id_author_batch_id"] == BATCH_ID, "Unknown native author batch"
        )
        import remediation_batch_author_reviews as native
    return native


def required_author_group(root, required, size, sequence):
    if load_registry(root) is not None:
        import remediation_batch_author_reviews as native

        expected = set(current_baseline(root)["candidate_question_hashes"])
        if expected & set(required):
            require(
                set(required) == expected and size >= 10 and sequence == 54,
                "Native author54 requires exactly all ten allocated IDs and size>=10",
            )
            native.validate_parent(Path(root), current_baseline(root))
            require(
                set(native.candidate_records(root)) == expected,
                "Missing current batch candidates",
            )
            return BATCH_ID
    import remediation_author_reviews as native

    require(
        set(required) == set(native.candidate_records(root)) and size >= 3,
        "Native current-ID author scope requires exactly the three allocated candidates and size >=3",
    )
    return None
