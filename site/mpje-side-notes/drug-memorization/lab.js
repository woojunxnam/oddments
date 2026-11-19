(()=>{'use strict';const DATA=window.MPJE_DRUG_LAB_DATA||[];const $=id=>document.getElementById(id);const key='mpje-drug-lab-v1';let saved={favorites:[],mastered:[]};try{const v=JSON.parse(localStorage.getItem(key)||'{}');saved.favorites=Array.isArray(v.favorites)?v.favorites:[];saved.mastered=Array.isArray(v.mastered)?v.mastered:[]}catch{}const fav=new Set(saved.favorites),mastered=new Set(saved.mastered);const save=()=>{try{localStorage.setItem(key,JSON.stringify({favorites:[...fav],mastered:[...mastered]}))}catch{}};const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const sched=s=>{if(/^II\b/.test(s))return'II';if(/^III\b/.test(s))return'III';if(/^IV\b/.test(s))return'IV';if(/^V\b/.test(s))return'V';if(/MA VI|Schedule VI|^VI\b|^Product-specific Rx;/.test(s))return'VI';return'Other'};const label=s=>{const v=sched(s);return v==='Other'?'Other / product-specific':'Schedule '+v};const categories=[...new Set(DATA.map(d=>d.category))].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));$('category').innerHTML='<option value="">All categories</option>'+categories.map(x=>'<option value="'+esc(x)+'">'+esc(x)+'</option>').join('');const schedules=['II','III','IV','V','VI','Other'];$('schedule').innerHTML='<option value="">All schedules</option>'+schedules.map(x=>'<option>'+x+'</option>').join('');let onlyFav=false,onlyNew=false,view='cards',filtered=DATA.slice(),deck=[],idx=0,revealed=false,quizIndex=0,quizScore=0,quizAnswered=false;function updateStats(){$('total').textContent=DATA.length;$('favoriteCount').textContent=fav.size;$('masteredCount').textContent=mastered.size;$('progress').style.width=(mastered.size/DATA.length*100)+'%';$('progressText').textContent=mastered.size+' / '+DATA.length+' marked learned'}function refresh(){const term=$('search').value.trim().toLowerCase(),cat=$('category').value,sc=$('schedule').value;filtered=DATA.filter(d=>(!cat||d.category===cat)&&(!sc||sched(d.schedule)===sc)&&(!onlyFav||fav.has(d.id))&&(!onlyNew||!mastered.has(d.id))&&(!term||[d.generic,d.brand,d.form,d.schedule,d.tip,d.category].join(' ').toLowerCase().includes(term)));$('resultCount').textContent=filtered.length+' matching drugs';const html=filtered.map(d=>'<article class="drug"><button class="fav" data-fav="'+esc(d.id)+'" aria-label="'+(fav.has(d.id)?'Remove from':'Add to')+' favorites" aria-pressed="'+fav.has(d.id)+'">'+(fav.has(d.id)?'★':'☆')+'</button><div class="small">'+esc(d.id)+' · '+esc(d.category)+' · '+(d.origin==='Chapter 26'?'Source directory':'New addition')+'</div><h3>'+esc(d.generic)+'</h3><div class="brand">'+esc(d.brand||'No brand listed')+'</div><span class="tag s'+sched(d.schedule).toLowerCase()+'">'+esc(label(d.schedule))+'</span><span class="tag">'+esc(d.form)+'</span><div class="small">'+esc(d.schedule)+'</div><div class="tip"><strong>MPJE memory point:</strong> '+esc(d.tip)+'</div><div class="links"><a target="_blank" rel="noopener noreferrer" href="https://dailymed.nlm.nih.gov/dailymed/search.cfm?query='+encodeURIComponent(d.generic)+'">DailyMed label search ↗</a>'+(d.origin==='Chapter 26'?'<a href="../drug-directory/#drug-'+esc(d.id.toLowerCase())+'">Chapter 26 source ↗</a>':'<span>Chapter 29 addition</span>')+'</div><label class="small"><input type="checkbox" data-learned="'+esc(d.id)+'" '+(mastered.has(d.id)?'checked':'')+'> Learned</label></article>').join('');$('catalog').innerHTML=html||'<div class="empty">No drugs match these filters. Clear filters to see all entries.</div>';document.querySelectorAll('[data-fav]').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.fav;fav.has(id)?fav.delete(id):fav.add(id);save();refresh();updateStats()}));document.querySelectorAll('[data-learned]').forEach(b=>b.addEventListener('change',()=>{b.checked?mastered.add(b.dataset.learned):mastered.delete(b.dataset.learned);save();updateStats()}));}function setToggle(id,value){$(id).setAttribute('aria-pressed',String(value))}['search','category','schedule'].forEach(id=>$(id).addEventListener(id==='search'?'input':'change',refresh));$('favoritesOnly').addEventListener('click',()=>{onlyFav=!onlyFav;setToggle('favoritesOnly',onlyFav);refresh()});$('unlearnedOnly').addEventListener('click',()=>{onlyNew=!onlyNew;setToggle('unlearnedOnly',onlyNew);refresh()});$('clearFilters').addEventListener('click',()=>{$('search').value='';$('category').value='';$('schedule').value='';onlyFav=false;onlyNew=false;setToggle('favoritesOnly',false);setToggle('unlearnedOnly',false);refresh()});function makeDeck(){const mode=$('deckMode').value;const pool=mode==='favorites'?DATA.filter(d=>fav.has(d.id)):mode==='unlearned'?DATA.filter(d=>!mastered.has(d.id)):mode==='filtered'?filtered:DATA;deck=pool.slice();for(let i=deck.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[deck[i],deck[j]]=[deck[j],deck[i]]}idx=0;revealed=false;renderFlash()}function renderFlash(){const d=deck[idx];$('flashCount').textContent=d?(idx+1)+' / '+deck.length:'No cards';$('flashcard').disabled=!d;$('flashPrev').disabled=idx===0;$('flashNext').disabled=idx>=deck.length-1;$('flashLearned').disabled=!d;$('flashcard').innerHTML=d?'<div class="small">'+($('direction').value==='generic'?'Name the brand(s)':'Name the generic')+' · '+esc(d.category)+'</div><div class="prompt">'+esc($('direction').value==='generic'?d.generic:d.brand||d.generic)+'</div>'+(revealed?'<div class="answer">'+esc($('direction').value==='generic'?d.brand||'No brand listed':d.generic)+'</div><div class="note">'+esc(d.schedule)+' · '+esc(d.tip)+'</div>':'<div class="note">Tap to reveal the answer and MPJE distinction</div>'): '<div class="empty">No cards in this deck. Choose All drugs or change your filters.</div>';if(d)$('flashLearned').textContent=mastered.has(d.id)?'Mark not learned':'Mark learned'}$('flashcard').addEventListener('click',()=>{revealed=!revealed;renderFlash()});$('flashNext').addEventListener('click',()=>{if(idx<deck.length-1){idx++;revealed=false;renderFlash()}});$('flashPrev').addEventListener('click',()=>{if(idx>0){idx--;revealed=false;renderFlash()}});$('flashShuffle').addEventListener('click',makeDeck);$('deckMode').addEventListener('change',makeDeck);$('direction').addEventListener('change',renderFlash);$('flashLearned').addEventListener('click',()=>{const d=deck[idx];if(!d)return;mastered.has(d.id)?mastered.delete(d.id):mastered.add(d.id);save();updateStats();renderFlash();refresh()});
const QUIZ_DETAILS=window.MPJE_DRUG_QUIZ_DETAILS||{};
function scheduleGuide(d){
  const s=d.schedule||'';
  if(/^II\b/.test(s))return {federal:'Schedule II (CII)',state:'Massachusetts Schedule II',rule:'Federal law prohibits Schedule II prescription refills (21 CFR 1306.12(a)). Narcotic vs nonnarcotic status can change the Massachusetts dispensing pathway.',url:'https://www.ecfr.gov/current/title-21/section-1306.12',cite:'21 CFR 1306.12(a)'};
  if(/^III\b/.test(s)||/^IV\b/.test(s)){const n=s.startsWith('III')?'III':'IV';return {federal:'Schedule '+n+' (C'+n+')',state:'Massachusetts Schedule '+n,rule:'Federal Schedule III/IV prescriptions: at most five authorized refills, and not more than six months after issue (21 CFR 1306.22(a)); state requirements still apply.',url:'https://www.ecfr.gov/current/title-21/section-1306.22',cite:'21 CFR 1306.22(a)'};}
  if(/^V\b/.test(s))return {federal:'Schedule V (CV), for the qualifying formulation',state:'Massachusetts Schedule V when applicable',rule:'Do not apply the federal Schedule III/IV five-refill/six-month cap automatically to Schedule V. Verify applicable Massachusetts rules, the prescription, and the exact formulation.',url:'https://www.deadiversion.usdoj.gov/GDP/%28DEA-DC-071%29%28EO-DEA226%29_Practitioner%27s_Manual_%28final%29.pdf',cite:'DEA Practitioner’s Manual: Schedule V refills'};
  if(s.startsWith('Federal exemption'))return {federal:'Possible federal exemption for exact listed preparations only',state:'Massachusetts status must be checked for the exact product',rule:'An exempt prescription product is not exempt simply because its ingredients match. Confirm the exact entry/NDC on the current DEA exempt-product list and verify state treatment.',url:'https://www.deadiversion.usdoj.gov/schedules/exempt/exempt_rx_list.pdf',cite:'DEA Exempt Prescription Products'};
  if(/OTC|Rx or OTC/.test(s))return {federal:'Not federally scheduled; OTC or Rx status varies by product',state:'An OTC product is not automatically Massachusetts Schedule VI; Rx versions generally fall under Schedule VI',rule:'Massachusetts Schedule VI applies to prescription drugs not in Schedules I–V (M.G.L. c.94C §3). OTC status, formulation and additional sales restrictions must be checked separately.',url:'https://www.mass.gov/info-details/learn-about-massachusetts-controlled-substances-registration-mcsr-for-practitioners',cite:'M.G.L. c.94C §3 (Mass.gov explanation)'};
  return {federal:'Not federally scheduled',state:'Massachusetts Schedule VI for the prescription product',rule:'Massachusetts Schedule VI includes prescription drugs outside Schedules I–V; it is not a federal DEA Schedule VI (M.G.L. c.94C §3).',url:'https://www.mass.gov/info-details/learn-about-massachusetts-controlled-substances-registration-mcsr-for-practitioners',cite:'M.G.L. c.94C §3 (Mass.gov explanation)'};
}
function quizAnswerHTML(d,yes){
  const info=QUIZ_DETAILS[d.id]||{};
  const law=scheduleGuide(d);
  const special={
    B001:['MA PMP reporting guidance','https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission'],
    B014:['FDA Mifepristone REMS','https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/information-about-mifepristone-medical-termination-pregnancy-through-ten-weeks-gestation'],
    B026:['FDA clozapine REMS removal','https://www.fda.gov/drugs/drug-safety-communications/fda-removes-risk-evaluation-and-mitigation-strategy-rems-program-antipsychotic-drug-clozapine'],
    B027:['FDA iPLEDGE update (November 2026)','https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/ipledge-risk-evaluation-and-mitigation-strategy-rems'],
    A076:['DEA exempt prescription product list','https://www.deadiversion.usdoj.gov/schedules/exempt/exempt_rx_list.pdf']
  };
  const refs=['<a target="_blank" rel="noopener noreferrer" href="https://dailymed.nlm.nih.gov/dailymed/search.cfm?query='+encodeURIComponent(d.generic)+'">DailyMed product labels</a>','<a target="_blank" rel="noopener noreferrer" href="'+esc(law.url)+'">'+esc(law.cite)+'</a>'];
  if(special[d.id])refs.push('<a target="_blank" rel="noopener noreferrer" href="'+esc(special[d.id][1])+'">'+esc(special[d.id][0])+'</a>');
  return '<div class="quiz-verdict '+(yes?'is-correct':'is-incorrect')+'">'+(yes?'Correct answer.':'Not quite. Review the correct match:')+'</div>'
    +'<h4 class="quiz-answer-title">'+esc(d.generic)+' <span aria-hidden="true">↔</span> '+esc(d.brand)+'</h4>'
    +'<dl class="quiz-answer-grid">'
    +'<div><dt>Common uses</dt><dd>'+esc(info.uses||'Consult the exact product label for indications.')+'</dd></div>'
    +'<div><dt>Drug class</dt><dd>'+esc(info.drugClass||d.category)+'</dd></div>'
    +'<div><dt>Dosage form</dt><dd>'+esc(d.form)+'</dd></div>'
    +'<div><dt>Federal schedule</dt><dd>'+esc(law.federal)+'</dd></div>'
    +'<div><dt>Massachusetts schedule</dt><dd>'+esc(law.state)+'</dd></div>'
    +'</dl>'
    +'<p class="quiz-law"><strong>MPJE legal rule:</strong> '+esc(law.rule)+'</p>'
    +'<p class="quiz-trap"><strong>Product-specific exam trap:</strong> '+esc(d.tip)+'</p>'
    +(info.examExtra?'<p class="quiz-extra"><strong>Remember:</strong> '+esc(info.examExtra)+'</p>':'')
    +'<div class="quiz-answer-sources"><strong>Official references:</strong> '+refs.join(' · ')+'</div>'
    +'<p class="quiz-qualifier">These are common uses and exam memory points, not exhaustive FDA indications or a substitute for checking the exact formulation, NDC, current labeling and state law.</p>';
}

