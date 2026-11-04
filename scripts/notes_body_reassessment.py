"""Root-only, inactive body correction and full non-author reassessment.

Census-only remediation is deliberately a different purpose. This module never
activates a body or edits a source/queue file outside the existing checkpoint.
"""
import copy
import json
import re

import note_review_queue as q
from notes_census_reassessment import LEDGER_FIELDS, disk_reader, latest_jobs

PURPOSE='BODY_CORRECTION_REASSESSMENT'
BLOCKER='ROOT_SEPARATE_16_FROM_ACTUALLY_PUBLISHED_15_SNAPSHOT'


def semantic(text):
    # Only explicit source-check metadata is ignored. A statutory effective date
    # or operational deadline is itself a proposition and must remain visible.
    text=re.sub(r'(?im)(source_review_date|law_checked_date|reviewed_at|출처\s*확인일|법규\s*확인일)\s*[:=]\s*'
                r'(?:19|20)\d{2}[-/.]\d{1,2}[-/.]\d{1,2}(?:T\S+)?',r'\1: <DATE>',text)
    return ' '.join(text.split())


def units(notes):
    return {u['id']:u for c in notes['chapters'] for u in c['units']}


def entries(state):
    return state.get('body_reassessments',[])


def entry_for(state,job):
    found=[e for e in entries(state) if e['record']['body_reassessment_id']==job['body_reassessment_id']]
    q.require(len(found)==1,'Missing unique body-correction record')
    return found[0]


def chain_link(state,job,latest,used):
    """Called from the scheduler's duplicate-unit chain validator."""
    bid=job['body_reassessment_id']; found=[e for e in entries(state)if e['record']['body_reassessment_id']==bid]
    q.require(len(found)==1 and bid not in used and not job.get('reassessment_id'),
              'Unknown/duplicate/mixed-purpose body reassessment')
    e=found[0];r=e['record'];uid=r['unit_id'];previous=latest.get(uid)
    q.require(r.get('purpose')==PURPOSE and job.get('purpose')==PURPOSE and job['unit_ids']==[uid] and
              previous is not None and previous['status']=='INTEGRATED' and
              previous['job_id']==r['previous_job_id'] and q.digest(previous)==r['previous_job_sha256'] and
              previous['unit_bindings'][uid]==r['previous_binding'] and
              job['body_reassessment_record_sha256']==e['raw_sha256'],
              'Body correction predecessor/history/purpose changed')
    used.add(bid)


def ancestry_bindings(state,job,uid):
    result=[];seen=set()
    while True:
        q.require(job['job_id'] not in seen,'Cyclic body correction history');seen.add(job['job_id'])
        result.append(job['unit_bindings'][uid])
        if job.get('body_reassessment_id'):
            record=entry_for(state,job)['record']
        elif job.get('reassessment_id'):
            record=next(e['record']for e in state['reassessments']if e['record']['reassessment_id']==job['reassessment_id'])
        elif job.get('inactive_census_successor_id'):
            from notes_inactive_census_successor import entry_for as inactive_entry
            record=inactive_entry(state,job)['record']
        else:return result
        job=next(j for j in state['jobs']if j['job_id']==record['previous_job_id'])


def current(job,inv,state,allow_pending=False):
    owners=latest_jobs(state);handled=set()
    for uid,binding in job['unit_bindings'].items():
        owner=owners.get(uid,job)
        if not any(e['record']['unit_id']==uid for e in entries(state)):continue
        allowed=ancestry_bindings(state,owner,uid)
        q.require(binding in allowed and inv['units'].get(uid) in allowed,
                  'Assigned body/census differs from explicit current or archived body correction')
        if owner.get('inactive_census_successor_id'):
            from notes_inactive_census_successor import current as inactive_current
            inactive_current(owner,inv,state)
        if owner.get('reassessment_id'):
            record=next(e['record']for e in state['reassessments']if e['record']['reassessment_id']==owner['reassessment_id'])
            q.require(inv['units'].get(uid)==owner['unit_bindings'][uid] or
                      (allow_pending and owner['status']=='QUEUED'and owner['attempt']==0 and
                       inv['units'].get(uid)==record['previous_binding']),
                      'Census-only successor still requires its exact selected current binding')
        handled.add(uid)
    return handled


