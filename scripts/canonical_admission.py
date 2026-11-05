"""Exact registered canonical successor contexts; legacy default APIs stay strict.

No supplied approval/PASS object is accepted. The production trust-root registry
is empty until actual evidence is independently enrolled. Positive test fixtures
never enroll this repository or grant audit/release credit.
"""
from dataclasses import dataclass
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess
import weakref

import canonical_admission_registry as registry
from canonical_successor import (ACTIVATION_PATH,FAMILY,PUBLISHED_NOTE16_SHA256,Seal,
    ALLOWED_ADDITION,BoundaryViolation,Proposal,digest,require,safe_path,strict_json,
    read_current_preimages,read_committed_preimages,verify_added_questions,verify_family_append,released)
from canonical_native_view import NativeView,native_validation

ROOT=Path(__file__).resolve().parents[1]
REGISTRY='scripts/canonical_admission_registry.py'
NOTE='revisions/notes/protected-migration-held-n1.json'
HOLDS='site/verified-law/delivery-holds.json'
PREVIEW='site/generated/preview_allowlist.json'
PAYLOAD='site/generated/questions.json'
BASELINE='reports/representative-rewrite/protected-baseline.json'
OLD_GUARDS={'scripts/verify_representative_protected.py','scripts/canonical_q0012_withdrawal.py',
    'scripts/notes_held_sixteenth.py','scripts/generate_artifacts.py'}
DERIVED={'duplicate_report.json','answer_distribution_report.json','structural_pattern_report.json','sba_answer_length_report.json'}
_TOKENS=weakref.WeakSet()


def json_hash(value):return digest(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args])
def seal(raw):return {'sha256':digest(raw),'bytes':len(raw)}
def exact(value,keys,label):require(isinstance(value,dict) and set(value)==set(keys),'Unknown/missing '+label+' fields')


def protocol_version(value):
    require(type(value)is int and value==1,'Unknown protocol version (must be integer1)')


def admission_id(value):
    require(isinstance(value,str)and bool(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}',value)),
        'Unsafe admission ID')
    return value


def coverage_destination(root,identifier,relative):
    identifier=admission_id(identifier);safe_path(relative)
    require(relative=='reports/canonical-successor/'+identifier+'-coverage.json','Coverage path outside exact derived namespace')
    root=Path(root).resolve();path=root/relative;cursor=root
    for part in Path(relative).parts:
        cursor=cursor/part;require(not cursor.is_symlink(),'Coverage output symlink rejected')
    require(path.resolve().parent==(root/'reports/canonical-successor').resolve()
        and root in path.resolve().parents,'Coverage output escapes root')
    return path


def current_inventory(root,parent):
    from verify_representative_protected import inventory
    return set(inventory(root))|set(parent['source_bindings'])|{p.relative_to(root).as_posix()
        for p in (root/'site/notes').rglob('*')if p.is_file()}|{NOTE,HOLDS,PREVIEW,PAYLOAD,BASELINE}|DERIVED


def require_committed_sources(root,head,actual):
    committed=read_committed_preimages(root,head,list(actual))
    require(committed==actual,'Enrollment/manifest/context must be exact committed HEAD regular blobs')


def require_clean_delivery_workspace(root,head,coverage_path):
    require(not git(root,'diff','--name-only','HEAD'),'Uncommitted tracked source is outside reviewed context')
    untracked={p.decode()for p in git(root,'ls-files','--others','--exclude-standard','-z').split(b'\0')if p}
    require(untracked<={coverage_path},'Unlisted untracked source outside exact derived coverage')
    # Pages copies the site directory, including ignored files. Check that disk
    # inventory as well; ignored local private folders outside site remain private.
    tree=git_tree(root,head);published={p for p in tree if p.startswith('site/')}
    require(all(tree[p]['type']=='blob'and tree[p]['mode']in {'100644','100755'}for p in published),'Published HEAD source is not a regular blob')
    disk={p.relative_to(root).as_posix()for p in (root/'site').rglob('*')if p.is_file()or p.is_symlink()}
    require(disk==published,'Unlisted or missing publishable UI disk source')
    if published:
        actual=read_current_preimages(root,sorted(published))
        immutable=read_committed_preimages(root,head,sorted(published))
        require(actual==immutable,'Published UI bytes differ from immutable HEAD; Git index flags cannot waive this check')


