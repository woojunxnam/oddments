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
    body=f'''<main><h1>문제은행 검토 범위와 현재 상태</h1>
<p>현재 연습판 설정: 기본 <strong>{st['recommended']:,}문항</strong> · 전체 보관 <strong>{st['available_total']:,}문항</strong>. 보관 수는 법규 검증 완료 수가 아닙니다.</p>
<table><thead><tr><th>원래 대표355개 처리</th><th>수</th></tr></thead><tbody>
<tr><td>새 ID 재작성</td><td>{st['newly_authored_replacements']}</td></tr>
<tr><td>기존 사례 통합</td><td>{st['replaced_by_existing_quality']}</td></tr>
<tr><td>보류</td><td>{st['held_from_default']}</td></tr>
<tr><td>개선 미반영</td><td>{original}</td></tr></tbody></table>
<p>기본 목록은 미반영 대표 {original}개 + 이전 MA-REV 96개 + 개정 MA-RW {st['newly_authored_replacements']}개입니다. 원본2,176개·MA-REV96개와 이전 판본은 삭제하지 않습니다. 신규 gap 사례 목표와 replacement를 중복 집계하지 않습니다.</p>
<h2>학습 범위와 문항 수는 어떻게 다른가요?</h2>
<table><thead><tr><th>집계 대상</th><th>현재 수</th><th>의미</th></tr></thead><tbody>
<tr><td>통합노트 목차</td><td>{inventory['notes_topics']}주제 · {inventory['notes_sections']}절</td><td>교재의 주제와 상세 절</td></tr>
<tr><td>고유 question family ID</td><td>{inventory['unique_family_ids']}</td><td>같은 판단 구조·판본을 묶은 데이터 단위; 독립 법규 수가 아님</td></tr>
<tr><td>추가 사례형 판단 모델</td><td>{inventory['additional_conditional_models']}</td><td>1,152문항을 만드는 조건별 모델</td></tr>
<tr><td>공개 연습판</td><td>{inventory['public_practice_questions']:,}</td><td>원본·변형·개정판을 모두 포함한 ID 수</td></tr>
<tr><td>Canonical</td><td>{inventory['canonical_questions']} / RELEASED {inventory['canonical_statuses']['RELEASED']}</td><td>별도의 감사·배포 체계; 위 연습판 수와 합산하지 않음</td></tr>
</tbody></table>
<p>과거 2,176은 원본1,024+추가1,152, 2,328은 여기에 MA-REV96+당시 MA-RW56을 더한 수입니다. 226은 과거 canonical 집계입니다. 전체 독립 사례 또는 독립 법규 판단 수의 전수 판정은 아직 수행하지 않았습니다.</p>
<h2>무엇을 확인했나요?</h2>
<p>이 전체검토 추적표에 ID별 공식 근거 대조 기록이 있는 문항은 누적 <strong>{progress['question_ids_with_review_records']:,}개</strong>이며 조건부·오류·보류 기록도 포함합니다. 아직 개별 재검증 기록이 없는 문항은 <strong>{progress['legal_review_counts']['NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW']:,}개</strong>입니다. 원본 1,024개 구조 검사는 별도 실적이며 법규 검토 수에 더하지 않습니다.</p>
<p>최근 CDTM05–12 배치에서는 원본 MA-EXP-0241–0272의 32개·128개 선택지, 이미 존재하는 개정판 MA-RW-0029–0036의 8개·32개 선택지를 개별 작성자 근거 검토 기록에 추가했습니다. 총 40개 ID·160개 선택지이며 독립 법규 감사가 아닙니다. 8개 family가 반복 판단을 공유하고 0255·0271은 SATA 전부 정답입니다. 보관 문항의 원본·정답·풀이 이력을 보존하고 기존 개정판을 중복 생성하지 않았습니다. 이전 Discipline/CDTM 배치의 MA-EXP-0223 오류·0224 모호성 안내도 유지합니다. <a href="../notes/cdtm05-12.html">CDTM05–12 집중 복습</a>으로 이동할 수 있습니다.</p>
<p>10개 기준의0–5점 편집 평가는 {progress['editorial_rubric_assessed_ids']}개 ID에만 기록했습니다. 미평가 항목은0점으로 처리하지 않습니다. 작성자 평가·같은 팀 교차 검토·자동검사·독립 canonical 감사를 구분하며, 점수나 합계로 법규 정확성 또는 RELEASED를 인증하지 않습니다.</p>
<p>이번에 통합노트 CDTM05–12 관련 w3-d-4–w3-d-8의 5개 절을 별도 versioned overlay로 개정했습니다. 이전 15개 개정 절과 원본은 보존합니다. 누적 {progress['notes_units_with_partial_claim_review']}절에 제한된 주장 대조 기록이 있고 versioned edit는 {progress['notes_units_with_versioned_edits']}절입니다. Claim/cluster {progress['reviewed_claims']}개 중 근거 대조 {progress['source_checked_claims']}개·OPEN {progress['open_claims']}개입니다. 모두 작성자 검토 범위이며 306절의 atomic claim 전수검증이나 독립 감사가 아닙니다. PharmD 자격 statute/regulation 관계와 reporting 및 CE 방식, 인력 관련 OPEN은 유지합니다.</p>
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
