"""Integrity/scope validator only. Does not mechanically certify legal truth or completeness."""
import hashlib,json,sys,subprocess
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts'))
from notes_revision import load_notes
from build_full_corpus_review import validate_note_census,record_hash
OUT=Path(__file__).parent
CENSUS=ROOT/'reports/full-corpus-review/note-wave13-census.json'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path):return json.loads(path.read_text())
c=read(CENSUS);a=read(ROOT/c['assignment_path']);notes=load_notes(ROOT)
effective={u['id']:u for chapter in notes['chapters'] for u in chapter['units']}
conf=read(ROOT/'site/practice-expansion/publication.json');qs=[]
for path in ['practice_expansion/2026-10-23/candidates/questions.json']+[b['path'] for b in conf['additional_banks']]:
 j=read(ROOT/path);qs.extend(j['questions'] if isinstance(j,dict) else j)
byid={q['question_id']:q for q in qs}
validate_note_census(c,effective,byid,ROOT)
assert len(a['units'])==len(c['units'])==20
assert {u['unit_id'] for u in a['units']}=={u['unit_id'] for u in c['units']}
assert sha((ROOT/c['assignment_path']).read_bytes())==c['assignment_sha256']
sel=c['selection_ledger_snapshot'];ledgerraw=(ROOT/sel['path']).read_bytes();assert sha(ledgerraw)==a['ledger_sha256']==sel['sha256']
ledger=[json.loads(l) for l in ledgerraw.decode().splitlines()]; assert len(ledger)==306
assert sum(bool(r['atomic_claim_census_complete']) for r in ledger)==172
lr={r['unit_id']:r for r in ledger}
for u in a['units']:
 uid=u['unit_id'];h=sha(effective[uid]['body'].encode());assert h==u['actual_body_sha256']==lr[uid]['actual_effective_body_sha256'];assert not lr[uid]['atomic_claim_census_complete']
assert not {'w2-c-1','w2-c-12','w4-a-19','w4-a-20'} & {u['unit_id'] for u in c['units']}
assert c['actor_provenance']['actor_role']=='AUTHOR' and c['actor_provenance']['independent'] is False
assert c['actor_provenance']['future_self_independent_review_prohibited']
assert not c['content_mutated'] and not c['K_whole_HOLD_candidate_applied'] and not c['emergency_M_candidate_applied']
assert c['existing_open_claim_registry_unchanged']
assert all(x['independent'] is False and x['actor_role']=='AUTHOR' for x in c['claims'])
for sid,s in c['sources'].items():
 for field in ('source_evidence','original_file'):
  if field in s:assert not Path(s[field]).is_absolute() and '..' not in Path(s[field]).parts
 assert sha((ROOT/s['source_evidence']).read_bytes())==s['source_evidence_sha256']
 if 'original_file' in s:assert sha((ROOT/s['original_file']).read_bytes())==s['original_bytes_sha256']
for x in c['claims']:
 s=c['sources'][x['source_id']]
 assert x['source_evidence_sha256']==s['source_evidence_sha256']
 assert x['official_url']==s['official_url'] and x['checked_at']=='2026-11-03'
 if x['review_status']=='AUTHOR_SOURCE_CHECKED':assert s['retrieval_status']=='RETRIEVED'
 for s2 in x['additional_authorities']:assert sha((ROOT/s2['source_evidence']).read_bytes())==s2['source_evidence_sha256']
 assert bool(x['related_question_ids'])==(x['related_question_link_basis']=='AUTHOR_READ_EXACT_STEM_EVERY_CHOICE_ACTUAL_DECISION_NOT_TAG_INHERITANCE')
ql=read(ROOT/c['question_link_review_path']);assert sha((ROOT/c['question_link_review_path']).read_bytes())==c['question_link_review_sha256']
assert ql['public_practice_inventory']==len(byid)==2346 and ql['canonical_439_mapping_reviewed'] is False
linked={q for x in c['claims'] for q in x['related_question_ids']}
assert linked=={r['question_id'] for r in ql['records']}
for r in ql['records']:
 q=byid[r['question_id']];assert record_hash(q)==r['question_record_sha256'];assert sha(q['stem'].encode())==r['stem_sha256']
 assert r['choice_text_sha256']=={x['id']:sha(x['text'].encode()) for x in q['choices']}
 assert set(r['claim_ids'])=={x['claim_id'] for x in c['claims'] if r['question_id'] in x['related_question_ids']}
 assert r['question_answer_or_independent_audit_credit']==0
counts=Counter(x['review_status'] for x in c['claims']);assert c['summary']['source_checked']==counts['AUTHOR_SOURCE_CHECKED'];assert c['summary']['source_blocked']==counts['SOURCE_BLOCKED'];assert c['summary']['atomic_claims']==len(c['claims'])
changed=subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=ROOT,text=True).splitlines();assert all(x.startswith('reports/full-corpus-review/note-wave13-') or x.startswith('reports/full-corpus-review/evidence/note-wave13-20261103/') for x in changed)
policies=['docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md']
root_context_paths=['/workspace/pr187-final/reports/full-corpus-review/progress.json','/workspace/pr187-final/docs/MPJE_MISSION_CHECKPOINT_2026-11-03_WAVES11-12.md']
result=dict(schema_version='note-wave-validation/1',wave_id='NOTE-WAVE13',checked_at='2026-11-03',actor_role='AUTHOR',independent=False,census_path=str(CENSUS.relative_to(ROOT)),census_raw_sha256=sha(CENSUS.read_bytes()),assignment_raw_sha256=sha((ROOT/c['assignment_path']).read_bytes()),selection_ledger_raw_sha256=sha(ledgerraw),current_J_body_snapshot_sha256=sha((OUT/'actual-current-J-bodies.json').read_bytes()),summary=c['summary'],checks=dict(validate_note_census='PASS',exact20_assignment_and_current_loader_UTF8_SHA='PASS',selection_ledger172_snapshot_not_old_worker_generated='PASS',all_source_evidence_and_retained_rawbytes_SHA='PASS',failed_endpoints_and_fullUSP_not_sourcechecked='PASS',public_question_record_stem_every_choice_SHA_and_claimlinks='PASS',author_only_no_self_independent_credit='PASS',no_shared_or_protected_tracked_files_modified='PASS'),policies_read={p:sha((ROOT/p).read_bytes()) for p in policies},root_context_read=[dict(path=p,sha256=sha(Path(p).read_bytes())) for p in root_context_paths],read_timing_note='worker local132checkpoint initiallyread; explicitroot172snapshot progress/waves11–12checkpoint subsequentlydirectlyread; selectionalwaysboundtoassignedroot172ledger, neveroldworkerledger',NOT_RUN=['independent_note_completeness_review','independent_legal_audit','canonical439_question_audit','full_current_USP_chapter_verification','full_current_radiation_license_conditions','full_pytest_suite','shared_generated_artifact_regeneration','HTTP_browser_UI_checks','GitHub_CI','deployment'],limitations_ko='이검증은SHA/집합/상태/출처바이트결합검사이다.424개원자열거의의미적완전성이나법적정확성을기계적으로인증하지않는다.')
(ROOT/'reports/full-corpus-review/note-wave13-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result['checks'],indent=2));print(json.dumps(result['summary'],indent=2));print('CENSUS_SHA256',result['census_raw_sha256'])