def historical_notes(state,uid,body_sha,notes,read):
    """Validate old census-only records against an explicit archived body only."""
    if q.raw_sha(units(notes)[uid]['body'].encode())==body_sha:return notes
    for e in entries(state):
        record=e['record']
        if record['unit_id']!=uid or record['previous_binding']['body_sha256']!=body_sha:continue
        b=record['archived_parent']['notes'];archived=json.loads(read(b['path'],b['raw_sha256']))
        unit=units(archived)[uid]
        q.require(q.raw_sha(unit['body'].encode())==body_sha,'Archived census-only body snapshot changed')
        result=copy.deepcopy(notes)
        for chapter in result['chapters']:
            chapter['units']=[copy.deepcopy(unit)if u['id']==uid else u for u in chapter['units']]
        return result
    q.require(False,'Changed historical census body has no explicit body-correction archive')


def selected_is_current(job,inv):
    return all(inv['units'].get(uid)==b for uid,b in job['unit_bindings'].items())


def current_content_keep_count(state,inv):
    actual=units(inv['notes'])
    excluded=sum(bool(j.get('body_reassessment_id')or j.get('inactive_census_successor_id'))and not selected_is_current(j,inv)and
                 actual[uid].get('independent_content_review',{}).get('decision')=='KEEP'
                 for uid,j in latest_jobs(state).items())
    return inv['existing_content_keep_units']-excluded


def derived_inputs(root,notes,uid,candidate):
    """Exact relevant final authored cards plus candidate source hashes; no UI writes."""
    from notes_revision import apply_study_revision
    old=units(notes);result=[]
    for kind,path,collections in [('study','notes/study/guide.json',['lessons','comparisons','clocks']),
                                  ('refresh','notes/refresh/guide.json',['cards','glossary'])]:
        if not (root/path).exists():continue  # Minimal fixtures have no authored cards.
        data=apply_study_revision(json.loads((root/path).read_bytes()),kind,root,notes_context=notes)
        for collection in collections:
            for item in data.get(collection,[]):
                if uid not in item.get('note_units',[]):continue
                before={x:q.raw_sha(old[x]['body'].encode())for x in item['note_units']}
                after=dict(before);after[uid]=q.raw_sha(candidate['body'].encode())
                result.append(dict(collection=kind+'.'+collection,id=item.get('id',item.get('term')),
                    original=copy.deepcopy(item),candidate=copy.deepcopy(item),text_changed=False,
                    source_hashes_before=before,source_hashes_candidate=after))
    chapter=next(c for c in notes['chapters']if any(u['id']==uid for u in c['units']))
    if all(k in chapter for k in ('id','title','summary','highlights')):
        text={k:chapter[k]for k in ('title','summary','highlights')}
        before={u['id']:q.raw_sha(u['body'].encode())for u in chapter['units']};after=dict(before)
        after[uid]=q.raw_sha(candidate['body'].encode())
        result.append(dict(collection='refresh.chapter-overview',id='RF-C-'+chapter['id'],
            original=text,candidate=copy.deepcopy(text),text_changed=False,
            source_hashes_before=before,source_hashes_candidate=after))
    return result


def replacement_row(record,census,candidate):
    row=dict(record['previous_ledger_fields']);unit=census['units'][0]
    row.update(actual_effective_body_sha256=q.raw_sha(candidate['body'].encode()),
        atomic_census_source=record['replacement']['census_path'],
        atomic_census_notes_revision=record['replacement']['notes_revision'],
        atomic_claim_census_status=unit['census_status'],atomic_claim_census_complete=True,
        atomic_claim_ids=[c['claim_id']for c in census['claims']],
        atomic_source_blocked_count=sum(c['review_status']=='SOURCE_BLOCKED'for c in census['claims']))
    return row


