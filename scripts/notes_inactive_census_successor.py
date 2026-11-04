"""One bounded inactive N1 census successor; no active-body or release writer.

The ordinary census-only validator remains unchanged. Its body invariant is
applied to the explicitly archived inactive candidate inside this purpose only.
"""
import copy
import json
from collections import Counter
from pathlib import Path

import note_review_queue as q
import notes_body_reassessment as body
import notes_census_reassessment as census_only

PURPOSE='INACTIVE_BODY_CENSUS_SUCCESSOR'
PREFIX='reports/full-corpus-review/body-corrections/w3-a-3-v1/inactive-census-successor/'
SCOPE={
    'unit_id':'w3-a-3',
    'parent_job_id':'review-independent-notes-body-4c3229fb7bfb76b6',
    'parent_job_sha256':'0d47c2ef9a60800988de3f59adc6b3205c67985bc2c21200f457a710311833d3',
    'parent_report_sha256':'16d98bf341fc6263b26e0b6d4efc9d6b2cfc148b5639aba510248e8a77d863a3',
    'body_record_path':'reports/full-corpus-review/body-corrections/w3-a-3-v1/registrations/after-census-v2.json',
    'body_record_sha256':'945e120c2676793b7f6649d0eaa5a3cb4eb22b3f2e85fd56d273331a0730dd1c',
    'old_census_sha256':'3989096b1c43abfd73996e8ce99abe52699cdadd4ada8252ce7514540cf65a04',
    'new_census_path':'reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/census.json',
    'new_census_sha256':'78570a654e5b6af56e2892dcf54681c45ce374cb9d5368f99e626ed18d74ca24',
    'body_sha256':'e082d19727f6000e00d21a2c78e76405dfd406bf3f1a786242f57a1047c1ab4a',
    'active_semantic_sha256':'e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824',
    'old_claim_count':24,'old_source_count':42,'total_units':306,'enumerated_units':306,
    'added_source_ids':['census-v2-e-mgl11239d','census-v2-e-policy2023-01'],
    'parent_claim_counts':{'KEEP':23,'LEGAL_HOLD':1},
    'added_claim_id':'NOTE-CENSUS-V2-W3-A-3-ADD-001',
    'omission_sha256':'5431d8c76f7e57575a52e044e2330a4d5c87f4a304d94bbb89b0a76a6a07aa96',
    'packet_bindings': {
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/README.md": "83a07954b3c9628ff207f8b2697d09afe8ad848013f5f21ff50205bfa7bb04ec",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/author-handoff.json": "6852dbc91d1056de54ef66e1a08124532c38a333f205691af10c040ab693a61e",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/author-review-memo.json": "cc426d5fe095a8c51c85ed42a012c4f471aefd7b6191c978032ffe81fb3c6876",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/census.json": "78570a654e5b6af56e2892dcf54681c45ce374cb9d5368f99e626ed18d74ca24",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/evidence/current-root-binding-snapshot.json": "e31f6287084822ca4d6060c9d306143089860c61a795ad0ec49abb16e7870ea5",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/evidence/mgl11239d-retrieval.json": "0bf930332339b6f0380819aad2abbb2fd5c2b7712122249fbb3e8f82f7cb724b",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/evidence/mgl11239d.html": "bd50d9891c1ef7932b42e96703169cfa27cecfd4e9f608d45656f721607c61cd",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/evidence/mgl11239d.txt": "84173789ecccc59d70df1efb673be55ae1901caabfbc0c7ba95667dc512c5886",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/evidence/policy2023-01-retrieval.json": "8e4d9f66461ad3a27254f06e0061f7cf165458504fc1e968dd86a39e695fb845",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/evidence/policy2023-01.pdf": "b3a205bbd29c3eca5e733d08fcef9d79650b00ea0a9dbc156b4eb474200bd548",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/evidence/policy2023-01.txt": "05e82e69df1cd36aa3b3a7dc3cf12e453ef6e276f80cbb84fea04c213a84f35c",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/evidence/validation-output.txt": "b2e6ae54ec723579713c8b7af2b22ac3983ac9bfcc2af5669b991af95fdad350",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/preservation-manifest.json": "cd435983577ae62e2c9e751e9a028cc6fa5985475fd3efb422d07ff582e3ffe3",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/validate.py": "8a31d0055d2073d7fb4b54cd4cc78d3727d0353a62dfb543cbb350befc394e79",
        "reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e/validation.json": "2534675a6b462b915894238b7b8a192c6643fbb5f01ddeebb74f1dd62a035d5d"
    },
}


