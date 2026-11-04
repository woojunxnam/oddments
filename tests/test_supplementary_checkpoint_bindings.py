"""Exact supplementary retention is validated before a final16 binding is emitted."""
import copy
import json

import pytest

import supplementary_checkpoint_bindings as collector
import notes_held_sixteenth as held
import procedural_secondary_metadata as procedural
import phase11_secondary_metadata as phase11
import phase11_context38_metadata as context38
import test_procedural_secondary_metadata as ptests
import test_phase11_secondary_metadata as ftests
import test_phase11_context38_metadata as ctests
from test_procedural_secondary_metadata import fixture as procedural_fixture
from test_phase11_secondary_metadata import fixture as phase11_fixture
from test_phase11_context38_metadata import fixture as context38_fixture

FAMILIES=[('procedural_fixture',procedural,ptests),('phase11_fixture',phase11,ftests),
          ('context38_fixture',context38,ctests)]


def public_source(fixture,module,tests):
    root,state,report,primary,questions,collections=fixture
    tests.write(root,'site/practice-expansion/publication.json',{'additional_banks':[]})
    tests.write(root,'practice_expansion/2026-10-23/candidates/questions.json',{'questions':list(questions.values())})
    tests.commit(root)
    return fixture


@pytest.mark.parametrize('fixture_name,module,tests',FAMILIES)
def test_successful_consumers_bind_actual_queue_envelope_report_and_proof_bytes(request,fixture_name,module,tests):
    root,state,report,primary,questions,collections=public_source(request.getfixturevalue(fixture_name),module,tests)
    original=copy.deepcopy(primary)
    bindings={};sources=collector.validated_sources(root,primary,source_bindings=bindings)
    assert set(sources)==set(module.IDS)
    assert {module.STATE,tests.REPORT,tests.ENVELOPE,tests.SOURCE,tests.RAW}<=set(bindings)
    for path,digest in bindings.items():assert procedural.sha((root/path).read_bytes())==digest
    if module is context38:assert {context38.DISCLOSURE,context38.CHECKPOINT}<=set(bindings)
    assert all(source['canonical_release_credit']==0 and source['does_not_override_primary'] for source in sources.values())
    assert primary==original


@pytest.mark.parametrize('fixture_name,module,tests',FAMILIES)
def test_pending_queue_binds_verified_parent_context_without_reading_future_result(request,fixture_name,module,tests):
    fixture=public_source(request.getfixturevalue(fixture_name),module,tests)
    root,state,report,primary,_,_=fixture
    state['jobs'][0]['status']='LEASED';tests.save(root,state)
    (root/tests.REPORT).unlink();(root/tests.ENVELOPE).unlink()
    bindings={};sources=collector.validated_sources(root,primary,source_bindings=bindings)
    assert sources=={} and module.STATE in bindings
    assert tests.REPORT not in bindings and tests.ENVELOPE not in bindings


@pytest.mark.parametrize('fixture_name,module,tests',FAMILIES)
@pytest.mark.parametrize('mutation',['queue_uncommitted','report_bytes','envelope_bytes','proof_bytes','wrong_actor_rehashed'])
def test_bad_supplement_never_publishes_partial_binding_trace(request,fixture_name,module,tests,mutation):
    fixture=public_source(request.getfixturevalue(fixture_name),module,tests)
    root,state,report,primary,_,_=fixture
    if mutation=='queue_uncommitted':
        state['events'].append({'kind':'UNCOMMITTED'});tests.write(root,module.STATE,state)
    elif mutation=='wrong_actor_rehashed':
        report['actor_provenance']['actor_id']='/root'
        tests.save(root,state,report,refresh=True)
    else:
        path={'report_bytes':tests.REPORT,'envelope_bytes':tests.ENVELOPE,'proof_bytes':tests.RAW}[mutation]
        (root/path).write_bytes(b'Changed committed proof bytes')
        tests.commit(root)
    bindings={'existing':'untouched'}
    with pytest.raises(ValueError):collector.validated_sources(root,primary,source_bindings=bindings)
    assert bindings=={'existing':'untouched'}


def test_absent_all_three_states_is_exact_noop_without_public_config(tmp_path):
    bindings={'existing':'untouched'}
    assert collector.validated_sources(tmp_path,[],source_bindings=bindings)=={}
    held.bind_supplementary_checkpoints(tmp_path,bindings,[])
    assert bindings=={'existing':'untouched'}


def test_deleted_queue_changes_final_binding_instead_of_retaining_stale_result(procedural_fixture):
    root,state,report,primary,_,_=public_source(procedural_fixture,procedural,ptests)
    original={};held.bind_supplementary_checkpoints(root,original,primary)
    (root/procedural.STATE).unlink();ptests.commit(root)
    changed={};held.bind_supplementary_checkpoints(root,changed,primary)
    assert changed=={} and original!=changed


def test_exposure_disclosure_tamper_cannot_publish_new_trace(context38_fixture):
    root,state,report,primary,_,_=public_source(context38_fixture,context38,ctests)
    value=json.loads((root/context38.DISCLOSURE).read_bytes());value['primary_fresh_key_credit']=38
    ctests.write(root,context38.DISCLOSURE,value);ctests.commit(root)
    bindings={}
    with pytest.raises(ValueError):collector.validated_sources(root,primary,source_bindings=bindings)
    assert bindings=={}


def test_deleted_context_queue_with_retained_exposure_fails_closed(context38_fixture):
    root,state,report,primary,_,_=public_source(context38_fixture,context38,ctests)
    (root/context38.STATE).unlink();ctests.commit(root)
    bindings={}
    with pytest.raises(ValueError,match='Retained aggregate exposure'):
        held.bind_supplementary_checkpoints(root,bindings,primary)
    assert bindings=={}
