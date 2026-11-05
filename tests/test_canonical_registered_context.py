"""Boundary/native-reader tests. Synthetic fixtures never enroll production data."""
import copy
import json
from pathlib import Path

import pytest

import canonical_admission as admission
import canonical_admission_registry as registry
from canonical_native_view import NativeView
from canonical_successor import BoundaryViolation
import qa_common

ROOT=Path(__file__).resolve().parents[1]
BASE='ea19d9881ec5b6a476f7dfc113cd1a4bc18c92da'


@pytest.fixture(scope='module')
def native_view():
    # HEAD is available even in shallow CI. Outputs/data at this stage remain
    # unchanged. Historical EA19 is not required by these unit tests.
    commit=admission.git(ROOT,'rev-parse','HEAD').decode().strip()
    return NativeView(ROOT,commit)


def test_no_registry_enrollment_is_an_explicit_absence_not_approval(tmp_path):
    assert admission.registered_context(tmp_path) is None
    assert registry.APPROVED_ADMISSIONS==registry.APPROVED_BASE_GUARD_PROOFS=={}


@pytest.mark.parametrize('payload',[{}, {'approved':True}, {'PASS':True},
    {'schema_version':1,'admission_id':'SYNTHETIC-NOT-REGISTERED','manifest':{},'notes_context':{}}])
def test_json_approval_or_unknown_enrollment_cannot_replace_reviewed_constants(tmp_path,payload):
    p=tmp_path/admission.ACTIVATION_PATH;p.parent.mkdir(parents=True);p.write_text(json.dumps(payload))
    with pytest.raises(BoundaryViolation):admission.registered_context(tmp_path)


def test_symlink_enrollment_is_rejected_even_when_its_target_is_missing(tmp_path):
    p=tmp_path/admission.ACTIVATION_PATH;p.parent.mkdir(parents=True);p.symlink_to(tmp_path/'missing')
    with pytest.raises(BoundaryViolation):admission.registered_context(tmp_path)


def test_calling_internal_validator_with_supplied_pass_or_approval_cannot_mint_a_token(tmp_path):
    e={'admission_id':'SYNTHETIC-UNREGISTERED'}
    with pytest.raises(BoundaryViolation,match='registry'):
        admission._validate_registered_sources(tmp_path,e,{'approved':True},{},{},b'{}',{})
    forged=admission.AdmissionContext(tmp_path,{},None,{},None,{},{})
    with pytest.raises(AttributeError):forged.native_ok=True
    with pytest.raises(BoundaryViolation,match='Unvalidated'):admission.require_context(forged)


def test_read_view_uses_fresh_values_does_not_mutate_source_and_resets_after_exception(native_view):
    path=ROOT/'data/blueprint.json';before=path.read_bytes()
    with pytest.raises(RuntimeError):
        with qa_common.canonical_read_view(native_view):
            first=qa_common.load_json(path);first['exam']='Synthetic mutation'
            assert qa_common.load_json(path)['exam']!='Synthetic mutation'
            with pytest.raises(ValueError,match='read-only'):qa_common.write_json(path,{})
            raise RuntimeError('test context reset')
    assert qa_common.load_json(path)==json.loads(before) and path.read_bytes()==before


def test_native_read_view_lists_real_original439_records_and_never_publishes(native_view):
    with qa_common.canonical_read_view(native_view):
        values=qa_common.load_records(ROOT/'data/questions')
        assert len(values)==439 and sum(admission.released(q)for _,q in values)==397
        assert not {'MA-Q-0012','MA-Q-0028'}&{q['question_id']for _,q in values if admission.released(q)}
    with pytest.raises(BoundaryViolation):native_view.load_json(Path('/tmp/outside-source.json'))


