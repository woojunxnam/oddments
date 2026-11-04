"""Synthetic exact146 native regressions: these fixtures confer no review credit."""
import copy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review_queue as q
import realism_completion_review as r
import realism_completion_metadata as m
from realism_completion_legal4 import LEGAL_IDS


def write(root,path,value):
    p=root/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(value if isinstance(value,bytes)else r.encoded(value))


def commit(root,message='SYNTHETIC fixture only'):
    q.git(root,'add','.');q.git(root,'commit','-qm',message);return q.git(root,'rev-parse','HEAD')


def question(uid):
    return dict(question_id=uid,question_type='SBA',stem='A pharmacist considers a transfer for '+uid+'. Which action is correct?',
        choices=[dict(id=x,text='Visible option '+x+' for '+uid)for x in 'ABCD'],correct_choice_ids=['A'],
        explanation={'core_reasoning':'보이는 해설 '+uid,'choice_analysis':{x:'보이는 오답 해설 '+x for x in 'ABCD'},'learning_boundary':'보이는 한계'},
        author_id='known-author',_statement_truth='DO_NOT_EXPOSE_HIDDEN_TRUTH')


@pytest.fixture(scope='session')
def template(tmp_path_factory):
    root=tmp_path_factory.mktemp('realism-completion-template')
    subprocess.run(['git','init','-q','-b','main',str(root)],check=True)
    q.git(root,'config','user.name','Synthetic tests');q.git(root,'config','user.email','synthetic@example.invalid')
    public={uid:question(uid)for uid in r.IDS}
    public.update({f'PUB-{i:04d}':question(f'PUB-{i:04d}')for i in range(2349-len(r.IDS))})
    canonical={f'CAN-{i:04d}':question(f'CAN-{i:04d}')for i in range(439)}
    bank='practice_expansion/2026-10-23/candidates/questions.json'
    write(root,bank,{'questions':list(public.values())})
    write(root,'site/practice-expansion/publication.json',{'additional_banks':[]})
    write(root,'practice_expansion/2026-10-28-representative/selection.json',{'recommended_ids':[]})
    write(root,r.STYLE,dict(profile_id='SYNTHETIC_STYLE',content_version=1,content_hash='a'*64))
    for uid,row in canonical.items():write(root,'data/questions/'+uid+'.json',row)
    primary=[]
    for uid in r.IDS:
        realism={'verdict':r.PENDING_VERDICTS.get(uid,'PASS')}
        legal={'verdict':'HOLD','existing_answer_correct':'YES'}
        if uid in LEGAL_IDS:
            realism={'verdict':'PASS'}
            legal={'verdict':'HOLD','existing_answer_correct':'NOT_ASSESSED','blocker':'PROCEDURAL_PRIOR_SOURCE_CONCLUSION_EXPOSURE: SYNTHETIC'}
        primary.append(dict(question_id=uid,record_sha256=q.digest(public[uid]),realism_review=realism,legal_review=legal))
    parent={'actor_provenance':{'actor_id':'prior-reviewer','session_id':'prior-reviewer'},'auditor_instance':'prior-instance','records':primary}
    path='reports/full-corpus-review/synthetic-primary.json';write(root,path,parent);raw=(root/path).read_bytes()
    inputs=r.nearest_inputs(public,canonical)
    style=json.loads((root/r.STYLE).read_bytes())
    scope=dict(schema_version=1,purpose=r.PURPOSE,controller_actor='/root',question_ids=list(r.IDS),
        question_hashes={uid:q.digest(public[uid])for uid in r.IDS},collections=dict.fromkeys(r.IDS,bank),
        prior_supplementary={},primary={row['question_id']:r.parent_binding(row['question_id'],row,path,parent,raw,public[row['question_id']])for row in primary},
        style_profile=dict(path=r.STYLE,raw_sha256=r.sha((root/r.STYLE).read_bytes()),**style),
        nearest_inputs=dict(path=r.INPUTS,raw_sha256=r.sha(r.encoded(inputs))),
        reviewers=[dict(actor_id=a,session_id=a,auditor_instance=i,fork_turns='none',controller_independence_basis='Root must actually spawn a fresh session before claim; queued allocation is not a claim or identity proof.')for a,i in zip(r.ACTORS,r.INSTANCES)],
        canonical_release_credit=0,key_assessment_credit=0,legal_audit_credit=0,new_original_read_credit=0)
    write(root,r.SCOPE,scope);write(root,r.INPUTS,inputs)
    for path in r.WORKER_PUBLIC_FILES:
        if path!=r.STYLE:write(root,path,b'SYNTHETIC PUBLIC WORKER DOCUMENT\n')
    ledger=''.join(json.dumps(dict(question_id=uid,collection=bank,content_sha256=q.digest(row)))+'\n'for uid,row in public.items())
    write(root,'reports/full-corpus-review/question-ledger.jsonl',ledger.encode())
    commit(root)
    return root,scope,inputs,public,primary


