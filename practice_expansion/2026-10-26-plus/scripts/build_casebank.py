#!/usr/bin/env python3
"""Build original conditional application exercises; not recalled examination content.

Question records are deterministic. Related variants are tagged with one family so
practice sessions never count nine siblings as nine independent reasoning models.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import argparse, hashlib, itertools, json, random, re, runpy
from pathlib import Path

PACKAGE=Path(__file__).resolve().parents[1]
ROOT=PACKAGE.parents[1]
DATE='2026-10-26'
EDITION='2026-10-26.casebank-plus.v1'

def sha(value):
    if not isinstance(value,bytes): value=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    return hashlib.sha256(value).hexdigest()

def tidy(s):
    # Readability only: do not rewrite English legal terms or legal conclusions.
    s=s.replace('現행','현행')
    s=re.sub(r'([가-힣])([A-Za-z0-9])',r'\1 \2',s)
    s=re.sub(r'([A-Za-z0-9])([가-힣])',r'\1 \2',s)
    s=re.sub(r'([.!?])([가-힣A-Z])',r'\1 \2',s)
    return s

# Model allocations are editorial practice coverage, not claims about current test frequency.
SBA_MODELS={1:['CE','PERSON','STAFF','LICENSE','MOR','CE','PERSON','STAFF'],
            2:['COUNSEL','PRIVACY','DUR','VACC','ADMIN','CDTM','ACCESS','REMS','OUD','COUNSEL','PRIVACY','DUR','VACC','ADMIN','CDTM','ACCESS','REMS','OUD','ADMIN','PRIVACY'],
            3:['RX','EPCS','CII','PARTIAL','REFILL','LABEL','PACK','PMP','EPCS','PARTIAL','LABEL','PMP'],
            4:['INVENTORY','ORDER','DISPOSE','STORAGE','AUTO','COMPOUND','STERILE','HD','SUPPLY','CQI']}
SATA_MODELS={1:['CE','PERSON','STAFF','LICENSE','MOR','PERSON'],
             2:['COUNSEL','PRIVACY','DUR','VACC','ADMIN','CDTM','ACCESS','REMS','OUD','COUNSEL','PRIVACY','VACC','ADMIN','CDTM','ACCESS','REMS','OUD'],
             3:['RX','EPCS','CII','PARTIAL','REFILL','LABEL','PACK','PMP','RX'],
             4:['INVENTORY','ORDER','DISPOSE','STORAGE','COMPOUND','STERILE','HD','CQI']}

# These are fresh source-read records, NOT item-level independent audit certificates.
FRESH={
 'src-0dcfd81d59da':'Policy 2026-02: supervisory ratios and dedicated-training conditions; official PDF extracted text',
 'src-55b6c21dc30e':'Policy 2024-05: Schedule II/III 90-day categories; official PDF extracted text',
 'src-1bccdb2e07d2':'Policy 2023-10: initial unfilled EPCS and original paper/fax/oral distinction; official PDF extracted text',
 'src-368bb8382bd0':'DCP 26-03-124: medication administration eligibility, training, record and communication conditions; official PDF extracted text',
 'src-351267598b0b':'247 CMR16: CDTM qualifications, retail restrictions and communication; official PDF extracted text',
 'src-6251c99ae2dd':'Policy 2023-02 revised 9/4/2025: vaccination personnel qualifications and workflow; official PDF extracted text',
 'src-a3da4c85d7a6':'Policy 2026-01: confirmed loss/theft, insignificant loss and dispensing-error distinction; official PDF extracted text',
 'src-6e9b85106a29':'Policy 2026-03: action-level tables and response; official extracted text, full visual PDF verification unavailable',
 'src-ec307e03cb52':'105 CMR222: MIIS reporting and data-sharing objection clocks; official PDF extracted text',
 'src-853b2c5f4d9e':'247 CMR15: CQI notification, 24-hour initial documentation and records; official PDF extracted text',
 'src-386cb3e809e7':'21 CFR1306: prescriptions, transfers and partial fills; current HTML through 10/22/2026; §1306.07(f) 45-day direct-delivery condition additionally checked',
 'src-f2bf7b29954d':'21 CFR1304.11: initial, biennial and opened-container inventory; current official HTML',
 'src-e353303b3fff':'21 CFR1305: paper/CSOS stock ordering and fulfillment; current official HTML',
 'src-9b6deb426285':'21 CFR1317: authorized collection and controlled-substance destruction; current official HTML',
 'src-3c0c5d9726e8':'16 CFR1700.14: product-specific packaging exceptions; current official HTML through 10/22/2026',
 'src-fbc9487ba46f':'FDA clozapine REMS removal effective 6/13/2025, with continued label-based monitoring; current official announcement',
 'src-da8a8280d110':'247 CMR9: reviewed text through counseling and selected operations; not a complete new audit of every subsection',
}

def build():
    guide_raw=(ROOT/'notes/guide.json').read_bytes();guide=json.loads(guide_raw)
    units={u['id']:(c['id'],u) for c in guide['chapters'] for u in c['units']}
    groups=runpy.run_path(str(PACKAGE/'authoring/atoms.py'))['GROUPS']
    cases=runpy.run_path(str(PACKAGE/'authoring/cases.py'))['CASES']
    sources=guide['sources'];out=[];truth_seen=set();family_count=Counter();positions=Counter()
    # Source lookup by URL makes this robust to previously generated source identifiers.
    for sid,entry in sources.items():
        url=entry['url']
        if '2021-04-continuing-education' in url:FRESH[sid]='Policy 2021-04 revised 9/4/2025: CE totals, categories, grace and email notice; official PDF extracted text'
        if '2020-15-scope-of-practice' in url:FRESH[sid]='Policy 2020-15 revised 11/6/2025: personnel roles; 2026 administration expansion read separately'
        if '2023-07-non-sterile-compounding' in url:FRESH[sid]='Policy 2023-07 revised 2/6/2025: nonsterile definitions, records and complex licensing; official PDF extracted text'
    def record(family,topic,area,scenario,lead,opts,unit_ids,authority,reason,facts,style,concepts,kind='SBA'):
        assert len(opts) in (4,5) and len({o['text'] for o in opts})==len(opts)
        assert sum(o['correct'] for o in opts)==1 if kind=='SBA' else 1<=sum(o['correct'] for o in opts)<len(opts)
        unit_ids=sorted(set(unit_ids));assert all(u in units for u in unit_ids),unit_ids
        idx=len(out)+1;qid=f'MA-CASE-{idx:04}';family='PLUS-'+family;family_count[family]+=1
        rng=random.Random('casebank-plus:'+qid);opts=[dict(x) for x in opts];rng.shuffle(opts)
        choices=[];answers=[];analysis={};truth={}
        for i,o in enumerate(opts):
            letter=chr(65+i);choices.append(dict(id=letter,text=o['text']));truth[letter]=bool(o['correct'])
            if o['correct']:answers.append(letter)
            analysis[letter]=('선택할 항목. ' if o['correct'] else '선택하지 않을 항목. ')+tidy(o['reason_ko'])
        if kind=='SBA':positions[answers[0]]+=1
        evidence=[];source_ids=set();flags=set()
        for uid in unit_ids:
            chapter,u=units[uid];source_ids.update(u['source_ids']);flags.update(u.get('flags',[]))
            evidence.append(dict(unit_id=uid,title=u['title'],body_sha256=u['body_sha256'],inherited_note_review_date=u.get('source_review_date'),inherited_flags=u.get('flags',[]),url=f'https://woojunxnam.github.io/oddments/notes/#chapter/{chapter}/{uid}'))
        extra=[]
        if family=='PLUS-SC31':
            extra=[dict(title='새로 대조한 연방 규칙: 21 CFR1306.07(f)',url='https://www.ecfr.gov/current/title-21/chapter-II/part-1306#p-1306.07(f)',accessed_at=DATE,scope='Named patient, registered location, no general stock, administration not later than 45 days after practitioner receipt. Separate from the inherited note summary.')]
        source_reads=[dict(source_id=sid,accessed_at=DATE,scope=FRESH[sid]) for sid in sorted(source_ids) if sid in FRESH]
        q=dict(question_id=qid,family_id=family,topic=topic,area=area,question_type=kind,
               practice_angle=style,collection_id='plus-20261026',scenario=scenario,lead_in=lead,
               stem=scenario+'\n\n'+lead,choices=choices,correct_choice_ids=answers,
               explanation=dict(core_reasoning=tidy(reason),choice_analysis=analysis,
                 learning_boundary='같은 모델의 9개 문항은 조건·기록 조합을 바꾸는 연습 변형이다. 독립된 9개 법규나 실제 기출로 세지 않으며, 세트에는 모델별 한 문항만 선택한다.'),
               note_evidence=evidence,source_ids=sorted(source_ids),authority=authority,
               primary_source_read_records=source_reads,additional_primary_evidence=extra,
               authority_level='INTEGRATED_NOTES_WITH_SEPARATELY_IDENTIFIED_PRIMARY_SOURCE_READS',
               primary_source_verification='AUTHOR_SOURCE_REVIEW_NOT_INDEPENDENT_ITEM_AUDIT',
               source_boundary='통합노트의 확인된 하위 규칙과 명시한 추가 원문에 기반한다. 연결된 장 전체의 OPEN 문제가 해결됐다는 뜻은 아니다. 주어진 조건 밖의 업무 허용으로 확대하지 않는다.',
               inherited_flags=sorted(flags),authored_at=DATE,edition=EDITION,
               publication_status='PUBLISHED_PRACTICE',online_practice_enabled=True,
               verification_status='NOT_INDEPENDENTLY_REVIEWED',independent_legal_audit=None,independent_realism_audit=None,
               duplicate_review_status='CONDITION_VARIANTS_TAGGED_AUTOMATED_COMPARISON',difficulty_status='NOT_CALIBRATED',
               conditional_facts=facts,concept_ids=concepts,_statement_truth=truth)
        q['content_sha256']=sha({k:q[k] for k in ['question_id','family_id','stem','choices','correct_choice_ids','explanation','note_evidence','source_ids']})
        out.append(q)
    for c in cases:
        record(c['family'],c['topic'],c['area'],c['scenario'],c['lead']+' Select ONE answer.',c['options'],c['units'],c['authority'],c['reason'],c['facts'],c['style'],[c['family']])
    # Work queues have independent propositions in one practical domain. No irrelevant Case B.
    for kind,allocation in [('SBA',SBA_MODELS),('SATA',SATA_MODELS)]:
        serial=0
        for area,keys in allocation.items():
            for key in keys:
                serial+=1;g=groups[key];family=('WQ' if kind=='SBA' else 'MR')+f'{serial:02}'
                rng=random.Random(EDITION+family+key)
                for v in range(9):
                    n=4 if kind=='SBA' else 5
                    # Explore different material action subsets, never count option shuffles alone.
                    for attempt in range(2000):
                        atoms=rng.sample(g['atoms'],n)
                        nc=1 if kind=='SBA' else 1+((serial+v)%4)
                        true_ids=set(rng.sample(range(n),nc))
                        fingerprint=tuple(sorted((a['id'],i in true_ids) for i,a in enumerate(atoms)))
                        if fingerprint not in truth_seen:truth_seen.add(fingerprint);break
                    else:raise ValueError('Cannot produce a new condition combination')
                    opts=[];uids=[];decisions=[]
                    for i,a in enumerate(atoms):
                        correct=i in true_ids;txt=a['good'] if correct else a['bad'];why=a['reason_ko']
                        if not correct:why+=' 올바른 처리: '+a['good']
                        opts.append(dict(text=txt,reason_ko=why,correct=correct));uids+=a['units']
                        decisions.append(dict(concept_id=a['id'],proposed_action_supported=correct))
                    lead=('Which ONE proposed handling is supported by the applicable requirements?' if kind=='SBA' else 'Which proposed actions are supported by the applicable requirements? Select ALL that apply.')
                    scope=' Each option describes a separate work-queue record. Assume all other prerequisites are satisfied; judge the action and facts actually stated, not an unstated exception.'
                    record(family,g['title'],area,g['context']+scope,lead,opts,uids,g['authority'],
                       '각 선택지는 별도 기록이다. 같은 약·업무 이름보다 자격, 실제 행위, 시작점과 예외를 비교한다. '+ ' '.join(a['reason_ko'] for a in atoms),
                       dict(action_records=decisions), 'workqueue' if kind=='SBA' else 'multiple-response',[a['id'] for a in atoms],kind)
    assert len(out)==1152 and len(family_count)==128 and set(family_count.values())=={9}
    areas=Counter(q['area'] for q in out);assert dict(areas)=={1:252,2:378,3:279,4:243},areas
    chosen={s for q in out for s in q['source_ids']};refs={s:sources[s] for s in sorted(chosen)}
    payload=dict(schema_version='notes-casebank-plus/1.0',edition=EDITION,authored_at=DATE,
      publication_status='PUBLISHED_PRACTICE',independent_review_status='NOT_INDEPENDENTLY_REVIEWED',
      input_guide_sha256=sha(guide_raw),input_guide_edition=guide['edition'],
      source_basis='Week 1–6 integrated notes, with separate source-read records and explicit new-source expansions.',
      default_jurisdiction='Massachusetts; federal-only scope is explicit when used',
      intended_outline_window='Current MPJE before March 1, 2027; not UMPJE or the future outline.',
      construction='38 single-case models, 50 independent-action SBA work queues, and 40 multiple-response models; nine condition variants each. Not 1,152 unrelated legal decisions.',
      scoring='Strict all-or-nothing practice feedback; no official scaled score, CAT or pass prediction.',
      stats=dict(questions=len(out),families=len(family_count),single_case_models=38,workqueue_models=50,multiple_response_models=40,
       types=dict(Counter(q['question_type'] for q in out)),areas={str(k):v for k,v in sorted(areas.items())},
       referenced_note_units=len({e['unit_id'] for q in out for e in q['note_evidence']}),linked_bibliography_entries=len(refs),
       single_answer_positions=dict(sorted(positions.items())),multiple_response_correct_count={str(k):v for k,v in sorted(Counter(len(q['correct_choice_ids']) for q in out if q['question_type']=='SATA').items())}),
      sources=refs,questions=out)
    return payload

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
    result=build();p=PACKAGE/'questions.json';b=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode()
    if args.check:
        assert p.read_bytes()==b,'Generated casebank differs from authoring source'
    else:p.write_bytes(b)
    print(json.dumps(result['stats'],ensure_ascii=False,indent=2))
if __name__=='__main__':main()
