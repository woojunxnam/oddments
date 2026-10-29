"""Refresh visible practice status from actual manifests; no legal audit claim."""
import argparse
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def output():
    selection=json.loads((ROOT/'practice_expansion/2026-10-28-representative/selection.json').read_text())
    metrics=json.loads((ROOT/'reports/representative-rewrite/pattern-metrics.json').read_text())
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
<h2>무엇을 확인했나요?</h2>
<p>문항별 작성자 검토,동일 팀 peer,자동검사,독립 canonical 감사를 구분합니다. 단위별 provenance가 다르며,최근 Unit3A/B는 작성자 대조입니다. 전체 문항·노트의 독립 전수감사,Board 승인 또는 합격 보장이 아닙니다. Canonical RELEASED 정책과 감사 기록은 그대로입니다.</p>
<p>노트33장/306절과 전체 ID의 인벤토리는 구축했지만 모든 atomic claim 검증이 끝난 것은 아닙니다. 현재는 인력비율·직접감독·전담교육의 작은 단위를 개정했고,1:6/4-intern 적용 관계 및CE 통지 경로 등의 미해결을 추적합니다.</p>
<h2>연습 모드와 기록</h2>
<p>문항 포함 범위와 문항 모음은 교집합으로 적용됩니다. 일반20·시간제120은 조건에 맞는 고유 family 수에 따라 짧아질 수 있습니다. 완전 랜덤10은 전체 {st['available_total']:,}개에서 복원추출하여 같은 ID/family 반복을 허용합니다. 보관·보류 문항의 검토 안내를 확인하세요. 기존 풀이·북마크·deep link·백업/가져오기는 보존합니다.</p>
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