def semantic_sha(notes):
    return q.raw_sha(json.dumps(notes,ensure_ascii=False,sort_keys=True).encode())


def entries(state):
    return state.get('inactive_census_successors',[])


def entry_for(state,job):
    matches=[e for e in entries(state)if e['record']['inactive_census_successor_id']==job['inactive_census_successor_id']]
    q.require(len(matches)==1,'Missing unique inactive census successor record')
    return matches[0]


def chain_link(state,job,latest,used):
    entry=entry_for(state,job);r=entry['record'];uid=r['unit_id'];previous=latest.get(uid)
    identifier=job['inactive_census_successor_id']
    q.require(identifier not in used and not(job.get('body_reassessment_id')or job.get('reassessment_id')) and
              job.get('purpose')==r.get('purpose')==PURPOSE and job['unit_ids']==[uid] and
              previous is not None and previous.get('body_reassessment_id') and previous['status']=='INTEGRATED' and
              previous['job_id']==r['previous_job_id'] and q.digest(previous)==r['previous_job_sha256'] and
              previous['unit_bindings'][uid]==r['previous_binding'] and
              job['inactive_census_successor_record_sha256']==entry['raw_sha256'],
              'Inactive successor purpose/unique latest inactive parent/history changed')
    used.add(identifier)


def sibling_evolution(job,inv,state,read=None):
    """Prove forward, registered census-only supersession of historical305.

    Pending registered author versions confer no independent credit. Integrated
    versions additionally require their actual HEAD report/envelope/authorities.
    This is not a wildcard for changed rows, new bodies or unregistered sources.
    """
    r=entry_for(state,job)['record'];uid=r['unit_id'];root=Path(inv['root'])
    read=read or census_only.disk_reader(root)
    archived=json.loads(read(r['active_notes_snapshot']['path'],r['active_notes_snapshot']['raw_sha256']))
    baseline=q.inventory(root,archived,ledger_raw=read(r['active_ledger_snapshot']['path'],r['active_ledger_snapshot']['raw_sha256']))
    q.require(set(baseline['units'])==set(inv['units'])and
              q.digest({k:b for k,b in baseline['units'].items()if k!=uid})==r['other_current_bindings_sha256'],
              'Historical305 registration snapshot changed or unit set expanded')
    changes=[k for k,b in baseline['units'].items()if k!=uid and b!=inv['units'][k]]
    latest=census_only.latest_jobs(state)
    evolved=[k for k,j in latest.items()if k!=uid and j.get('reassessment_id')and
             j['unit_bindings'][k]!=baseline['units'].get(k)]
    if not changes and not evolved:return []
    q.validate_state(state)
    census_only.validate_registered(state,root,inv['notes'],read)
    for sibling in evolved:
        owner=latest[sibling]
        # Validate only this sibling; an old multi-unit job can also contain
        # the inactive target, which would otherwise recurse into this helper.
        q.current({**owner,'unit_ids':[sibling],'unit_bindings':{sibling:owner['unit_bindings'][sibling]}},
                  inv,state,allow_pending=True)
    entries_by_id={e['record']['reassessment_id']:e for e in state.get('reassessments',[])}
    proof=[]
    for sibling in sorted(changes):
        cursor=baseline['units'][sibling];target=inv['units'][sibling];steps=[]
        q.require(cursor['body_sha256']==target['body_sha256'],'Sibling body changes are outside inactive census succession')
        for node in state['jobs']:
            rid=node.get('reassessment_id')
            if not rid or node['unit_ids']!=[sibling]:continue
            e=entries_by_id[rid];record=e['record']
            if record['previous_binding']!=cursor:continue
            q.require(not(node.get('body_reassessment_id')or node.get('inactive_census_successor_id')) and
                      record['purpose']==census_only.PURPOSE and node['unit_bindings'][sibling]['body_sha256']==cursor['body_sha256'],
                      'Only explicit forward same-body native census versions may supersede historical305')
            if node['status']=='INTEGRATED':
                result=node['result'];q.validate_result(node,result)
                q.require(json.loads(read(result['result_path'],node['result_sha256']))==result and
                          any(x.get('kind')=='INTEGRATE'and x.get('job_id')==node['job_id']and
                              x.get('commit')==node.get('integrated_commit')and x.get('result_sha256')==node['result_sha256']
                              for x in state['events']),'Sibling integrated census lacks exact captured native history')
                report=json.loads(read(result['evidence']['path'],result['evidence']['raw_sha256']))
                from notes_independent_metadata import evidence_bindings
                for path,sha in set(q.validate_evidence(node,result,report))|set(evidence_bindings(report)):read(path,sha)
            cursor=node['unit_bindings'][sibling]
            steps.append(dict(job_id=node['job_id'],status=node['status'],record_path=e['record_path'],
                record_raw_sha256=e['raw_sha256'],binding_sha256=q.digest(cursor),independent_credit_created=0))
            if cursor==target:break
        q.require(steps and cursor==target,'Current sibling binding has no exact append-only native census chain')
        proof.append(dict(unit_id=sibling,original_binding_sha256=q.digest(baseline['units'][sibling]),
            current_binding_sha256=q.digest(target),native_census_supersessions=steps))
    return proof


