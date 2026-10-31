#!/usr/bin/env python3
"""Materialize explicitly authored CDTM05-12 note-claim evidence.

This script attaches hashes to the author's ten pre-specified assertions.
It does NOT infer legal truth from text or grant independent audit status.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from notes_revision import ROOT, load_notes

EVIDENCE = 'reports/full-corpus-review/evidence/cdtm0512-official-crosscheck.json'
OUT = ROOT/'reports/full-corpus-review/cdtm05-12-note-claims.json'
CHECKED_AT = '2026-10-30'

# Each statement is author-curated and tied to listed primary-source clauses.
CURATED = [
 ('CDTM0512-CE-01','w3-d-4','연간 일반 CE 20시간에 CDTM 관련 최소 5시간을 추가하여 총 25시간이며 여러 CPA를 자동으로 5시간씩 누적하지 않는다.',['247 CMR 16.02(1)(e)','Board Policy 2021-04 §IV']),
 ('CDTM0512-CE-02','w3-d-4','CDTM 처방 시 개인 MCSR, 관련 biennial training, MassHealth participation-or-application attestation과 별도의 CE 증빙 보존을 확인한다.',['247 CMR 16.02(1)(f)1–3','247 CMR 16.02(2)']),
 ('CDTM0512-SET-01','w3-d-5','Hospital, LTCF, hospice, ambulatory clinic의 승인권자는 setting별로 다르며 ambulatory clinic은 규정의 on-site supervision 조건도 충족한다.',['247 CMR 16.03(1)–(4)']),
 ('CDTM0512-SET-02','w3-d-5','한 setting의 CDTM 승인만으로 별도 시설의 승인 또는 retail 추가 제한을 자동으로 충족하지 않는다.',['247 CMR 16.03 introductory clause, (1)–(5)']),
 ('CDTM0512-REF-01','w3-d-6','Retail CDTM 환자는 18세 이상이어야 하고 supervising physician의 환자별 written referral 및 primary/secondary diagnoses를 확인한다.',['247 CMR 16.03(5)(a),(c)1–3']),
 ('CDTM0512-CONS-01','w3-d-6','Original consent는 physician custody에 두고 pharmacist에게 24시간 이내 사본을 보내며 양쪽 기록을 유지한다.',['247 CMR 16.03(5)(c)4,(d)1–3','247 CMR 16.04(6)']),
 ('CDTM0512-EXT-01','w3-d-7','Retail CDTM 치료 연장은 기본 30일 두 차례이며 추가 연장은 physician의 환자별 referral와 CPA에 구체적으로 규정되어야 한다.',['247 CMR 16.03(5)(e)1.a']),
 ('CDTM0512-SCHED-01','w3-d-7','Retail CPA의 Schedule II–V 처방 금지와 별도의 유효한 practitioner Schedule III 처방의 통상적 조제는 다른 행위다.',['247 CMR 16.03(5)(e)3–4','M.G.L. c.94C §17(c)']),
 ('CDTM0512-CLOCK-01','w3-d-8','Pharmacist의 initial Rx/변경/중단 copy는 issuance 후 24시간 이내 의사에게 전달하며 urgent 시 더 신속히 통지한다.',['247 CMR 16.03(5)(e)2']),
 ('CDTM0512-CPA-01','w3-d-8','CPA에는 구체적 communication 및 supervision 절차가 필요하고 적어도 2년마다 review·renew하며 종료 시 continuation 및 환자 서면 통지를 다룬다.',['247 CMR 16.04(2),(4)–(6)']),
]


def make() -> str:
    evidence_raw = (ROOT/EVIDENCE).read_bytes()
    evidence = json.loads(evidence_raw)
    assert evidence['schema_version'] == 'cdtm0512-official-crosscheck/1'
    assert evidence['provenance'] == 'AUTHOR_OFFICIAL_SOURCE_TEXT_AND_SCREENSHOT_CHECK_NOT_INDEPENDENT_AUDIT'
    eff = load_notes(ROOT)
    assert eff['edition'] == '2026-10-30.cdtm05-12.1'
    units = {unit['id']: unit for chapter in eff['chapters'] for unit in chapter['units']}
    records=[]
    for identifier,unit_id,statement,authorities in CURATED:
        unit=units[unit_id]
        assert unit['content_version'] == eff['edition'], unit_id
        records.append(dict(
            claim_id=identifier, unit_id=unit_id, statement_ko=statement,
            authority_clauses=authorities, review_status='AUTHOR_SOURCE_CHECKED',
            checked_at=CHECKED_AT,
            reviewer_provenance='AUTHOR_NOT_INDEPENDENT_20261030_CDTM0512',
            source_evidence=EVIDENCE,
            source_evidence_sha256=hashlib.sha256(evidence_raw).hexdigest(),
            unit_content_sha256=unit['body_sha256'],
            scope='Only the explicit listed claim cluster; not unit-wide atomic census or independent legal audit.'
        ))
    return json.dumps({'claims':records,'scope':{'ids':len(records),'note_units':5,
            'atomic_claim_census':False,'independent_review':'NOT_RUN'}},
            ensure_ascii=False,indent=2)+'\n'


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument('--check',action='store_true')
    opt=p.parse_args()
    content=make()
    if opt.check:
        if not OUT.exists() or OUT.read_text()!=content:
            raise SystemExit('Stale author claim file: '+str(OUT))
    else:
        OUT.write_text(content)
    print('Checked 10 explicitly authored CDTM claims; no independent audit conferred.')


if __name__=='__main__':
    main()
