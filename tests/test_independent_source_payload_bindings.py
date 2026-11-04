"""Actual retrieval logs retain failed attempts without counting them as law."""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_full_corpus_review import validate_independent_source_bytes


def report():
    return json.loads((ROOT/'reports/full-corpus-review/independent-phase6-e-review.json').read_bytes())


def test_actual_primary_raw_bindings_and_unused_failed_attempts_remain_verifiable_and_separate():
    data=report();original=copy.deepcopy(data)
    for source in data['sources']:
        validate_independent_source_bytes(source,ROOT)
    unused={s['source_id'] for s in data['sources'] if not s['used_as_law']}
    assert unused=={'112-24Bhalf','94c-19B','nabp-live'}
    used={a['authority'] for r in data['records'] for a in r['legal_review']['authorities']}
    assert not used&unused
    assert data==original


def test_historical_original_raw_sha_without_a_retained_path_is_provenance_only():
    data=json.loads((ROOT/'reports/full-corpus-review/wave2-independent-review.json').read_bytes())
    source=next(s for s in data['sources'] if 'raw_sha256' in s and 'raw_path' not in s)
    assert source['evidence_path'] and source['evidence_sha256']!=source['raw_sha256']
    validate_independent_source_bytes(source,ROOT)


@pytest.mark.parametrize('defect',[None,'redistribution_claim','missing_memo'])
def test_declared_copyrighted_private_raw_is_never_read_as_a_public_repository_payload(defect):
    data=json.loads((ROOT/'reports/full-corpus-review/independent-phase4-h-review.json').read_bytes())
    source=next(s for s in data['sources'] if s.get('public_raw_redistribution') is False)
    assert Path(source['raw_path']).is_absolute() and 'memo' in source['public_evidence_mode']
    if defect=='redistribution_claim':source['public_raw_redistribution']=True
    elif defect=='missing_memo':source.pop('evidence_path');source.pop('evidence_sha256')
    if defect:
        with pytest.raises(ValueError):validate_independent_source_bytes(source,ROOT)
    else:validate_independent_source_bytes(source,ROOT)


@pytest.mark.parametrize('defect',['changed_raw_sha','missing_raw_sha','partial_second_alias','missing_all','unsafe_path'])
def test_alternative_field_names_do_not_allow_missing_changed_or_unsafe_evidence(defect):
    source=copy.deepcopy(report()['sources'][1])
    if defect=='changed_raw_sha':source['raw_sha256']='0'*64
    elif defect=='missing_raw_sha':source.pop('raw_sha256')
    elif defect=='partial_second_alias':source['evidence_path']=source['raw_path']
    elif defect=='missing_all':source.pop('raw_path');source.pop('raw_sha256')
    else:source['raw_path']='../outside.txt'
    with pytest.raises(ValueError):validate_independent_source_bytes(source,ROOT)
