"""Synthetic scheduler fixtures only; these records are not actual legal audits."""
import copy
import json
import subprocess

import pytest

from test_note_review_queue import repo,claimed,worker_result,integrate_files,NOW,LATER
from test_notes_census_reassessment import commit,persist,authority
import note_review_queue as q
import notes_body_reassessment as body
from notes_independent_metadata import load_metadata,notices_for_units

PREFIX='reports/full-corpus-review/body-corrections/fixture/'
RECORD=PREFIX+'record.json'


def test_source_date_only_changes_do_not_hide_actual_statutory_date_or_deadline_changes():
    assert body.semantic('source_review_date: 2026-11-03')==body.semantic('source_review_date: 2026-11-04')
    assert body.semantic('법규 확인일: 2026-11-03')==body.semantic('법규 확인일: 2026-11-04')
    assert body.semantic('법 시행일 2026-01-01')!=body.semantic('법 시행일 2026-02-01')
    assert body.semantic('within 7 days')!=body.semantic('within 30 days')


def put(root,path,value):
    target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(q.encoded(value))
    return {'path':path,'raw_sha256':q.raw_sha(target.read_bytes())}


@pytest.fixture
def correction(repo,request):
    root,notes,inv=repo
    # Complete synthetic author-census shape for the real builder validator.
    original=json.loads((root/inv['units']['z-first']['census_path']).read_bytes())
    path=q.OUTPUT+'fixture-author-source.txt'
    target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b'Synthetic author source fixture')
    original['sources']={'fixture':{'official_url':'https://example.gov/fixture','source_evidence':path,
                                  'source_evidence_sha256':q.raw_sha(target.read_bytes())}}
    for u in original['units']:u['census_status']='AUTHOR_ENUMERATED'
    for c in original['claims']:
        c.update(related_question_ids=[],authority_clauses=['Synthetic section only'],source_id='fixture',blocker='Synthetic source limitation')
    put(root,inv['units']['z-first']['census_path'],original);commit(root,'complete synthetic census fixture shape')
    inv=q.inventory(root,notes);repo=(root,notes,inv);state,old=claimed(repo)
    def negative(report):
        row=report['records'][0];row['claims'][0].update(legal_status='LEGAL_HOLD',finding='Incorrect original legal scope',blocker='Correct the source body scope')
        row['legal_status']='LEGAL_HOLD'
        if getattr(request,'param',None)=='omissions':row.update(completeness='OMISSIONS_FOUND',omissions=['Original independently found omission'])
        if getattr(request,'param',None)=='sibling_omissions':
            for sibling in report['records'][1:4]:
                sibling.update(completeness='OMISSIONS_FOUND',omissions=['Omitted sibling atom'],legal_status='LEGAL_HOLD')
    result,worker=worker_result(repo,state,old,negative)
    q.submit(state,old['job_id'],old['lease_token'],q.encoded(result),root,inv,NOW)
    integrate_files(root,result);q.integrate(state,old['job_id'],root,inv,NOW);persist(root,state)
    uid=old['unit_ids'][0];binding=old['unit_bindings'][uid];old_unit=body.units(notes)[uid]
    census=json.loads((root/binding['census_path']).read_bytes())
    replacement=copy.deepcopy(census);replacement.update(author_provenance={'actor_id':'body-author','session_id':'body-author-session'})
    replacement['units']=[copy.deepcopy(next(u for u in census['units']if u['unit_id']==uid))]
    replacement['claims']=[copy.deepcopy(c)for c in census['claims']if c['unit_id']==uid]
    candidate=copy.deepcopy(old_unit);candidate.pop('independent_content_review',None)
    statement='Corrected legal scope includes the actually stated controlled-substance class.'
    candidate.update(body=statement,body_sha256=q.raw_sha(statement.encode()),content_version='fixture-body-v2')
    for c in replacement['claims']:c['unit_content_sha256']=candidate['body_sha256']
    changed=replacement['claims'][0];changed['statement_ko']=statement
    replacement['units'][0].update(unit_content_sha256=candidate['body_sha256'],
        census_status='COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK')
    rev=put(root,PREFIX+'revision.json',{'purpose':body.PURPOSE,'inactive':True,'id':'fixture-body-v2',
        'author_provenance':replacement['author_provenance'],'author_instance':'body-author-instance','units':[candidate]})
    cb=put(root,PREFIX+'census.json',replacement)
    archive={'notes':put(root,PREFIX+'old-notes.json',notes),
        'job':put(root,PREFIX+'old-job.json',{'job':old,'events':[e for e in state['events']if e.get('job_id')==old['job_id']]})}
    for key,path in [('census',binding['census_path']),('report',old['result']['evidence']['path']),('result',old['result']['result_path'])]:
        target=root/(PREFIX+'old-'+key+'.json');target.write_bytes((root/path).read_bytes())
        archive[key]={'path':target.relative_to(root).as_posix(),'raw_sha256':q.raw_sha(target.read_bytes())}
    dp=put(root,PREFIX+'derived.json',{'items':[],'full_published_builder_status':'NOT_RUN_INACTIVE_BODY_PUBLICATION_REQUIRES_SEPARATE_16'})
    attempt=root/(PREFIX+'blocked-attempt.txt');attempt.write_text('Synthetic failed source attempt, never legal proof')
    primary=put(root,PREFIX+'retrieval.json',{'retrievals':[{'requested_url':'https://example.gov/fixture',
        'retrieval_started_at_utc':NOW,'transport':'SYNTHETIC_TEST_ONLY','document_identity_status':'SOURCE_BLOCKED',
        'status':403,'raw_path':attempt.relative_to(root).as_posix(),'raw_sha256':q.raw_sha(attempt.read_bytes())}]})
    from notes_census_reassessment import LEDGER_FIELDS
    row=next(json.loads(x)for x in(root/q.LEDGER).read_text().splitlines()if json.loads(x)['unit_id']==uid)
    record=dict(schema_version=1,purpose=body.PURPOSE,body_reassessment_id='fixture-body-v2',unit_id=uid,
        inactive=True,publication_blocker=body.BLOCKER,change_basis='Actual fixture body scope correction',
        previous_job_id=old['job_id'],previous_job_sha256=q.digest(old),previous_binding=copy.deepcopy(binding),
        previous_report=copy.deepcopy(old['result']['evidence']),previous_result={'path':old['result']['result_path'],'raw_sha256':old['result_sha256']},
        previous_ledger_fields={k:row.get(k)for k in LEDGER_FIELDS},archived_parent=archive,
        replacement={'revision':rev,'census_path':cb['path'],'census_sha256':cb['raw_sha256'],'notes_revision':'fixture-body-v2'},
        author_provenance=replacement['author_provenance'],author_instance='body-author-instance',
        claim_mapping={c['claim_id']:[c['claim_id']]for c in replacement['claims']},added_claim_ids=[],
        semantic_changed_claim_ids=[changed['claim_id']],
        edit_spans=[{'old_text':old_unit['body'],'new_text':statement,'old_text_sha256':q.raw_sha(old_unit['body'].encode()),
                     'new_text_sha256':q.raw_sha(statement.encode()),'claim_ids':[changed['claim_id']]}],
        other_current_bindings_sha256=q.digest({k:b for k,b in inv['units'].items()if k!=uid}),derived_preview=dp,primary_retrieval=primary)
    put(root,RECORD,record);commit(root,'inactive author body/census correction fixture')
    return root,notes,inv,state,old,record