def overlay(questions):
    return {'schema_version':'canonical-delivery-holds/1','status':'DELIVERY_HOLD_NOT_CANONICAL_CHANGE',
        'reviews':[{'id':'SYNTHETIC-REVIEW','url':'https://github.com/woojunxnam/oddments/blob/main/reports/coverage336/synthetic.json','source_sha256':'a'*64,'reviewed_date':'2026-11-05'}],
        'holds':[{'question_id':uid,'question_content_hash':qa_common.question_audit_hash(q),'category':'LEGAL_HOLD',
            'reason':'합성 경계 fixture','review_reason':'실제 법규 판정 아님','review_id':'SYNTHETIC-REVIEW'}for uid,q in questions.items()]}


def test_delivery_holds_extend_monotonically_without_fixed16_count():
    q1={'question_id':'SYNTHETIC-ONE','stem':'first'};q2={'question_id':'SYNTHETIC-TWO','stem':'second'}
    before=overlay({'SYNTHETIC-ONE':q1});after=overlay({'SYNTHETIC-ONE':q1,'SYNTHETIC-TWO':q2})
    assert admission.verify_hold_extension(before,after,{'SYNTHETIC-ONE':q1,'SYNTHETIC-TWO':q2})=={'SYNTHETIC-ONE','SYNTHETIC-TWO'}
    removed=copy.deepcopy(after);removed['holds'].pop(0)
    with pytest.raises(BoundaryViolation):admission.verify_hold_extension(before,removed,{'SYNTHETIC-ONE':q1,'SYNTHETIC-TWO':q2})
    stale=copy.deepcopy(after);stale['holds'][1]['question_content_hash']='b'*64
    with pytest.raises(BoundaryViolation):admission.verify_hold_extension(before,stale,{'SYNTHETIC-ONE':q1,'SYNTHETIC-TWO':q2})
    rewritten=copy.deepcopy(after);rewritten['holds'][0]['reason']='silently replaced reason'
    with pytest.raises(BoundaryViolation):admission.verify_hold_extension(before,rewritten,{'SYNTHETIC-ONE':q1,'SYNTHETIC-TWO':q2})


def test_delivery_floor_requires_all19_current_public_negatives_not_just_old16():
    floor=registry.DELIVERY_HOLD_FLOOR
    assert floor['source_commit']=='c7d5162fa8deb75d61f17ec02159e69634ffcbd7' and len(floor['question_hashes'])==19
    full={'holds':[{'question_id':uid,'question_content_hash':sha}for uid,sha in floor['question_hashes'].items()]}
    admission.verify_delivery_floor(full)
    missing=copy.deepcopy(full);missing['holds']=missing['holds'][:16]
    with pytest.raises(BoundaryViolation):admission.verify_delivery_floor(missing)
    stale=copy.deepcopy(full);stale['holds'][-1]['question_content_hash']='a'*64
    with pytest.raises(BoundaryViolation):admission.verify_delivery_floor(stale)


def test_public_delivery_review_evidence_is_exact_local_repo_namespace():
    good=overlay({});assert admission.delivery_evidence(good)=={'reports/coverage336/synthetic.json':'a'*64}
    bad=copy.deepcopy(good);bad['reviews'][0]['url']='https://example.invalid/approved.json'
    with pytest.raises(BoundaryViolation):admission.delivery_evidence(bad)
    bad=copy.deepcopy(good);bad['reviews'][0]['url']='https://github.com/woojunxnam/oddments/blob/main/private_sources/hidden.json'
    with pytest.raises(BoundaryViolation):admission.delivery_evidence(bad)


def test_generated_append_preserves_old_objects_and_rejects_metadata_overwrite():
    before={'meta':{'question_count':1,'release_status':'RELEASE_AVAILABLE'},'blueprint':{'id':'fixture'},'questions':[{'question_id':'OLD','audits':['OLD-AUDIT'],'key':'A'}]}
    after=copy.deepcopy(before);after['meta']['question_count']=2;after['questions'].append({'question_id':'NEW'})
    admission.verify_payload_append(before,after,{'NEW'})
    for mutation in [lambda x:x['questions'][0].update(key='B'),lambda x:x['questions'][0]['audits'].append('NEW-OPINION'),lambda x:x['meta'].update(release_status='APPROVED')]:
        changed=copy.deepcopy(after);mutation(changed)
        with pytest.raises(BoundaryViolation):admission.verify_payload_append(before,changed,{'NEW'})