def current(job,inv,state):
    """Only the real M binding or fully integrated exact N1/25 is admissible."""
    r=entry_for(state,job)['record'];uid=r['unit_id'];selected=inv['units'].get(uid)
    actual=body.units(inv['notes'])[uid]
    sibling_evolution(job,inv,state)
    if selected==r['active_binding']:
        q.require(q.digest(actual)==r['active_unit_record_sha256']and semantic_sha(inv['notes'])==SCOPE['active_semantic_sha256'],
                  'Inactive successor active M unit changed')
    else:
        read=census_only.disk_reader(Path(inv['root']))
        br=json.loads(read(r['body_parent_record']['path'],r['body_parent_record']['raw_sha256']))
        revision=br['replacement']['revision']
        candidate=json.loads(read(revision['path'],revision['raw_sha256']))['units'][0]
        q.require(job['status']=='INTEGRATED' and selected==job['unit_bindings'][uid] and
                  actual==candidate and q.raw_sha(actual['body'].encode())==SCOPE['body_sha256'],
                  'Inactive census successor cannot fake activation or select a stale/partial N1 binding')


def parent_info(state,root,notes,read):
    for path,sha in SCOPE['packet_bindings'].items():read(path,sha)
    uid=SCOPE['unit_id'];parent=next((j for j in state['jobs']if j['job_id']==SCOPE['parent_job_id']),None)
    q.require(parent is not None and parent['status']=='INTEGRATED' and
              q.digest(parent)==SCOPE['parent_job_sha256'] and parent.get('body_reassessment_id'),
              'Exact integrated inactive C31 parent is required')
    entry=body.entry_for(state,parent)
    q.require(entry['record_path']==SCOPE['body_record_path'] and entry['raw_sha256']==SCOPE['body_record_sha256'],
              'Inactive body registration source differs')
    record=json.loads(read(entry['record_path'],entry['raw_sha256']))
    q.require(record==entry['record'],'Inactive body registration bytes changed')
    info=body.validate_record(state,record,root,notes,read)
    q.require(info['binding']==parent['unit_bindings'][uid] and
              info['binding']['body_sha256']==SCOPE['body_sha256'] and
              info['binding']['census_sha256']==SCOPE['old_census_sha256'] and
              parent['result']['evidence']['raw_sha256']==SCOPE['parent_report_sha256'],
              'Inactive candidate/body24/C31 report binding changed')
    result=parent['result'];q.validate_result(parent,result)
    q.require(json.loads(read(result['result_path'],parent['result_sha256']))==result,
              'Inactive C31 original envelope changed')
    report=json.loads(read(result['evidence']['path'],result['evidence']['raw_sha256']))
    for path,sha in q.validate_evidence(parent,result,report):read(path,sha)
    row=next(r for r in report['records']if r['unit_id']==uid)
    q.require(row['completeness']=='OMISSIONS_FOUND' and row['legal_status']=='LEGAL_HOLD' and
              dict(Counter(c['legal_status']for c in row['claims']))==SCOPE['parent_claim_counts'] and
              len(row['omissions'])==1 and q.raw_sha(row['omissions'][0].encode())==SCOPE['omission_sha256'],
              'C31 original completeness/23KEEP/011HOLD/omission changed')
    return parent,record,info,row


