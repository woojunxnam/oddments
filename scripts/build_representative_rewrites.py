#!/usr/bin/env python3
"""Build separately versioned representative revisions; never rewrite archived questions.

Author source checks and editorial triage are not canonical independent audits.
The original 355 selection and previous 96 questions remain reproducible inputs.
"""
from __future__ import annotations

import argparse
import collections
import copy
from datetime import date
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'practice_expansion/2026-10-28-representative'
REPORTS = ROOT / 'reports/representative-rewrite'
ORIGINAL_SELECTION = ROOT / 'practice_expansion/2026-10-27-quality/selection.json'
COLLECTION = 'representative-20261028'
INITIAL_EDITION = '2026-10-28.representative1'
EDITION = '2026-10-29.representative3'
REVIEW_DATE = '2026-10-29'
PUBLISHED_UNIT1_COMMIT = 'f112d3578664aa51785ba4596547e8d722fad36c'
BASE_COMMIT = 'b5bd6b02c7ea8a5c6731871fa6e330ac6795fd36'
ARCHIVES = [
    'practice_expansion/2026-10-23/candidates/questions.json',
    'practice_expansion/2026-10-26-plus/questions.json',
    'practice_expansion/2026-10-27-quality/questions.json',
]
REVIEW_STATUS = 'AUTHOR_SOURCE_REVIEW_NOT_INDEPENDENT_AUDIT'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def read(path: Path):
    return json.loads(path.read_text())


def content_hash(question: dict) -> str:
    body = {k: v for k, v in question.items() if k != 'content_sha256'}
    return digest(json.dumps(body, ensure_ascii=False, sort_keys=True).encode())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def norm(text):
    return re.sub(r'[^\w]+', ' ', text.casefold()).strip()


def verify_published_baseline(bank):
    """Read-only protection of already-published revisions, including metadata."""
    baseline = read(REPORTS / 'published-unit1-baseline.json')
    require(baseline['baseline_commit'] == PUBLISHED_UNIT1_COMMIT,
            'The published-unit1 baseline must remain anchored to its merged commit.')
    require(len(baseline['question_hashes']) == 46, 'Published unit1 protection lost questions.')
    questions = {q['question_id']: q for q in bank['questions']}
    for key, records in [('question_hashes', questions), ('source_hashes', bank['sources'])]:
        for record_id, expected in baseline[key].items():
            require(record_id in records, 'Missing published record: ' + record_id)
            actual = digest(json.dumps(records[record_id], ensure_ascii=False, sort_keys=True).encode())
            require(actual == expected, 'Published content changed under an existing ID: ' + record_id)
    for relative, expected in baseline['authoring_files'].items():
        require(digest((ROOT / relative).read_bytes()) == expected,
                'Published unit1 authoring source changed: ' + relative)


def pattern_metrics(questions):
    """Descriptive signals, never a legal-error or semantic-duplicate count."""
    stems = collections.Counter(norm(q['stem']) for q in questions)
    packs = collections.Counter(tuple(sorted(norm(c['text']) for c in q['choices'])) for q in questions)
    choices = collections.Counter(norm(c['text']) for q in questions for c in q['choices'])
    sata = [q for q in questions if q['question_type'] == 'SATA']
    sba = [q for q in questions if q['question_type'] == 'SBA']
    longest = sum(
        len(next(c['text'] for c in q['choices'] if c['id'] == q['correct_choice_ids'][0]))
        > max(len(c['text']) for c in q['choices'] if c['id'] not in q['correct_choice_ids'])
        for q in sba
    )
    return dict(
        questions=len(questions), types=dict(collections.Counter(q['question_type'] for q in questions)),
        paired_case_questions=sum('Case A:' in q['stem'] and 'Case B:' in q['stem'] for q in questions),
        all_correct_sata=sum(len(q['correct_choice_ids']) == len(q['choices']) for q in sata),
        sata_correct_count_distribution=dict(sorted(collections.Counter(str(len(q['correct_choice_ids'])) for q in sata).items())),
        sba_answer_letters=dict(sorted(collections.Counter(q['correct_choice_ids'][0] for q in sba).items())),
        sole_longest_sba_key_heuristic=longest,
        repeated_normalized_stem_occurrences=sum(n - 1 for n in stems.values()),
        questions_in_identical_option_sets=sum(n for n in packs.values() if n > 1),
        repeated_choice_slots=sum(n - 1 for n in choices.values()),
        distinct_normalized_choices=len(choices),
        answer_patterns=dict(sorted(collections.Counter(','.join(q['correct_choice_ids']) for q in questions).items())),
    )


