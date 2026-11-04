"""Native immutable proposal validation; source-only author evidence, zero review credit."""
import json,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
import notes_census_reassessment as nr
P='reports/full-corpus-review/notes120-census-author/'
state=json.loads((ROOT/q.STATE).read_bytes());notes=json.loads(Path('/workspace/scratch/notes120-verified-inventory.json').read_bytes())['notes']
index=json.loads((ROOT/(P+'proposal-index.json')).read_bytes());out=[]
for row in index['finalized_real_integrated_predecessors']:
 raw=(ROOT/row['record_path']).read_bytes();assert q.raw_sha(raw)==row['record_sha256'];rec=json.loads(raw)
 binding,carried=nr.validate_record(state,rec,ROOT,notes,nr.disk_reader(ROOT))
 out.append({'unit_id':row['unit_id'],'native_validate_record':'PASSED','replacement_binding':binding,'carried_legal_blockers':carried})
path=ROOT/(P+'native-validation.json');path.write_bytes(q.encoded({'validation_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'method':'실제 native validate_record(state,record,root,root의 strict 검증 notes,disk_reader(root)); guard우회/모킹/등록없음.','canonical_release_credit':0,'question_audit_credit':0,'independent_audit_credit':0,'records':out,'pending_integrated_predecessors':index['pending_integrated_predecessors']}));print([(r['unit_id'],r['native_validate_record'])for r in out])