def verify_git_delta(root,base,content,head,allowed_content,allowed_post):
    def paths(before,after):
        return {p.decode()for p in git(root,'diff','--name-only','--no-renames','-z',before,after).split(b'\0')if p}
    require(paths(base,content)<=set(allowed_content),'Unlisted base-to-content Git delta')
    require(paths(content,head)<=set(allowed_post),'Unlisted content-to-enrollment Git delta')


def git_tree(root,commit):
    require(isinstance(commit,str) and len(commit)==40 and set(commit)<=set('0123456789abcdef'),'Exact Git commit required')
    require(git(root,'cat-file','-t',commit).strip()==b'commit','Anchor is not an immutable commit')
    result={}
    for entry in git(root,'ls-tree','-r','-z',commit).split(b'\0'):
        if entry:
            meta,name=entry.split(b'\t',1);mode,kind,oid=meta.decode().split();path=name.decode();safe_path(path)
            require(path not in result,'Duplicate Git tree path');result[path]={'mode':mode,'type':kind,'oid':oid}
    return result


def code_bindings(root):
    # Exact complete current runtime source inventory, excluding only the trust
    # root to avoid manifest -> registry -> enrollment -> manifest self-reference.
    paths=[p.relative_to(root).as_posix()for p in sorted((root/'scripts').glob('*.py'))if p.relative_to(root).as_posix()!=REGISTRY]
    return {path:digest(raw)for path,raw in read_current_preimages(root,paths).items()}


def protected_paths(root,tree,parent):
    from verify_representative_protected import in_scope
    return {p for p in tree if in_scope(p) or p.startswith('site/notes/')}|set(parent['source_bindings'])|{NOTE,HOLDS,PREVIEW,PAYLOAD,BASELINE}|DERIVED


def base_bundle(root,commit):
    tree=git_tree(root,commit)
    parent_raw=read_committed_preimages(root,commit,[NOTE])[NOTE]
    require(digest(parent_raw)==PUBLISHED_NOTE16_SHA256,'Base is not the retained approved notes16 body/context')
    parent=strict_json(parent_raw);paths=protected_paths(root,tree,parent)
    require(paths<=set(tree),'Base lacks a protected/bound path')
    require(all(tree[p]['type']=='blob' and tree[p]['mode'] in {'100644','100755'}for p in paths),'Base protected source is not a regular blob')
    return tree,parent_raw,parent,paths


def verify_hold_extension(before,after,questions):
    require(isinstance(before,dict)and isinstance(after,dict)and set(before)==set(after)=={'schema_version','status','reviews','holds'},'Delivery-hold schema changed')
    require(after['holds'][:len(before['holds'])]==before['holds'],'Existing delivery HOLD removed, rewritten or reordered')
    # Public source reports may append. Existing top-level provenance must remain.
    for key,value in before.items():
        if key in {'holds','reviews'}:continue
        require(after[key]==value,'Existing delivery HOLD provenance changed')
    require(after['reviews'][:len(before['reviews'])]==before['reviews'],'Old HOLD review provenance removed')
    review_ids=[r['id']for r in after['reviews']];require(len(review_ids)==len(set(review_ids)),'Duplicate public HOLD review ID')
    ids=[row['question_id']for row in after['holds']];require(len(ids)==len(set(ids)),'Duplicate delivery HOLD')
    from qa_common import question_audit_hash
    for row in after['holds']:
        exact(row,{'question_id','question_content_hash','category','reason','review_reason','review_id'},'delivery hold')
        require(row['category']in {'EDITORIAL_HOLD','LEGAL_HOLD','REALISM_REVIEW_REQUIRED'}and row['review_id']in review_ids and row['reason']and row['review_reason'],'Malformed public HOLD disposition')
        uid=row['question_id'];require(uid in questions and row['question_content_hash']==question_audit_hash(questions[uid]),'HOLD stale/unknown hash requires actual review; never silently released')
    return set(ids)


def verify_delivery_floor(overlay):
    floor=registry.DELIVERY_HOLD_FLOOR
    exact(floor,{'source_commit','source_path','source_sha256','question_hashes'},'reviewed delivery floor')
    current={row['question_id']:row['question_content_hash']for row in overlay['holds']}
    require(bool(floor['question_hashes'])and all(current.get(uid)==sha for uid,sha in floor['question_hashes'].items()),
        'A newer reviewed public delivery HOLD would be omitted or silently released')


