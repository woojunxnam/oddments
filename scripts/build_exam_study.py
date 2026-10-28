#!/usr/bin/env python3
"""Build an exam-first learning overlay; never alter source notes or question archives."""
from __future__ import annotations
import argparse, copy, hashlib, html, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build_payload() -> dict:
    note_path=ROOT/'notes/guide.json'; author_path=ROOT/'notes/study/guide.json'
    notes=json.loads(note_path.read_text()); data=json.loads(author_path.read_text())
    chapters={c['id']:c for c in notes['chapters']}
    units={u['id']:(c,u) for c in notes['chapters'] for u in c['units']}
    modules={m['id']:m for m in data['modules']}
    lessons={x['id']:x for x in data['lessons']}
    if len(lessons)!=len(data['lessons']): raise ValueError('Duplicate lesson ID')
    config=json.loads((ROOT/'site/practice-expansion/publication.json').read_text())
    paths=['practice_expansion/2026-10-23/candidates/questions.json']+[a['path'] for a in config['additional_banks']]
    questions=[]
    for path in paths:
        bank=json.loads((ROOT/path).read_text());questions.extend(bank['questions'])
        if bank['input_guide_sha256']!=digest(note_path): raise ValueError('Question-note snapshot mismatch')
    recommended=set(); revised=set(); held=set()
    if config.get('representative_selection'):
        selection_path=ROOT/config['representative_selection']['path']
        if digest(selection_path)!=config['representative_selection']['sha256']:raise ValueError('Stale representative selection')
        selection=json.loads(selection_path.read_text())
        recommended=set(selection['recommended_ids']);revised=set(selection['new_ids'])
        held={qid for h in selection['holds'] for qid in [h['legacy_question_id'],*h.get('affected_archive_ids',[])]}
    def enrich(x:dict)->None:
        refs=x['note_units']
        if not refs or any(uid not in units for uid in refs): raise ValueError('Unknown source unit '+x['id'])
        x['source_hashes']={uid:units[uid][1]['body_sha256'] for uid in refs}
        x['source_review_dates']=list(dict.fromkeys(units[uid][1]['source_review_date'] for uid in refs))
        x['flags']=sorted({f for uid in refs for f in units[uid][1]['flags']})
        x['source_ids']=list(dict.fromkeys(sid for uid in refs for sid in units[uid][1]['source_ids']))
        x['kind']='source-derived-study-overlay'
    for item in data['lessons']:
        enrich(item); families=set();links=[]
        candidates=[q for q in questions if q['question_id'] not in held and set(item['note_units'])&{e['unit_id'] for e in q['note_evidence']}]
        candidates.sort(key=lambda q:(q['question_id'] not in revised,q['question_id'] not in recommended,hashlib.sha256((item['id']+q['question_id']).encode()).hexdigest()))
        for q in candidates:
            if q['family_id'] in families or set(q.get('inherited_flags',[]))&{'open','source-gap'}:continue
            shared=sorted(set(item['note_units'])&{e['unit_id'] for e in q['note_evidence']})
            links.append(dict(id=q['question_id'],family=q['family_id'],topic=q['topic'],kind=q['question_type'],shared_units=shared,url='../practice-expansion/#'+q['question_id']))
            families.add(q['family_id'])
            if len(links)==3:break
        item['practice_links']=links
    for c in data['comparisons']:
        if c['lesson_id'] not in lessons:raise ValueError('Unknown comparison lesson')
        c['note_units']=c.get('note_units',lessons[c['lesson_id']]['note_units']);enrich(c)
    for c in data['clocks']:enrich(c)
    for m in data['modules']:
        if not m['lessons'] or any(l not in lessons or lessons[l]['module_id']!=m['id'] for l in m['lessons']):raise ValueError('Invalid module lessons')
        if any(c not in chapters for c in m['chapters']):raise ValueError('Invalid chapter')
        m['full_unit_count']=sum(len(chapters[c]['units']) for c in m['chapters'])
    for p in data['plan']:
        if any(m not in modules for m in p['module_ids']):raise ValueError('Invalid study day')
    mapped={code for m in data['modules'] for code in m['competencies']}
    expected={f'{a}.{i}' for a,n in [(1,2),(2,5),(3,8),(4,7)] for i in range(1,n+1)}
    if mapped!=expected:raise ValueError('Blueprint map incomplete')
    if {c for m in data['modules'] for c in m['chapters']}!=set(chapters):raise ValueError('Chapter map incomplete')
    data.update(notes_sha256=digest(note_path),authoring_sha256=digest(author_path),
        question_sources={p:digest(ROOT/p) for p in paths},
        representative_selection=copy.deepcopy(config.get('representative_selection')),
        stats=dict(modules=len(modules),concepts=len(lessons),comparisons=len(data['comparisons']),clocks=len(data['clocks']),sessions=len(data['plan']),competencies=len(mapped),chapters=len(chapters),linked_questions=len({q['id'] for l in data['lessons'] for q in l['practice_links']})))
    return data

def outputs()->dict[Path,str]:
    d=build_payload(); esc=html.escape
    manifest={k:d[k] for k in ['schema_version','edition','edited_at','notes_sha256','authoring_sha256','question_sources','representative_selection','stats','source_policy','blueprint']}
    payload=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    body=''.join(f'<section><h2>{esc(m["title"])}</h2><p>{esc(m["exam_task"])}</p>'+''.join(f'<article><h3>{esc(l["title"])}</h3><p><strong>핵심:</strong> {esc(l["core"])}</p><p>{esc(l["why"])}</p><p><strong>혼동 방지:</strong> {esc(l["trap"])}</p><p><strong>설명해 보기:</strong> {esc(l["recall"])}</p><p>원문 기준: {esc(", ".join(l["source_review_dates"]))} · 주의: {esc(", ".join(l["flags"]) or "아래 본문 조건 확인")}</p><p>'+''.join(f'<a href="./#chapter/{next(c["id"] for c in json.loads((ROOT/"notes/guide.json").read_text())["chapters"] if any(u["id"]==uid for u in c["units"]))}/{uid}">{esc(uid)} 원문</a> ' for uid in l['note_units'])+'</p></article>' for l in d['lessons'] if l['module_id']==m['id'])+'</section>' for m in d['modules'])
    static='<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MPJE 법규 학습 · 전체 읽기</title><style>body{font:18px/1.8 system-ui,sans-serif;max-width:850px;margin:32px auto;padding:0 22px;overflow-wrap:anywhere}article{border-bottom:1px solid #ccc;padding:16px 0}a{display:inline-block;margin:4px}@media print{article{break-inside:avoid}}</style><link rel="stylesheet" href="../assets/learning-tools.css" data-oddments-tools><script src="../assets/learning-tools.js" defer data-oddments-tools></script><header><a href="./#study">시험 학습 화면</a><a href="book.html">전체 상세노트</a><h1>MPJE 법규 학습</h1><p>'+esc(d['source_policy'])+'</p></header><main>'+body+'</main></html>\n'
    return {ROOT/'site/notes/study-data.js':'/* Generated by build_exam_study.py; notes-derived, not a new legal audit. */\nwindow.MPJE_EXAM_STUDY = '+payload+';\n',ROOT/'site/notes/study-build.json':json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',ROOT/'site/notes/study.html':static}

def main()->None:
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    for path,text in outputs().items():
        if a.check:
            if not path.exists() or path.read_text()!=text:raise SystemExit('Stale exam-study output: '+str(path))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    print('Exam study: source hashes, 22 competencies and 33 chapters checked; canonical notes/questions unchanged.')
if __name__=='__main__':main()
