"""Bounded realism-only native controller; old review_queue engine is unchanged."""
from __future__ import annotations
import argparse
import copy
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from collections import Counter

import review_queue as q
from realism_completion_scope import IDS, PENDING_VERDICTS
from procedural_secondary_metadata import principals
from notes_published15_closure import committed, snapshotted

PREFIX='reports/full-corpus-review/realism-completion-v1/'
STATE=PREFIX+'work-queue.json'
SCOPE=PREFIX+'controller-scope.json'
INPUTS=PREFIX+'nearest-visible-input.json'
STYLE='data/exam_style/mpje_style_profile.json'
STATIC_PRIMARY_PATHS=tuple('reports/full-corpus-review/'+name for name in ('pub05-14-independent-review.json','wave2-independent-review.json','wave5-independent-review.json'))
PURPOSE='FIXED146_REALISM_COMPLETION_FIXED4_LEGAL_RETRY_NO_DEFAULT_OR_RELEASE_OVERRIDE'
ACTORS=tuple('/root/realism95_'+letter for letter in 'abcd')
INSTANCES=tuple('GPT:'+actor+':20261104' for actor in ACTORS)
CRITERIA=('jurisprudence_reasoning','practice_plausibility','authentic_distractors',
 'wording_not_guessable','reasoning_not_trivia','natural_rule_combination',
 'appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying')
APPROVED_ORIGIN={'path':'reports/full-corpus-review/final26-evidence/sources/nabpformat.meta.json','raw_sha256':'636934be58e2fd6567b355d40a76d7748d51b005674aa7903da480ceb847a665'}
FORMAT_URL='https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/'
BINDING_KEYS=('job_id','sequence','question_hashes','stage','worker','worker_branch','attempt')


def require(test,message):
    if not test:raise ValueError(message)