@pytest.fixture
def fixture(template,tmp_path,monkeypatch):
    original,scope,inputs,public,primary=template
    root=tmp_path/'repo';subprocess.run(['git','clone','-q','--shared',str(original),str(root)],check=True)
    q.git(root,'config','user.name','Synthetic tests');q.git(root,'config','user.email','synthetic@example.invalid')
    scope=copy.deepcopy(scope);inputs=copy.deepcopy(inputs)
    monkeypatch.setattr(r,'build_scope',lambda root:(copy.deepcopy(scope),copy.deepcopy(inputs)))
    state,_,_=r.plan(root,at="2026-11-04T11:59:00+00:00");write(root,r.STATE,state);commit(root)
    return root,state,scope,inputs,public,primary


def claim(f,index=0):
    root,state,scope,*_=f
    return r.claim(root,state,scope,r.ACTORS[index],r.ACTORS[index],r.INSTANCES[index],
        fresh_session_actually_created=True,at='2026-11-04T12:00:00+00:00')


def make_report(f,index=0,verdict='PASS'):
    root,state,scope,inputs,public,_=f;job=state['jobs'][index];prefix=job['output_prefix']
    memo=dict(own_abstract_memo_ko='SYNTHETIC TEST OWN MEMO: public format only, no exam or source text.',source_is_format_only=True,
        protected_material_not_used=True,reviewed_at='2026-11-04T12:05:00+00:00')
    meta=dict(official_url=r.FORMAT_URL,final_url=r.FORMAT_URL,status=200,retrieved_at='2026-11-04T12:01:00+00:00',
        read_at='2026-11-04T12:02:00+00:00',raw_sha256='a'*64,text_sha256='b'*64,
        raw_path=None,text_path=None,retention='PRIVATE_NOT_REDISTRIBUTED',document_identity_status='OFFICIAL_FORMAT_TARGET_DIRECTLY_READ')
    paths={prefix+'format-memo.json':memo,prefix+'format-meta.json':meta}
    report=dict(purpose=r.PURPOSE,stage='independent-legacy',independent_of_authors=True,auditor='GPT',
        auditor_instance=job['auditor_instance'],actor_provenance=job['actor_provenance'],canonical_audit=False,
        canonical_release_credit=0,key_assessment_credit=0,legal_audit_credit=0,new_original_read_credit=0,release_eligible=False,
        fresh_session_fork_turns='none',prior_conclusions_read=False,hidden_truth_read=False,
        scope_raw_sha256=r.sha(r.encoded(scope)),question_hashes=job['question_hashes'],style_profile=scope['style_profile'],
        native_assignment_binding={k:job[k]for k in r.BINDING_KEYS},reviewed_at='2026-11-04',completed_at='2026-11-04T12:06:00+00:00',
        public_format_evidence=dict(memo_path=prefix+'format-memo.json',memo_sha256=r.sha(r.encoded(memo)),
            metadata_path=prefix+'format-meta.json',metadata_sha256=r.sha(r.encoded(meta))),records=[])
    for uid in job['question_hashes']:
        options=[c['id']for c in public[uid]['choices']]
        criteria=dict.fromkeys(r.CRITERIA,True)
        if verdict=='FAIL':criteria['practice_plausibility']=False
        duplicate=dict(canonical_pool_count=439,public_pool_count=2349,pool_visible_sha256=inputs['pool_visible_sha256'])
        for name in ('canonical','public'):
            duplicate[name]=[dict(question_id=n['question_id'],visible_sha256=n['visible_sha256'],stem_and_all_choices_read=True,
                comparison_ko='SYNTHETIC comparison of '+uid+' and '+n['question_id'])for n in inputs['records'][uid][name]]
        row=dict(question_id=uid,record_sha256=job['question_hashes'][uid],visible_content_sha256=q.digest(r.visible(public[uid],True)),
            release_eligible=False,read_scope=dict(original_stem=True,all_choices_read=options,stored_key_read=True,
                complete_core_reasoning_read=True,all_choice_explanations_read=options,learning_boundary_read=True,
                prior_question_author_or_independent_verdicts_read=False,hidden_statement_truth_read=False),
            realism_review=dict(verdict=verdict,decision='KEEP'if verdict=='PASS'else 'HOLD',criteria=criteria,
                criterion_findings_ko={k:'SYNTHETIC '+uid+' criterion '+k for k in r.CRITERIA},finding_ko='SYNTHETIC individual '+uid,duplicate_evidence=duplicate))
        if uid in LEGAL_IDS:
            rawpath=prefix+'official.raw';textpath=prefix+'official.txt';metapath=prefix+'official-meta.json'
            raw=b'SYNTHETIC OFFICIAL RAW';text=b'SYNTHETIC OFFICIAL TEXT'
            lawmeta=dict(official_url='https://www.ecfr.gov/current/title-21',raw_sha256=r.sha(raw),text_sha256=r.sha(text),
                raw_path=rawpath,text_path=textpath,status=200,method='SYNTHETIC FIXTURE',document_identity_status='OFFICIAL_TARGET_PROVISIONS_DIRECTLY_READ',
                retrieved_at='2026-11-04T12:01:00+00:00',read_at='2026-11-04T12:03:00+00:00')
            paths.update({rawpath:raw,textpath:text,metapath:lawmeta})
            authority=dict(source_id='official',official_url=lawmeta['official_url'],exact_section='SYNTHETIC section',
                effective_date_or_version_basis='SYNTHETIC version / unknown separate commencement',law_checked_date='2026-11-04',
                raw_path=rawpath,raw_sha256=r.sha(raw),text_path=textpath,text_sha256=r.sha(text),metadata_path=metapath,metadata_sha256=r.sha(r.encoded(lawmeta)))
            row['legal_review']=dict(existing_answer_correct='YES',verdict='KEEP',stored_key=['A'],independently_expected_key=['A'],
                question_type='SBA',polarity='CORRECT',finding_ko='SYNTHETIC legal finding '+uid,prior_conclusions_read=False,hidden_truth_read=False,
                authorities=[authority],original_explanation_review=dict(core_reasoning_read=True,all_choice_rationales_read=options,
                    learning_boundary_read=True,finding_ko='SYNTHETIC full rationale review'),per_choice_findings=[dict(choice_id=c['id'],
                    option_text_sha256=r.sha(c['text'].encode()),proposition_supported=c['id']=='A',finding_ko='SYNTHETIC option '+c['id'],authority_refs=['official'])for c in public[uid]['choices']])
        report['records'].append(row)
    return report,paths


