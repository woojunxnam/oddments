"""Pin the author-reviewed CDTM13/VAX04 note claims without inventing audit approval."""
import argparse,hashlib,json
from pathlib import Path
from notes_revision import ROOT,load_notes
EVIDENCE='reports/full-corpus-review/evidence/cdtm-vax-official-crosscheck.json'
OUT=ROOT/'reports/full-corpus-review/cdtm-vax-note-claims.json'
RECORDS=[["CDTM1316-CPA-01","w3-d-9","CPA에는 서명뿐 아니라 주질환·동반질환, 처방권한, protocol, 위험관리, 정보·긴급연락, 양측 자격 진술이 필요하다.","247 CMR 16.04(1)–(2)"],["CDTM1316-DELEG-01","w3-d-9","CPA는 위임 가능·불가능 업무와 시기·방법·기간·범위를 규정하고 intern·technician의 247 CMR 8 scope를 넘길 수 없다.","247 CMR 16.04(3)"],["CDTM1316-TERM-01","w3-d-10","CPA 종료 전 약물치료의 연속성을 확보하고 종료/미갱신 시 환자에게 서면으로 종료·후속치료 절차를 알려야 한다.","247 CMR 16.04(5)"],["CDTM1316-REC-01","w3-d-10","Pharmacist는 현재 CPA·referral·consent 사본을 primary setting에 즉시 조회 가능하게 보관하고 physician은 원본을 보관한다.","247 CMR 16.04(6)"],["CDTM1316-EMP-01","w3-d-10","Community pharmacy의 physician QA review 고용은 가능하지만 CPA 설립·유지 목적의 physician 고용은 금지된다.","247 CMR 16.04(7)(a)–(c)"],["VAX0104-PER-01","w3-c-1","주 예방접종 policy에서 PTT는 제외되며 pharmacist, intern, 적격 licensed technician만 포함된다.","DPH Policy2023-02 Introduction"],["VAX0104-SUP-01","w3-c-1","Intern·technician에게는 on-duty pharmacist 승인과 적격 immunizer의 직접 감독이 요구되며 전화 승인만으로 대체할 수 없다.","DPH Policy2023-02 Introduction, III"],["VAX0104-AGE-01","w3-c-2","주 policy의 5세 기준은 모든 vaccine의 제품별 연령·standing order 범위를 충족한다는 의미가 아니다.","DPH Policy2023-02 I–II, IV"],["VAX0104-FLU-01","w3-c-2","2026–27 influenza standing order는 면역억제제를 복용 중인 18–64세 고형장기 이식 수혜자의 high-dose/보강 백신 경로를 명시한다.","DPH Standing Order2026-06, Procedure 1(b), 5"],["VAX0104-TRAIN-01","w3-c-3","Pharmacist·intern 초기 vaccine 교육은 12시간 self-study, 8시간 live, 연령에 맞는 IM/SC 실기평가가 필요하다.","DPH Policy2023-02 III.C.1"],["VAX0104-CPR-01","w3-c-3","현재 CPR과 교육증빙의 약국 보관은 별도 의무이고 pharmacist의 예방접종 관련 CE 1시간은 매년 필요하다.","DPH Policy2023-02 III.A–C"],["VAX0104-TECH-01","w3-c-4","Licensed technician은 national certification 또는 면허 이후 500시간 경력, 6시간 과정과 추가 2시간 OJT 및 적격 감독·현재 CPR이 필요하다.","DPH Policy2023-02 III.A–D"],["VAX0104-TECH-02","w3-c-4","Technician은 약사의 vaccine selection·counseling 후 물리적 준비·투여를 수행하며 2년마다 관련 2시간 유지교육을 이수한다.","DPH Policy2023-02 III.D.4–5"]]
def make():
    raw=(ROOT/EVIDENCE).read_bytes()
    e=json.loads(raw)
    assert e['schema_version']=='cdtm-vax-official-crosscheck/1'
    units={u['id']:u for c in load_notes(ROOT)['chapters'] for u in c['units']}
    assert load_notes(ROOT)['edition']=='2026-10-30.cdtm13-vax04.1'
    result=[]
    for id,uid,english,clause in RECORDS:
        unit=units[uid]
        assert unit['content_version']=='2026-10-30.cdtm13-vax04.1'
        result.append(dict(claim_id=id,unit_id=uid,statement_ko=english,
            authority_clauses=[clause],review_status='AUTHOR_SOURCE_CHECKED',
            checked_at='2026-10-30',reviewer_provenance='AUTHOR_NOT_INDEPENDENT_20261030_CDTM_VAX',
            source_evidence=EVIDENCE,source_evidence_sha256=hashlib.sha256(raw).hexdigest(),
            unit_content_sha256=unit['body_sha256'],
            scope='Explicit selected claim only; no full unit atomic census or independent legal audit.'))
    return json.dumps(dict(claims=result,scope=dict(claims=len(result),units=6,
        independent_review='NOT_RUN',atomic_claim_census=False)),ensure_ascii=False,indent=2)+'\n'
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    body=make()
    if a.check:
        if not OUT.exists() or OUT.read_text()!=body:raise SystemExit('Stale CDTM/VAX note-claim artifact')
    else:OUT.write_text(body)
    print('CDTM/VAX 13 claims source-bound; independent audit not inferred')
if __name__=='__main__':main()
