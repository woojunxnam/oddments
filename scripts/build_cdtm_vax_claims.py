"""Pin the author-reviewed CDTM13/VAX04 note claims without inventing audit approval."""
import argparse,hashlib,json
from pathlib import Path
from notes_revision import ROOT,load_notes
EVIDENCE='reports/full-corpus-review/evidence/cdtm-vax-official-crosscheck.json'
OUT=ROOT/'reports/full-corpus-review/cdtm-vax-note-claims.json'
RECORDS=[["CDTM1316-CPA-01","w3-d-9","CPA is written and signed with specific disease states, prescribing authority, risk protocols, patient documents, urgent communication and both qualification attestations.","247 CMR 16.04(1)–(2)"],["CDTM1316-DELEG-01","w3-d-9","Delegation terms list delegable and nondelegable duties, manner, duration, scope; interns/technicians remain in 247 CMR8 scope.","247 CMR 16.04(3)"],["CDTM1316-TERM-01","w3-d-10","Before CPA termination the parties arrange continuity and then inform patients of termination and continued therapy in writing.","247 CMR 16.04(5)"],["CDTM1316-REC-01","w3-d-10","Pharmacist retains current CPA/referral/consent copies accessible at primary practice setting; physician retains current originals.","247 CMR 16.04(6)"],["CDTM1316-EMP-01","w3-d-10","Community pharmacy may employ physician for QA review but not for establishing or maintaining CPAs.","247 CMR 16.04(7)(a)–(c)"],["VAX0104-PER-01","w3-c-1","PTT does not fall within policy eligible vaccine personnel; pharmacist, intern, qualifying licensed technician do.","DPH Policy2023-02 Introduction"],["VAX0104-SUP-01","w3-c-1","Intern/technician require on-duty pharmacist approval and qualified immunizing pharmacist direct supervision, not phone-only consent.","DPH Policy2023-02 Introduction, III"],["VAX0104-AGE-01","w3-c-2","Policy's five-year pathway floor is not authority to administer any vaccine outside product or DPH recommendations and standing order.","DPH Policy2023-02 I–II, IV"],["VAX0104-FLU-01","w3-c-2","2026-27 flu standing order includes high-dose influenza vaccine for age18-64 solid-organ transplant recipients on immunosuppressive regimens.","DPH Standing Order2026-06, Procedure 1(b), 5"],["VAX0104-TRAIN-01","w3-c-3","Pharmacist/intern ACPE initial vaccine course is 12 self-study+8 live+IM/SC hands-on assessment, not any 20 hours.","DPH Policy2023-02 III.C.1"],["VAX0104-CPR-01","w3-c-3","Current CPR and evidence on pharmacy file are required; pharmacists need annual one-hour immunization-related CE.","DPH Policy2023-02 III.A–C"],["VAX0104-TECH-01","w3-c-4","Licensed technician must be nationally certified or have 500 hours after license, ACPE six-hour training plus two hours on-the-job, direct supervision and current CPR.","DPH Policy2023-02 III.A–D"],["VAX0104-TECH-02","w3-c-4","Technician may physically prepare/administer only after pharmacist selects/counsels; technician CE at least two hours biennially.","DPH Policy2023-02 III.D.4–5"]]
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