def read_memory(paths):
    def read(path,expected=None):
        raw=paths[path]if isinstance(paths[path],bytes)else r.encoded(paths[path])
        r.require(expected is None or r.sha(raw)==expected,'SHA changed in synthetic evidence');return raw
    return read


def complete(f,index=0,verdict='PASS',extra_worker_path=None):
    root,state,scope,inputs,public,_=f;assigned=claim(f,index);write(root,r.STATE,state);commit(root,'SYNTHETIC actual claim')
    job=state['jobs'][index];q.git(root,'checkout','-qb',job['worker_branch'],job['base_commit'])
    report,paths=make_report(f,index,verdict)
    for path,value in paths.items():write(root,path,value)
    if extra_worker_path is not None:write(root,extra_worker_path,b'UNAUTHORIZED SYNTHETIC worker mutation')
    reportpath=job['output_prefix']+'report.json';write(root,reportpath,report);worker=commit(root,'SYNTHETIC worker evidence')
    q.git(root,'checkout','-q','main');q.git(root,'cherry-pick',worker)
    result={k:copy.deepcopy(report[k])for k in ('stage','independent_of_authors','auditor','auditor_instance','actor_provenance','canonical_audit',
        'canonical_release_credit','key_assessment_credit','legal_audit_credit','new_original_read_credit','release_eligible')}
    result.update(worker_commit=worker,question_hashes=job['question_hashes'],result_path=job['output_prefix']+'result.json',
        results=[dict(question_id=uid,disposition='INDEPENDENT_ASSESSED',evidence_path=reportpath,evidence_sha256=r.sha(r.encoded(report)))for uid in job['question_hashes']])
    write(root,result['result_path'],result)
    r.submit(root,state,scope,job['job_id'],assigned['lease_token'],result,inputs,public,at='2026-11-04T12:07:00+00:00')
    write(root,r.STATE,state);commit(root,'SYNTHETIC submitted envelope')
    r.integrate(root,state,scope,job['job_id'],inputs,public,at='2026-11-04T12:08:00+00:00')
    write(root,r.STATE,state);commit(root,'SYNTHETIC ordered integration')
    return result,report