def delivery_evidence(overlay):
    from urllib.parse import urlparse
    result={}
    for row in overlay['reviews']:
        exact(row,{'id','url','source_sha256','reviewed_date'},'public HOLD review')
        parsed=urlparse(row['url']);prefix='/woojunxnam/oddments/blob/main/'
        require(parsed.scheme=='https'and parsed.netloc=='github.com'and parsed.path.startswith(prefix),
            'HOLD review must resolve to the public repository evidence')
        relative=parsed.path[len(prefix):];safe_path(relative)
        require(relative.startswith('reports/coverage336/')and relative.endswith('.json'),'HOLD evidence path outside exact public report namespace')
        require(relative not in result,'Duplicate public HOLD evidence path');result[relative]=row['source_sha256']
    return result


def verify_payload_append(before,after,new_ids):
    exact(after,before.keys(),'generated payload')
    require(after['blueprint']==before['blueprint'],'Original blueprint payload changed')
    original=before['questions'];require(after['questions'][:len(original)]==original,'Old generated question objects/order/history changed')
    added=after['questions'][len(original):]
    require({q['question_id']for q in added}==set(new_ids)and len(added)==len(new_ids),'Generated additions differ from exact approved IDs')
    expected=copy.deepcopy(before['meta']);expected['question_count']=len(original)+len(added)
    require(after['meta']==expected,'Generated meta changed outside derived question count')
    require(len({q['question_id']for q in after['questions']})==len(after['questions']),'Duplicate generated ID')


def verify_preview_append(before,after,new_ids,new_audit_ids):
    require(set(after)==set(before),'Preview schema changed')
    for key,value in before.items():
        if key in {'question_ids','source_audits'}:continue
        require(after[key]==value,'Preview history/notice changed outside exact append')
    require(after['question_ids'][:len(before['question_ids'])]==before['question_ids'],'Old preview membership/order changed')
    require(set(after['question_ids'][len(before['question_ids']):])==set(new_ids)and len(after['question_ids'])==len(before['question_ids'])+len(new_ids),'Preview new IDs differ')
    require(after['source_audits'][:len(before['source_audits'])]==before['source_audits'],'Old preview audit history changed')
    extra=after['source_audits'][len(before['source_audits']):]
    require(set(extra)==set(new_audit_ids)and len(extra)==len(new_audit_ids),'Preview audit additions differ')
    require(not {'MA-Q-0012','MA-Q-0028'}&set(after['question_ids']),'Quarantined original returned to preview')


def verify_retained_preimages(root,commit,proof,baseline):
    from canonical_q0012_withdrawal import PATHS
    refs=proof['withdrawal_preimages'];require(set(refs)==set(PATHS)|{PREVIEW},'Original withdrawal return-map incomplete')
    rows={row['path']:row for row in baseline['files']}
    result={}
    for relative,binding in refs.items():
        exact(binding,{'path','sha256'},'retained original preimage')
        raw=read_committed_preimages(root,commit,[binding['path']])[binding['path']]
        require(digest(raw)==binding['sha256'],'Retained original preimage differs')
        if relative in rows:require(digest(raw)==rows[relative]['sha256'],'Original1781 preimage mapping changed')
        result[relative]=raw
    binding=proof['original_markdown'];exact(binding,{'path','sha256'},'original note preimage')
    md=read_committed_preimages(root,commit,[binding['path']])[binding['path']]
    require(digest(md)==binding['sha256']==rows['site/notes/complete-notes.md']['sha256'],'Original1781 note preimage differs')
    return result,md


class AdmissionContext:
    """Opaque validated handle. Construction alone cannot create a usable token."""
    def __init__(self,root,manifest,view,proof,parent,base_raw,new_questions):
        self._root=root;self._manifest=copy.deepcopy(manifest);self._view=view
        self._proof=copy.deepcopy(proof);self._parent=copy.deepcopy(parent)
        self._base_raw=dict(base_raw);self._new_questions=copy.deepcopy(new_questions);self._native_ok=False
    @property
    def root(self):return self._root
    @property
    def manifest(self):return copy.deepcopy(self._manifest)
    @property
    def view(self):return self._view
    @property
    def proof(self):return copy.deepcopy(self._proof)
    @property
    def parent(self):return copy.deepcopy(self._parent)
    @property
    def base_raw(self):return dict(self._base_raw)
    @property
    def new_questions(self):return copy.deepcopy(self._new_questions)
    @property
    def native_ok(self):return self._native_ok
    @property
    def current_seals(self):return copy.deepcopy(self._current_seals)
    @property
    def source_head(self):return self._source_head
    @property
    def registry_sha256(self):return self._registry_sha256
    @property
    def manifest_binding(self):return copy.deepcopy(self._manifest_binding)
    @property
    def note_binding(self):return copy.deepcopy(self._note_binding)
    def verify_withheld_reference(self,section,question):
        require(self in _TOKENS,'Unvalidated context token')
        require(section==strict_json(self.view.read('data/study_guide/sections/sg-cii-lifecycle.json'))and
            question==strict_json(self.view.read('data/questions/ma-q-0012.json')),'Withheld private guide/body changed')
        require(section['section_id']=='SG-CII-LIFECYCLE'and question['question_id']=='MA-Q-0012','Withheld reference scope expanded')
        return True


