"""Read-only focused validation of this independent note reassessment evidence."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
import note_review_queue as queue


def validate(job, result, root=ROOT):
    report = json.loads((root / result['evidence']['path']).read_bytes())
    paths = queue.validate_evidence(job, result, report)
    assert len(report['records']) == 1 and len(report['records'][0]['claims']) == 10
    assert report['records'][0]['reassessment_review'] == {**job['reassessment_review'],
        'final_census_read_completely': True, 'all_original_omissions_reassessed': True,
        'all_original_propositions_preserved': True}
    for relative, expected in paths:
        assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == expected
    for source in report['sources']:
        assert source['http_status'] == 200 and source['normal_TLS_certificate_verification'] is True
        for path_key, hash_key in [('raw_path', 'raw_sha256'), ('extracted_text_path', 'extracted_text_sha256')]:
            assert hashlib.sha256((root / source[path_key]).read_bytes()).hexdigest() == source[hash_key]
    uid = job['unit_ids'][0]
    census = json.loads((root / job['unit_bindings'][uid]['census_path']).read_bytes())
    record = json.loads((root / report['reassessment_record_path']).read_bytes())
    original = json.loads((root / record['previous_binding']['census_path']).read_bytes())
    old = {c['claim_id']: c for c in original['claims'] if c['unit_id'] == uid}
    new = {c['claim_id']: c for c in census['claims']}
    assert len(old) == 9 and all(new[cid] == claim for cid, claim in old.items())
    assert all(queue.digest(c) == job['unit_bindings'][uid]['claim_record_sha256s'][c['claim_id']] for c in census['claims'])
    text = record['omission_resolutions'][0]['original_omission_text']
    assert hashlib.sha256(text.encode()).hexdigest() == '53ba62c66400813151c50293639b5b31fc74bd39226fb2ab47e46f25dff8f466'
    assert job['carried_legal_blockers'][uid] == {}
    assert report['new_claim_question_alignment']['original_questions_full_read'] == 31
    return {'assigned_units': 1, 'claim_bindings': 10, 'original_claim_JSON_records_preserved': 9,
            'source_authority_entries': len(paths), 'fresh_official_sources': len(report['sources']),
            'original_omissions_resolved': 1, 'new_omissions': 0, 'status': 'PASS'}