def test_plan_exact146_idempotent_queued_and_blinded_claim_export(fixture,monkeypatch):
    root,state,scope,inputs,public,primary=fixture
    assert [len(j['question_hashes'])for j in state['jobs']]==[40,40,40,26]
    assert all(j['status']=='QUEUED'for j in state['jobs'])and not any(e['kind']=='CLAIM'for e in state['events'])
    before=copy.deepcopy(state);assert r.plan(root,state)[0]==before
    a=claim(fixture);assert claim(fixture)==a
    assert not {'primary','old_realism_verdict','legal_retry_parent','known_author_and_prior_actor_ids'}&set(a)
    packet=r.export_packet(root,a,scope,inputs);serialized=json.dumps(packet)
    assert 'DO_NOT_EXPOSE_HIDDEN_TRUTH'not in serialized and 'prior-reviewer'not in serialized and 'EDITORIAL_REVIEW_REQUIRED'not in serialized
    assert len(packet['records'])==40 and packet['records'][0]['original_visible_content']['correct_choice_ids']==['A']
    assert packet['comparison_counts']=={'canonical':439,'public':2349}
    assert set(packet['nearest_visible'])==set(a['question_hashes'])
    with pytest.raises(ValueError,match='Actually spawn'):
        r.claim(root,state,scope,r.ACTORS[1],r.ACTORS[1],r.INSTANCES[1])
    with pytest.raises(ValueError,match='Controller action'):
        r.plan(root,actor='not-root')


def test_pending_and_submitted_never_count_as_realism_or_key_credit(fixture):
    root,state,scope,inputs,public,primary=fixture
    assert m.load_metadata(root,primary,public)['progress']['integrated_units']==0
    claim(fixture);write(root,r.STATE,state);commit(root)
    result=m.load_metadata(root,primary,public)
    assert result['records']==[] and result['legal_records']==[] and result['progress']['pending_units']==146


@pytest.mark.parametrize('defect',['missing_row','duplicate_row','content_hash','style_hash','criterion_none','criterion_missing','empty_reason',
 'nearest_missing','nearest_hash','no_comparison','pool_count','memo_tamper','raw_publication','prior_exposure','actor','predated_claim','illegal91'])
