#!/usr/bin/env python3
"""Lossless engineering adapter for three reviewed G drafts; creates no audit credit.

The allocation is frozen once against an explicit Git tree. Subsequent builds read
that manifest; they never allocate a different ID or change the reviewed wording.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = 'practice_expansion/2026-10-28-representative'
OUT = 'reports/representative-rewrite/sata-remediation'
ALLOCATION = OUT + '/allocation.json'
PUBLISHED_BASELINE = OUT + '/published-record-baseline.json'
AUTHORING = BASE + '/authoring/10_sata_remediation.json'
AUTHOR_COMMIT = '7a50ba013a5dc271f62f3cd6ffaf39757cb53898'
REVIEW_COMMIT = '1c540bd3ced12ccfc097486df57c0d71b3b86ef8'
REVIEW_PATH = 'reports/full-corpus-review/substantive-remediation-independent-e/review.json'
REVIEW_SHA = '88f926d7cdce722a2998cfae45f36db7072389d701fef48869da7604164e886d'
G_BASE = 'reports/full-corpus-review/substantive-remediation-g'
REGISTER = G_BASE + '/evidence/primary-source-register.json'
ORIGINALS = ('MA-EXP-0351', 'MA-EXP-0367', 'MA-EXP-0383')
NAMESPACE = 'rw7-remediation-'
EDITION = '2026-11-04.representative7'
REVIEW_DATE = '2026-11-04'
PUBLIC_BANKS = ('practice_expansion/2026-10-23/candidates/questions.json',
                'practice_expansion/2026-10-26-plus/questions.json',
                'practice_expansion/2026-10-27-quality/questions.json', BASE + '/questions.json')
ENGINEER = dict(actor_id='/root/independent_case_e', session_id='/root/independent_case_e',
                stable_instance='gpt-independent-session-root-independent_case_e-20261103',
                role='LOSSLESS_ENGINEERING_NOT_CURRENT_ID_INDEPENDENT_AUDITOR')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def record_sha(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def git_bytes(root, commit, relative):
    return subprocess.check_output(['git', '-C', str(root), 'show', commit + ':' + relative])


def next_rewrite_ids(reserved, count):
    require(bool(reserved) and count > 0, 'Reservation inventory/count required')
    require(all(re.fullmatch(r'MA-RW-\d{4}', qid) for qid in reserved), 'Invalid reserved rewrite ID')
    start = max(int(qid.rsplit('-', 1)[1]) for qid in reserved) + 1
    require(start + count <= 10000, 'MA-RW four-digit ID space exhausted')
    return [f'MA-RW-{n:04d}' for n in range(start, start + count)]


def published_baseline_snapshot(root, commit):
    """One-time capture using the actual, unmodified base publication builder."""
    import io, tarfile, tempfile, sys
    stream = subprocess.check_output(['git', '-C', str(root), 'archive', commit])
    code = """import sys,json,hashlib