def register(fixture):
    root,notes,inv,state,_,_=fixture
    bid=body.register(state,inv,root,RECORD,notes,NOW);persist(root,state)
    return next(j for j in state['jobs']if j['job_id']==bid)


def final_review(job,root,resolve=False):
    def edit(report):
        row=report['records'][0];uid=row['unit_id']
        row.update(actual_body_sha256=job['unit_bindings'][uid]['body_sha256'],reviewed_at=NOW,
            body_correction_review={**job['body_correction_review'],'final_body_read_completely':True,
                'final_census_read_completely':True,'all_parent_negatives_explicitly_reassessed':True,
                'all_parent_omissions_explicitly_reassessed':True,
                'all_derived_inputs_read_completely':True,'no_current_credit_before_matching_active_binding':True})
        row['original_omission_reassessments']=[{'omission_sha256':o['raw_sha256'],
            'decision':'UNRESOLVED_REMAINS_OMISSION','finding':'Synthetic fresh review still finds this original omission'}
            for o in job['body_correction_review']['parent_omissions']]
        row['omissions']=[o['omission']for o in job['body_correction_review']['parent_omissions']]
        if row['omissions']:row['completeness']='OMISSIONS_FOUND'
        for claim in row['claims']:
            cid=claim['claim_id'];carried=job['carried_legal_blockers'][uid].get(cid)
            if carried:claim['inherited_legal_blockers']=carried
            negative=job['reconsidered_legal_negatives'][uid].get(cid)
            if not negative:continue
            claim['original_legal_negatives']=negative
            claim['body_negative_reassessment']={'original_negatives_sha256':q.digest(negative),
                'changed_statement_sha256':job['body_correction_review']['changed_statement_sha256s'][cid],
                'edit_span_sha256s':job['body_correction_review']['edit_span_sha256s'],
                'original_negative_read_completely':True,'corrected_statement_read_completely':True,
                'finding':'Synthetic explicit comparison of old legal negative with genuinely changed body/proposition',
                'decision':'RESOLVED_BY_CHANGED_BODY_AND_PROPOSITION'if resolve else'UNRESOLVED_REMAINS_HELD'}
            if resolve:
                path=q.OUTPUT+'fixture-official.txt';worker=root.parent/('worker-'+str(job['sequence']))
                (worker/path).write_bytes(b'Official fixture authority bytes')
                a=authority(path)
                a['source_retrieval']={'mode':'LIVE','http_status':200,'transport':'SYNTHETIC_TEST_ONLY',
                    'document_identity_status':'OFFICIAL_DOCUMENT_TARGET_PROVISIONS_DIRECTLY_READ',
                    'raw_sha256':a['evidence_sha256'],'retrieved_at_utc':NOW,'read_at_utc':NOW}
                claim.update(legal_status='KEEP',authorities=[a]);claim.pop('blocker',None)
            else:claim['legal_status']='LEGAL_HOLD'
        row['legal_status']='LEGAL_HOLD'if row['omissions']or any(c['legal_status']=='LEGAL_HOLD'for c in row['claims'])else'SOURCE_BLOCKED'
    return edit


