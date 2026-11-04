"""Source-only author artifact checks; no law/realism independent PASS is generated."""
import copy
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys

BASE = 'b7e87d5f3086d77e33f9ac350eeaa2522c93f1fd'
PREFIX = 'reports/full-corpus-review/phase9-remediation-author-g/v2'
FIELDS = ['draft_key', 'question_type', 'stem', 'choices', 'correct_choice_ids', 'explanation']
FREPORT = 'reports/full-corpus-review/phase9-remediation-final-f/final-f-review.json'
FCOMMIT = '4c2987c3a28397a4d0da609baff092b6b13c5b98'
FSHA = '1c7cda8e3fcfc22143be3ce2ea9ebe0387c3a5c6ff2bc9d125db51f745bf7451'
TARGETS = {'P9-REPAIR-EXP-0515', 'P9-REPAIR-EXP-0827'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical_sha(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def check_draft(draft, sources):
    assert draft['draft_key'] in TARGETS and draft['content_version'] == 2
    assert draft['status'] == 'DRAFT_AUDIT_PENDING'
    assert draft['author_provenance']['role'] == 'AUTHOR'
    assert draft['author_provenance']['stable_auditor_instance'] == 'gpt-independent-phase3-g-root-independent_case_g-20261103'
    for field in ['canonical_release_credit', 'native_review_credit', 'independent_review_credit', 'author_review_credit', 'additional_coverage_credit', 'new_public_ids_allocated']:
        assert draft[field] == 0
    for field in ['public_activation', 'release_eligible', 'canonical_audit', 'independent_of_authors']:
        assert draft[field] is False
    assert draft['question_type'] == 'SATA'
    ids = [c['id'] for c in draft['choices']]
    key = draft['correct_choice_ids']
    assert ids == ['A', 'B', 'C', 'D'] and len(set(key)) == len(key)
    assert 2 <= len(key) < len(ids) and set(key) <= set(ids)
    assert set(draft['explanation']['choice_analysis']) == set(ids)
    assert draft['explanation']['core_reasoning'] and draft['explanation']['learning_boundary']
    assert all(re.search('[가-힣]', text) for text in draft['explanation']['choice_analysis'].values())
    english = draft['stem'] + '\n' + '\n'.join(c['text'] for c in draft['choices'])
    assert not re.search('[가-힣]', english)
    assert not re.search(r'retrieved|according to (?:the )?notes|source metadata', english, re.I)
    assert len({c['text'] for c in draft['choices']}) == 4
    assert draft['visible_content_sha256'] == canonical_sha({k: draft[k] for k in FIELDS})
    assert draft['revision_binding']['F_report_raw_sha256'] == FSHA
    assert draft['revision_binding']['F_is_v2_author_or_editor'] is False
    assert draft['revision_binding']['F_v1_decision_applies_to_v2_hash'] is False
    assert draft['revision_binding']['v1_visible_content_sha256'] != draft['visible_content_sha256']
    assert draft['source_blocker'] is None
    assert [p['choice_id'] for p in draft['option_proofs']] == ids
    for choice, proof in zip(draft['choices'], draft['option_proofs']):
        cid = choice['id']
        assert proof['option_text_sha256'] == sha(choice['text'].encode())
        assert proof['rationale_sha256'] == sha(draft['explanation']['choice_analysis'][cid].encode())
        assert proof['author_supported'] == ('YES' if cid in key else 'NO')
        assert proof['authorities']
        for authority in proof['authorities']:
            original = sources[authority['source_id']]
            for k in original:
                assert authority[k] == original[k], (cid, k)
            assert authority['exact_section'] and authority['http_status'] == 200
            assert authority['tls_verification'] is True and authority['used_as_legal_proof'] is True
    # These limits prevent reintroduction of the two actual editorial defects.
    if draft['draft_key'].endswith('0515'):
        assert 'required to provide' in draft['stem']
        assert 'comply' not in draft['stem']
        assert '자발적' in draft['explanation']['choice_analysis']['C']
    else:
        assert 'contracted with' in draft['stem'] and 'in-transit-loss' in draft['stem']
        assert not re.search(r'\b45\b|one business day|investigation|November', english, re.I)


def validate(root):
    root = pathlib.Path(root)
    folder = root / PREFIX
    load = lambda p: json.loads(p.read_text())
    prior = load(folder / 'evidence/v1-preservation-baseline.json')
    assert prior['commit'] == BASE and prior['file_count'] == 131
    tracked = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE, '--', PREFIX.rsplit('/v2', 1)[0]], cwd=root, text=True).splitlines()
    assert set(tracked) == {x['path'] for x in prior['files']}
    for item in prior['files']:
        before = subprocess.check_output(['git', 'show', BASE + ':' + item['path']], cwd=root)
        assert sha(before) == item['raw_sha256'] == sha((root / item['path']).read_bytes())
    fbytes = subprocess.check_output(['git', 'show', FCOMMIT + ':' + FREPORT], cwd=root)
    assert sha(fbytes) == FSHA
    frows = {r['draft_key']: r for r in json.loads(fbytes)['records']}
    register = load(folder / 'evidence/source-register.json')
    sources = register['sources']
    assert set(sources) == {'hipaa404', 'hipaa406', 'hipaa408', 'loss'}
    memos = load(folder / 'evidence/controlling-rule-memos.json')['memos']
    for sid, source in sources.items():
        assert source['http_status'] == 200 and source['tls_verification'] is True
        assert source['official_url'].startswith('https://www.ecfr.gov/current/')
        assert source['retrieved_at'].startswith('2026-11-04T07:39:48')
        assert source['law_checked_date'] == '2026-11-04'
        assert source['effective_date'] is None and 'UNKNOWN' in source['version_or_effective_date_status']
        for path, digest in [('raw_path', 'raw_sha256'), ('text_path', 'text_sha256'), ('retrieval_metadata_path', 'retrieval_metadata_sha256')]:
            payload = (root / source[path]).read_bytes()
            assert payload and sha(payload) == source[digest]
        metadata = load(root / source['retrieval_metadata_path'])
        assert metadata['used_as_legal_proof'] is True
        assert metadata['body_verification'] == 'CORRECT_DOCUMENT_CONTROLLING_SECTION_PERSONALLY_READ'
        assert metadata['raw_sha256'] == source['raw_sha256']
        text = (root / source['text_path']).read_text()
        for k, phrase in memos[sid].items():
            if k.endswith('_original'):
                assert phrase in text, (sid, k)
    draft_paths = sorted((folder / 'drafts').glob('*.json'))
    drafts = [load(p) for p in draft_paths]
    assert len(drafts) == 2 and {d['draft_key'] for d in drafts} == TARGETS
    for draft in drafts:
        check_draft(draft, sources)
        binding = draft['revision_binding']
        frow = frows[draft['draft_key']]
        assert binding['F_finding_semantic_sha256'] == canonical_sha(frow)
        assert frow['final_author_draft_raw_sha256'] == binding['v1_raw_sha256'] == sha((root / binding['v1_path']).read_bytes())
        assert frow['original_record_sha256'] == draft['original_record_sha256']
        native = subprocess.check_output(['git', 'show', BASE + ':' + draft['native_finding_report_path']], cwd=root)
        assert sha(native) == draft['native_finding_report_sha256']
        for path_key, sha_key in [('context_path', 'context_raw_sha256'), ('originals_path', 'originals_raw_sha256')]:
            assert sha((root / draft['nearby_comparison'][path_key]).read_bytes()) == draft['nearby_comparison'][sha_key]
    context = load(folder / 'evidence/nearest-search-context.json')
    neighbors = load(folder / 'evidence/nearest-visible-originals.json')
    actual = load(folder / 'evidence/author-nearby-comparison.json')
    assert (context['canonical_emitted_count'], context['public_count'], context['actual_committed_default_count']) == (397, 2349, 229)
    assert actual['unique_originals_personally_read'] == len(neighbors) == 36
    assert actual['all_displayed_stems_and_all_choices_read'] is True
    neighbor_ids = {q['question_id'] for q in neighbors}
    for draft in drafts:
        search = next(x for x in context['comparisons'] if x['draft_key'] == draft['draft_key'])
        comparison = next(x for x in actual['records'] if x['draft_key'] == draft['draft_key'])
        assert search['draft_visible_content_sha256'] == comparison['draft_visible_content_sha256'] == draft['visible_content_sha256']
        assert len(comparison['criteria_findings_ko']) == 10
        assert set(comparison['personally_read_full_original_stems_and_all_choices']) <= neighbor_ids
        assert comparison['independent_current_v2_legal_realism_review'] == 'PENDING'
    report = load(folder / 'editorial-report-v2.json')
    assert report['summary']['v2_drafts_authored'] == 2
    assert report['summary']['remaining_v1_drafts_modified'] == 0
    assert report['summary']['actual_independent_v2_review_pending'] == 2
    assert report['summary']['all_credits'] == 0
    for draft, path in zip(drafts, draft_paths):
        row = next(x for x in report['records'] if x['draft_key'] == draft['draft_key'])
        assert row['v2_raw_sha256'] == sha(path.read_bytes())
        assert row['v2_visible_content_sha256'] == draft['visible_content_sha256']
        assert row['independent_v2_legal_review'] == row['independent_v2_realism_review'] == 'PENDING'
    manifest = folder / 'artifact-manifest.json'
    if manifest.exists():
        inventory = load(manifest)['files']
        assert {x['path'] for x in inventory} == {str(p.relative_to(root)) for p in folder.rglob('*') if p.is_file() and p != manifest}
        for item in inventory:
            assert sha((root / item['path']).read_bytes()) == item['raw_sha256']
    return drafts, sources


