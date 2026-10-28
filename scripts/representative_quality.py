"""Reader integration for immutable old/new question versions and explicit holds."""
from html import escape
from practice_quality import once


def transform(text, data):
    revision = data['representative_revision']
    stats = revision['stats']
    count, default = len(revision['new_ids']), stats['recommended']
    text = once(text, '<option value="quality-20261027">',
        f'<option value="representative-20261028">대표 재작성 {count}문항</option><option value="quality-20261027">')
    text = once(text, "else if(initialBank==='quality')$('#collection').value='quality-20261027';if(initialBank&&initialBank!=='quality')$('#scope').value='all';",
        "else if(initialBank==='quality')$('#collection').value='quality-20261027';else if(initialBank==='rewrite')$('#collection').value='representative-20261028';if(initialBank&&!['quality','rewrite'].includes(initialBank))$('#scope').value='all';")
    text = once(text,
        "filtered.sort((a,b)=>Number(b.collection_id==='quality-20261027')-Number(a.collection_id==='quality-20261027'));",
        "filtered.sort((a,b)=>revisionRank(b)-revisionRank(a));")
    anchor = 'const QC=window.MPJEQuality,recommendedIds=new Set(D.quality_selection.recommended_ids);'
    replacement = anchor + "const revisionLinks=new Map(D.representative_revision.replacements.map(r=>[r.legacy_question_id,r])),heldVersions=new Map(D.representative_revision.holds.flatMap(h=>[h.legacy_question_id,...(h.affected_archive_ids||[])].map(id=>[id,h])));const revisionRank=q=>q.collection_id==='representative-20261028'?2:q.collection_id==='quality-20261027'?1:0;"
    text = once(text, anchor, replacement)
    old_description = f'기본 목록은 {default}문항입니다. 기존 2,176문항을 삭제하지 않고 대표 355개와 개별 작성 96개를 우선합니다. 보기 순서는 매번 바뀌지만 원래 답안 ID로 채점합니다.'
    description = (f'기본 목록은 {default}문항입니다. 기존 대표 355개 중 {count}개를 새 사례로 다시 작성하고, '
        f'{stats["replaced_by_existing_quality"]}개는 이미 있는 개별 사례로 통합했습니다. '
        f'{stats["held_from_default"]}개는 검토 보류로 기본 목록에서 제외했습니다. '
        '기존 2,272개와 그 풀이 기록은 보존되며, 개정 사례는 별도 기록으로 학습합니다. '
        '기존 대표 전체의 법규 재검증이 완료됐다는 뜻은 아닙니다.')
    text = once(text, old_description, description)
    text = once(text, '전수 구조 검사·수정 범위', '전체 편집 감사·실제 재작성 범위')
    text = once(text, '기존 family별 대표에서 같은 문제 문장·보기 세트를 줄였습니다. 의미상 중복이나 법적 정확성의 전수 검증은 아닙니다. 북마크·오답·ID 검색은 제외된 변형도 찾습니다.',
        '개별 재작성 사례와 기존 대표를 우선합니다. 검토 보류·이전 판본은 전체 목록, 북마크, ID 검색으로 확인할 수 있습니다. 전체 법규 감사 완료 표시는 아닙니다.')
    text = once(text, '<div id="q-meta" class="meta"></div>', '<div id="q-meta" class="meta"></div><div id="revision-notice" class="notice tiny" hidden></div>')
    functions = r'''function revisionNotice(q){const box=$('#revision-notice');box.replaceChildren();const next=revisionLinks.get(q.question_id),held=heldVersions.get(q.question_id);if(q.revision_of){box.append(el('span','대표 사례 개정판 · 이전 판본과 풀이 기록은 별도로 보존됩니다. '));const a=el('a','이전 문항 보기');a.href='#'+q.revision_of;if(!session)box.append(a);else box.append(el('span','이전 문항은 세트를 마친 뒤 열람할 수 있습니다.'));}else if(next){box.append(el('span','기록이 보존된 이전 문항입니다. '));const a=el('a','개정 사례 보기');a.href='#'+next.replacement_question_id;if(!session)box.append(a);else box.append(el('span','개정 사례는 세트를 마친 뒤 열람할 수 있습니다.'));}else if(held){box.append(el('strong','검토 보류 · 기본 연습에서 제외'));box.append(el('p','이전 문항과 답안은 기록 보존을 위해 열람할 수 있습니다. 아래 기존 채점 결과를 확정된 법규 판단으로 사용하지 마세요.'));const d=el('details'),s=el('summary','보류 이유');d.append(s,el('p',held.reason));box.append(d);}box.hidden=!box.childNodes.length;}
'''
    text = once(text, 'function openQuestion(q){', functions + 'function openQuestion(q){')
    text = once(text, 'active=q;checked=false;', 'active=q;checked=false;revisionNotice(q);')
    text = once(text, "row.append(el('span',q.explanation.choice_analysis[c.id]));",
        "row.append(el('span',q.explanation.choice_analysis[c.id]));for(const ref of q.explanation.choice_authorities?.[c.id]||[]){const authority=D.sources[ref.source_id];row.append(link(authority.url,ref.exact_section+' · 확인 '+authority.checked_at));}")
    text = once(text, '아래는 관련 노트 절의 참고문헌입니다. 각 선택지의 정확한 조항을 독립적으로 확인한 문항별 검증 기록은 아닙니다.',
        '아래는 연결 노트와 공식 근거입니다. 개정 사례는 각 선택지 아래에 작성자가 대조한 정확한 조항·확인일을 표시합니다. 독립 법규 감사 완료 표시는 아닙니다.')
    text = once(text, 'sessionMode:session?.mode||null,', 'revisionOf:active?.revision_of||null,heldForReview:heldVersions.has(active?.question_id),sessionMode:session?.mode||null,')
    return text
