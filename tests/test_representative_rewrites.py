"""Safety contracts for meaning-changing question revisions and preserved learner history."""
from __future__ import annotations

import hashlib
import copy
from datetime import date
import json
from pathlib import Path
import re
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_representative_rewrites import BASE, REPORTS, build, content_hash, encoded, pattern_metrics, verify_published_baseline
from publish_practice import build_payload, render


class RepresentativeRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bank = json.loads((BASE / 'questions.json').read_text())
        cls.selection = json.loads((BASE / 'selection.json').read_text())
        cls.payload = build_payload()
        cls.by_id = {q['question_id']: q for q in cls.payload['questions']}
        cls.original_selection = json.loads((ROOT / 'practice_expansion/2026-10-27-quality/selection.json').read_text())

    def test_all_three_archives_are_byte_identical(self):
        expected = {
            'practice_expansion/2026-10-23/candidates/questions.json': 'f2b27d3105f2efab40d3ab943f0f5813bdadd793e5ffa60d262fe5ab4e40a74f',
            'practice_expansion/2026-10-26-plus/questions.json': 'f9a600504be007913c996163db29a482cc30ae3781055e50dc3ef9d83f2655b6',
            'practice_expansion/2026-10-27-quality/questions.json': '27f39f5607b58d56796aadd6c68236d576972150ffd65fcece790aba5ea5e344',
        }
        for path, digest in expected.items():
            self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), digest, path)

    def test_legacy_stems_keys_rationales_and_ids_survive_publication(self):
        for relative in ['2026-10-23/candidates', '2026-10-26-plus', '2026-10-27-quality']:
            data = json.loads((ROOT / 'practice_expansion' / relative / 'questions.json').read_text())
            for old in data['questions']:
                current = self.by_id[old['question_id']]
                for key in ['stem', 'choices', 'correct_choice_ids', 'explanation', 'note_evidence', 'family_id']:
                    self.assertEqual(current[key], old[key], old['question_id'] + '/' + key)

    def test_new_content_has_new_ids_and_old_family_exclusion(self):
        legacy_ids = set(self.original_selection['recommended_ids']) - set(self.original_selection['new_ids'])
        for q in self.bank['questions']:
            self.assertRegex(q['question_id'], r'^MA-RW-\d{4}$')
            self.assertNotIn(q['question_id'], legacy_ids)
            self.assertIn(q['revision_of'], legacy_ids)
            self.assertEqual(q['family_id'], self.by_id[q['revision_of']]['family_id'])
            self.assertEqual(q['history_policy'], 'NEW_ID_NO_ATTEMPT_OR_BOOKMARK_MIGRATION')
            self.assertEqual(q['content_sha256'], content_hash(q))

    def test_every_choice_has_exact_current_author_citations(self):
        sources = self.bank['sources']
        for q in self.bank['questions']:
            ids = {c['id'] for c in q['choices']}
            read_dates = {r['source_id']: r['accessed_at'] for r in q['primary_source_read_records']}
            self.assertEqual(ids, set(q['explanation']['choice_authorities']))
            self.assertEqual(ids, set(q['explanation']['choice_analysis']))
            for option_id, refs in q['explanation']['choice_authorities'].items():
                self.assertTrue(refs, q['question_id'] + '/' + option_id)
                for ref in refs:
                    self.assertTrue(ref['exact_section'].strip())
                    source = sources[ref['source_id']]
                    self.assertEqual(source['access_status'], 'READ_OFFICIAL')
                    self.assertEqual(source['checked_at'], read_dates[ref['source_id']])
                    self.assertLessEqual(date.fromisoformat(source['checked_at']), date.fromisoformat(q['authored_at']))
                    self.assertTrue(source['url'].startswith('https://'))
                    self.assertTrue(source['retrieval_method'])

    def test_note_evidence_pins_original_or_explicit_versioned_unit_hashes_and_dates(self):
        from notes_revision import load_notes
        guide = json.loads((ROOT / 'notes/guide.json').read_text())
        units = {u['id']: u for c in guide['chapters'] for u in c['units']}
        authored = {q['question_id']: q
                    for path in (BASE / 'authoring').glob('*.json')
                    for q in json.loads(path.read_text()).get('questions', [])}
        versioned_ids = set()
        for q in self.bank['questions']:
            source = authored[q['question_id']]
            expected_units = units
            if source.get('note_evidence_basis') == 'EFFECTIVE_REVISION':
                versioned_ids.add(q['question_id'])
                revised = load_notes(ROOT, revision_id=source['notes_revision'])
                self.assertEqual(q['notes_revision'], revised['revision_provenance'])
                expected_units = {u['id']: u for c in revised['chapters'] for u in c['units']}
            for ref in q['note_evidence']:
                u = expected_units[ref['unit_id']]
                self.assertEqual(ref['body_sha256'], u['body_sha256'])
                self.assertEqual(ref['inherited_note_review_date'], u['source_review_date'])
                self.assertEqual(ref['inherited_flags'], u['flags'])
        self.assertEqual(versioned_ids, {f'MA-RW-{index:04d}' for index in range(77, 81)})

    def test_independent_audit_status_is_not_fabricated(self):
        self.assertEqual(self.payload['canonical_released_question_count'], 0)
        for q in self.bank['questions']:
            self.assertEqual(q['publication_status'], 'PUBLISHED_PRACTICE')
            self.assertEqual(q['verification_status'], 'NOT_INDEPENDENTLY_REVIEWED')
            self.assertIsNone(q['independent_legal_audit'])
            self.assertIsNone(q['independent_realism_audit'])

    def test_default_replaces_or_holds_legacy_without_deleting_it(self):
        recommended = set(self.selection['recommended_ids'])
        self.assertEqual(recommended, set(self.payload['quality_selection']['recommended_ids']))
        for replacement in self.selection['replacements']:
            self.assertNotIn(replacement['legacy_question_id'], recommended)
            self.assertIn(replacement['legacy_question_id'], self.by_id)
            self.assertIn(replacement['replacement_question_id'], recommended)
        for hold in self.selection['holds']:
            self.assertNotIn(hold['legacy_question_id'], recommended)
            self.assertIn(hold['legacy_question_id'], self.by_id)
        self.assertTrue(set(self.original_selection['new_ids']) <= recommended)

    def test_first_authoring_unit_addresses_exactly_48_originals(self):
        authored = [json.loads((BASE / 'authoring' / name).read_text())
                    for name in ['01_personnel.json', '02_clinical_authority.json']]
        ids = [q['legacy_question_id'] for a in authored for q in a['questions']]
        ids += [q['legacy_question_id'] for a in authored for q in a.get('holds', [])]
        ids += [q['legacy_question_id'] for a in authored for q in a.get('reuse_existing', [])]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 48)

    def test_second_unit_has_explicit_nonoverlapping_legacy_dispositions(self):
        authored = [json.loads((BASE / 'authoring' / name).read_text())
                    for name in ['03_personnel_scope.json', '04_pharmacy_operations.json']]
        ids = [q['legacy_question_id'] for unit in authored
               for field in ['questions', 'holds', 'reuse_existing'] for q in unit.get(field, [])]
        expected = {f'MA-EXP-{n:04d}' for n in [99, 103, 107, 111, 115, 119, 155, 159, 163, 167, 171, 175]}
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), expected)
        for unit in authored:
            self.assertEqual(unit['authored_at'], '2026-10-29')
            self.assertEqual(unit['edition'], '2026-10-29.representative2')
            for q in unit['questions']:
                actual = self.by_id[q['question_id']]
                self.assertEqual(actual['authored_at'], unit['authored_at'])
                self.assertEqual(actual['source_edition'], unit['edition'])
                self.assertEqual(actual['edition'], self.payload['edition'])
                source = next(item for item in self.bank['questions'] if item['question_id'] == q['question_id'])
                self.assertEqual(source['edition'], unit['edition'])

    def test_published_first_unit_objects_and_sources_remain_unchanged(self):
        verify_published_baseline(self.bank)

    def test_published_first_unit_guard_rejects_silent_content_changes(self):
        altered = copy.deepcopy(self.bank)
        question = next(q for q in altered['questions'] if q['question_id'] == 'MA-RW-0001')
        question['stem'] += ' Changed condition.'
        question['content_sha256'] = content_hash(question)
        with self.assertRaisesRegex(ValueError, 'Published content changed'):
            verify_published_baseline(altered)
        altered = copy.deepcopy(self.bank)
        altered['sources']['rw-cmr3']['checked_at'] = '2026-10-29'
        with self.assertRaisesRegex(ValueError, 'Published content changed'):
            verify_published_baseline(altered)

    def test_reused_source_ids_cannot_bypass_read_and_provenance_checks(self):
        original = json.loads((BASE / 'authoring/01_personnel.json').read_text())['sources']['rw-cmr3']
        cases = [
            ('access_status', 'NOT_READ', 'invalid official text read/date'),
            ('checked_at', '2026-10-29', 'conflicting checked_at'),
            ('retrieval_method', 'a different unrecorded access path', 'conflicting retrieval_method'),
            ('verification_scope', '', 'missing read scope/provenance'),
        ]
        for field, value, message in cases:
            with self.subTest(field=field):
                source = copy.deepcopy(original)
                source[field] = value
                def changed_read(path):
                    data = json.loads(path.read_text())
                    if path.name == '03_personnel_scope.json':
                        data['sources']['rw-cmr3'] = source
                    return data
                with patch('build_representative_rewrites.read', side_effect=changed_read):
                    with self.assertRaisesRegex(ValueError, message):
                        build()
    def test_new_design_has_no_all_correct_sata_or_duplicate_packs(self):
        metrics = pattern_metrics(self.bank['questions'])
        self.assertEqual(metrics['all_correct_sata'], 0)
        self.assertEqual(metrics['paired_case_questions'], 0)
        self.assertEqual(metrics['repeated_normalized_stem_occurrences'], 0)
        self.assertEqual(metrics['questions_in_identical_option_sets'], 0)
        self.assertEqual(len({q['decision_signature'] for q in self.bank['questions']}), len(self.bank['questions']))

    def test_english_questions_korean_explanations_and_outline(self):
        for q in self.bank['questions']:
            self.assertIsNone(re.search(r'[가-힣]', q['stem'] + ' '.join(c['text'] for c in q['choices'])))
            for rationale in q['explanation']['choice_analysis'].values():
                self.assertRegex(rationale, r'[가-힣]')
            self.assertEqual(q['exam_outline'], 'MPJE-MA-PRE2027')
            self.assertEqual(q['valid_for_exams_before'], '2027-03-01')

    def test_build_is_deterministic_and_inputs_are_not_mutated(self):
        for path, expected in build().items():
            self.assertEqual(path.read_bytes(), encoded(expected), str(path))

    def test_html_retains_history_chaos_and_explicit_revision_links(self):
        html = render(self.payload)
        for token in ["KEY='oddments.mpje.practice.v1'", 'QC.chaos(Q,count)',
                      'QC.record(session,active,selected,displayOrder)', 'id="revision-notice"',
                      "a.href='#'+q.revision_of", "a.href='#'+next.replacement_question_id",
                      'q.explanation.choice_authorities?.[c.id]', "initialBank==='rewrite'"]:
            self.assertIn(token, html)
        self.assertNotIn('id="ack"', html)
        self.assertNotIn('session.answers[active.question_id]=', html)

    def test_full_355_editorial_ledger_is_explicitly_not_legal_certification(self):
        ledger = json.loads((REPORTS / 'audit-ledger.json').read_text())
        rows = ledger['questions']
        expected = set(self.original_selection['recommended_ids']) - set(self.original_selection['new_ids'])
        self.assertEqual({q['question_id'] for q in rows}, expected)
        self.assertEqual(len(rows), 355)
        self.assertFalse(ledger['canonical_independent_audit_created'])
        for row in rows:
            self.assertTrue(row['editorial_triage'])
            self.assertIn(row['implementation_status'], {'REWRITTEN_NEW_ID', 'REUSED_EXISTING_QUALITY', 'HOLD_FROM_DEFAULT', 'NOT_YET_IMPLEMENTED'})


if __name__ == '__main__':
    unittest.main()