def test_realism_pass_rejects_missing_tampered_or_exposed_evidence(fixture,defect):
    root,state,scope,inputs,public,_=fixture;claim(fixture);job=state['jobs'][0];report,paths=make_report(fixture)
    row=report['records'][0]
    if defect=='missing_row':report['records'].pop()
    elif defect=='duplicate_row':report['records'][-1]=copy.deepcopy(row)
    elif defect=='content_hash':row['record_sha256']='0'*64
    elif defect=='style_hash':report['style_profile']=dict(report['style_profile'],raw_sha256='0'*64)
    elif defect=='criterion_none':row['realism_review']['criteria'][r.CRITERIA[0]]=None
    elif defect=='criterion_missing':row['realism_review']['criteria'].pop(r.CRITERIA[0])
    elif defect=='empty_reason':row['realism_review']['criterion_findings_ko'][r.CRITERIA[0]]=' '
    elif defect=='nearest_missing':row['realism_review']['duplicate_evidence']['canonical'].pop()
    elif defect=='nearest_hash':row['realism_review']['duplicate_evidence']['canonical'][0]['visible_sha256']='0'*64
    elif defect=='no_comparison':row['realism_review']['duplicate_evidence']['public'][0]['stem_and_all_choices_read']=False
    elif defect=='pool_count':row['realism_review']['duplicate_evidence']['canonical_pool_count']=438
    elif defect=='memo_tamper':paths[report['public_format_evidence']['memo_path']]['own_abstract_memo_ko']+=' tampered'
    elif defect=='raw_publication':
        path=report['public_format_evidence']['metadata_path'];paths[path]['raw_path']='source.pdf';report['public_format_evidence']['metadata_sha256']=r.sha(r.encoded(paths[path]))
    elif defect=='prior_exposure':report['prior_conclusions_read']=True
    elif defect=='actor':report['actor_provenance']={'actor_id':'known-author','session_id':'known-author'}
    elif defect=='predated_claim':report['completed_at']='2026-11-04T11:59:00+00:00'
    else:row['legal_review']={'verdict':'KEEP'}
    with pytest.raises(ValueError):r.validate_report(job,scope,report,read_memory(paths),inputs,public)


def test_old_fail_and_author_exclusion_fail_closed(fixture):
    root,state,scope,inputs,public,primary=fixture;uid=r.IDS[0];old=copy.deepcopy(primary[0]);old['realism_review']['verdict']='FAIL'
    parent={'records':[old],'actor_provenance':{'actor_id':'old'}}
    with pytest.raises(ValueError,match='FAIL cannot'):
        r.parent_binding(uid,old,'p',parent,r.encoded(parent),public[uid])
    scope=copy.deepcopy(scope);state=copy.deepcopy(state)
    scope['primary'][uid]['known_author_and_prior_actor_ids'].append(r.ACTORS[0]);scope['primary'][uid]['known_author_and_prior_actor_ids'].sort()
    state['realism_completion_scope']['raw_sha256']=r.sha(r.encoded(scope));state['jobs'][0]['excluded_worker_actor_ids'].append(r.ACTORS[0]);state['jobs'][0]['excluded_worker_actor_ids'].sort()
    with pytest.raises(ValueError,match='Known author'):
        r.claim(root,state,scope,r.ACTORS[0],r.ACTORS[0],r.INSTANCES[0],fresh_session_actually_created=True,at='2026-11-04T12:00:00+00:00')


