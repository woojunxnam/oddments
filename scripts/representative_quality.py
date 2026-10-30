"""Reader integration for immutable old/new question versions and explicit holds."""
from html import escape
from practice_quality import line, once


def connect_notes(text, data):
    """Link exact note evidence to a reversible filter, using existing study records."""
    panel = '''<section id="note-context" class="note-context" hidden aria-labelledby="note-context-title">
<p class="tiny">통합노트에서 이어서 연습</p><h2 id="note-context-title"></h2>
<p id="note-context-counts" class="tiny"></p>
<div class="note-context-actions"><a id="note-return" href="../notes/">이 절 다시 읽기 →</a>
<button type="button" id="note-wrong">이 절 오답만 보기</button><button type="button" id="note-clear">노트 연결 해제</button></div>
<p id="note-context-help" class="tiny">아래 검색·포함 범위·모음과 함께 적용합니다. 완전 랜덤은 전체 문항에서 출제합니다.</p>
</section>'''
    text = once(text, '<aside id="controls" class="panel">', '<aside id="controls" class="panel">' + panel)
    text = once(text, '</style>', '''
.note-context{margin-bottom:18px;padding:14px;border:1px solid var(--line);border-radius:9px;background:var(--pale)}
.note-context h2{margin:5px 0;font-size:1rem;overflow-wrap:anywhere}.note-context p{margin:6px 0}
.note-context-actions{display:flex;flex-wrap:wrap;gap:8px;align-items:center}.note-context-actions button,.note-context-actions a{font-size:.85rem;white-space:normal}
</style>''')
    anchor = 'const revisionRank=q=>q.collection_id'
    # Place the filter state after the immutable question payload, before startup.
    text = once(text, anchor,
        "const noteParams=new URLSearchParams(location.search);let selectedNoteId=noteParams.get('note')||'';"
        "if(selectedNoteId&&noteParams.get('scope')==='all')$('#scope').value='all';"
        "if(selectedNoteId&&noteParams.get('review')==='wrong')$('#saved').value='wrong';" + anchor)
    text = once(text, 'return{query,saved,scope,collection,archiveReason,includeArchive:',
        'return{query,saved,scope,collection,note:selectedNoteId,archiveReason,includeArchive:')
    text = once(text,
        "function inSelectedPool(q,c){return(!c.collection||q.collection_id===c.collection)&&",
        "function inSelectedPool(q,c){return(!c.note||(q.note_evidence||[]).some(e=>e.unit_id===c.note))&&(!c.collection||q.collection_id===c.collection)&&")
    functions = r'''function updateNoteContext(){const box=$('#note-context'),note=D.note_practice_index?.[selectedNoteId];box.hidden=!selectedNoteId;if(!selectedNoteId)return;$('#note-context-title').textContent=note?note.title:'연결된 노트 절을 찾을 수 없습니다';$('#note-context-counts').textContent=note?`이 절의 대표·개정 ${note.recommended.toLocaleString()}문항 · 모든 변형 ${note.total.toLocaleString()}문항. 연결 수는 독립 법규 검증 수가 아닙니다.`:'연결된 목록은 비어 있습니다. 주소의 노트 ID를 확인하거나 노트 연결을 해제해 주세요.';const outside=active&&!(active.note_evidence||[]).some(e=>e.unit_id===selectedNoteId);$('#note-context-help').textContent=(outside?'현재 열린 문항은 이 절의 연결 문항이 아닙니다. 목록·연습 세트에는 이 절 필터가 계속 적용됩니다. ':'아래 검색·포함 범위·모음과 함께 적용합니다. ')+(session?'세트 중 노트는 새 탭에서 열리며 시간 연습의 시계는 계속 갑니다. ':'')+'완전 랜덤은 전체 문항에서 출제합니다.';$('#note-return').hidden=!note;if(note)$('#note-return').href=note.note_url;$('#note-return').target=session?'_blank':'_self';$('#note-return').rel='noopener noreferrer';$('#note-wrong').disabled=!!session||!note;$('#note-clear').disabled=!!session;}
function openFilteredQuestion(){const q=filtered[0];reviewQueue=null;if(q)openQuestion(q);else{$('#question').hidden=true;$('#locked').hidden=false;$('#locked').textContent='현재 조건에 맞는 문항이 없습니다. 이 절에 남은 오답이 없거나 다른 필터가 적용되어 있을 수 있습니다. 검색·복습 조건을 조정해 주세요.';}}
'''
    text = once(text, 'function filterContext(){', functions + 'function filterContext(){')
    text = once(text, 'revisionRank(a));updateFilterSummary();',
        'revisionRank(a));updateFilterSummary();updateNoteContext();')
    # A filter remains stable while a practice/exam set is in progress.
    text = text.replace("'#collection','#scope'].forEach", "'#collection','#scope','#note-wrong','#note-clear'].forEach")
    text = once(text, 'const pool=filtered.length?filtered:Q;',
        'const pool=filtered.length?filtered:(selectedNoteId?[]:Q);if(!pool.length){openFilteredQuestion();return;}')
    # The event-registration list has two action buttons with dedicated handlers.
    text = text.replace("for(const s of ['#query','#area','#qtype','#saved','#collection','#scope','#note-wrong','#note-clear'])",
        "for(const s of ['#query','#area','#qtype','#saved','#collection','#scope'])")
    handlers = r'''$('#note-wrong').onclick=()=>{if(session)return;$('#saved').value='wrong';page=0;catalog();openFilteredQuestion();};
$('#note-clear').onclick=()=>{if(session)return;selectedNoteId='';const url=new URL(location.href);url.searchParams.delete('note');url.searchParams.delete('review');try{history.replaceState(null,'',url);}catch{}page=0;catalog();openFilteredQuestion();};
'''
    text = once(text, "$('#controls-link').onclick=", handlers + "$('#controls-link').onclick=")
    text = once(text, "openQuestion(byId.get(location.hash.slice(1))||filtered[0]||Q[0]);",
        "const initialQuestion=byId.get(location.hash.slice(1))||filtered[0]||(!selectedNoteId?Q[0]:null);if(initialQuestion)openQuestion(initialQuestion);else openFilteredQuestion();")
    text = once(text, 'filterSummary:filterSummaryData(),scope:',
        'filterSummary:filterSummaryData(),noteUnit:selectedNoteId||null,scope:')
    text = once(text, "${c.includeArchive?'모든 변형':'대표·개정 대상'} ${number(info.scopeCount)}개를 포함하고,",
        "${c.note?'이 절에 연결된 ':''}${c.includeArchive?'모든 변형':'대표·개정 대상'} ${number(info.scopeCount)}개를 포함하고,")
    return text


