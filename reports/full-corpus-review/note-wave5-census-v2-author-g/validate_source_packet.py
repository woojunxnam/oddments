"""Read-only source packet compatibility/preservation, never native registration or legal PASS."""
import copy
import datetime
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
PREFIX = 'reports/full-corpus-review/note-wave5-census-v2-author-g'
BASE = '4e5f150cc60908386d52fdbaeaae33351a1a5144'
sys.path.insert(0, str(ROOT / 'scripts'))
import note_review_queue as q
import notes_census_reassessment as cr
from notes_revision import load_notes


def load(path):
    return json.loads((ROOT / path).read_bytes())


def reader(path, digest):
    raw = (ROOT / path).read_bytes()
    assert q.raw_sha(raw) == digest, path
    return raw


def preserve(old, new, inputs):
    old_claims = [c for c in old['claims'] if c['unit_id'] == inputs['unit_id']]
    assert new['claims'][:len(old_claims)] == old_claims
    assert {c['claim_id']:q.digest(c) for c in old_claims} == inputs['previous_binding']['claim_record_sha256s']
    assert all(new['sources'][sid] == source for sid, source in old['sources'].items())
    assert inputs['claim_mapping'] == {c['claim_id']:[c['claim_id']] for c in old_claims}
    assert inputs['changed_claim_ids'] == []
    assert [c['claim_id'] for c in new['claims'][len(old_claims):]] == inputs['added_claim_ids']
    statements = {' '.join(c['statement_ko'].split()) for c in old_claims}
    assert all(' '.join(c['statement_ko'].split()) not in statements for c in new['claims'][len(old_claims):])
    assert new['current_review_valid'] is False and new['current_coverage_credit'] == 0
    assert new['registration_executed'] is False and new['native_version_record_created'] is False
    assert new['author_provenance'] == {'actor_id':'/root/independent_case_g','session_id':'/root/independent_case_g'}
    assert new['author_instance'] == 'gpt-independent-phase3-g-root-independent_case_g-20261103'
    assert new['units'][0]['census_status'] == 'COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK'
    assert new['units'][0]['claim_count'] == len(new['claims'])
    assert new['units'][0]['source_blocked_claim_count'] == sum(c['review_status'] == 'SOURCE_BLOCKED' for c in old_claims)
    assert inputs['not_a_native_version_record'] is True