def activate_fixture(root,notes,record):
    """Test-only stand-in for a future explicit published-15-based 16th guard."""
    active=copy.deepcopy(notes);candidate=json.loads((root/record['replacement']['revision']['path']).read_bytes())['units'][0]
    for chapter in active['chapters']:
        chapter['units']=[candidate if u['id']==record['unit_id']else u for u in chapter['units']]
    census=json.loads((root/record['replacement']['census_path']).read_bytes())
    rows=[json.loads(x)for x in(root/q.LEDGER).read_text().splitlines()]
    rows=[body.replacement_row(record,census,candidate)if r['unit_id']==record['unit_id']else r for r in rows]
    (root/q.LEDGER).write_text(''.join(json.dumps(r)+'\n'for r in rows));put(root,'notes-fixture.json',active)
    commit(root,'synthetic future current-binding selection')
    return active,q.inventory(root,active)


def test_registration_is_inactive_root_owned_idempotent_and_drops_old_current_credit(correction):
    root,notes,inv,state,old,record=correction
    original=q.encoded(old);before=load_metadata(root,notes);job=register(correction)
    metadata=load_metadata(root,notes);uid=record['unit_id'];r=metadata['units'][uid]
    assert metadata['progress']['processed_units']==4 and metadata['progress']['pending_body_reassessment_units']==1
    assert metadata['progress']['existing_current_body_content_keep_units']==0
    assert r['current_review_valid']is False and r['requires_review'] and r['legal_status']=='LEGAL_HOLD'
    assert r['completeness']=='PENDING_BODY_CORRECTION_REASSESSMENT' and notices_for_units([uid],metadata['units'])
    assert r['review_history'][0]['body_sha256']==old['unit_bindings'][uid]['body_sha256']
    assert all(metadata['units'][uid]==before['units'][uid]for uid in old['unit_ids'][1:])
    assert q.encoded(old)==original and body.units(notes)[uid]['body']!='Corrected legal scope includes the actually stated controlled-substance class.'
    assert body.register(state,inv,root,RECORD,notes,NOW)==job['job_id'] and len(state['jobs'])==2
    with pytest.raises(ValueError,match='Only root'):
        with q.checkpoint(root,'body-author'):pytest.fail('worker wrote checkpoint')


def test_preview_is_read_only_and_requires_committed_controller_snapshot(correction):
    root,notes,inv,state,old,record=correction
    before=q.git(root,'status','--porcelain');state_raw=(root/q.STATE).read_bytes()
    result=body.preview(root,RECORD,notes)
    assert result['inactive'] and not result['current_review_valid'] and result['legal_status']=='LEGAL_HOLD'
    assert not result['daily_eligible'] and not result['release_eligible'] and result['canonical_release_credit']==result['question_audit_credit']==0
    assert before==q.git(root,'status','--porcelain') and state_raw==(root/q.STATE).read_bytes()
    (root/q.STATE).write_bytes(state_raw+b' ')
    with pytest.raises(ValueError,match='Uncommitted'):body.preview(root,RECORD,notes)


def test_census_only_old_body_validation_uses_only_explicit_bound_archive(correction):
    root,notes,inv,state,old,record=correction;register(correction)
    active=copy.deepcopy(notes);active['chapters'][0]['units'][0]['body']='Some future effective body'
    read=body.disk_reader(root);uid=record['unit_id'];sha=record['previous_binding']['body_sha256']
    restored=body.historical_notes(state,uid,sha,active,read)
    assert restored==notes and active['chapters'][0]['units'][0]['body']=='Some future effective body'
    with pytest.raises(ValueError,match='no explicit'):body.historical_notes({'body_reassessments':[]},uid,sha,active,read)