def test_actual_native_submission_integration_shallow_and_duplicate_counts(fixture,tmp_path):
    root,state,scope,inputs,public,primary=fixture;original=copy.deepcopy(primary)
    result,report=complete(fixture)
    # Exact repeated completion/integration adds no second event or count.
    before=copy.deepcopy(state);job=state['jobs'][0]
    r.submit(root,state,scope,job['job_id'],job['lease_token'],result,inputs,public,at='2026-11-04T12:09:00+00:00')
    r.integrate(root,state,scope,job['job_id'],inputs,public,at='2026-11-04T12:10:00+00:00')
    assert state==before
    bindings={};metadata=m.load_metadata(root,primary,public,source_bindings=bindings)
    assert metadata['progress']['integrated_units']==metadata['progress']['fresh_realism_pass']==40
    assert metadata['progress']['new_legal_key_assessed']==0 and len(metadata['assessments'])==40
    assert r.STATE in bindings and r.SCOPE in bindings and report['public_format_evidence']['memo_path']in bindings
    rows=[dict(question_id=uid,disposition='HOLD',publication_status='PRACTICE_CONFIG_ARCHIVE',original_key=['A'])for uid in r.IDS]
    before_rows=copy.deepcopy(rows);p=m.apply_metadata(rows,primary,metadata,4)
    assert p['effective_realism_pass']==44-sum(primary_row['realism_review']['verdict']=='HOLD'for primary_row in primary[:40]) and p['raw_primary_realism_pass']==4
    assert all({k:v for k,v in row.items()if k!='independent_legacy_realism_supplementary_assessment'}==before for row,before in zip(rows,before_rows))
    assert primary==original
    target=tmp_path/'shallow';subprocess.run(['git','clone','-q','--depth','1',root.as_uri(),str(target)],check=True)
    with pytest.raises(subprocess.CalledProcessError):q.git(target,'cat-file','-e',result['worker_commit']+'^{commit}')
    assert m.load_metadata(target,primary,public)['progress']==metadata['progress']
    path=root/report['public_format_evidence']['memo_path'];path.write_bytes(path.read_bytes()+b' tampered')
    with pytest.raises(ValueError):m.load_metadata(root,primary,public)


def test_fixed4_requires_legal_read_exposure_and_official_bytes(fixture):
    root,state,scope,inputs,public,_=fixture
    claim(fixture,0);claim(fixture,1);claim(fixture,2);assigned=claim(fixture,3)
    assert set(assigned['legal_retry_question_hashes'])==set(LEGAL_IDS)
    job=state['jobs'][3];report,paths=make_report(fixture,3)
    assert len([row for row in report['records']if 'legal_review'in row])==4
    r.validate_report(job,scope,report,read_memory(paths),inputs,public)
    row=next(row for row in report['records']if row['question_id']in LEGAL_IDS)
    original=copy.deepcopy(row['legal_review'])
    row['legal_review']['prior_conclusions_read']=True
    with pytest.raises(ValueError,match='Exposure'):r.validate_report(job,scope,report,read_memory(paths),inputs,public)
    row['legal_review']=copy.deepcopy(original);row['legal_review']['per_choice_findings'].pop()
    with pytest.raises(ValueError,match='Every original option'):r.validate_report(job,scope,report,read_memory(paths),inputs,public)
    row['legal_review']=copy.deepcopy(original);paths[job['output_prefix']+'official.raw']=b'TAMPERED'
    with pytest.raises(ValueError,match='SHA'):r.validate_report(job,scope,report,read_memory(paths),inputs,public)


def test_all_four_native_jobs_only_four_new_keys_and_no_default_or_double_credit(fixture):
    root,state,scope,inputs,public,primary=fixture
    for index in range(4):complete(fixture,index)
    metadata=m.load_metadata(root,primary,public)
    assert metadata['progress']['integrated_units']==146 and metadata['progress']['fresh_realism_pass']==146
    assert metadata['progress']['new_legal_key_assessed']==4 and set(metadata['legal_assessments'])==set(LEGAL_IDS)
    from phase11_context38_metadata import combine_metadata
    combined=combine_metadata(primary,{'assessments':metadata['legal_assessments'],'records':metadata['legal_records']})
    assert combined['progress']['effective_key_assessed']==146 and combined['progress']['primary_key_assessed']==142
    assert combined['progress']['unique_originals_read']==146 and combined['progress']['canonical_release_credit']==0
    assert m.apply_metadata([],primary,metadata,4)['effective_realism_pass']==118
    # Parent4 HOLD/NOT_ASSESSED are immutable despite actual fresh YES.
    assert all(row['legal_review']['verdict']=='HOLD'and row['legal_review']['existing_answer_correct']=='NOT_ASSESSED'for row in primary if row['question_id']in LEGAL_IDS)