def validate_record(state,record,root,notes,read=None,inv=None):
    read=read or disk_reader(root)
    q.require(record.get('schema_version')==1 and record.get('purpose')==PURPOSE and record.get('inactive') is True and
              record.get('publication_blocker')==BLOCKER and record.get('change_basis') and
              record.get('body_reassessment_id'), 'Explicit inactive BODY_CORRECTION_REASSESSMENT required')
    uid=record['unit_id'];previous=next((j for j in state['jobs']if j['job_id']==record['previous_job_id']),None)
    q.require(previous is not None and previous['status']=='INTEGRATED' and
              q.digest(previous)==record['previous_job_sha256'] and previous['unit_bindings'].get(uid)==record['previous_binding'],
              'Body correction must pin exact integrated parent')
    original=record['previous_binding'];parent=record['archived_parent']
    get=lambda b:read(b['path'],b['raw_sha256'])
    old_notes=json.loads(get(parent['notes']));old_unit=units(old_notes)[uid]
    snapshot=json.loads(get(parent['job']))
    q.require(snapshot['job']==previous and
              snapshot['events']==[e for e in state['events']if e.get('job_id')==previous['job_id']] and
              any(e.get('kind')=='INTEGRATE'and e.get('commit')==previous.get('integrated_commit')for e in snapshot['events']) and
              q.raw_sha(old_unit['body'].encode())==original['body_sha256'],
              'Archived parent body/job snapshot changed')
    result=previous['result'];q.validate_result(previous,result)
    q.require(record['previous_report']==result['evidence'] and
              record['previous_result']=={'path':result['result_path'],'raw_sha256':previous['result_sha256']} and
              get(parent['report'])==get(record['previous_report']) and
              get(parent['result'])==get(record['previous_result']) and json.loads(get(parent['result']))==result,
              'Body correction parent report/envelope raw bindings changed')
    report=json.loads(get(parent['report']))
    for path,sha in q.validate_evidence(previous,result,report):read(path,sha)
    row=next(r for r in report['records']if r['unit_id']==uid)
    q.require(row['legal_status'] in {'LEGAL_HOLD','SOURCE_BLOCKED'},
              'Body correction requires actual parent legal negative, not new positive review')
    old_census_raw=get(parent['census'])
    q.require(q.raw_sha(old_census_raw)==original['census_sha256'] and
              old_census_raw==read(original['census_path'],original['census_sha256']),
              'Archived parent census differs from original immutable JSON')
    old_census=json.loads(old_census_raw);old_claims=[c for c in old_census['claims']if c['unit_id']==uid]
    old_units=[u for u in old_census['units']if u['unit_id']==uid]
    q.require(len(old_units)==1 and q.digest(old_units[0])==original['census_unit_record_sha256'] and
              {c['claim_id']:q.digest(c)for c in old_claims}==original['claim_record_sha256s'],
              'Parent claim records/unit binding changed')
    fields=record['previous_ledger_fields']
    q.require(set(fields)==set(LEDGER_FIELDS) and q.digest(fields)==original['ledger_binding_sha256'],
              'Parent ledger binding changed')
    revision=json.loads(get(record['replacement']['revision']));author=record['author_provenance']
    q.require(set(author)=={'actor_id','session_id'} and all(isinstance(x,str)and x.strip()for x in author.values()) and
              isinstance(record.get('author_instance'),str)and record['author_instance'].strip() and
              revision.get('purpose')==PURPOSE and revision.get('inactive') is True and
              revision.get('author_provenance')==author and revision.get('author_instance')==record['author_instance'] and
              [u['id']for u in revision['units']]==[uid], 'Inactive body author/unit scope changed')
    candidate=revision['units'][0];body=q.raw_sha(candidate['body'].encode())
    expected_unit=copy.deepcopy(old_unit)
    expected_unit.pop('independent_content_review',None)  # an old-body KEEP is historical only
    expected_unit.update(body=candidate['body'],body_sha256=body,content_version=revision['id'])
    q.require(candidate==expected_unit,'Body candidate changes unit fields outside body/hash/version scope')
    q.require(body==candidate['body_sha256'] and body!=original['body_sha256'] and
              semantic(candidate['body'])!=semantic(old_unit['body']),
              'Body correction needs actual semantic delta, not whitespace/source-date metadata')
    q.require(body not in {j['unit_bindings'][uid]['body_sha256']for j in state['jobs']
                          if uid in j['unit_bindings']and j['sequence']<=previous['sequence']},
              'An archived body hash cannot return as a newly corrected positive version')
    rebuilt=old_unit['body'];covered=[]
    for span in record['edit_spans']:
        q.require(span['old_text'] and rebuilt.count(span['old_text'])==1 and
                  semantic(span['old_text'])!=semantic(span['new_text']) and
                  q.raw_sha(span['old_text'].encode())==span['old_text_sha256'] and
                  q.raw_sha(span['new_text'].encode())==span['new_text_sha256'], 'Body correction edit span is stale/nonsemantic')
        rebuilt=rebuilt.replace(span['old_text'],span['new_text'],1);covered.extend(span['claim_ids'])
    q.require(rebuilt==candidate['body'], 'Candidate body changes outside exact correction spans')
    actual=units(notes)
    q.require(uid in actual,'Body correction unit is absent from current notes')
    if inv is not None:
        q.require(inv['units'].get(uid)==original and actual[uid]==old_unit,
                  'Body correction predecessor must be the exact currently selected body/census/unit')
        q.require({k:q.digest(u)for k,u in actual.items()if k!=uid}==
                  {k:q.digest(u)for k,u in units(old_notes).items()if k!=uid},
                  'Body correction changed another unit or dropped the archived inventory')
    census=json.loads(read(record['replacement']['census_path'],record['replacement']['census_sha256']))
    for author_record in (record,revision,census):
        q.require(all(type(v)is int and v==0 for k,v in author_record.items()if k.endswith('credit')) and
                  author_record.get('canonical_audit',False)is False and
                  author_record.get('independent_of_authors',False)is False,
                  'Author correction cannot claim independent/canonical/question credit')
    if 'independent_audit' in census:
        q.require(census['independent_audit']=={'status':'NOT_PERFORMED_BY_THIS_AUTHOR','verified_units':0,'verified_claims':0},
                  'Author census cannot certify its own independent completeness/legal audit')
    q.require(record['replacement']['census_path']!=original['census_path'] and
              record['replacement']['notes_revision']==revision['id'] and
              census.get('author_provenance')==author and [u['unit_id']for u in census['units']]==[uid] and
              all(c['unit_id']==uid for c in census['claims']) and census['units'][0]['census_status']==
              'COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK',
              'Body correction requires a new exact single-unit author census, not independent completion')
    for source in census.get('sources',{}).values():
        q.require(source['official_url'].startswith('https://'),'Body correction source requires official HTTPS')
        read(source['source_evidence'],source['source_evidence_sha256'])
    new_row=replacement_row(record,census,candidate)
    binding=q.inventory(root,{'chapters':[{'units':[candidate]}]},ledger_raw=(json.dumps(new_row)+'\n').encode())['units'][uid]
    old={c['claim_id']:c for c in old_claims};new={c['claim_id']:c for c in census['claims']}
    mapping=record['claim_mapping'];added=record['added_claim_ids'];mapped=[x for v in mapping.values()for x in v]
    q.require(set(mapping)==set(old) and all(isinstance(v,list)and v for v in mapping.values()) and
              len(mapped)==len(set(mapped)) and len(added)==len(set(added)) and not set(mapped)&set(added) and
              set(mapped+added)==set(new),'Every original claim needs exact mapping; no dropped/duplicate/current orphan claim')
    changed=sorted(cid for oid,ids in mapping.items()for cid in ids if semantic(new[cid]['statement_ko'])!=semantic(old[oid]['statement_ko']))
    delta=set(changed)|set(added)
    q.require(changed==record['semantic_changed_claim_ids'] and changed and delta==set(covered) and
              all(semantic(new[cid]['statement_ko']) not in {semantic(c['statement_ko'])for c in old.values()}for cid in added) and
              all(any(semantic(new[cid]['statement_ko']) in semantic(s['new_text'])for s in record['edit_spans']if cid in s['claim_ids'])for cid in delta),
              'Changed statements must be real propositions in exact corrected body spans')
    for historical in state['jobs']:
        if uid not in historical['unit_bindings']or historical['sequence']>previous['sequence']:continue
        envelope=historical['result'];historical_report=json.loads(get(envelope['evidence']))
        historical_census=json.loads(read(historical['unit_bindings'][uid]['census_path'],historical['unit_bindings'][uid]['census_sha256']))
        negative_ids={c['claim_id']for r in historical_report['records']if r['unit_id']==uid
                      for c in r['claims']if c['legal_status']!='KEEP'}
        unsafe_statements={semantic(c['statement_ko'])for c in historical_census['claims']
                           if c['unit_id']==uid and c['claim_id'] in negative_ids}
        q.require(not {semantic(new[cid]['statement_ko'])for cid in changed}&unsafe_statements,
                  'A previously negative unchanged statement cannot return through a renamed/modified version')
    retrieval=json.loads(get(record['primary_retrieval']))
    q.require(isinstance(retrieval.get('retrievals'),list)and retrieval['retrievals'],
              'Body correction needs retained actual primary retrieval/blocked-attempt provenance')
    for source in retrieval['retrievals']:
        q.require(source.get('requested_url','').startswith('https://')and source.get('retrieval_started_at_utc') and
                  source.get('transport') and source.get('document_identity_status'),
                  'Body correction primary retrieval provenance incomplete')
        if source.get('raw_path'):read(source['raw_path'],source['raw_sha256'])
        if source.get('extracted_text_path'):read(source['extracted_text_path'],source['extracted_text_sha256'])
    if not any(s.get('status')==200 and s.get('document_identity_status')=='OFFICIAL_DOCUMENT_TARGET_PROVISIONS_DIRECTLY_READ'
               for s in retrieval['retrievals']):
        q.require(all(new[cid]['review_status']=='SOURCE_BLOCKED'for cid in changed),
                  'Blocked/access-page source attempts cannot become author source checks')
    carried={};reconsidered={}
    for claim in row['claims']:
        if claim['legal_status']=='KEEP':continue
        negatives=[*claim.get('inherited_legal_blockers',[]),dict(original_claim_id=claim['claim_id'],
            legal_status=claim['legal_status'],finding=claim['finding'],blocker=claim['blocker'],
            original_report_sha256=result['evidence']['raw_sha256'])]
        for cid in mapping[claim['claim_id']]:
            target=(reconsidered if cid in changed else carried).setdefault(cid,[])
            for negative in negatives:
                if negative not in target:target.append(negative)
    q.require(reconsidered,'At least one actually changed original legal negative required')
    preview=json.loads(get(record['derived_preview']))
    q.require(preview['items']==derived_inputs(root,old_notes,uid,candidate) and
              preview.get('full_published_builder_status')=='NOT_RUN_INACTIVE_BODY_PUBLICATION_REQUIRES_SEPARATE_16',
              'Actual related derived inputs/candidate source hashes changed or publication claimed')
    if inv is not None:
        q.require(q.digest({k:b for k,b in inv['units'].items()if k!=uid})==record['other_current_bindings_sha256'],
                  'Body correction changed another unit claim binding')
    return dict(binding=binding,carried=carried,reconsidered=reconsidered,candidate=candidate,
                old_notes=old_notes,census=census,row=new_row,derived=preview,parent_omissions=row['omissions'])


