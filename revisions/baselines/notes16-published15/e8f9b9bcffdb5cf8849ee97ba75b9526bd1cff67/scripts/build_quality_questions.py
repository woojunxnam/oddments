#!/usr/bin/env python3
"""Build individually authored practice revisions, preserving inherited source boundaries."""
from __future__ import annotations
import hashlib,json,random,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'practice_expansion/2026-10-27-quality'
H=lambda b:hashlib.sha256(b).hexdigest()
FRESH={
 'FEDRX':('21 CFR Part 1306 — selected prescription, partial-fill and transfer provisions','https://www.ecfr.gov/current/title-21/chapter-II/part-1306','Selected §§1306.03–.05, .08, .11–.13, .22–.25; eCFR title editorial currency 2026-10-23.'),
 'MA23':('M.G.L. c.94C §23','https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23','CII validity/refill and II–III supply categories; no new interpretation of unresolved overlaps.'),
 'HIPMIN':('HHS Minimum Necessary Requirement','https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/minimum-necessary-requirement/index.html','Treatment disclosure exception and role-based workforce access.'),
 'HIPACCESS':('45 CFR 164.524 — access to PHI','https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.524','§164.524(b)(2): initial 30 days and one documented extension; title currency 2026-10-23.'),
 'CLOZ':('FDA removes clozapine REMS','https://www.fda.gov/drugs/drug-safety-communications/fda-removes-risk-evaluation-and-mitigation-strategy-rems-program-antipsychotic-drug-clozapine','REMS removal June 13, 2025; continued labeling-based monitoring and risk.'),
 'INVENTORY':('21 CFR 1304.11 — inventory requirements','https://www.ecfr.gov/current/title-21/chapter-II/part-1304/subject-group-ECFR9944e94ba5f1eb0/section-1304.11','Initial zero inventory, opening/closing, biennial interval, on-hand and sealed-liner records; title currency 2026-10-23.'),
 'RECALL':('21 CFR 7.3 — recall definitions','https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-7/subpart-A/section-7.3','Recall, market withdrawal and stock recovery distinctions; title currency 2026-10-23.'),
 'LOSS':('21 CFR 1301.76 — practitioner security controls','https://www.ecfr.gov/current/title-21/chapter-II/part-1301/subject-group-ECFRa7ff8142033a7a2/section-1301.76','§1301.76(b): written notice within one business day, completed electronic Form106 within45 days; title currency 2026-10-23.')}
def parse():
 out=[];cur=None
 for p in sorted((BASE/'authoring').glob('*.txt')):
  for n,line in enumerate(p.read_text().splitlines(),1):
   if not line.strip():continue
   x=line.split('|')
   if line.startswith('@'):
    if cur:out.append(cur)
    if len(x)==4:x.append('')
    assert len(x)==5,(p,n)
    cur=dict(number=int(x[0][1:]),area=int(x[1]),topic=x[2],units=x[3].split(','),fresh=[v for v in x[4].split(',') if v],options=[])
   elif x[0] in ('S','Q','E'):
    assert len(x)==2,(p,n);cur[dict(S='scenario',Q='lead',E='core')[x[0]]]=x[1]
   elif x[0] in ('+','-'):
    assert len(x)==3,(p,n);cur['options'].append((x[0]=='+',x[1],x[2]))
   else:raise ValueError((p,n,line))
 if cur:out.append(cur)
 return out