def test_preview_append_preserves_prior_history_and_quarantines():
    before={'question_ids':['OLD'],'source_audits':['OLD-AUDIT'],'notice':'unchanged'}
    after={'question_ids':['OLD','NEW'],'source_audits':['OLD-AUDIT','NEW-AUDIT'],'notice':'unchanged'}
    admission.verify_preview_append(before,after,{'NEW'},{'NEW-AUDIT'})
    for key in ['question_ids','source_audits']:
        value=copy.deepcopy(after);value[key].reverse()
        with pytest.raises(BoundaryViolation):admission.verify_preview_append(before,value,{'NEW'},{'NEW-AUDIT'})
    value=copy.deepcopy(after);value['question_ids'][-1]='MA-Q-0028'
    with pytest.raises(BoundaryViolation):admission.verify_preview_append(before,value,{'MA-Q-0028'},{'NEW-AUDIT'})


def test_code_manifest_has_exact_runtime_inventory_but_excludes_trust_root_self_cycle():
    code=admission.code_bindings(ROOT)
    assert admission.REGISTRY not in code
    assert {'scripts/canonical_admission.py','scripts/canonical_native_view.py','scripts/qa_common.py'}<=set(code)
    assert admission.OLD_GUARDS<=set(code)


def test_legacy_default_withdrawal_api_returns_original_four_preimage_bytes():
    import canonical_q0012_withdrawal as old
    result=admission.validate_withdrawal(ROOT)
    assert result==old.validate(ROOT) and set(result)==set(old.PATHS)|{admission.PREVIEW}


def test_rootless_default_coverage_remains_exact_original397_contract():
    import canonical_q0012_withdrawal as old
    coverage=json.loads((ROOT/old.CURRENT_COVERAGE).read_bytes())
    questions=json.loads((ROOT/admission.PAYLOAD).read_bytes())
    guide=json.loads((ROOT/'site/generated/study_guide.json').read_bytes())
    assert admission.coverage_snapshot(coverage,questions,guide)==old.coverage_snapshot(coverage,questions,guide)
    expanded=copy.deepcopy(questions);expanded['questions'].append({'question_id':'SYNTHETIC-UNAPPROVED'})
    with pytest.raises(ValueError):admission.coverage_snapshot(coverage,expanded,guide)


def test_native_guide_adapter_rejects_generic_caller_pass_object():
    from validate_study_guide import validate_study_guide
    class FakePass:
        def verify_withheld_reference(self,section,question):return True
    with pytest.raises(ValueError,match='Unvalidated'):
        validate_study_guide({}, {},withdrawal_context=FakePass())


def test_validated_context_and_native_cache_do_not_expose_mutable_grade_inputs(native_view):
    context=admission.AdmissionContext(ROOT,{'admission_id':'SYNTHETIC'},native_view,{'protected_result':{'files':1781}},None,{}, {'SYNTHETIC':{'stem':'original'}})
    changed=context.manifest;changed['admission_id']='FORGED'
    questions=context.new_questions;questions['SYNTHETIC']['stem']='changed'
    assert context.manifest['admission_id']=='SYNTHETIC'and context.new_questions['SYNTHETIC']['stem']=='original'
    with pytest.raises(TypeError):native_view.cache['data/fake.json']=b'{}'
    with pytest.raises(TypeError):native_view.replacements['data/fake.json']=b'{}'
    with pytest.raises(AttributeError):native_view.base_commit='0'*40


