#!/usr/bin/env python3
"""Join the immutable 355-item editorial triage with actual implementation records.

This ledger does not turn editorial triage or author source review into an
independent legal audit. The original triage is copied without changing its
NOT_REVERIFIED legal findings; implementation is a separate dimension.
"""
from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports/representative-rewrite'
TRIAGE = REPORTS / 'legacy-editorial-triage.json'
BASELINE_SELECTION = ROOT / 'practice_expansion/2026-10-27-quality/selection.json'
REVISION_BASE = ROOT / 'practice_expansion/2026-10-28-representative'
SELECTION = REVISION_BASE / 'selection.json'
REVISION_BANK = REVISION_BASE / 'questions.json'
BASE_COMMIT = 'b5bd6b02c7ea8a5c6731871fa6e330ac6795fd36'
ARCHIVES = (
    'practice_expansion/2026-10-23/candidates/questions.json',
    'practice_expansion/2026-10-26-plus/questions.json',
    'practice_expansion/2026-10-27-quality/questions.json',
)
IMPLEMENTATION_STATUSES = (
    'REWRITTEN_NEW_ID', 'REUSED_EXISTING_QUALITY',
    'HOLD_FROM_DEFAULT', 'NOT_YET_IMPLEMENTED',
)
EDITORIAL_STATUSES = ('KEEP', 'MINOR_EDIT', 'MAJOR_REWRITE', 'REPLACE', 'HOLD_FOR_LEGAL_REVIEW')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def relative(path):
    return str(path.relative_to(ROOT))


def source_path(value):
    path = (ROOT / value).resolve()
    require(ROOT in path.parents, 'Input path escapes repository: ' + value)
    return path


def counter(values):
    return dict(sorted(collections.Counter(values).items()))