sys.path.insert(0,'scripts')
from publish_practice import build_payload
d=build_payload()
print(json.dumps({'base_commit':sys.argv[1],
'method':'Actual unmodified base publish_practice.build_payload in isolated Git archive; complete delivered question object canonical JSON hashes.',
'question_count':len(d['questions']),
'record_hashes':{q['question_id']:hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest() for q in d['questions']}},ensure_ascii=False,indent=2))
"""
    with tempfile.TemporaryDirectory(prefix='sata-publication-baseline-') as folder:
        with tarfile.open(fileobj=io.BytesIO(stream)) as archive:
            archive.extractall(folder, filter='data')
        raw = subprocess.check_output([sys.executable, '-c', code, commit], cwd=folder)
    require(json.loads(raw)['question_count'] == 2346, 'Unexpected actual publication baseline')
    return raw


def allocation_snapshot(root, commit):
    """Scan every tracked textual reservation, including all authoring/draft trees."""
    # One archive stream avoids launching a Git process for every source file.
    import io, tarfile
    stream = subprocess.check_output(['git', '-C', str(root), 'archive', commit])
    reservations, authoring_files = {}, {}
    with tarfile.open(fileobj=io.BytesIO(stream)) as archive:
        for member in archive:
            if not member.isfile():
                continue
            path = member.name
            if Path(path).suffix not in {'.json', '.jsonl', '.txt', '.md', '.py', '.js', '.html'}:
                continue
            raw = archive.extractfile(member).read()
            ids = sorted(set(re.findall(r'\bMA-RW-\d{4}\b', raw.decode(errors='replace'))))
            if ids:
                reservations[path] = dict(raw_sha256=sha(raw), reserved_ids=ids)
            if '/authoring/' in path or ('draft' in path.lower() and Path(path).suffix == '.json'):
                authoring_files[path] = sha(raw)
    reserved = sorted({qid for row in reservations.values() for qid in row['reserved_ids']})
    allocated = next_rewrite_ids(reserved, len(ORIGINALS))
    banks = {path: json.loads(git_bytes(root, commit, path)) for path in PUBLIC_BANKS}
    public = {q['question_id']: record_sha(q) for bank in banks.values() for q in bank['questions']}
    require(len(public) == sum(len(b['questions']) for b in banks.values()) == 2346,
            'Unexpected original public inventory')
    representative = banks[BASE + '/questions.json']
    original_selection = json.loads(git_bytes(root, commit, BASE + '/selection.json'))
    draft_bindings = {G_BASE + '/drafts/' + qid + '-remediation-v1.json':
                      sha(git_bytes(root, commit, G_BASE + '/drafts/' + qid + '-remediation-v1.json'))
                      for qid in ORIGINALS}
    independent_paths = subprocess.check_output(['git', '-C', str(root), 'diff-tree', '--no-commit-id', '--name-only', '-r', REVIEW_COMMIT], text=True).splitlines()
    independent_artifacts = {}
    for path in independent_paths:
        require(path.startswith(str(Path(REVIEW_PATH).parent) + '/'), 'Unexpected independent review commit scope')
        expected = sha(git_bytes(root, REVIEW_COMMIT, path))
        require(sha((root / path).read_bytes()) == expected, 'Missing/changed original independent artifact: ' + path)
        independent_artifacts[path] = expected
    require(len(independent_artifacts) == 42, 'Independent report artifact scope changed')
    require(len(representative['questions']) == 74, 'Unexpected representative baseline')
    return dict(schema_version='sata-remediation-allocation/1', base_commit=commit,
        allocation_rule='Next consecutive MA-RW numbers above every exact tracked textual reservation; sorted original IDs.',
        reservation_scan_scope='Every tracked JSON/JSONL/TXT/MD/PY/JS/HTML, including all public banks, authoring and reserved drafts; no prior review conclusion used.',
        reserved_ids=reserved, reservation_files=reservations, authoring_and_draft_file_sha256=authoring_files,
        public_question_record_hashes=public,
        original_bank_sha256={p: sha(git_bytes(root, commit, p)) for p in PUBLIC_BANKS[:-1]},
        representative_question_hashes={q['question_id']: record_sha(q) for q in representative['questions']},
        representative_source_hashes={sid: record_sha(s) for sid, s in representative['sources'].items()},
        original_selection_sha256=sha(git_bytes(root, commit, BASE + '/selection.json')),
        published_record_baseline_sha256=sha((root / PUBLISHED_BASELINE).read_bytes()),
        preserved_selection={k: original_selection[k] for k in ('recommended_ids', 'replacements', 'holds', 'safety_holds')},
        original_draft_sha256=draft_bindings,
        original_G_source_register_sha256=sha(git_bytes(root, commit, REGISTER)),
        independent_artifact_sha256=independent_artifacts,
        allocations=[dict(original_question_id=old, draft_key=old + '-remediation-v1', question_id=new)
                     for old, new in zip(ORIGINALS, allocated)],
        canonical_audit=False, canonical_release_credit=0, question_audit_credit=0,
        engineering_provenance=ENGINEER)


def load_draft(root, row):
    relative = G_BASE + '/drafts/' + row['draft_key'] + '.json'
    raw = (root / relative).read_bytes()
    allocation = json.loads((root / ALLOCATION).read_text())
    require(sha(raw) == allocation['original_draft_sha256'][relative], 'Reviewed G draft bytes changed: ' + relative)
    return relative, raw, json.loads(raw)


def validate_independent_binding(root):
    raw = (root / REVIEW_PATH).read_bytes()
    require(sha(raw) == REVIEW_SHA, 'Independent draft report working bytes changed')
    allocation = json.loads((root / ALLOCATION).read_text())
    require(len(allocation['independent_artifact_sha256']) == 42, 'Missing independent evidence inventory')
    for relative, expected in allocation['independent_artifact_sha256'].items():
        require(sha((root / relative).read_bytes()) == expected, 'Missing/changed original independent artifact: ' + relative)
    report = json.loads(raw)
    require(report['canonical_audit'] is False and report['canonical_release_credit'] == 0,
            'Unexpected canonical review claim')
    return {r['draft_key']: r for r in report['records']}


def validate_retained_source(root, source):
    require(source['http_status'] == 200 and source['tls_verification'] is True,
            'Unavailable/non-TLS source cannot be proof')
    for path_key, hash_key in [('evidence_path', 'evidence_sha256'),
                               ('text_evidence_path', 'text_sha256'),
                               ('retrieval_metadata_path', 'retrieval_metadata_sha256')]:
        require(sha((root / source[path_key]).read_bytes()) == source[hash_key],
                'Source evidence bytes changed: ' + source['source_id'])
    require(source['raw_sha256'] == source['evidence_sha256'], 'Raw/source payload hash mismatch')


def authoring_payload(root=ROOT):
    allocation = json.loads((root / ALLOCATION).read_text())
    rows = allocation['allocations']
    require([r['original_question_id'] for r in rows] == list(ORIGINALS), 'Unexpected allocation scope')
    require([r['question_id'] for r in rows] == next_rewrite_ids(allocation['reserved_ids'], 3), 'Non-deterministic ID allocation')
    require(len({r['question_id'] for r in rows}) == 3 and
            not {r['question_id'] for r in rows} & set(allocation['reserved_ids']), 'ID allocation collision')
    reviews = validate_independent_binding(root)
    register_raw = (root / REGISTER).read_bytes()
    require(sha(register_raw) == allocation['original_G_source_register_sha256'], 'G source register changed')
    register = json.loads(register_raw)
    sources = {}
    for source in register['sources']:
        validate_retained_source(root, source)
        sid = NAMESPACE + source['source_id']
        sources[sid] = dict(source_id=sid, title=source['source_id'] + ' — G retained official source',
            official_url=source['official_url'], exact_sections=source['exact_sections'],
            checked_at=source['law_checked_date'], access_status='READ_OFFICIAL',
            retrieval_method=source['retrieval_method'] + '; original G retrieval; engineering adapter did not re-read law.',
            source_currency=source['version_or_effective_date_status'],
            verification_scope=source['read_scope'], original_source_id=source['source_id'],
            original_author_commit=AUTHOR_COMMIT, **{k: copy.deepcopy(source[k]) for k in
                ('retrieved_at', 'http_status', 'tls_verification', 'effective_date', 'effective_date_status',
                 'raw_sha256', 'evidence_path', 'evidence_sha256', 'text_evidence_path', 'text_sha256',
                 'retrieval_metadata_path', 'retrieval_metadata_sha256')})
    require(len(sources) == 9, 'Unexpected G source scope')
    old_questions = {q['question_id']: q for path in PUBLIC_BANKS
                     for q in json.loads((root / path).read_text())['questions']}
    questions = []
    for row in rows:
        path, raw, draft = load_draft(root, row)
        review = reviews[row['draft_key']]
        require(review['binding']['path'] == path and review['binding']['source_file_sha256'] == sha(raw),
                'Independent report binds different G source bytes')
        require(review['legal_disposition'] == 'KEEP' and review['realism']['disposition'] == 'PASS' and
                review['independently_expected_choice_ids'] == draft['correct_choice_ids'], 'Draft review does not bind this key')
        scenario, separator, lead = draft['stem'].rpartition('\n\n')
        require(separator and scenario + separator + lead == draft['stem'], 'Cannot split stem losslessly')
        old = old_questions[row['original_question_id']]
        choices = []
        for c in draft['choices']:
            proof = next(p for p in draft['option_proofs'] if p['choice_id'] == c['id'])
            require(proof['option_text_sha256'] == sha(c['text'].encode()), 'Stale G option proof')
            require((proof['author_supported'] == 'YES') == (c['id'] in draft['correct_choice_ids']), 'G proof/key mismatch')
            refs = []
            for authority in proof['authorities']:
                source = sources[NAMESPACE + authority['source_id']]
                require(authority['official_url'] == source['official_url'] and authority['raw_sha256'] == source['raw_sha256'], 'G authority/source mismatch')
                refs.append({**copy.deepcopy(authority), 'source_id': source['source_id']})
            require([(r['source_id'].removeprefix(NAMESPACE), r['exact_section']) for r in refs] ==
                    [tuple(pair) for pair in draft['option_source_specs'][c['id']]], 'G proof/spec mismatch')
            choices.append(dict(id=c['id'], text=c['text'], correct=c['id'] in draft['correct_choice_ids'],
                rationale_ko=draft['explanation']['choice_analysis'][c['id']], authority_refs=refs))
        binding = dict(draft_key=row['draft_key'], source_path=path, source_full_file_sha256=sha(raw),
            source_author_commit=AUTHOR_COMMIT, original_author_provenance=draft['author_provenance'],
            visible_record_sha256=review['safe_visible_record_sha256'],
            independent_draft_review=dict(commit=REVIEW_COMMIT, path=REVIEW_PATH, report_sha256=REVIEW_SHA,
                draft_key=row['draft_key'], canonical_audit=False, current_public_id_assessed=False),
            engineering_provenance=ENGINEER,
            known_author_editor_actor_ids=[draft['author_provenance']['actor_id'], ENGINEER['actor_id']],
            current_id_independent_audit='PENDING',
            additional_coverage_credit=0, question_audit_credit=0, author_review_credit=0,
            canonical_audit=False, canonical_release_credit=0, release_eligible=False,
            public_activation=False)
        questions.append(dict(question_id=row['question_id'], legacy_question_id=row['original_question_id'],
            topic=draft['topic'], area=old['area'], question_type=draft['question_type'],
            scenario=scenario, lead_in=lead, choices=choices,
            core_reasoning_ko=draft['explanation']['core_reasoning'],
            learning_boundary_ko=draft['explanation']['learning_boundary'],
            note_unit_ids=[ref['unit_id'] for ref in old['note_evidence']],
            decision_path=['Apply the unchanged reviewed scenario and each option to its retained primary-source proof.',
                           'Keep distinct actors, conditional reporting recipients, exceptions and recommendation strength as written.'],
            decision_signature='reviewed-G-draft-lossless:' + row['draft_key'],
            difference_from_legacy=draft['design_change_ko'],
            comparison_with_existing_quality=[dict(relationship='NON_ADDITIVE_REMEDIATION_VARIANT',
                material_difference=review['novelty_and_coverage']['finding_ko'], additional_coverage_credit=0)],
            competency_codes=['2.1'], competency_rationale='Existing area2 administration/dispensing pathway; editorial metadata only, not a new legal judgment.',
            exam_outline='MPJE-MA-PRE2027', valid_for_exams_before='2027-03-01',
            archive_only_candidate=True, remediation_candidate=binding))
    return dict(scope='Three lossless, separately identified archive replacement candidates; original HOLDs/default list retained.',
        edition=EDITION, authored_at=REVIEW_DATE, base_commit=allocation['base_commit'],
        review_status='AUTHOR_SOURCE_REVIEW_NOT_INDEPENDENT_AUDIT',
        author_session='/root/independent_case_g', engineering_provenance=ENGINEER,
        source_limitations=['Original G source review and prior E draft review are preserved provenance. No compiled-current-ID audit or new engineering legal review.',
            'PUBLISHED_PRACTICE is delivery metadata, not canonical RELEASED. Root integration/publication remains separate.',
            'Retained version/effective-date unknowns and underlying legal scope are copied without strengthening.'],
        sources=sources, questions=questions)


def validate_preservation(bank, root=ROOT):
    allocation = json.loads((root / ALLOCATION).read_text())
    by_id = {q['question_id']: q for q in bank['questions']}
    for qid, expected in allocation['representative_question_hashes'].items():
        require(qid in by_id and record_sha(by_id[qid]) == expected, 'Existing representative object changed: ' + qid)
    for sid, expected in allocation['representative_source_hashes'].items():
        require(sid in bank['sources'] and record_sha(bank['sources'][sid]) == expected, 'Existing source object changed: ' + sid)
    for path, expected in allocation['original_bank_sha256'].items():
        require(sha((root / path).read_bytes()) == expected, 'Original question archive changed: ' + path)
    for path, expected in allocation['authoring_and_draft_file_sha256'].items():
        require(sha((root / path).read_bytes()) == expected, 'Reserved authoring/draft source changed: ' + path)
    drafts = {r['question_id']: load_draft(root, r)[2] for r in allocation['allocations']}
    for qid, draft in drafts.items():
        require(qid in by_id, 'Missing remediation candidate: ' + qid)
        q = by_id[qid]
        for field in ('stem', 'choices', 'correct_choice_ids', 'question_type', 'topic'):
            require(q[field] == draft[field], 'Reviewed visible wording changed: ' + qid + '/' + field)
        for field, value in draft['explanation'].items():
            require(q['explanation'][field] == value, 'Reviewed Korean explanation changed: ' + qid + '/' + field)
        require(q['stem'] == q['scenario'] + '\n\n' + q['lead_in'], 'Split stem changed')
        require(q['remediation_candidate']['current_id_independent_audit'] == 'PENDING' and
                q['independent_legal_audit'] is q['independent_realism_audit'] is None,
                'Engineering cannot certify current-ID audit')
    require(set(by_id) == set(allocation['representative_question_hashes']) | set(drafts), 'Unexpected representative IDs')
    require(len(bank['sources']) == len(allocation['representative_source_hashes']) + 9, 'Source namespace collision')
    return allocation


def bind_candidate_inventory_row(row, question, root=ROOT):
    """Expose frozen author-source provenance for scheduling, never E review credit.

    The G draft date remains context. checked_at stays empty until a committed
    native current-ID author review passes the narrow source consumer.
    """
    authored = authoring_payload(root)
    matches = [a for a in authored['questions'] if a['question_id'] == question['question_id']]
    require(len(matches) == 1, 'Unallocated remediation inventory ID')
    a = matches[0]
    require(question['remediation_candidate'] == a['remediation_candidate'] and
            question['stem'] == a['scenario'] + '\n\n' + a['lead_in'] and
            question['choices'] == [dict(id=c['id'], text=c['text']) for c in a['choices']] and
            question['correct_choice_ids'] == [c['id'] for c in a['choices'] if c['correct']] and
            question['explanation']['core_reasoning'] == a['core_reasoning_ko'] and
            question['explanation']['choice_analysis'] == {c['id']: c['rationale_ko'] for c in a['choices']} and
            question['explanation']['choice_authorities'] == {c['id']: c['authority_refs'] for c in a['choices']} and
            question['explanation']['learning_boundary'] == a['learning_boundary_ko'],
            'Stale remediation inventory binding')
    require(question['independent_legal_audit'] is question['independent_realism_audit'] is None and
            question['remediation_candidate']['current_id_independent_audit'] == 'PENDING',
            'Candidate cannot inherit compiled-ID audit')
    row.update(disposition='AUDIT_PENDING',
        legal_review_status='DRAFT_SOURCE_REVIEW_BOUND_NOT_CURRENT_ID_AUDIT',
        checked_at=None, checked_at_scope='FORMAL_CURRENT_ID_AUTHOR_REVIEW_REQUIRED',
        source_author_review_date=authored['authored_at'], current_id_author_review_required=True,
        source_author_review_binding=question['remediation_candidate'],
        known_author_editor_actor_ids=question['remediation_candidate']['known_author_editor_actor_ids'],
        reviewer_provenance=dict(author_session=authored['author_session'],
            engineering_provenance=ENGINEER, independent='NOT_RUN_FOR_COMPILED_ID'),
        implementation_status='ARCHIVE_ONLY_REPLACEMENT_CANDIDATE',
        blocker='Compiled current-ID legal and realism review pending; original HOLD/default unchanged.',
        next_action='Assign the actual content author a native current-ID author review before independent assessment.',
        answer_key_assessment='EXACT_G_DRAFT_KEY_COPY_NOT_NEW_ENGINEERING_ASSESSMENT',
        author_review_increment=0, independent_review_credit=0, canonical_release_credit=0)
    from remediation_author_reviews import apply_review
    apply_review(row, question, root)


def validate_published_preservation(data, root=ROOT):
    allocation = json.loads((root / ALLOCATION).read_text())
    raw = (root / PUBLISHED_BASELINE).read_bytes()
    require(sha(raw) == allocation['published_record_baseline_sha256'], 'Published-object baseline snapshot changed')
    baseline = json.loads(raw)
    require(baseline['base_commit'] == allocation['base_commit'] and baseline['question_count'] == 2346,
            'Published-object baseline scope changed')
    by_id = {q['question_id']: q for q in data['questions']}
    for qid, expected in baseline['record_hashes'].items():
        require(qid in by_id and record_sha(by_id[qid]) == expected, 'Existing delivered object changed: ' + qid)


def publication_candidate_manifest(root=ROOT):
    path = root / 'site/practice-expansion/publication.json'
    config = json.loads(path.read_text())
    bank_path = root / BASE / 'questions.json'
    bank_raw = bank_path.read_bytes()
    bank = json.loads(bank_raw)
    validate_preservation(bank, root)
    for addition in config['additional_banks']:
        if addition['collection_id'] == 'representative-20261028':
            addition.update(sha256=sha(bank_raw), question_count=len(bank['questions']),
                            title='대표 재작성 74문항·별도 대체 후보 3문항')
    config['published_total'] = config['question_count'] + sum(a['question_count'] for a in config['additional_banks'])
    config['representative_selection']['sha256'] = sha((root / config['representative_selection']['path']).read_bytes())
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--initialize-allocation', metavar='EXACT_BASE_COMMIT')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--sync-publication-candidate', action='store_true',
                        help='Reconcile proposed local manifest hashes/counts only; does not publish or deploy.')
    args = parser.parse_args()
    if args.initialize_allocation:
        baseline_path = ROOT / PUBLISHED_BASELINE
        baseline_raw = published_baseline_snapshot(ROOT, args.initialize_allocation)
        require(not baseline_path.exists() or baseline_path.read_bytes() == baseline_raw, 'Refusing to replace actual publication baseline')
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_bytes(baseline_raw)
        path = ROOT / ALLOCATION
        payload = encoded(allocation_snapshot(ROOT, args.initialize_allocation))
        require(not path.exists() or path.read_bytes() == payload, 'Refusing to replace frozen ID allocation')
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        review = git_bytes(ROOT, REVIEW_COMMIT, REVIEW_PATH)
        require(sha(review) == REVIEW_SHA, 'Original independent report commit binding mismatch')
    payload = encoded(authoring_payload())
    path = ROOT / AUTHORING
    if args.check:
        require(path.read_bytes() == payload, 'Lossless authoring adapter drift')
    else:
        path.write_bytes(payload)
    print(('Checked ' if args.check else 'Built ') + AUTHORING)
    if args.sync_publication_candidate:
        path = ROOT / 'site/practice-expansion/publication.json'
        payload = encoded(publication_candidate_manifest())
        if args.check:
            require(path.read_bytes() == payload, 'Proposed publication manifest drift')
        else:
            path.write_bytes(payload)
        print(('Checked ' if args.check else 'Prepared candidate ') + str(path.relative_to(ROOT)))


if __name__ == '__main__':
    main()
