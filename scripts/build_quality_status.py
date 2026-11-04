"""Refresh visible practice status from actual manifests; no legal audit claim."""
import argparse
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def output():
    selection=json.loads((ROOT/'practice_expansion/2026-10-28-representative/selection.json').read_text())
    metrics=json.loads((ROOT/'reports/representative-rewrite/pattern-metrics.json').read_text())
    progress=json.loads((ROOT/'reports/full-corpus-review/progress.json').read_text())
    inventory=json.loads((ROOT/'reports/full-corpus-review/inventory-definitions.json').read_text())
    st=selection['stats']
    new=metrics['revised_unit']
    original=st['legacy_representatives_remaining']
    previous_default=st.get('previous_quality_default',st['previous_quality'])
    previous_held=st.get('previous_quality_safety_held',0)
    rewrite_default=st.get('rewrite_default',st['newly_authored_replacements'])
    rewrite_held=st.get('rewrite_safety_held',0)
    supplementary=progress.get('independent_legacy_supplementary_review',
        progress.get('independent_legacy_procedural_supplementary_review'))
    supplementary_notice=('' if supplementary is None else
        f"<p>절차적 미평가의 별도 보충 검토 {supplementary['supplementary_integrated_records']}개 중 "
        f"새 정답 평가 {supplementary['supplementary_new_key_assessed']}개를 고유 ID 기준으로 반영했습니다. "
        f"기존 primary 정답 평가 {supplementary['primary_key_assessed']}개와 중복 합산하지 않습니다. "
        "원래 NOT_ASSESSED·HOLD·현실성 FAIL과 부정 이력을 그대로 보존하며, 보충 KEEP도 원문 수정 없이 "
        "기존 보류를 해제하거나 기본 연습 복귀·canonical RELEASED 승인을 만들지 않습니다. 정답 평가 수는 법규 PASS 수가 아닙니다.</p>")
    pending=progress['independent_note_completeness_legal_review'].get('pending_census_reassessment_units',0)
    pending_notice=(f'<p>누락을 보완한 노트 {pending}절은 새 독립 검토 대기 상태로, 현재 처리·완전성 완료 수에서 제외합니다. 원래 누락 지적과 법규 보류 이력은 유지합니다.</p>' if pending else '')
    body=f'''<main><h1>문제은행 검토 범위와 현재 상태</h1>
<p>현재 연습판 설정: 기본 <strong>{st['recommended']:,}문항</strong> · 전체 보관 <strong>{st['available_total']:,}문항</strong>. 보관 수는 법규 검증 완료 수가 아닙니다.</p>
<table><thead><tr><th>원래 대표355개 처리</th><th>수</th></tr></thead><tbody>
<tr><td>새 ID 재작성</td><td>{st['newly_authored_replacements']}</td></tr>
<tr><td>기존 사례 통합</td><td>{st['replaced_by_existing_quality']}</td></tr>
<tr><td>보류</td><td>{st['held_from_default']}</td></tr>
<tr><td>개선 미반영</td><td>{original}</td></tr></tbody></table>
<p>기본 목록은 미반영 대표 {original}개 + 이전 MA-REV {previous_default}개 + 개정 MA-RW {rewrite_default}개입니다. MA-REV {st['previous_quality']}개 중 {previous_held}개와 MA-RW {st['newly_authored_replacements']}개 중 {rewrite_held}개는 원본355개 처리와 별도의 증거 기반 안전 보류입니다. 원본2,176개·MA-REV96개와 MA-RW의 모든 ID·원문·정답·학습 기록은 보관합니다. 신규 gap 사례 목표와 replacement를 중복 집계하지 않습니다.</p>
<h2>검토와 실제 개선</h2>
<table><thead><tr><th>서로 다른 집계</th><th>현재 범위</th><th>한계</th></tr></thead><tbody>
<tr><td>저자 개별 검토</td><td>{progress['question_ids_with_review_records']}/{progress['current_questions']} ({100*progress['question_ids_with_review_records']/progress['current_questions']:.2f}%)</td><td>조건부·오류·보류를 포함하며 독립 감사가 아님</td></tr>
<tr><td>독립 legacy 정답 평가</td><td>{progress['independent_legacy_legal_assessed']}/{progress['current_questions']} ({100*progress['independent_legacy_legal_assessed']/progress['current_questions']:.2f}%)</td><td>원문 읽음 {progress['independent_legacy_originals_read']}개, 정답 미평가 {progress['independent_legacy_keys_unassessed']}개. 모호·실패 판정을 포함하며 canonical RELEASED 승인이 아님</td></tr>
<tr><td>이번 작업의 실제 문항 재작성</td><td>0/{progress['current_questions']} (0%)</td><td>PR182 이후 원문·보기·정답 객체를 보존. 기존 MA-RW {st['newly_authored_replacements']}개는 이전 작성 실적</td></tr>
<tr><td>노트 저자 주장 열거</td><td>{progress['notes_units_with_author_atomic_claim_enumeration_records']}/306 ({100*progress['notes_units_with_author_atomic_claim_enumeration_records']/306:.2f}%)</td><td>저자 기록 존재 수이며 누락 없는 완전성을 뜻하지 않음</td></tr>
<tr><td>독립 노트 열거 완전성 확인</td><td>{progress['notes_units_with_complete_atomic_claim_census']}/306 ({100*progress['notes_units_with_complete_atomic_claim_census']/306:.2f}%)</td><td>독립 처리 {progress['independent_note_completeness_legal_review']['processed_units']}절 중 누락 지적 {progress['independent_note_completeness_legal_review']['omissions_found_units']}절은 보완 필요</td></tr>
<tr><td>배포 검증</td><td>이 집계에서 인증하지 않음</td><td>정확한 빌드의 CI와 공개 파일 대조 기록을 별도로 확인</td></tr>
</tbody></table>{supplementary_notice}{pending_notice}
<p>기본 연습에서 증거를 바탕으로 보류한 문항은 원래 대표 {st['held_from_default']}개와 MA-REV/MA-RW 별도 {previous_held+rewrite_held}개입니다. 보류는 실제 재작성 완료 수에 더하지 않습니다. 아카이브 {st['archive_ids_with_review_notice']}개에는 구체적인 검토 안내가 있습니다. 독립 현실성 PASS {progress['independent_legacy_realism_pass']}개도 법규·해설의 모든 문제를 해소했다는 뜻은 아닙니다. 정답이 맞아도 해설 오류·모호성·근거 미확인·정답 추측 단서가 있으면 안내를 확인하세요.</p>
<p>노트의 {progress.get('atomic_claims_enumerated',0)}개 저자 열거 명제 중 공식근거 대조 {progress.get('atomic_claims_source_checked',0)}개·SOURCE_BLOCKED {progress.get('atomic_claims_source_blocked',0)}개를 별도 기록했습니다. 독립 검토의 법규 상태는 KEEP {progress['independent_note_completeness_legal_review']['legal_keep_units']}절·HOLD {progress['independent_note_completeness_legal_review']['legal_hold_units']}절·SOURCE_BLOCKED {progress['independent_note_completeness_legal_review']['source_blocked_units']}절입니다. 열거의 완전성과 법규 확인을 구분합니다. 누락·보류 절과 연결 카드에는 실제 사유를 표시하고 자동 일일 복습에서 제외합니다.</p>
<p>노트의 versioned 본문 수정은 누적 {progress['notes_units_with_versioned_edits']}절이고, 현재 최종 본문의 별도 검토 기록은 {progress['notes_units_with_independent_final_content_review']}절입니다. 이를 전체306절의 독립 명제 감사 완료 수로 확대하지 않습니다. 기존 인력 비율·intern·reporting·CDTM의 OPEN {progress['open_claims']}건은 유지합니다. USP 접근 제한과 미확인 시행 관계도 임의로 확정하지 않습니다.</p>
<h2>학습 범위와 문항 수는 어떻게 다른가요?</h2>
<table><thead><tr><th>집계 대상</th><th>현재 수</th><th>의미</th></tr></thead><tbody>
<tr><td>통합노트 목차</td><td>{inventory['notes_topics']}주제 · {inventory['notes_sections']}절</td><td>교재의 주제와 상세 절</td></tr>
<tr><td>고유 question family ID</td><td>{inventory['unique_family_ids']}</td><td>같은 판단 구조·판본을 묶은 데이터 단위; 독립 법규 수가 아님</td></tr>
<tr><td>추가 사례형 판단 모델</td><td>{inventory['additional_conditional_models']}</td><td>1,152문항을 만드는 조건별 모델</td></tr>
<tr><td>공개 연습판</td><td>{inventory['public_practice_questions']:,}</td><td>원본·변형·개정판을 모두 포함한 ID 수</td></tr>
<tr><td>Canonical</td><td>{inventory['canonical_questions']} / RELEASED {inventory['canonical_statuses']['RELEASED']}</td><td>별도의 감사·배포 체계; 위 연습판 수와 합산하지 않음</td></tr>
</tbody></table>
<p>과거 2,176은 원본1,024+추가1,152, 2,328은 여기에 MA-REV96+당시 MA-RW56을 더한 수입니다. 226은 과거 canonical 집계입니다. 전체 독립 사례 또는 독립 법규 판단 수의 전수 판정은 아직 수행하지 않았습니다.</p>
<h2>원문과 학습 기록</h2>
<p>공개 연습판의 문항 ID·원래 정답·풀이·북마크는 보존합니다. 기존 내용과 다른 실제 사례는 별도 판본으로 작성하고 최종 내용의 독립 법규·현실성 검토를 받아야 합니다. 저자 점검·자동 검사·배포 성공을 이 독립 검토 대신 사용하지 않습니다.</p>
<p>MA-EXP-0351·0367·0383의 모든 보기가 정답인 SATA도 편집 보류 상태로 기본 연습에서 제외했습니다. 전부 정답이라는 형식 자체를 법적 오답으로 판정하지 않습니다. <a href="../notes/cdtm13-16-vax01-04.html">CDTM·예방접종 집중 복습</a>과 노트의 관련 문항 연결은 복습 경로이며 별도 감사 통과 표시는 아닙니다.</p>
<h2>연습 모드와 기록</h2>
<p>문항 포함 범위와 문항 모음은 교집합으로 적용됩니다. 일반20·시간제120은 조건에 맞는 고유 family 수에 따라 짧아질 수 있습니다. 완전 랜덤10은 전체 {st['available_total']:,}개에서 복원추출하여 같은 ID/family 반복을 허용합니다. 보관·보류 문항의 검토 안내를 확인하세요. 기존 풀이·북마크·deep link·백업/가져오기는 보존합니다.</p>
<p>상세 통합노트의 관련 문제 풀기·이 절의 오답 복습은 실제 근거 절 ID로 연결합니다. 대표·개정 문항 수와 전체 변형 수를 구분하며, 연습 화면에서 같은 절로 돌아갈 수 있습니다. 연결 수·읽음·정답률은 법규 검증 또는 합격 예측이 아닙니다.</p>
<h2>현재 개정판 구조 통계</h2>
<p>MA-RW {new['questions']}개: SBA {new['types'].get('SBA',0)} · SATA {new['types'].get('SATA',0)}. 정답분포·길이·유사도는 편집 신호이며 법규 유효성 또는 실제 MPJE 난도 점수가 아닙니다. archive의 반복은 남아 있습니다.</p>
<h2>실행 근거와 다음 작업</h2>
<p><a href="https://github.com/woojunxnam/oddments/actions/workflows/representative-quality-qa.yml">문항·기록 회귀 CI</a> · <a href="https://github.com/woojunxnam/oddments/blob/main/docs/MPJE_QUALITY_CHECKPOINT.md">checkpoint</a> · <a href="https://github.com/woojunxnam/oddments/blob/main/reports/full-corpus-review/progress.json">전체 추적표</a></p>
<p>빌드 설정과 실제 배포를 구별하고,정확한 head의 CI 및 공개 origin 검증 기록을 확인합니다. 아직 수행하지 않은 검사나 독립 감사를 PASS로 바꾸지 않습니다. 비공개 기출·Pre-MPJE·유료 원문은 사용하지 않습니다.</p>
<p><a href="./">연습으로</a> · <a href="../notes/">통합노트</a></p></main>'''
    path=ROOT/'site/practice-expansion/quality-review.html'
    original_html=path.read_text()
    updated,n=re.subn(r'<main>.*?</main>',lambda _:body,original_html,flags=re.S)
    if n!=1:raise ValueError('Unexpected quality report template')
    return path,updated


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    path,text=output()
    if a.check:
        if path.read_text()!=text:raise SystemExit('Stale visible quality status')
    else:path.write_text(text)
    print('Practice status matches manifest; no audit certification added.')
