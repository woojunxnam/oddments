"""Only two actual SHA fields can evolve; scope and original202 defaults stay fixed."""
import copy
import json

import pytest

import notes_published15_closure as c
import phase11_context38_metadata as context38
from test_notes_published15_closure import put,commit,git


@pytest.fixture
def config_fixture(tmp_path,monkeypatch):
    root=tmp_path/'repo';root.mkdir();git(root,'init','-q')
    git(root,'config','user.name','Synthetic publication wrapper')
    git(root,'config','user.email','fixture@example.invalid')
    defaults=['SYNTHETIC-%03d'%i for i in range(202)]
    old_selection=dict(recommended_ids=defaults,archive_review_notices=[],holds=[],safety_holds=[])
    bank=dict(questions=[dict(question_id=qid,correct_choice_ids=['A'])for qid in defaults],
              source_authoring_hashes={'archive-notices':'original'})
    config=dict(enabled=True,published_total=202,canonical_release_policy_unchanged=True,
                additional_banks=[dict(path='practice_expansion/other/questions.json',sha256='unchanged',enabled=True),
                                  dict(path=c.REPRESENTATIVE_BANK,sha256=c.sha(c.encoded(bank)),question_count=202)],
                representative_selection=dict(path=c.REPRESENTATIVE_SELECTION,sha256=c.sha(c.encoded(old_selection))))
    original=copy.deepcopy(config);old_files={c.PUBLICATION_CONFIG:c.encoded(config),
        c.REPRESENTATIVE_BANK:c.encoded(bank),c.REPRESENTATIVE_SELECTION:c.encoded(old_selection)}
    files={};preimages={}
    for relative,raw in old_files.items():
        destination=c.PREIMAGES+'synthetic/'+relative;put(root,destination,raw)
        files[relative]={'raw_sha256':c.sha(raw)};preimages[relative]={'path':destination,'raw_sha256':c.sha(raw)}
    selection=copy.deepcopy(old_selection);selection['archive_review_notices']=[dict(question_ids=['ARCHIVE-ONLY'])]
    bank['source_authoring_hashes']['archive-notices']='updated'
    config['representative_selection']['sha256']=c.sha(c.encoded(selection))
    config['additional_banks'][1]['sha256']=c.sha(c.encoded(bank))
    put(root,c.PUBLICATION_CONFIG,config);put(root,c.REPRESENTATIVE_BANK,bank);put(root,c.REPRESENTATIVE_SELECTION,selection)
    commit(root,'synthetic exact two current digest changes')
    records=[dict(question_id=qid,legal_review=dict(verdict='KEEP',existing_answer_correct='YES'),
                  realism_review=dict(verdict='PASS'))for qid in defaults]
    validated=dict(primary_records=records,supplementary_sources={})
    # The actual bank/native proof is exercised by test_notes_archive_wrapper;
    # this stub isolates the new coupled-config/default-safety boundary.
    monkeypatch.setattr(c,'validate_archive_notice_wrapper',lambda *a:validated)
    return root,dict(full_source_files=files,retained_preimages=preimages),config,selection,bank,validated,original


def save(config_fixture):
    root,closure,config,selection,bank,validated,original=config_fixture
    put(root,c.PUBLICATION_CONFIG,config);put(root,c.REPRESENTATIVE_SELECTION,selection);put(root,c.REPRESENTATIVE_BANK,bank)
    commit(root,'synthetic publication attack or allowed binding')


def test_only_two_actual_sha_changes_preserve_ordered202_defaults_and_config(config_fixture):
    root,closure,config,selection,bank,validated,original=config_fixture
    c.validate_publication_config(root,closure)
    assert json.loads(c.old_bytes(root,closure,c.PUBLICATION_CONFIG))==original
    assert len(selection['recommended_ids'])==202


@pytest.mark.parametrize('mutation',['selection_sha','bank_sha','selection_path','bank_path','new_bank',
    'bank_order','bank_enabled','scope','boolean_integer','count_float','unknown_field',
    'default_drop','default_add','default_order','default_replace','stale_bank_data','old_digest'])
def test_scope_default_or_unbound_digest_change_is_rejected(config_fixture,mutation):
    root,closure,config,selection,bank,validated,original=config_fixture
    if mutation=='selection_sha':config['representative_selection']['sha256']='stale'
    elif mutation=='bank_sha':config['additional_banks'][1]['sha256']='stale'
    elif mutation=='selection_path':config['representative_selection']['path']='practice_expansion/unrelated/selection.json'
    elif mutation=='bank_path':config['additional_banks'][1]['path']='practice_expansion/unrelated/questions.json'
    elif mutation=='new_bank':config['additional_banks'].append(copy.deepcopy(config['additional_banks'][0]))
    elif mutation=='bank_order':config['additional_banks'].reverse()
    elif mutation=='bank_enabled':config['additional_banks'][0]['enabled']=False
    elif mutation=='scope':config['enabled']=False
    elif mutation=='boolean_integer':config['canonical_release_policy_unchanged']=1
    elif mutation=='count_float':config['published_total']=202.0
    elif mutation=='unknown_field':config['canonical_release_credit']=1
    elif mutation=='stale_bank_data':bank['questions'][0]['correct_choice_ids']=['B']
    elif mutation=='old_digest':closure['full_source_files'][c.REPRESENTATIVE_SELECTION]['raw_sha256']='wrong-old-digest'
    else:
        if mutation=='default_drop':selection['recommended_ids'].pop()
        elif mutation=='default_add':selection['recommended_ids'].append('NEW-DEFAULT')
        elif mutation=='default_replace':selection['recommended_ids'][0]='OTHER-DEFAULT'
        else:selection['recommended_ids'].reverse()
        config['representative_selection']['sha256']=c.sha(c.encoded(selection))
    if mutation!='old_digest':save(config_fixture)
    with pytest.raises(ValueError):c.validate_publication_config(root,closure)


def test_existing_native_bank_guard_cannot_be_bypassed_with_a_correct_digest(config_fixture,monkeypatch):
    root,closure,*_=config_fixture
    def invalid(*a):raise ValueError('Actual bank or native warning proof rejected')
    monkeypatch.setattr(c,'validate_archive_notice_wrapper',invalid)
    with pytest.raises(ValueError,match='native warning'):c.validate_publication_config(root,closure)


@pytest.mark.parametrize('field',['wrong_key','legal_hold','realism_fail'])
def test_known_negative_cannot_remain_in_the_unchanged202_default_list(config_fixture,field):
    root,closure,config,selection,bank,validated,original=config_fixture
    row=validated['primary_records'][0]
    if field=='wrong_key':row['legal_review']['existing_answer_correct']='NO'
    elif field=='legal_hold':row['legal_review']['verdict']='HOLD'
    else:row['realism_review']['verdict']='FAIL'
    with pytest.raises(ValueError,match='Uncontained independent finding'):c.validate_publication_config(root,closure)


def test_context_conditioned_default_exclusion_survives_exact_two_hash_updates(config_fixture,monkeypatch):
    root,closure,config,selection,bank,validated,original=config_fixture
    put(root,context38.STATE,{'synthetic_already_validated_context':True});commit(root,'synthetic strict-context boundary')
    monkeypatch.setattr(context38,'IDS',[selection['recommended_ids'][0]])
    with pytest.raises(ValueError,match='Context-conditioned'):c.validate_publication_config(root,closure)