@pytest.mark.parametrize('status',['NOT_ASSESSED','HOLD'])
def test_incomplete_style_remains_nullable_blocked_and_never_pass(fixture,status):
    root,state,scope,inputs,public,primary=fixture;claim(fixture);job=state['jobs'][0];report,paths=make_report(fixture)
    row=report['records'][0];review=row['realism_review'];review.update(verdict=status,decision='HOLD',blocker='SYNTHETIC actual-source limitation')
    review['criteria'][r.CRITERIA[0]]=None
    r.validate_report(job,scope,report,read_memory(paths),inputs,public)
    review.pop('blocker')
    with pytest.raises(ValueError,match='explicit HOLD/blocker'):r.validate_report(job,scope,report,read_memory(paths),inputs,public)


def test_lost_lease_requeue_uses_new_native_attempt_and_rejects_old_token(fixture):
    root,state,scope,*_=fixture;old=claim(fixture);job=state['jobs'][0]
    q.revoke(state,job['job_id'],old['lease_token'],'SYNTHETIC lost worker','/root',at='2026-11-04T12:01:00+00:00')
    new=r.claim(root,state,scope,r.ACTORS[0],r.ACTORS[0],r.INSTANCES[0],fresh_session_actually_created=True,at='2026-11-04T12:02:00+00:00')
    assert new['attempt']==2 and new['lease_token']!=old['lease_token']
    with pytest.raises(ValueError,match='Stale or absent'):q.require_lease(state['jobs'][0],old['lease_token'],'2026-11-04T12:03:00+00:00')
    assert any(e['kind']=='LEASE_REVOKED'for e in state['events'])


@pytest.mark.parametrize('path',['outside-original.json',r.PREFIX+'a/unreferenced.txt'])
def test_worker_commit_cannot_modify_original_or_unreferenced_payloads(fixture,path):
    with pytest.raises(ValueError,match='exactly own report/memo/metadata'):complete(fixture,extra_worker_path=path)


@pytest.mark.parametrize('verdict,negative',[('PASS',False),('FAIL',True)])
def test_strict_supplementary_source_binding_and_negative_notice_gate(fixture,verdict,negative):
    root,state,scope,inputs,public,primary=fixture;complete(fixture,verdict=verdict)
    from supplementary_checkpoint_bindings import validated_sources
    bindings={};sources=validated_sources(root,primary,source_bindings=bindings)
    assert len(sources)==40 and all(s['negative']is negative for s in sources.values())
    assert r.STATE in bindings and r.SCOPE in bindings
    metadata=m.load_metadata(root,primary,public)
    selection={'recommended_ids':[],'archive_review_notices':[],'safety_holds':[]}
    if verdict=='PASS':m.validate_archive_containment(selection,metadata)
    else:
        with pytest.raises(ValueError,match='actual source-bound archive notice'):m.validate_archive_containment(selection,metadata)
        for uid,proof in metadata['assessments'].items():
            selection['archive_review_notices'].append(dict(question_ids=[uid],issue_type='INDEPENDENT_REVIEW_FINDING',
                review_source=proof['report_path'],review_source_sha256=proof['report_sha256'],question_record_hashes={uid:proof['record']['record_sha256']}))
        m.validate_archive_containment(selection,metadata)
    selection['recommended_ids']=[r.IDS[0]]
    with pytest.raises(ValueError,match='cannot return to default'):m.validate_archive_containment(selection,metadata)


