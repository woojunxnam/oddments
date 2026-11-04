"""Use native immutable validate_record; no controller mutation or load_notes bypass."""
import json,sys,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
import notes_census_reassessment as nr
P='reports/full-corpus-review/notes101-census-author/'
state=json.loads((ROOT/q.STATE).read_bytes());inventory=json.loads(Path('/workspace/scratch/notes101-validated-inventory.json').read_bytes())
notes=inventory['notes']; index=json.loads((ROOT/(P+'proposal-index.json')).read_bytes())
notes_units={u['id']:u for ch in notes['chapters'] for u in ch['units']}
assert len(notes_units)==306
for uid,binding in inventory['units'].items():assert q.raw_sha(notes_units[uid]['body'].encode())==binding['body_sha256']
rows=[]
for proposal in index['proposals']:
 record=json.loads((ROOT/proposal['record_path']).read_bytes())
 assert q.raw_sha((ROOT/proposal['record_path']).read_bytes())==proposal['record_sha256']
 binding,carried=nr.validate_record(state,record,ROOT,notes,nr.disk_reader(ROOT))
 rows.append({'unit_id':record['unit_id'],'native_validate_record':'PASSED','replacement_binding':binding,'carried_legal_blockers':carried,'registration_performed':False,'independent_review_credit':0,'canonical_release_credit':0,'question_audit_credit':0})
report={'validation_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'method':'Native notes_census_reassessment.validate_record(state, record, root, explicit previously strict-validated notes, disk_reader(root)); all306 body hashes reconfirmed. No register/load_notes/guard changes.','all306_body_hashes_reconfirmed':True,'records':rows}
(ROOT/(P+'native-validation.json')).write_bytes(q.encoded(report));print(json.dumps([{'unit_id':r['unit_id'],'native_validate_record':r['native_validate_record'],'carried_legal_blocker_claim_ids':list(r['carried_legal_blockers'])}for r in rows],ensure_ascii=False,indent=2))
