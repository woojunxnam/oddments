/* Pure deterministic helpers shared by browser and Node regression tests. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.MPJE_REFRESH_CORE = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const KEY = 'oddments.mpje.refresh.v1';
  const datePattern = /^\d{4}-\d{2}-\d{2}$/;
  const own = (o,k) => Object.prototype.hasOwnProperty.call(o,k);
  function dayKey(now = new Date()) {
    const parts = new Intl.DateTimeFormat('en-US', {timeZone:'America/New_York', year:'numeric', month:'2-digit', day:'2-digit'}).formatToParts(now);
    const get = type => parts.find(p=>p.type===type).value;
    return `${get('year')}-${get('month')}-${get('day')}`;
  }
  function validDay(day) {
    if (typeof day !== 'string' || !datePattern.test(day)) return false;
    const time=Date.parse(day+'T12:00:00Z');
    return Number.isFinite(time) && new Date(time).toISOString().slice(0,10)===day;
  }
  function addDays(day, count) {
    if (!validDay(day) || !Number.isInteger(count)) throw new Error('Invalid calendar day');
    const date = new Date(day+'T12:00:00Z');date.setUTCDate(date.getUTCDate()+count);
    return date.toISOString().slice(0,10);
  }
  function hash(text) {let h=2166136261;for(const c of text){h^=c.codePointAt(0);h=Math.imul(h,16777619);}return h>>>0;}
  function shuffled(items, seed) {
    let state=hash(String(seed))||1;const random=()=>{state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)/4294967296;};
    const out=[...items];for(let i=out.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[out[i],out[j]]=[out[j],out[i]];}return out;
  }
  function cleanState(value, ids, fieldIds, strict = false) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('잘못된 기록 형식입니다.');
    if (strict && (value.application !== 'oddments-refresh' || value.version!==1)) throw new Error('복습 카드 기록 파일이 아닙니다.');
    const idset=new Set(ids),fieldset=new Set(fieldIds);
    const pick=(key,set)=>Array.isArray(value[key])?[...new Set(value[key].filter(v=>typeof v==='string'&&set.has(v)))].slice(0,set.size):[];
    const reviews=Object.create(null);
    const raw=value.reviews;
    if(raw && typeof raw==='object' && !Array.isArray(raw)) for(const id of ids) {
      if(!own(raw,id))continue;const r=raw[id];
      if(r&&typeof r==='object'&&['again','hard','good'].includes(r.grade)&&validDay(r.due)&&validDay(r.last)&&Number.isInteger(r.count)&&r.count>=1&&r.count<=100000){
        reviews[id]={grade:r.grade,due:r.due,last:r.last,count:r.count};
      } else if(strict)throw new Error('잘못된 복습 일정이 있습니다.');
    }
    const daily= value.daily&&validDay(value.daily.date)&&Array.isArray(value.daily.ids)?
      {date:value.daily.date,ids:[...new Set(value.daily.ids.filter(id=>idset.has(id)))].slice(0,10),completed:[...new Set((Array.isArray(value.daily.completed)?value.daily.completed:[]).filter(id=>idset.has(id)&&value.daily.ids.includes(id)))].slice(0,10)}:null;
    return {version:1,saved:pick('saved',idset),field:pick('field',fieldset),reviews,daily,
      recall:!!value.recall, font:Number.isFinite(value.font)?Math.min(24,Math.max(16,value.font)):18,
      last:typeof value.last==='string'&&idset.has(value.last)?value.last:null};
  }
  function gradeReview(previous,grade,day) {
    if(!['again','hard','good'].includes(grade))throw new Error('Unknown grade');
    return {grade,due:addDays(day,{again:1,hard:3,good:7}[grade]),last:day,count:Math.min(100000,(previous?.count||0)+1)};
  }
  function dailyCards(cards, reviews, day) {
    const eligible=cards.filter(c=>c.deck==='core'&&!c.flags.some(f=>['open','date-sensitive','source-gap'].includes(f)));
    const tie=c=>hash(day+':'+c.id);
    const due=eligible.filter(c=>reviews[c.id]&&reviews[c.id].due<=day).sort((a,b)=>reviews[a.id].due.localeCompare(reviews[b.id].due)||tie(a)-tie(b));
    const out=due.slice(0,3);const picked=new Set(out.map(c=>c.id));
    // Prioritize new material, then oldest reviews; add one per stage before filling.
    const rest=eligible.filter(c=>!picked.has(c.id)).sort((a,b)=>Number(!!reviews[a.id])-Number(!!reviews[b.id])||(reviews[a.id]?.last||'').localeCompare(reviews[b.id]?.last||'')||tie(a)-tie(b));
    const represented=new Set(out.map(c=>c.stage));
    for(const c of rest)if(out.length<10&&!represented.has(c.stage)){out.push(c);picked.add(c.id);represented.add(c.stage);}
    for(const c of rest)if(out.length<10&&!picked.has(c.id)){out.push(c);picked.add(c.id);}
    return out.map(c=>c.id);
  }
  function mergeState(current,incoming) {
    const reviews={...current.reviews};
    for(const [id,r] of Object.entries(incoming.reviews))if(!reviews[id]||r.last>reviews[id].last||(r.last===reviews[id].last&&r.count>reviews[id].count))reviews[id]=r;
    return {...current,reviews,saved:[...new Set([...current.saved,...incoming.saved])],field:[...new Set([...current.field,...incoming.field])],last:current.last||incoming.last};
  }
  return {KEY,dayKey,validDay,addDays,hash,shuffled,cleanState,gradeReview,dailyCards,mergeState};
});