def review_contract(record,sha,info):
    return dict(body_reassessment_id=record['body_reassessment_id'],record_sha256=sha,
        revision=record['replacement']['revision'],census={'path':record['replacement']['census_path'],
        'raw_sha256':record['replacement']['census_sha256']},derived_preview=record['derived_preview'],
        semantic_changed_claim_ids=record['semantic_changed_claim_ids'],
        changed_statement_sha256s={c['claim_id']:q.digest(c['statement_ko'])for c in info['census']['claims']
                                  if c['claim_id'] in record['semantic_changed_claim_ids']},
        parent_omissions=[{'omission':x,'raw_sha256':q.raw_sha(x.encode())}for x in info['parent_omissions']],
        edit_span_sha256s=[q.digest(s)for s in record['edit_spans']],publication_blocker=BLOCKER)


def validate_registered(state,root,notes,read=None,inv=None):
    read=read or disk_reader(root);out=[]
    for e in entries(state):
        record=json.loads(read(e['record_path'],e['raw_sha256']))
        q.require(record==e['record'],'Captured body correction differs from committed immutable record')
        # The immutable registration already bound the other-unit snapshot.
        # Current unrelated units may later receive their own explicit versions.
        info=validate_record(state,record,root,notes,read)
        job=next(j for j in state['jobs']if j.get('body_reassessment_id')==record['body_reassessment_id'])
        q.require(job['unit_bindings']=={record['unit_id']:info['binding']} and
                  job['carried_legal_blockers']=={record['unit_id']:info['carried']} and
                  job['reconsidered_legal_negatives']=={record['unit_id']:info['reconsidered']} and
                  job['body_correction_review']==review_contract(record,e['raw_sha256'],info) and
                  set(record['previous_binding']['known_author_ids'])|set(record['author_provenance'].values())|
                  {record['author_instance']} <= set(job['known_author_ids']) and
                  any(x.get('kind')=='REGISTER_BODY_CORRECTION'and x.get('job_id')==job['job_id']and
                      x.get('record_sha256')==e['raw_sha256']for x in state['events']),
                  'Body assignment/source author/negative/registration binding changed')
        out.append((record,info))
    return out