def validate_record(state,r,root,notes,read=None,inv=None):
    read=read or census_only.disk_reader(root);uid=SCOPE['unit_id']
    q.require(set(r)=={'schema_version','purpose','inactive_census_successor_id','unit_id','inactive','publication_blocker',
        'change_basis','body_sha256','previous_job_id','previous_job_sha256','previous_binding','previous_report',
        'previous_result','previous_ledger_fields','body_parent_record','active_notes_snapshot','active_ledger_snapshot',
        'active_binding','active_unit_record_sha256','other_current_bindings_sha256','replacement','author_provenance',
        'author_instance','claim_mapping','changed_claim_ids','added_claim_ids','omission_resolutions','canonical_audit',
        'independent_of_authors','canonical_release_credit','question_audit_credit','current_coverage_credit',
        'new_independent_legal_audit_credit'},'Unknown/missing inactive successor fields')
    q.require(r.get('schema_version')==1 and r.get('purpose')==PURPOSE and r.get('inactive')is True and
              r.get('publication_blocker')==body.BLOCKER and r.get('unit_id')==uid and
              isinstance(r.get('inactive_census_successor_id'),str)and r['inactive_census_successor_id'].strip() and
              r.get('canonical_audit')is False and r.get('independent_of_authors')is False and
              all(type(r.get(k))is int and r[k]==0 for k in
                  ('canonical_release_credit','question_audit_credit','current_coverage_credit','new_independent_legal_audit_credit')),
              'Explicit inactive census successor with zero current/legal/release credit required')
    active=json.loads(read(r['active_notes_snapshot']['path'],r['active_notes_snapshot']['raw_sha256']))
    q.require(semantic_sha(active)==SCOPE['active_semantic_sha256'],'Retained real M semantic snapshot changed')
    raw=read(r['active_ledger_snapshot']['path'],r['active_ledger_snapshot']['raw_sha256'])
    q.require(r['active_ledger_snapshot']['path'].startswith(PREFIX) and
              r['active_ledger_snapshot']['path']!=q.LEDGER,'Dedicated immutable active-M ledger snapshot required')
    archived=q.inventory(root,active,ledger_raw=raw)
    q.require(archived['total_units']==SCOPE['total_units'] and len(archived['units'])==SCOPE['enumerated_units'] and
              archived['units'][uid]==r['active_binding'] and
              q.digest(body.units(active)[uid])==r['active_unit_record_sha256'] and
              q.digest({k:b for k,b in archived['units'].items()if k!=uid})==r['other_current_bindings_sha256'],
              'Retained active M/other305 binding snapshot changed')
    parent,br,info,parent_row=parent_info(state,root,active,read)
    q.require(r['previous_job_id']==parent['job_id'] and r['previous_job_sha256']==q.digest(parent) and
              r['previous_binding']==parent['unit_bindings'][uid] and
              r['body_parent_record']=={'path':SCOPE['body_record_path'],'raw_sha256':SCOPE['body_record_sha256']} and
              r['active_notes_snapshot']==br['archived_parent']['notes'] and
              r['active_binding']==br['previous_binding'] and
              r['previous_ledger_fields']=={k:info['row'][k]for k in census_only.LEDGER_FIELDS},
              'Inactive parent/old24/actualM ledger provenance differs')
    if inv is not None:
        q.require(inv['units']==archived['units'] and inv['notes']==active,
                  'Registration requires the actual unchanged M body and all other305 current bindings')
    replacement=r['replacement']
    q.require(replacement=={'census_path':SCOPE['new_census_path'],'census_sha256':SCOPE['new_census_sha256'],
                            'notes_revision':br['replacement']['notes_revision']} and
              r['body_sha256']==SCOPE['body_sha256'], 'Only exact same inactive N1 body and E25 census are in scope')
    new=json.loads(read(replacement['census_path'],replacement['census_sha256']));old=info['census']
    old_claims={c['claim_id']:c for c in old['claims']};new_claims={c['claim_id']:c for c in new['claims']}
    added=SCOPE['added_claim_id']
    q.require(len(old_claims)==SCOPE['old_claim_count'] and len(old['sources'])==SCOPE['old_source_count'] and
              len(new_claims)==len(old_claims)+1 and set(new_claims)==set(old_claims)|{added} and
              all(new_claims[k]==v for k,v in old_claims.items()) and
              set(new['sources'])==set(old['sources'])|set(SCOPE['added_source_ids']) and
              all(new['sources'].get(k)==v for k,v in old['sources'].items()) and
              r['claim_mapping']=={k:[k]for k in old_claims} and r['changed_claim_ids']==[] and
              r['added_claim_ids']==[added] and new_claims[added]['statement_ko'] in info['candidate']['body'],
              'All old24 claim JSON/42 sources must remain exact; only the actual omitted classification atom may be added')
    q.require(r['author_provenance']==new.get('author_provenance') and r['author_instance']==new.get('author_instance') and
              new.get('independent_of_authors')is False and new.get('canonical_audit')is False and
              all(type(v)is int and v==0 for k,v in new.items()if k.endswith('credit')),
              'Census source author or zero-credit declaration changed')
    context=copy.deepcopy(active)
    for chapter in context['chapters']:
        chapter['units']=[copy.deepcopy(info['candidate'])if u['id']==uid else u for u in chapter['units']]
    # Do not relax the ordinary public-path body invariant. A local projection
    # explicitly supplies this retained candidate solely within the new purpose.
    projected={**r,'purpose':census_only.PURPOSE,'reassessment_id':r['inactive_census_successor_id']}
    binding,carried=census_only.validate_record(state,projected,root,context,read)
    return dict(binding=binding,carried=carried,candidate=info['candidate'],parent=parent,
                body_record=br,parent_row=parent_row,derived=br['derived_preview'])