def build_ledger():
    triage = read(TRIAGE)
    selection = read(SELECTION)
    baseline = read(BASELINE_SELECTION)
    bank = read(REVISION_BANK)
    require(triage['base_commit'] == selection['base_commit'] == BASE_COMMIT,
            'Unexpected baseline commit; reconcile the ledger explicitly.')
    require(triage['review_scope'] == 'EDITORIAL_TRIAGE_ONLY', 'Unexpected triage scope.')
    require(triage['canonical_independent_audit'] is False,
            'Editorial input must not assert a canonical independent audit.')
    require(triage['official_source_reverification_performed'] is False,
            'This ledger preserves the original NOT_REVERIFIED triage contract.')
    require(selection['baseline_selection_sha256'] == digest(BASELINE_SELECTION.read_bytes()),
            'Baseline selection no longer matches the revision input.')

    # Confirm the old material underlying the review still has the recorded bytes.
    verified_triage_inputs = []
    for entry in triage['input_files']:
        path = source_path(entry['path'])
        actual = digest(path.read_bytes())
        require(actual == entry['sha256'], 'Reviewed source changed: ' + entry['path'])
        verified_triage_inputs.append(copy.deepcopy(entry))

    legacy_ids = set(baseline['recommended_ids']) - set(baseline['new_ids'])
    require(len(legacy_ids) == 355, 'Expected the original 355 representatives.')
    original = {}
    for name in ARCHIVES:
        for question in read(ROOT / name)['questions']:
            qid = question['question_id']
            require(qid not in original, 'Duplicate archived question ID: ' + qid)
            original[qid] = question
    require(legacy_ids <= original.keys(), 'An original representative is missing.')

    items = triage['items']
    triage_ids = [item['question_id'] for item in items]
    require(len(triage_ids) == len(set(triage_ids)) == 355,
            'Triage must contain 355 distinct individual records.')
    require(set(triage_ids) == legacy_ids, 'Triage does not cover the baseline representatives.')
    require(all(item['review_status'] in EDITORIAL_STATUSES for item in items), 'Unknown editorial triage status.')
    require(len({item['selection_index'] for item in items}) == 355,
            'Duplicate editorial selection index.')
    recommended = set(selection['recommended_ids'])
    require(len(recommended) == len(selection['recommended_ids']),
            'Duplicate current default ID.')
    fresh = {q['question_id']: q for q in bank['questions']}
    require(len(fresh) == len(bank['questions']), 'Duplicate new-bank ID.')
    require(set(selection['new_ids']) == set(fresh), 'Selection/new-bank ID mismatch.')
    require(set(baseline['new_ids']) <= recommended, 'The previous96 must remain recommended.')

    replacements = {}
    for record in selection['replacements']:
        qid = record['legacy_question_id']
        require(qid in legacy_ids and qid not in replacements, 'Invalid duplicate replacement: ' + qid)
        replacements[qid] = record
    holds = {}
    for record in selection['holds']:
        qid = record['legacy_question_id']
        require(qid in legacy_ids and qid not in holds, 'Invalid duplicate hold: ' + qid)
        require(record.get('reason'), 'Hold without a reason: ' + qid)
        holds[qid] = record
    require(not replacements.keys() & holds.keys(), 'A representative is both replaced and held.')
    archive_notice_ids = set(holds) | {
        qid for record in holds.values() for qid in record.get('affected_archive_ids', [])
    }
    archive_notice_ids |= {
        qid for notice in selection.get('archive_review_notices', []) for qid in notice['question_ids']
    }
    require(archive_notice_ids <= original.keys(), 'A related archive warning refers to an unknown original ID.')
    require(not archive_notice_ids & recommended, 'An archive item carrying a hold warning remains in the default pool.')

    questions = []
    for item in sorted(items, key=lambda x: x['selection_index']):
        qid = item['question_id']
        require(item['family_id'] == original[qid]['family_id'], 'Legacy family changed: ' + qid)
        legal = item['editorial_judgment']['legal_correctness']
        require(legal['status'] == 'NOT_REVERIFIED' and legal['fresh_primary_source_check'] is False,
                'Original editorial legal finding must remain NOT_REVERIFIED: ' + qid)
        implementation = {
            'legacy_id_retained_in_archive': True,
            'legacy_is_in_current_default': qid in recommended,
            'replacement_question_id': None,
            'new_independent_legal_audit_created': False,
        }
        if qid in replacements:
            record = replacements[qid]
            target = record['replacement_question_id']
            require(qid not in recommended and target in recommended, 'Invalid default replacement: ' + qid)
            implementation['replacement_question_id'] = target
            implementation['selection_record'] = copy.deepcopy(record)
            if record['kind'] == 'NEW_CASE':
                require(target in fresh, 'Missing separately authored replacement: ' + target)
                new = fresh[target]
                require(new['revision_of'] == qid and new['family_id'] == item['family_id'],
                        'Replacement lineage mismatch: ' + qid)
                require(record['content_sha256'] == new['content_sha256'],
                        'Replacement content hash differs from selection: ' + target)
                require(new['independent_legal_audit'] is None and new['independent_realism_audit'] is None,
                        'Unexpected independent-audit evidence on a newly authored case: ' + target)
                status = 'REWRITTEN_NEW_ID'
                implementation.update(
                    replacement_content_sha256=new['content_sha256'],
                    replacement_source_review_status=new['primary_source_verification'],
                    replacement_verification_status=new['verification_status'],
                    history_policy=new['history_policy'],
                    implementation_basis='Separate new case recorded in the generated bank and current selection; original content is unchanged.',
                )
            elif record['kind'] == 'EXISTING_QUALITY_CASE':
                require(target in set(baseline['new_ids']) and target in original,
                        'Reuse target must be an unchanged previous96 case: ' + target)
                status = 'REUSED_EXISTING_QUALITY'
                implementation.update(
                    reuse_reason=record['reason'],
                    replacement_source_review_status='EXISTING_QUALITY_CASE_NO_FRESH_REVIEW_ASSERTED_BY_THIS_LEDGER',
                    history_policy='Original and existing target IDs retain separate histories; no migration.',
                    implementation_basis='Selection redirects the default representative to an already-existing quality case; no new case is counted.',
                )
            else:
                raise ValueError('Unknown replacement kind: ' + record['kind'])
        elif qid in holds:
            require(qid not in recommended, 'Held question remains in default: ' + qid)
            status = 'HOLD_FROM_DEFAULT'
            implementation.update(
                hold=copy.deepcopy(holds[qid]),
                implementation_basis='Excluded only from the default pool; archived question, answer and existing records remain accessible with the review warning.',
            )
        else:
            require(qid in recommended, 'Unrecorded removal from the default pool: ' + qid)
            status = 'NOT_YET_IMPLEMENTED'
            implementation['implementation_basis'] = 'Individual editorial triage exists; no rewrite, reuse or hold implementation is recorded in this selection.'

        questions.append(dict(
            question_id=qid, family_id=item['family_id'], topic=item['topic'],
            editorial_status=item['review_status'], editorial_priority=item['priority'],
            legacy_legal_correctness=copy.deepcopy(legal),
            editorial_triage=copy.deepcopy(item),
            implementation_status=status, implementation=implementation,
        ))

    counts = {status: sum(row['implementation_status'] == status for row in questions)
              for status in IMPLEMENTATION_STATUSES}
    expected = selection['stats']
    require(counts['REWRITTEN_NEW_ID'] == expected['newly_authored_replacements'], 'Rewrite count mismatch.')
    require(counts['REUSED_EXISTING_QUALITY'] == expected['replaced_by_existing_quality'], 'Reuse count mismatch.')
    require(counts['HOLD_FROM_DEFAULT'] == expected['held_from_default'], 'Hold count mismatch.')
    require(counts['NOT_YET_IMPLEMENTED'] == expected['legacy_representatives_remaining'], 'Remaining count mismatch.')
    require(len(recommended) == expected['recommended'], 'Default count mismatch.')
    require(len(archive_notice_ids) == expected.get('archive_ids_with_review_notice', len(holds)),
            'Related archive-warning count mismatch.')

    return dict(
        schema_version='representative-editorial-implementation-ledger/1',
        base_commit=BASE_COMMIT, reviewed_at=triage['reviewed_at'],
        implementation_updated_at=bank.get('updated_at', bank['authored_at']), selection_edition=selection['edition'],
        scope='355 individual editorial triage records joined with explicit implementation records. This generated join performs no new legal review.',
        canonical_independent_audit_created=False,
        official_source_reverification_performed_by_ledger=False,
        original_editorial_triage_preserved=True,
        subsequent_source_bound_archive_notices=copy.deepcopy(selection.get('archive_review_notices', [])),
        input_hashes={relative(path): digest(path.read_bytes()) for path in (TRIAGE, BASELINE_SELECTION, SELECTION, REVISION_BANK)},
        verified_original_triage_inputs=verified_triage_inputs,
        editorial_triage_metadata={key: copy.deepcopy(value) for key, value in triage.items() if key != 'items'},
        counts=dict(
            original_representatives=355, individual_editorial_records=len(questions),
            original_editorial_statuses={status: sum(row['editorial_status'] == status for row in questions)
                                         for status in EDITORIAL_STATUSES},
            original_legal_statuses=counter(row['legacy_legal_correctness']['status'] for row in questions),
            implementation_statuses=counts, current_default=len(recommended),
            archive_ids_with_review_notice=len(archive_notice_ids),
            previous_quality_retained=len(baseline['new_ids']),
            newly_authored_replacement_questions=len(fresh),
            originals_rewritten_in_place=0, originals_deleted=0,
            canonical_independent_audits_created=0,
        ),
        interpretation_ko=[
            'editorial_status는 원본을 읽은 편집자의 최초 판정이다. implementation_status는 현재 파일·selection으로 확인되는 반영 상태이며 서로 덮어쓰지 않는다.',
            '원본 355개 모두의 legal_correctness는 기존 triage대로 NOT_REVERIFIED이다. 새 ID에 대한 작성자 출처 검토가 원본의 법규 재검증이나 독립 감사로 소급되지 않는다.',
            '후속 원본 ID별 법규 대조는 reports/full-corpus-review/question-ledger.jsonl에 별도로 기록한다. 현재 오류·조건부 안내는 source-bound archive notices이며 과거 triage나 canonical 상태를 덮어쓰지 않는다.',
            'REWRITTEN_NEW_ID는 별도 새 사례의 작성·반영을 뜻한다. REUSED_EXISTING_QUALITY는 이미 있는 96개 중 한 사례를 재사용한 것이며 신규 작성 수에 넣지 않는다.',
            'HOLD_FROM_DEFAULT는 기본 목록에서의 보류이다. 원본 파일·정답·기존 학습 기록을 삭제하거나 바꾸지 않는다.',
            'NOT_YET_IMPLEMENTED는 편집 검토만 완료된 범위이다. 355개 전부가 수정·교체 또는 법규 감사 완료되었다고 해석하면 안 된다.',
        ],
        questions=questions,
    )


