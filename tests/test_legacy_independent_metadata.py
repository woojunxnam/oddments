"""Publication discovers committed controller results, never an orphan PASS file."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import legacy_independent_metadata as metadata
import review_queue as queue

REPORT=metadata.PREFIX+'future-unlisted-review.json'


def write(root,path,value):
    destination=root/path;destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(value)+'\n')


def commit(root):
    subprocess.run(['git','-C',str(root),'add','.'],check=True,stdout=subprocess.DEVNULL)
    subprocess.run(['git','-C',str(root),'commit','-qm','fixture checkpoint'],check=True,stdout=subprocess.DEVNULL)


@pytest.fixture
def checkpoint(tmp_path):
    subprocess.run(['git','init','-q',str(tmp_path)],check=True)
    for key,value in [('user.name','fixture'),('user.email','fixture@example.invalid')]:
        subprocess.run(['git','-C',str(tmp_path),'config',key,value],check=True)
    provenance=dict(stage='independent-legacy',independent_of_authors=True,auditor='GPT',
        auditor_instance='same-real-test-session',actor_provenance=dict(actor_id='/root/test',session_id='/root/test'),
        canonical_audit=False,canonical_release_credit=0)
    report=dict(provenance,records=[dict(question_id='Q1',record_sha256='a'*64)])
    write(tmp_path,REPORT,report)
    sha=hashlib.sha256((tmp_path/REPORT).read_bytes()).hexdigest()
    result=dict(provenance,question_hashes={'Q1':'a'*64},worker_commit='b'*40,
        results=[dict(question_id='Q1',disposition='HOLD',evidence_path=REPORT,evidence_sha256=sha)])
    state=queue.empty('independent-legacy')
    state['jobs']=[dict(stage='independent-legacy',job_id='job1',sequence=1,status='INTEGRATED',
        worker='/root/test',question_hashes={'Q1':'a'*64},result=result,integrated_commit='c'*40,integrated_at='2026-11-03')]
    state['events']=[dict(kind='INTEGRATE',job_id='job1',commit='c'*40)]
    write(tmp_path,metadata.STATE,state);commit(tmp_path)
    return tmp_path,state,report


def test_future_integrated_report_is_discovered_without_filename_registration(checkpoint):
    root,_,report=checkpoint
    assert metadata.integrated_sources(root)==[report]
    write(root,metadata.PREFIX+'unsubmitted-orphan.json',dict(canonical_release_credit=999))
    assert metadata.integrated_sources(root)==[report]


def test_optional_bindings_retain_the_validated_source_and_exact_review(checkpoint):
    root,_,report=checkpoint
    bindings={}
    assert metadata.integrated_sources(root,source_bindings=bindings)==[report]
    assert bindings['Q1']==dict(question_id='Q1',source_path=REPORT,
        source_sha256=hashlib.sha256((root/REPORT).read_bytes()).hexdigest(),job_id='job1',
        record_sha256='a'*64,review_record_sha256=queue.digest(report['records'][0]),
        reviewed_at=None,auditor_instance=report['auditor_instance'],
        actor_provenance=report['actor_provenance'])


def test_later_stale_report_does_not_publish_earlier_partial_bindings(checkpoint):
    root,state,first=checkpoint
    second_path=metadata.PREFIX+'second-review.json'
    second=copy.deepcopy(first)
    second['records']=[dict(question_id='Q2',record_sha256='d'*64)]
    write(root,second_path,second)
    job=copy.deepcopy(state['jobs'][0])
    job.update(job_id='job2',sequence=2,question_hashes={'Q2':'d'*64})
    job['result'].update(question_hashes=job['question_hashes'],results=[dict(
        question_id='Q2',disposition='HOLD',evidence_path=second_path,
        evidence_sha256=hashlib.sha256((root/second_path).read_bytes()).hexdigest())])
    state['jobs'].append(job)
    state['events'].append(dict(kind='INTEGRATE',job_id='job2',commit=job['integrated_commit']))
    second['unexpected_change']='Retained source no longer matches submitted SHA.'
    write(root,second_path,second)
    write(root,metadata.STATE,state);commit(root)
    bindings={}
    with pytest.raises(ValueError,match='raw SHA changed'):
        metadata.integrated_sources(root,source_bindings=bindings)
    assert bindings=={}


@pytest.mark.parametrize('status',['QUEUED','LEASED','SUBMITTED'])
def test_unintegrated_results_never_receive_publication_credit(checkpoint,status):
    root,state,_=checkpoint;state['jobs'][0]['status']=status
    write(root,metadata.STATE,state);commit(root)
    (root/REPORT).unlink()  # Excluded reports do not even need to exist.
    assert metadata.integrated_sources(root)==[]


@pytest.mark.parametrize('change,expected',[
    ('uncommitted_state','Uncommitted'),('uncommitted_report','Uncommitted'),
    ('report_sha','raw SHA changed'),('actor','actor_id must match'),
    ('canonical','canonical release credit'),('extra_id','assignment differs'),
    ('event','Missing captured'),('sequence','sequence changed'),
    ('predecessor','incomplete predecessor'),('escape','repository-relative'),
])
def test_stale_or_unaccountable_results_fail_closed(checkpoint,change,expected):
    root,state,report=checkpoint;job=state['jobs'][0]
    if change=='uncommitted_state': state['new_field']='changed'
    elif change=='uncommitted_report': report['note']='uncommitted'
    elif change=='report_sha': report['note']='committed but stale'
    elif change=='actor': job['worker']='/root/another'
    elif change=='canonical': report['canonical_release_credit']=1
    elif change=='extra_id': report['records'].append(dict(question_id='Q2',record_sha256='d'*64))
    elif change=='event': state['events']=[]
    elif change=='sequence': job['sequence']=2
    elif change=='predecessor':
        earlier=copy.deepcopy(job);earlier.update(job_id='old',status='SUBMITTED')
        job['sequence']=2;state['jobs']=[earlier,job]
    elif change=='escape': job['result']['results'][0]['evidence_path']='reports/full-corpus-review/../outside.json'
    write(root,REPORT,report)
    if change in {'canonical','extra_id'}:
        job['result']['results'][0]['evidence_sha256']=hashlib.sha256((root/REPORT).read_bytes()).hexdigest()
    write(root,metadata.STATE,state)
    if not change.startswith('uncommitted'):commit(root)
    bindings={}
    with pytest.raises(ValueError,match=expected): metadata.integrated_sources(root,source_bindings=bindings)
    assert bindings=={}
