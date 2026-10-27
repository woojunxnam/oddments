/* Global, route-preserving navigation. No progress storage or question-bank access. */
(() => {
  'use strict';
  const script=document.currentScript;
  if(!script||document.getElementById('oddments-tools'))return;
  const root=script.src?new URL('../',script.src):new URL('./',document.baseURI);
  const nav=document.createElement('nav');nav.id='oddments-tools';nav.className='om-tools';nav.setAttribute('aria-label','페이지 이동 도구');
  const menu=document.createElement('div');menu.id='om-tools-menu';menu.className='om-tools-menu';
  const top=document.createElement('button');top.type='button';top.id='om-to-top';top.textContent='↑ 맨 위';top.setAttribute('aria-label','현재 페이지 맨 위로 이동');
  top.addEventListener('click',()=>{
    // Never assign location.hash: it encodes notes routes and active question IDs.
    window.scrollTo({top:0,left:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
    const target=document.querySelector('header h1, h1, .brand');
    if(target){const old=target.getAttribute('tabindex');target.setAttribute('tabindex','-1');target.focus({preventScroll:true});if(old===null)target.addEventListener('blur',()=>target.removeAttribute('tabindex'),{once:true});}
  });
  function link(path,text,id){const a=document.createElement('a');a.href=new URL(path,root).href;a.textContent=text;a.id=id;return a;}
  menu.append(top,link('./','⌂ 홈','om-home'),link('notes/#refresh','복습 카드','om-cards'));
  const toggle=document.createElement('button');toggle.type='button';toggle.id='om-tools-toggle';toggle.textContent='이동';toggle.setAttribute('aria-controls',menu.id);toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','맨 위·홈·복습 카드 이동 메뉴');
  const media=matchMedia('(max-width: 760px)');let expanded=false;
  function update(){menu.hidden=media.matches&&!expanded;toggle.hidden=!media.matches;toggle.setAttribute('aria-expanded',String(expanded));}
  toggle.addEventListener('click',()=>{expanded=!expanded;update();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&expanded){expanded=false;update();toggle.focus();}});
  document.addEventListener('click',e=>{if(expanded&&!nav.contains(e.target)){expanded=false;update();}});
  media.addEventListener?.('change',update);
  nav.append(menu,toggle);document.body.append(nav);update();
})();