def validate_review(job,row):
    contract=job['body_correction_review']
    reviewed=q.instant(row.get('reviewed_at',''))
    q.require(row.get('actual_body_sha256')==job['unit_bindings'][row['unit_id']]['body_sha256'] and
              row.get('body_correction_review')=={**contract,'final_body_read_completely':True,
                'final_census_read_completely':True,'all_parent_negatives_explicitly_reassessed':True,
                'all_parent_omissions_explicitly_reassessed':True,
                'all_derived_inputs_read_completely':True,'no_current_credit_before_matching_active_binding':True},
              'Full fresh body/census/derived/negative review of exact candidate is required')
    omissions=row.get('original_omission_reassessments')
    q.require(isinstance(omissions,list)and len(omissions)==len(contract['parent_omissions']) and
              {x.get('omission_sha256')for x in omissions}=={x['raw_sha256']for x in contract['parent_omissions']} and
              all(x.get('decision') in {'RESOLVED_BY_FRESH_COMPLETE_BODY_CENSUS_REVIEW','UNRESOLVED_REMAINS_OMISSION'}and
                  isinstance(x.get('finding'),str)and x['finding'].strip()for x in omissions),
              'Every original omission needs an explicit fresh body/census reassessment')
    unresolved={x['omission_sha256']for x in omissions if x['decision']=='UNRESOLVED_REMAINS_OMISSION'}
    q.require(all(x['omission'] in row.get('omissions',[])for x in contract['parent_omissions']if x['raw_sha256'] in unresolved),
              'Unresolved original omission cannot be hidden from current completeness')
    reconsidered=job['reconsidered_legal_negatives'][row['unit_id']]
    for claim in row['claims']:
        cid=claim['claim_id']
        if claim.get('legal_status')=='KEEP':
            for source in claim.get('authorities',[]):
                retrieval=source.get('source_retrieval',{})
                q.require(retrieval.get('mode') in {'LIVE','SAME_DAY_RETAINED_CACHE'} and
                          retrieval.get('http_status')==200 and retrieval.get('transport') and
                          retrieval.get('document_identity_status')=='OFFICIAL_DOCUMENT_TARGET_PROVISIONS_DIRECTLY_READ' and
                          retrieval.get('raw_sha256')==source.get('evidence_sha256'),
                          'Fresh body KEEP needs actual official document provenance; access pages are not proof')
                retrieved=q.instant(retrieval.get('retrieved_at_utc',''));read_at=q.instant(retrieval.get('read_at_utc',''))
                q.require(retrieved<=read_at<=reviewed and retrieved.date()==read_at.date() and
                          source.get('law_checked_date')==read_at.date().isoformat(),
                          'Body authority actual retrieval/cache/read/review dates differ')
        if cid not in reconsidered:continue
        review=claim.get('body_negative_reassessment',{})
        q.require(claim.get('original_legal_negatives')==reconsidered[cid] and
                  review.get('original_negatives_sha256')==q.digest(reconsidered[cid]) and
                  review.get('changed_statement_sha256')==contract['changed_statement_sha256s'][cid] and
                  review.get('edit_span_sha256s')==contract['edit_span_sha256s'] and
                  review.get('original_negative_read_completely') is True and
                  review.get('corrected_statement_read_completely') is True and
                  isinstance(review.get('finding'),str)and review['finding'].strip(),
                  'Original legal negative and genuinely changed proposition require explicit fresh reassessment')
        q.require(review.get('decision')==('RESOLVED_BY_CHANGED_BODY_AND_PROPOSITION'if claim['legal_status']=='KEEP'else'UNRESOLVED_REMAINS_HELD') and
                  (claim['legal_status']!='KEEP' or bool(claim.get('authorities'))),
                  'New positive opinion cannot override unchanged body/statement or omit current primary proof')