let quizPool=[],quizBatch=[],quizCursor=0,current=null;
const QUIZ_SET_SIZE=10;
function shuffleQuiz(items){
  for(let i=items.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    [items[i],items[j]]=[items[j],items[i]];
  }
}
function beginQuiz(){
  const filter=$('quizSchedule').value;
  quizPool=DATA.filter(d=>d.brand&&d.brand.trim()&&(!filter||sched(d.schedule)===filter));
  shuffleQuiz(quizPool);
  quizCursor=0;
  nextQuizBatch();
}
function nextQuizBatch(){
  quizBatch=[];
  const target=Math.min(QUIZ_SET_SIZE,quizPool.length);
  const usedHere=new Set();
  while(quizBatch.length<target){
    if(quizCursor>=quizPool.length){
      shuffleQuiz(quizPool);
      // Finish an exhausted schedule before recycling. Keep current-set IDs
      // at the tail of the fresh rotation, so no question repeats within a set.
      quizPool=[...quizPool.filter(d=>!usedHere.has(d.id)),...quizPool.filter(d=>usedHere.has(d.id))];
      quizCursor=0;
    }
    const item=quizPool[quizCursor++];
    if(!usedHere.has(item.id)){
      usedHere.add(item.id);
      quizBatch.push(item);
    }
  }
  quizIndex=0;
  quizScore=0;
  const filter=$('quizSchedule').value;
  const scope=!filter?'All schedules':filter==='Other'?'Other / OTC / exempt':'Schedule '+filter;
  $('quizScopeInfo').textContent=scope+' · '+quizPool.length+' eligible drug/formulation entries · '+quizBatch.length+' questions this set'
    +(quizPool.length>quizBatch.length?' · Next questions uses new entries before repeating.':'.');
  $('quizNextSet').disabled=!quizPool.length;
  renderQuiz();
}
function renderQuiz(){
  quizAnswered=false;
  current=quizBatch[quizIndex]||null;
  const total=quizBatch.length;
  $('quizNext').disabled=true;
  $('quizProgress').textContent=current?'Question '+(quizIndex+1)+' of '+total+' · '+quizScore+' correct':'';
  if(!current){
    $('quizPrompt').textContent=total?'Quiz complete — '+quizScore+' / '+total+' correct':'No matching drugs available for this filter.';
    $('quizChoices').innerHTML='';
    $('quizFeedback').textContent=total?'Choose Next questions for another set or Start new quiz to reshuffle.':'Choose another schedule to continue.';
    return;
  }
  const reverse=$('quizDirection').value==='brand';
  const correct=reverse?current.generic:current.brand;
  const related=quizPool.filter(d=>d.id!==current.id&&sched(d.schedule)===sched(current.schedule));
  let distractors=[...new Set(related.map(d=>reverse?d.generic:d.brand).filter(Boolean))].filter(v=>v!==correct);
  if(distractors.length<3){
    const more=DATA.filter(d=>d.id!==current.id).map(d=>reverse?d.generic:d.brand).filter(Boolean);
    distractors=[...new Set([...distractors,...more])].filter(v=>v!==correct);
  }
  shuffleQuiz(distractors);
  const options=[correct,...distractors.slice(0,3)];
  shuffleQuiz(options);
  $('quizPrompt').textContent=reverse?'Which generic matches '+current.brand+'?':'Which brand matches '+current.generic+'?';
  $('quizChoices').innerHTML=options.map((v,i)=>'<button class="choice" data-choice="'+i+'">'+String.fromCharCode(65+i)+'. '+esc(v)+'</button>').join('');
  $('quizFeedback').textContent='Select one answer.';
  document.querySelectorAll('[data-choice]').forEach((b,i)=>b.addEventListener('click',()=>{
    if(quizAnswered)return;
    quizAnswered=true;
    const yes=options[i]===correct;
    if(yes)quizScore++;
    document.querySelectorAll('[data-choice]').forEach((x,j)=>{
      x.disabled=true;
      if(options[j]===correct)x.classList.add('correct');
      else if(j===i)x.classList.add('wrong');
    });
    $('quizFeedback').innerHTML=quizAnswerHTML(current,yes);
    $('quizNext').disabled=false;
    $('quizProgress').textContent='Question '+(quizIndex+1)+' of '+total+' · '+quizScore+' correct';
  }));
}
$('quizNext').addEventListener('click',()=>{quizIndex++;renderQuiz()});$('quizRestart').addEventListener('click',beginQuiz);$('quizNextSet').addEventListener('click',nextQuizBatch);$('quizDirection').addEventListener('change',beginQuiz);$('quizSchedule').addEventListener('change',beginQuiz);$('exportProgress').addEventListener('click',()=>{const payload=JSON.stringify({favorites:[...fav],mastered:[...mastered]},null,2);const blob=new Blob([payload],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='mpje-drug-lab-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)});$('resetProgress').addEventListener('click',()=>{if(!confirm('Clear saved favorites and learned marks on this device?'))return;fav.clear();mastered.clear();save();updateStats();refresh();makeDeck()});updateStats();refresh();makeDeck();beginQuiz();})();