@pytest.mark.parametrize('actor,session,instance',[('body-author','fresh','new'),('other','body-author-session','new'),
                                               ('other','fresh','body-author-instance'),('known-author','fresh','new')])
def test_body_and_original_authors_cannot_claim(correction,actor,session,instance):
    root,notes,inv,state,_,_=correction;register(correction)
    with pytest.raises(ValueError,match='cannot self-audit'):
        q.claim(state,inv,actor,session,'Controller author exclusion',auditor_instance=instance,at=NOW)


def test_fresh_non_author_review_integrates_but_inactive_candidate_is_not_current_credit(correction):
    root,notes,inv,state,old,record=correction;job=register(correction)
    q.claim(state,inv,'fresh-body-reviewer','fresh-body-session','Root attested actual non-author',at=NOW)
    result,worker=worker_result((root,notes,inv),state,job,final_review(job,root,resolve=True))
    q.submit(state,job['job_id'],job['lease_token'],q.encoded(result),root,inv,NOW);persist(root,state)
    assert load_metadata(root,notes)['progress']['processed_units']==4
    integrate_files(root,result);q.integrate(state,job['job_id'],root,inv,NOW);persist(root,state)
    meta=load_metadata(root,notes);r=meta['units'][record['unit_id']]
    assert r['candidate_review_valid']is True and r['current_review_valid']is False
    assert meta['progress']['processed_units']==4 and meta['progress']['reviewed_body_candidates_not_current_credit']==1
    assert q.progress(state,inv,root)['independent_completeness_legal_processed_units']==4
    before=q.encoded(state);q.submit(state,job['job_id'],job['lease_token'],q.encoded(result),root,inv,NOW)
    q.integrate(state,job['job_id'],root,inv,NOW);assert q.encoded(state)==before
    # This explicit synthetic activation models a FUTURE separately guarded 16th
    # migration. Production code here has no activation/write operation.
    active,active_inv=activate_fixture(root,notes,record);meta=load_metadata(root,active)
    assert meta['progress']['processed_units']==5 and meta['units'][record['unit_id']]['current_review_valid']is True
    assert meta['units'][record['unit_id']]['legal_status']=='SOURCE_BLOCKED'  # unchanged negative survived
    assert q.progress(state,active_inv,root)['independent_completeness_legal_processed_units']==5


@pytest.mark.parametrize('defect',['same_body','whitespace','source_date_only','missing_mapping','dropped_claim',
    'wrong_parent','old_report_sha','author_mismatch','changed_other_unit','changed_other_binding',
    'fake_span','new_statement_outside_span','no_actual_negative','active_revision','stale_primary',
    'self_certified_credit','self_certified_census'])
def test_registration_rejects_nonsemantic_tampered_or_unbounded_author_corrections(correction,defect):
    root,notes,inv,state,old,record=correction
    rev=json.loads((root/record['replacement']['revision']['path']).read_bytes());census=json.loads((root/record['replacement']['census_path']).read_bytes())
    if defect in {'same_body','whitespace','source_date_only'}:
        rev['units'][0]['body']=body.units(notes)[record['unit_id']]['body']+('  'if defect=='whitespace'else'')
        if defect=='source_date_only':rev['source_review_date']='2026-11-04'
        rev['units'][0]['body_sha256']=q.raw_sha(rev['units'][0]['body'].encode())
    elif defect=='missing_mapping':record['claim_mapping'].pop(next(iter(record['claim_mapping'])))
    elif defect=='dropped_claim':census['claims'].pop()
    elif defect=='wrong_parent':record['previous_job_sha256']='0'*64
    elif defect=='old_report_sha':record['previous_report']['raw_sha256']='0'*64
    elif defect=='author_mismatch':rev['author_provenance']['actor_id']='hidden-author'
    elif defect=='changed_other_unit':
        notes['chapters'][0]['units'][1]['body']+=' other semantic change'
        put(root,'notes-fixture.json',notes)
    elif defect=='changed_other_binding':record['other_current_bindings_sha256']='0'*64
    elif defect=='fake_span':record['edit_spans'][0]['old_text']='unread original'
    elif defect=='new_statement_outside_span':census['claims'][0]['statement_ko']='Unrelated unsupported legal proposition'
    elif defect=='no_actual_negative':record['semantic_changed_claim_ids']=[]
    elif defect=='active_revision':rev['inactive']=False
    elif defect=='self_certified_credit':rev['independent_legal_audit_credit']=1
    elif defect=='self_certified_census':census['independent_audit']={'status':'COMPLETE','verified_units':1,'verified_claims':2}
    else:(root/record['primary_retrieval']['path']).write_bytes(b'{}\n')
    record['replacement']['revision']=put(root,record['replacement']['revision']['path'],rev)
    cb=put(root,record['replacement']['census_path'],census);record['replacement']['census_sha256']=cb['raw_sha256']
    put(root,RECORD,record);commit(root,'defective body correction fixture')
    before=q.encoded(state)
    with pytest.raises(ValueError):body.register(state,inv,root,RECORD,notes,NOW)
    assert q.encoded(state)==before


