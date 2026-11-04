"""Citation corrections cannot alter preserved legal truth or answer history."""
import copy
import json
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_full_corpus_review import apply_citation_errata, CITATION_ERRATA_FILES


def raw_rows():
    rows = {}
    for name in CITATION_ERRATA_FILES:
        doc=json.loads((ROOT/'reports/full-corpus-review'/name).read_bytes())
        records={r['question_id']:r for r in json.loads((ROOT/doc['original_report_path']).read_bytes())['records']}
        for patch in doc['errata']:
            qid=patch['question_id'];r=records[qid]
            rows[qid]=dict(question_id=qid,content_sha256=r['record_sha256'],
                choice_by_choice_findings=copy.deepcopy(r['choice_by_choice_findings']),
                review_evidence=dict(source_path=doc['original_report_path']))
    return list(rows.values())


def test_both_locator_levels_are_corrected_without_mutating_original_findings():
    rows=raw_rows();original=copy.deepcopy(rows)
    apply_citation_errata(rows)
    current={r['question_id']:r for r in rows}
    f=current['MA-EXP-0425']['choice_by_choice_findings']['C']
    assert 'retained large-print direction clause' in f['exact_authority']
    assert 'retained large-print direction clause' in f['authorities'][1]['exact_section']
    old=next(r for r in original if r['question_id']=='MA-EXP-0425')['choice_by_choice_findings']['C']
    assert 'first-paragraph' in old['exact_authority']
    for before,after in zip(original,rows):
        assert before['content_sha256']==after['content_sha256']
        for cid in before['choice_by_choice_findings']:
            b=before['choice_by_choice_findings'][cid];a=after['choice_by_choice_findings'][cid]
            assert b.get('statement_supported')==a.get('statement_supported')
            assert b['finding_ko']==a['finding_ko']


def test_locator_overlay_rejects_a_truth_field_even_with_unchanged_question_binding(tmp_path):
    paths=set()
    for name in CITATION_ERRATA_FILES:
        relative='reports/full-corpus-review/'+name;paths.add(relative)
        doc=json.loads((ROOT/relative).read_bytes());paths.add(doc['original_report_path'])
        for ref in [doc['official_authority']]+doc.get('supplemental_official_authorities',[]):
            paths.add(ref['source_evidence_path'])
            if ref.get('retrieval_metadata_path'):paths.add(ref['retrieval_metadata_path'])
    for relative in paths:
        dest=tmp_path/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/relative,dest)
    p=tmp_path/'reports/full-corpus-review/wave10-1-citation-errata.json';doc=json.loads(p.read_bytes())
    patch=doc['errata'][0];patch['field']='statement_supported'
    patch['field_path_segments']=['choice_by_choice_findings',patch['choice_id'],'statement_supported']
    patch['field_path']='.'.join(patch['field_path_segments'])
    p.write_text(json.dumps(doc))
    with pytest.raises(ValueError,match='scope or question binding changed'):
        apply_citation_errata(raw_rows(),tmp_path)