def review_contract(r,sha,info):
    return dict(inactive_census_successor_id=r['inactive_census_successor_id'],record_sha256=sha,
        candidate_body_sha256=SCOPE['body_sha256'],body_parent_record=r['body_parent_record'],
        census=r['replacement'],derived_preview=info['derived'],
        parent_omissions=[{'omission':x,'raw_sha256':q.raw_sha(x.encode())}for x in info['parent_row']['omissions']],
        omission_resolutions=r['omission_resolutions'],publication_blocker=body.BLOCKER)


def validate_registered(state,root,notes,read=None):
    read=read or census_only.disk_reader(root);out=[]
    for entry in entries(state):
        r=json.loads(read(entry['record_path'],entry['raw_sha256']))
        q.require(r==entry['record'],'Captured inactive successor differs from committed record')
        info=validate_record(state,r,root,notes,read)
        jobs=[j for j in state['jobs']if j.get('inactive_census_successor_id')==r['inactive_census_successor_id']]
        q.require(len(jobs)==1,'Inactive successor lacks unique native assignment');job=jobs[0]
        authors=set(info['parent'].get('known_author_ids',[]))|set(info['binding']['known_author_ids'])|set(r['author_provenance'].values())|{r['author_instance']}
        q.require(job['unit_bindings']=={r['unit_id']:info['binding']} and
                  job['carried_legal_blockers']=={r['unit_id']:info['carried']} and
                  authors<=set(job['known_author_ids']) and
                  job['inactive_census_successor_review']==review_contract(r,entry['raw_sha256'],info) and
                  job['prior_review_provenance']=={**info['parent']['actor_provenance'],'auditor_instance':info['parent']['auditor_instance']} and
                  any(e.get('kind')=='REGISTER_INACTIVE_CENSUS_SUCCESSOR'and e.get('job_id')==job['job_id']and
                      e.get('record_sha256')==entry['raw_sha256']for e in state['events']),
                  'Inactive assignment authors/negative/contract/registration history changed')
        if job.get('actor_provenance'):
            q.require(not {job['actor_provenance'].get('actor_id'),job['actor_provenance'].get('session_id'),job.get('auditor_instance')}&
                      set(job['prior_review_provenance'].values()),'Inactive successor must retain actual fresh non-parent session')
        out.append((r,info))
    return out