@pytest.mark.parametrize('defect',['unchanged_negative_keep','no_old_negative','no_fresh_body','no_derived_read','no_resolution_proof'])
def test_changed_hash_alone_does_not_override_old_negative_or_skip_full_review(correction,defect):
    root,notes,inv,state,old,record=correction;job=register(correction)
    q.claim(state,inv,'fresh','fresh-session','Checked original/correcting authors',at=NOW)
    def edit(report):
        final_review(job,root,resolve=True)(report);row=report['records'][0]
        if defect=='unchanged_negative_keep':
            c=row['claims'][1];c.update(legal_status='KEEP',authorities=row['claims'][0]['authorities']);c.pop('blocker',None)
        elif defect=='no_old_negative':row['claims'][0].pop('original_legal_negatives')
        elif defect=='no_fresh_body':row['actual_body_sha256']=old['unit_bindings'][record['unit_id']]['body_sha256']
        elif defect=='no_derived_read':row['body_correction_review']['all_derived_inputs_read_completely']=False
        else:row['claims'][0].pop('body_negative_reassessment')
    result,_=worker_result((root,notes,inv),state,job,edit)
    with pytest.raises(ValueError):q.submit(state,job['job_id'],job['lease_token'],q.encoded(result),root,inv,NOW)
    assert job['status']=='LEASED'


def test_recovery_fences_stale_tokens_and_duplicate_or_mixed_purpose_jobs(correction):
    root,notes,inv,state,old,record=correction;job=register(correction)
    q.claim(state,inv,'fresh','fresh-session','Actual author exclusion attested',at=NOW)
    token=job['lease_token'];branch=job['worker_branch']
    assert q.recover(state,LATER)==[job['job_id']]
    q.claim(state,inv,'replacement','replacement-session','Actual replacement exclusion',at=LATER)
    assert job['attempt']==2 and job['worker_branch']!=branch
    with pytest.raises(ValueError,match='Stale'):q.heartbeat(state,job['job_id'],token,inv,at=LATER)
    duplicate=copy.deepcopy(state);duplicate['jobs'].append(copy.deepcopy(job));duplicate['jobs'][-1].update(job_id='forged',sequence=3)
    with pytest.raises(ValueError):q.validate_state(duplicate)
    mixed=copy.deepcopy(state);mixed['jobs'][-1]['reassessment_id']='forged-census-route'
    with pytest.raises(ValueError,match='mixed-purpose'):q.validate_state(mixed)
    wrong=copy.deepcopy(inv);wrong['units'][record['unit_id']]['census_sha256']='0'*64
    with pytest.raises(ValueError,match='Assigned body/census'):q.current(job,wrong,state)


def test_unfinished_wave_cannot_register_body_correction(correction):
    root,notes,inv,state,old,record=correction
    inv=copy.deepcopy(inv);binding=copy.deepcopy(next(iter(inv['units'].values())))
    binding['body_sha256']=q.raw_sha(body.units(notes)['not-enumerated']['body'].encode())
    binding['claim_record_sha256s']={'unrelated-claim':'a'*64};inv['units']['not-enumerated']=binding
    extra=dict(job_id='unrelated-pending-wave',stage=q.STAGE,sequence=2,status='QUEUED',attempt=0,
        unit_ids=['not-enumerated'],unit_bindings={'not-enumerated':binding})
    state['jobs'].append(extra)
    with pytest.raises(ValueError,match='Finish current wave'):body.register(state,inv,root,RECORD,notes,NOW)


