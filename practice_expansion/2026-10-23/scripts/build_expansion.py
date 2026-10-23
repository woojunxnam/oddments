#!/usr/bin/env python3
"""Build a segregated, NOT RELEASED notes-derived review corpus. Python 3.10+."""
from __future__ import annotations
import argparse, collections, hashlib, json, random, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITION = '2026-10-23.draft1'
BASE_COMMIT = '503397955cf123c9369a4d476dbc874cef84ff2f'

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def canonical_hash(obj: object) -> str:
    return digest(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())

def normalized(text: str) -> str:
    return re.sub(r'[^a-z0-9가-힣]+', ' ', text.casefold()).strip()

def parse_families() -> list[dict]:
    out=[]
    for path in sorted((ROOT/'authoring').glob('*.txt')):
        for b in re.split(r'\n\s*\n',path.read_text(encoding='utf-8').strip()):
            lines=[x.strip() for x in b.splitlines() if x.strip()]
            if len(lines)!=7 or not lines[0].startswith('@'):
                raise ValueError(f'{path.name}: expected one header, two cases and four pairs')
            h=lines[0][1:].split('|')
            if len(h)!=5 or not lines[1].startswith('S|') or not lines[2].startswith('R|'):
                raise ValueError(f'{path.name}: malformed header or cases')
            fid,area,comp,units,title=h
            if comp.split('.')[0]!=area:
                raise ValueError(f'{fid}: provisional area/competency mismatch')
            pairs=[]
            for row in lines[3:]:
                vals=row.split('|')
                if len(vals)!=4 or vals[0]!='P' or not all(vals[1:]):
                    raise ValueError(f'{fid}: malformed proposition pair')
                pairs.append(dict(true=vals[1],false=vals[2],reason_ko=vals[3]))
            out.append(dict(family_id=fid,area=int(area),competency_provisional=comp,
                            note_unit_ids=units.split(','),title=title,
                            case_a=lines[1][2:],case_b=lines[2][2:],pairs=pairs,
                            authoring_file=f'authoring/{path.name}'))
    if len(out)!=256 or len({f['family_id'] for f in out})!=256:
        raise ValueError('Expected exactly 256 unique authored families')
    return out

EXCLUSIONS={
 'MOR04':'No item decides the unresolved exact 30-/100-day interim boundary or conflicting departure deadlines.',
 'MOR05':'Only handover inventory and signature conditions; unresolved MOR deadline overlaps are not tested.',
 'CDTM12':'No cannabis scheduling, temporary telemedicine, or unread statewide HIV protocol detail is tested.',
 'PMP02':'Only the described gabapentin/pregabalin distinction; cannabis and temporary scheduling topics excluded.',
 'PART05':'Narrow initial out-of-state and requested-remainder distinction; redacted-copy submission operations excluded; independent legal confirmation still required.',
 'PART06':'Specified ordinary counter-pickup paths, not the unresolved redacted-copy reporting channel.',
 'REF08':'Only ordinary VI validity and transfer rights; disputed 14-/30-day emergency continuation not tested.',
 'SALE04':'Only stated veterinary scope and federal VCPR boundary; state-specific remote-practice variations not inferred.',
 'ORD06':'The specific facility/pathway is stipulated; no resolution of all Board/DCP overlap is claimed.',
 'FDA03':'No exemption extension date or numerical eligibility criterion is asserted; only the limits of an expressly stipulated exemption.'
}

