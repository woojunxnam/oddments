#!/usr/bin/env python3
"""Focused, read-only preservation/binding validation for this source-only author packet."""
import copy
import hashlib
import json
import subprocess
import unittest
from pathlib import Path

PREFIX = 'reports/full-corpus-review/body-corrections/w3-a-3-v1/census-v2-author-e'
ROOT = Path(__file__).resolve().parents[5]
OLD_PATH = 'reports/full-corpus-review/body-corrections/w3-a-3-v1/census.json'
REPORT_PATH = 'reports/full-corpus-review/independent-notes/body-v1-c-review.json'
REV_PATH = 'revisions/notes/candidates/2026-11-04-w3-a-3-pamphlet-scope-v1.json'
NEW_ID = 'NOTE-CENSUS-V2-W3-A-3-ADD-001'
ACTOR = '/root/independent_case_e'
INSTANCE = 'gpt-independent-session-root-independent_case_e-20261103'
BLOCKED = 'BLOCKED_PENDING_N1_ACTIVATION_AND_NATIVE_REGISTRATION'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def digest(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())

def load(path):
    return json.loads((ROOT / path).read_text())

def validate(census=None, handoff=None, raw_overrides=None):
    census = load(PREFIX + '/census.json') if census is None else census
    handoff = load(PREFIX + '/author-handoff.json') if handoff is None else handoff
    raw_overrides = {} if raw_overrides is None else raw_overrides
    original = load(OLD_PATH)
    report = load(REPORT_PATH)
    revision = load(REV_PATH)
    manifest = load(PREFIX + '/preservation-manifest.json')
    unit = census['units'][0]
    new = census['claims'][-1]
    prior = report['records'][0]
    # Every original field/status/source and record order remains exactly identical.
    assert len(original['claims']) == 24
    assert census['claims'][:24] == original['claims'], 'Original24 changed'
    assert len(census['claims']) == 25, 'Exact25 required'
    assert {x['claim_id']: digest(x) for x in census['claims'][:24]} == manifest['original_claim_record_sha256s']
    assert {k: census['sources'][k] for k in original['sources']} == original['sources'], 'Old source metadata changed'
    assert len(census['sources']) == len(original['sources']) + 2
    assert len({x['claim_id'] for x in census['claims']}) == 25
    assert new['claim_id'] == NEW_ID
    assert all(new['statement_ko'] != x['statement_ko'] for x in original['claims']), 'Duplicate proposition'
    body = revision['units'][0]['body']
    assert sha(body.encode()) == unit['unit_content_sha256'] == 'e082d19727f6000e00d21a2c78e76405dfd406bf3f1a786242f57a1047c1ab4a'
    assert new['unit_content_sha256'] == unit['unit_content_sha256']
    assert body.count(new['statement_ko']) == 1
    assert new['statement_ko'] == prior['new_omission_assessments'][0]['body_quote']
    assert new['body_span']['utf8_sha256'] == sha(new['statement_ko'].encode())
    assert unit['claim_count'] == 25 and unit['source_checked_claim_count'] == 22 and unit['source_blocked_claim_count'] == 3
    assert new['review_status'] == 'AUTHOR_SOURCE_CHECKED' and new['independent'] is False
    assert new['related_question_ids'] == [] and new['related_question_alignment_status'] == 'NOT_ASSESSED'
    assert new['effective_date'] is None and 'UNKNOWN' in new['effective_date_note']
    assert census['author_provenance'] == {'actor_id': ACTOR, 'session_id': ACTOR}
    assert census['author_instance'] == INSTANCE == handoff['author_instance']
    assert set(handoff['future_independent_review_excluded_actor_ids']) == {'/root/independent_procedural_retry', ACTOR}
    assert {'/root/independent_procedural_retry', ACTOR}.issubset(census['known_author_ids'])
    assert census['candidate_body_inactive'] is True and census['current_census_ready'] is False and census['current_review_valid'] is False
    assert census['activation_and_registration_status'] == handoff['status'] == BLOCKED
    assert handoff['native_version_record_created'] is False
    assert handoff['native_registration_performed'] is False and handoff['body_activation_performed'] is False
    assert handoff['queue_ledger_generated_writes'] is False
    assert all(v == 0 for v in handoff['credits'].values())
    for key in ['canonical_release_credit', 'question_audit_credit', 'new_author_review_credit', 'new_independent_legal_audit_credit', 'new_active_body_release_credit', 'current_coverage_credit']:
        assert census[key] == 0
    assert census['canonical_audit'] is False and census['independent_of_authors'] is False
    assert census['independent_audit'] == {'status': 'NOT_PERFORMED_BY_THIS_AUTHOR', 'verified_units': 0, 'verified_claims': 0}
    assert handoff['claim_mapping'] == {x['claim_id']: [x['claim_id']] for x in original['claims']}
    assert handoff['added_claim_ids'] == [NEW_ID] and handoff['changed_claim_ids'] == []
    omission = handoff['omission_resolutions'][0]
    assert omission['original_omission_exact'] == prior['omissions'][0]
    assert omission['omission_sha256'] == sha(prior['omissions'][0].encode())
    assert omission['claim_ids'] == [NEW_ID]
    expected_hold = next(c for c in prior['claims'] if c['claim_id'] == 'NOTE-WAVE8-W3-A-3-011')
    hold = handoff['inherited_mandatory_legal_blockers']['NOTE-WAVE8-W3-A-3-011']
    assert hold['full_original_review_object'] == expected_hold, 'C011 carried object changed'
    assert hold['status'] == 'LEGAL_HOLD' and hold['may_clear_in_census_only_correction'] is False
    assert expected_hold['legal_status'] == 'LEGAL_HOLD'
    assert [x['claim_id'] for x in handoff['all_original_author_negative_records_preserved']] == [x['claim_id'] for x in original['claims'] if x['review_status'] == 'SOURCE_BLOCKED']
    queue = load('reports/full-corpus-review/independent-notes-work-queue.json')
    job = next(j for j in queue['jobs'] if j['job_id'] == report['job_id'])
    parent = handoff['parent_independent_review']
    assert job['status'] == 'INTEGRATED' and parent['previous_job_sha256'] == digest(job)
    assert parent['previous_binding'] == job['unit_bindings']['w3-a-3']
    assert parent['previous_report']['raw_sha256'] == '16d98bf341fc6263b26e0b6d4efc9d6b2cfc148b5639aba510248e8a77d863a3'
    for key in ['previous_report', 'previous_result']:
        item = parent[key]
        assert sha((ROOT / item['path']).read_bytes()) == item['raw_sha256']
    snapshot = load(PREFIX + '/evidence/current-root-binding-snapshot.json')
    assert sha(snapshot['actual_effective_unit']['body'].encode()) == snapshot['unit_row']['actual_effective_body_sha256']
    assert snapshot['unit_row']['actual_effective_body_sha256'] != unit['unit_content_sha256']
    assert snapshot['candidate_body_is_current'] is False
    for proof in new['authorities']:
        assert proof['source_type'] == 'PUBLIC_OFFICIAL'
        assert proof['official_url'].startswith(('https://malegislature.gov/', 'https://www.mass.gov/'))
        assert proof['normal_TLS_certificate_verification'] is True
        assert proof['law_checked_date'] == '2026-11-04'
        assert proof['exact_section'] and 'UNKNOWN' in proof['version_or_effective_date_status']
        raw = raw_overrides.get(proof['evidence_path'], (ROOT / proof['evidence_path']).read_bytes())
        assert sha(raw) == proof['evidence_sha256'], 'Primary payload hash mismatch'
        source = census['sources'][proof['source_id']]
        assert source['http_status'] == 200
        assert source['document_identity_and_legal_scope'] == 'OFFICIAL_DOCUMENT_IDENTIFIED_AND_TARGET_PROVISIONS_DIRECTLY_READ'
        assert proof['retrieved_at_utc'] == source['retrieved_at_utc']
        assert proof['read_at_utc'] == source['read_at_utc']
        assert sha((ROOT / source['extracted_text_path']).read_bytes()) == source['extracted_text_sha256']
    # Verify every protected artifact, not merely semantic statements.
    for item in manifest['protected_artifacts']:
        assert sha((ROOT / item['path']).read_bytes()) == item['raw_sha256'], 'Protected artifact modified: ' + item['path']
    for target in [handoff['replacement_census'], manifest['new_census']]:
        assert target['path'] == PREFIX + '/census.json'
        assert target['raw_sha256'] == sha((ROOT / target['path']).read_bytes())
    changed = subprocess.check_output(['git', '-C', str(ROOT), 'diff', '--name-only', manifest['source_only_base_commit']], text=True).splitlines()
    untracked = subprocess.check_output(['git', '-C', str(ROOT), 'ls-files', '--others', '--exclude-standard'], text=True).splitlines()
    assert all(p.startswith(PREFIX + '/') for p in changed + untracked), 'Path outside owned source-only prefix'
    return {'status': 'PASS', 'claims': 25, 'old_claims_identical': 24, 'new_atoms': 1, 'primary_payloads': 2, 'protected_artifacts': len(manifest['protected_artifacts']), 'current_coverage_credit': 0, 'registration_status': BLOCKED}

