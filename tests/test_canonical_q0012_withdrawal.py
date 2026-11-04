"""Bounded safety withdrawal tests; no new legal/realism audit is generated."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import canonical_q0012_withdrawal as guard
import verify_representative_protected as protected


def encoded(value):
    return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()


@pytest.fixture(scope='module')
def spec():
    return json.loads((ROOT/guard.MANIFEST).read_bytes())


@pytest.fixture
def sandbox(tmp_path,spec):
    # No .git directory, live note queue, note review consumer, or worker Git
    # object is needed: exact pinned archive bytes are sufficient for this hold.
    shutil.copytree(ROOT/'data/questions',tmp_path/'data/questions')
    shutil.copytree(ROOT/guard.PREFIX,tmp_path/guard.PREFIX)
    paths={guard.FAMILY,guard.PREVIEW,guard.BASELINE}
    paths.update(r['preimage_path'] for r in spec['changes'].values())
    for relative in paths:
        target=tmp_path/relative;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/relative,target)
    return tmp_path


def alter(root,path,change):
    value=json.loads((root/path).read_bytes());change(value)
    (root/path).write_bytes(encoded(value))


def test_exact_decoder_authenticates_original_main_bytes_and_preserves_audits(spec,sandbox):
    originals=guard.validate(sandbox)
    for relative in guard.PATHS:
        raw=(sandbox/relative).read_bytes()
        assert protected.migrated_baseline_bytes(sandbox,relative,raw)==originals[relative]
    before=json.loads(originals[guard.QUESTION]);after=json.loads((sandbox/guard.QUESTION).read_bytes())
    assert guard.question_audit_hash(before)==guard.question_audit_hash(after)==guard.AUDIT_HASH
    assert after['audits']==before['audits'] and after['independent_audit_status']=='PASSED'
    assert after['correct_choice_ids']==before['correct_choice_ids']==['B']
    assert after['final_adjudication']==before['final_adjudication']
    assert not (sandbox/'reports/full-corpus-review/independent-notes-work-queue.json').exists()
    assert not (sandbox/'.git').exists()


def test_all_1781_protected_files_pass_with_original_baseline_and_fourteen_guards():
    baseline=json.loads((ROOT/guard.BASELINE).read_bytes())
    result=protected.verify(baseline,ROOT)
    assert result['files']==1781 and result['bytes']==60969461
    source=(ROOT/'scripts/verify_representative_protected.py').read_text()
    old=source[source.index("    fourteenth_path=root/"):]
    assert guard.sha(old.encode())=='ba8f3ae371b9cacf05e896064ebd3b6c170f151e9a877ca3b09113c6ca250300'
    assert guard.sha((ROOT/'revisions/notes/protected-migration-independent-notes-wave3.json').read_bytes())==\
        '53537abd57b56bc8a839901a766de916c7a06b4275beba8bd2ebf435adf0353e'


def test_retained_inputs_are_actual_current_committed_bytes(spec):
    paths={guard.BASELINE,spec['config']['path'],spec['withdrawal_report']['path']}
    paths.update(r['preimage_path'] for r in spec['changes'].values())
    paths.update(spec['source_bindings'])
    for relative in paths:
        assert (ROOT/relative).read_bytes()==subprocess.check_output(['git','-C',str(ROOT),'show','HEAD:'+relative])
    assert spec['same_hash_release_restoration_allowed'] is False
    for key in ['canonical_release_credit','question_audit_credit','author_review_credit']:
        assert type(spec[key]) is int and spec[key]==0


@pytest.mark.parametrize('change',[
    'old_released_bytes','verification_restore','lifecycle_restore','stem_unicode','choice_unicode',
    'key','explanation','audits','adjudication','passed_history','unrelated_metadata',
    'same_hash_added_keep_then_restore',
])
def test_q0012_content_history_or_unsafe_release_restore_is_rejected(sandbox,spec,change):
    path=sandbox/guard.QUESTION
    if change=='old_released_bytes':
        path.write_bytes((sandbox/spec['changes'][guard.QUESTION]['preimage_path']).read_bytes())
    else:
        def mutate(q):
            if change=='verification_restore':q['verification_status']='RELEASED'
            elif change=='lifecycle_restore':q['lifecycle_status']='RELEASED'
            elif change=='stem_unicode':q['stem']+=' 한글 본문 변조'
            elif change=='choice_unicode':q['choices'][3]['text']+=' 한글 보기 변조'
            elif change=='key':q['correct_choice_ids']=['D']
            elif change=='explanation':q['explanation']['choice_analysis']['D']='새 한국어 해설'
            elif change=='audits':q['audits']=[]
            elif change=='adjudication':q['final_adjudication']['decision']='DELETE'
            elif change=='passed_history':q['independent_audit_status']='PENDING'
            elif change=='unrelated_metadata':q['last_legal_review']='2026-11-04'
            else:
                # A temporary negative fixture, never a repository audit record.
                q['audits'].append('FABRICATED_TEST_KEEP_DOES_NOT_CLEAR_KNOWN_DEFECT')
                q['verification_status']=q['lifecycle_status']='RELEASED'
        alter(sandbox,guard.QUESTION,mutate)
    with pytest.raises(ValueError):guard.validate(sandbox)


@pytest.mark.parametrize('change',['restore_count','candidate','other_family','scope','boolean'])
def test_family_change_is_exactly_one_released_count_decrement(sandbox,change):
    def mutate(value):
        target=next(r for r in value['families']if r['family_id']==guard.FAMILY_ID)
        if change=='restore_count':target['current_released_count']=1
        elif change=='candidate':target['current_candidate_count']=0
        elif change=='other_family':value['families'][0]['current_released_count']+=1
        elif change=='boolean':target['current_released_count']=False
        else:target['max_questions_in_final_bank']=3
    alter(sandbox,guard.FAMILY,mutate)
    with pytest.raises(ValueError):guard.validate(sandbox)


@pytest.mark.parametrize('change',['restore','add_q0012','add_q0028','add_new','remove_other','reorder','audit_history'])
def test_preview_cannot_import_any_question_or_change_preserved_history(sandbox,spec,change):
    if change=='restore':
        (sandbox/guard.PREVIEW).write_bytes((sandbox/spec['changes'][guard.PREVIEW]['preimage_path']).read_bytes())
    else:
        def mutate(value):
            if change=='add_q0012':value['question_ids'].append(guard.QID)
            elif change=='add_q0028':value['question_ids'].append('MA-Q-0028')
            elif change=='add_new':value['question_ids'].append('MA-Q-9999')
            elif change=='remove_other':value['question_ids'].pop()
            elif change=='reorder':value['question_ids'].reverse()
            else:value['source_audits']=[]
        alter(sandbox,guard.PREVIEW,mutate)
    with pytest.raises(ValueError):guard.validate(sandbox)


@pytest.mark.parametrize('change',['other_question','other_status','q0028_release','new_file','deleted_file'])
def test_other_438_canonical_questions_and_inventory_are_immutable(sandbox,change):
    relative='data/questions/ma-q-0001.json'
    if change=='new_file':(sandbox/'data/questions/ma-q-9999.json').write_bytes(b'{}\n')
    elif change=='deleted_file':(sandbox/relative).unlink()
    elif change=='q0028_release':
        alter(sandbox,'data/questions/ma-q-0028.json',lambda q:q.update(verification_status='RELEASED',lifecycle_status='RELEASED'))
    elif change=='other_status':alter(sandbox,relative,lambda q:q.update(verification_status='HOLD'))
    else:alter(sandbox,relative,lambda q:q.update(stem=q['stem']+' 원문변조'))
    with pytest.raises(ValueError):guard.validate(sandbox)


@pytest.mark.parametrize('change',['path','restore_permission','credit','boolean_credit','baseline','source_hash'])
def test_manifest_cannot_be_rebound_to_expand_scope_or_grant_credit(sandbox,change):
    def mutate(value):
        if change=='path':value['protected_paths'].append('data/audits/new.json')
        elif change=='restore_permission':value['same_hash_release_restoration_allowed']=True
        elif change=='credit':value['canonical_release_credit']=1
        elif change=='boolean_credit':value['question_audit_credit']=False
        elif change=='baseline':value['baseline_raw_sha256']='0'*64
        else:value['source_bindings']={}
    alter(sandbox,guard.MANIFEST,mutate)
    with pytest.raises(ValueError):guard.validate(sandbox)


def test_missing_manifest_or_baseline_does_not_restore_old_release_acceptance(sandbox):
    (sandbox/guard.MANIFEST).unlink()
    with pytest.raises(ValueError):
        protected.migrated_baseline_bytes(sandbox,guard.QUESTION,(sandbox/guard.QUESTION).read_bytes())


def test_decoder_cannot_expand_scope_or_accept_another_current_payload(sandbox):
    with pytest.raises(ValueError,match='expands protected scope'):
        guard.decode(sandbox,'data/questions/ma-q-0001.json',b'{}')
    with pytest.raises(ValueError,match='different current bytes'):
        guard.decode(sandbox,guard.QUESTION,b'{}')


def test_changed_preimage_or_original_baseline_is_rejected(sandbox,spec):
    relative=spec['changes'][guard.QUESTION]['preimage_path']
    (sandbox/relative).write_bytes((sandbox/relative).read_bytes()+b'\n')
    with pytest.raises(ValueError):guard.validate(sandbox)


@pytest.mark.parametrize('change',['actor','session','stage','canonical','credit','boolean_credit',
                                  'event','job','row_scope','row_key','visible_text'])
def test_cause_provenance_and_local_not_whole_question_scope_cannot_be_forged(spec,change):
    cause=spec['cause']
    values={k:json.loads((ROOT/cause[k]['path']).read_bytes()) for k in
            ('attestation','result','report','alignment','visible_packet')}
    before=json.loads((ROOT/spec['changes'][guard.QUESTION]['preimage_path']).read_bytes())
    row=next(r for r in values['alignment']['records']if r['question_id']==guard.QID)
    if change=='actor':values['report']['actor_provenance']['actor_id']='/root/wrong'
    elif change=='session':values['report']['auditor_instance']='invented-independent-session'
    elif change=='stage':values['report']['stage']='canonical-positive-audit'
    elif change=='canonical':values['report']['canonical_audit']=True
    elif change=='credit':values['report']['question_audit_credit']=1
    elif change=='boolean_credit':values['report']['question_audit_credit']=False
    elif change=='event':values['attestation']['events'][1]['worker_commit']='0'*40
    elif change=='job':values['attestation']['job']['status']='LEASED'
    elif change=='row_scope':row['full_question_key_assessment']='YES'
    elif change=='row_key':row['stored_key']=['D']
    else:
        p=next(r for r in values['visible_packet']['records']if r['question_id']==guard.QID)
        p['original_visible_content']['explanation']['choice_analysis']['D']='다른 해설'
    with pytest.raises(ValueError):
        guard.validate_cause_contents(values['attestation'],values['result'],values['report'],
                                       values['alignment'],values['visible_packet'],before)


@pytest.mark.parametrize('which',['report','alignment','result','visible_packet','attestation','authority',
                                 'local_projection','source_manifest','controller_safety_scope',
                                 'config','withdrawal_report'])
def test_retained_cause_raw_payload_tamper_fails_closed(sandbox,spec,which):
    binding=(spec['cause']['authorities'][0]if which=='authority'else
             spec['cause'][which]if which in spec['cause']else spec[which])
    path=sandbox/binding['path'];path.write_bytes(path.read_bytes()+b'\n')
    with pytest.raises(ValueError):guard.validate(sandbox)


def test_original_1781_file_baseline_cannot_be_rewritten(sandbox):
    alter(sandbox,guard.BASELINE,lambda b:b['files'][0].update(sha256='0'*64))
    with pytest.raises(ValueError):guard.validate(sandbox)


def test_false_withdrawal_report_assertion_cannot_be_accepted(sandbox,spec):
    alter(sandbox,spec['withdrawal_report']['path'],lambda r:r['assertions'].update(hash_unchanged=False))
    with pytest.raises(ValueError):guard.validate(sandbox)
