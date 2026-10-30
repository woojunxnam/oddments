"""Quality reader overlay: immutable archive + explicit representative pool and new cases."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def attach(data, revision_selection=None):
 selection=json.loads((ROOT/'practice_expansion/2026-10-27-quality/selection.json').read_text())
 available={q['question_id'] for q in data['questions']}
 if not set(selection['recommended_ids'])<=available:raise ValueError('Unknown recommended ID')
 data['quality_selection']={k:selection[k] for k in ['edition','recommended_ids','new_ids','stats']}
 if revision_selection:
  path=(ROOT/revision_selection['path']).resolve()
  if ROOT not in path.parents:raise ValueError('Revision selection path escapes repository')
  raw=path.read_bytes()
  if hashlib.sha256(raw).hexdigest()!=revision_selection['sha256']:raise ValueError('Revision selection hash changed')
  revised=json.loads(raw)
  baseline=(ROOT/'practice_expansion/2026-10-27-quality/selection.json').read_bytes()
  if hashlib.sha256(baseline).hexdigest()!=revised['baseline_selection_sha256']:raise ValueError('Revision baseline selection changed')
  if not set(revised['recommended_ids'])<=available:raise ValueError('Unknown revision recommendation')
  if len(set(revised['recommended_ids']))!=len(revised['recommended_ids']):raise ValueError('Duplicate revision recommendation')
  if revised['stats']['available_total']!=len(available):raise ValueError('Revision corpus count mismatch')
  for r in revised['replacements']:
   if r['legacy_question_id'] not in available or r['replacement_question_id'] not in available:raise ValueError('Invalid revision link')
  if not set(selection['new_ids'])<=set(revised['recommended_ids']):raise ValueError('Previous96 must remain in the default pool')
  data['representative_revision']={k:revised[k] for k in ['edition','replacements','holds','stats','new_ids','history_policy']}
  notices=revised.get('archive_review_notices',[])
  noticed=[]
  for notice in notices:
   ids=notice.get('question_ids',[])
   if not ids or not set(ids)<=available or not isinstance(notice.get('reason'),str) or not notice['reason'].strip():raise ValueError('Invalid archive review notice')
   noticed.extend(ids)
  if len(noticed)!=len(set(noticed)):raise ValueError('Duplicate archive review notice ID')
  data['representative_revision']['archive_review_notices']=notices
  data['quality_selection'].update(edition=revised['edition'],recommended_ids=revised['recommended_ids'],stats=revised['stats'])
 data['generation_method']=f"Original 256 paired families and128 conditional models and previous96 individual cases are retained. {len(data['quality_selection']['recommended_ids'])} default cases after explicit revision/hold mappings; all{len(available)} archived and new IDs remain available. This is not independent legal or psychometric validation."
 return data

def once(text,old,new):
 if text.count(old)!=1:raise ValueError(f'Quality template drift: {old[:90]} ({text.count(old)})')
 return text.replace(old,new,1)
def line(text,prefix,new):
 lines=text.splitlines();indices=[i for i,x in enumerate(lines) if x.startswith(prefix)]
 if len(indices)!=1:raise ValueError(f'Expected one line: {prefix}')
 lines[indices[0]]=new;return '\n'.join(lines)+'\n'

def transform(text,data):
 total=data['published_question_count'];recommended=len(data['quality_selection']['recommended_ids'])
 text=text.replace('전체 2,176문항',f'전체 {total:,}문항')
 text=once(text,'<b>384</b><span>사례·조건 모델</span>',f'<b>{recommended}</b><span>중복 축소 기본 목록</span>')
 text=once(text,'<b>1,560 / 616</b>',f"<b>{data['stats']['types']['SBA']:,} / {data['stats']['types']['SATA']:,}</b>")
 text=once(text,'<label for="collection">','<label for="scope">학습 범위</label><select id="scope"><option value="recommended">대표·개정 우선 (451문항)</option><option value="all">모든 변형 포함 (2,272문항)</option></select><p class="tiny">기존 family별 대표에서 같은 문제 문장·보기 세트를 줄였습니다. 의미상 중복이나 법적 정확성의 전수 검증은 아닙니다. 북마크·오답·ID 검색은 제외된 변형도 찾습니다.</p><label for="collection">')
 text=once(text,'<option value="plus-20261026">','<option value="quality-20261027">개별 작성·개정 사례 96문항</option><option value="plus-20261026">')
 text=once(text,'<button id="timed"','<button id="chaos" class="primary">완전 랜덤 10문항</button><p class="tiny" id="chaos-help">전체 2,272문항에서 매번 독립 추첨합니다. 현재 필터·비율·family 제한 없이, 같은 문항도 다시 나올 수 있습니다.</p><button id="timed"')
 text=once(text,'120문항 · 150분','최대 120문항 · 150분')
 text=once(text,'<details class="notice" id="publication-info">','<details class="notice" id="quality-info"><summary><strong>반복 축소·개별 사례 개정판</strong></summary><p>기본 목록은 451문항입니다. 기존 2,176문항을 삭제하지 않고 대표 355개와 개별 작성 96개를 우선합니다. 보기 순서는 매번 바뀌지만 원래 답안 ID로 채점합니다.</p><a href="quality-review.html">전수 구조 검사·수정 범위</a></details><details class="notice" id="publication-info">')
 # Original sibling variants remain stored, while redesigned items receive separate IDs.
 text=once(text,'const Q=D.questions, byId=new Map(Q.map(q=>[q.question_id,q]));','const Q=D.questions, byId=new Map(Q.map(q=>[q.question_id,q]));const QC=window.MPJEQuality,recommendedIds=new Set(D.quality_selection.recommended_ids);')
 text=once(text,"else if(initialBank==='original')$('#collection').value='original-20261023';", "else if(initialBank==='original')$('#collection').value='original-20261023';else if(initialBank==='quality')$('#collection').value='quality-20261027';if(initialBank&&initialBank!=='quality')$('#scope').value='all';")
 text=once(text,'session=null,reviewQueue=null;', 'session=null,reviewQueue=null;let reviewPosition=0,displayOrder=[],displayLabels={};')
 text=once(text,"return Q.filter(q=>", "return Q.filter(q=>($('#scope').value==='all'||recommendedIds.has(q.question_id)||!!s||query.startsWith('ma-'))&&")
 text=once(text,'filtered=matches();',"filtered=matches();filtered.sort((a,b)=>Number(b.collection_id==='quality-20261027')-Number(a.collection_id==='quality-20261027'));")
 text=once(text,"const b=el('button',q.topic);","const b=el('button',q.question_id+' · 법규 적용');")
 # Add the scope control to all enable/disable/event paths and keep Chaos global.
 text=text.replace("['#query','#area','#qtype','#saved','#collection']", "['#query','#area','#qtype','#saved','#collection','#scope']")
 text=once(text,"$('#timed').disabled=disabled;", "$('#timed').disabled=disabled;$('#chaos').disabled=!!session;")
 text=line(text,'function renderSession()',r'''function renderSession(){const n=$('#session-status');n.replaceChildren();if(!session){n.textContent=reviewQueue?`제출 회차 검토 ${reviewPosition+1}/${reviewQueue.length}`:'자율 보기 · 대표 목록과 모든 변형을 구분해서 학습하세요.';return;}n.append(el('span',`세트 ${session.pos+1}/${session.ids.length} · ${session.mode==='chaos'?'완전 랜덤·중복 허용':'family당 최대 1문항'} · `));const c=el('span','');c.id='clock';n.append(c);const bar=el('div',undefined,'bar'),fill=el('div');fill.style.width=(Object.keys(session.answers).length/session.ids.length*100)+'%';bar.append(fill);n.append(bar);updateClock();}''')
 text=once(text,"$('#q-title').textContent=q.topic;","$('#q-title').textContent='법규 적용 사례';")
 text=once(text,"$('#feedback').hidden=false;","$('#feedback').hidden=false;$('#q-title').textContent=q.topic;")
 text=once(text,"active=q;checked=false;", "active=q;checked=false;displayOrder=QC.shuffle(q.choices).map(c=>c.id);displayLabels=Object.fromEntries(displayOrder.map((id,i)=>[id,LETTERS[i]]));")
 text=text.replace("q.practice_angle==='single-case'?'CASE':'WORK QUEUE'", "q.practice_angle==='queue-selection'?'WORK QUEUE':'CASE'")
 text=once(text,'for(const c of q.choices){const l=', 'for(const id of displayOrder){const c=q.choices.find(c=>c.id===id);const l=')
 text=once(text,"el('span',c.id,'letter')", "el('span',displayLabels[c.id],'letter')")
 # Explanations show the same displayed letter AND text, not stale source-letter shorthand.
 text=once(text,"q.correct_choice_ids.join(', ')", "q.correct_choice_ids.map(id=>displayLabels[id]).sort().join(', ')")
 text=once(text,"for(const c of q.choices){const row=", "for(const id of displayOrder){const c=q.choices.find(c=>c.id===id);const row=")
 text=once(text,"c.id+' · '+(q.correct_choice_ids.includes(c.id)", "displayLabels[c.id]+' · '+c.text+' · '+(q.correct_choice_ids.includes(c.id)")
 text=once(text,"if(session)session.answers[active.question_id]={correct,selected};", "if(session)QC.record(session,active,selected,displayOrder);")
 text=line(text,"$('#next').onclick=",r'''$('#next').onclick=()=>{if(session){if(!checked)return;if(session.pos+1>=session.ids.length){endSession('세트가 완료되었습니다.');return;}session.pos++;openQuestion(byId.get(session.ids[session.pos]));}else if(reviewQueue?.length){reviewPosition=(reviewPosition+1)%reviewQueue.length;openReview(reviewQueue[reviewPosition]);}else{const pool=filtered.length?filtered:Q;const i=pool.findIndex(x=>x.question_id===active?.question_id);openQuestion(pool[(i+1)%pool.length]);}};''')
 text=line(text,'function openReview(',r'''function openReview(entry){const id=typeof entry==='string'?entry:entry.question_id;openQuestion(byId.get(id));const a=typeof entry==='string'?state.attempts[id]:entry;if(!a)return;for(const n of $('#choices').querySelectorAll('input')){n.checked=a.selected.includes(n.value);n.disabled=true;}checked=true;$('#check').disabled=true;showFeedback(active,a.selected,a.correct);renderSession();}''')
 text=line(text,'function startSession(',r'''function startSession(count,timed,mode='standard'){if(session)return;reviewQueue=null;reviewPosition=0;const chosen=mode==='chaos'?QC.chaos(Q,count):QC.diverse(matches(),count,state.attempts);if(!chosen.length)return;session={ids:chosen.map(q=>q.question_id),pos:0,answers:{},timed,mode,deadline:timed?Date.now()+150*60*1000:null};$('#end-session').hidden=false;['#query','#area','#qtype','#saved','#collection','#scope'].forEach(s=>$(s).disabled=true);openQuestion(chosen[0]);}''')
 text=line(text,'function endSession(',r'''function endSession(message){if(!session)return;const s=session;session=null;$('#end-session').hidden=true;['#query','#area','#qtype','#saved','#collection','#scope'].forEach(x=>$(x).disabled=false);const answers=QC.responses(s),correct=answers.filter(a=>a.correct).length;const box=$('#summary');box.hidden=false;box.className='summary';box.replaceChildren(el('h3',message),el('p',`${s.ids.length}회 출제 중 ${answers.length}회 제출 · 정답 ${correct}회 · 미응답 ${s.ids.length-answers.length}회`),el('p',`서로 다른 문항 ${new Set(s.ids).size}개 · family ${new Set(s.ids.map(id=>byId.get(id).family_id)).size}개. 같은 문항이 다시 나오면 출제 회차별로 따로 채점·검토합니다.`),el('p','단순 연습 기록입니다. 공식 점수·합격률·실제 시험 난도와 같다는 뜻은 아닙니다. 반복 출제는 새 법규를 익혔다는 증거가 아닙니다.'));const b=el('button','제출 답안과 해설 검토');b.type='button';b.id='review-submitted';b.disabled=!answers.length;b.onclick=()=>{reviewQueue=answers;reviewPosition=0;openReview(reviewQueue[0]);};box.append(b);$('#question').hidden=true;renderSession();catalog();}''')
 text=once(text,"$('#practice').onclick=()=>startSession(20,false);", "$('#chaos').onclick=()=>startSession(10,false,'chaos');$('#practice').onclick=()=>startSession(20,false);")
 text=once(text,'sessionIds:session?.ids||[]', "sessionMode:session?.mode||null,sessionAnswers:session?QC.responses(session):[],displayOrder:[...displayOrder],displayLabels:{...displayLabels},reviewPosition,reviewSelected:reviewQueue?.[reviewPosition]?.selected||null,sessionIds:session?.ids||[]")
 core=(ROOT/'site/practice-expansion/quality-core.js').read_text()
 text=once(text,'</head>', '<script>'+core+'</script></head>')
 text=text.replace('451문항',f'{recommended}문항').replace('2,272문항',f'{total:,}문항')
 if data.get('representative_revision'):
  from representative_quality import transform as transform_revisions
  text=transform_revisions(text,data)
 return text