class PreservationRefusals(unittest.TestCase):
    def setUp(self):
        self.census = load(PREFIX + '/census.json')
        self.handoff = load(PREFIX + '/author-handoff.json')

    def refused(self, change):
        change()
        with self.assertRaises(AssertionError):
            validate(self.census, self.handoff)

    def test_actual_packet(self):
        self.assertEqual(validate()['status'], 'PASS')

    def test_original_statement_change_rejected(self):
        self.refused(lambda: self.census['claims'][0].update(statement_ko='changed'))

    def test_original_source_status_clear_rejected(self):
        self.refused(lambda: self.census['claims'][10].update(review_status='AUTHOR_SOURCE_CHECKED'))

    def test_original_metadata_date_change_rejected(self):
        self.refused(lambda: self.census['claims'][7].update(checked_at='2026-11-04'))

    def test_old_source_mutation_rejected(self):
        self.refused(lambda: self.census['sources']['21'].update(effective_date='2026-11-04'))

    def test_omitted_old_record_rejected(self):
        self.refused(lambda: self.census['claims'].pop(7))

    def test_duplicate_new_atom_rejected(self):
        self.refused(lambda: self.census['claims'][-1].update(statement_ko=self.census['claims'][7]['statement_ko']))

    def test_c011_legal_hold_cannot_be_cleared(self):
        self.refused(lambda: self.handoff['inherited_mandatory_legal_blockers']['NOTE-WAVE8-W3-A-3-011'].update(status='KEEP'))

    def test_c011_inherited_blocker_cannot_be_edited(self):
        self.refused(lambda: self.handoff['inherited_mandatory_legal_blockers']['NOTE-WAVE8-W3-A-3-011']['full_original_review_object']['inherited_legal_blockers'].clear())

    def test_inactive_cannot_be_current(self):
        self.refused(lambda: self.census.update(current_review_valid=True))

    def test_no_future_version_record(self):
        self.refused(lambda: self.handoff.update(native_version_record_created=True))

    def test_no_self_independent_credit(self):
        self.refused(lambda: self.handoff['credits'].update(independent_review_credit=1))

    def test_author_exclusion_cannot_disappear(self):
        self.refused(lambda: self.handoff['future_independent_review_excluded_actor_ids'].remove(ACTOR))

    def test_unread_question_alignment_cannot_be_claimed(self):
        self.refused(lambda: self.census['claims'][-1].update(related_question_ids=['MA-Q-0001']))

    def test_primary_bytes_mismatch_rejected(self):
        proof = self.census['claims'][-1]['authorities'][0]
        with self.assertRaises(AssertionError):
            validate(self.census, self.handoff, {proof['evidence_path']: b'HTTP200 wrong document'})

    def test_http200_not_document_proof(self):
        self.refused(lambda: self.census['sources']['census-v2-e-mgl11239d'].update(document_identity_and_legal_scope='PENDING_DIRECT_READ; HTTP200 alone is not proof'))

    def test_parent_binding_change_rejected(self):
        self.refused(lambda: self.handoff['parent_independent_review']['previous_binding'].update(body_sha256='0' * 64))

if __name__ == '__main__':
    print(json.dumps(validate(), ensure_ascii=False))
    unittest.main(verbosity=2)
