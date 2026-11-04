"""Package this session's authored findings; never derive legal verdicts from hidden fields."""
import hashlib
import json
import re
import runpy
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVD = Path('reports/full-corpus-review/phase9-a-evidence')
OUT = Path('reports/full-corpus-review/independent-phase9-a-review.json')
NOW = datetime.now(timezone.utc).isoformat()
DAY = NOW[:10]
ACTOR = '/root/independent_wave9_a'
INSTANCE = 'GPT:/root/independent_wave9_a:20261104'

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()

def binding(path):
    return {'path': str(path), 'sha256': sha(path)}

def write(path, obj):
    (ROOT / path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

packet = json.loads((ROOT / EVD / 'assigned-visible-input.json').read_text())
assignment = json.loads(Path('/tmp/independent-phase9-a-assignment.json').read_text())
assessments = runpy.run_path(str(ROOT / EVD / 'reviewer-assessments.py'))['ASSESSMENTS']
register = json.loads((ROOT / EVD / 'source-register.json').read_text())
source_by_id = {s['source_id']: dict(s) for s in register}
duplicates = json.loads((ROOT / EVD / 'duplicate-visible-comparison.json').read_text())
dup_by_id = {r['question_id']: r for r in duplicates['records']}
assert set(assessments) == set(assignment['question_hashes'])
assert len(packet['records']) == len(assessments) == 40

# Whole objects are used only to calculate assignment hashes and select a strict
# context whitelist. No hidden truth, author review or prior audit is exported.
context = {}
family_checks = []
for collection in sorted({r['collection'] for r in packet['records']}):
    container = json.loads((ROOT / collection).read_text())
    qs = container['questions']
    byid = {q['question_id']: q for q in qs}
    for row in packet['records']:
        if row['collection'] != collection:
            continue
        qid = row['visible']['question_id']
        q = byid[qid]
        assert digest(q) == assignment['question_hashes'][qid] == row['record_sha256']
        context[qid] = {k: q.get(k) for k in ('family_id', 'source_ids')}
        context[qid]['note_evidence'] = [
            {k: n.get(k) for k in ('unit_id', 'title', 'body_sha256', 'url')}
            for n in q.get('note_evidence', [])]
        siblings = [x for x in qs if x.get('family_id') == q.get('family_id')]
        prefixes = [x['stem'].split('\n\nWhich')[0] for x in siblings]
        family_checks.append({'question_id': qid, 'family_id': q.get('family_id'),
            'member_ids': [x['question_id'] for x in siblings],
            'member_count': len(siblings),
            'same_case_prefix_before_which': len(set(prefixes)) == 1,
            'method': 'Code-only visible stem prefix equality and family inventory; not an assertion of manual full reading of all four archived variants.',
            'manual_nearest_variant_read': dup_by_id[qid]['archive']['question_id']})
write(EVD / 'source-context-whitelist.json', {
    'purpose': 'Source discovery and family context only; inherited review/flags/truth omitted.',
    'records': [{'question_id': k, **v} for k, v in context.items()]})
write(EVD / 'family-boundary-check.json', {'checked_at': NOW, 'records': family_checks})

nabp = json.loads((ROOT / EVD / 'nabp-retrieval-metadata.json').read_text())
nabp_memo = [
    '작성자: ' + ACTOR,
    '최종 공개 형식 원문 재독 시각(UTC): ' + NOW,
    '이 문서는 직접 작성한 형식 검토 메모이며 원 sample 질문·정답·보호된 exam/recalled/Pre-MPJE/commercial 항목을 재배포하지 않는다.',
    '공식 공개 sample PDF에서 multiple-choice, multiple-response, ordered-response 형식만 확인했다. 실제 문항 내용이나 문구를 후보 설계의 재료로 복제하지 않았다.',
    '공식 take-the-MPJE 페이지는 2.5시간, 120문항, adaptive selected-response 형식을 안내한다. 공개 형식의 존재가 본 batch의 distractor 품질이나 실전성을 자동 보증하지 않는다.',
    '공식 competency 페이지는 2027-03-01부터 새 outline이 적용됨을 명시한다. 이 batch는 그 전 시험 범위이며 영역 비중 22/33/24/21을 확인했다.',
    '공개 표본의 형식 확인은 법률 권위 또는 실제 시험 문항 난이도의 검증이 아니다. 내부 style profile의 10개 기준을 각 원문에 따로 적용했다.',
    'MA-EXP-0615 보기 B의 criteria described in the notes는 공개 MPJE 상황문항 안에서 자족적으로 평가할 수 없는 노트 의존 문구다.',
]
for item in nabp:
    assert hashlib.sha256(Path(item['private_temp_raw_path']).read_bytes()).hexdigest() == item['raw_sha256']
    nabp_memo.extend(['', item['source_id'] + ': ' + item['official_url'],
        'HTTP ' + str(item['http_status']) + '; retrieval ' + item['retrieved_at'],
        'Raw SHA256 ' + item['raw_sha256'],
        'Private temporary original retained outside repository; public evidence is this own memo only.'])
(ROOT / EVD / 'nabp-public-format-review-memo.txt').write_text('\n'.join(nabp_memo) + '\n')

version = {
 'cmr247_9': ('Current official posted 247 CMR 9; Mass. Register #1536, 2024-12-06', '별도 전 조항 commencement 날짜를 추정하지 않았다. 현재 게시 원문과 해당 조항을 확인했다.'),
 'cmr247_15': ('Current official posted 247 CMR 15; Mass. Register #1536, 2024-12-06', '15.02–15.04의 현 게시 문구를 확인했다. 별도 시행일을 만들어내지 않았다.'),
 'cmr105_721': ('Current official posted 105 CMR 721; Mass. Register #1531, 2024-09-27', '721.070(A)(11)의 2025-01-01 또는 Department later date 문구를 읽었다. 현재 LTCF 연장 종료일 자체는 이 review에서 확정하지 않으며 0583 A의 모든 형태 자동 연장 주장을 부정하는 데만 사용한다.'),
 'cmr105_700': ('Current official posted 105 CMR 700; Mass. Register #1514, 2024-02-02', '700.012 PMP 보고 범위와 현재 DPH 직접 보고 안내를 교차 확인했다.'),
 'policy2018_01': ('Board policy 2018-01, revised 2024-01-11', '공식 정책의 처방 변경 금지/허용 및 IV 기록 요건을 확인했다. 약사 치료 변경의 일반 권한으로 확대하지 않았다.'),
 'policy2023_01': ('Board policy 2023-01, revised 2025-01-09', 'Compliance packaging과 reusable dose planners, return/repackaging 구획을 구분했다.'),
 'policy2024_05': ('Board policy 2024-05, adopted 2024-09-05', '현 법률 94C§23(d)와 교차 확인. ADD/ADHD/narcolepsy 진단 확인은 더 이상 요구하지 않는다고 명시한다.'),
 'delivery': ('Board Medication Delivery and Shipping advisory, revised 2025-01-09', '문서가 best-practice recommendations임을 구분했다. 법적 근거는 247 CMR 9.02 등이며 advisory를 새 blanket reporting deadline/mandate로 바꾸지 않았다.'),
 'hhs_security': ('HHS current Security Rule summary fetched on review date; NPRM distinguished from operative rule', '게시 요약과 현행 45 CFR164.306–316을 구분하여 읽었다. 제안 규칙을 시행 규칙으로 사용하지 않았다.'),
 'hhs_part2': ('HHS Part 2 fact sheet updated 2026-01-30; compliance required 2026-02-16', '현재 42 CFR Part2 조항과 함께 확인. 2026-11-04 review는 해당 compliance date 이후다.'),
 'fda_rems': ('FDA REMS FAQ, content current as of 2018-01-26', 'REMS와 Medication Guide의 일반 법적 구조만 확인했다. 특정 제품의 2026년 active REMS/등록 상태는 주장하지 않는다.'),
 'cdc_vis': ('CDC official Facts About VIS page retrieved on review date', '법률상 지정 vaccine별 VIS 제공 의무를 확인. 모든 백신에 똑같은 VIS 의무가 있다고 확대하지 않았다.'),
 'pmp_reporting': ('Current Massachusetts DPH Pharmacy reporting and data submission webpage', 'II–V와 gabapentin VI 보고 범위를 직접 확인. 별도 공식-hosted vendor guide는 저작권 raw 비공개 context일 뿐이다.'),
}
coverage = {}
for value in assessments.values():
    for refs in value['refs']:
        for segment in refs.split('; '):
            if '@' in segment:
                sid, section = segment.split('@', 1)
                coverage.setdefault(sid, set()).add(section)
coverage['hhs_part2'] = {'2024 Final Rule fact sheet; required compliance by 2026-02-16'}

sources = []
for sid in sorted(coverage):
    item = source_by_id[sid]
    assert item['http_status'] == 200 and item['error'] is None
    if sid.startswith('cfr'):
        text = (ROOT / item['evidence_path']).read_text()
        m = re.search(r'Displaying title\s+(\d+),\s+up to date\s+as of\s+([\d/]+)\.\s+Title\s+\d+\s+was last amended\s+([\d/]+)', text, re.I)
        assert m, sid
        ver = f'eCFR current display title {m.group(1)}, up to date as of {m.group(2)}; title last amended {m.group(3)}'
        limit = 'eCFR는 공식 정부의 continuously updated compilation이며 legal edition이라는 주장은 하지 않는다. Title 전체 last-amended 날짜를 개별 조항 시행일로 오인하지 않았다. 해당 현행 조항 문구를 대조했고 임의 시행일을 붙이지 않았다.'
    elif sid.startswith('mgl'):
        ver, limit = 'Massachusetts Legislature current General Laws online section retrieved on review date', '현재 공식 게시 section을 읽었다. 개별 개정 시행일이 원문에 없으면 별도 날짜를 추정하지 않았다.'
    else:
        ver, limit = version[sid]
    sources.append({**item, 'law_checked_date': DAY, 'version': ver,
        'effective_date': None, 'effective_date_or_version_limitation_ko': limit,
        'coverage': sorted(coverage[sid]), 'exact_section': '; '.join(sorted(coverage[sid])),
        'source_identity_verified': True, 'legal_credit': sid != 'hhs_part2',
        'source_read_mode': 'ACTUAL_SAME_DAY_OFFICIAL_RETAINED_BYTES_READ; original retrieval times preserved',
        'read_completion_attested_at': NOW,
        'read_timestamp_note_ko': '이 시각은 본 세션에서 실제 수행한 해당 조항 읽기와 최종 evidence binding 확인의 완료를 기록한 시각이다. 이전 최초 읽기 시각이나 새 live retrieval 시각을 소급 생성하지 않았다.'})
for item in nabp:
    sources.append({**{k: v for k, v in item.items() if k != 'private_temp_raw_path'},
        'raw_path': item['private_temp_raw_path'],
        'evidence_path': str(EVD / 'nabp-public-format-review-memo.txt'),
        'evidence_sha256': sha(EVD / 'nabp-public-format-review-memo.txt'),
        'law_checked_date': DAY, 'legal_credit': False,
        'exact_section': 'Public item format/2026 competency outline only; no exam content copied',
        'version': 'Official public page/PDF retrieved on review date; outline changes 2027-03-01',
        'read_completion_attested_at': NOW,
        'tls_verification': 'DEFAULT_VERIFIED_HTTPS',
        'source_identity_verified': True})
source_bound = {s['source_id']: s for s in sources}

def authorities(refs):
    answer = []
    for segment in refs.split('; '):
        if '@' not in segment:
            if answer:
                answer[-1]['exact_section'] += '; ' + segment
            continue
        sid, section = segment.split('@', 1)
        s = source_bound[sid]
        answer.append({k: s[k] for k in ['source_id', 'official_url', 'resolved_url',
            'http_status', 'retrieved_at', 'raw_sha256', 'evidence_path',
            'evidence_sha256', 'law_checked_date', 'version', 'read_completion_attested_at']})
        answer[-1]['exact_section'] = section
        answer[-1]['source_support_status'] = 'OFFICIAL_PRIMARY_TEXT_VERIFIED'
    assert answer
    return answer

criteria_names = ['jurisprudence_reasoning', 'practice_plausibility', 'authentic_distractors',
    'wording_not_guessable', 'reasoning_not_trivia', 'natural_rule_combination',
    'appropriate_drug_context', 'distinct_from_bank', 'not_schedule_flashcard',
    'public_style_without_copying']
records = []
for row in packet['records']:
    v = row['visible']; qid = v['question_id']; a = assessments[qid]
    assert v['correct_choice_ids'] == a['expected_key'], qid
    assert [c['id'] for c in v['choices']] == list('ABCD')
    criteria = {name: name not in a['failed'] for name in criteria_names}
    criterion_findings = dict(zip(criteria_names, [a['juris'], a['practice'], a['distractors'],
        a['cue'], a['depth'], a['combination'], a['drug'], a['dup'],
        '네 보기 모두 schedule 이름만 맞추는 flashcard가 아니다. ' + a['juris'],
        ('보기 B의 criteria described in the notes는 문항 자체에서 제공되지 않은 노트를 전제하므로 실제 공개 MPJE 상황문항의 자족적인 판단 형식에 어긋난다.' if qid == 'MA-EXP-0615' else
         '공식 공개 sample의 multiple-response 형식과 양립하는 영문 SATA다. 사례/보기의 구체적인 품질은 다른 기준에서 따로 판정했다. 공개 형식만 참고했고 보호된 항목이나 sample 문구를 복제하지 않았다.')]))
    choice_findings = {}
    for i, c in enumerate(v['choices']):
        choice_findings[c['id']] = {
            'original_text': c['text'], 'original_text_sha256': hashlib.sha256(c['text'].encode()).hexdigest(),
            'independently_assessed_truth': c['id'] in a['expected_key'],
            'should_be_selected': c['id'] in a['expected_key'],
            'support': 'SUPPORTED' if c['id'] in a['expected_key'] else 'REFUTED_AS_WRITTEN',
            'finding_ko': a['findings'][i], 'authorities': authorities(a['refs'][i]),
            'original_rationale_sha256': digest(v['explanation']['choice_analysis'][c['id']]),
            'original_rationale_fully_read': True,
            'original_rationale_assessment_ko': '원래 보기 해설 전체를 읽었으며 이 보기의 위 독립 법규 판단과 일치한다. 잘못된 보기의 교정문을 현재 보기의 일부로 오인하지 않았다.'}
    expected = a['expected_key']
    explanation = v['explanation']
    fail = bool(a['failed'])
    dup = dup_by_id[qid]
    records.append({'question_id': qid, 'record_sha256': row['record_sha256'],
        'collection': row['collection'], 'family_id': context[qid]['family_id'],
        'visible_content_sha256': digest(v),
        'input_binding': {**binding(EVD / 'assigned-visible-input.json'), 'selector': 'records[].visible.question_id=' + qid},
        'read_scope': {'stem': True, 'all_choices': list('ABCD'), 'stored_key': True,
            'core_reasoning': True, 'all_choice_analysis': list('ABCD'), 'learning_boundary': True,
            'actual_session_completed_read_at': NOW,
            'note_ko': '보고서 작성 전에 원 stem·4보기·저장 key·한국어 core·4보기 해설·learning boundary 전체를 직접 읽었다. 시각은 전체 review 완료 확인 시각이며 최초 읽기 시각을 추정한 것이 아니다.'},
        'legal_review': {'existing_answer_correct': 'YES', 'verdict': 'KEEP',
            'stored_key': v['correct_choice_ids'], 'independently_expected_key': expected,
            'polarity': 'CORRECT_SELECT_ALL_TRUE_STATEMENTS', 'question_type': v['question_type'],
            'sata_exact_combination_recomputed': True, 'ambiguity_assessment': 'NO_MATERIAL_KEY_AMBIGUITY_FOUND',
            'choice_by_choice_findings': choice_findings,
            'authorities': [x for c in choice_findings.values() for x in c['authorities']],
            'finding_ko': a['legal'], 'blocker': None,
            'original_explanation_review': {'core_fully_read': True,
                'core_sha256': digest(explanation['core_reasoning']),
                'all_choice_rationales_fully_read': list('ABCD'),
                'learning_boundary_fully_read': True,
                'learning_boundary_sha256': digest(explanation['learning_boundary']),
                'core_assessment_ko': a['legal'],
                'per_choice_rationale_findings_ko': {c: choice_findings[c]['finding_ko'] for c in 'ABCD'},
                'learning_boundary_assessment_ko': '같은 family 4문항을 독립적인 네 임상 사례로 세지 않는 원문의 경계가 타당하다. family inventory/visible prefix는 별도 코드 확인이며 가장 가까운 archive 원 stem·모든 보기만 수동 비교했다. 나머지 세 변형의 모든 해설을 새로 읽었다고 주장하지 않는다.',
                'error_found': False, 'scope_overreach_found': False,
                'limitation_ko': '현재 보이는 원 해설의 법적 핵심을 평가했다. 원 저자 hidden truth/기존 auditor verdict를 독립 근거로 사용하지 않았다.'}},
        'realism_review': {'verdict': 'FAIL' if fail else 'PASS',
            'decision': ('MINOR_EDIT' if qid == 'MA-EXP-0615' else 'MAJOR_REWRITE') if fail else 'KEEP',
            'criteria': criteria, 'criterion_findings_ko': criterion_findings,
            'failed_criteria': a['failed'],
            'duplicate_evidence': {**binding(EVD / 'duplicate-visible-comparison.json'),
                'method': duplicates['method'],
                'manual_read_scope': 'nearest archive, current-default and canonical candidate: original stem and every choice; 120 candidate comparisons across 40 records',
                'archive_candidate': dup['archive']['question_id'],
                'current_default_candidate': dup['current_default']['question_id'],
                'canonical_candidate': dup['canonical']['question_id'],
                'finding_ko': a['dup'],
                'pool_limitation_ko': '2349 public visible items와 439 canonical visible items에서 후보를 찾았다. 439개가 현재 모두 RELEASED라는 뜻이 아니다. current default는 배정시 publication/selection에 따른 298개 pool이다. Q0012 active/released 상태를 가정하지 않았다.'},
            'finding_ko': a['action'] if fail else a['practice'] + ' ' + a['juris'] + ' ' + a['dup']},
        'safe_hold_recommended': fail, 'release_eligible': False,
        'native_disposition': 'NEEDS_REMEDIATION' if fail else 'INDEPENDENT_ASSESSED',
        'required_next_action_ko': a['action'], 'canonical_audit': False,
        'canonical_release_credit': 0, 'author_review_credit': 0})

policies = ['docs/INDEPENDENT_DEFAULT_WAVE9_RUNBOOK.md', 'docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md',
    'docs/RELEASE_POLICY.md', 'docs/AUDIT_WORKFLOW.md', 'docs/SOURCE_USE_POLICY.md',
    'docs/QUESTION_AUTHORING_STANDARD.md', 'reports/full-corpus-review/progress.json']
report = {'report_id': 'independent-phase9-a-current-default-review', 'stage': 'independent-legacy',
    'job_id': assignment['job_id'], 'job_sequence': assignment['sequence'],
    'reviewed_at': DAY, 'review_completed_at': NOW,
    'auditor': 'GPT', 'auditor_instance': INSTANCE,
    'actor_provenance': {'actor_id': ACTOR, 'session_id': ACTOR},
    'independent_of_authors': True, 'canonical_audit': False,
    'canonical_release_credit': 0, 'author_review_credit': 0,
    'independence_statement_ko': '실제 새 세션 /root/independent_wave9_a가 배정 원문을 처음 독립 검토했다. 해당 원문의 author/editor가 아니며 이전 whole-key 판정 이력이 없다. 이전 author/auditor verdict와 숨은 truth 배열은 읽거나 답의 근거로 사용하지 않았다. 고정 auditor_instance를 여러 identity로 바꾸지 않았다.',
    'input_binding': binding(EVD / 'assigned-visible-input.json'),
    'question_hashes': assignment['question_hashes'],
    'policy_bindings': [binding(p) for p in policies],
    'schema_binding': {**binding('schemas/question.schema.json'), 'schema_id': json.loads((ROOT/'schemas/question.schema.json').read_text()).get('$id')},
    'style_profile_binding': {**binding('data/exam_style/mpje_style_profile.json'),
        **{k:v for k,v in json.loads((ROOT/'data/exam_style/mpje_style_profile.json').read_text()).items()
           if k in ('profile_id','content_version','content_hash','valid_for_exams_before')}},
    'blueprint_binding': {**binding('data/blueprint.json'),
        **{k:v for k,v in json.loads((ROOT/'data/blueprint.json').read_text()).items()
           if k in ('blueprint_id','content_version','content_hash')}},
    'source_register_binding': binding(EVD/'source-register.json'),
    'source_context_binding': binding(EVD/'source-context-whitelist.json'),
    'reviewer_authored_findings_binding': binding(EVD/'reviewer-assessments.py'),
    'family_boundary_binding': binding(EVD/'family-boundary-check.json'),
    'retrieval_limitations_ko': '공식 정부 원문은 verified HTTPS로 실제 조회했다. source-register의 gabapentin 경로 HTTP404는 실패 기록이며 법률 credit이 없다. 별도의 성공한 DPH pharmacy-reporting 원문으로 gabapentin을 확인했다. 정부 호스팅 vendor guide와 NABP 원문은 저작권 raw를 repo에 공개하지 않고 SHA·조회정보·자체 memo만 보존했다. 현재 source credit은 per-option verified primary text에서만 부여하며 문서 수를 문항 감사 수로 계산하지 않는다.',
    'publication_context_ko': '배정 이후 root가 canonical Q0012를 HOLD하고 연결 guide를 철회했음을 전달받았다. 본 배정 40개의 whole-record hash는 바뀌지 않았다. 기존 canonical 원문의 비교는 현재 release status를 보증하지 않는다.',
    'sources': sources, 'records': records,
    'summary': {'assigned':40, 'fully_assessed':40, 'legal_existing_answer_correct_yes':40,
        'legal_verdict_counts': dict(Counter(r['legal_review']['verdict'] for r in records)),
        'realism_verdict_counts': dict(Counter(r['realism_review']['verdict'] for r in records)),
        'source_blocked':0, 'hold':0,
        'needs_remediation_ids':[r['question_id'] for r in records if r['safe_hold_recommended']],
        'canonical_release_credit':0, 'author_review_credit':0,
        'scope_ko':'현재 원문 독립 assessment만 완료했다. 원 문항·key·해설·source·queue·ledger·generated는 변경하지 않았으며 canonical RELEASED나 publication 승격을 인증하지 않는다.'}}
write(OUT, report)
print(json.dumps({'report':str(OUT), 'sha256':sha(OUT), 'sources':len(sources),
    'summary': report['summary']},ensure_ascii=False,indent=2))