def register(state,inv,root,record_path,notes=None,at=None):
    from notes_revision import load_notes
    q.validate_state(state,root);notes=notes if notes is not None else load_notes(root)
    read=disk_reader(root);raw=q.safe_path(root,record_path).read_bytes();sha=q.raw_sha(raw)
    for job in state['jobs']:q.current(job,inv,state,allow_pending=True)
    record=json.loads(read(record_path,sha));bid=record['body_reassessment_id']
    old=next((e for e in entries(state)if e['record']['body_reassessment_id']==bid),None)
    if old:
        q.require(old=={'record_path':record_path,'raw_sha256':sha,'record':record},'Conflicting body correction registration')
        validate_registered(state,root,notes,read,inv)
        return next(j['job_id']for j in state['jobs']if j.get('body_reassessment_id')==bid)
    q.require(all(j['status']=='INTEGRATED'or(j.get('body_reassessment_id')and j['status']=='QUEUED'and j['attempt']==0)
                  for j in state['jobs']),'Finish current wave before body correction registration')
    q.require(latest_jobs(state).get(record['unit_id'],{}).get('job_id')==record['previous_job_id'],
              'Body correction predecessor is not current')
    # Registration uses the controller's original Git/branch/evidence checks;
    # only the read-only publication consumer is independent of old Git objects.
    q.integrate(state,record['previous_job_id'],root,inv,at)
    info=validate_record(state,record,root,notes,read,inv);uid=record['unit_id']
    q.require(not set(info['binding']['claim_record_sha256s'])&{cid for other,b in inv['units'].items()if other!=uid
                                                             for cid in b['claim_record_sha256s']},
              'Body correction claim ID belongs to another unit')
    identifier='review-independent-notes-body-'+q.digest({'record_sha256':sha})[:16];at=at or q.timestamp()
    previous=next(j for j in state['jobs']if j['job_id']==record['previous_job_id'])
    authors=set(previous.get('known_author_ids',[]))|set(info['binding']['known_author_ids'])|set(record['author_provenance'].values())|{record['author_instance']}
    state.setdefault('body_reassessments',[]).append(dict(record_path=record_path,raw_sha256=sha,record=record))
    state['jobs'].append(dict(job_id=identifier,stage=q.STAGE,purpose=PURPOSE,sequence=len(state['jobs'])+1,
        unit_ids=[uid],unit_bindings={uid:info['binding']},status='QUEUED',attempt=0,
        base_commit=q.git(root,'rev-parse','HEAD'),inventory_ledger_sha256=inv['ledger_sha256'],created_at=at,
        body_reassessment_id=bid,body_reassessment_record_sha256=sha,known_author_ids=sorted(authors),
        carried_legal_blockers={uid:info['carried']},reconsidered_legal_negatives={uid:info['reconsidered']},
        body_correction_review=review_contract(record,sha,info)))
    q.event(state,'REGISTER_BODY_CORRECTION',at,job_id=identifier,body_reassessment_id=bid,record_sha256=sha)
    q.validate_state(state,root)
    return identifier


