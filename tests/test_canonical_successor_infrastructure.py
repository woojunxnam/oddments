"""Synthetic boundary fixtures have no law or native admission/audit credit."""
import ast
import copy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import random
import re
import string
import subprocess
import unicodedata

import pytest

import canonical_successor as successor
import qa_common

ROOT=Path(__file__).resolve().parents[1]


def encoded(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()


def fixture_question(uid, family, stem):
    return {'question_id':uid,'family_id':family,'stem':stem,'question_type':'SBA',
        'choices':[{'id':'A','text':'Synthetic first choice'},{'id':'B','text':'Synthetic second choice'}],
        'correct_choice_ids':['A'],'verification_status':'AUDIT_PENDING','lifecycle_status':'AUDIT_PENDING',
        'audits':[],'final_adjudication':None}


def fixture_family(fid):
    return {'family_id':fid,'area':'SYNTHETIC','topic':'Boundary fixture','subtopic':'No legal conclusion',
        'primary_rule_ids':[],'secondary_rule_ids':[],'drug_required':False,'scenario_types':[],
        'common_traps':[],'target_difficulties':[],'target_item_types':['SBA'],
        'max_questions_in_final_bank':1,'current_candidate_count':1,'current_released_count':0}


@pytest.fixture
def plan():
    original=fixture_question('MA-Q-0001','ORIGINAL','Synthetic original boundary body')
    old_questions={original['question_id']:original}
    family={'matrix_id':'SYNTHETIC','profile_id':'SYNTHETIC','last_reviewed':'2026-11-05','families':[fixture_family('ORIGINAL')]}
    originals={'data/questions/ma-q-0001.json':encoded(original),successor.FAMILY:encoded(family),
        'site/notes/complete-notes.md':b'Unchanged synthetic note',
        'site/verified-law/delivery-holds.json':b'Unchanged synthetic hold',
        'site/generated/questions.json':b'Unchanged synthetic generated payload'}
    base={path:successor.Seal.of(raw) for path,raw in originals.items()}
    raws={};after_family=copy.deepcopy(family)
    for number in range(9000,9031):
        uid=f'MA-Q-{number:04d}';fid=f'SYNTHETIC_{number}'
        raws['data/questions/'+uid.lower()+'.json']=encoded(fixture_question(uid,fid,f'Synthetic boundary only {number}'))
        after_family['families'].append(fixture_family(fid))
    family_raw=encoded(after_family)
    additions={path:successor.Seal.of(raw) for path,raw in raws.items()}
    proposal=successor.Proposal(additions,base[successor.FAMILY],successor.Seal.of(family_raw))
    return {'base':base,'after':{**base,**additions,successor.FAMILY:proposal.family_after},'proposal':proposal,
        'questions':old_questions,'family':family,'family_raw':family_raw,'raws':raws,'originals':originals}


def inspect(plan,**changes):
    plan={**plan,**changes}
    return successor.verify_proposal(plan['base'],plan['after'],plan['proposal'],plan['questions'],plan['family'],
        plan['family_raw'],plan['raws'],frozen_anchor=plan['base'],
        original_question_raw={p:raw for p,raw in plan['originals'].items() if p.startswith('data/questions/')},
        original_family_raw=plan['originals'][successor.FAMILY])


def test_exact_synthetic_boundary_has_zero_audit_approval_or_admission_credit(plan):
    result=inspect(plan)
    assert len(result['new_question_ids'])==31
    assert result['activation']=='INFRASTRUCTURE_INACTIVE' and result['approval_credit']==result['native_audit_credit']==0
    assert successor.activation_assessment(boundary=result,approved=True,legacy_replay={'PASS':True})['activation_allowed'] is False


@pytest.mark.parametrize('path',['data/questions/ma-q-0001.json','site/notes/complete-notes.md',
    'site/verified-law/delivery-holds.json','site/generated/questions.json'])
def test_original_mutation_cannot_be_hidden_by_an_exact_addition_manifest(plan,path):
    plan['after'][path]=successor.Seal.of(b'Changed original')
    with pytest.raises(successor.BoundaryViolation):inspect(plan)


@pytest.mark.parametrize('path',['data/questions/../rules/x.json','data/questions/nested/x.json','data/x.json',
    'scripts/x.py','/tmp/x.json','data/questions/a\\b.json','data/questions/a\nx.json'])
def test_additions_cannot_escape_the_four_exact_direct_json_directories(plan,path):
    proposed=replace(plan['proposal'],additions={path:successor.Seal.of(b'{}')})
    with pytest.raises(successor.BoundaryViolation):inspect(plan,proposal=proposed)


def test_unlisted_missing_and_existing_file_additions_are_rejected(plan):
    after=dict(plan['after']);after['data/questions/extra.json']=successor.Seal.of(b'{}')
    with pytest.raises(successor.BoundaryViolation):inspect(plan,after=after)
    after=dict(plan['after']);del after['site/generated/questions.json']
    with pytest.raises(successor.BoundaryViolation):inspect(plan,after=after)
    proposal=replace(plan['proposal'],additions={**plan['proposal'].additions,'data/questions/ma-q-0001.json':plan['base']['data/questions/ma-q-0001.json']})
    with pytest.raises(successor.BoundaryViolation):inspect(plan,proposal=proposal)
    with pytest.raises(successor.BoundaryViolation):inspect(plan,proposal=replace(plan['proposal'],status='APPROVED'))


@pytest.mark.parametrize('mutate',[
    lambda d:d['families'][0].update(max_questions_in_final_bank=999),
    lambda d:d['families'][0].update(topic='Rebased old topic'),
    lambda d:d['families'][0].update(current_candidate_count=True),
    lambda d:d['families'].reverse(),
    lambda d:d['families'].append(copy.deepcopy(d['families'][0])),
    lambda d:d.update(last_reviewed='2026-99-99'),
])
def test_redeclaring_the_expected_family_hash_cannot_authorize_old_semantic_changes(plan,mutate):
    family=json.loads(plan['family_raw']);mutate(family);raw=encoded(family)
    proposal=replace(plan['proposal'],family_after=successor.Seal.of(raw))
    after={**plan['after'],successor.FAMILY:proposal.family_after}
    with pytest.raises(successor.BoundaryViolation):inspect(plan,proposal=proposal,after=after,family_raw=raw)


def test_old_question_semantics_cannot_be_substituted_behind_unchanged_seals(plan):
    questions=copy.deepcopy(plan['questions']);questions['MA-Q-0001']['stem']='Substituted original semantic body'
    with pytest.raises(successor.BoundaryViolation):inspect(plan,questions=questions)
    anchor=dict(plan['base']);anchor.pop('site/notes/complete-notes.md')
    with pytest.raises(successor.BoundaryViolation):successor.verify_preservation_anchor(plan['base'],anchor)


def test_original_body_cannot_be_reidentified_by_renaming_id_family_and_choices(plan):
    question=copy.deepcopy(plan['questions']['MA-Q-0001']);question.update(question_id='MA-Q-9000',family_id='SYNTHETIC_9000')
    raw=encoded(question);path='data/questions/ma-q-9000.json';seal=successor.Seal.of(raw)
    proposal=replace(plan['proposal'],additions={**plan['proposal'].additions,path:seal})
    with pytest.raises(successor.BoundaryViolation):inspect(plan,proposal=proposal,after={**plan['after'],path:seal},raws={**plan['raws'],path:raw})


def test_duplicate_json_property_and_missing_semantic_document_rejected(plan):
    with pytest.raises(successor.BoundaryViolation):successor.strict_json(b'{"same":1,"same":2}')
    raws=dict(plan['raws']);raws.pop(next(iter(raws)))
    with pytest.raises(successor.BoundaryViolation):inspect(plan,raws=raws)


@pytest.mark.parametrize('payload',[b'{}',b'{"approved":true}',b'{"activation_allowed":true}'])
def test_any_activation_enrollment_is_denied_even_when_it_claims_approval(tmp_path,payload):
    target=tmp_path/successor.ACTIVATION_PATH;target.parent.mkdir(parents=True);target.write_bytes(payload)
    with pytest.raises(successor.BoundaryViolation,match='unsupported'):successor.inactive_status(tmp_path)


def test_missing_activation_is_inactive_and_symlink_activation_cannot_be_ignored(tmp_path):
    assert successor.inactive_status(tmp_path)['canonical_admission_credit']==0
    target=tmp_path/successor.ACTIVATION_PATH;target.parent.mkdir(parents=True);target.symlink_to(tmp_path/'missing')
    with pytest.raises(successor.BoundaryViolation):successor.inactive_status(tmp_path)


def test_source_reader_rejects_missing_symlink_duplicate_and_escaping_paths(tmp_path):
    (tmp_path/'actual').write_bytes(b'preimage');(tmp_path/'linked').symlink_to(tmp_path/'actual')
    assert successor.read_current_preimages(tmp_path,['actual'])=={'actual':b'preimage'}
    for paths in [['missing'],['linked'],['actual','actual'],['../escape']]:
        with pytest.raises(successor.BoundaryViolation):successor.read_current_preimages(tmp_path,paths)


def test_committed_preimages_are_read_without_repository_writes_or_reenrollment(tmp_path):
    subprocess.run(['git','init','--quiet',str(tmp_path)],check=True)
    subprocess.run(['git','config','user.name','Synthetic Test'],cwd=tmp_path,check=True)
    subprocess.run(['git','config','user.email','synthetic@example.invalid'],cwd=tmp_path,check=True)
    (tmp_path/'source.json').write_bytes(b'{"synthetic":true}\n')
    subprocess.run(['git','add','source.json'],cwd=tmp_path,check=True)
    subprocess.run(['git','commit','--quiet','-m','synthetic immutable source'],cwd=tmp_path,check=True)
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=tmp_path,text=True).strip()
    before=subprocess.check_output(['git','status','--porcelain'],cwd=tmp_path)
    original=successor.read_committed_preimages(tmp_path,commit,['source.json'])
    assert original=={'source.json':b'{"synthetic":true}\n'}
    assert subprocess.check_output(['git','status','--porcelain'],cwd=tmp_path)==before
    with pytest.raises(successor.BoundaryViolation):successor.read_committed_preimages(tmp_path,'HEAD',['source.json'])
    with pytest.raises(successor.BoundaryViolation):successor.read_committed_preimages(tmp_path,commit,['missing-object'])