def validate_review(job,row):
    contract=job['inactive_census_successor_review'];reviewed=q.instant(row.get('reviewed_at',''))
    q.require(row.get('actual_body_sha256')==contract['candidate_body_sha256'] and
              row.get('inactive_census_successor_review')=={**contract,'final_candidate_body_read_completely':True,
                  'final_census_read_completely':True,'all_original_omissions_reassessed':True,
                  'all_original_propositions_preserved':True,'all_derived_inputs_read_completely':True,
                  'no_current_credit_before_matching_active_binding':True},
              'Fresh whole inactive body/all25/omission/derived review is required')
    assessments=row.get('original_omission_reassessments',[])
    q.require(len(assessments)==len(contract['parent_omissions']) and
              {x.get('omission_sha256')for x in assessments}=={x['raw_sha256']for x in contract['parent_omissions']} and
              all(x.get('decision')in {'RESOLVED_BY_FRESH_COMPLETE_BODY_CENSUS_REVIEW','UNRESOLVED_REMAINS_OMISSION'}and
                  isinstance(x.get('finding'),str)and x['finding'].strip()for x in assessments),
              'Every exact C31 omission requires a fresh explicit assessment')
    for item in assessments:
        if item['decision']=='UNRESOLVED_REMAINS_OMISSION':
            q.require(next(x['omission']for x in contract['parent_omissions']if x['raw_sha256']==item['omission_sha256'])in row['omissions'],
                      'Unresolved original omission cannot be hidden')
    for claim in row['claims']:
        if claim['legal_status']!='KEEP':continue
        for a in claim.get('authorities',[]):
            t=a.get('source_retrieval',{})
            q.require(t.get('mode')in {'LIVE','SAME_DAY_RETAINED_CACHE'}and t.get('http_status')==200 and
                      t.get('transport')and t.get('document_identity_status')=='OFFICIAL_DOCUMENT_TARGET_PROVISIONS_DIRECTLY_READ'and
                      t.get('raw_sha256')==a.get('evidence_sha256'),'Inactive successor KEEP requires genuine primary retrieval/read provenance')
            fetched=q.instant(t.get('retrieved_at_utc',''));read=q.instant(t.get('read_at_utc',''))
            q.require(fetched<=read<=reviewed and fetched.date()==read.date()and a.get('law_checked_date')==read.date().isoformat(),
                      'Inactive successor source/read/review dates differ')


def propose(root,identifier,ledger_snapshot,notes=None):
    """Read-only genuine inactive proposal; caller must first commit raw snapshot."""
    from notes_revision import load_notes
    notes=notes if notes is not None else load_notes(root);read=census_only.disk_reader(root)
    state=json.loads(read(q.STATE,q.raw_sha(q.safe_path(root,q.STATE).read_bytes())));q.validate_state(state)
    parent,br,info,row=parent_info(state,root,notes,read);uid=SCOPE['unit_id'];new=json.loads(read(SCOPE['new_census_path'],SCOPE['new_census_sha256']))
    inv=q.inventory(root,notes);raw=q.safe_path(root,ledger_snapshot).read_bytes()
    r=dict(schema_version=1,purpose=PURPOSE,inactive_census_successor_id=identifier,unit_id=uid,
        inactive=True,publication_blocker=body.BLOCKER,change_basis='C31 exact omitted classification atom; same inactive body; no legal blocker closure',
        body_sha256=SCOPE['body_sha256'],previous_job_id=parent['job_id'],previous_job_sha256=q.digest(parent),
        previous_binding=parent['unit_bindings'][uid],previous_report=parent['result']['evidence'],
        previous_result={'path':parent['result']['result_path'],'raw_sha256':parent['result_sha256']},
        previous_ledger_fields={k:info['row'][k]for k in census_only.LEDGER_FIELDS},
        body_parent_record={'path':SCOPE['body_record_path'],'raw_sha256':SCOPE['body_record_sha256']},
        active_notes_snapshot=br['archived_parent']['notes'],active_ledger_snapshot={'path':ledger_snapshot,'raw_sha256':q.raw_sha(raw)},
        active_binding=inv['units'][uid],active_unit_record_sha256=q.digest(body.units(notes)[uid]),
        other_current_bindings_sha256=q.digest({k:b for k,b in inv['units'].items()if k!=uid}),
        replacement={'census_path':SCOPE['new_census_path'],'census_sha256':SCOPE['new_census_sha256'],'notes_revision':br['replacement']['notes_revision']},
        author_provenance=new['author_provenance'],author_instance=new['author_instance'],
        claim_mapping={c['claim_id']:[c['claim_id']]for c in info['census']['claims']},changed_claim_ids=[],added_claim_ids=[SCOPE['added_claim_id']],
        omission_resolutions=[{'omission_sha256':SCOPE['omission_sha256'],'claim_ids':[SCOPE['added_claim_id']],
                              'explanation':'기존 분류 한정 문장을 별도 atom으로 열거하며 원24 명제·source·011 법적 보류는 그대로 보존한다.'}],
        canonical_audit=False,independent_of_authors=False,canonical_release_credit=0,question_audit_credit=0,
        current_coverage_credit=0,new_independent_legal_audit_credit=0)
    validate_record(state,r,root,notes,read,inv)
    return r