def test_actual_retained_withdrawal_and_markdown_preimages_are_verified_before_token_mint():
    import hashlib
    import canonical_q0012_withdrawal as old
    commit=admission.git(ROOT,'rev-parse','HEAD').decode().strip();tree=admission.git_tree(ROOT,commit)
    originals=old.validate(ROOT);baseline=json.loads((ROOT/admission.BASELINE).read_bytes())
    def binding(raw):
        oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        path=next(p for p,v in tree.items()if v['oid']==oid)
        return {'path':path,'sha256':admission.digest(raw)}
    row=next(r for r in baseline['files']if r['path']=='site/notes/complete-notes.md')
    md_path=next(p for p,v in tree.items()if v['oid']==row['git_blob_sha1'])
    proof={'withdrawal_preimages':{p:binding(raw)for p,raw in originals.items()},'original_markdown':{'path':md_path,'sha256':row['sha256']}}
    result,md=admission.verify_retained_preimages(ROOT,commit,proof,baseline)
    assert result==originals and admission.digest(md)==row['sha256']
    missing=copy.deepcopy(proof);missing['withdrawal_preimages'].pop(admission.PREVIEW)
    with pytest.raises(BoundaryViolation):admission.verify_retained_preimages(ROOT,commit,missing,baseline)
    stale=copy.deepcopy(proof);stale['withdrawal_preimages'][admission.PREVIEW]['sha256']='a'*64
    with pytest.raises(BoundaryViolation):admission.verify_retained_preimages(ROOT,commit,stale,baseline)


@pytest.mark.parametrize('identifier',['../../../outside-reviewed-root','../escape','bad/id','bad\\id','bad id','',None])
def test_admission_ids_and_coverage_destinations_reject_escape_before_registration(tmp_path,identifier):
    with pytest.raises(BoundaryViolation):admission.coverage_destination(tmp_path,identifier,'reports/canonical-successor/'+str(identifier)+'-coverage.json')


def test_exact_coverage_namespace_rejects_symlink_and_wrong_destination(tmp_path):
    path=admission.coverage_destination(tmp_path,'SAFE_31','reports/canonical-successor/SAFE_31-coverage.json')
    assert path==tmp_path/'reports/canonical-successor/SAFE_31-coverage.json'
    with pytest.raises(BoundaryViolation):admission.coverage_destination(tmp_path,'SAFE_31','reports/other/SAFE_31-coverage.json')
    outside=tmp_path/'elsewhere';outside.mkdir();(tmp_path/'reports').mkdir()
    (tmp_path/'reports/canonical-successor').symlink_to(outside,target_is_directory=True)
    with pytest.raises(BoundaryViolation):admission.coverage_destination(tmp_path,'SAFE_31','reports/canonical-successor/SAFE_31-coverage.json')


@pytest.mark.parametrize('version',[True,False,1.0,'1',None,0,2])
def test_protocol_versions_are_integer1_not_boolean_or_numeric_aliases(version):
    with pytest.raises(BoundaryViolation):admission.protocol_version(version)
    admission.protocol_version(1)


def synthetic_git(root):
    import subprocess
    def run(*args):return subprocess.check_output(['git','-C',str(root),*args])
    run('init','--quiet');run('config','user.name','Synthetic Test');run('config','user.email','synthetic@example.invalid')
    return run


def test_whole_git_delta_accepts_only_exact_content_and_enrollment_paths(tmp_path):
    run=synthetic_git(tmp_path)
    for path,body in [('data/item.json','{}'),('site/app.js','original')]:
        p=tmp_path/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body)
    run('add','.');run('commit','--quiet','-m','synthetic base');base=run('rev-parse','HEAD').decode().strip()
    (tmp_path/'data/item.json').write_text('{"synthetic":true}')
    run('add','.');run('commit','--quiet','-m','synthetic content');content=run('rev-parse','HEAD').decode().strip()
    (tmp_path/'enrollment.json').write_text('{}');run('add','.');run('commit','--quiet','-m','synthetic enrollment')
    head=run('rev-parse','HEAD').decode().strip()
    admission.verify_git_delta(tmp_path,base,content,head,{'data/item.json'},{'enrollment.json'})
    (tmp_path/'site/app.js').write_text('unlisted post-content mutation')
    run('add','.');run('commit','--quiet','-m','synthetic unsafe post-content')
    with pytest.raises(BoundaryViolation,match='content-to-enrollment'):
        admission.verify_git_delta(tmp_path,base,content,'HEAD',{'data/item.json'},{'enrollment.json'})
    with pytest.raises(BoundaryViolation,match='base-to-content'):
        admission.verify_git_delta(tmp_path,base,'HEAD','HEAD',{'data/item.json'},{'enrollment.json'})


