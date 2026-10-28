#!/usr/bin/env python3
"""Build user-authorized online practice without inventing independent audit evidence.

Archived questions are unchanged. PUBLISHED_PRACTICE is a delivery channel,
not the canonical RELEASED/independently-audited status. Output is a site copy.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'practice_expansion/2026-10-23'
CONFIG = ROOT / 'site/practice-expansion/publication.json'


def replace_exact(text: str, old: str, new: str, count: int = 1) -> str:
    actual = text.count(old)
    if actual != count:
        raise ValueError(f'Unexpected template drift: {old[:75]!r}: {actual} != {count}')
    return text.replace(old, new)


def build_payload() -> dict:
    config = json.loads(CONFIG.read_text(encoding='utf-8'))
    raw = (PACKAGE / 'candidates/questions.json').read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != config['source_sha256']:
        raise ValueError('The archived question source changed; review the publication manifest.')
    source = json.loads(raw)
    if len(source['questions']) != config['question_count']:
        raise ValueError('Question count mismatch.')
    if hashlib.sha256((ROOT / 'notes/guide.json').read_bytes()).hexdigest() != source['input_guide_sha256']:
        raise ValueError('Integrated-note snapshot changed; explicitly reconcile the practice edition.')
    data = copy.deepcopy(source)
    data.update(schema_version='notes-public-practice/1.0', edition=config['edition'],
                status='PUBLISHED_PRACTICE', published_question_count=len(source['questions']),
                publication_date=config['publication_date'],
                independent_review_status='NOT_INDEPENDENTLY_REVIEWED',
                canonical_released_question_count=0, source_sha256=digest)
    data.pop('released_new_questions', None)
    data.pop('base_commit', None)
    for item in data['questions']:
        # Content, answer keys and evidence stay intact; only delivery metadata changes.
        item['source_lifecycle_status'] = item.pop('lifecycle_status')
        item['source_publication_eligible'] = item.pop('publication_eligible')
        item['source_edition'] = item['edition']
        item['edition'] = config['edition']
        item['publication_status'] = 'PUBLISHED_PRACTICE'
        item['online_practice_enabled'] = True
    # Additive bank: preserve every original substantive field and its progress ID.
    total_original = len(data['questions'])
    for item in data['questions']:
        item['collection_id'] = 'original-20261023'
    config_additions = config.get('additional_banks', [])
    collections = [dict(id='original-20261023', title='기존 1,024문항', count=total_original)]
    for addition in config_additions:
        path = (ROOT / addition['path']).resolve()
        if ROOT not in path.parents:
            raise ValueError('Additional bank path escapes repository.')
        raw_plus = path.read_bytes()
        if hashlib.sha256(raw_plus).hexdigest() != addition['sha256']:
            raise ValueError('Additional bank hash changed; reconcile publication metadata.')
        plus = json.loads(raw_plus)
        if len(plus['questions']) != addition['question_count'] or plus['input_guide_sha256'] != source['input_guide_sha256']:
            raise ValueError('Additional bank count or note snapshot mismatch.')
        existing_ids = {q['question_id'] for q in data['questions']}
        if existing_ids.intersection(q['question_id'] for q in plus['questions']):
            raise ValueError('Question IDs collide across collections.')
        for sid, reference in plus['sources'].items():
            if sid in data['sources'] and data['sources'][sid]['url'] != reference['url']:
                raise ValueError('Source ID collision.')
            data['sources'][sid] = reference
        for item in copy.deepcopy(plus['questions']):
            item['source_edition'] = item['edition']
            item['edition'] = config['edition']
            if item['publication_status'] != 'PUBLISHED_PRACTICE' or not item['online_practice_enabled']:
                raise ValueError('Additional publication state is inconsistent.')
            data['questions'].append(item)
        collections.append(dict(id=addition['collection_id'],title=addition['title'],count=len(plus['questions'])))
    data['collections'] = collections
    data['published_question_count'] = len(data['questions'])
    if data['published_question_count'] != config['published_total']:
        raise ValueError('Combined publication count mismatch.')
    data['stats'] = dict(questions=len(data['questions']),
        families=len({q['family_id'] for q in data['questions']}),
        types={kind:sum(q['question_type']==kind for q in data['questions']) for kind in ('SBA','SATA')},
        areas={str(area):sum(q['area']==area for q in data['questions']) for area in (1,2,3,4)})
    data['generation_method'] = 'Original 256 paired-case families plus 128 new conditional models. Nine deliberate condition variants per new model; not 1,152 unrelated legal principles.'
    data['additional_bank_sha256'] = {a['collection_id']: a['sha256'] for a in config_additions}
    from practice_quality import attach
    return attach(data, config.get('representative_selection'))


def render(data: dict) -> str:
    text = (PACKAGE / 'review/reader.template.html').read_text(encoding='utf-8')
    text = replace_exact(text, 'MA MPJE Practice Lab — 1,024 Draft Exercises',
                         'MA MPJE — 1,024문항 온라인 연습')
    text = replace_exact(text, 'Week 1–6 통합노트 기반 신규 연습문항 초안. 독립 검토 전, 기존 공개 문제은행과 분리.',
                         'Week 1–6 통합노트 기반 1,024문항 온라인 학습판. 영어 문제, 한국어 해설, 검색과 오답 복습.')
    text = replace_exact(text, '.pill.draft', '.pill.practice')
    text = replace_exact(text, '<aside class="panel">', '<aside id="controls" class="panel">')
    text = replace_exact(text, '<nav class="topnav" aria-label="외부 학습자료">',
                         '<nav class="topnav" aria-label="학습 메뉴">')
    text = replace_exact(text,
        '<a href="https://woojunxnam.github.io/oddments/notes/" target="_blank" rel="noopener noreferrer">통합노트 ↗</a><a href="https://woojunxnam.github.io/oddments/" target="_blank" rel="noopener noreferrer">기존 공개 문제은행 ↗</a><span>2026.10.23 · 독립 검토 전</span>',
        '<a href="../" id="return-main">← 메인 문제은행</a><a href="../notes/" target="_blank" rel="noopener noreferrer">통합노트 ↗</a><a href="#controls" id="controls-link">검색·세트 설정 ↓</a><span>온라인 공개판 · '+data['publication_date']+'</span>')
    start = text.index('<section class="notice" aria-label="검증 상태">')
    end = text.index('</section>', start) + len('</section>')
    text = text[:start] + '''<details class="notice" id="publication-info"><summary><strong>공개 연습판 · 자료 검토 범위</strong></summary><p>문항은 바로 풀 수 있습니다. 영어 문제와 한국어 해설은 통합노트 기반이며, 문항별 독립 법규 검토·실전 난도 보정은 아직 완료되지 않았습니다. 기존 독립 검토 문제은행과는 별도 학습판입니다.</p><p>256개 사례 묶음의 1,024개 연습 변형입니다. 실제 기출·NABP 공식 채점·합격 예측 자료가 아닙니다. 의심되는 답은 해설에 연결된 노트·출처와 대조하세요.</p></details>''' + text[end:]
    text = replace_exact(text, '<span>연습문항 초안</span>', '<span>바로 풀 수 있는 문항</span>')
    text = replace_exact(text, '<b>0</b><span>독립 검토·공개 승인 완료</span>',
                         '<b id="answered-count">0</b><span>이 기기에서 푼 문항</span>')
    text = replace_exact(text, '위의 초안 확인란을 선택하면 문항을 열 수 있습니다.',
                         '문항을 불러오는 중입니다. 표시되지 않으면 새로고침해 주세요.')
    text = replace_exact(text,
        '이 파일은 GitHub에 배포된 페이지가 아닌 로컬 검토판입니다.',
        '온라인 연습용으로 공개된 학습판이며 독립 검토 완료 표시는 아닙니다.')
    text = replace_exact(text, "KEY='oddments.mpje.expansion.draft1'", "KEY='oddments.mpje.practice.v1'")
    text = replace_exact(text, "const s=localStorage.getItem(KEY);",
        "const s=localStorage.getItem(KEY)||localStorage.getItem('oddments.mpje.expansion.draft1');")
    text = replace_exact(text, "function persist(){try{", "function persist(){updateProgress();try{")
    text = replace_exact(text, "function prefs(){", "function updateProgress(){$('#answered-count').textContent=Object.keys(state.attempts).length.toLocaleString();}\nfunction prefs(){")
    text = replace_exact(text, "b.disabled=!$('#ack').checked||!!session;", "b.disabled=!!session;")
    text = replace_exact(text, "const disabled=!$('#ack').checked||!filtered.length||!!session;", "const disabled=!filtered.length||!!session;")
    text = replace_exact(text, "if(!$('#ack').checked)return;", '')
    text = replace_exact(text, "if(!$('#ack').checked||session)return;", "if(session)return;")
    text = replace_exact(text, "!session&&$('#ack').checked&&", "!session&&")
    lines = text.splitlines()
    gated = [line for line in lines if line.startswith("$('#ack').onchange=")]
    if len(gated) != 1:
        raise ValueError('Acknowledgement handler not found uniquely.')
    text = '\n'.join(line for line in lines if line not in gated) + '\n'
    text = replace_exact(text, "'Area '+q.area,'DRAFT'", "'Area '+q.area,'연습용 공개'")
    text = replace_exact(text, "t==='DRAFT'?' draft':''", "t==='연습용 공개'?' practice':''")
    text = text.replace('작성자 정답', '해설 기준 정답')
    text = replace_exact(text, 'mpje-expansion-draft-progress.json', 'mpje-online-practice-progress.json')
    text = replace_exact(text, '원본 패키지로 다시 열어 주세요.', '페이지를 새로고침해 주세요.')
    text = replace_exact(text, 'setInterval(updateClock,1000);catalog();',
        "setInterval(updateClock,1000);catalog();updateProgress();openQuestion(byId.get(location.hash.slice(1))||Q[0]);")
    text = replace_exact(text, "window.addEventListener('hashchange'", "$('#controls-link').onclick=e=>{e.preventDefault();$('#controls').scrollIntoView({behavior:'smooth'});$('#query').focus({preventScroll:true});};\nwindow.addEventListener('hashchange'")
    text = replace_exact(text, '</style></head>', '''
@media(max-width:820px){#reader{order:1}.panel{order:2}.topnav{gap:12px}.stats{margin:12px 0}.stat{padding:12px}.stat b{font-size:1.45rem}.notice{margin:12px 0;padding:10px 13px}}
#publication-info summary{cursor:pointer}#publication-info p{font-size:.87rem}#controls{scroll-margin-top:18px}
</style></head>''')
    if "$('#ack')" in text or 'id="ack"' in text or 'DRAFT' in text:
        raise ValueError('A draft access gate or label remains in the public template.')
    # Current edition additions are transformations of the immutable archived reader.
    count = data['published_question_count']
    text = text.replace('1,024문항 온라인', f'{count:,}문항 온라인')
    text = replace_exact(text, '<b>1,024</b>', f'<b>{count:,}</b>')
    text = replace_exact(text, '<b>256</b><span>공유 사례 묶음</span>', '<b>384</b><span>사례·조건 모델</span>')
    text = replace_exact(text, '<b>768 / 256</b>', '<b>1,560 / 616</b>')
    text = replace_exact(text,
        '256개 사례 묶음의 1,024개 연습 변형입니다.',
        '기존 1,024문항과 신규 1,152문항을 함께 제공합니다. 신규 묶음은 단일 사례 38개·업무 기록 판단 50개·복수선택 40개 모델을 각각 9개 조건으로 연습합니다. 1,152개의 서로 무관한 사례나 새로운 법규라는 뜻은 아닙니다.')
    text = replace_exact(text, '<label for="area">',
        '<label for="collection">문항 묶음</label><select id="collection"><option value="">전체 2,176문항</option><option value="plus-20261026">NEW · 사례형 1,152문항</option><option value="original-20261023">기존 1,024문항</option></select><label for="area">')
    text = replace_exact(text, "LETTERS='ABCD'", "LETTERS='ABCDE'")
    text = replace_exact(text, 'D.questions.length!==1024', 'D.questions.length!==D.published_question_count')
    # Validate backup answers against the actual question's choices (including new E).
    text = replace_exact(text, "a.selected.some(x=>!LETTERS.includes(x)||x.length!==1)",
        "a.selected.some(x=>typeof x!=='string'||!byId.get(id).choices.some(c=>c.id===x))")
    anchor="const Q=D.questions, byId=new Map(Q.map(q=>[q.question_id,q]));"
    text = replace_exact(text, anchor, anchor+"const initialBank=new URLSearchParams(location.search).get('bank');if(initialBank==='plus')$('#collection').value='plus-20261026';else if(initialBank==='original')$('#collection').value='original-20261023';")
    text = replace_exact(text, 'return Q.filter(q=>', "return Q.filter(q=>(!$('#collection').value||q.collection_id===$('#collection').value)&&")
    text = text.replace("['#query','#area','#qtype','#saved']", "['#query','#area','#qtype','#saved','#collection']")
    old=r"const parts=q.stem.split('\n\n');$('#cases').replaceChildren();for(const [i,p]of parts.slice(0,2).entries()){const d=el('div',undefined,'case');d.append(el('b',i?'CASE B':'CASE A'));const t=el('p',p.replace(/^Case [AB]: /,''));t.lang='en';d.append(t);$('#cases').append(d);}$('#lead').textContent=parts[2];"
    new=r"$('#cases').replaceChildren();if(q.scenario){const d=el('div',undefined,'case');d.append(el('b',q.practice_angle==='single-case'?'CASE':'WORK QUEUE'));const t=el('p',q.scenario);t.lang='en';d.append(t);$('#cases').append(d);$('#lead').textContent=q.lead_in;}else{const parts=q.stem.split('\n\n');for(const [i,p]of parts.slice(0,2).entries()){const d=el('div',undefined,'case');d.append(el('b',i?'CASE B':'CASE A'));const t=el('p',p.replace(/^Case [AB]: /,''));t.lang='en';d.append(t);$('#cases').append(d);}$('#lead').textContent=parts[2];}"
    text = replace_exact(text, old, new)
    text = replace_exact(text, '같은 family의 다른 문항은 이 두 사례와 판단을 공유합니다. 읽은 해설을 기억하는 효과와 새로운 사례의 판단 능력을 구분하세요.',
        '같은 family의 문항은 사례 또는 판단 모델을 공유합니다. 조건 연습의 반복 효과와 새로운 사례를 푸는 능력을 구분하세요.')
    text = replace_exact(text, "$('#boundary').textContent='독립 법규·현실성 검토 전. '+q.source_boundary;",
        "for(const e of q.additional_primary_evidence||[]){const li=el('li');li.append(link(e.url,e.title),el('small',' · 추가 원문 확인 '+e.accessed_at+' · '+e.scope));$('#sources').append(li);}$('#boundary').textContent='독립 법규·현실성 검토 전. '+q.source_boundary+' '+q.explanation.learning_boundary;")
    text = replace_exact(text, 'openQuestion(byId.get(location.hash.slice(1))||Q[0])',
        'openQuestion(byId.get(location.hash.slice(1))||filtered[0]||Q[0])')
    text = replace_exact(text, 'filtered:filtered.length,sessionIds:',
        "filtered:filtered.length,collection:$('#collection').value,total:Q.length,sessionIds:")
    text = replace_exact(text, '통합노트 ↗</a><a href="#controls"',
        '통합노트 ↗</a><a href="research.html">공개 샘플·작성 기준</a><a href="#controls"')
    text = replace_exact(text, '</head>', '<link rel="stylesheet" href="../assets/learning-tools.css" data-oddments-tools><script src="../assets/learning-tools.js" defer data-oddments-tools></script></head>')
    from practice_quality import transform
    text = transform(text,data)
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    return replace_exact(text, '__PAYLOAD__', payload)


def prepare(output: Path) -> dict:
    source = (ROOT / 'site').resolve()
    output = output.resolve()
    if output == source or source in output.parents or output in source.parents:
        raise ValueError('Use a separate output directory; tracked site sources are never rewritten.')
    shutil.copytree(source, output, dirs_exist_ok=True)
    data = build_payload()
    folder = output / 'practice-expansion'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'index.html').write_text(render(data), encoding='utf-8')
    manifest = {k: data[k] for k in ('edition','status','published_question_count','publication_date','independent_review_status','canonical_released_question_count','source_sha256','collections','additional_bank_sha256')}
    manifest['quality_selection'] = data['quality_selection']['stats']
    if data.get('representative_revision'):
        manifest['representative_revision'] = data['representative_revision']
    manifest['question_ids'] = [q['question_id'] for q in data['questions']]
    (folder / 'build.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    main = (output / 'index.html').read_text(encoding='utf-8')
    substitutions = {
        '1,024문항 · 검토 원고': '2,176문항 · 온라인 연습',
        '신규 연습문항 1,024개 · 독립 검토 대기': '온라인 연습 2,176문항 · 새 사례형 1,152개 추가',
        '원고·검토 상태 보기 →': '2,176문항 연습 시작 →',
        '기존 시험 모드에는 섞지 않았습니다. 별도 원고·로컬 검토판과 검토 상태를 확인하세요.':
        '다운로드 없이 문제를 풀고 한국어 해설을 확인하세요. 기존 독립 검토 문제은행과 별도인 공개 연습판입니다.'
    }
    for old, new in substitutions.items():
        main = replace_exact(main, old, new)
    main = replace_exact(main, '2,176문항 연습 시작 →</a>', '2,176문항 연습 시작 →</a><a class="notes-entry-link" href="practice-expansion/?bank=plus">NEW · 1,152문항만 풀기 →</a>')
    main = main.replace('2,176문항', f"{data['published_question_count']:,}문항")
    main = main.replace('NEW · 1,152문항만 풀기 →', '조건 변형 1,152문항 보기 →')
    main = main.replace('</a><a class="notes-entry-link" href="practice-expansion/?bank=plus">', '</a><a class="notes-entry-link" href="practice-expansion/?bank=quality">개별 작성·개정 96문항 →</a><a class="notes-entry-link" href="practice-expansion/?bank=plus">')
    if data.get('representative_revision'):
        number = len(data['representative_revision']['new_ids'])
        main = main.replace('<a class="notes-entry-link" href="practice-expansion/?bank=quality">', f'<a class="notes-entry-link" href="practice-expansion/?bank=rewrite">대표 재작성 {number}문항 →</a><a class="notes-entry-link" href="practice-expansion/?bank=quality">')
    (output / 'index.html').write_text(main, encoding='utf-8')
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'public-site')
    args = parser.parse_args()
    manifest = prepare(args.output)
    print(f"Published practice build: {manifest['published_question_count']} questions, {manifest['status']}; independent audit unchanged.")


if __name__ == '__main__':
    main()