def preview(root,notes=None):
    """Inspect genuine source bytes, without inventing a registration/version."""
    from notes_revision import load_notes
    notes=notes if notes is not None else load_notes(root);read=census_only.disk_reader(root)
    state=json.loads(read(q.STATE,q.raw_sha(q.safe_path(root,q.STATE).read_bytes())));q.validate_state(state)
    parent,br,info,row=parent_info(state,root,notes,read);uid=SCOPE['unit_id'];inv=q.inventory(root,notes)
    new=json.loads(read(SCOPE['new_census_path'],SCOPE['new_census_sha256']));old=info['census']
    old_claims={c['claim_id']:c for c in old['claims']};new_claims={c['claim_id']:c for c in new['claims']}
    q.require(semantic_sha(notes)==SCOPE['active_semantic_sha256']and inv['units'][uid]==br['previous_binding']and
              len(old_claims)==SCOPE['old_claim_count']and len(old['sources'])==SCOPE['old_source_count']and
              inv['total_units']==SCOPE['total_units']and len(inv['units'])==SCOPE['enumerated_units']and
              set(new['sources'])==set(old['sources'])|set(SCOPE['added_source_ids'])and
              set(new_claims)==set(old_claims)|{SCOPE['added_claim_id']}and
              all(new_claims[k]==v for k,v in old_claims.items())and all(new['sources'].get(k)==v for k,v in old['sources'].items())and
              new_claims[SCOPE['added_claim_id']]['statement_ko'] in info['candidate']['body'],
              'Inactive source preview requires real M plus exact old24/42source preservation and one body atom')
    return dict(purpose=PURPOSE,unit_id=uid,inactive=True,registration_record_created=False,
        active_body_sha256=inv['units'][uid]['body_sha256'],candidate_body_sha256=SCOPE['body_sha256'],
        parent_job_id=parent['job_id'],parent_report=parent['result']['evidence'],
        parent_completeness=row['completeness'],parent_legal_status=row['legal_status'],
        old_claim_count=len(old_claims),new_claim_count=len(new_claims),original_sources_preserved=len(old['sources']),
        added_claim_ids=[SCOPE['added_claim_id']],source_packet_bindings=SCOPE['packet_bindings'],
        current_review_valid=False,requires_review=True,daily_eligible=False,release_eligible=False,
        current_completeness_credit=0,current_author_credit=0,current_legal_credit=0,
        canonical_release_credit=0,question_audit_credit=0,publication_blocker=body.BLOCKER,
        registration_prerequisites=['ALL_CURRENT_NATIVE_JOBS_INTEGRATED','ROOT_COMMITTED_ACTUAL_M_LEDGER_SNAPSHOT',
            'EXPLICIT_INACTIVE_SUCCESSOR_RECORD','ROOT_ONLY_REGISTER_AND_ACTUAL_FRESH_NON_AUTHOR_CLAIM'])


