"""Native immutable proposal validation; source-only author evidence, zero review credit."""
import json,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
import notes_census_reassessment as nr
P='reports/full-corpus-review/final86-census-author/'
state=json.loads((ROOT/q.STATE).read_bytes());inventory_raw=Path('/workspace/scratch/notes-final86-verified-inventory.json').read_bytes()
assert q.raw_sha(inventory_raw)=='5b810a28f12c0a13417d79e2f0d6b0226dd5bbe1dfe085b3d84b61183019ae9c'
inventory=json.loads(inventory_raw);notes=inventory['notes']
actual={u['id']:u for ch in notes['chapters'] for u in ch['units']}
assert len(actual)==306
for uid,binding in inventory['units'].items():assert q.raw_sha(actual[uid]['body'].encode())==binding['body_sha256']
index=json.loads((ROOT/(P+'combined-index.json')).read_bytes());out=[]
for row in index['finalized_real_integrated_predecessors']:
 raw=(ROOT/row['record_path']).read_bytes();assert q.raw_sha(raw)==row['record_sha256'];rec=json.loads(raw)
 binding,carried=nr.validate_record(state,rec,ROOT,notes,nr.disk_reader(ROOT))
 assert rec['author_provenance']['actor_id'] in binding['known_author_ids']
 out.append({'unit_id':row['unit_id'],'native_validate_record':'PASSED','replacement_binding':binding,'carried_legal_blockers':carried})
path=ROOT/(P+'native-validation.json');path.write_bytes(q.encoded({'validation_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'method':'실제 native validate_record(state,record,root,root의 strict 검증 notes,disk_reader(root)); guard우회/모킹/등록없음.','canonical_release_credit':0,'question_audit_credit':0,'independent_audit_credit':0,'all306_body_hashes_reconfirmed':True,'records':out,'pending_integrated_predecessors':index['pending_integrated_predecessors']}));print([(r['unit_id'],r['native_validate_record'])for r in out])
