from __future__ import annotations
import base64,json,pathlib,zlib
from qa_common import question_audit_hash

ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=ROOT/"data"
SOURCE_SHA="516771a93f939c843ba4c2be7ef745718606f448"
TODAY="2026-08-18"
PARTS=ROOT/"repair_specs"/"prebatch3_t2"
encoded="".join(p.read_text(encoding="ascii").strip() for p in sorted(PARTS.glob("payload.part*")))
PAYLOAD=json.loads(zlib.decompress(base64.b64decode(encoded)).decode("utf-8"))
RULES=PAYLOAD["rules"]; QUESTIONS=PAYLOAD["questions"]; FAMILIES=PAYLOAD["families"]
REPORT_PATH=ROOT/"audits/remediation/2026-08-18/PRE-BATCH3-COVERAGE-T2-AUTHORING-REPORT.json"

def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def locked_hashes():
    out={}
    for i in range(1,211):
        qid=f"MA-Q-{i:04d}"
        p=DATA/"questions"/f"ma-q-{i:04d}.json"
        if not p.exists():
            raise SystemExit(f"missing locked existing question {qid}")
        q=json.loads(p.read_text(encoding="utf-8"))
        if q.get("question_id")!=qid:
            raise SystemExit(f"question id mismatch {p}")
        out[qid]=question_audit_hash(q)
    return out

def main():
    before=locked_hashes()
    expected={f"MA-Q-{i:04d}" for i in range(211,227)}
    if {q["question_id"] for q in QUESTIONS}!=expected:
        raise SystemExit("T2 question id set mismatch")
    for i in range(211,227):
        p=DATA/"questions"/f"ma-q-{i:04d}.json"
        if p.exists():
            raise SystemExit(f"refusing overwrite of existing {p}")

    existing=set()
    for p in (DATA/"rules").glob("*.json"):
        existing.add(json.loads(p.read_text(encoding="utf-8")).get("rule_id"))
    for r in RULES:
        if r["rule_id"] in existing:
            raise SystemExit(f"new T2 rule id already exists: {r['rule_id']}")
        dump(DATA/"rules"/(r["rule_id"].lower()+".json"),r)
    for q in QUESTIONS:
        dump(DATA/"questions"/(q["question_id"].lower()+".json"),q)

    mp=DATA/"exam_style"/"question_family_matrix.json"
    matrix=json.loads(mp.read_text(encoding="utf-8"))
    ids={f["family_id"] for f in matrix["families"]}
    new={f["family_id"] for f in FAMILIES}
    if ids&new:
        raise SystemExit(f"T2 family collision: {sorted(ids&new)}")
    matrix["families"].extend(FAMILIES)
    matrix["last_reviewed"]=TODAY
    dump(mp,matrix)

    after=locked_hashes()
    if before!=after:
        raise SystemExit(f"existing semantic question hash drift: {[x for x in before if before[x]!=after[x]]}")

    report={
      "report_id":"PRE-BATCH3-COVERAGE-T2-AUTHORING",
      "date":TODAY,
      "issue":68,
      "source_branch":"remediation/pre-batch3-legacy-salvage-t1",
      "source_sha":SOURCE_SHA,
      "author_branch":"remediation/pre-batch3-coverage-t2-author",
      "question_ids":sorted(expected),
      "question_count":len(QUESTIONS),
      "new_rule_ids":sorted(r["rule_id"] for r in RULES),
      "new_family_ids":sorted(new),
      "existing_question_semantic_hashes_before":before,
      "existing_question_semantic_hashes_after":after,
      "existing_question_semantic_hash_preservation":"PASS",
      "t2_release_state":{
        "verification_status":"AUDIT_PENDING",
        "lifecycle_status":"AUDIT_PENDING",
        "independent_audit_status":"PENDING",
        "development_fixture":True,
        "released_count":0
      },
      "full_bank_duplicate_pattern_preflight":"PENDING",
      "repository_validation":"PENDING",
      "full_tests":"PENDING",
      "generated_artifact_freshness":"PENDING",
      "notes":[
        "All T2 items remain audit-pending and are not released.",
        "Existing Q0001-Q0210 canonical semantic content is preserved.",
        "Fresh independent legal and realism audit is required before any T2 release."
      ]
    }
    dump(REPORT_PATH,report)
    print(f"T2 authoring generated: {len(QUESTIONS)} questions, {len(RULES)} rules, {len(FAMILIES)} families")

if __name__=="__main__":
    main()