def register(state,inv,root,path,notes=None,at=None):
    notes=notes if notes is not None else inv['notes'];q.validate_state(state,root);read=census_only.disk_reader(root)
    q.require(path.startswith(PREFIX)and path.endswith('.json'),'Inactive successor record must have its dedicated immutable path')
    raw=q.safe_path(root,path).read_bytes();sha=q.raw_sha(raw);r=json.loads(read(path,sha));identifier=r['inactive_census_successor_id']
    old=next((e for e in entries(state)if e['record']['inactive_census_successor_id']==identifier),None)
    if old:
        q.require(old==dict(record_path=path,raw_sha256=sha,record=r),'Conflicting inactive successor registration')
        for job in state['jobs']:q.current(job,inv,state,allow_pending=True)
        validate_registered(state,root,notes,read)
        return next(j['job_id']for j in state['jobs']if j.get('inactive_census_successor_id')==identifier)
    q.require(all(j['status']=='INTEGRATED'for j in state['jobs']),'Finish current native wave before inactive successor registration')
    q.require(not entries(state),'Only the one explicitly bounded E25 successor is authorized')
    for job in state['jobs']:q.current(job,inv,state,allow_pending=True)
    q.validate_reassessments(state,inv,root)
    q.require(census_only.latest_jobs(state).get(r['unit_id'],{}).get('job_id')==r['previous_job_id'],
              'Inactive successor parent is not latest native review')
    q.integrate(state,r['previous_job_id'],root,inv,at)
    info=validate_record(state,r,root,notes,read,inv);uid=r['unit_id']
    q.require(not set(info['binding']['claim_record_sha256s'])&{cid for other,b in inv['units'].items()if other!=uid for cid in b['claim_record_sha256s']},
              'Inactive successor claim ID collides with another unit')
    at=at or q.timestamp();jid='review-independent-notes-inactive-census-'+q.digest({'record_sha256':sha})[:16]
    authors=set(info['parent'].get('known_author_ids',[]))|set(info['binding']['known_author_ids'])|set(r['author_provenance'].values())|{r['author_instance']}
    state.setdefault('inactive_census_successors',[]).append(dict(record_path=path,raw_sha256=sha,record=r))
    state['jobs'].append(dict(job_id=jid,stage=q.STAGE,purpose=PURPOSE,sequence=len(state['jobs'])+1,
        unit_ids=[uid],unit_bindings={uid:info['binding']},status='QUEUED',attempt=0,
        base_commit=q.git(root,'rev-parse','HEAD'),inventory_ledger_sha256=inv['ledger_sha256'],created_at=at,
        inactive_census_successor_id=identifier,inactive_census_successor_record_sha256=sha,
        known_author_ids=sorted(authors),carried_legal_blockers={uid:info['carried']},
        prior_review_provenance={**info['parent']['actor_provenance'],'auditor_instance':info['parent']['auditor_instance']},
        inactive_census_successor_review=review_contract(r,sha,info)))
    q.event(state,'REGISTER_INACTIVE_CENSUS_SUCCESSOR',at,job_id=jid,record_sha256=sha)
    q.validate_state(state,root);return jid


def registered_specs(root,notes):
    path=q.safe_path(root,q.STATE)
    if not path.exists():return []
    read=census_only.disk_reader(root);state=json.loads(read(q.STATE,q.raw_sha(path.read_bytes())));q.validate_state(state)
    specs=[]
    for r,info in validate_registered(state,root,notes,read):
        uid=r['unit_id'];job=next(j for j in state['jobs']if j.get('inactive_census_successor_id')==r['inactive_census_successor_id'])
        if q.raw_sha(body.units(notes)[uid]['body'].encode())!=SCOPE['body_sha256']:continue
        q.require(job['status']=='INTEGRATED','Inactive successor census cannot be activated before fresh whole review is integrated')
        result=job['result'];q.require(json.loads(read(result['result_path'],job['result_sha256']))==result,'Inactive successor envelope changed')
        report=json.loads(read(result['evidence']['path'],result['evidence']['raw_sha256']))
        from notes_independent_metadata import evidence_bindings
        for p,sha in set(q.validate_evidence(job,result,report))|set(evidence_bindings(report)):read(p,sha)
        specs.append(dict(path=r['replacement']['census_path'],notes_revision=r['replacement']['notes_revision'],
            supersedes={uid:r['previous_binding']['census_path']},body_correction_history={
                'record_path':r['body_parent_record']['path'],'raw_sha256':r['body_parent_record']['raw_sha256']}))
    return specs