def test_post_validation_inventory_and_dirty_tracked_ui_are_rejected(tmp_path,monkeypatch):
    # Deliberately test-only post-mint capability fixture. It bypasses no real
    # registration check and is never counted as native admission or audit.
    run=synthetic_git(tmp_path)
    for path,body in [('data/item.json','{}'),(admission.REGISTRY,'# synthetic fixture'),('site/app.js','original')]:
        p=tmp_path/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body)
    run('add','.');run('commit','--quiet','-m','synthetic post-mint predicate')
    def inventory(root,parent):return {p.relative_to(root).as_posix()for p in (root/'data').glob('*.json')}
    monkeypatch.setattr(admission,'current_inventory',inventory)
    m={'admission_id':'SYNTHETIC_ONLY','coverage_path':'reports/canonical-successor/SYNTHETIC_ONLY-coverage.json','code_sha256':{}}
    context=admission.AdmissionContext(tmp_path,m,None,{}, {},{}, {})
    context._native_ok=True;context._source_head=run('rev-parse','HEAD').decode().strip()
    context._registry_sha256=admission.digest((tmp_path/admission.REGISTRY).read_bytes())
    context._scope_paths=frozenset(inventory(tmp_path,{}));context._expected_coverage=None
    context._current_seals={'data/item.json':admission.seal((tmp_path/'data/item.json').read_bytes())}
    admission._TOKENS.add(context)
    assert admission.require_context(context)is context
    (tmp_path/'data/unlisted.json').write_text('{}')
    with pytest.raises(BoundaryViolation,match='inventory'):admission.require_context(context)
    (tmp_path/'data/unlisted.json').unlink()
    (tmp_path/'site/app.js').write_text('uncommitted tracked mutation')
    with pytest.raises(BoundaryViolation,match='Uncommitted'):admission.require_context(context)
    assert registry.APPROVED_ADMISSIONS=={}


def test_publishable_ignored_ui_file_is_not_an_enrolled_disk_input(tmp_path):
    run=synthetic_git(tmp_path)
    (tmp_path/'site').mkdir();(tmp_path/'site/app.js').write_text('tracked')
    (tmp_path/'.gitignore').write_text('site/ignored/\n')
    run('add','.');run('commit','--quiet','-m','synthetic clean delivery')
    head=run('rev-parse','HEAD').decode().strip()
    admission.require_clean_delivery_workspace(tmp_path,head,'reports/canonical-successor/TEST-coverage.json')
    (tmp_path/'site/new.js').write_text('unlisted')
    with pytest.raises(BoundaryViolation,match='untracked'):admission.require_clean_delivery_workspace(tmp_path,head,'reports/canonical-successor/TEST-coverage.json')
    (tmp_path/'site/new.js').unlink();(tmp_path/'site/ignored').mkdir();(tmp_path/'site/ignored/private.html').write_text('synthetic ignored material')
    with pytest.raises(BoundaryViolation,match='publishable'):admission.require_clean_delivery_workspace(tmp_path,head,'reports/canonical-successor/TEST-coverage.json')


