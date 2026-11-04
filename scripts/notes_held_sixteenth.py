"""Source-only N1 held activation and sixteenth gate; approvals are absent.

Builder-source approval is separate from publication approval. Both require real
published15 proof and an actual complete fresh25 review; this module creates none.
"""
import argparse
import copy
import json
from pathlib import Path

import note_review_queue as q
import notes_body_reassessment as body
import notes_census_reassessment as census
import notes_inactive_census_successor as inactive
import notes_published15_closure as old

ROOT=Path(__file__).resolve().parents[1]
SOURCE='revisions/notes/held-n1-activation.json'
MANIFEST='revisions/notes/protected-migration-held-n1.json'
EDITION='2026-11-04.w3-a-3-held.1'
SIBLINGS={'w3-a-15','w3-a-16','return-pathways'}
APPROVED_ACTIVATION_SOURCES={}
APPROVED_MIGRATIONS={}


def validate_job(root,state,job):
    old.require(job['status']=='INTEGRATED'and job.get('controller_independence_basis'),
                'Actual integrated native non-author review is required')
    actor=job['actor_provenance'];authors=set(job.get('known_author_ids',[]))|{
        a for b in job['unit_bindings'].values()for a in b['known_author_ids']}
    old.require(not {actor['actor_id'],actor['session_id'],job['auditor_instance']}&authors and
        any(e.get('kind')=='CLAIM'and e.get('job_id')==job['job_id']and e.get('actor')==actor and e.get('attempt')==job['attempt']for e in state['events'])and
        any(e.get('kind')=='INTEGRATE'and e.get('job_id')==job['job_id']and e.get('commit')==job.get('integrated_commit')and
            e.get('result_sha256')==job['result_sha256']for e in state['events']),
        'Actual native claim/integration/author exclusion provenance changed')
    result=job['result'];q.validate_result(job,result)
    old.require(json.loads(old.committed(root,result['result_path'],job['result_sha256']))==result and
        any(e.get('kind')=='SUBMIT'and e.get('job_id')==job['job_id']and e.get('result_sha256')==job['result_sha256']for e in state['events']),
        'Native original submission/envelope differs')
    report=json.loads(old.committed(root,result['evidence']['path'],result['evidence']['raw_sha256']))
    from notes_independent_metadata import evidence_bindings
    for p,sha in set(q.validate_evidence(job,result,report))|set(evidence_bindings(report)):old.committed(root,p,sha)
    return report


@old.snapshotted
def source_contract(root):
    raw=old.committed(root,SOURCE);binding={'path':SOURCE,'raw_sha256':old.sha(raw)}
    approval=APPROVED_ACTIVATION_SOURCES.get((SOURCE,binding['raw_sha256']))
    old.require(approval is not None,'BLOCKED: no actual published15/fresh25 held-builder source approval')
    config=json.loads(raw)
    old.require(config.get('closure')==approval['closure']and config.get('review')==approval['review'],
                'Held source differs from explicit actual-publication/fresh-review approval')
    return validate_source_payload(root,config,binding)