def build(guide: dict, guide_bytes: bytes) -> dict:
    units={u['id']:{**u,'chapter_id':c['id'],'chapter_title':c['title']} for c in guide['chapters'] for u in c['units']}
    families=parse_families();questions=[];used=set();single_counter=0
    for fi,f in enumerate(families):
        for uid in f['note_unit_ids']:
            if uid not in units: raise ValueError(f"{f['family_id']}: unknown unit {uid}")
            used.add(uid)
        evidence=[{'unit_id':uid,'title':units[uid]['title'],
                   'body_sha256':digest(units[uid]['body'].encode()),
                   'inherited_note_review_date':units[uid]['source_review_date'],
                   'inherited_flags':units[uid]['flags'],
                   'url':f"https://woojunxnam.github.io/oddments/notes/#chapter/{units[uid]['chapter_id']}/{uid}"}
                  for uid in f['note_unit_ids']]
        srcs=sorted({sid for uid in f['note_unit_ids'] for sid in units[uid]['source_ids']})
        for variant in range(4):
            qid=f'MA-EXP-{len(questions)+1:04d}'
            rng=random.Random(f'{EDITION}:{qid}')
            if variant==0:
                selection=[(0,True),(1,False),(2,False),(3,False)]
                prompt='Which conclusion correctly addresses Case A? Select ONE answer.'
                typ='SBA';negative=False;angle='case-a-application'
            elif variant==1:
                selection=[(0,False),(1,True),(2,False),(3,False)]
                prompt='Which conclusion correctly addresses Case B? Select ONE answer.'
                typ='SBA';negative=False;angle='case-b-application'
            elif variant==2:
                k=fi%4+1; true_indices=set(rng.sample(range(4),k))
                selection=[(i,i in true_indices) for i in range(4)]
                prompt='Which statements accurately apply to the described cases or the related requirements? Select ALL that apply.'
                typ='SATA';negative=False;angle='combined-requirements'
            else:
                selection=[(0,True),(1,True),(2,True),(3,False)]
                prompt='Which proposed interpretation is INCORRECT? Select ONE answer.'
                typ='SBA';negative=True;angle='error-identification'
            rng.shuffle(selection)
            if typ=='SBA':
                def is_answer(x): return (not x[1]) if negative else x[1]
                a=next(x for x in selection if is_answer(x));others=[x for x in selection if x!=a]
                selection=others[:];selection.insert(single_counter%4,a);single_counter+=1
            choices=[];answers=[];rationales={};statement_truth={}
            for ci,(pi,truth) in enumerate(selection):
                cid='ABCD'[ci];p=f['pairs'][pi];text=p['true' if truth else 'false']
                right=(not truth) if negative else truth
                choices.append(dict(id=cid,text=text))
                if right:answers.append(cid)
                status=('오류를 고르는 문항의 정답' if negative and right else
                        '옳은 설명이므로 오류 선택의 정답이 아님' if negative else
                        '선택해야 하는 옳은 설명' if right else '선택하지 않아야 하는 잘못된 설명')
                rationales[cid]=f'{status}. {p["reason_ko"]}'
                if not truth:rationales[cid]+=f'\n교정된 설명: {p["true"]}'
                statement_truth[cid]=truth
            if len({c['text'] for c in choices})!=4:raise ValueError(qid+' duplicate option')
            flags=sorted({flag for e in evidence for flag in e['inherited_flags']})
            q=dict(question_id=qid,family_id=f['family_id'],topic=f['title'],area=f['area'],
                   competency_provisional=f['competency_provisional'],question_type=typ,
                   practice_angle=angle,negative_lead_in=negative,
                   stem=f"Case A: {f['case_a']}\n\nCase B: {f['case_b']}\n\n{prompt}",
                   choices=choices,correct_choice_ids=answers,
                   explanation=dict(core_reasoning=' '.join(p['reason_ko'] for p in f['pairs']),
                                    choice_analysis=rationales,
                                    learning_boundary='같은 family의 네 문항은 같은 두 사례와 네 판단을 공유하는 연습 변형이다. 독립적인 네 임상 사례로 세지 않는다.'),
                   note_evidence=evidence,source_ids=srcs,
                   authority_level='NOTES_DERIVED_WITH_INHERITED_READING_BIBLIOGRAPHY',
                   primary_source_verification='ITEM_LEVEL_VERIFICATION_PENDING',
                   source_boundary=EXCLUSIONS.get(f['family_id'],
                     'Based on the cited notes. No independent item-level legal or realism review has been completed.'),
                   inherited_flags=flags,authored_at='2026-10-23',edition=EDITION,
                   lifecycle_status='DRAFT',verification_status='NOT_INDEPENDENTLY_REVIEWED',
                   independent_legal_audit=None,independent_realism_audit=None,
                   duplicate_review_status='SEMANTIC_REVIEW_PENDING',publication_eligible=False,
                   difficulty_status='NOT_CALIBRATED',canonical_rule_mapping_status='PENDING',
                   _statement_truth=statement_truth)
            q['content_sha256']=canonical_hash(q);questions.append(q)
    sources={sid:guide['sources'][sid] for sid in sorted({sid for q in questions for sid in q['source_ids']})}
    for s in sources.values():
        if not s['url'].startswith('https://') or 'docs.google.com' in s['url'] or 'drive.google.com' in s['url']:
            raise ValueError('Private/non-https bibliography URL')
    result=dict(schema_version='notes-expansion-draft/1.0',edition=EDITION,
        target_repository='woojunxnam/oddments',base_commit=BASE_COMMIT,
        input_guide_sha256=digest(guide_bytes),input_guide_edition=guide['edition'],
        source_basis='Week 1–6 integrated notes; selected primary-source rechecks documented separately.',
        default_jurisdiction='Massachusetts, unless an item explicitly specifies a federal rule or another setting.',
        intended_outline_window='Before 2027-03-01; item mappings are provisional and not independently audited.',
        status='DRAFT_ONLY_NOT_RELEASED',released_new_questions=0,
        generation_method='256 authored two-case/four-distinction families, each materialized as 3 SBA + 1 SATA. These are related practice variations, not 1024 independent cases.',
        scoring='Local exact-match practice only; not NABP scoring, CAT, scaled score, readiness, or pass prediction.',
        stats=dict(questions=len(questions),families=len(families),shared_case_vignettes=2*len(families),
                   types=dict(collections.Counter(q['question_type'] for q in questions)),
                   areas=dict(collections.Counter(q['area'] for q in questions)),referenced_note_units=len(used),
                   input_note_units=len(units),linked_bibliography_entries=len(sources)),
        sources=sources,questions=questions)
    (ROOT/'candidates').mkdir(exist_ok=True)
    (ROOT/'candidates/questions.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'candidates/questions.jsonl').write_text(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in questions))
    (ROOT/'authoring/families.json').write_text(json.dumps(families,ensure_ascii=False,indent=2)+'\n')
    # Preserve only our notes and public bibliography; never include protected/external question text.
    (ROOT/'research/note_evidence.json').write_text(json.dumps({
        'guide_sha256':digest(guide_bytes),'guide_edition':guide['edition'],
        'scope':'Selected inherited note units, not newly verified official law.',
        'units':[units[i] for i in sorted(used)]},ensure_ascii=False,indent=2)+'\n')
    for bi in range(32):
        part=questions[bi*32:(bi+1)*32]
        packet={'packet_id':f'EXP-REVIEW-{bi+1:02d}','status':'REVIEW_QUEUE_ONLY',
                'notice':'This packet is not a canonical initial-batch audit or release record.',
                'items':[{'question_id':q['question_id'],'content_sha256':q['content_sha256'],
                          'decision':None,'legal_correctness':None,'realism':None,
                          'exact_authority':None,'notes':None} for q in part]}
        (ROOT/f'review/packet-{bi+1:02d}.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n')
    md=['# MA MPJE Notes Expansion — DRAFT review corpus',
        '> 1,024 related exercises / 256 families / 512 shared case vignettes. Independent review pending. Not released.\n',
        '문제·선택지는 영어, 해설은 한국어입니다. 모든 정답은 작성자의 초안이며 독립 검증된 시험 정답이 아닙니다.\n']
    for q in questions:
        md += [f"## {q['question_id']} · {q['family_id']} · {q['question_type']} — {q['topic']}",q['stem'],'']
        md += [f"{c['id']}. {c['text']}" for c in q['choices']]
        md += ['',f"**작성자 정답 초안: {', '.join(q['correct_choice_ids'])}**",q['explanation']['core_reasoning'],'']
        md += [f"**{c['id']}** — {q['explanation']['choice_analysis'][c['id']]}" for c in q['choices']]
        md += ['', '**연결 노트**: '+', '.join(f"[{e['unit_id']}]({e['url']})" for e in q['note_evidence']),
               '**검토 상태**: DRAFT · 법규/현실성 독립 검토 전 · '+q['source_boundary'],'']
    (ROOT/'candidates/complete-practice-draft.md').write_text('\n\n'.join(md)+'\n')
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--guide',type=Path,required=True);args=ap.parse_args()
    raw=args.guide.read_bytes();result=build(json.loads(raw),raw)
    print(json.dumps(result['stats'],ensure_ascii=False,indent=2))

if __name__=='__main__':main()