def build():
 guide_raw=(ROOT/'notes/guide.json').read_bytes();g=json.loads(guide_raw)
 units={u['id']:(c['id'],u) for c in g['chapters'] for u in c['units']}
 sources={};items=[]
 for a in parse():
  i=a['number'];kind='SATA' if 'ALL' in a['lead'] else 'SBA'
  assert sum(x[0] for x in a['options']) >=1
  if kind=='SBA':assert sum(x[0] for x in a['options'])==1
  assert len(a['options'])==(5 if kind=='SATA' else 4),(i,kind)
  assert len(set(x[1] for x in a['options']))==len(a['options'])
  sid=[];evidence=[]
  for uid in a['units']:
   assert uid in units,(i,uid)
   cid,u=units[uid];sid+=u['source_ids']
   evidence.append(dict(unit_id=uid,title=u['title'],body_sha256=u['body_sha256'],inherited_note_review_date=u['source_review_date'],inherited_flags=u['flags'],url=f'https://woojunxnam.github.io/oddments/notes/#chapter/{cid}/{uid}'))
  sid=list(dict.fromkeys(sid))
  for s in sid:sources[s]=g['sources'][s]
  fresh=[]
  for token in a['fresh']:
   title,url,scope=FRESH[token];s='fresh-20261027-'+token.lower();sources[s]=dict(id=s,title=title,url=url,checked_at='2026-10-27',access='Official public HTML read',scope_note=scope)
   fresh.append(dict(source_id=s,accessed_at='2026-10-27',scope=scope));sid.append(s)
  opts=list(a['options']);random.Random('MA-REV-'+str(i)).shuffle(opts)
  choices=[dict(id=chr(65+j),text=v[1]) for j,v in enumerate(opts)]
  keys=[chr(65+j) for j,v in enumerate(opts) if v[0]]
  lead=a['lead']+(' Select ONE answer.' if kind=='SBA' and 'Select ONE' not in a['lead'] else '')
  q=dict(question_id=f'MA-REV-{i:04}',family_id=f'REV-{i:03}',topic=a['topic'],area=a['area'],question_type=kind,practice_angle='individually-authored-application',collection_id='quality-20261027',scenario=a['scenario'],lead_in=lead,stem=a['scenario']+'\n\n'+lead,
    choices=choices,correct_choice_ids=keys,explanation=dict(core_reasoning=a['core'],choice_analysis={chr(65+j):v[2] for j,v in enumerate(opts)},learning_boundary='한 판단을 위한 개별 작성 사례. 기존 원칙을 더 명확한 사례로 연습하며 새로운 법규 96개 또는 최근 기출의 재현이라는 뜻은 아닙니다.'),note_evidence=evidence,source_ids=sid,
    authority='; '.join(sources[s]['title'] for s in sid),primary_source_read_records=fresh,additional_primary_evidence=[],authority_level='INTEGRATED_NOTES_WITH_EXPLICIT_SELECTED_PRIMARY_READS',primary_source_verification='AUTHOR_SOURCE_REVIEW_NOT_INDEPENDENT_ITEM_AUDIT',source_boundary='기존 노트에 기반한 하위 규칙과 별도로 표시한 원문 열람 범위만 사용합니다. 기존 OPEN이나 장 전체를 이번에 재검증한 것으로 보지 않습니다.',inherited_flags=list(dict.fromkeys(f for e in evidence for f in e['inherited_flags'])),authored_at='2026-10-27',edition='2026-10-27.quality1',publication_status='PUBLISHED_PRACTICE',online_practice_enabled=True,verification_status='NOT_INDEPENDENTLY_REVIEWED',independent_legal_audit=None,independent_realism_audit=None,duplicate_review_status='FULL_BANK_STRUCTURAL_COMPARISON_AND_EDITORIAL_TOPIC_REVIEW',difficulty_status='NOT_CALIBRATED',_statement_truth={chr(65+j):v[0] for j,v in enumerate(opts)})
  q['content_sha256']=H(json.dumps(q,ensure_ascii=False,sort_keys=True).encode());items.append(q)
 assert [a['question_id'] for a in items]==[f'MA-REV-{i:04}' for i in range(1,97)]
 out=dict(schema_version='notes-practice-quality/1',edition='2026-10-27.quality1',authored_at='2026-10-27',publication_status='PUBLISHED_PRACTICE',independent_review_status='NOT_INDEPENDENTLY_REVIEWED',input_guide_sha256=H(guide_raw),input_guide_edition=g['edition'],default_jurisdiction='Massachusetts',construction='96 individually authored cases; no numerical/name-only expansion. Existing principles recur intentionally; no claim of 96 new legal rules or psychometric equivalence.',stats=dict(questions=len(items),families=len(items)),sources=sources,questions=items)
 (BASE/'questions.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('Built',len(items),'items',sum(q['question_type']=='SATA' for q in items),'SATA')
 return out
if __name__=='__main__':build()