def test_distinct_inactive_candidates_queue_together_and_integrate_in_controller_order(correction):
    from notes_census_reassessment import LEDGER_FIELDS
    root,notes,inv,state,old,record=correction;first=register(correction)
    uid=old['unit_ids'][1];second=copy.deepcopy(record);old_unit=body.units(notes)[uid]
    census=json.loads((root/old['unit_bindings'][uid]['census_path']).read_bytes())
    census['units']=[u for u in census['units']if u['unit_id']==uid];census['claims']=[c for c in census['claims']if c['unit_id']==uid]
    census['author_provenance']=record['author_provenance']
    statement='Different synthetic corrected legal proposition in the second body.'
    candidate=dict(old_unit,body=statement,body_sha256=q.raw_sha(statement.encode()),content_version='body-second')
    census['units'][0].update(unit_content_sha256=candidate['body_sha256'],census_status='COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK')
    for c in census['claims']:c['unit_content_sha256']=candidate['body_sha256']
    census['claims'][0]['statement_ko']=statement
    revision=put(root,PREFIX+'second-revision.json',dict(purpose=body.PURPOSE,inactive=True,id='body-second',
        author_provenance=record['author_provenance'],author_instance=record['author_instance'],units=[candidate]))
    cb=put(root,PREFIX+'second-census.json',census)
    row=next(json.loads(x)for x in(root/q.LEDGER).read_text().splitlines()if json.loads(x)['unit_id']==uid)
    second.update(body_reassessment_id='body-second',unit_id=uid,previous_binding=copy.deepcopy(old['unit_bindings'][uid]),
        previous_ledger_fields={k:row.get(k)for k in LEDGER_FIELDS},
        replacement={'revision':revision,'census_path':cb['path'],'census_sha256':cb['raw_sha256'],'notes_revision':'body-second'},
        claim_mapping={c['claim_id']:[c['claim_id']]for c in census['claims']},
        semantic_changed_claim_ids=[census['claims'][0]['claim_id']],
        edit_spans=[dict(old_text=old_unit['body'],new_text=statement,old_text_sha256=q.raw_sha(old_unit['body'].encode()),
                        new_text_sha256=q.raw_sha(statement.encode()),claim_ids=[census['claims'][0]['claim_id']])],
        other_current_bindings_sha256=q.digest({k:v for k,v in inv['units'].items()if k!=uid}))
    second_path=PREFIX+'second-record.json';put(root,second_path,second);commit(root,'distinct inactive second candidate')
    second_id=body.register(state,inv,root,second_path,notes,NOW);persist(root,state);second_job=q.job_for(state,second_id)
    q.claim(state,inv,'fresh-one','session-one','Root author exclusion',at=NOW)
    q.claim(state,inv,'fresh-two','session-two','Root author exclusion',at=NOW)
    result2,_=worker_result((root,notes,inv),state,second_job,final_review(second_job,root))
    q.submit(state,second_id,second_job['lease_token'],q.encoded(result2),root,inv,NOW);integrate_files(root,result2)
    with pytest.raises(ValueError,match='assignment order'):q.integrate(state,second_id,root,inv,NOW)
    result1,_=worker_result((root,notes,inv),state,first,final_review(first,root))
    q.submit(state,first['job_id'],first['lease_token'],q.encoded(result1),root,inv,NOW);integrate_files(root,result1)
    q.integrate(state,first['job_id'],root,inv,NOW);q.integrate(state,second_id,root,inv,NOW);persist(root,state)
    metadata=load_metadata(root,notes)
    assert metadata['progress']['processed_units']==3 and metadata['progress']['reviewed_body_candidates_not_current_credit']==2
    assert all(not metadata['units'][u]['current_review_valid']for u in (record['unit_id'],uid))


@pytest.mark.parametrize('target',['record','revision','census','archived_body','archived_report','primary','derived'])
def test_committed_source_tamper_after_registration_cannot_be_claimed(correction,target):
    root,notes,inv,state,old,record=correction;job=register(correction)
    path={'record':RECORD,'revision':record['replacement']['revision']['path'],
        'census':record['replacement']['census_path'],'archived_body':record['archived_parent']['notes']['path'],
        'archived_report':record['archived_parent']['report']['path'],'primary':record['primary_retrieval']['path'],
        'derived':record['derived_preview']['path']}[target]
    (root/path).write_bytes((root/path).read_bytes()+b' ');commit(root,'tampered captured source fixture')
    with pytest.raises(ValueError,match='snapshot|SHA'):q.claim(state,inv,'fresh','fresh-session','Checked authors',at=NOW)
    assert job['status']=='QUEUED'