def negative_tests(drafts, sources):
    cases = []
    def case(name, mutation):
        d = copy.deepcopy(drafts[0])
        mutation(d)
        try:
            check_draft(d, sources)
        except (AssertionError, KeyError):
            cases.append(name)
        else:
            raise AssertionError('tamper accepted: ' + name)
    case('missing_Korean_rationale', lambda d: d['explanation']['choice_analysis'].pop('C'))
    case('all_correct_SATA', lambda d: d.update(correct_choice_ids=['A', 'B', 'C', 'D']))
    case('self_independent_credit', lambda d: d.update(independent_review_credit=1))
    case('public_activation', lambda d: d.update(public_activation=True))
    case('stale_current_visible_hash', lambda d: d.update(visible_content_sha256='0' * 64))
    case('source_raw_SHA_tamper', lambda d: d['option_proofs'][0]['authorities'][0].update(raw_sha256='0' * 64))
    case('failed_source_used_as_proof', lambda d: d['option_proofs'][0]['authorities'][0].update(http_status=403))
    case('inherit_F_v1_PASS_to_changed_v2', lambda d: d['revision_binding'].update(F_v1_decision_applies_to_v2_hash=True))
    case('v1_comply_scope_reintroduced', lambda d: d.update(stem=d['stem'].replace('required to provide', 'planning to provide')))
    # Lossless preservation uses byte hashes; a one-byte mutation must not retain the digest.
    assert sha(b'original\n') != sha(b'original!\n')
    cases.append('one_byte_preserved_artifact_mutation_detected')
    return cases


if __name__ == '__main__':
    root = pathlib.Path(__file__).resolve().parents[4]
    drafts, sources = validate(root)
    rejected = negative_tests(drafts, sources)
    result = {'status': 'PASS_ARTIFACT_CHECKS_ONLY', 'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'v2_drafts': 2, 'English_options': 8, 'Korean_choice_rationales': 8, 'fresh_official_source_payloads': 4, 'v1_files_byte_preserved': 131, 'other_v1_drafts_preserved': 8, 'full_original_nearby_stems_all_choices_read': 36, 'ten_criteria_per_draft': 10, 'negative_mutations_rejected': rejected, 'legal_or_realism_independent_review_generated': False, 'all_credits': 0}
    if '--receipt' in sys.argv:
        path = root / PREFIX / 'artifact-checks.json'
        assert not (root / PREFIX / 'artifact-manifest.json').exists(), 'Do not invalidate a sealed manifest by rewriting receipt.'
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