def build():
    original_selection = read(ORIGINAL_SELECTION)
    original_banks = [read(ROOT / path) for path in ARCHIVES]
    original_questions = [q for bank in original_banks for q in bank['questions']]
    old_by_id = {q['question_id']: q for q in original_questions}
    legacy_ids = set(original_selection['recommended_ids']) - set(original_selection['new_ids'])
    require(len(legacy_ids) == 355, 'The baseline representative set changed; reconcile explicitly.')
    guide_raw = (ROOT / 'notes/guide.json').read_bytes()
    guide = json.loads(guide_raw)
    units = {u['id']: (c['id'], u) for c in guide['chapters'] for u in c['units']}
    source_files = sorted((BASE / 'authoring').glob('*.json'))
    require(bool(source_files), 'No individually authored source files.')
    sources, authored, holds, reused, input_hashes, scope_notes = {}, [], [], [], {}, []
    author_metadata = {}
    for path in source_files:
        d = read(path)
        require(d['review_status'] == REVIEW_STATUS, f'{path}: unsupported review claim')
        original_file = path.name in {'01_personnel.json', '02_clinical_authority.json'}
        authored_at = d.get('authored_at', '2026-10-28' if original_file else None)
        require(bool(authored_at), f'{path}: missing authoring date')
        require(date.fromisoformat(authored_at) <= date.fromisoformat(REVIEW_DATE),
                f'{path}: future authoring date')
        item_edition = d.get('edition', INITIAL_EDITION if original_file else None)
        require(isinstance(item_edition, str)
                and re.fullmatch(r'\d{4}-\d{2}-\d{2}\.representative\d+', item_edition)
                and item_edition.split('.')[0] == authored_at,
                f'{path}: authoring edition/date mismatch')
        input_hashes[str(path.relative_to(ROOT))] = digest(path.read_bytes())
        scope_notes.append(dict(authoring_file=str(path.relative_to(ROOT)),
            source_limitations=d.get('source_limitations', []),
            legal_reconciliation_notes=d.get('legal_reconciliation_notes', [])))
        for sid, s in d['sources'].items():
            host = (urlparse(s['official_url']).hostname or '').lower()
            require(host in {'www.mass.gov', 'mass.gov', 'malegislature.gov', 'www.ecfr.gov', 'www.dea.gov', 'www.deadiversion.usdoj.gov', 'www.fda.gov', 'accessdata.fda.gov', 'www.accessdata.fda.gov', 'dailymed.nlm.nih.gov', 'nabp.pharmacy', 'www.hhs.gov', 'www.cdc.gov'}, f'Non-official source: {sid}')
            require(s['official_url'].startswith('https://'), sid)
            require(date.fromisoformat(s['checked_at']) <= date.fromisoformat(authored_at)
                    and s['access_status'] == 'READ_OFFICIAL', f'{sid}: invalid official text read/date')
            require(s.get('verification_scope') and s.get('retrieval_method'), f'{sid}: missing read scope/provenance')
            if sid in sources:
                require(sources[sid]['url'] == s['official_url'], f'Source collision: {sid}')
                for field in ['checked_at', 'access_status', 'retrieval_method', 'source_currency']:
                    require(sources[sid].get(field) == s.get(field),
                            f'{sid}: conflicting {field}; record a distinct source ID')
                # Two authors may have read different, nonconflicting sections of one source.
                sources[sid]['exact_sections'] = sorted(set(sources[sid].get('exact_sections', [])) | set(s.get('exact_sections', [])))
                if s['verification_scope'] not in sources[sid]['verification_scope']:
                    sources[sid]['verification_scope'] += '\nAdditional author read: ' + s['verification_scope']
                continue
            sources[sid] = {**copy.deepcopy(s), 'id': sid, 'url': s['official_url'], 'source_class': 'PUBLIC_OFFICIAL'}
        authored.extend(d['questions'])
        for question in d['questions']:
            author_metadata[question['question_id']] = (authored_at, item_edition)
        holds.extend(d.get('holds', []))
        reused.extend(d.get('reuse_existing', []))
    # Optional separately documented editorial holds do not alter archive bytes or keys.
    extra_holds = REPORTS / 'default-holds.json'
    if extra_holds.exists():
        holds.extend(read(extra_holds)['holds'])
        input_hashes[str(extra_holds.relative_to(ROOT))] = digest(extra_holds.read_bytes())
    require(len({q['question_id'] for q in authored}) == len(authored), 'Duplicate new IDs')
    addressed = [q['legacy_question_id'] for q in authored] + [h['legacy_question_id'] for h in holds] + [q['legacy_question_id'] for q in reused]
    require(len(set(addressed)) == len(addressed), 'A legacy question has more than one disposition')
    require(set(addressed) <= legacy_ids, 'Disposition outside the original 355')
    items = []
    for a in sorted(authored, key=lambda q: q['question_id']):
        qid, legacy_id = a['question_id'], a['legacy_question_id']
        authored_at, item_edition = author_metadata[qid]
        require(re.fullmatch(r'MA-RW-\d{4}', qid) and qid not in old_by_id, f'ID not new: {qid}')
        require(a['exam_outline'] == 'MPJE-MA-PRE2027' and a['valid_for_exams_before'] == '2027-03-01', qid + ': outline')
        require(a['question_type'] in {'SBA', 'SATA'}, qid + ': type')
        require(4 <= len(a['choices']) <= 5, qid + ': choice count')
        ids = [c['id'] for c in a['choices']]
        require(ids == list('ABCDE'[:len(ids)]), qid + ': stable choice IDs')
        correct = [c['id'] for c in a['choices'] if c['correct']]
        require(bool(correct) and (a['question_type'] != 'SBA' or len(correct) == 1), qid + ': key')
        require(len(set(norm(c['text']) for c in a['choices'])) == len(ids), qid + ': duplicate choices')
        require(len(set(c['rationale_ko'] for c in a['choices'])) == len(ids), qid + ': duplicate rationales')
        require(not re.search(r'[가-힣]', a['scenario'] + a['lead_in'] + ' '.join(c['text'] for c in a['choices'])), qid + ': English item')
        require(a.get('decision_signature') and a.get('difference_from_legacy') and a.get('comparison_with_existing_quality'), qid + ': no editorial decision')
        require(len(a.get('decision_path', [])) >= 2 and a.get('competency_codes'), qid + ': reasoning/competency')
        primary_refs, choice_refs = [], {}
        for c in a['choices']:
            require(re.search(r'[가-힣]', c['rationale_ko']), qid + ': Korean rationale')
            require(c.get('authority_refs'), qid + '/' + c['id'] + ': no authority')
            for ref in c['authority_refs']:
                require(ref['source_id'] in sources and ref.get('exact_section'), qid + ': invalid exact authority')
                if ref not in primary_refs:
                    primary_refs.append(ref)
            choice_refs[c['id']] = copy.deepcopy(c['authority_refs'])
        evidence, inherited_source_ids = [], []
        for uid in a['note_unit_ids']:
            require(uid in units, qid + ': unknown note ' + uid)
            chapter, unit = units[uid]
            inherited_source_ids.extend(unit['source_ids'])
            evidence.append(dict(unit_id=uid, title=unit['title'], body_sha256=unit['body_sha256'],
                inherited_note_review_date=unit['source_review_date'], inherited_flags=unit['flags'],
                url=f'https://woojunxnam.github.io/oddments/notes/#chapter/{chapter}/{uid}'))
        require(bool(evidence), qid + ': no note link')
        for sid in inherited_source_ids:
            if sid not in sources:
                sources[sid] = copy.deepcopy(guide['sources'][sid])
        primary_ids = list(dict.fromkeys(ref['source_id'] for ref in primary_refs))
        old = old_by_id[legacy_id]
        item = dict(
            question_id=qid, family_id=old['family_id'], revision_of=legacy_id, content_version=1,
            history_policy='NEW_ID_NO_ATTEMPT_OR_BOOKMARK_MIGRATION', topic=a['topic'], area=a['area'],
            question_type=a['question_type'], practice_angle='individually-authored-application',
            collection_id=COLLECTION, scenario=a['scenario'], lead_in=a['lead_in'],
            stem=a['scenario'] + '\n\n' + a['lead_in'],
            choices=[dict(id=c['id'], text=c['text']) for c in a['choices']], correct_choice_ids=correct,
            explanation=dict(core_reasoning=a['core_reasoning_ko'],
                choice_analysis={c['id']: c['rationale_ko'] for c in a['choices']},
                choice_authorities=choice_refs,
                learning_boundary='기존 대표 문항을 별도 사례로 다시 작성했습니다. 원본과 새 문항의 풀이 기록은 각각 보존됩니다. 작성자 출처 대조와 편집 검토이며 독립 법규 감사 또는 실제 시험 난도 보정은 아닙니다.'),
            note_evidence=evidence, source_ids=list(dict.fromkeys(inherited_source_ids + primary_ids)),
            authority='; '.join(dict.fromkeys(ref['exact_section'] for ref in primary_refs)),
            primary_source_read_records=[dict(source_id=sid, accessed_at=sources[sid]['checked_at'],
                exact_sections=list(dict.fromkeys(r['exact_section'] for r in primary_refs if r['source_id'] == sid)),
                access_status=sources[sid]['access_status'], retrieval_method=sources[sid]['retrieval_method'],
                source_currency=sources[sid].get('source_currency'), scope=sources[sid]['verification_scope']) for sid in primary_ids],
            additional_primary_evidence=[dict(source_id=sid, title=sources[sid]['title'], url=sources[sid]['url'],
                accessed_at=sources[sid]['checked_at'], scope='; '.join(dict.fromkeys(r['exact_section'] for r in primary_refs if r['source_id'] == sid))) for sid in primary_ids],
            authority_level='OFFICIAL_PRIMARY_TEXT_AUTHOR_REVIEW', primary_source_verification=REVIEW_STATUS,
            source_boundary=f'이 사례의 선택지별 조항은 {authored_at} 공식 본문과 대조했습니다. 공식 URL의 추출문 열람 방식·확인 범위·문서 개정일은 출처 기록을 참조하세요. 연결 노트의 기존 확인일과 OPEN은 별도이며 전체 노트 재검증이나 독립 감사 완료를 뜻하지 않습니다.',
            inherited_flags=list(dict.fromkeys(flag for e in evidence for flag in e['inherited_flags'])),
            decision_path=a['decision_path'], decision_signature=a['decision_signature'],
            difference_from_legacy=a['difference_from_legacy'], comparison_with_existing_quality=a['comparison_with_existing_quality'],
            competency_codes=a['competency_codes'], competency_rationale=a['competency_rationale'],
            exam_outline=a['exam_outline'], valid_for_exams_before=a['valid_for_exams_before'],
            authored_at=authored_at, edition=item_edition, publication_status='PUBLISHED_PRACTICE',
            online_practice_enabled=True, verification_status='NOT_INDEPENDENTLY_REVIEWED',
            independent_legal_audit=None, independent_realism_audit=None,
            duplicate_review_status='EDITORIAL_DECISION_PATH_COMPARISON_NOT_GLOBAL_SEMANTIC_CERTIFICATION',
            difficulty_status='NOT_CALIBRATED', _statement_truth={c['id']: c['correct'] for c in a['choices']},
        )
        if a.get('notes_revision'):
            from notes_revision import load_notes
            item['notes_revision'] = load_notes(ROOT)['revision_provenance']
            require(item['notes_revision']['id'] == a['notes_revision'], qid + ': stale notes revision')
        item['content_sha256'] = content_hash(item)
        if qid in {'MA-RW-0045', 'MA-RW-0046', 'MA-RW-0047'}:
            item['authority_caveats'] = ['일반 247 CMR 8의 예방접종 제한 문구와, technician을 명시한 105 CMR 700.004(B)(6) 및 DPH/Board/DCP Policy 2023-02의 특정 경로를 함께 확인했습니다. 일반 문구가 폐지됐다고 판단한 것은 아닙니다. 이 문항은 해당 경로의 특정 교육·자격 요건만 평가하며 모든 투여 권한을 포괄 승인하지 않습니다.']
            item['source_boundary'] += ' ' + item['authority_caveats'][0]
            item['content_sha256'] = content_hash(item)
        items.append(item)
    replacements = [dict(legacy_question_id=q['revision_of'], replacement_question_id=q['question_id'],
        kind='NEW_CASE', content_sha256=q['content_sha256']) for q in items]
    for reuse in reused:
        existing = reuse['existing_question_id']
        require(existing in original_selection['new_ids'], 'Reuse target is not in unchanged previous96')
        replacements.append(dict(legacy_question_id=reuse['legacy_question_id'], replacement_question_id=existing,
            kind='EXISTING_QUALITY_CASE', reason=reuse['rationale']))
    replacement_map = {r['legacy_question_id']: r['replacement_question_id'] for r in replacements}
    held_ids = {h['legacy_question_id'] for h in holds}
    archive_notice_ids = held_ids | {qid for h in holds for qid in h.get('affected_archive_ids', [])}
    require(archive_notice_ids <= set(old_by_id), 'Unknown related archive hold ID')
    recommended = []
    for old_id in original_selection['recommended_ids']:
        if old_id in held_ids:
            continue
        chosen = replacement_map.get(old_id, old_id)
        if chosen not in recommended:
            recommended.append(chosen)
    all_questions = original_questions + items
    by_id = {q['question_id']: q for q in all_questions}
    require(set(recommended) <= set(by_id), 'Unknown recommended ID')
    require(not archive_notice_ids & set(recommended), 'An affected archive representative needs an explicit default hold')
    require(len({by_id[i]['family_id'] for i in recommended}) == len(recommended), 'Repeated family in default')
    new_metrics = pattern_metrics(items)
    require(new_metrics['repeated_normalized_stem_occurrences'] == 0 and new_metrics['questions_in_identical_option_sets'] == 0, 'Exact duplicate among new cases')
    selection = dict(
        edition=EDITION, base_commit=BASE_COMMIT, baseline_selection_path=str(ORIGINAL_SELECTION.relative_to(ROOT)),
        baseline_selection_sha256=digest(ORIGINAL_SELECTION.read_bytes()), recommended_ids=recommended,
        new_ids=[q['question_id'] for q in items], previous_quality_ids=original_selection['new_ids'],
        replacements=replacements, holds=holds, history_policy='All legacy and previous96 IDs/keys remain. No progress, attempt, or bookmark migration. Cross-links are informational only.',
        stats=dict(recommended=len(recommended), legacy_representatives_remaining=sum(i in legacy_ids for i in recommended),
            baseline_legacy_representatives=355, newly_authored_replacements=len(items), previous_quality=96,
            replaced_by_existing_quality=len(reused), held_from_default=len(holds), available_total=len(all_questions)),
        input_hashes=input_hashes,
        scope='Cumulative individually reviewed implementation units. Remaining legacy representatives have editorial triage only unless separately recorded. All archived variants remain accessible and Chaos10 still samples the complete published corpus with replacement.',
    )
    selection['stats']['archive_ids_with_review_notice'] = len(archive_notice_ids)
    bank = dict(schema_version='notes-practice-representative/1', edition=EDITION, authored_at='2026-10-28', updated_at=REVIEW_DATE,
        base_commit=BASE_COMMIT, publication_status='PUBLISHED_PRACTICE', independent_review_status='NOT_INDEPENDENTLY_REVIEWED',
        input_guide_sha256=digest(guide_raw), input_guide_edition=guide['edition'],
        default_jurisdiction='Massachusetts', intended_outline_window='Examinations before 2027-03-01',
        construction='Individually written replacement scenarios, distinct IDs, explicit legacy mapping. Same-law boundary extensions are identified. No variant multiplication or independent audit claim.',
        stats=dict(questions=len(items), families=len({q['family_id'] for q in items})),
        source_authoring_hashes=input_hashes, authoring_scope_notes=scope_notes, sources=sources, questions=items)
    verify_published_baseline(bank)
    metrics = dict(date=REVIEW_DATE, base_commit=BASE_COMMIT,
        method='Exact text normalization retains numbers. Length and key-pattern statistics are review signals, not validity findings. Semantic findings are recorded separately by editors.',
        baseline_legacy_355=pattern_metrics([old_by_id[i] for i in sorted(legacy_ids)]),
        baseline_default_451=pattern_metrics([old_by_id[i] for i in original_selection['recommended_ids']]),
        revised_unit=new_metrics, current_default=pattern_metrics([by_id[i] for i in recommended]),
        baseline_full_2272=pattern_metrics(original_questions), current_full=pattern_metrics(all_questions),
        protected_input_hashes={p: digest((ROOT / p).read_bytes()) for p in ARCHIVES},
        limits=['The full archive is intentionally retained, so old duplicates remain in all-variants/Chaos10.',
                'No before/after global semantic-duplicate number is inferred from lexical statistics.',
                'No canonical independent audit is created by this builder.'])
    return {BASE / 'questions.json': bank, BASE / 'selection.json': selection, REPORTS / 'pattern-metrics.json': metrics}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail on any generated-file drift, without writing.')
    args = parser.parse_args()
    for path, data in build().items():
        payload = encoded(data)
        if args.check:
            require(path.exists() and path.read_bytes() == payload, f'Generated drift: {path.relative_to(ROOT)}')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        print(('Checked ' if args.check else 'Built ') + str(path.relative_to(ROOT)))


if __name__ == '__main__':
    main()