def validate():
    report = load(PREFIX + '/author-report.json')
    manifest = load(PREFIX + '/preservation-manifest.json')
    state = load(q.STATE)
    notes = load_notes(ROOT)
    actual = {u['id']:u for c in notes['chapters'] for u in c['units']}
    assert report['source_base_commit'] == BASE
    parent = next(j for j in state['jobs'] if j['job_id'] == report['parent']['job_id'])
    assert parent['status'] == 'INTEGRATED' and q.digest(parent) == report['parent']['job_semantic_sha256']
    assert q.raw_sha((ROOT / report['parent']['report']['path']).read_bytes()) == 'df4642aa85a010873e03a50e805edd550f13218d9e381fc5ffce09fc002fab08'
    prior_report = load(report['parent']['report']['path'])
    for binding in manifest['protected_source_files']:
        raw = reader(binding['path'], binding['raw_sha256'])
        assert raw == subprocess.check_output(['git','show',BASE+':'+binding['path']], cwd=ROOT)
    out = []
    totals = [0,0,0,0]
    datasets = []
    for unit in report['units']:
        uid = unit['unit_id']
        inputs = load(unit['parent_inputs']['path'])
        new = load(unit['census']['path'])
        assert q.raw_sha((ROOT / unit['census']['path']).read_bytes()) == unit['census']['raw_sha256']
        assert q.raw_sha((ROOT / unit['parent_inputs']['path']).read_bytes()) == unit['parent_inputs']['raw_sha256']
        old = load(inputs['previous_binding']['census_path'])
        preserve(old, new, inputs)
        assert actual[uid]['body'].encode() == (ROOT / unit['body_evidence']['path']).read_bytes()
        assert q.raw_sha(actual[uid]['body'].encode()) == inputs['body_sha256']
        original = next(r for r in prior_report['records'] if r['unit_id'] == uid)
        assert original['completeness'] == 'OMISSIONS_FOUND'
        assert {x['omission_sha256'] for x in inputs['omission_resolutions']} == {q.raw_sha(s.encode()) for s in original['omissions']}
        fields = ['unit_id','body_sha256','previous_job_id','previous_job_sha256','previous_binding','previous_result','previous_report','previous_ledger_fields','replacement','author_provenance','claim_mapping','added_claim_ids','changed_claim_ids','omission_resolutions','change_basis']
        # This synthetic record exists in memory only. No version file, state mutation, or registration.
        candidate = {k:copy.deepcopy(inputs[k]) for k in fields}
        candidate.update(schema_version=1,purpose=cr.PURPOSE,reassessment_id='IN_MEMORY_COMPATIBILITY_ONLY_'+uid)
        returned, carried = cr.validate_record(state, candidate, ROOT, notes, reader)
        assert carried == inputs['carried_legal_blockers'] == unit['carried_legal_blockers']
        assert len(returned['claim_record_sha256s']) == len(new['claims'])
        out.append({'unit_id':uid,'native_read_only_validate_record':'PASS_COMPATIBILITY_NOT_REGISTRATION','body_sha256':inputs['body_sha256'],'claims':len(new['claims']),'carried_negative_claims':len(carried)})
        totals[0] += unit['old_claim_count']; totals[1] += len(inputs['added_claim_ids'])
        totals[2] += len(inputs['original_author_SOURCE_BLOCKED_claims']); totals[3] += len(carried)
        datasets.append((old,new,inputs))
    assert totals == [66,4,7,4]
    sources = load(PREFIX + '/evidence/fresh-primary-source-register.json')['sources']
    assert len(sources) == 3
    signatures = {'G5-scope2020':'not considered “re-dispensing.”','G5-practice9':'assessment of the integrity of the medication','G5-packaging2023':'properly and clearly'}
    for sid, source in sources.items():
        assert source['retrieval_status'] == 'RETRIEVED_FRESH_OFFICIAL_PRIMARY'
        assert source['retrieved_at'].startswith('2026-11-04T08:22:17')
        assert source['http_status'] == 200 and source['tls_verification'] is True
        assert source['effective_date'] is None and 'UNKNOWN' in source['effective_date_note']
        assert reader(source['source_evidence'],source['source_evidence_sha256']).startswith(b'%PDF')
        text = reader(source['extracted_path'],source['extracted_sha256']).decode()
        assert signatures[sid] in text
        metadata = json.loads(reader(source['retrieval_metadata_path'],source['retrieval_metadata_sha256']))
        assert metadata['body_verification'] == 'CORRECT_OFFICIAL_DOCUMENT_TARGET_CLAUSES_PERSONALLY_READ'
        assert metadata['used_as_legal_proof'] is True
    inventory_path = ROOT / PREFIX / 'artifact-manifest.json'
    if inventory_path.exists():
        for item in json.loads(inventory_path.read_text())['files']:
            reader(item['path'],item['raw_sha256'])
    return out, datasets


def negatives(data):
    old, new, inputs = data
    rejected = []
    def reject(name, mutation):
        changed = copy.deepcopy(new)
        mutation(changed)
        try:
            preserve(old, changed, inputs)
        except (AssertionError, KeyError):
            rejected.append(name)
        else:
            raise AssertionError('Mutation accepted: '+name)
    reject('old_statement_changed', lambda c:c['claims'][0].update(statement_ko='Changed old proposition'))
    reject('old_author_SOURCE_BLOCKED_upgraded', lambda c:next(x for x in c['claims'] if x['review_status']=='SOURCE_BLOCKED').update(review_status='AUTHOR_SOURCE_CHECKED'))
    reject('old_source_metadata_rewritten', lambda c:next(iter(c['sources'].values())).update(checked_at='2026-11-04-NEW'))
    reject('new_atom_repeats_old_statement', lambda c:c['claims'][-1].update(statement_ko=c['claims'][0]['statement_ko']))
    reject('current_review_credit_granted', lambda c:c.update(current_review_valid=True,current_coverage_credit=1))
    reject('native_registration_claimed', lambda c:c.update(registration_executed=True))
    return rejected


if __name__ == '__main__':
    results, datasets = validate()
    cases = negatives(datasets[0])
    receipt = {'status':'PASS_SOURCE_PACKET_PRESERVATION_AND_READ_ONLY_NATIVE_COMPATIBILITY','validated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'units':results,'old_claim_JSON_objects_preserved':66,'new_atoms':4,'total_claims':70,'old_author_SOURCE_BLOCKED_preserved':7,'actual_C32_negatives_carried':4,'protected_source_files_byte_preserved':76,'fresh_primary_payloads':3,'negative_mutations_rejected':cases,'native_version_record_created':False,'native_registration_executed':False,'independent_completeness_legal_review_performed':False,'new_current_credit':0}
    if '--receipt' in sys.argv:
        assert not (ROOT / PREFIX / 'artifact-manifest.json').exists()
        (ROOT / PREFIX / 'validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
