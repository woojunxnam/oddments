from pathlib import Path
import collections,hashlib,importlib.util,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from publish_practice import build_payload,render
from audit_practice_quality import analyze,normalize,signature
NEW=ROOT/'practice_expansion/2026-10-27-quality'

def test_archives_unchanged():
 expected={'practice_expansion/2026-10-23/candidates/questions.json':'f2b27d3105f2efab40d3ab943f0f5813bdadd793e5ffa60d262fe5ab4e40a74f','practice_expansion/2026-10-26-plus/questions.json':'f9a600504be007913c996163db29a482cc30ae3781055e50dc3ef9d83f2655b6'}
 for p,h in expected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h

def test_every_archived_item_still_present():
 d=build_payload();qs={q['question_id']:q for q in d['questions']}
 config=json.loads((ROOT/'site/practice-expansion/publication.json').read_text())
 assert len(qs)==config['published_total']
 for path in ['practice_expansion/2026-10-23/candidates/questions.json','practice_expansion/2026-10-26-plus/questions.json']:
  for old in json.loads((ROOT/path).read_text())['questions']:
   for k in ['stem','choices','correct_choice_ids','explanation','note_evidence','family_id']:assert qs[old['question_id']][k]==old[k]

def test_new_case_counts_and_keys():
 qs=json.loads((NEW/'questions.json').read_text())['questions'];assert len(qs)==96
 assert len({q['family_id'] for q in qs})==96
 for q in qs:
  ids={c['id'] for c in q['choices']};correct=set(q['correct_choice_ids'])
  assert correct and correct<=ids and len(ids)==len(q['choices'])
  assert len(set(q['explanation']['choice_analysis'].values()))==len(ids)
  assert set(q['explanation']['choice_analysis'])==ids
  if q['question_type']=='SBA':assert len(correct)==1

def test_new_evidence_matches_notes():
 g=json.loads((ROOT/'notes/guide.json').read_text());units={u['id']:u for c in g['chapters'] for u in c['units']}
 d=json.loads((NEW/'questions.json').read_text())
 assert hashlib.sha256((ROOT/'notes/guide.json').read_bytes()).hexdigest()==d['input_guide_sha256']
 for q in d['questions']:
  for e in q['note_evidence']:assert e['body_sha256']==units[e['unit_id']]['body_sha256']
  for sid in q['source_ids']:assert sid in d['sources'] and d['sources'][sid]['url'].startswith('https://')
  assert q['independent_legal_audit'] is None and q['independent_realism_audit'] is None

def test_new_stems_and_full_option_packs_unique():
 qs=json.loads((NEW/'questions.json').read_text())['questions']
 assert len(set(normalize(q['stem']) for q in qs))==96
 assert len(set(signature(q) for q in qs))==96
 assert len(set(normalize(c['text']) for q in qs for c in q['choices']))==396

def test_representatives_reduce_exact_repetition():
 d=build_payload();ids=d['quality_selection']['recommended_ids'];q=[q for q in d['questions'] if q['question_id'] in ids]
 count=d['quality_selection']['stats']['recommended']
 assert len(q)==len(set(ids))==count
 assert len({x['family_id'] for x in q})==count
 assert len({normalize(x['stem']) for x in q})==count
 assert len({signature(x) for x in q})==count
 assert len([x for x in q if x['question_id'].startswith('MA-REV-')])==96

def test_existing_ids_and_new_ids_disjoint():
 d=build_payload();new=set(d['quality_selection']['new_ids']);assert len(new)==96
 assert all(i.startswith('MA-REV-') for i in new)
 assert d['canonical_released_question_count']==0

def test_render_features_and_no_gate():
 t=render(build_payload())
 for x in ['id="chaos"','id="scope"','MA-REV-0096','QC.record(session,active,selected,displayOrder)','QC.chaos(Q,count)','displayLabels[c.id]'] :assert x in t
 assert 'id="ack"' not in t
 assert "KEY='oddments.mpje.practice.v1'" in t
 assert '__PAYLOAD__' not in t
 assert "session.answers[active.question_id]=" not in t

def test_core_random_sampling_and_occurrence_scoring():
 core=ROOT/'site/practice-expansion/quality-core.js'
 js=r'''
const assert=require('assert');const C=require(process.argv[1]);
const mk=(id,f)=>({question_id:id,family_id:f,stem:id,choices:[{id:'A',text:id+'a'},{id:'B',text:id+'b'}],correct_choice_ids:['A']});
const pool=[mk('one','f1'),mk('two','f1'),mk('three','f2')];
assert.deepEqual(C.chaos(pool,10,()=>0).map(q=>q.question_id),Array(10).fill('one'));
assert.deepEqual(C.chaos(pool,10,()=>.999999).map(q=>q.question_id),Array(10).fill('three'));
let values=[0,.34,.7,0,.34,.7,0,.34,.7,.999];let pos=0;assert.deepEqual(C.chaos(pool,10,()=>values[pos++]).map(q=>q.question_id),['one','two','three','one','two','three','one','two','three','three']);
const d=C.diverse(pool,20,{},()=>.5);assert.equal(d.length,2);assert.equal(new Set(d.map(q=>q.family_id)).size,2);
const session={ids:Array(10).fill('one'),pos:0,answers:{}};
for(let i=0;i<10;i++){session.pos=i;C.record(session,pool[0],i%2?['B']:['A'],['B','A']);}
assert.equal(C.responses(session).length,10);assert.equal(C.responses(session).filter(x=>x.correct).length,5);
assert.deepEqual(C.responses(session)[0].selected,['A']);assert.deepEqual(C.responses(session)[1].selected,['B']);
assert.throws(()=>C.record(session,pool[0],['A'],['A','B']));
assert.throws(()=>C.chaos([],10));assert.throws(()=>C.chaos(pool,1,()=>1));
assert.throws(()=>C.answer(pool[0],['A','A']));
const a=C.shuffle(['A','B','C','D'],()=>.4);assert.deepEqual([...a].sort(),['A','B','C','D']);
console.log('core contracts passed');
'''
 r=subprocess.run(['node','-e',js,str(core)],capture_output=True,text=True)
 assert r.returncode==0,r.stderr

def test_normalized_audit_preserves_numbers():
 assert normalize('Within 45 days.')!=normalize('Within 60 days.')

def test_full_structural_ledger_counts():
 d=json.loads((ROOT/'reports/practice-quality/baseline-audit.json').read_text())
 assert [x['total_questions'] for x in d['results']]==[1024,1152,2176,439,2615]
 assert len(d['results'][-1]['question_ledger'])==2615

def test_deterministic_authoring_and_selection():
 from build_quality_questions import build
 from select_quality_representatives import build as select
 before=[p.read_bytes() for p in [NEW/'questions.json',NEW/'selection.json']];build();select()
 assert before==[p.read_bytes() for p in [NEW/'questions.json',NEW/'selection.json']]