def actual_committed_note_output_seals():
    # Current committed output bytes, not caller before/after hashes. This checks
    # a boundary only; Git HEAD selection is not an admission authorization.
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    paths=['site/notes/complete-notes.md','site/notes/build.json','site/notes/content.js']
    raw=successor.read_committed_preimages(ROOT,commit,paths)
    return {path:successor.Seal.of(value) for path,value in raw.items()}


def check_actual_note_context(*args):
    return successor.note_source_context_only(*args,trusted_output_seals=actual_committed_note_output_seals())


def test_actual_note16_context_preserves_bindings_outputs_claim_ledger_and_hold():
    raw=(ROOT/'revisions/notes/protected-migration-held-n1.json').read_bytes();parent=json.loads(raw)
    outputs={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['site/notes/complete-notes.md','site/notes/build.json','site/notes/content.js']}
    claims=hashlib.sha256((ROOT/'reports/full-corpus-review/notes-unit-ledger.jsonl').read_bytes()).hexdigest()
    additions={'data/questions/ma-q-9000.json':'a'*64}
    result=check_actual_note_context(raw,parent['source_bindings'],dict(parent['source_bindings']),outputs,dict(outputs),claims,claims,additions,additions)
    assert result['note_body_delta']==result['note_legal_PASS_credit']==0
    with pytest.raises(successor.BoundaryViolation):check_actual_note_context(raw,parent['source_bindings'],{},outputs,outputs,claims,claims,additions,additions)
    with pytest.raises(successor.BoundaryViolation):check_actual_note_context(raw,parent['source_bindings'],dict(parent['source_bindings']),outputs,{**outputs,'site/notes/build.json':'b'*64},claims,claims,additions,additions)