def sha(raw):return hashlib.sha256(raw).hexdigest()
def encoded(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()
def moment(value):
    require(isinstance(value,str),'Aware timestamp required')
    dt=datetime.fromisoformat(value.replace('Z','+00:00'));require(dt.tzinfo is not None,'Aware timestamp required');return dt


def safe(relative):
    p=Path(relative)
    require(not p.is_absolute()and '..'not in p.parts and p.as_posix()==relative,'Unsafe repository path')
    return relative


def disk_read(root,relative,expected=None):
    safe(relative);p=root/relative
    require(not p.is_symlink()and root.resolve()in p.resolve().parents,'Unsafe evidence symlink')
    raw=committed(root,relative)
    require(expected is None or sha(raw)==expected,'Committed raw SHA changed: '+relative)
    return raw


def read_json(read,path,expected=None):return json.loads(read(path,expected))
def nonempty(value):return isinstance(value,str)and bool(value.strip())


def no_credit(value):
    require(value.get('canonical_audit')is False,'Noncanonical realism only')
    for key in ('canonical_release_credit','key_assessment_credit','legal_audit_credit','new_original_read_credit'):
        require(type(value.get(key))is int and value[key]==0,'Forbidden new credit: '+key)
    require(value.get('release_eligible')is False,'Supplement cannot release')


def questions(root,read):
    config=read_json(read,'site/practice-expansion/publication.json')
    paths=['practice_expansion/2026-10-23/candidates/questions.json']+[a['path']for a in config['additional_banks']]
    require(len(paths)==len(set(paths)),'Repeated public bank')
    public={};collections={}
    for path in paths:
        for row in read_json(read,path)['questions']:
            uid=row['question_id'];require(uid not in public,'Repeated public ID');public[uid]=row;collections[uid]=path
    canonical={}
    # Only file paths are discovered from disk; every payload must match HEAD.
    for path in sorted((root/'data/questions').glob('*.json')):
        row=read_json(read,path.relative_to(root).as_posix());uid=row['question_id']
        require(uid not in canonical,'Repeated canonical ID');canonical[uid]=row
    require(len(public)==2349 and len(canonical)==439,'Exact current public2349/canonical439 comparison inventory required')
    return public,collections,canonical


def visible(row,full=False):
    require(all(set(c)=={'id','text'}for c in row['choices']),'Unknown visible choice structure')
    keys=('question_id','question_type','stem','choices','correct_choice_ids','explanation')if full else ('question_id','stem','choices')
    if full:
        from export_legacy_review_input import EXPLANATION_FIELDS
        require(not set(row['explanation'])-EXPLANATION_FIELDS,'Unknown visible explanation structure')
    return {key:copy.deepcopy(row[key])for key in keys}


def nearest_inputs(public,canonical):
    def vector(row):return Counter(re.findall(r'[a-z0-9]+',row['stem'].lower()))
    def indexed(pool):
        return [(uid,vector(r),visible(r))for uid,r in sorted(pool.items())]
    pools={'canonical':indexed(canonical),'public':indexed(public)}
    pools_sha={k:q.digest([v for _,_,v in pool])for k,pool in pools.items()}
    out={}
    for uid in IDS:
        target=vector(public[uid]);tn=math.sqrt(sum(v*v for v in target.values()))or 1
        out[uid]={}
        for name,pool in pools.items():
            ranked=[]
            for other,vec,view in pool:
                if name=='public'and uid==other:continue
                vn=math.sqrt(sum(v*v for v in vec.values()))or 1
                score=sum(v*vec.get(k,0)for k,v in target.items())/(tn*vn)
                ranked.append((score,other,view))
            ranked.sort(key=lambda item:(-item[0],item[1]))
            out[uid][name]=[dict(question_id=other,visible_sha256=q.digest(view),score=round(score,10),visible=view)for score,other,view in ranked[:3]]
    return dict(schema_version=1,purpose='VISIBLE_NEAREST_LOCATOR_NOT_SEMANTIC_VERDICT',
        canonical_count=len(canonical),public_count=len(public),pool_visible_sha256=pools_sha,records=out)


def parent_binding(uid,row,path,report,raw,question):
    realism=row['realism_review'];verdict=realism.get('verdict')
    require(verdict!='FAIL','Prior realism FAIL cannot be overridden')
    require(uid not in PENDING_VERDICTS or verdict==PENDING_VERDICTS[uid],'Exact142 original realism grade changed')
    incomplete=(set(realism.get('criteria')or{})!=set(CRITERIA)or
                any(v is None for v in (realism.get('criteria')or{}).values()))
    require(verdict in {'NOT_ASSESSED','EDITORIAL_REVIEW_REQUIRED','HOLD'}or(verdict=='PASS'and incomplete),
            'Only the exact146 incomplete public-style reviews are eligible')
    require(row['record_sha256']==q.digest(question),'Stale parent/current question')
    authors=principals(question)|principals(report)
    for declared in (question.get('remediation_candidate',{}).get('known_author_editor_actor_ids',[]),question.get('known_author_ids',[]),report.get('known_author_ids',[])):
        require(isinstance(declared,list)and all(nonempty(actor)for actor in declared)and len(declared)==len(set(declared)),'Known author declarations must be unique actual actor strings')
        authors.update(declared)
    from realism_completion_legal4 import bind_parent
    legal=bind_parent(uid,row)
    actor=report.get('actor_provenance',{})
    authors|={actor.get('actor_id'),actor.get('session_id'),report.get('auditor_instance'),'/root'}
    authors.discard(None)
    return dict(report_path=path,report_raw_sha256=sha(raw),row_sha256=q.digest(row),
        old_realism_verdict=verdict,known_author_and_prior_actor_ids=sorted(authors),legal_retry_parent=legal)


def prior_supplementary(root,primary,public,collections):
    # Only the unchanged original fixed consumers may supply prior findings.
    import procedural_secondary_metadata as old2
    import phase11_secondary_metadata as phase11
    import phase11_context38_metadata as context38
    result={}
    for consumer in (old2,phase11,context38):
        source=consumer.load_metadata(root,primary,public,collections)
        for uid,proof in source['assessments'].items():
            if uid not in IDS:continue
            require(uid in old2.IDS,'Unexpected overlap with existing supplementary scope')
            raw=disk_read(root,proof['report_path'],proof['report_sha256']);report=json.loads(raw)
            result.setdefault(uid,[]).append(dict(report_path=proof['report_path'],report_sha256=proof['report_sha256'],
                row_sha256=q.digest(proof['record']),realism_verdict=proof['record']['realism_review']['verdict'],
                actor_provenance=report['actor_provenance'],auditor_instance=report['auditor_instance']))
    return result


def excluded_actors(scope,ids):
    found={a for uid in ids for a in scope['primary'][uid]['known_author_and_prior_actor_ids']}
    for uid in ids:
        for proof in scope['prior_supplementary'].get(uid,[]):
            found.update(principals(proof));found.add(proof['auditor_instance'])
    return found


@snapshotted
def build_scope(root):
    read=lambda path,expected=None:disk_read(root,path,expected)
    public,collections,canonical=questions(root,read)
    from legacy_independent_metadata import integrated_sources
    bindings={};reports=integrated_sources(root,source_bindings=bindings)
    for name in ('pub05-14-independent-review.json','wave2-independent-review.json','wave5-independent-review.json'):
        path='reports/full-corpus-review/'+name;raw=read(path);report=json.loads(raw);reports.append(report)
        for row in report['records']:bindings[row['question_id']]={'source_path':path,'source_sha256':sha(raw)}
    found={}
    for report in reports:
        for row in report['records']:
            uid=row['question_id']
            if uid in IDS:
                require(uid not in found,'Duplicate primary realism row')
                path=bindings[uid]['source_path'];raw=read(path,bindings[uid]['source_sha256'])
                found[uid]=parent_binding(uid,row,path,report,raw,public[uid])
    require(set(found)==set(IDS),'Exact146 original integrated primary bindings required')
    selection=read_json(read,'practice_expansion/2026-10-28-representative/selection.json')
    require(not set(IDS)&set(selection['recommended_ids']),'All146 must remain outside default practice')
    read(APPROVED_ORIGIN['path'],APPROVED_ORIGIN['raw_sha256'])
    style=read(STYLE);profile=json.loads(style)
    inputs=nearest_inputs(public,canonical)
    scope=dict(schema_version=1,purpose=PURPOSE,controller_actor='/root',question_ids=list(IDS),
        question_hashes={uid:q.digest(public[uid])for uid in IDS},collections={uid:collections[uid]for uid in IDS},
        static_primary_sources={p:sha(read(p))for p in STATIC_PRIMARY_PATHS},format_cache_origin=copy.deepcopy(APPROVED_ORIGIN),primary=found,prior_supplementary=prior_supplementary(root,[row for report in reports for row in report['records']],public,collections),style_profile=dict(path=STYLE,raw_sha256=sha(style),profile_id=profile['profile_id'],
            content_version=profile['content_version'],content_hash=profile['content_hash']),
        nearest_inputs=dict(path=INPUTS,raw_sha256=sha(encoded(inputs))),
        reviewers=[dict(actor_id=a,session_id=a,auditor_instance=i,fork_turns='none',
            controller_independence_basis='Root must actually spawn a fresh session before claim; queued allocation is not a claim or identity proof.')for a,i in zip(ACTORS,INSTANCES)],
        canonical_release_credit=0,key_assessment_credit=0,legal_audit_credit=0,new_original_read_credit=0)
    for reviewer in scope['reviewers']:
        require(not {reviewer['actor_id'],reviewer['session_id'],reviewer['auditor_instance']} &
                excluded_actors(scope,IDS),'Known author/prior actor cannot review')
    return scope,inputs


def validate_scope(scope,primary,public,read,expected_prior):
    require(scope.get('purpose')==PURPOSE and scope.get('controller_actor')=='/root'and
            scope.get('question_ids')==list(IDS)and set(scope['primary'])==set(IDS),'Fixed146 controller scope changed')
    require(scope['question_hashes']=={uid:q.digest(public[uid])for uid in IDS},'Current146 question hashes changed')
    require(set(scope.get('static_primary_sources',{}))==set(STATIC_PRIMARY_PATHS),'Exact original static3 source scope required')
    for path,expected in scope['static_primary_sources'].items():read(path,expected)
    require(scope.get('format_cache_origin')==APPROVED_ORIGIN,'Approved official format cache origin changed')
    read(APPROVED_ORIGIN['path'],APPROVED_ORIGIN['raw_sha256'])
    profile=read_json(read,STYLE,scope['style_profile']['raw_sha256'])
    require(scope['style_profile']==dict(path=STYLE,raw_sha256=sha(read(STYLE)),profile_id=profile['profile_id'],
        content_version=profile['content_version'],content_hash=profile['content_hash']),'Current style profile changed')
    require(scope['reviewers']==[dict(actor_id=a,session_id=a,auditor_instance=i,fork_turns='none',
        controller_independence_basis='Root must actually spawn a fresh session before claim; queued allocation is not a claim or identity proof.')for a,i in zip(ACTORS,INSTANCES)],'Actual reviewer/session scope changed')
    require(set(IDS)<=set(primary),'Complete static3/native primary inventory required')
    for uid,binding in scope['primary'].items():
        raw=read(binding['report_path'],binding['report_raw_sha256']);report=json.loads(raw)
        rows=[r for r in report['records']if r['question_id']==uid]
        require(len(rows)==1 and primary[uid]==rows[0],'Original primary row changed or missing')
        require(binding==parent_binding(uid,rows[0],binding['report_path'],report,raw,public[uid]),'Original primary verdict/hash/author binding changed')
    require(scope.get('prior_supplementary')==expected_prior,'Existing supplementary PASS/negative history changed')
    for field in ('canonical_release_credit','key_assessment_credit','legal_audit_credit','new_original_read_credit'):
        require(type(scope.get(field))is int and scope[field]==0,'Forbidden controller review credit')


def validate_state(state,scope):
    q.state_stage(state,'independent-legacy')
    require(state.get('realism_completion_scope')==dict(path=SCOPE,raw_sha256=sha(encoded(scope)),purpose=PURPOSE), 'State/controller raw scope binding changed')
    require(len(state['jobs'])==4,'Exactly four realism jobs required')
    for index,job in enumerate(state['jobs']):
        ids=IDS[index*40:(index+1)*40]
        require(job['sequence']==index+1 and job['job_id']=='review-realism-completion-'+str(index+1)and
            job['question_hashes']=={uid:scope['question_hashes'][uid]for uid in ids}and
            job['stage']=='independent-legacy'and job['purpose']==PURPOSE and
            job['required_realism_actor']==ACTORS[index]and job['required_realism_instance']==INSTANCES[index]and
            job['output_prefix']==PREFIX+'abcd'[index]+'/'and job['status']in {'QUEUED','LEASED','SUBMITTED','INTEGRATED'},'Exact40/40/40/26 assignment changed')
        excluded=excluded_actors(scope,ids)
        require(set(job['excluded_worker_actor_ids'])==excluded,'Known author exclusions changed')
        if job['status']!='QUEUED':
            require(job.get('worker')==ACTORS[index]and job.get('actor_provenance')=={'actor_id':ACTORS[index],'session_id':ACTORS[index]}and
                job.get('auditor_instance')==INSTANCES[index]and job.get('fresh_session_actually_created')is True,
                'Actual fresh actor/session/instance required')
            require(not {job['worker'],job['auditor_instance']} & excluded,'Known author/prior actor excluded')
            require(any(e.get('kind')=='CLAIM'and e.get('job_id')==job['job_id']and e.get('worker')==job['worker']and e.get('attempt')==job['attempt']for e in state['events']), 'Missing actual native claim event')


def root_only(actor):require(actor=='/root','Controller action requires /root')

def plan(root,state=None,actor='/root',at=None):
    root_only(actor);scope,inputs=build_scope(root)
    if state is not None:
        validate_state(state,scope);return state,scope,inputs
    state=q.empty('independent-legacy');state['realism_completion_scope']=dict(path=SCOPE,raw_sha256=sha(encoded(scope)),purpose=PURPOSE)
    for i in range(4):
        ids=IDS[i*40:(i+1)*40]
        state['jobs'].append(dict(job_id='review-realism-completion-'+str(i+1),sequence=i+1,stage='independent-legacy',purpose=PURPOSE,
            question_hashes={uid:scope['question_hashes'][uid]for uid in ids},status='QUEUED',attempt=0,
            required_realism_actor=ACTORS[i],required_realism_instance=INSTANCES[i],output_prefix=PREFIX+'abcd'[i]+'/',
            excluded_worker_actor_ids=sorted(excluded_actors(scope,ids))))
    q.event(state,'PLAN',at or q.timestamp(),scope_raw_sha256=sha(encoded(scope)),question_count=146)
    validate_state(state,scope);return state,scope,inputs


def assignment(state,job,scope):
    # Never export the controller scope contents, old report paths or verdicts.
    allowed=(*BINDING_KEYS,'lease_token','lease_until','output_prefix','actor_provenance','auditor_instance','base_commit')
    result={k:copy.deepcopy(job[k])for k in allowed}
    result.update(scope_binding=copy.deepcopy(state['realism_completion_scope']),style_profile=copy.deepcopy(scope['style_profile']),
        purpose=PURPOSE,controller_scope_is_blinded=True)
    from realism_completion_legal4 import LEGAL_IDS
    result['legal_retry_question_hashes']={uid:h for uid,h in job['question_hashes'].items()if uid in LEGAL_IDS}
    return result


def claim(root,state,scope,actor,session_id,auditor_instance,*,fresh_session_actually_created=False,controller_actor='/root',minutes=240,at=None):
    root_only(controller_actor);validate_state(state,scope)
    original=state;state=copy.deepcopy(state);q.recover(state,at=at)
    require(fresh_session_actually_created is True,'Actually spawn fresh session before claim')
    require(actor==session_id and actor in ACTORS and auditor_instance==INSTANCES[ACTORS.index(actor)],'Reserved actual reviewer/session required')
    i=ACTORS.index(actor);wanted=state['jobs'][i]
    require(actor not in wanted['excluded_worker_actor_ids'],'Known author excluded')
    # Delegate lease/token/expiry/reconnect to the unchanged native engine.
    pending=next((j for j in state['jobs']if j['status']=='QUEUED'),None)
    active=next((j for j in state['jobs']if j['status']=='LEASED'and j['worker']==actor),None)
    require(active is not None or pending is wanted,'Claim in assignment order')
    previous_attempt=wanted['attempt'];job=q.claim(state,actor,minutes=minutes,at=at)
    require(job is wanted,'Wrong native job selected')
    job.update(actor_provenance={'actor_id':actor,'session_id':session_id},auditor_instance=auditor_instance,
        fresh_session_actually_created=True,base_commit=job.get('base_commit')if job['attempt']==previous_attempt else q.git(root,'rev-parse','HEAD'),
        claim_started_at=job.get('claim_started_at')if job['attempt']==previous_attempt else next(e['at']for e in reversed(state['events'])if e['kind']=='CLAIM'and e['job_id']==job['job_id']))
    validate_state(state,scope);exported=assignment(state,job,scope);original.clear();original.update(state);return exported


WORKER_PUBLIC_FILES=('.gitignore','docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md',
 'docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md',
 'docs/REALISM_COMPLETION_WORKER_CONTRACT.md','data/exam_style/mpje_style_profile.json')


def prepare_worker(root,state,job_id,token,destination,at=None):
    job=q.get_job(state,job_id);q.require_lease(job,token,at or q.timestamp())
    destination=destination.resolve()
    if destination.exists():
        require(q.git(destination,'branch','--show-current')==job['worker_branch'],'Destination belongs to another worker')
        return destination
    q.git(root,'worktree','add','--no-checkout','-b',job['worker_branch'],str(destination),job['base_commit'])
    q.git(destination,'reset','--mixed','HEAD')
    patterns=['/'+path for path in WORKER_PUBLIC_FILES]+['/'+job['output_prefix']]
    q.git(destination,'sparse-checkout','set','--no-cone',*patterns)
    q.git(destination,'checkout','HEAD','--',*WORKER_PUBLIC_FILES)
    require(not q.git(destination,'status','--porcelain'),'Prepared worker view must be clean')
    return destination


def export_packet(root,assigned,scope,inputs):
    from export_legacy_review_input import export
    packet=export(assigned,root)
    require(sha(encoded(scope))==assigned['scope_binding']['raw_sha256'],'Blinded assignment scope SHA changed')
    require(sha(encoded(inputs))==scope['nearest_inputs']['raw_sha256'],'Nearest packet changed')
    packet.update(style_profile=scope['style_profile'],comparison_counts={'canonical':439,'public':2349},
        comparison_pool_sha256=inputs['pool_visible_sha256'],
        nearest_visible={uid:inputs['records'][uid]for uid in assigned['question_hashes']},
        public_format_cache_origin=dict(binding=copy.deepcopy(APPROVED_ORIGIN),original_metadata=json.loads(disk_read(root,APPROVED_ORIGIN['path'],APPROVED_ORIGIN['raw_sha256']))))
    return packet


def validate_report(job,scope,report,read,inputs,public):
    no_credit(report)
    require(report.get('purpose')==PURPOSE and report.get('scope_raw_sha256')==sha(encoded(scope))and
        report.get('stage')=='independent-legacy'and report.get('question_hashes')==job['question_hashes']and
        report.get('style_profile')==scope['style_profile']and
        report.get('native_assignment_binding')=={k:job[k]for k in BINDING_KEYS},'Report assignment/style/scope binding changed')
    require(report.get('independent_of_authors')is True and report.get('actor_provenance')==job['actor_provenance']and
        report.get('auditor_instance')==job['auditor_instance']and report.get('auditor')=='GPT','Report actual reviewer changed')
    require(report.get('prior_conclusions_read')is False and report.get('hidden_truth_read')is False and
        report.get('fresh_session_fork_turns')=='none','Prior conclusion exposure cannot gain fresh realism credit')
    completed=moment(report['completed_at']);require(completed.date().isoformat()==report['reviewed_at'],'Review date mismatch')
    require(moment(job['claim_started_at'])<=completed<=moment(job['lease_until']),'Fresh review must follow its actual current claim and lease')
    source=report['public_format_evidence'];allowed=job['output_prefix']
    paths=[source['memo_path'],source['metadata_path']]
    require(all(p.startswith(allowed)for p in paths),'Format evidence outside own worker prefix')
    memo=read_json(read,paths[0],source['memo_sha256']);meta=read_json(read,paths[1],source['metadata_sha256'])
    require(nonempty(memo.get('own_abstract_memo_ko'))and memo.get('source_is_format_only')is True and
        memo.get('protected_material_not_used')is True and moment(job['claim_started_at'])<=moment(memo['reviewed_at'])<=completed,'Retained own format memo required')
    require(meta.get('official_url')==meta.get('final_url')==FORMAT_URL and
        'raw_path'in meta and meta['raw_path']is None and 'text_path'in meta and meta['text_path']is None and
        meta.get('retention')=='PRIVATE_NOT_REDISTRIBUTED','Public raw/text redistribution prohibited; own memo only')
    for key in ('raw_sha256','text_sha256'):require(re.fullmatch('[0-9a-f]{64}',meta.get(key,'')),'Format retrieval SHA required')
    fetched=moment(meta['retrieved_at']);read_at=moment(meta['read_at']);claim_at=moment(job['claim_started_at'])
    mode=meta.get('retrieval_mode','LIVE')
    require(mode in {'LIVE','SAME_DAY_RETAINED_CACHE'},'Unknown format retrieval mode')
    require(fetched<=read_at<=completed and fetched.date()==read_at.date()==completed.date()and claim_at<=read_at,
            'Actual format retrieval/read/review timestamps required')
    if mode=='LIVE':
        require(claim_at<=fetched,'A live format GET must follow the actual claim')
        require('origin_metadata_path'not in source and 'origin_metadata_sha256'not in source,'Live retrieval cannot hide an origin cache')
    else:
        origin_path=source.get('origin_metadata_path')
        require(origin_path==allowed+'format-origin-meta.json','Exact own-prefix original format metadata required')
        require(scope.get('format_cache_origin')==APPROVED_ORIGIN and source.get('origin_metadata_sha256')==APPROVED_ORIGIN['raw_sha256'],
                'Retained cache must copy the exact controller-approved original metadata bytes')
        origin=read_json(read,origin_path,APPROVED_ORIGIN['raw_sha256'])
        require(isinstance(source.get('origin_metadata_sha256'),str)and re.fullmatch('[0-9a-f]{64}',source['origin_metadata_sha256']),
                'Origin metadata must bind exact raw SHA')
        for key in ('official_url','final_url','retrieved_at','raw_sha256','text_sha256'):
            require(key in origin and origin[key]==meta[key],'Original cache metadata differs: '+key)
        require(origin.get('status')==meta.get('status')==200 and origin.get('public_raw_redistribution')is False,
                'Same-day retained cache needs genuine original official200 retrieval')
        paths.append(origin_path)

    from realism_completion_legal4 import LEGAL_IDS, validate_legal
    rows=report.get('records',[])
    require(len(rows)==len(job['question_hashes'])and{r['question_id']for r in rows}==set(job['question_hashes']),'Missing/duplicate/extra realism rows')
    for row in rows:
        uid=row['question_id'];expected_fields={'question_id','record_sha256','visible_content_sha256','read_scope','realism_review','release_eligible'}
        if uid in LEGAL_IDS:expected_fields.add('legal_review')
        require(set(row)==expected_fields,'Only fixed4 permits a mandatory separate legal retry')
        if uid in LEGAL_IDS:paths.extend(validate_legal(row,public[uid],read,allowed,completed))
        require(row['record_sha256']==job['question_hashes'][uid]and row['release_eligible']is False and
            row['visible_content_sha256']==q.digest(visible(public[uid],True)),'Current full/visible content SHA changed')
        options=[c['id']for c in public[uid]['choices']];read_scope=row['read_scope']
        require(read_scope==dict(original_stem=True,all_choices_read=options,stored_key_read=True,
            complete_core_reasoning_read=True,all_choice_explanations_read=options,learning_boundary_read=True,
            prior_question_author_or_independent_verdicts_read=False,hidden_statement_truth_read=False),'Complete original visible read required')
        realism=row['realism_review'];criteria=realism['criteria'];reasons=realism['criterion_findings_ko']
        require(set(criteria)==set(reasons)==set(CRITERIA)and all(v is None or type(v)is bool for v in criteria.values())and
            all(nonempty(v)for v in reasons.values())and len(set(reasons.values()))==len(CRITERIA),'All10 actual criteria and individual reasons required')
        verdict=realism.get('verdict');require(verdict in {'PASS','FAIL','NOT_ASSESSED','HOLD'},'Unknown realism verdict')
        require(nonempty(realism.get('finding_ko')),'Realism finding required')
        if verdict=='PASS':require(all(v is True for v in criteria.values())and meta['status']==200 and
            realism.get('decision')=='KEEP'and meta.get('document_identity_status')=='OFFICIAL_FORMAT_TARGET_DIRECTLY_READ','PASS requires all10 true and official format actually read')
        if verdict in {'NOT_ASSESSED','HOLD'}:require(nonempty(realism.get('blocker'))and realism.get('decision')=='HOLD','Incomplete style needs an explicit HOLD/blocker and actual format attempt evidence')
        if verdict=='FAIL':require(any(v is False for v in criteria.values())and realism.get('decision')in {'MINOR_EDIT','MAJOR_REWRITE','HOLD','DELETE'},'FAIL needs actual failed criterion')
        duplicate=realism['duplicate_evidence']
        require(duplicate.get('canonical_pool_count')==439 and duplicate.get('public_pool_count')==2349 and
            duplicate.get('pool_visible_sha256')==inputs['pool_visible_sha256'],'Exact439/2349 comparison required')
        for name in ('canonical','public'):
            expected=inputs['records'][uid][name];comparisons=duplicate.get(name,[])
            require(len(comparisons)==len(expected)and len({r['question_id']for r in comparisons})==len(expected),'All nearest candidates required')
            by_id={r['question_id']:r for r in comparisons}
            for neighbor in expected:
                item=by_id.get(neighbor['question_id'],{})
                require(item.get('visible_sha256')==neighbor['visible_sha256']and item.get('stem_and_all_choices_read')is True and
                    nonempty(item.get('comparison_ko')),'Nearest original stems/all choices must actually be compared')
    return paths


def worker_reader(root,commit):
    require(re.fullmatch('[0-9a-f]{40}',commit or ''),'Exact40 worker commit required')
    q.git(root,'cat-file','-e',commit+'^{commit}')
    def read(path,expected=None):
        safe(path);raw=subprocess.check_output(['git','-C',str(root),'show',commit+':'+path])
        require(expected is None or sha(raw)==expected,'Worker evidence SHA changed: '+path);return raw
    return read


def validate_submission(root,job,scope,result,inputs,public):
    q.validate_result(job,result);no_credit(result)
    require(result.get('result_path')==job['output_prefix']+'result.json','Own exact result envelope path required')
    require(result.get('actor_provenance')==job['actor_provenance']and result.get('auditor_instance')==job['auditor_instance'],'Envelope actual actor changed')
    source=worker_reader(root,result['worker_commit']);paths=set()
    require(q.git(root,'merge-base',job['base_commit'],result['worker_commit'])==job['base_commit'],'Worker must descend from actual claim base')
    require(q.git(root,'rev-parse',job['worker_branch'])==result['worker_commit'],'Worker branch/commit binding changed')
    reports={r['evidence_path']for r in result['results']};require(len(reports)==1,'One exact report per assigned batch')
    report_path=next(iter(reports));require(report_path==job['output_prefix']+'report.json','Own exact report path required')
    for row in result['results']:
        raw=source(report_path,row['evidence_sha256']);report=json.loads(raw)
        q.validate_independent_evidence({**job,'result':result},row,report)
    paths.add(report_path);paths.update(validate_report(job,scope,report,source,inputs,public))
    changed=set(q.git(root,'diff','--name-only',job['base_commit'],result['worker_commit']).splitlines())
    require(changed==paths and all(p.startswith(job['output_prefix'])for p in changed),'Worker may commit exactly own report/memo/metadata; no original/generated/queue changes')
    return source,paths


def submit(root,state,scope,job_id,token,result,inputs,public,actor='/root',at=None):
    root_only(actor);validate_state(state,scope);job=q.get_job(state,job_id)
    worker_source,_=validate_submission(root,job,scope,result,inputs,public)
    raw=(root/result['result_path']).read_bytes();require(json.loads(raw)==result,'Result envelope differs from submission')
    if job.get('result_raw_sha256'):require(job['result_raw_sha256']==sha(raw),'Conflicting result envelope raw bytes')
    require(moment(json.loads(worker_source(result['results'][0]['evidence_path']))['completed_at'])<=moment(at or q.timestamp()),'Report cannot complete after submission')
    q.submit(state,job_id,token,result,at=at);job['result_raw_sha256']=sha(raw)


def integrate(root,state,scope,job_id,inputs,public,actor='/root',at=None):
    root_only(actor);validate_state(state,scope);job=q.get_job(state,job_id)
    require(job['status']in {'SUBMITTED','INTEGRATED'},'Submit before integration')
    source,paths=validate_submission(root,job,scope,job['result'],inputs,public)
    for path in paths:require(disk_read(root,path)==source(path),'All worker raw bytes must be exactly committed at integration')
    raw=disk_read(root,job['result']['result_path'],job['result_raw_sha256']);require(json.loads(raw)==job['result'],'Committed envelope changed')
    q.integrate(state,job_id,root,at=at)


def save_once(root,path,value):
    target=root/path;raw=encoded(value);target.parent.mkdir(parents=True,exist_ok=True)
    require(not target.exists()or target.read_bytes()==raw,'Refuse overwrite of existing evidence: '+path)
    if not target.exists():target.write_bytes(raw)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--controller-actor')
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('plan')
    export_parser=sub.add_parser('export-input');export_parser.add_argument('--assignment',type=Path,required=True);export_parser.add_argument('--output',type=Path,required=True)
    worker_parser=sub.add_parser('validate-worker');worker_parser.add_argument('--job',required=True);worker_parser.add_argument('--result',type=Path,required=True)
    prepare_parser=sub.add_parser('prepare-worker');prepare_parser.add_argument('--job',required=True);prepare_parser.add_argument('--token',required=True);prepare_parser.add_argument('--destination',type=Path,required=True)
    claim_parser=sub.add_parser('claim');claim_parser.add_argument('--actor',required=True);claim_parser.add_argument('--session-id',required=True);claim_parser.add_argument('--auditor-instance',required=True);claim_parser.add_argument('--actual-fresh-session-created',action='store_true');claim_parser.add_argument('--output',type=Path,required=True)
    for command in ('submit','integrate','heartbeat','revoke'):
        child=sub.add_parser(command);child.add_argument('--job',required=True)
        if command!='integrate':child.add_argument('--token',required=True)
        if command=='submit':child.add_argument('--result',type=Path,required=True)
        if command=='revoke':child.add_argument('--reason',required=True)
    args=parser.parse_args();root=args.root.resolve()
    if args.command in {'export-input','validate-worker'}:
        read=lambda p,h=None:disk_read(root,p,h)
        state=read_json(read,STATE);scope=read_json(read,SCOPE,state['realism_completion_scope']['raw_sha256'])
        validate_state(state,scope);public,collections,canonical=questions(root,read)
        from realism_completion_metadata import original_records
        primary=original_records(root,read)
        validate_scope(scope,{row['question_id']:row for row in primary},public,read,prior_supplementary(root,primary,public,collections))
        inputs=read_json(read,INPUTS,scope['nearest_inputs']['raw_sha256'])
        require(inputs==nearest_inputs(public,canonical),'Current comparison pools changed')
        if args.command=='export-input':
            assigned=json.loads(args.assignment.read_bytes());job=q.get_job(state,assigned['job_id'])
            q.require_lease(job,assigned['lease_token'],q.timestamp())
            require(assigned==assignment(state,job,scope),'Blinded assignment differs from actual claim')
            args.output.write_bytes(encoded(export_packet(root,assigned,scope,inputs)))
            print('Exported original visible content and measured nearest visible comparisons; no verdict credit.')
        else:
            job=q.get_job(state,args.job);result=json.loads(args.result.read_bytes())
            validate_submission(root,job,scope,result,inputs,public)
            print(json.dumps({'validation':'PASS','assigned_rows':len(job['question_hashes']),'canonical_release_credit':0,'new_review_credit_from_validation':0}))
        return
    root_only(args.controller_actor)
    # Unchanged native checkpoint locking and atomic persistence.
    with q.checkpoint(root/STATE,'independent-legacy')as state:
        if args.command=='plan':
            existing=state if state['jobs']else None
            planned,scope,inputs=plan(root,existing,actor=args.controller_actor)
            save_once(root,SCOPE,scope);save_once(root,INPUTS,inputs)
            replacement=copy.deepcopy(planned);state.clear();state.update(replacement);return
        scope=read_json(lambda p,h=None:disk_read(root,p,h),SCOPE);validate_state(state,scope)
        if args.command=='claim':
            exported=claim(root,state,scope,args.actor,args.session_id,args.auditor_instance,
                fresh_session_actually_created=args.actual_fresh_session_created,controller_actor=args.controller_actor)
            args.output.write_bytes(encoded(exported));return
        if args.command=='prepare-worker':
            print(prepare_worker(root,state,args.job,args.token,args.destination));return
        if args.command=='heartbeat':q.heartbeat(state,args.job,args.token,minutes=240);return
        if args.command=='revoke':q.revoke(state,args.job,args.token,args.reason,args.controller_actor);return
        read=lambda p,h=None:disk_read(root,p,h);public,_,canonical=questions(root,read)
        inputs=read_json(read,INPUTS,scope['nearest_inputs']['raw_sha256'])
        from realism_completion_metadata import original_records
        primary=original_records(root,read)
        validate_scope(scope,{row['question_id']:row for row in primary},public,read,prior_supplementary(root,primary,public,questions(root,read)[1]))
        require(inputs==nearest_inputs(public,canonical),'Current comparison pools changed')
        if args.command=='submit':submit(root,state,scope,args.job,args.token,json.loads(args.result.read_bytes()),inputs,public,actor=args.controller_actor)
        else:integrate(root,state,scope,args.job,inputs,public,actor=args.controller_actor)


if __name__=='__main__':main()