def cell(value):
    return ' '.join(str(value).split()).replace('|', '\\|')


def render_markdown(ledger):
    counts = ledger['counts']
    lines = [
        '# 기존 대표 355문항: 편집 판정과 실제 반영 원장', '',
        f"기준 main: `{ledger['base_commit']}` · 현재 selection: `{ledger['selection_edition']}`", '',
        f"원문 편집 검토일: {ledger['reviewed_at']} · 구현 상태 갱신일: {ledger['implementation_updated_at']}", '',
        '이 문서는 개별 편집 triage와 현재 반영 기록을 결합한 결과입니다. 자동 생성 과정에서 법규를 재검증하거나 독립 감사 기록을 만들지 않습니다.', '',
        '## 실제 반영 상태', '',
        '| 상태 | 문항 수 |', '|---|---:|',
    ]
    lines.extend(f'| {status} | {number} |' for status, number in counts['implementation_statuses'].items())
    lines += ['', f"기본 목록 {counts['current_default']}개에는 기존 고품질 {counts['previous_quality_retained']}개가 유지됩니다. 별도 작성한 재작성 사례는 {counts['newly_authored_replacement_questions']}개입니다. 원본의 제자리 수정·삭제 및 새 canonical 독립 감사는 각각 0개입니다.", '',
              f"대표 보류·관련 변형·후속 오류 또는 조건부 판단을 합쳐 원본 {counts['archive_ids_with_review_notice']}개에 검토 안내가 연결됩니다. 이 수는 대표 355개 중 보류 수와 별개이며 전체 목록·Chaos에서 원본 접근을 없애지 않습니다.", '',
              '## 최초 편집 판정 보존', '', '| 최초 판정 | 문항 수 |', '|---|---:|']
    lines.extend(f'| {status} | {number} |' for status, number in counts['original_editorial_statuses'].items())
    lines += ['', '원본 법규 상태는 355개 모두 **NOT_REVERIFIED**로 유지됩니다. 새 ID의 작성자 출처 확인과 원본·전체 corpus의 독립 법률 감사를 구별합니다.', '']
    lines.extend('- ' + note for note in ledger['interpretation_ko'])
    lines += ['', '## 문항별 원장', '',
              '전체 선택지 분석·출처 관찰·기계적 신호와 기존 triage 원문은 [audit-ledger.json](audit-ledger.json)의 `editorial_triage`에 그대로 보존됩니다.', '',
              '| 원본 ID | Family | 최초 판정 / 우선순위 | 실제 반영 | 대상 ID | 원본 법규 상태 | 개별 편집 발견사항 |',
              '|---|---|---|---|---|---|---|']
    for row in ledger['questions']:
        target = row['implementation']['replacement_question_id'] or '—'
        finding = row['editorial_triage']['editorial_judgment']['finding_ko']
        if row['implementation_status'] == 'HOLD_FROM_DEFAULT':
            finding += ' 현재 보류 이유: ' + row['implementation']['hold']['reason']
        fields = [row['question_id'], row['family_id'], row['editorial_status'] + ' / ' + row['editorial_priority'],
                  row['implementation_status'], target, row['legacy_legal_correctness']['status'], finding]
        lines.append('| ' + ' | '.join(cell(value) for value in fields) + ' |')
    lines += ['', '## 재현 입력', '', '| 파일 | SHA-256 |', '|---|---|']
    lines.extend(f'| {cell(path)} | `{sha}` |' for path, sha in ledger['input_hashes'].items())
    lines += ['', '`python scripts/build_representative_audit_ledger.py --check`는 현재 입력과 JSON·Markdown 산출물의 바이트 일치를 확인합니다.', '']
    return '\n'.join(lines).encode('utf-8')


def build():
    ledger = build_ledger()
    return {REPORTS / 'audit-ledger.json': encoded(ledger),
            REPORTS / 'audit-ledger.md': render_markdown(ledger)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Check generated JSON and Markdown without writing.')
    args = parser.parse_args()
    for path, payload in build().items():
        if args.check:
            require(path.exists() and path.read_bytes() == payload, 'Generated ledger drift: ' + relative(path))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_suffix(path.suffix + '.tmp')
            temporary.write_bytes(payload)
            temporary.replace(path)
        print(('Checked ' if args.check else 'Built ') + relative(path))


if __name__ == '__main__':
    main()