def test_existing_secondary_negative_and_pass_are_preserved_in_effective_union(fixture):
    _,_,_,_,_,primary=fixture
    original={row['question_id']:row for row in primary};ids=['MA-CASE-0401','MA-CASE-0441']
    supplement={'assessments':{uid:{'record':{'realism_review':{'verdict':'PASS'}}}for uid in ids},
        'prior_realism_negative_ids':[ids[0]],'prior_realism_pass_ids':[ids[1]],'progress':{}}
    before=copy.deepcopy(primary)
    result=m.apply_metadata([],primary,supplement,5)
    assert result['effective_realism_pass']==5 and result['fresh_pass_with_preserved_existing_supplementary_negative']==1 and result['fresh_pass_with_preserved_primary_realism_hold']==0
    assert primary==before


def test_exact_two_overlap_keeps_old_negative_and_never_replaces_with_positive():
    from supplementary_checkpoint_bindings import merge_completion_source
    old={'source_path':'old-actual.json','negative':True};passed={'source_path':'new-pass.json','negative':False};failed={'source_path':'new-fail.json','negative':True}
    a=merge_completion_source('MA-CASE-0401',old,passed)
    assert a['source_path']=='old-actual.json'and a['negative']is True and a['realism_completion_source']==passed
    b=merge_completion_source('MA-CASE-0441',old,failed)
    assert b['source_path']=='new-fail.json'and b['previous_supplementary_sources']==[old]
    with pytest.raises(ValueError,match='Unexpected supplementary realism overlap'):merge_completion_source('outside-fixed-two',old,failed)


def test_native_out_of_order_submission_waits_without_credit(fixture):
    root,state,scope,inputs,public,primary=fixture;claim(fixture,0)
    with pytest.raises(ValueError,match='assignment order'):complete(fixture,index=1)
    assert state['jobs'][1]['status']=='SUBMITTED'and state['jobs'][0]['status']=='LEASED'
    assert m.load_metadata(root,primary,public)['progress']['integrated_units']==0


@pytest.mark.parametrize('target',['parent_report','current_question','style_profile','scope'])
def test_changed_committed_inputs_fail_closed_without_publishing_partial_bindings(fixture,target):
    root,state,scope,inputs,public,primary=fixture
    if target=='parent_report':path=scope['primary'][r.IDS[0]]['report_path']
    elif target=='current_question':path=scope['collections'][r.IDS[0]]
    elif target=='style_profile':path=r.STYLE
    else:path=r.SCOPE
    if target=='current_question':
        bank=json.loads((root/path).read_bytes());bank['questions'][0]['stem']+=' Actual changed condition.';write(root,path,bank)
    else:write(root,path,(root/path).read_bytes()+b' ')
    commit(root)
    bindings={'existing':'unchanged'}
    with pytest.raises(ValueError):m.load_metadata(root,primary,public,source_bindings=bindings)
    assert bindings=={'existing':'unchanged'}


def test_worker_view_is_small_and_does_not_checkout_prior_verdicts_or_hidden_originals(fixture,tmp_path):
    root,state,scope,inputs,public,primary=fixture;a=claim(fixture)
    destination=tmp_path/'blinded-worker'
    actual=r.prepare_worker(root,state,a['job_id'],a['lease_token'],destination,at='2026-11-04T12:01:00+00:00')
    assert actual==destination and r.prepare_worker(root,state,a['job_id'],a['lease_token'],destination,at='2026-11-04T12:01:00+00:00')==destination
    assert (destination/r.STYLE).exists()and(destination/'docs/REALISM_COMPLETION_WORKER_CONTRACT.md').exists()
    assert not(destination/r.SCOPE).exists()and not(destination/r.STATE).exists()
    assert not(destination/scope['collections'][r.IDS[0]]).exists()
    assert not(destination/scope['primary'][r.IDS[0]]['report_path']).exists()
    assert q.git(destination,'rev-parse','HEAD')==a['base_commit']and q.git(destination,'status','--porcelain')==''