@pytest.mark.parametrize('defect',['access_page','stale_read_date','no_retrieval','old_review_date'])
def test_changed_negative_keep_requires_genuine_current_document_and_actual_review_dates(correction,defect):
    root,notes,inv,state,old,record=correction;job=register(correction)
    q.claim(state,inv,'fresh','fresh-session','Root attested actual actor',at=NOW)
    def edit(report):
        final_review(job,root,resolve=True)(report);row=report['records'][0];source=row['claims'][0]['authorities'][0]
        if defect=='access_page':source['source_retrieval']['document_identity_status']='HTTP200_ACCESS_PAGE'
        elif defect=='stale_read_date':source['source_retrieval']['read_at_utc']='2026-11-04T12:00:00+00:00'
        elif defect=='no_retrieval':source.pop('source_retrieval')
        else:row['reviewed_at']='2026-11-02T12:00:00+00:00'
    result,_=worker_result((root,notes,inv),state,job,edit)
    with pytest.raises(ValueError):q.submit(state,job['job_id'],job['lease_token'],q.encoded(result),root,inv,NOW)


def test_inactive_builder_selection_full_fresh_review_and_shallow_archived_reader(correction,tmp_path,monkeypatch):
    from build_full_corpus_review import compose_note_censuses
    import notes_revision
    root,notes,inv,state,old,record=correction;job=register(correction)
    assert body.registered_specs(root,notes)==[]
    # Merely selecting the candidate body before full independent integration fails.
    active=copy.deepcopy(notes)
    active['chapters'][0]['units'][0]=json.loads((root/record['replacement']['revision']['path']).read_bytes())['units'][0]
    with pytest.raises(ValueError,match='fully integrated'):body.registered_specs(root,active)
    q.claim(state,inv,'fresh','fresh-session','Actual non-author attested',at=NOW)
    result,_=worker_result((root,notes,inv),state,job,final_review(job,root))
    q.submit(state,job['job_id'],job['lease_token'],q.encoded(result),root,inv,NOW)
    integrate_files(root,result);q.integrate(state,job['job_id'],root,inv,NOW);persist(root,state)
    assert body.registered_specs(root,notes)==[]
    active,active_inv=activate_fixture(root,notes,record)
    specs=body.registered_specs(root,active);assert len(specs)==1
    assert body.census_snapshot(root,specs[0],active)=={record['unit_id']:body.units(active)[record['unit_id']]}
    forged=copy.deepcopy(specs[0]);forged['notes_revision']='forged-unregistered-revision'
    with pytest.raises(ValueError,match='Unknown/unreviewed'):body.census_snapshot(root,forged,active)
    monkeypatch.setattr(notes_revision,'load_notes',lambda *a,**kw:notes)
    initial={'path':record['previous_binding']['census_path'],'notes_revision':'current'}
    selected,claims=compose_note_censuses([initial]+specs,body.units(active),{},root)
    assert selected[record['unit_id']]['unit_content_sha256']==active_inv['units'][record['unit_id']]['body_sha256']
    assert len(claims)==10 and selected[record['unit_id']]['census_source']==record['replacement']['census_path']
    metadata=load_metadata(root,active)
    global_config=tmp_path/'empty-global.gitconfig';global_config.write_text('');monkeypatch.setenv('GIT_CONFIG_GLOBAL',str(global_config))
    shallow=tmp_path/'shallow';subprocess.run(['git','clone','-q','--depth','1',root.as_uri(),str(shallow)],check=True)
    with pytest.raises(subprocess.CalledProcessError):q.git(shallow,'cat-file','-e',result['worker_commit']+'^{commit}')
    assert load_metadata(shallow,active)==metadata and body.registered_specs(shallow,active)==specs
    (shallow/record['archived_parent']['notes']['path']).write_bytes(b'{}')
    with pytest.raises(ValueError):load_metadata(shallow,active)


@pytest.mark.parametrize('correction',['omissions'],indirect=True)
@pytest.mark.parametrize('defect',[None,'not_reassessed','unresolved_hidden','false_complete'])
def test_original_omissions_are_separate_from_corrected_legal_scope_and_cannot_disappear(correction,defect):
    root,notes,inv,state,old,record=correction;job=register(correction)
    q.claim(state,inv,'fresh','fresh-session','Actual new non-author attested',at=NOW)
    def edit(report):
        final_review(job,root)(report);row=report['records'][0]
        if defect=='not_reassessed':row['original_omission_reassessments']=[]
        elif defect=='unresolved_hidden':row['omissions']=[];row['completeness']='COMPLETE'
        elif defect=='false_complete':row['completeness']='COMPLETE'
    result,_=worker_result((root,notes,inv),state,job,edit)
    if defect:
        with pytest.raises(ValueError):q.submit(state,job['job_id'],job['lease_token'],q.encoded(result),root,inv,NOW)
    else:
        q.submit(state,job['job_id'],job['lease_token'],q.encoded(result),root,inv,NOW)
        assert result['results']==[{'unit_id':record['unit_id'],'completeness':'OMISSIONS_FOUND','legal_status':'LEGAL_HOLD'}]