def test_hash_context_enrollment_dependencies_must_be_acyclic():
    assert successor.require_acyclic_hash_dependencies({'base':[],'manifest':['base'],'context':['manifest'],'enrollment':['context']})
    for graph in [{'self':['self']},{'manifest':['context'],'context':['manifest']},{'manifest':['missing']}]:
        with pytest.raises(successor.BoundaryViolation):successor.require_acyclic_hash_dependencies(graph)


def old_normalize(text,normalize_numbers=False):
    text=text.casefold()
    if normalize_numbers:text=re.sub(r'\b\d+(?:\.\d+)?\b','<num>',text)
    return ' '.join(re.sub(r'[^a-z0-9<>]+',' ',text).split())


def test_unicode_preserves_distinct_legal_meanings_names_and_identical_duplicates():
    examples=['약사는 처방을 확인해야 합니다.','직원은 임상 판단을 대신할 수 없습니다.','기록은 보관해야 합니다.','환자에게 즉시 알려야 합니다.']
    assert set(map(old_normalize,examples))=={''}
    assert len(set(map(qa_common.normalize_text,examples)))==4
    assert qa_common.normalize_text(examples[0])==qa_common.normalize_text(examples[0])
    assert qa_common.normalize_text('조제할 수 있다')!=qa_common.normalize_text('조제할 수 없다')
    assert qa_common.normalize_text('김민수')!=qa_common.normalize_text('김민서')
    assert qa_common.normalize_text('105 CMR 700')!=qa_common.normalize_text('247 CMR 700')
    assert qa_common.normalize_text('조제')==qa_common.normalize_text(unicodedata.normalize('NFD','조제'))
    assert qa_common.normalize_text('café')==qa_common.normalize_text('cafe\u0301')
    assert qa_common.normalize_text('café')!=qa_common.normalize_text('cafe')


