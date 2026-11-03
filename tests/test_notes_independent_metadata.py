"""Publication reads actual negative audit evidence without creating audit credit."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as queue
from notes_revision import load_notes
from notes_independent_metadata import load_metadata, notices_for_units
from build_ultimate_notes import independent_notice_html, independent_notice_markdown


@pytest.fixture
def actual_reports(tmp_path):
    """Capture real C/F report bytes in a portable, synthetic integration checkpoint.

    This is a consumer fixture, not an independent review or a controller action.
    Original worker objects/branches deliberately do not exist in this repository.
    """
    root = tmp_path/'repo'; root.mkdir(); notes = load_notes(ROOT)
    ledger = (ROOT/queue.LEDGER).read_bytes()
    rows = [json.loads(s) for s in ledger.decode().splitlines()]
    for relative in {queue.LEDGER,*[r['atomic_census_source'] for r in rows if r['atomic_census_source']]}:
        path=root/relative; path.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(ROOT/relative,path)
    shutil.copytree(ROOT/queue.OUTPUT,root/queue.OUTPUT,dirs_exist_ok=True)
    subprocess.run(['git','init','-q','-b','main',str(root)],check=True)
    queue.git(root,'config','user.name','Publication fixture'); queue.git(root,'config','user.email','fixture@example.test')
    queue.git(root,'add','.'); queue.git(root,'commit','-qm','actual audit/census bytes for consumer fixture')
    state = json.loads((ROOT/queue.STATE).read_bytes())
    state['jobs'] = [j for j in state['jobs'] if j.get('result',{}).get('evidence',{}).get('path') in {
        queue.OUTPUT+'first-c-review.json',queue.OUTPUT+'first-f-review.json'}]
    assert len(state['jobs']) == 2
    state['events'] = []
    for i,job in enumerate(state['jobs'],1):
        job.update(sequence=i,status='INTEGRATED',integrated_commit=queue.git(root,'rev-parse','HEAD'),
                   integrated_at='2026-11-03T20:00:00+00:00')
        state['events'].append({'kind':'INTEGRATE','job_id':job['job_id'],'commit':job['integrated_commit'],
                                'result_sha256':job['result_sha256']})
    persist(root,state)
    return root,notes,state


def persist(root,state):
    (root/queue.STATE).write_bytes(queue.encoded(state))
    queue.git(root,'add','.'); queue.git(root,'commit','-qm','persist captured publication checkpoint')


def test_only_integrated_committed_reports_provide_metadata_and_negative_findings_survive(actual_reports):
    root,notes,state = actual_reports
    original = copy.deepcopy(notes)
    metadata = load_metadata(root,notes)
    assert metadata['progress']['processed_units'] == 10
    assert metadata['progress']['complete_units'] == 9
    assert metadata['progress']['omissions_found_units'] == 1
    assert metadata['progress']['legal_hold_units'] == 3
    assert metadata['progress']['legal_keep_units'] == 7
    assert metadata['units']['w1-a-4']['completeness'] == 'OMISSIONS_FOUND'
    assert metadata['units']['w1-a-4']['omissions']
    assert metadata['units']['w1-b-8']['legal_status'] == 'LEGAL_HOLD'
    assert metadata['units']['w1-b-9']['requires_review'] is True
    assert notes == original
    for job in state['jobs']: job['status'] = 'SUBMITTED'
    persist(root,state)
    assert load_metadata(root,notes)['progress']['processed_units'] == 0
    for job in state['jobs']: job['status'] = 'LEASED'
    persist(root,state)
    assert load_metadata(root,notes)['units'] == {}


def test_consumption_works_in_shallow_checkout_without_worker_objects_or_branches(actual_reports,tmp_path):
    root,notes,state = actual_reports
    target = tmp_path/'shallow'
    subprocess.run(['git','clone','-q','--depth','1',root.as_uri(),str(target)],check=True)
    with pytest.raises(subprocess.CalledProcessError):
        queue.git(target,'cat-file','-e',state['jobs'][0]['result']['worker_commit']+'^{commit}')
    assert load_metadata(target,notes)['progress']['processed_units'] == 10


@pytest.mark.parametrize('defect',['envelope_sha','report_bytes','authority_bytes','actor','uncommitted_state'])
def test_tampered_committed_envelope_evidence_and_actor_are_rejected(actual_reports,defect):
    root,notes,state = actual_reports
    if defect == 'envelope_sha': state['jobs'][0]['result_sha256'] = '0'*64
    elif defect == 'actor': state['jobs'][0]['result']['actor_provenance']['actor_id'] = 'forged-actor'
    elif defect == 'uncommitted_state':
        (root/queue.STATE).write_bytes(queue.encoded(state)+b' ')
    else:
        report = state['jobs'][0]['result']['evidence']['path']
        if defect == 'report_bytes': path=root/report
        else:
            data=json.loads((root/report).read_bytes())
            path=root/data['records'][0]['claims'][0]['authorities'][0]['evidence_path']
        path.write_bytes(path.read_bytes()+b' tampered')
    if defect != 'uncommitted_state': persist(root,state)
    with pytest.raises(ValueError): load_metadata(root,notes)


def test_stale_actual_body_or_selected_census_never_retains_previous_credit(actual_reports):
    root,notes,state = actual_reports
    changed = copy.deepcopy(notes)
    next(u for c in changed['chapters'] for u in c['units'] if u['id']=='w1-a-4')['body'] += ' Changed legal condition.'
    with pytest.raises(ValueError,match='Stale ledger/current body'): load_metadata(root,changed)
    census = root/state['jobs'][0]['unit_bindings']['w1-a-4']['census_path']
    census.write_bytes(census.read_bytes()+b'\n')
    queue.git(root,'add','.'); queue.git(root,'commit','-qm','tampered selected census')
    with pytest.raises(ValueError,match='Assigned ledger/census/body changed'): load_metadata(root,notes)


def test_computed_ledger_annotations_are_not_bindings_and_regeneration_is_idempotent(actual_reports):
    root,notes,state = actual_reports
    ledger = (root/queue.LEDGER).read_bytes()
    first = load_metadata(root,notes,ledger_raw=ledger)
    rows = [json.loads(s) for s in ledger.decode().splitlines()]
    for row in rows: row['independent_atomic_census_review'] = first['units'].get(row['unit_id'])
    generated = ''.join(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n' for r in rows).encode()
    # Deliberately leave the old generated ledger on disk: no second build pass.
    second = load_metadata(root,notes,ledger_raw=generated)
    assert second == first == load_metadata(root,notes,ledger_raw=generated)


def test_real_omission_and_ratio_intern_holds_render_in_html_markdown_and_derived_adapter(actual_reports):
    root,notes,state = actual_reports; reviews=load_metadata(root,notes)['units']
    for uid in ['w1-a-4','w1-b-8','w1-b-9']:
        review = reviews[uid]
        page = independent_notice_html(review); markdown = independent_notice_markdown(review)
        assert '독립' in page and '보류' in page and '독립 검토 기록' in markdown
        assert review['report_path'] in page and review['report_path'] in markdown
        assert 'RELEASED' not in page
    assert 'census 누락' in independent_notice_html(reviews['w1-a-4'])
    assert independent_notice_html(reviews['w1-a-5']) == ''
    notices=notices_for_units(['w1-a-5','w1-a-4','w1-b-8','w1-a-4'],reviews)
    assert [r['unit_id'] for r in notices] == ['w1-a-4','w1-b-8']


def test_frontend_renders_independent_warning_and_findings_with_escaped_text(actual_reports):
    root,notes,state=actual_reports; review=load_metadata(root,notes)['units']['w1-a-4']
    review=copy.deepcopy(review); review['omissions'].append('<script>unsafe()</script>')
    source=(ROOT/'site/notes/notes.js').read_text()
    function=source[source.index('  function independentReview(u) {'):source.index('  function chapterNavigation() {')]
    runner="""const fs=require('fs'); const input=JSON.parse(fs.readFileSync(0,'utf8'));
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
"""+function+"\nprocess.stdout.write(independentReview(input));"
    html=subprocess.run(['node','-e',runner],input=json.dumps({'independent_atomic_census_review':review}),
                        text=True,capture_output=True,check=True).stdout
    assert 'census 누락' in html and '독립 검토의 누락·보류 사유' in html
    assert '<script>' not in html and '&lt;script&gt;' in html
    assert '${sourceHold(u)}${independentReview(u)}' in source