def test_exact_hash_but_untracked_manifest_is_not_a_committed_source(tmp_path):
    run=synthetic_git(tmp_path);p=tmp_path/'enrollment.json';p.write_bytes(b'{"synthetic":true}\n')
    run('add','.');run('commit','--quiet','-m','synthetic committed source')
    head=run('rev-parse','HEAD').decode().strip()
    admission.require_committed_sources(tmp_path,head,{'enrollment.json':p.read_bytes()})
    (tmp_path/'manifest.json').write_bytes(p.read_bytes())
    with pytest.raises(BoundaryViolation):admission.require_committed_sources(tmp_path,head,{'manifest.json':p.read_bytes()})
    with pytest.raises(BoundaryViolation):admission.require_committed_sources(tmp_path,head,{'enrollment.json':b'{"different":true}\n'})


def test_public_snapshot_cannot_copy_arbitrary_coverage_with_equal_counts(tmp_path,monkeypatch):
    # Test-only post-mint state, not actual registration/native audit evidence.
    run=synthetic_git(tmp_path);(tmp_path/'scripts').mkdir();(tmp_path/admission.REGISTRY).write_text('# synthetic')
    run('add','.');run('commit','--quiet','-m','synthetic immutable post-native state')
    monkeypatch.setattr(admission,'current_inventory',lambda root,parent:set())
    questions={'questions':[{'question_id':'SYNTHETIC'}]};guide={'sections':[]};coverage={'counts':{'VERIFIED':1},'uncovered_rule_ids':['SYNTHETIC-RULE']}
    class ReadView:
        def read(self,path):return json.dumps(questions).encode()
    m={'admission_id':'SYNTHETIC_ONLY','coverage_path':'reports/canonical-successor/SYNTHETIC_ONLY-coverage.json','code_sha256':{}}
    context=admission.AdmissionContext(tmp_path,m,ReadView(),{}, {},{}, {})
    context._native_ok=True;context._source_head=run('rev-parse','HEAD').decode().strip()
    context._registry_sha256=admission.digest((tmp_path/admission.REGISTRY).read_bytes())
    context._scope_paths=frozenset();context._current_seals={};context._expected_guide=guide
    context._expected_coverage={'current_native_coverage':coverage,'test_only':True}
    admission._TOKENS.add(context)
    actual=admission.coverage_snapshot(coverage,questions,guide,context=context)
    assert actual==context._expected_coverage
    forged=copy.deepcopy(coverage);forged['uncovered_rule_ids']=[]
    with pytest.raises(BoundaryViolation,match='coverage'):admission.coverage_snapshot(forged,questions,guide,context=context)
    with pytest.raises(BoundaryViolation,match='question/guide'):admission.coverage_snapshot(coverage,{'questions':[]},guide,context=context)
    actual['test_only']=False;assert context._expected_coverage['test_only']is True
    assert registry.APPROVED_ADMISSIONS=={}


@pytest.mark.parametrize('index_flag',['--assume-unchanged','--skip-worktree'])
@pytest.mark.parametrize('replacement',['changed-bytes','outside-symlink'])
def test_git_index_flags_cannot_hide_public_ui_bytes_or_external_symlink(tmp_path,index_flag,replacement):
    run=synthetic_git(tmp_path)
    (tmp_path/'site').mkdir();path=tmp_path/'site/app.js';path.write_text('tracked original')
    run('add','.');run('commit','--quiet','-m','synthetic indexed source')
    head=run('rev-parse','HEAD').decode().strip()
    run('update-index',index_flag,'site/app.js')
    if replacement=='changed-bytes':path.write_text('hidden changed bytes')
    else:
        outside=tmp_path.parent/(tmp_path.name+'-outside.txt');outside.write_text('outside synthetic bytes')
        path.unlink();path.symlink_to(outside)
    assert not run('diff','--name-only','HEAD')
    with pytest.raises(BoundaryViolation):admission.require_clean_delivery_workspace(tmp_path,head,'reports/canonical-successor/TEST-coverage.json')
    assert registry.APPROVED_ADMISSIONS=={}