def clarify_filters(text, data):
    """Describe the intersection, including the existing archive-lookup exceptions."""
    total = len(data['questions'])
    recommended = len(data['quality_selection']['recommended_ids'])
    scope_start = text.index('<label for="scope">')
    scope_end = text.index('</select>', scope_start) + len('</select>')
    text = once(text, text[scope_start:scope_end],
        '<label for="scope">문항 포함 범위</label>'
        '<select id="scope" aria-describedby="scope-help">'
        f'<option value="recommended">대표·개정 우선 ({recommended:,}개)</option>'
        f'<option value="all">모든 변형 포함 ({total:,}개)</option></select>')
    text = once(text,
        '<p class="tiny">개별 재작성 사례와 기존 대표를 우선합니다. 검토 보류·이전 판본은 전체 목록, 북마크, ID 검색으로 확인할 수 있습니다. 전체 법규 감사 완료 표시는 아닙니다.</p>',
        '<p class="tiny" id="scope-help">대표·개정 우선은 반복 변형과 이전 판본을 줄인 기본 목록입니다. '
        '모든 변형에는 이전 판본·검토 보류 문항도 포함됩니다. 북마크·오답·ID 검색에서는 기록 보존을 위해 제외된 문항도 찾습니다.</p>')

    # Collection counts describe storage, not the result after the scope filter.
    names = {
        'representative-20261028': '대표 재작성',
        'quality-20261027': '개별 작성·개정 사례',
        'plus-20261026': '사례형 조건 연습',
        'original-20261023': '기존 변형 연습',
    }
    options = [f'<option value="" data-name="모든 모음">모든 모음 (총 {total:,}개)</option>']
    for collection in reversed(data['collections']):
        identifier = collection['id']
        name = names.get(identifier, collection['title'])
        count = sum(q['collection_id'] == identifier for q in data['questions'])
        options.append(f'<option value="{escape(identifier, quote=True)}" '
            f'data-name="{escape(name, quote=True)}">{escape(name)} (모음 총 {count:,}개)</option>')
    collection_start = text.index('<label for="collection">')
    collection_end = text.index('</select>', collection_start) + len('</select>')
    text = once(text, text[collection_start:collection_end],
        '<label for="collection">문항 모음 (선택)</label>'
        '<select id="collection" aria-describedby="collection-help">' + ''.join(options) + '</select>'
        '<p class="tiny" id="collection-help">모음의 숫자는 보관된 전체 문항 수입니다. '
        '선택한 모음에도 위 포함 범위를 함께 적용합니다.</p>')

    feedback = '''<section id="filter-feedback" class="filter-feedback" aria-labelledby="filter-summary-title">
<h3 id="filter-summary-title">현재 연습 대상</h3>
<p id="filter-summary" role="status" aria-live="polite" aria-atomic="true"></p>
<p id="filter-breakdown" class="tiny"></p><p id="filter-exception" class="tiny" hidden></p>
<p id="filter-session-help" class="tiny"></p>
<details id="filter-examples" class="tiny"><summary>두 선택의 조합 예시</summary><p id="filter-example-text"></p></details>
</section>'''
    text = once(text, '<div class="stack"><button id="practice"', feedback + '<div class="stack"><button id="practice"')
    text = once(text, '<button id="practice" class="primary"', '<button id="practice" aria-describedby="filter-session-help" class="primary"')
    text = once(text, '<button id="timed"', '<button id="timed" aria-describedby="filter-session-help"')
    text = once(text, '<button id="chaos" class="primary"', '<button id="chaos" aria-describedby="chaos-help" class="primary"')
    # Only the count next to the controls is announced; pagination remains visible.
    text = once(text, '<p id="result-count" class="status" aria-live="polite">', '<p id="result-count" class="status">')
    text = once(text, '</style>', '''
.filter-feedback{margin:14px 0;padding:12px;border:1px solid var(--line);border-radius:9px;background:var(--pale)}
#filter-summary-title{font-size:.85rem;margin:0}#filter-summary{font-size:.95rem;font-weight:700;margin:5px 0}
.filter-feedback p{margin:6px 0}.filter-feedback summary{cursor:pointer}#filter-examples{margin-top:8px}
</style>''')

    functions = r'''function filterContext(){const query=$('#query').value.trim().toLocaleLowerCase(),saved=$('#saved').value,scope=$('#scope').value,collection=$('#collection').value;const archiveReason=saved?(saved==='wrong'?'오답 복습':'북마크 복습'):(query.startsWith('ma-')?'ID 검색':'');return{query,saved,scope,collection,archiveReason,includeArchive:scope==='all'||!!archiveReason};}
function inSelectedPool(q,c){return(!c.collection||q.collection_id===c.collection)&&(c.includeArchive||recommendedIds.has(q.question_id));}
function filterSummaryData(){const c=filterContext(),collectionQuestions=Q.filter(q=>!c.collection||q.collection_id===c.collection),scopeCount=collectionQuestions.filter(q=>inSelectedPool(q,c)).length,familyCount=new Set(filtered.map(q=>q.family_id)).size;return{collectionTotal:collectionQuestions.length,scopeCount,matchedCount:filtered.length,familyCount,standardCeiling:Math.min(20,familyCount),timedCeiling:Math.min(120,familyCount),archiveReason:c.scope==='recommended'?c.archiveReason:'',collection:c.collection,scope:c.scope};}
function updateFilterSummary(){const c=filterContext(),info=filterSummaryData(),number=n=>n.toLocaleString(),name=$('#collection').selectedOptions[0].dataset.name;$('#filter-summary').textContent=`현재 조건에 맞는 ${number(info.matchedCount)}문항`;$('#filter-breakdown').textContent=`${name}의 전체 ${number(info.collectionTotal)}개 중 ${c.includeArchive?'모든 변형':'대표·개정 대상'} ${number(info.scopeCount)}개를 포함하고, 검색·영역·유형·복습 조건을 모두 적용했습니다.`;$('#filter-exception').hidden=!info.archiveReason;$('#filter-exception').textContent=info.archiveReason?`${info.archiveReason}에서는 이전 판본·검토 보류·변형도 찾습니다. 선택한 모음과 나머지 필터는 계속 적용됩니다.`:'';$('#filter-session-help').textContent=info.matchedCount?`일반 연습 최대 ${info.standardCeiling}문항 · 시간 연습 최대 ${info.timedCeiling}문항. 같은 사례·지문·보기의 반복을 제외하므로 실제 세트는 더 짧을 수 있습니다.`:'조건에 맞는 문항이 없습니다. 검색어나 필터를 조정해 주세요. 완전 랜덤 10문항은 전체 모음에서 시작할 수 있습니다.';const exampleId=c.collection||D.collections.find(group=>Q.some(q=>q.collection_id===group.id&&!recommendedIds.has(q.question_id)))?.id||D.collections[0]?.id;const option=Array.from($('#collection').options).find(o=>o.value===exampleId),example=Q.filter(q=>q.collection_id===exampleId),exampleRecommended=example.filter(q=>recommendedIds.has(q.question_id)).length;$('#filter-example-text').textContent=option?`다른 필터를 사용하지 않을 때, ‘대표·개정 우선 + ${option.dataset.name}’은 ${number(exampleRecommended)}문항, ‘모든 변형 + ${option.dataset.name}’은 ${number(example.length)}문항입니다.`:'';}
'''
    text = once(text, 'function matches(){', functions + 'function matches(){')
    text = line(text, 'function matches()', r'''function matches(){const c=filterContext(),area=$('#area').value,t=$('#qtype').value;return Q.filter(q=>inSelectedPool(q,c)&&(!c.query||searchIndex.get(q.question_id).includes(c.query))&&(!area||String(q.area)===area)&&(!t||q.question_type===t)&&(!c.saved||(c.saved==='wrong'?state.attempts[q.question_id]?.correct===false:state.bookmarks.includes(q.question_id))));}''')
    text = once(text, 'filtered.sort((a,b)=>revisionRank(b)-revisionRank(a));',
        'filtered.sort((a,b)=>revisionRank(b)-revisionRank(a));updateFilterSummary();')
    text = once(text, 'filtered:filtered.length,collection:',
        "filtered:filtered.length,filteredIds:filtered.map(q=>q.question_id),filterSummary:filterSummaryData(),scope:$('#scope').value,collection:")
    return text


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
    replacement = anchor + "const revisionLinks=new Map(D.representative_revision.replacements.map(r=>[r.legacy_question_id,r])),heldVersions=new Map(D.representative_revision.holds.flatMap(h=>[h.legacy_question_id,...(h.affected_archive_ids||[])].map(id=>[id,h]))),archiveReviewNotices=new Map((D.representative_revision.archive_review_notices||[]).flatMap(n=>n.question_ids.map(id=>[id,n])));const revisionRank=q=>q.collection_id==='representative-20261028'?2:q.collection_id==='quality-20261027'?1:0;"
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
    text = once(text, "box.hidden=!box.childNodes.length;}",
        "const warning=archiveReviewNotices.get(q.question_id);if(warning){const section=el('div',undefined,'archive-review-warning');section.append(el('strong','이전 판본 · 법규 검토 주의'),el('p',warning.reason));box.append(section);}box.hidden=!box.childNodes.length;}")
    text = once(text, 'active=q;checked=false;', 'active=q;checked=false;revisionNotice(q);')
    text = once(text, "row.append(el('span',q.explanation.choice_analysis[c.id]));",
        "row.append(el('span',q.explanation.choice_analysis[c.id]));for(const ref of q.explanation.choice_authorities?.[c.id]||[]){const authority=D.sources[ref.source_id];row.append(link(authority.url,ref.exact_section+' · 확인 '+authority.checked_at));}")
    text = once(text, '아래는 관련 노트 절의 참고문헌입니다. 각 선택지의 정확한 조항을 독립적으로 확인한 문항별 검증 기록은 아닙니다.',
        '아래는 연결 노트와 공식 근거입니다. 개정 사례는 각 선택지 아래에 작성자가 대조한 정확한 조항·확인일을 표시합니다. 독립 법규 감사 완료 표시는 아닙니다.')
    text = once(text, 'sessionMode:session?.mode||null,', 'revisionOf:active?.revision_of||null,heldForReview:heldVersions.has(active?.question_id),archiveReviewWarning:archiveReviewNotices.has(active?.question_id),sessionMode:session?.mode||null,')
    return connect_notes(clarify_filters(text, data), data)