def validate_source_payload(root,config,binding=None):
    old.require(set(config)=={'schema_version','purpose','edition','unit_id','closure','review','required_sibling_jobs',
        'release_eligible','current_legal_pass','canonical_release_credit','question_audit_credit',
        'new_author_review_credit','new_independent_legal_audit_credit'},'Unknown/missing held-source fields')
    old.require(config.get('schema_version')==1 and config.get('purpose')=='N1_HELD_BUILDER_SOURCE_NOT_PUBLICATION_APPROVAL'and
        config.get('edition')==EDITION and config.get('unit_id')==inactive.SCOPE['unit_id']and
        set(config.get('required_sibling_jobs',{}))==SIBLINGS and
        config.get('release_eligible')is False and config.get('current_legal_pass')is False and
        all(type(config.get(k))is int and config[k]==0 for k in
            ('canonical_release_credit','question_audit_credit','new_author_review_credit','new_independent_legal_audit_credit')),
        'Held N1 source scope/provenance/zero-credit fields changed')
    closure=old.validate(root,config['closure'])
    state=json.loads(old.committed(root,q.STATE));q.validate_state(state)
    latest=census.latest_jobs(state);uid=inactive.SCOPE['unit_id'];job=latest.get(uid)
    old.require(job is not None and job.get('purpose')==inactive.PURPOSE and job['job_id']==config['review']['job_id'],
                'BLOCKED: actual latest inactive25 review is not bound')
    br=json.loads(old.committed(root,inactive.SCOPE['body_record_path'],inactive.SCOPE['body_record_sha256']))
    previous=json.loads(old.committed(root,br['archived_parent']['notes']['path'],br['archived_parent']['notes']['raw_sha256']))
    read=lambda p,s:old.committed(root,p,s)
    census.validate_registered(state,root,previous,read);body.validate_registered(state,root,previous,read)
    inactive.validate_registered(state,root,previous,read)
    report=validate_job(root,state,job);row=next(r for r in report['records']if r['unit_id']==uid)
    expected_review=dict(job_id=job['job_id'],actor_provenance=job['actor_provenance'],auditor_instance=job['auditor_instance'],
        report=job['result']['evidence'],result={'path':job['result']['result_path'],'raw_sha256':job['result_sha256']})
    old.require(config['review']==expected_review and row['completeness']=='COMPLETE'and not row['omissions']and
        len(row['claims'])==25 and job['unit_bindings'][uid]['body_sha256']==inactive.SCOPE['body_sha256']and
        job['unit_bindings'][uid]['census_sha256']==inactive.SCOPE['new_census_sha256'],
        'BLOCKED: fresh whole25 COMPLETE at exact inactive N1/census binding is required')
    hold=next(c for c in row['claims']if c['claim_id']=='NOTE-WAVE8-W3-A-3-011')
    old.require(hold['legal_status']=='LEGAL_HOLD'and
        hold['inherited_legal_blockers']==job['carried_legal_blockers'][uid][hold['claim_id']]and
        row['legal_status']=='LEGAL_HOLD','Unchanged011 HOLD cannot become a legal PASS during activation')
    for sibling,jid in config['required_sibling_jobs'].items():
        node=latest.get(sibling)
        old.require(node is not None and node['job_id']==jid and node.get('reassessment_id'),
                    'Actual latest G3 native census reassessment must be explicitly bound')
        validate_job(root,state,node)  # Keep actual COMPLETE/OMIS/HOLD/SB, never force positive.
    revision=br['replacement']['revision']
    candidate=json.loads(old.committed(root,revision['path'],revision['raw_sha256']))['units'][0]
    old.require(q.raw_sha(candidate['body'].encode())==inactive.SCOPE['body_sha256'],'Exact N1 source body changed')
    return config,closure,state,job,previous,candidate,binding


@old.snapshotted
def propose_builder_source(root,closure_binding):
    old.validate(root,closure_binding)
    state=json.loads(old.committed(root,q.STATE));q.validate_state(state);latest=census.latest_jobs(state)
    job=latest.get(inactive.SCOPE['unit_id'])
    old.require(job is not None and job.get('purpose')==inactive.PURPOSE and job['status']=='INTEGRATED',
                'BLOCKED: actual fresh25 integrated source is unavailable')
    old.require(SIBLINGS<=set(latest),'BLOCKED: actual G3 native source history is unavailable')
    result=job['result']
    config=dict(schema_version=1,purpose='N1_HELD_BUILDER_SOURCE_NOT_PUBLICATION_APPROVAL',edition=EDITION,
        unit_id=inactive.SCOPE['unit_id'],closure=closure_binding,review=dict(job_id=job['job_id'],
            actor_provenance=job['actor_provenance'],auditor_instance=job['auditor_instance'],report=result['evidence'],
            result={'path':result['result_path'],'raw_sha256':job['result_sha256']}),
        required_sibling_jobs={uid:latest[uid]['job_id']for uid in sorted(SIBLINGS)},
        release_eligible=False,current_legal_pass=False,canonical_release_credit=0,question_audit_credit=0,
        new_author_review_credit=0,new_independent_legal_audit_credit=0)
    validate_source_payload(root,config)
    return config  # Read-only output; no approval table or activation file is written.


def apply_if_bound(root,previous):
    if not old.path(root,SOURCE).exists():return previous
    config,closure,state,job,archived,candidate,binding=source_contract(root)
    old.require(previous==archived and inactive.semantic_sha(previous)==inactive.SCOPE['active_semantic_sha256'],
                'Held activation may replace only exact M, not an unrelated or already changed revision')
    result=copy.deepcopy(previous)
    for chapter in result['chapters']:
        chapter['units']=[copy.deepcopy(candidate)if u['id']==candidate['id']else u for u in chapter['units']]
    result['edition']=EDITION
    result['revision_provenance']=dict(id=EDITION,path=SOURCE,sha256=binding['raw_sha256'],
        base_guide_sha256=previous['revision_provenance']['base_guide_sha256'],
        review_status='HELD_COMPLETE_CENSUS_NOT_LEGAL_PASS',
        history_policy='IMMUTABLE_M_BODY_CENSUS_AND_NEGATIVES_RETAINED',
        parent_revision_provenance=previous['revision_provenance'])
    return result