@pytest.mark.parametrize('correction',['omissions'],indirect=True)
def test_census_only_successor_uses_corrected_snapshot_without_weakening_body_or_legal_hold(correction,monkeypatch):
    import notes_census_reassessment as census_route
    import notes_revision
    from build_full_corpus_review import compose_note_censuses
    from test_notes_census_reassessment import final_review as census_review
    root,notes,inv,state,old,record=correction;body_job=register(correction);uid=record['unit_id']
    q.claim(state,inv,'fresh','fresh-session','Actual non-author attested',at=NOW)
    result,_=worker_result((root,notes,inv),state,body_job,final_review(body_job,root))
    q.submit(state,body_job['job_id'],body_job['lease_token'],q.encoded(result),root,inv,NOW)
    integrate_files(root,result);q.integrate(state,body_job['job_id'],root,inv,NOW);persist(root,state)
    active,body_inv=activate_fixture(root,notes,record)
    replacement=json.loads((root/record['replacement']['census_path']).read_bytes())
    replacement['author_provenance']={'actor_id':'census-author','session_id':'census-author-session'}
    added=copy.deepcopy(replacement['claims'][0]);added.update(claim_id=uid+'-new-inventory-claim',statement_ko='Synthetic newly enumerated operational condition')
    replacement['claims'].append(added);replacement['units'][0]['claim_count']=3
    cb=put(root,PREFIX+'later-census.json',replacement)
    row=next(json.loads(x)for x in(root/q.LEDGER).read_text().splitlines()if json.loads(x)['unit_id']==uid)
    later=dict(schema_version=1,purpose=census_route.PURPOSE,reassessment_id='later-census',unit_id=uid,
        body_sha256=body_job['unit_bindings'][uid]['body_sha256'],previous_job_id=body_job['job_id'],
        previous_job_sha256=q.digest(body_job),previous_binding=copy.deepcopy(body_job['unit_bindings'][uid]),
        previous_report=result['evidence'],previous_result={'path':result['result_path'],'raw_sha256':body_job['result_sha256']},
        previous_ledger_fields={k:row.get(k)for k in census_route.LEDGER_FIELDS},
        replacement={'census_path':cb['path'],'census_sha256':cb['raw_sha256'],'notes_revision':record['replacement']['notes_revision']},
        author_provenance=replacement['author_provenance'],change_basis='Synthetic original omission enumeration after separate activation',
        claim_mapping={cid:[cid]for cid in body_job['unit_bindings'][uid]['claim_record_sha256s']},
        added_claim_ids=[added['claim_id']],changed_claim_ids=[],omission_resolutions=[{
            'omission_sha256':q.raw_sha(b'Original independently found omission'),'claim_ids':[added['claim_id']],
            'explanation':'Synthetic explicit claim enumeration; independent review still required'}])
    later_path=PREFIX+'later-census-record.json';put(root,later_path,later);commit(root,'synthetic later census-only source')
    jid=census_route.register(state,body_inv,root,later_path,active,NOW);persist(root,state);job=q.job_for(state,jid)
    with pytest.raises(ValueError,match='exact selected'):q.claim(state,body_inv,'later-reviewer','later-session','Non-author attested',at=NOW)
    specs=body.ordered_specs(root,census_route.registered_specs(root,active)+body.registered_specs(root,active))
    assert specs[-1]['body_correction_history'] and specs[-1]['path']==cb['path']
    monkeypatch.setattr(notes_revision,'load_notes',lambda *a,**kw:notes)
    initial={'path':record['previous_binding']['census_path'],'notes_revision':'current'}
    selected,_=compose_note_censuses([initial]+specs,body.units(active),{},root)
    assert selected[uid]['census_source']==cb['path']
    rows=[json.loads(x)for x in(root/q.LEDGER).read_text().splitlines()]
    rows=[census_route.replacement_row(later,replacement)if r['unit_id']==uid else r for r in rows]
    (root/q.LEDGER).write_text(''.join(json.dumps(r)+'\n'for r in rows));commit(root,'synthetic current later census binding')
    current_inv=q.inventory(root,active);q.claim(state,current_inv,'later-reviewer','later-session','Non-author attested',at=NOW)
    result2,_=worker_result((root,active,current_inv),state,job,lambda report:census_review(job,report))
    q.submit(state,jid,job['lease_token'],q.encoded(result2),root,current_inv,NOW);integrate_files(root,result2)
    q.integrate(state,jid,root,current_inv,NOW);persist(root,state)
    metadata=load_metadata(root,active)
    assert metadata['progress']['processed_units']==5 and metadata['units'][uid]['legal_status']=='LEGAL_HOLD'
    with pytest.raises(ValueError,match='exact selected'):q.current(job,body_inv,state,allow_pending=True)
