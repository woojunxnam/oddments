"""Read-only scope/provenance/current-content checks for this worker's evidence."""
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'scripts'))
import review_queue as queue
from build_full_corpus_review import validate_independent_source_bytes

EVD = Path('reports/full-corpus-review/phase9-a-evidence')
REPORT = Path('reports/full-corpus-review/independent-phase9-a-review.json')
job = json.loads(Path('/tmp/independent-phase9-a-assignment.json').read_text())
report = json.loads((ROOT/REPORT).read_text())
packet = json.loads((ROOT/EVD/'assigned-visible-input.json').read_text())
register = json.loads((ROOT/EVD/'source-register.json').read_text())
assert report['stage'] == 'independent-legacy'
assert report['canonical_audit'] is False
assert report['canonical_release_credit'] == report['author_review_credit'] == 0
queue.validate_independent_provenance(job, report)
assert report['auditor_instance'] == 'GPT:/root/independent_wave9_a:20261104'
assert report['actor_provenance']['session_id'] == '/root/independent_wave9_a'
assert report['question_hashes'] == job['question_hashes']
assert len(report['records']) == len(job['question_hashes']) == 40
assert {r['question_id'] for r in report['records']} == set(job['question_hashes'])
assert report['input_binding']['sha256'] == hashlib.sha256((ROOT/EVD/'assigned-visible-input.json').read_bytes()).hexdigest()
for source in report['sources'] + register:
    validate_independent_source_bytes(source, ROOT)

byid = {r['visible']['question_id']:r for r in packet['records']}
officials = {s['source_id']:s for s in report['sources']}
checks = []
current_banks = {}
for row in report['records']:
    qid = row['question_id']; inp = byid[qid]; v = inp['visible']; legal = row['legal_review']
    assert row['record_sha256'] == inp['record_sha256'] == job['question_hashes'][qid]
    assert row['visible_content_sha256'] == queue.digest(v)
    for root in (ROOT, Path('/workspace/oddments')):
        name = (str(root), inp['collection'])
        if name not in current_banks:
            # Whole records are used solely for hash equality; never output or
            # derive a legal finding from hidden author arrays/metadata.
            bank = json.loads((root/inp['collection']).read_text())
            current_banks[name] = {q['question_id']:queue.digest(q) for q in bank['questions']}
        assert current_banks[name][qid] == job['question_hashes'][qid], qid
    assert set(legal['choice_by_choice_findings']) == {c['id'] for c in v['choices']}
    assert legal['stored_key'] == v['correct_choice_ids'] == legal['independently_expected_key']
    selected = [c['id'] for c in v['choices'] if legal['choice_by_choice_findings'][c['id']]['should_be_selected']]
    assert selected == legal['independently_expected_key']
    for c in v['choices']:
        finding = legal['choice_by_choice_findings'][c['id']]
        assert finding['original_text'] == c['text']
        assert finding['original_text_sha256'] == hashlib.sha256(c['text'].encode()).hexdigest()
        assert finding['original_rationale_sha256'] == queue.digest(v['explanation']['choice_analysis'][c['id']])
        assert finding['original_rationale_fully_read'] is True
        assert finding['finding_ko'] and finding['authorities']
        for a in finding['authorities']:
            source = officials[a['source_id']]
            assert source['http_status'] == a['http_status'] == 200 and source.get('error') is None
            assert a['source_support_status'] == 'OFFICIAL_PRIMARY_TEXT_VERIFIED'
            assert a['exact_section'] and a['official_url'].startswith('https://')
            for k in ('raw_sha256','evidence_path','evidence_sha256','retrieved_at'):
                assert a[k] == source[k]
    assert legal['original_explanation_review']['core_sha256'] == queue.digest(v['explanation']['core_reasoning'])
    assert legal['original_explanation_review']['learning_boundary_sha256'] == queue.digest(v['explanation']['learning_boundary'])
    criteria = row['realism_review']['criteria']
    assert len(criteria) == len(row['realism_review']['criterion_findings_ko']) == 10
    assert all(isinstance(v,bool) for v in criteria.values())
    assert all(row['realism_review']['criterion_findings_ko'].values())
    assert (row['realism_review']['verdict']=='PASS') == all(criteria.values())
    assert row['safe_hold_recommended'] == (row['realism_review']['verdict']=='FAIL')
    assert row['native_disposition'] == ('NEEDS_REMEDIATION' if row['safe_hold_recommended'] else 'INDEPENDENT_ASSESSED')
    assert row['release_eligible'] is False
    assert row['required_next_action_ko']
    checks.append({'question_id':qid, 'assigned_whole_hash_matches_worker_and_current_root':True,
        'visible_input_and_full_explanation_binding':True, 'all_four_option_primary_bindings':True,
        'exact_sata_recomputed_key_matches':True, 'ten_realism_criteria_consistent':True})

out = {'validated_at':datetime.now(timezone.utc).isoformat(),
    'scope':'Worker evidence only; no shared queue mutation or full-repository QA',
    'report_path':str(REPORT),
    'report_sha256':hashlib.sha256((ROOT/REPORT).read_bytes()).hexdigest(),
    'native_checks':['review_queue.validate_independent_provenance',
        'build_full_corpus_review.validate_independent_source_bytes'],
    'native_report_source_bindings_verified':len(report['sources']),
    'retrieval_attempt_bindings_verified':len(register),
    'failed_http_attempt_used_as_authority':False,
    'private_copyrighted_raw_redistributed':False,
    'all_assigned_records':checks,
    'dispositions':dict(Counter(r['native_disposition'] for r in report['records'])),
    'postcommit_result_validation':'PENDING_ACTUAL_COMMIT; no invented commit SHA'}
(ROOT/EVD/'precommit-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='all_assigned_records'},ensure_ascii=False,indent=2))