def preview(root,record_path,notes=None):
    from notes_revision import load_notes
    notes=notes if notes is not None else load_notes(root);read=disk_reader(root)
    state=json.loads(read(q.STATE,q.raw_sha(q.safe_path(root,q.STATE).read_bytes())));q.validate_state(state)
    raw=q.safe_path(root,record_path).read_bytes();record=json.loads(read(record_path,q.raw_sha(raw)))
    inv=q.inventory(root,notes)
    for job in state['jobs']:q.current(job,inv,state,allow_pending=True)
    info=validate_record(state,record,root,notes,read,inv)
    return dict(purpose=PURPOSE,unit=info['candidate'],census_binding=info['binding'],
        mandatory_carried_legal_blockers=info['carried'],changed_proposition_negatives_requiring_fresh_review=info['reconsidered'],
        derived_inputs=info['derived'],inactive=True,current_review_valid=False,requires_review=True,
        completeness='NOT_ASSESSED',legal_status='LEGAL_HOLD',daily_eligible=False,release_eligible=False,
        publication_blocker=BLOCKER,canonical_release_credit=0,question_audit_credit=0,independent_legal_audit_credit=0)


def registered_specs(root,notes):
    """Select a reviewed census only after an external guarded body activation.

    An inactive candidate is never an input to load_notes or the public builders.
    This hook does not activate it, alter an edition, or authorize publication.
    """
    path=q.safe_path(root,q.STATE)
    if not path.exists():return []
    read=disk_reader(root);state=json.loads(read(q.STATE,q.raw_sha(path.read_bytes())))
    q.validate_state(state)
    if not entries(state):return []
    actual=units(notes);specs=[]
    for record,info in validate_registered(state,root,notes,read):
        uid=record['unit_id'];job=next(j for j in state['jobs']if j.get('body_reassessment_id')==record['body_reassessment_id'])
        # A newer inactive candidate must not remove the last active census.
        # Keep historical versions through the actually selected body in order.
        body_owners=[j for j in state['jobs']if uid in j['unit_ids']and j.get('body_reassessment_id')]
        matching=[j for j in body_owners if q.raw_sha(actual[uid]['body'].encode())==j['unit_bindings'][uid]['body_sha256']]
        q.require(len(matching)<=1,'Ambiguous reused active body hash')
        if not matching or job['sequence']>matching[0]['sequence']:continue
        q.require(job['status']=='INTEGRATED','Active corrected body needs a fully integrated fresh independent review')
        result=job['result'];q.validate_result(job,result)
        q.require(json.loads(read(result['result_path'],job['result_sha256']))==result,
                  'Body review envelope differs from committed snapshot')
        report=json.loads(read(result['evidence']['path'],result['evidence']['raw_sha256']))
        from notes_independent_metadata import evidence_bindings
        for relative,sha in set(q.validate_evidence(job,result,report))|set(evidence_bindings(report)):read(relative,sha)
        entry=entry_for(state,job)
        specs.append(dict(path=record['replacement']['census_path'],notes_revision=record['replacement']['notes_revision'],
            supersedes={uid:record['previous_binding']['census_path']},
            body_correction_record={'path':entry['record_path'],'raw_sha256':entry['raw_sha256']}))
    return specs