def require_context(context,*,native=True):
    require(isinstance(context,AdmissionContext)and context in _TOKENS and (context.native_ok or not native),'Unvalidated or failed native admission context')
    require(git(context.root,'rev-parse','HEAD').decode().strip()==context.source_head,'Validated source HEAD advanced')
    require(code_bindings(context.root)==context.manifest['code_sha256'],'Validated runtime source became stale')
    require(digest((context.root/REGISTRY).read_bytes())==context.registry_sha256,'Reviewed trust-root registry became stale')
    require(current_inventory(context.root,context.parent)==context._scope_paths,'Unlisted/deleted post-validation source inventory')
    coverage=coverage_destination(context.root,context.manifest['admission_id'],context.manifest['coverage_path'])
    require_clean_delivery_workspace(context.root,context.source_head,context.manifest['coverage_path'])
    if coverage.exists()and context._expected_coverage is not None:
        require(strict_json(coverage.read_bytes())==context._expected_coverage,'Derived coverage is not actual native output')
    # Revalidate all current file seals before consumption; no stale handle may
    # authorize a mutation performed after native validation.
    for path,expected in context.current_seals.items():
        raw=read_current_preimages(context.root,[path])[path]
        require(seal(raw)==expected,'Validated context became stale: '+path)
    return context


def registered_context(root=ROOT):
    root=Path(root).resolve();active=root/ACTIVATION_PATH
    if not active.exists() and not active.is_symlink():return None
    require(not active.is_symlink(),'Enrollment symlink rejected')
    raw=read_current_preimages(root,[ACTIVATION_PATH])[ACTIVATION_PATH];enrollment=strict_json(raw)
    exact(enrollment,{'schema_version','admission_id','manifest','notes_context'},'enrollment')
    protocol_version(enrollment['schema_version']);admission_id(enrollment['admission_id'])
    approved=registry.APPROVED_ADMISSIONS.get(enrollment['admission_id'])
    require(approved is not None,'No reviewed constant registry enrollment; approval/PASS JSON cannot authorize admission')
    exact(approved,{'enrollment_sha256','manifest','notes_context','base_proof_id'},'reviewed registry entry')
    require(digest(raw)==approved['enrollment_sha256']and enrollment['manifest']==approved['manifest']and enrollment['notes_context']==approved['notes_context'],'Enrollment differs from exact reviewed constant')
    # The trust-root source itself must be committed, not an unreviewed disk edit.
    require((root/REGISTRY).read_bytes()==git(root,'show','HEAD:'+REGISTRY),'Admission registry is not exact committed source')
    bindings=[approved['manifest'],approved['notes_context']]
    for binding in bindings:
        exact(binding,{'path','sha256'},'source binding');safe_path(binding['path'])
        require(binding['path'].startswith('revisions/canonical/')and binding['path']!=ACTIVATION_PATH,'Wrong successor manifest/context scope')
    sources=read_current_preimages(root,[b['path']for b in bindings])
    for b in bindings:require(digest(sources[b['path']])==b['sha256'],'Reviewed manifest/context bytes changed')
    require_committed_sources(root,git(root,'rev-parse','HEAD').decode().strip(),{ACTIVATION_PATH:raw,**sources})
    manifest=strict_json(sources[approved['manifest']['path']]);notes=strict_json(sources[approved['notes_context']['path']])
    return _validate_registered_sources(root,enrollment,approved,manifest,notes,raw,sources)