def checkpoint_prefix(root,closure,relative):
    before=json.loads(old.old_bytes(root,closure,relative));after=json.loads(old.committed(root,relative))
    old.require(after['jobs'][:len(before['jobs'])]==before['jobs']and after['events'][:len(before['events'])]==before['events'],
                'Published native history cannot be rewritten by sixteen')


@old.snapshotted
def expected_migration(root,closure_binding):
    config,source_closure,state,job,previous,candidate,source_binding=source_contract(root)
    closure=old.validate(root,closure_binding,coverage=True)
    old.require((closure['published_commit'],closure['published_tree'],closure['fifteenth_raw_sha256'])==
        (source_closure['published_commit'],source_closure['published_tree'],source_closure['fifteenth_raw_sha256']),
        'Expanded preimage closure must preserve the exact same published15 identity')
    for relative in [q.STATE,'reports/full-corpus-review/independent-legacy-work-queue.json']:
        checkpoint_prefix(root,closure,relative)
    from notes_revision import load_notes
    from notes_independent_metadata import load_metadata
    notes=load_notes(root);expected=apply_if_bound(root,previous)
    old.require(notes==expected,'Only the exact single-unit held N1 substitution is allowed')
    bindings={SOURCE:source_binding['raw_sha256'],closure_binding['path']:closure_binding['raw_sha256']}
    ledger=old.committed(root,q.LEDGER);bindings[q.LEDGER]=old.sha(ledger)
    inv=q.inventory(root,notes,ledger_raw=ledger);metadata=load_metadata(root,notes,ledger_raw=ledger,source_bindings=bindings)
    target=metadata['units'][candidate['id']]
    old.require(target.get('current_review_valid')is True and target['completeness']=='COMPLETE'and
        target['legal_status']=='LEGAL_HOLD'and target['requires_review']is True and target.get('notice')and
        inv['units'][candidate['id']]==job['unit_bindings'][candidate['id']],
        'Actual latest N1/25 selected binding must retain public HOLD and review warning')
    evolution=inactive.sibling_evolution(job,inv,state)
    from notes_after190_annotation import bind_native_author,bind_current_review_context
    author=bind_native_author(root,bindings)  # Original2346/native3/archive and actual default safety.
    bind_current_review_context(root,bindings)  # Current counters, never historical aliases.
    # Capture the whole actual current prefix, including pending zero-credit
    # definitions. A later Q41/other append cannot reuse an older16 manifest.
    legacy_path='reports/full-corpus-review/independent-legacy-work-queue.json'
    legacy_raw=old.committed(root,legacy_path);bindings[legacy_path]=old.sha(legacy_raw)
    from legacy_independent_metadata import integrated_sources
    legacy_sources={};integrated_sources(root,source_bindings=legacy_sources)
    for receipt in legacy_sources.values():
        old.committed(root,receipt['source_path'],receipt['source_sha256'])
        bindings[receipt['source_path']]=receipt['source_sha256']
    from build_ultimate_notes import make_outputs
    outputs=make_outputs(root=root);md=outputs[Path(root)/old.EXPORT].encode();build=outputs[Path(root)/old.BUILD].encode()
    old.require(old.committed(root,old.EXPORT)==md and old.committed(root,old.BUILD)==build,
                'Current held exports must be regenerated from actual current sources')
    before=body.units(previous);after=body.units(notes)
    old.require(set(before)==set(after)and len(before)==306 and
        [uid for uid in before if before[uid]!=after[uid]]==[candidate['id']],
        'Sixteen may not change any of the other305 unit records')
    return dict(schema_version=1,purpose='SIXTEENTH_EXACT_HELD_N1_NOT_LEGAL_PASS',
        publication_approval='NOT_GRANTED_BY_ENGINEERING',closure=closure_binding,source=source_binding,
        parent_fifteenth={'path':old.FIFTEENTH,'raw_sha256':closure['fifteenth_raw_sha256']},
        old_markdown_sha256=closure['full_source_files'][old.EXPORT]['raw_sha256'],
        new_markdown_sha256=old.sha(md),new_build_sha256=old.sha(build),edition=EDITION,
        old_semantic_sha256=inactive.SCOPE['active_semantic_sha256'],new_semantic_sha256=inactive.semantic_sha(notes),
        body_delta={'unit_id':candidate['id'],'old_body_sha256':q.raw_sha(before[candidate['id']]['body'].encode()),
            'new_body_sha256':inactive.SCOPE['body_sha256'],'other305_unchanged':True},
        current_note_progress=metadata['progress'],selected_author_claim_count=sum(len(b['claim_record_sha256s'])for b in inv['units'].values()),
        current_sibling_evolution=evolution,native_author_checkpoint=author,source_bindings=dict(sorted(bindings.items())),
        current_legacy_checkpoint=[dict(job_id=j['job_id'],sequence=j['sequence'],status=j['status'],
            question_hashes_sha256=q.digest(j['question_hashes']),annotation_question_audit_credit=0)
            for j in json.loads(legacy_raw)['jobs']],
        public_unit_legal_status='LEGAL_HOLD',daily_eligible=False,canonical_audit=False,
        canonical_release_credit=0,question_audit_credit=0,new_author_review_credit=0,new_independent_legal_audit_credit=0)


