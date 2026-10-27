/* Pure sampling and occurrence-scoring contracts. No content or answer mutation. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.MPJEQuality=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
function random(){if(typeof crypto!=='undefined'&&crypto.getRandomValues){const a=new Uint32Array(1);crypto.getRandomValues(a);return a[0]/4294967296;}return Math.random();}
function value(rng){const n=rng();if(!Number.isFinite(n)||n<0||n>=1)throw new Error('RNG must return [0,1).');return n;}
function shuffle(input,rng=random){const a=[...input];for(let i=a.length-1;i>0;i--){const j=Math.floor(value(rng)*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
function chaos(pool,count=10,rng=random){if(!Array.isArray(pool)||!pool.length||!Number.isInteger(count)||count<0)throw new Error('Invalid sampling pool/count.');return Array.from({length:count},()=>pool[Math.floor(value(rng)*pool.length)]);}
function norm(t){return t.toLocaleLowerCase().replace(/[^\p{L}\p{N}_]+/gu,' ').trim();}
function pack(q){return q.choices.map(c=>norm(c.text)).sort().join('\u001f');}
function diverse(pool,count,attempts={},rng=random){const f=new Set(),stems=new Set(),packs=new Set(),out=[];const candidates=shuffle(pool,rng);candidates.sort((a,b)=>Number(!!attempts[a.question_id])-Number(!!attempts[b.question_id]));for(const q of candidates){const s=norm(q.stem),p=pack(q);if(f.has(q.family_id)||stems.has(s)||packs.has(p))continue;f.add(q.family_id);stems.add(s);packs.add(p);out.push(q);if(out.length===count)break;}return out;}
function answer(q,selected){const ids=new Set(q.choices.map(c=>c.id));if(!Array.isArray(selected)||!selected.length||new Set(selected).size!==selected.length||selected.some(x=>!ids.has(x)))throw new Error('Invalid answer.');const got=[...selected].sort(),want=[...q.correct_choice_ids].sort();return JSON.stringify(got)===JSON.stringify(want);}
function record(session,q,selected,order){const slot=session.pos;if(session.ids[slot]!==q.question_id)throw new Error('Occurrence mismatch.');if(Object.prototype.hasOwnProperty.call(session.answers,slot))throw new Error('Occurrence already submitted.');const result={slot,question_id:q.question_id,selected:[...selected],correct:answer(q,selected),display_order:[...order]};session.answers[slot]=result;return result;}
function responses(session){return Object.values(session.answers).sort((a,b)=>a.slot-b.slot);}
return {random,shuffle,chaos,diverse,norm,pack,answer,record,responses};
});
