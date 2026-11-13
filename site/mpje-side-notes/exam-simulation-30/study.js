/* Chapter 30 original exam-style practice. No secure exam items. */
(() => {
  'use strict';
  const all = Array.isArray(window.MPJE_CH30_QUESTIONS) ? window.MPJE_CH30_QUESTIONS : [];
  const letters = ['A','B','C','D'];
  const key = 'mpje-side-notes-ch30-v1';
  const sets = [...new Set(all.map(q => q.set))].sort((a,b) => a-b);
  const $ = id => document.getElementById(id);
  const node = (tag,cls,txt) => {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (txt !== undefined) el.textContent = txt;
    return el;
  };
  let state = {set:1, answers:{}, submitted:{}};
  try {
    const raw = JSON.parse(localStorage.getItem(key) || '{}');
    if (raw && typeof raw === 'object' && raw.answers && raw.submitted) {
      state = {set:sets.includes(Number(raw.set)) ? Number(raw.set) : 1, answers:raw.answers, submitted:raw.submitted};
    }
  } catch(_) { /* Storage is optional. */ }
  const requestedSet = Number(new URLSearchParams(window.location.search).get('set'));
  if (sets.includes(requestedSet)) state.set = requestedSet;
  function save() { try { localStorage.setItem(key, JSON.stringify(state)); } catch(_) {} }
  function getAnswer(q) {
    const value = state.answers[q.id] || [];
    return Array.isArray(value) ? value.filter(x => letters.includes(x)) : [];
  }
  function isComplete(q) {return getAnswer(q).length > 0;}
  function isRight(q) {
    const a = [...getAnswer(q)].sort().join(',');
    const b = [...q.correct].sort().join(',');
    return a === b;
  }
  function switchSet(set) {state.set = set; save(); const url = new URL(window.location.href); url.searchParams.set('set', String(set)); window.history.replaceState(null, '', url); render(); $('set-heading').focus();}
  function renderTabs() {
    const root = $('set-tabs'); root.replaceChildren();
    sets.forEach(s => {
      const b = node('button', 'exam-tab'+(s===state.set?' is-active':''),'Set '+s+' · 5 questions');
      b.type='button';
      b.setAttribute('aria-pressed',String(s===state.set));
      const n = all.filter(q => q.set===s).filter(isComplete).length;
      const note = node('small','exam-tab-status',state.submitted[s]?'Scored':'Answered '+n+'/5');
      b.append(note);
      b.addEventListener('click',()=>switchSet(s));
      root.append(b);
    });
  }
  function renderQuestions() {
    const root=$('question-grid'); root.replaceChildren();
    const qs=all.filter(q => q.set===state.set);
    const revealed=!!state.submitted[state.set];
    $('set-heading').textContent = 'Practice Set '+state.set;
    $('set-desc').textContent = revealed
      ? 'Set submitted. Review every option and its legal reference, or retake this set.'
      : 'Select an answer for each question. Answers and explanations remain hidden until you submit this entire set.';
    qs.forEach((q,index)=>{
      const card=node('article','exam-question');
      const head=node('div','exam-question-head');
      head.append(node('span','exam-number','QUESTION '+String(index+1).padStart(2,'0')+' / 05'));
      head.append(node('span','exam-kind',q.kind==='multi'?'SELECT ALL THAT APPLY':'SINGLE BEST ANSWER'));
      card.append(head);
      card.append(node('div','exam-topic',q.topic));
      card.append(node('h3','exam-stem',q.stem));
      const choices=node('fieldset','exam-choices');
      const legend=node('legend','sr-only','Answer choices for '+q.id);
      choices.append(legend);
      q.choices.forEach((choice,i)=>{
        const letter=letters[i];
        const label=node('label','exam-choice');
        const input=node('input','exam-choice-input');
        input.type=q.kind==='multi'?'checkbox':'radio';
        input.name=q.id;
        input.value=letter;
        input.checked=getAnswer(q).includes(letter);
        input.disabled=revealed;
        const badge=node('span','exam-letter',letter);
        const t=node('span','exam-choice-text',choice.text);
        label.append(input,badge,t);
        if(revealed){
          if(q.correct.includes(letter))label.classList.add('is-correct');
          else if(input.checked)label.classList.add('is-wrong');
        }
        input.addEventListener('change',()=>{
          const a=new Set(getAnswer(q));
          if(q.kind==='single'){state.answers[q.id]=[letter];}
          else {if(input.checked)a.add(letter);else a.delete(letter);state.answers[q.id]=[...a];}
          save();
          const qs = all.filter(item => item.set === state.set);
          const answered = qs.filter(isComplete).length;
          $('set-progress').textContent = answered + '/' + qs.length + ' answered';
          $('submit-set').disabled = answered !== qs.length;
          renderTabs();
        });
        choices.append(label);
      });
      card.append(choices);
      if(revealed) {
        const yes=isRight(q);
        const result=node('div','exam-feedback '+(yes?'exam-right':'exam-wrong'),
          (yes?'Correct. ':'Review needed. ')+'Correct answer'+(q.correct.length>1?'s':'')+': '+q.correct.join(', ')+'.');
        const explanations=node('div','exam-explanations');
        q.choices.forEach((choice,i)=>{
          const letter=letters[i];
          const p=node('p','',letter+' — '+choice.why);
          if(q.correct.includes(letter))p.classList.add('is-keyed');
          explanations.append(p);
        });
        const reference=node('p','exam-reference');
        reference.append(node('strong','',q.citation+' · '));
        const link=node('a','', 'Official legal source');
        link.href=q.url; link.target='_blank';link.rel='noopener noreferrer';
        reference.append(link);
        if(q.note)explanations.append(node('p','exam-editor-note','Editorial note: '+q.note));
        card.append(result,explanations,reference);
      }
      root.append(card);
    });
    const answered=qs.filter(isComplete).length;
    $('set-progress').textContent=revealed ? 'Submitted · '+qs.filter(isRight).length+'/5 correct' : answered+'/5 answered';
    $('submit-set').disabled=revealed || answered!==qs.length;
    $('submit-set').hidden=revealed;
    $('retake-set').hidden=!revealed;
    $('score-announcement').hidden=!revealed;
    if(revealed) $('score-announcement').textContent='You scored '+qs.filter(isRight).length+' out of 5. SATA earns a point only when every correct answer and no extra answer is selected.';
    $('prev-set').disabled=state.set===sets[0];
    $('next-set').disabled=state.set===sets[sets.length-1];
  }
  function render(){
    renderTabs();
    renderQuestions();
  }
  $('submit-set').addEventListener('click',()=>{
    const qs=all.filter(q => q.set===state.set);
    if(!qs.every(isComplete))return;
    state.submitted[state.set]=true;
    save();render();
    $('score-announcement').focus();
  });
  $('retake-set').addEventListener('click',()=>{
    all.filter(q=>q.set===state.set).forEach(q=>delete state.answers[q.id]);
    delete state.submitted[state.set];
    save();render();
    $('set-heading').focus();
  });
  $('prev-set').addEventListener('click',()=>switchSet(Math.max(sets[0],state.set-1)));
  $('next-set').addEventListener('click',()=>switchSet(Math.min(sets[sets.length-1],state.set+1)));
  if(!all.length || all.length % 5 !== 0 || sets.length !== all.length / 5
    || sets.some(set => {
      const qs = all.filter(q => q.set === set);
      return qs.length !== 5 || qs.filter(q => q.kind === 'single').length !== 3
        || qs.filter(q => q.kind === 'multi').length !== 2
        || qs.some(q => !q.id || !q.url || q.choices.length !== 4
          || !Array.isArray(q.correct) || !q.correct.length);
    })) {
    $('set-desc').textContent='Question data could not be validated. Please report this to the maintainer.';
    return;
  }
  render();
})();