def _validate_registered_sources(root,enrollment,approved,m,notes,enrollment_raw,sources):
    """Internal registry-resolved validation. No caller PASS/approval parameter."""
    require(approved is not None and registry.APPROVED_ADMISSIONS.get(enrollment.get('admission_id'))==approved,
        'Only a resolved reviewed registry entry may mint a context')
    require(digest(enrollment_raw)==approved['enrollment_sha256']and strict_json(enrollment_raw)==enrollment,
        'Enrollment input differs from reviewed exact bytes')
    require((root/REGISTRY).read_bytes()==git(root,'show','HEAD:'+REGISTRY),'Trust root is not committed')
    for key,parsed in [('manifest',m),('notes_context',notes)]:
        binding=approved[key]
        raw=read_current_preimages(root,[binding['path']])[binding['path']]
        require(raw==sources[binding['path']]and digest(raw)==binding['sha256']and strict_json(raw)==parsed,
            'Unreviewed source passed directly to context validator')
    require_committed_sources(root,git(root,'rev-parse','HEAD').decode().strip(),{ACTIVATION_PATH:enrollment_raw,**sources})
    exact(m,{'schema_version','kind','admission_id','base_commit','base_tree','content_commit','base_proof_id','additions','changes','code_sha256','author_instances','coverage_path','delivery_evidence'},'manifest')
    require(m['kind']=='APPEND_CANONICAL_INITIAL','Unsupported context kind; safety withdrawals require a separate exact transaction')
    protocol_version(m['schema_version']);admission_id(m['admission_id'])
    require(m['admission_id']==enrollment['admission_id']and m['base_proof_id']==approved['base_proof_id'],'Manifest identity mismatch')
    coverage_destination(root,m['admission_id'],m['coverage_path'])
    proof=registry.APPROVED_BASE_GUARD_PROOFS.get(m['base_proof_id']);require(proof is not None,'No actual reviewed immutable-base guard proof')
    exact(proof,{'base_commit','base_tree','input_inventory_sha256','guard_code_sha256','receipt','protected_result','withdrawal_preimages','original_markdown'},'base guard proof')
    require(m['base_commit']==proof['base_commit']and m['base_tree']==proof['base_tree']==git(root,'rev-parse',m['base_commit']+'^{tree}').decode().strip(),'Unreviewed base commit/tree')
    tree,parent_raw,parent,base_paths=base_bundle(root,m['base_commit'])
    require(json_hash({p:tree[p]for p in sorted(base_paths-{HOLDS})})==proof['input_inventory_sha256'],'Reviewed base inventory differs; no re-enrollment')
    require(set(proof['guard_code_sha256'])==OLD_GUARDS,'Old guard code proof incomplete')
    for p,value in proof['guard_code_sha256'].items():require(digest((root/p).read_bytes())==value==digest(read_committed_preimages(root,m['base_commit'],[p])[p]),'Old guard/producer changed')
    receipt=proof['receipt'];exact(receipt,{'path','sha256'},'actual base receipt')
    require(digest(read_committed_preimages(root,m['base_commit'],[receipt['path']])[receipt['path']])==receipt['sha256'],'Reviewed actual base-guard receipt missing/stale')
    require(proof['protected_result']=={'files':1781,'bytes':60969461,'baseline_commit':'b5bd6b02c7ea8a5c6731871fa6e330ac6795fd36'},'Original1781 result changed')
    additions=m['additions'];changes=m['changes'];require(bool(additions),'No exact native additions')
    allowed_changes={FAMILY,PREVIEW,PAYLOAD,HOLDS}|DERIVED
    require(set(changes)==allowed_changes,'Missing or expanded existing-file delta')
    for p,expected in additions.items():safe_path(p);require(bool(ALLOWED_ADDITION.fullmatch(p))and p not in tree,'Unbounded/old-file addition')
    # Current selected inventory includes every unknown file under old protection.
    current_paths=current_inventory(root,parent)
    require(current_paths==base_paths|set(additions),'Protected/bound source omitted, deleted or added outside exact delta')
    current=read_current_preimages(root,sorted(current_paths));expected_content={}
    for p,raw in current.items():
        if p in additions:require(seal(raw)==additions[p],'New native bytes differ from manifest')
        elif p in changes:
            exact(changes[p],{'before','after'},'changed file seal')
            require(seal(raw)==changes[p]['after'],'Changed file after seal differs')
        else:
            require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==tree[p]['oid'],'Original source bytes changed: '+p)
        expected_content[p]=seal(raw)
    base_raw=read_committed_preimages(root,m['base_commit'],[p for p in base_paths if p.startswith('data/questions/')and p.endswith('.json')]+list(allowed_changes)+[BASELINE,NOTE])
    for p in changes:require(seal(base_raw[p])==changes[p]['before'],'Changed file preimage re-enrolled')
    original_returns,original_markdown=verify_retained_preimages(root,m['base_commit'],proof,strict_json(base_raw[BASELINE]))
    # Content commit exists before manifest/context/enrollment, with exact proposed
    # data/output and runtime code bytes. It cannot require its own future HEAD.
    content_tree=git_tree(root,m['content_commit'])
    require(not {ACTIVATION_PATH,approved['manifest']['path'],approved['notes_context']['path'],m['coverage_path']}&set(content_tree),'Content commit must precede manifest/context/enrollment/coverage')
    require(m['coverage_path']not in tree,'Coverage ID must not overwrite a retained prior artifact')
    require(subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',m['base_commit'],m['content_commit']],capture_output=True).returncode==0,'Content commit is not descended from trusted base')
    require(subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',m['content_commit'],'HEAD'],capture_output=True).returncode==0,'Content commit is not in current reviewed history')
    content_paths=list(additions)+list(changes)
    committed=read_committed_preimages(root,m['content_commit'],content_paths)
    require(all(committed[p]==current[p]for p in content_paths),'Current content differs from fixed content commit')
    require(m['code_sha256']==code_bindings(root),'Runtime code inventory/hash differs from reviewed manifest')
    committed_code=read_committed_preimages(root,m['content_commit'],list(m['code_sha256']))
    require(all(digest(committed_code[p])==value for p,value in m['code_sha256'].items()),'Runtime code differs from pre-enrollment content commit')
    base_code=read_committed_preimages(root,m['base_commit'],list(m['code_sha256']))
    require(base_code==committed_code,'Runtime implementation must already exist in trusted base; content cannot change code')
    verify_git_delta(root,m['base_commit'],m['content_commit'],'HEAD',set(additions)|set(changes)|set(m['delivery_evidence']),
        {ACTIVATION_PATH,REGISTRY,approved['manifest']['path'],approved['notes_context']['path'],m['coverage_path']})
    old_questions={q['question_id']:q for q in (strict_json(raw)for p,raw in base_raw.items()if p.startswith('data/questions/')and p.endswith('.json'))}
    new_raw={p:current[p]for p in additions};new_questions=verify_added_questions(old_questions,new_raw)
    require(len(old_questions)==439 and sum(released(q)for q in old_questions.values())==397,'Original439/397 base membership changed')
    require(all(released(q)for q in new_questions.values()),'Draft/HOLD candidate cannot be admitted by a release context')
    verify_family_append(strict_json(base_raw[FAMILY]),strict_json(current[FAMILY]),old_questions,new_questions)
    questions={**old_questions,**new_questions};held=verify_hold_extension(strict_json(base_raw[HOLDS]),strict_json(current[HOLDS]),questions)
    require(not held&set(new_questions),'New admitted item has a current delivery HOLD')
    after_holds=strict_json(current[HOLDS]);verify_delivery_floor(after_holds)
    evidence=delivery_evidence(after_holds)
    require(m['delivery_evidence']==evidence,'Public HOLD evidence missing or expanded')
    committed_evidence=read_committed_preimages(root,m['content_commit'],list(evidence))
    for path,value in evidence.items():
        raw=read_current_preimages(root,[path])[path]
        require(digest(raw)==value and raw==committed_evidence[path],'Public HOLD evidence is stale/uncommitted')
        expected_content[path]=seal(raw)
    new_audits={strict_json(current[p])['audit_id']for p in additions if p.startswith('data/audits/')}
    verify_preview_append(strict_json(base_raw[PREVIEW]),strict_json(current[PREVIEW]),new_questions,new_audits)
    verify_payload_append(strict_json(base_raw[PAYLOAD]),strict_json(current[PAYLOAD]),new_questions)
    require(isinstance(m['author_instances'],list)and m['author_instances']and all(isinstance(a,str)and a for a in m['author_instances'])and len(m['author_instances'])==len(set(m['author_instances'])),'Actual author provenance required')
    from qa_common import question_audit_hash
    for p in additions:
        value=strict_json(current[p])
        if p.startswith('data/questions/'):
            require(value.get('provenance')=='GEN'and value.get('source_signal_ids')==[]and not value.get('development_fixture'),'Only independent official-law GEN questions allowed')
        if p.startswith('data/audits/'):
            require(value.get('independent')is True and value.get('auditor_instance')not in m['author_instances'],'Author/session cannot self-certify independence')
            require(set(value.get('question_ids',[]))<=set(new_questions),'Append-initial audit cannot mutate old-ID audit history; use a separate safety context')
    for uid,q in new_questions.items():
        initials=[strict_json(current[p])for p in additions if p.startswith('data/audits/')]
        require(any(a.get('audit_scope')=='INITIAL_BATCH'and a.get('review_type')=='LEGAL_VERIFICATION'and a.get('question_hashes',{}).get(uid)==question_audit_hash(q)for a in initials),'No new exact-current-hash ordinary INITIAL audit')
    exact(notes,{'schema_version','purpose','parent_sha256','manifest_sha256','parent_source_bindings','source_delta','outputs','claim_ledger_sha256'},'notes source context')
    protocol_version(notes['schema_version'])
    require(notes['purpose']=='CANONICAL_SOURCE_ONLY_NOT_NOTE_LEGAL_REVIEW'and notes['parent_sha256']==digest(parent_raw)and notes['manifest_sha256']==approved['manifest']['sha256'],'Notes source context parent/manifest changed or cycle')
    require(notes['parent_source_bindings']==parent['source_bindings'],'Old notes source binding removed/replaced')
    expected_delta={p:{'before':changes[p]['before']['sha256'],'after':changes[p]['after']['sha256']}for p in changes}
    expected_delta.update({p:{'before':None,'after':expected['sha256']}for p,expected in additions.items()})
    require(notes['source_delta']==expected_delta,'Source-only delta missing/expanded')
    outputs={p:digest(current[p])for p in base_paths if p.startswith('site/notes/')}
    require(notes['outputs']==outputs and notes['claim_ledger_sha256']==parent['source_bindings']['reports/full-corpus-review/notes-unit-ledger.jsonl'],'Note output/claim context differs')
    coverage_destination(root,m['admission_id'],m['coverage_path'])
    view=NativeView(root,m['base_commit'],{p:current[p]for p in set(additions)|set(changes)})
    context=AdmissionContext(root,m,view,proof,parent,base_raw,new_questions)
    context._scope_paths=frozenset(current_paths);context._expected_coverage=None
    context._current_seals={**expected_content,ACTIVATION_PATH:seal(enrollment_raw),**{p:seal(raw)for p,raw in sources.items()}}
    context._manifest_binding=approved['manifest'];context._note_binding=approved['notes_context']
    context._original_returns=original_returns;context._original_markdown=original_markdown
    context._registry_sha256=digest((root/REGISTRY).read_bytes())
    context._source_head=git(root,'rev-parse','HEAD').decode().strip()
    _TOKENS.add(context)
    try:
        native,validated=native_validation(view,release=True,withdrawal_context=context)
        require(native.ok,'Actual native full validators rejected admission: '+'; '.join(native.errors))
        from qa_common import canonical_read_view
        from build_site_data import build_site_payload
        with canonical_read_view(view):produced=build_site_payload()
        require(produced==strict_json(current[PAYLOAD]),'Generated append is not actual native producer output')
        outputs=_produce_artifacts(context)
        for relative in DERIVED:
            require(outputs[root/relative]==strict_json(current[relative]),'Derived report differs from actual native producer: '+relative)
        expected_guide=strict_json(read_committed_preimages(root,m['base_commit'],['site/generated/study_guide.json'])['site/generated/study_guide.json'])
        require(outputs[root/'site/generated/study_guide.json']==expected_guide,'Original generated guide changed')
        context._expected_guide=copy.deepcopy(expected_guide)
        context._expected_coverage=outputs[coverage_destination(root,m['admission_id'],m['coverage_path'])]
        context._native_ok=True
    except BaseException:
        _TOKENS.discard(context);raise
    return require_context(context)


def original_preimages(context):
    context=require_context(context)
    return dict(context._original_returns)



def verify_protected(manifest,root=ROOT,*,context=None):
    """Compatibility adapter: unchanged legacy default, explicit validated successor."""
    if context is None:
        from verify_representative_protected import verify
        return verify(manifest,root)
    context=require_context(context);require(Path(root).resolve()==context.root,'Context/root mismatch')
    require(manifest==strict_json(context.base_raw[BASELINE]),'Original1781 manifest replaced')
    return copy.deepcopy(context.proof['protected_result'])


def validate_withdrawal(root=ROOT,*,context=None):
    if context is None:
        from canonical_q0012_withdrawal import validate
        return validate(root)
    require(Path(root).resolve()==context.root,'Context/root mismatch')
    return original_preimages(context)


def decode_notes(root,relative,current,*,context=None):
    if context is None:
        from notes_held_sixteenth import decode
        return decode(root,relative,current)
    context=require_context(context);require(Path(root).resolve()==context.root and relative=='site/notes/complete-notes.md','Note decoder scope/root changed')
    require(seal(current)==context.current_seals[relative],'Note decoder received noncurrent bytes')
    return context._original_markdown



def coverage_snapshot(coverage,questions,guide,*,context=None):
    """Rootless old API remains397; registered coverage is a separate artifact."""
    if context is None:
        from canonical_q0012_withdrawal import coverage_snapshot as old
        return old(coverage,questions,guide)
    context=require_context(context)
    require(coverage==context._expected_coverage['current_native_coverage'],'Supplied coverage differs from actual native producer')
    require(questions==strict_json(context.view.read(PAYLOAD))and guide==context._expected_guide,'Supplied question/guide payload differs from actual native producer')
    return copy.deepcopy(context._expected_coverage)


def _coverage_value(coverage,questions,guide,context):
    original=strict_json(context.base_raw[PAYLOAD]);verify_payload_append(original,questions,context.new_questions)
    public=guide['sections'];ids={s['section_id']for s in public}
    require('SG-CII-LIFECYCLE'not in ids and 'MA-Q-0012'not in guide['question_to_sections'],'Withheld linked guide returned')
    require(not {'MA-Q-0012','MA-Q-0028'}&{q['question_id']for q in questions['questions']},'Quarantined original returned')
    require(coverage['sections']['by_status']['VERIFIED']==len(public)==guide['meta']['public_verified_section_count'],'Actual guide coverage public count differs')
    public_rules={rid for section in public for rid in section['rule_ids']}
    require(coverage['canonical_rules']['covered_by_verified_public_section']==len(public_rules),'Actual public rule coverage count differs')
    from canonical_q0012_withdrawal import CURRENT_COVERAGE
    historical=context.view.read(CURRENT_COVERAGE)
    return {'schema_version':'canonical-successor-coverage/1','admission_id':context.manifest['admission_id'],
        'manifest_sha256':context.manifest_binding['sha256'],'notes_context_sha256':context.note_binding['sha256'],
        'immutable_original_coverage':{'path':CURRENT_COVERAGE,'sha256':digest(historical)},
        'current_native_coverage':copy.deepcopy(coverage),
        'canonical_released_question_count':len(questions['questions']),
        'new_exact_eligible_question_ids':sorted(context.new_questions),
        'original397_objects_preserved':True,'quarantines_preserved':['MA-Q-0012','MA-Q-0028'],
        'note_legal_PASS_credit':0,'legacy_replay_executed_by_this_snapshot':False}


def artifact_payloads(context):
    """Run the real producers under the exact validated immutable registry view."""
    context=require_context(context)
    return _produce_artifacts(context)


def _produce_artifacts(context):
    from qa_common import canonical_read_view
    from build_site_data import build_site_payload
    from build_study_guide_data import build_study_guide_payload,build_study_guide_coverage
    from detect_duplicates import detect_duplicates
    from check_answer_distribution import analyze_answer_distribution
    from check_structural_patterns import analyze_structural_patterns
    from check_sba_answer_length import analyze_sba_answer_length
    with canonical_read_view(context.view):
        questions=build_site_payload()
        guide=build_study_guide_payload(admission_context=context)
        coverage=_coverage_value(build_study_guide_coverage(admission_context=context),questions,guide,context)
        distribution,_=analyze_answer_distribution();structural,_=analyze_structural_patterns();length,_=analyze_sba_answer_length()
        result={context.root/'duplicate_report.json':detect_duplicates(),context.root/'answer_distribution_report.json':distribution,
            context.root/'structural_pattern_report.json':structural,context.root/'sba_answer_length_report.json':length,
            coverage_destination(context.root,context.manifest['admission_id'],context.manifest['coverage_path']):coverage,context.root/PAYLOAD:questions,
            context.root/'site/generated/study_guide.json':guide}
    # Derived artifacts must not overwrite any retained old input/output except
    # the exactly reviewed generated questions append. Notes outputs never change.
    for path,value in result.items():
        relative=path.relative_to(context.root).as_posix()
        if relative in context.current_seals and relative not in DERIVED|{PAYLOAD,context.manifest['coverage_path']}:
            require(strict_json(context.view.read(relative))==value,'Producer would overwrite a retained source/artifact: '+relative)
    return result
