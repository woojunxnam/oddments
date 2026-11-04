"""Exact published15 retention and an isolated old-HEAD verification view.

Only preparation reads historical Git objects. Runtime reconstructs the exact
old tree from committed current bytes or explicitly retained old preimages.
No actual publication is asserted by shipping this source-only module.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile

REPOSITORY='woojunxnam/oddments'
API='https://api.github.com/repos/'+REPOSITORY+'/'
ORIGIN='https://woojunxnam.github.io/oddments/'
RECEIPTS='reports/full-corpus-review/notes16-publication/'
PREIMAGES='revisions/baselines/notes16-published15/'
CLOSURE_PREFIX='revisions/notes/published15-closures/'
FIFTEENTH='revisions/notes/protected-migration-after190.json'
FOURTEENTH='revisions/notes/protected-migration-independent-notes-wave3.json'
FOURTEENTH_SHA='53537abd57b56bc8a839901a766de916c7a06b4275beba8bd2ebf435adf0353e'
OLD14_ANCHOR='    fourteenth_path=root/'
OLD14_TAIL_SHA='ba8f3ae371b9cacf05e896064ebd3b6c170f151e9a877ca3b09113c6ca250300'
OLD_GUARD='scripts/verify_representative_protected.py'
OLD15_CODE='scripts/notes_after190_annotation.py'
EXPORT='site/notes/complete-notes.md'
BUILD='site/notes/build.json'
PROTECTED='reports/representative-rewrite/protected-baseline.json'
POLICIES={'docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md'}
# Root binds actual path/rawSHA/commit/tree only after actual main/CI/Pages/assets.
# There is intentionally no proposed candidate or future merge in this table.
APPROVED_CLOSURES={
    ('revisions/notes/published15-closures/pr192-resume-v1.json',
     '6a981911268dd32acd7c314e13286f7643e0a8ae99503e41ef949e476012cdfc'): {
        'published_commit': 'e8f9b9bcffdb5cf8849ee97ba75b9526bd1cff67',
        'published_tree': '0039604281827d2dec95df65a05536bd3b735897',
    },
}
_HEAD_VIEW=ContextVar('published15_head_view',default=None)
DYNAMIC_PUBLICATION_INPUTS={
    'reports/full-corpus-review/progress.json','reports/full-corpus-review/notes-unit-ledger.jsonl',
    'reports/full-corpus-review/question-ledger.jsonl','reports/full-corpus-review/independent-notes-work-queue.json',
    'reports/full-corpus-review/independent-legacy-work-queue.json',
    'reports/representative-rewrite/default-holds.json','reports/representative-rewrite/nonlegacy-default-holds.json',
    'practice_expansion/2026-10-28-representative/selection.json',
}
REPRESENTATIVE_BANK='practice_expansion/2026-10-28-representative/questions.json'
ARCHIVE_NOTICES='reports/representative-rewrite/archive-review-notices.json'


def require(ok,message):
    if not ok:raise ValueError(message)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def encoded(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()


@contextmanager
def head_snapshot(root):
    root=Path(root).resolve();active=_HEAD_VIEW.get()
    if active is not None and active['root']==root:
        yield;return
    git=lambda *args:subprocess.check_output(['git','-C',str(root),*args])
    head=git('rev-parse','HEAD').decode().strip();objects={}
    for entry in git('ls-tree','-r','-z','HEAD').split(b'\0'):
        if entry:
            meta,relative=entry.split(b'\t',1);objects[relative.decode()]=meta.split()[2].decode()
    token=_HEAD_VIEW.set(dict(root=root,head=head,objects=objects))
    try:
        yield
        require(git('rev-parse','HEAD').decode().strip()==head,'Source HEAD advanced during closure verification')
    finally:_HEAD_VIEW.reset(token)


def snapshotted(function):
    def wrapped(root,*args,**kwargs):
        with head_snapshot(root):return function(root,*args,**kwargs)
    return wrapped


def path(root,relative):
    p=PurePosixPath(relative)
    require(not p.is_absolute()and str(p)==relative and '..'not in p.parts and '\n'not in relative and '\0'not in relative,
            'Unsafe published15 closure path')
    target=Path(root)/relative
    require(Path(root).resolve()in target.resolve().parents and not target.is_symlink(),'Unsafe closure file/symlink')
    return target


def committed(root,relative,expected=None):
    p=path(root,relative);raw=p.read_bytes()
    view=_HEAD_VIEW.get()
    if view is not None and view['root']==Path(root).resolve():
        actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        exact=view['objects'].get(relative)==actual
    else:exact=subprocess.check_output(['git','-C',str(root),'show','HEAD:'+relative])==raw
    require(exact,
            'Closure input is not exact HEAD bytes: '+relative)
    require(expected is None or sha(raw)==expected,'Closure input raw SHA changed: '+relative)
    return raw


def proof(root,binding,official_url):
    require(set(binding)=={'path','raw_sha256','official_url','http_status','tls_verified','retrieved_at_utc'}and
            binding['path'].startswith(RECEIPTS)and binding['official_url']==official_url and
            type(binding['http_status'])is int and binding['http_status']==200 and binding['tls_verified']is True,
            'Actual retained official HTTPS publication payload is required')
    at=datetime.fromisoformat(binding['retrieved_at_utc'].replace('Z','+00:00'))
    require(at.tzinfo is not None,'Publication retrieval timestamp requires timezone')
    return committed(root,binding['path'],binding['raw_sha256'])


def publication(root,binding):
    require(set(binding)=={'path','raw_sha256'}and binding['path'].startswith(RECEIPTS),
            'Publication receipt must be retained separately from mutable outputs')
    receipt=json.loads(committed(root,binding['path'],binding['raw_sha256']))
    require(receipt.get('schema_version')==1 and receipt.get('status')=='ACTUAL_PUBLISHED_VERIFIED'and
            receipt.get('controller_actor')=='/root'and receipt.get('repository')==REPOSITORY and
            all(type(receipt.get(k))is int and receipt[k]==0 for k in ('canonical_release_credit','question_audit_credit')),
            'BLOCKED: actual published15 primary receipt, not a proposed candidate, is required')
    merge=receipt['published_commit'];tested=receipt['tested_commit'];tree=receipt['published_tree']
    require(all(isinstance(x,str)and len(x)==40 and set(x)<=set('0123456789abcdef')for x in [merge,tested,tree]),
            'Exact actual merge/tested/tree identities required')
    pr=json.loads(proof(root,receipt['pull'],API+'pulls/'+str(receipt['pull_number'])))
    require(pr.get('number')==receipt['pull_number']and pr.get('merged')is True and pr.get('merge_commit_sha')==merge and pr['head']['sha']==tested and
            pr['base']['ref']=='main'and pr['base']['repo']['full_name']==REPOSITORY and pr.get('merged_at'),
            'Publication pull is not the exact actually merged tested candidate')
    for key,commit in [('published_commit_payload',merge),('tested_commit_payload',tested)]:
        value=json.loads(proof(root,receipt[key],API+'commits/'+commit))
        require(value.get('sha')==commit and value['commit']['tree']['sha']==tree,
                'Published main tree differs from tested tree')
    qa_heads=set();run_ids=set()
    for item in receipt['ci_runs']:
        url=item['official_url'];require(url.startswith(API+'actions/runs/'),'Unexpected publication CI origin')
        run=json.loads(proof(root,item,url))
        require(url==API+'actions/runs/'+str(run['id'])and run['id']not in run_ids and run['repository']['full_name']==REPOSITORY and
                run['head_sha']in {merge,tested}and run['status']=='completed'and run['conclusion']=='success'and
                run['path'].startswith('.github/workflows/'),'Actual successful current-tree CI run is required')
        run_ids.add(run['id'])
        if run['path']=='.github/workflows/qa.yml':qa_heads.add(run['head_sha'])
    require({merge,tested}<=qa_heads,'Actual full-QA CI proof is required for tested candidate and merged main')
    item=receipt['pages_run'];url=item['official_url']
    require(url.startswith(API+'actions/runs/'),'Unexpected Pages proof origin')
    pages=json.loads(proof(root,item,url))
    require(url==API+'actions/runs/'+str(pages['id'])and pages['repository']['full_name']==REPOSITORY and pages['head_sha']==merge and pages['head_branch']=='main'and
            pages['path']=='.github/workflows/pages.yml'and pages['status']=='completed'and pages['conclusion']=='success',
            'Actual successful Pages run at published main is required')
    assets={}
    for entry in receipt['public_assets']:
        source=entry['source_path'];require(source.startswith('site/')and source not in assets,'Unexpected/duplicate published asset')
        expected_url=ORIGIN+source.removeprefix('site/')
        raw=proof(root,entry['payload'],expected_url)
        assets[source]=sha(raw)
    require({EXPORT,BUILD}<=set(assets),'Actual published15 Markdown/build asset payloads are required')
    return receipt,assets


@snapshotted
def prepare(root,published_commit,publication_binding):
    """Return a genuine post-publication proposal plus exact old blobs to retain.

    Caller/root chooses new immutable manifest paths and commits the returned
    payloads. This function never writes a source, approval or activation file.
    """
    root=Path(root);receipt,assets=publication(root,publication_binding)
    require(published_commit==receipt['published_commit'],'Preparation commit differs from actual publication proof')
    tree=subprocess.check_output(['git','-C',str(root),'rev-parse',published_commit+'^{tree}'],text=True).strip()
    tested_tree=subprocess.check_output(['git','-C',str(root),'rev-parse',receipt['tested_commit']+'^{tree}'],text=True).strip()
    require(tree==tested_tree==receipt['published_tree'],'Actual historical Git tree differs from published/tested primary proof')
    rows=subprocess.check_output(['git','-C',str(root),'ls-tree','-r','-z',published_commit]).split(b'\0')
    files={};retained={};writes={}
    for row in rows:
        if not row:continue
        meta,name=row.split(b'\t',1);mode,kind,oid=meta.decode().split();relative=name.decode()
        path(root,relative);require(kind=='blob'and mode in {'100644','100755'},'Unsupported old-tree file/submodule/symlink')
        raw=subprocess.check_output(['git','-C',str(root),'cat-file','blob',oid]);expected=sha(raw)
        files[relative]={'raw_sha256':expected,'git_blob_sha1':oid,'mode':mode}
        current=path(root,relative)
        if current.is_file()and sha(current.read_bytes())==expected:
            committed(root,relative,expected)
        else:
            dest=PREIMAGES+published_commit+'/'+relative
            retained[relative]={'path':dest,'raw_sha256':expected}
            if path(root,dest).exists():require(path(root,dest).read_bytes()==raw,'Cannot overwrite a retained publication preimage')
            writes[dest]=raw
    old=lambda p:subprocess.check_output(['git','-C',str(root),'show',published_commit+':'+p])
    fifteenth=json.loads(old(FIFTEENTH));baseline=json.loads(old(PROTECTED))
    guard=old(OLD_GUARD).decode()
    require(OLD14_ANCHOR in guard and sha(guard[guard.index(OLD14_ANCHOR):].encode())==OLD14_TAIL_SHA,
            'Published fourteenth decoder tail differs from the immutable original')
    require(fifteenth.get('annotation_inputs_ready')is True and fifteenth.get('purpose')=='FIFTEENTH_ANNOTATION_LAYER_NOT_SEMANTIC_OR_AUDIT_APPROVAL'and
            fifteenth.get('semantic_notes_sha256')=='e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824'and
            sha(old(FOURTEENTH))==FOURTEENTH_SHA,'Only exact actually published15 over unchanged14/M is supported')
    require(all(files[p]['raw_sha256']==digest for p,digest in fifteenth['source_bindings'].items()),
            'Published15 source-bindings do not match its actual full tree')
    require(all(files[p]['raw_sha256']==digest for p,digest in assets.items()),'Public origin assets differ from published tree')
    protected={r['path']:files[r['path']]['raw_sha256']for r in baseline['files']}
    require(len(protected)==1781,'Original1781 protected inventory is required')
    manifest=dict(schema_version=1,purpose='PUBLISHED15_READ_ONLY_HEAD_CLOSURE',status='ACTUAL_PUBLISHED_SOURCE_PROPOSAL_NOT_ACTIVATION',
        publication=publication_binding,published_commit=published_commit,tested_commit=receipt['tested_commit'],published_tree=tree,
        fifteenth_path=FIFTEENTH,fifteenth_raw_sha256=files[FIFTEENTH]['raw_sha256'],
        full_source_files=files,retained_preimages=retained,protected_current_raw_sha256=protected,
        canonical_release_credit=0,question_audit_credit=0)
    return manifest,writes


@snapshotted
def validate(root,binding,*,coverage=False):
    require(set(binding)=={'path','raw_sha256'},'Exact closure path/raw SHA binding required')
    expected=APPROVED_CLOSURES.get((binding['path'],binding['raw_sha256']))
    require(expected is not None,'BLOCKED: actual published15 closure has not been explicitly bound')
    value=json.loads(committed(root,binding['path'],binding['raw_sha256']))
    require(value.get('schema_version')==1 and value.get('purpose')=='PUBLISHED15_READ_ONLY_HEAD_CLOSURE'and
            value.get('status')=='ACTUAL_PUBLISHED_SOURCE_PROPOSAL_NOT_ACTIVATION'and
            value['published_commit']==expected['published_commit']and value['published_tree']==expected['published_tree']and
            type(value.get('canonical_release_credit'))is int and value['canonical_release_credit']==0 and
            type(value.get('question_audit_credit'))is int and value['question_audit_credit']==0,
            'Published15 closure approval/scope/credit changed')
    receipt,assets=publication(root,value['publication'])
    require((value['published_commit'],value['tested_commit'],value['published_tree'])==
            (receipt['published_commit'],receipt['tested_commit'],receipt['published_tree']),
            'Closure no longer matches actual published/tested identity')
    files=value['full_source_files'];require({FIFTEENTH,FOURTEENTH,EXPORT,BUILD,PROTECTED}<=set(files),'Incomplete old source closure')
    require(value['fifteenth_path']==FIFTEENTH and value['fifteenth_raw_sha256']==files[FIFTEENTH]['raw_sha256']and
            files[FOURTEENTH]['raw_sha256']==FOURTEENTH_SHA and len(value['protected_current_raw_sha256'])==1781,
            'Published14/15 or original1781 inventory changed')
    baseline=json.loads(old_bytes(root,value,PROTECTED))
    require(value['protected_current_raw_sha256']=={r['path']:files[r['path']]['raw_sha256']for r in baseline['files']},
            'Original protected1781 path/SHA projection changed')
    require(all(files[p]['raw_sha256']==digest for p,digest in assets.items()),'Closure differs from actual public assets')
    for relative,ref in value['retained_preimages'].items():
        require(relative in files and ref=={'path':PREIMAGES+value['published_commit']+'/'+relative,
                'raw_sha256':files[relative]['raw_sha256']},'Preimage alias expands source origin/scope')
        committed(root,ref['path'],ref['raw_sha256'])
    frozen=set(value['protected_current_raw_sha256'])-{EXPORT}
    frozen|=POLICIES|{PROTECTED,OLD15_CODE}|{p for p in files if p.startswith('revisions/baselines/')or
                    (p.startswith('revisions/notes/protected-migration')and p.endswith('.json'))}
    parent=json.loads(committed(root,FIFTEENTH,files[FIFTEENTH]['raw_sha256']))
    frozen|={p for p in parent['source_bindings']if p.startswith('reports/')and p not in DYNAMIC_PUBLICATION_INPUTS}
    config='site/practice-expansion/publication.json'
    if config in files:
        settings=json.loads(committed(root,config,files[config]['raw_sha256']))
        frozen|={config,'practice_expansion/2026-10-23/candidates/questions.json'}
        frozen|={b['path']for b in settings['additional_banks']}
    for p in frozen:
        if p==REPRESENTATIVE_BANK and sha(committed(root,p))!=files[p]['raw_sha256']:
            validate_archive_notice_wrapper(root,value)
        else:committed(root,p,files[p]['raw_sha256'])
    current_guard=committed(root,OLD_GUARD).decode()
    require(OLD14_ANCHOR in current_guard and sha(current_guard[current_guard.index(OLD14_ANCHOR):].encode())==OLD14_TAIL_SHA,
            'Live original14 decoder tail changed; historical view is not a bypass')
    if coverage:
        for p,entry in files.items():old_bytes(root,value,p)
    return value


def validate_archive_notice_wrapper(root,closure):
    """Only a native negative notice's input digest may evolve in this bank.

    Every question, answer, source and other wrapper field stays identical to
    the actually published bank. Historical bytes remain in the old-tree view.
    This is not an authoring, legal-pass or release exception.
    """
    old_bank=json.loads(old_bytes(root,closure,REPRESENTATIVE_BANK))
    current=json.loads(committed(root,REPRESENTATIVE_BANK));normalized=copy.deepcopy(current)
    old_digest=old_bank['source_authoring_hashes'][ARCHIVE_NOTICES]
    require(old_digest==closure['full_source_files'][ARCHIVE_NOTICES]['raw_sha256'],
            'Published representative wrapper lacks its exact original notice source')
    notice_raw=committed(root,ARCHIVE_NOTICES)
    require(normalized['source_authoring_hashes'][ARCHIVE_NOTICES]==sha(notice_raw),
            'Representative notice input digest is stale')
    normalized['source_authoring_hashes'][ARCHIVE_NOTICES]=old_digest
    require(normalized==old_bank,'Only the archive-notice digest may change in the published representative bank')
    old_notices=json.loads(old_bytes(root,closure,ARCHIVE_NOTICES))['notices']
    notices=json.loads(notice_raw)['notices']
    def project(notice,qid):
        value=copy.deepcopy(notice);value['question_ids']=[qid]
        value['question_record_hashes']={qid:notice['question_record_hashes'][qid]}
        return value
    def index(rows):
        result={}
        for n in rows:
            for qid in n['question_ids']:
                require(qid not in result,'Repeated archive notice ID')
                result[qid]=n
        return result
    previous=index(old_notices);latest=index(notices)
    require(set(previous)<=set(latest),'Published archive warnings cannot disappear')
    def preserved(node,qid,expected):
        if qid in node.get('question_ids',[]) and project(node,qid)==expected:return True
        return any(preserved(n,qid,expected)for n in node.get('previous_notices',[]))
    from legacy_independent_metadata import integrated_sources
    bindings={};integrated_sources(Path(root),source_bindings=bindings)
    for qid,notice in latest.items():
        original=previous.get(qid)
        if original is not None and project(notice,qid)==project(original,qid):continue
        if original is not None:
            require(any(preserved(n,qid,project(original,qid))for n in notice.get('previous_notices',[])),
                    'Changed archive warning must preserve its exact published history: '+qid)
        binding=bindings.get(qid)
        required={'question_ids','question_record_hashes','issue_type','reason','checked_at','review_source','review_source_sha256'}
        require(required<=set(notice)<=required|{'previous_notices'} and
                notice['issue_type']=='INDEPENDENT_REVIEW_FINDING' and binding is not None and
                notice['review_source']==binding['source_path'] and
                notice['review_source_sha256']==binding['source_sha256'] and
                notice['question_record_hashes'][qid]==binding['record_sha256'] and
                notice['checked_at']==str(binding['reviewed_at'])[:10],
                'Archive wrapper delta requires actual integrated current-ID independent evidence: '+qid)
    # The existing builder checks every negative finding/source hash/current
    # question binding and exact deterministic bank/selection/metrics outputs.
    verify_representative_outputs(root)


def verify_representative_outputs(root):
    result=subprocess.run([sys.executable,str(Path(root)/'scripts/build_representative_rewrites.py'),'--check'],
                          cwd=root,env=git_env(),capture_output=True,text=True)
    require(result.returncode==0,'Current archive notices or deterministic representative outputs are invalid: '+result.stdout+result.stderr)


def old_bytes(root,closure,relative):
    entry=closure['full_source_files'][relative];p=path(root,relative)
    if p.is_file()and sha(p.read_bytes())==entry['raw_sha256']:
        return committed(root,relative,entry['raw_sha256'])
    retained=closure['retained_preimages'].get(relative)
    require(retained is not None,'SOURCE_BLOCKED: changed old path has no exact retained preimage: '+relative)
    return committed(root,retained['path'],entry['raw_sha256'])


def git_env():
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM='1')
    for key in list(env):
        if key.startswith('GIT_')and key not in {'GIT_CONFIG_GLOBAL','GIT_CONFIG_NOSYSTEM'}:env.pop(key)
    env['GIT_OPTIONAL_LOCKS']='0';env['GIT_TERMINAL_PROMPT']='0'
    env.pop('PYTHONPATH',None);env.pop('GIT_DIR',None);env.pop('GIT_WORK_TREE',None)
    return env


@contextmanager
def fixed_view(root,binding):
    env=git_env()
    with head_snapshot(root),tempfile.TemporaryDirectory(prefix='mpje-published15-')as name:
        closure=validate(root,binding,coverage=True)
        view=Path(name);files=closure['full_source_files']
        for relative,entry in files.items():
            p=path(view,relative);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(old_bytes(root,closure,relative))
            p.chmod(0o755 if entry['mode']=='100755'else 0o644)
        run=lambda *args,**kw:subprocess.check_output(['git','-C',str(view),*args],env=env,**kw)
        run('init','-q');names=''.join(str(view/p)+'\n'for p in files)
        oids=run('hash-object','-w','--no-filters','--stdin-paths',input=names.encode()).decode().splitlines()
        require(oids==[e['git_blob_sha1']for e in files.values()],'Old closure raw bytes do not match original Git blobs')
        index=b''.join((files[p]['mode']+' '+oid+'\t'+p+'\0').encode()for p,oid in zip(files,oids))
        run('update-index','-z','--index-info',input=index)
        tree=run('write-tree').decode().strip();require(tree==closure['published_tree'],'Full reconstructed old tree is incomplete or altered')
        commit=run('-c','user.name=Frozen publication view','-c','user.email=frozen@example.invalid',
                   'commit-tree',tree,input=b'Read-only reconstructed actual published tree; not original commit provenance\n').decode().strip()
        run('update-ref','refs/heads/frozen',commit);run('symbolic-ref','HEAD','refs/heads/frozen')
        for p in view.rglob('*'):
            if p.is_file():p.chmod(0o555 if p.stat().st_mode&stat.S_IXUSR else 0o444)
        for p in sorted(view.rglob('*'),key=lambda p:len(p.parts),reverse=True):
            if p.is_dir():p.chmod(0o555)
        view.chmod(0o555)
        try:yield view,closure
        finally:
            # TemporaryDirectory cleanup must remain possible after the test.
            view.chmod(0o755)
            for p in view.rglob('*'):
                if p.is_dir():p.chmod(0o755)
            for p in view.rglob('*'):
                if p.is_file():p.chmod(0o644)


def verify_old_guards(root,binding):
    with fixed_view(root,binding)as(view,closure):
        output=subprocess.check_output([sys.executable,str(view/'scripts/verify_representative_protected.py'),'--check'],
            cwd=view,env=git_env(),stderr=subprocess.STDOUT).decode()
        original=path(view,'revisions/baselines/complete-notes-2026-10-23.1.md').read_bytes()
        return dict(published_tree=closure['published_tree'],old_guard_output=output,original_markdown=original,
                    old_git_objects_required=False,view='EXACT_RECONSTRUCTED_PUBLISHED_HEAD_NOT_LIVE_N1')


def write_preparation(root,actor,published_commit,publication_binding,output):
    require(actor=='/root'and output.startswith(CLOSURE_PREFIX)and output.endswith('.json'),
            'Only root may retain a new immutable publication closure proposal')
    import note_review_queue as q
    q.validate_state(json.loads(committed(root,q.STATE)),Path(root))
    manifest,writes=prepare(root,published_commit,publication_binding)
    writes[output]=encoded(manifest)
    # Validate all destinations first; never overwrite an established revision.
    for relative,raw in writes.items():
        p=path(root,relative)
        require(not p.exists()or p.read_bytes()==raw,'Refusing to replace an established publication snapshot: '+relative)
    for relative,raw in writes.items():
        p=path(root,relative);p.parent.mkdir(parents=True,exist_ok=True)
        if not p.exists():p.write_bytes(raw)
    return {'path':output,'raw_sha256':sha(encoded(manifest)),'preimages':len(manifest['retained_preimages']),
            'status':'RETAINED_PROPOSAL_REQUIRES_COMMIT_AND_EXPLICIT_APPROVAL_NOT_ACTIVATION'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--actor');parser.add_argument('--prepare',action='store_true');parser.add_argument('--verify-old',action='store_true')
    parser.add_argument('--published-commit');parser.add_argument('--receipt');parser.add_argument('--output');parser.add_argument('--binding')
    args=parser.parse_args();root=args.root.resolve()
    if args.prepare:
        require(args.published_commit and args.receipt and args.output,'Actual published commit, committed primary receipt and new output path required')
        binding={'path':args.receipt,'raw_sha256':sha(committed(root,args.receipt))}
        print(json.dumps(write_preparation(root,args.actor,args.published_commit,binding,args.output),ensure_ascii=False))
    elif args.binding:
        binding={'path':args.binding,'raw_sha256':sha(committed(root,args.binding))}
        result=verify_old_guards(root,binding)if args.verify_old else validate(root,binding,coverage=True)
        print(json.dumps({'status':'VERIFIED_OLD_INPUT_VIEW_NOT_N1_APPROVAL','published_tree':result['published_tree']},ensure_ascii=False))
    else:
        print('BLOCKED: no actual published15 closure is bound; proposed candidate/CI or Pages assumptions are not publication proof.')
        raise SystemExit(1)


if __name__=='__main__':main()
