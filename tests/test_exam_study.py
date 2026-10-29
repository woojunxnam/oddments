"""Source and integration contracts for exam-focused study; not an independent law audit."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('examstudy',ROOT/'scripts/build_exam_study.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
D=builder.build_payload();N=__import__('notes_revision').load_notes(ROOT)
U={u['id']:u for c in N['chapters'] for u in c['units']}

def test_counts_and_distinct_lesson_ids():
    assert D['stats']['modules']==16 and D['stats']['concepts']==64
    assert D['stats']['comparisons']==12 and D['stats']['clocks']==24 and D['stats']['sessions']==30
    assert len({l['id'] for l in D['lessons']})==64
    assert all(len(m['lessons'])==4 for m in D['modules'])

def test_module_and_scope_mapping():
    ids=[x for m in D['modules'] for x in m['lessons']]
    assert len(ids)==len(set(ids))==64
    assert {c for m in D['modules'] for c in m['chapters']}=={c['id'] for c in N['chapters']}
    assert {c for m in D['modules'] for c in m['competencies']}=={f'{a}.{i}' for a,n in [(1,2),(2,5),(3,8),(4,7)] for i in range(1,n+1)}

def test_nonempty_explanations_conditions_and_recall():
    for l in D['lessons']:
        for k in ['title','core','why','trap','recall']:assert isinstance(l[k],str) and len(l[k])>7
        assert l['kind']=='source-derived-study-overlay'

def test_each_source_hash_date_and_flag_is_inherited():
    for l in D['lessons']+D['comparisons']+D['clocks']:
        assert l['note_units'] and all(uid in U for uid in l['note_units'])
        assert l['source_hashes']=={uid:U[uid]['body_sha256'] for uid in l['note_units']}
        assert l['source_review_dates']==list(dict.fromkeys(U[uid]['source_review_date'] for uid in l['note_units']))
        assert l['flags']==sorted({f for uid in l['note_units'] for f in U[uid]['flags']})

def test_open_and_implementation_boundaries_remain_visible():
    assert 'open' in next(l for l in D['lessons'] if l['id']=='LAW-032')['flags']
    assert 'date-sensitive' in next(l for l in D['lessons'] if l['id']=='LAW-044')['flags']
    assert 'open' in next(c for c in D['comparisons'] if c['id']=='compare-05')['flags']
    assert '재검증으로 표시하지' in D['source_policy']

def test_clocks_keep_trigger_and_boundary():
    for c in D['clocks']:
        assert all(c[k].strip() for k in ['title','limit','trigger','boundary'])
    lookup={c['id']:c for c in D['clocks']}
    assert lookup['clock-05']['trigger']=='first partial filling'
    assert lookup['clock-07']['trigger']=='issue date'
    assert lookup['clock-11']['trigger']!=lookup['clock-12']['trigger']

def test_practice_links_use_exact_existing_evidence_not_guessed_topics():
    q={}
    for p in D['question_sources']:q.update({x['question_id']:x for x in json.loads((ROOT/p).read_text())['questions']})
    for l in D['lessons']:
        assert len({x['family'] for x in l['practice_links']})==len(l['practice_links'])
        for link in l['practice_links']:
            original=q[link['id']]
            assert link['url']=='../practice-expansion/#'+original['question_id']
            assert link['shared_units']==sorted(set(l['note_units'])&{e['unit_id'] for e in original['note_evidence']})
            assert link['shared_units']

def test_original_notes_and_banks_preserved():
    assert D['notes_sha256']=='004c2f9f309db00705a3b35ddd2fa1fb360235f4fd0d364a9ccdf8b3c43aa384'
    assert D['question_sources']['practice_expansion/2026-10-23/candidates/questions.json']=='f2b27d3105f2efab40d3ab943f0f5813bdadd793e5ffa60d262fe5ab4e40a74f'
    assert D['question_sources']['practice_expansion/2026-10-26-plus/questions.json']=='f9a600504be007913c996163db29a482cc30ae3781055e50dc3ef9d83f2655b6'

def test_thirty_sessions_are_manual_not_a_guarantee():
    assert [p['day'] for p in D['plan']]==list(range(1,31))
    assert all(p['task'] for p in D['plan'])
    assert '합격예측' in D['source_policy']

def test_current_blueprint_is_dated_and_not_future_outline():
    assert [a['weight'] for a in D['blueprint']['areas']]==[22,33,24,21]
    assert D['blueprint']['valid_before']=='2027-03-01'
    assert D['blueprint']['checked_at']=='2026-10-27'

def test_artifacts_are_deterministic_and_source_linked():
    for p,text in builder.outputs().items():assert p.read_text()==text
    assert len(re.findall('<article>',(ROOT/'site/notes/study.html').read_text()))==64

def test_entry_priority_and_optional_return_path():
    main=(ROOT/'site/index.html').read_text();assert main.index('id="exam-study-title"')<main.index('id="ultimate-notes-title"')
    index=(ROOT/'site/notes/index.html').read_text();assert index.index('href="#study"')<index.index('href="#return"')
    assert '<details class="study-side"><summary>합격 후' in index
    assert "link('notes/#study','MPJE 학습','om-study')" in (ROOT/'site/assets/learning-tools.js').read_text()

def test_separate_progress_namespace_no_existing_bank_writes():
    js=(ROOT/'site/notes/study.js').read_text()
    assert "KEY='oddments.mpje.exam-study.v1'" in js
    for key in ['oddments.mpje.refresh.v1','oddments.mpje.practice.v1','oddments.mpje.ultimate-notes.v1']:assert key not in js
    assert '합격예측 점수가 아닙니다' in js

def test_javascript_syntax():
    subprocess.run(['node','--check',str(ROOT/'site/notes/study.js')],check=True)