def ordered_specs(root,specs):
    """Interleave explicit census-only/body successors in controller order."""
    path=q.safe_path(root,q.STATE)
    if not path.exists():return specs
    state=json.loads(disk_reader(root)(q.STATE,q.raw_sha(path.read_bytes())))
    q.validate_state(state)
    jobs={j['unit_bindings'][j['unit_ids'][0]]['census_path']:j
          for j in state['jobs']if j.get('reassessment_id')or j.get('body_reassessment_id')or j.get('inactive_census_successor_id')}
    sequence={p:j['sequence']for p,j in jobs.items()}
    q.require(all(s['path'] in sequence for s in specs),'Unregistered note census replacement spec')
    out=[]
    for original in specs:
        spec=copy.deepcopy(original);job=jobs[spec['path']];uid=job['unit_ids'][0]
        if job.get('reassessment_id'):
            history=[e for e in entries(state)if e['record']['unit_id']==uid and
                     next(j for j in state['jobs']if j.get('body_reassessment_id')==e['record']['body_reassessment_id'])['sequence']<job['sequence'] and
                     next(j for j in state['jobs']if j.get('body_reassessment_id')==e['record']['body_reassessment_id'])['unit_bindings'][uid]['body_sha256']==job['unit_bindings'][uid]['body_sha256']]
            if history:
                q.require(len(history)==1,'Ambiguous corrected-body census ancestry')
                spec['body_correction_history']={k:history[0][k]for k in ('record_path','raw_sha256')}
        out.append(spec)
    return sorted(out,key=lambda s:sequence[s['path']])


def census_snapshot(root,spec,notes):
    """Exact registered spec only; a caller cannot smuggle an inactive revision."""
    from notes_census_reassessment import registered_specs as census_specs
    from notes_inactive_census_successor import registered_specs as inactive_specs
    matches=[s for s in ordered_specs(root,registered_specs(root,notes)+census_specs(root,notes)+inactive_specs(root,notes))if s==spec]
    q.require(len(matches)==1,'Unknown/unreviewed/inactive body census builder spec')
    binding=spec.get('body_correction_record')
    if binding is None:
        history=spec['body_correction_history'];binding={'path':history['record_path'],'raw_sha256':history['raw_sha256']}
    record=json.loads(disk_reader(root)(binding['path'],binding['raw_sha256']))
    # Historical corrected versions need their immutable candidate snapshot;
    # the final compose check still requires the selected current body exactly.
    revision=json.loads(disk_reader(root)(record['replacement']['revision']['path'],record['replacement']['revision']['raw_sha256']))
    return {u['id']:u for u in revision['units']}