def test_ascii_and_number_masking_compatibility():
    randomizer=random.Random(336);inputs=[string.printable,'A B C <> <num> 1301.76(b)']
    inputs+=[''.join(randomizer.choice(string.printable) for _ in range(80)) for _ in range(400)]
    for text in inputs:
        for numeric in [False,True]:assert qa_common.normalize_text(text,numeric)==old_normalize(text,numeric)


def test_actual397_objects_audit_hash_function_and_question_hashes_remain_identical():
    payload=json.loads((ROOT/'site/generated/questions.json').read_bytes())
    assert len(payload['questions'])==397
    tree=ast.parse((ROOT/'scripts/qa_common.py').read_bytes())
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='question_audit_hash')
    assert hashlib.sha256(ast.dump(function,include_attributes=False).encode()).hexdigest()=='587f33447479ffd74adbe7403288d32102f18bfc27223d87d88a604cd793c4f5'
    for question in payload['questions']:assert qa_common.question_audit_hash(question)==question['question_content_hash']
    assert successor.inactive_status(ROOT)['activation_allowed'] is False


def test_existing_guard_and_producer_sources_are_unchanged():
    expected={'scripts/verify_representative_protected.py':'6c63e6ac6f564cc496c1bd6ff030e529fc6106e8e96706afd0deab211c374212',
        'scripts/canonical_q0012_withdrawal.py':'a1a7174f29b56f5c7ef4596700ee9e1c7c3e9749fd95e5db9d8af6ac787a2565',
        'scripts/notes_held_sixteenth.py':'f7b040f162716c1a9e1aee88d80b8dc0e2d55608a713fe04f3b0baed617fb537',
        'scripts/generate_artifacts.py':'69e54f32157b1dab8e54d887c85bd13445970486d3e512976cc628210e22f2b6'}
    for path,digest in expected.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest


@pytest.mark.parametrize('count',[29,41])
def test_ordinary_initial_batch_bounds_are_not_relaxed(plan,count):
    raws={}
    for number in range(9000,9000+count):
        uid=f'MA-Q-{number:04d}'
        raws['data/questions/'+uid.lower()+'.json']=encoded(fixture_question(uid,f'SYNTHETIC_{number}',f'Synthetic only {number}'))
    with pytest.raises(successor.BoundaryViolation,match='30–40'):successor.verify_added_questions(plan['questions'],raws)


def test_unicode_similarity_uses_meaningful_korean_tokens_and_retains_true_duplicates():
    first='약사는 처방을 확인해야 합니다';second='직원은 임상 판단을 대신할 수 없습니다'
    assert qa_common.token_jaccard(first,second)<1.0
    assert qa_common.token_jaccard(first,first)==1.0
    assert qa_common.token_jaccard('Rule 30 days','Rule 90 days')==1.0


def test_actual_original_inventory_quarantines_and_delivery_hold_hashes_are_unchanged():
    questions=[json.loads(path.read_bytes()) for path in (ROOT/'data/questions').glob('*.json')]
    assert len(questions)==439
    released={q['question_id'] for q in questions if successor.released(q)}
    assert len(released)==397 and not {'MA-Q-0012','MA-Q-0028'} & released
    payload=json.loads((ROOT/'site/generated/questions.json').read_bytes())
    hashes={q['question_id']:q['question_content_hash'] for q in payload['questions']}
    holds=json.loads((ROOT/'site/verified-law/delivery-holds.json').read_bytes())['holds']
    assert len(holds)==16
    assert all(hashes[h['question_id']]==h['question_content_hash'] for h in holds)