def decode(root,relative,current):
    old.require(relative==old.EXPORT,'Sixteen cannot expand the protected export scope')
    raw=old.committed(root,MANIFEST);key=(MANIFEST,old.sha(raw));approval=APPROVED_MIGRATIONS.get(key)
    old.require(approval is not None,'BLOCKED: final actual16 source/output manifest has not been explicitly bound')
    metadata=json.loads(raw);old.require(metadata['closure']==approval['closure'],'Sixteenth closure approval changed')
    old.require(metadata.get('canonical_audit')is False and metadata.get('daily_eligible')is False and
        metadata.get('public_unit_legal_status')=='LEGAL_HOLD'and metadata.get('body_delta',{}).get('other305_unchanged')is True and
        all(type(v)is int and v==0 for k,v in metadata.items()if k.endswith('credit')),
        'Sixteen cannot claim legal/release credit or remove held-unit boundaries')
    expected=expected_migration(root,metadata['closure'])
    old.require(metadata==expected and old.sha(current)==expected['new_markdown_sha256'],
                'Sixteenth source/counter/HOLD/export binding changed')
    # The old fifteen layers and original1781 are run only in the actual frozen
    # publication HEAD. Returning here prevents live-N1 reads by old14/15 code.
    verified=old.verify_old_guards(root,metadata['closure'])
    return verified['original_markdown']


def readiness(root):
    blockers=[]
    if not old.APPROVED_CLOSURES:blockers.append('ACTUAL_PUBLISHED15_MAIN_TESTED_TREE_CI_PAGES_ASSET_CLOSURE_NOT_BOUND')
    if not APPROVED_ACTIVATION_SOURCES:blockers.append('ACTUAL_FRESH_B_COMPLETE25_WITH_011_HOLD_NOT_BOUND')
    if not APPROVED_MIGRATIONS:blockers.append('ACTUAL_CURRENT_N1_DERIVED_COUNTER_MANIFEST_NOT_BOUND')
    return dict(status='BLOCKED'if blockers else'EXPLICIT_CHECK_REQUIRED',blockers=blockers,
        active_body_written=False,registration_performed=False,canonical_release_credit=0,question_audit_credit=0)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true')
    parser.add_argument('--propose-source',action='store_true');parser.add_argument('--propose-migration',action='store_true')
    parser.add_argument('--closure');args=parser.parse_args()
    if args.propose_source or args.propose_migration:
        old.require(args.closure,'Actual committed approved closure path is required')
        binding={'path':args.closure,'raw_sha256':old.sha(old.committed(ROOT,args.closure))}
        result=propose_builder_source(ROOT,binding)if args.propose_source else expected_migration(ROOT,binding)
        print(json.dumps(result,ensure_ascii=False,indent=2));return
    state=readiness(ROOT)
    if state['blockers']:
        print(json.dumps(state,ensure_ascii=False));raise SystemExit(1)
    old.require(args.check,'Use explicit --check; this source-only module has no approval/activation writer')
    decode(ROOT,old.EXPORT,old.path(ROOT,old.EXPORT).read_bytes())
    print('Verified exact held-N1/source/current counters and frozen published15; no legal PASS created.')


if __name__=='__main__':main()