def test_published_note16_parent_and_required_output_inventory_cannot_be_forged():
    raw=(ROOT/'revisions/notes/protected-migration-held-n1.json').read_bytes();parent=json.loads(raw)
    outputs={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['site/notes/complete-notes.md','site/notes/build.json','site/notes/content.js']}
    claims=parent['source_bindings']['reports/full-corpus-review/notes-unit-ledger.jsonl'];added={'data/questions/ma-q-9000.json':'a'*64}
    forged=copy.deepcopy(parent);forged['new_markdown_sha256']='b'*64
    with pytest.raises(successor.BoundaryViolation):check_actual_note_context(encoded(forged),parent['source_bindings'],parent['source_bindings'],outputs,outputs,claims,claims,added,added)
    with pytest.raises(successor.BoundaryViolation):check_actual_note_context(raw,parent['source_bindings'],parent['source_bindings'],{}, {},claims,claims,added,added)
    with pytest.raises(successor.BoundaryViolation):check_actual_note_context(raw,parent['source_bindings'],parent['source_bindings'],outputs,outputs,'b'*64,'b'*64,added,added)


def test_same_forged_content_js_before_after_hash_or_omitted_trusted_seal_is_rejected():
    raw=(ROOT/'revisions/notes/protected-migration-held-n1.json').read_bytes();parent=json.loads(raw)
    trusted=actual_committed_note_output_seals();outputs={path:seal.sha256 for path,seal in trusted.items()}
    claims=parent['source_bindings']['reports/full-corpus-review/notes-unit-ledger.jsonl'];added={'data/questions/ma-q-9000.json':'a'*64}
    forged={**outputs,'site/notes/content.js':'b'*64}
    with pytest.raises(successor.BoundaryViolation,match='trusted immutable'):
        successor.note_source_context_only(raw,parent['source_bindings'],parent['source_bindings'],forged,forged,claims,claims,added,added,trusted_output_seals=trusted)
    omitted={path:seal for path,seal in trusted.items() if path!='site/notes/content.js'}
    with pytest.raises(successor.BoundaryViolation,match='inventory'):
        successor.note_source_context_only(raw,parent['source_bindings'],parent['source_bindings'],outputs,outputs,claims,claims,added,added,trusted_output_seals=omitted)
    with pytest.raises(successor.BoundaryViolation,match='preimages are required'):
        successor.note_source_context_only(raw,parent['source_bindings'],parent['source_bindings'],outputs,outputs,claims,claims,added,added)


@pytest.fixture
def committed_source_modes(tmp_path):
    def git(*args):
        return subprocess.check_output(['git','-C',str(tmp_path),*args])
    git('init','--quiet');git('config','user.name','Synthetic Test');git('config','user.email','synthetic@example.invalid')
    (tmp_path/'actual.json').write_bytes(b'{"synthetic":true}\n')
    (tmp_path/'literal[1].json').write_bytes(b'{"literal":true}\n')
    (tmp_path/'한글.json').write_bytes(b'{"unicode":true}\n')
    (tmp_path/'script.py').write_bytes(b'# synthetic executable source\n');(tmp_path/'script.py').chmod(0o755)
    (tmp_path/'nested').mkdir();(tmp_path/'nested/item.json').write_bytes(b'{"nested":true}\n')
    (tmp_path/'linked.json').symlink_to('actual.json')
    (tmp_path/'linked-dir').symlink_to('nested',target_is_directory=True)
    git('add','.');git('commit','--quiet','-m','synthetic source modes')
    first=git('rev-parse','HEAD').decode().strip()
    git('update-index','--add','--cacheinfo','160000,'+first+',vendor')
    git('commit','--quiet','-m','synthetic gitlink without external repository')
    return tmp_path,git('rev-parse','HEAD').decode().strip()


@pytest.mark.parametrize('path',['linked.json','linked-dir/item.json','nested','vendor'])
def test_git_source_reader_rejects_final_intermediate_symlink_tree_and_gitlink(committed_source_modes,path):
    root,commit=committed_source_modes
    with pytest.raises(successor.BoundaryViolation):successor.read_committed_preimages(root,commit,[path])


def test_git_source_reader_accepts_regular_and_executable_literal_unicode_paths(committed_source_modes):
    root,commit=committed_source_modes
    paths=['actual.json','script.py','literal[1].json','한글.json','nested/item.json']
    assert successor.read_committed_preimages(root,commit,paths)=={path:(root/path).read_bytes() for path in paths}
