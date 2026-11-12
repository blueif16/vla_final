// Usage: node cdp-check-emphasis.mjs <page url> <width>   (Chrome with --headless=new --remote-debugging-port=9334)
// Checks a chapter page: glossary terms, Chinese labels, the widgets it has (skipped when absent), every
// multiple-choice option by click and by keyboard, margin notes (inside the viewport, no collision with wide
// blocks), the emphasis budget, console errors and horizontal overflow. Written for chapter 2, 2026-11-12.
const [,, url, width] = process.argv;
const W = +width || 1440;
const list = await (await fetch('http://127.0.0.1:9334/json/new?' + encodeURIComponent('about:blank'), { method: 'PUT' })).json();
const ws = new WebSocket(list.webSocketDebuggerUrl);
let id = 0; const pending = new Map(); const logs = [];
ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d); pending.delete(d.id); } else if (d.method === 'Runtime.consoleAPICalled') logs.push(d.params.type + ': ' + d.params.args.map((a) => a.value).join(' ')); else if (d.method === 'Runtime.exceptionThrown') logs.push('EXCEPTION: ' + d.params.exceptionDetails.text + ' ' + (d.params.exceptionDetails.exception?.description || '')); };
await new Promise((r) => ws.onopen = r);
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true }); if (r.result.exceptionDetails) return 'EVAL ERROR ' + JSON.stringify(r.result.exceptionDetails.exception?.description || r.result.exceptionDetails.text); return r.result.result.value; };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
await send('Runtime.enable');
await send('Network.enable');
await send('Network.setCacheDisabled', { cacheDisabled: true });
await send('Emulation.setDeviceMetricsOverride', { width: W, height: 900, deviceScaleFactor: 1, mobile: W < 500 });
await send('Page.navigate', { url });
await sleep(3000);
const out = (k, v) => console.log(k.padEnd(14), typeof v === 'string' ? v : JSON.stringify(v));

out('width', W);
out('terms', await ev(`(() => { const ks=[...document.querySelectorAll('[data-term]')].map(b=>b.dataset.term); const miss=ks.filter(k=>!window.GLOSSARY[k]); return ks.length+' used, '+new Set(ks).size+' distinct, missing: '+JSON.stringify(miss); })()`));
out('zh', await ev(`(() => { const z=[...document.querySelectorAll('.term-zh')]; const off=z.filter(p=>{ const a=p.querySelector('.term').getBoundingClientRect(), b=p.querySelector('.zh').getClientRects()[0]; return !(b && b.top < a.bottom && b.bottom > a.top); }).map(p=>p.querySelector('.term').dataset.term); return z.length+' Chinese labels, off their term line: '+JSON.stringify(off); })()`));
out('popover', await ev(`(() => { const b=document.querySelector('.term'); if(!b) return 'no terms'; b.click(); const p=document.getElementById('term-pop'); const r=(p.hidden?'HIDDEN ':'shown ')+p.textContent.slice(0,60); document.body.click(); return r; })()`));
out('episode', await ev(`(() => { const w=document.querySelector('[data-widget=episode]'); if(!w) return 'none'; const a=w.querySelector('.ep-label').textContent; w.querySelector('.ep-next').click(); const b=w.querySelector('.ep-label').textContent; w.querySelector('.ep-prev').click(); return a+' -> '+b; })()`));
out('scrolly', await ev(`(async () => { const st=[...document.querySelectorAll('.scrolly .step')]; if(st.length<7) return 'none'; document.documentElement.style.scrollBehavior='auto'; st[6].scrollIntoView({block:'center', behavior:'instant'}); window.dispatchEvent(new Event('scroll')); await new Promise(r=>setTimeout(r,500)); const on=document.querySelector('.scrolly .step.is-on .label')?.textContent; const ctrl=document.querySelector('.stage-ctrl'); return 'on: '+on+' | slider shown: '+!ctrl.hidden+' | '+document.querySelector('.stage-ctrl .readout').textContent; })()`));
out('modes', await ev(`(() => { const w=document.querySelector('[data-widget=modes]'); if(!w) return 'none'; return [...w.querySelectorAll('.seg button')].map(b=>{ b.click(); const vis=[...w.querySelectorAll('.mode-note')].filter(n=>n.style.display!=='none').map(n=>n.dataset.show); return b.dataset.mode+'->'+vis.join(','); }).join(' | '); })()`));
out('annotate', await ev(`(() => { const k=document.querySelector('[data-widget=annotate] .k[data-part]'); if(!k) return 'none'; k.dispatchEvent(new Event('mouseenter')); const t=document.querySelector('.annot-out').textContent.slice(0,50); const hot=document.querySelectorAll('.spec .row.hot').length; k.dispatchEvent(new Event('mouseleave')); return hot+' rows lit: '+t; })()`));
out('yt', await ev(`(() => { const b=document.querySelector('.yt-play'); if(!b) return 'none'; b.click(); const f=document.querySelector('[data-yt] iframe'); return f ? f.src.replace(/^.*embed\\//,'') : 'no iframe'; })()`));

// multiple choice: every option by click
const mcq = await ev(`(async () => {
  const qs=[...document.querySelectorAll('.mcq')]; const rows=[];
  for (const [qi,q] of qs.entries()) {
    const opts=[...q.querySelectorAll('.mcq-opt')];
    const rights=opts.filter(o=>o.classList.contains('right')).length;
    const res=[];
    for (const [oi,o] of opts.entries()) {
      o.querySelector('summary').click(); await new Promise(r=>setTimeout(r,60));
      const fb=o.querySelector(':scope > p'); const shown=o.open && fb && fb.offsetHeight>0;
      const others=opts.filter(x=>x!==o && x.open).length;
      const word=(fb?.textContent||'').split(/[ .,]/)[0];
      const ok= shown && others===0 && ((word==='Right') === o.classList.contains('right'));
      res.push(String.fromCharCode(65+oi)+(o.classList.contains('right')?'*':'')+(ok?' ok':' FAIL('+word+',shown='+shown+',others='+others+')'));
    }
    rows.push((qi+1)+'. '+res.join(' ')+' | right options: '+rights+' | first: '+q.dataset.first+' "'+(q.querySelector('.mcq-first')?.textContent||'').slice(0,40)+'"');
    opts.forEach(o=>o.open=false);
  }
  return rows;
})()`);
(Array.isArray(mcq) && mcq.length ? mcq : ['none']).forEach((r) => out('mcq', r));

// keyboard: Tab focus to the first option of the last question and press Enter, then Space on the next
const kb = await ev(`(() => { const s=document.querySelector('.mcq:last-of-type .mcq-opt summary'); if(!s) return 'no mcq'; s.scrollIntoView({block:'center'}); s.focus(); return document.activeElement===s; })()`);
if (kb !== true) out('keyboard', String(kb)); else {
await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13, text: '\r' });
await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
await sleep(150);
const kb1 = await ev(`document.querySelector('.mcq:last-of-type .mcq-opt').open`);
await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 });
await sleep(100);
const focusedNext = await ev(`(() => { const a=document.activeElement; const all=[...document.querySelectorAll('.mcq:last-of-type .mcq-opt summary')]; return all.indexOf(a); })()`);
await send('Input.dispatchKeyEvent', { type: 'keyDown', key: ' ', code: 'Space', windowsVirtualKeyCode: 32, text: ' ' });
await send('Input.dispatchKeyEvent', { type: 'keyUp', key: ' ', code: 'Space', windowsVirtualKeyCode: 32 });
await sleep(150);
const kb2 = await ev(`[...document.querySelectorAll('.mcq:last-of-type .mcq-opt')].map(o=>o.open?1:0).join('')`);
out('keyboard', `focused: ${kb} | Enter opens A: ${kb1} | Tab moves to option index ${focusedNext} | Space -> open states ${kb2}`);
}

// margin notes
out('side notes', await ev(`(() => {
  const wide=[...document.querySelectorAll('.fig, .scrolly, .callcard, .timeline, .rail, .chapter-nav, .scrolly-cap')].map(e=>e.getBoundingClientRect());
  const abs=(r)=>({l:r.left, r:r.right, t:r.top+scrollY, b:r.bottom+scrollY});
  const W=document.documentElement.clientWidth;
  return [...document.querySelectorAll('.side')].map((s,i)=>{
    const r=abs(s.getBoundingClientRect()); const pos=getComputedStyle(s).position;
    const hits=wide.map(abs).filter(w=>w.l<r.r && w.r>r.l && w.t<r.b && w.b>r.t).length;
    const host=abs(s.parentElement.getBoundingClientRect());
    return i+': '+pos+' x '+Math.round(r.l)+'-'+Math.round(r.r)+' h '+Math.round(r.b-r.t)+' (host h '+Math.round(host.b-host.t)+')'+' collisions '+hits+(r.r>W?' OUTSIDE':'');
  });
})()`));
out('emphasis', await ev(`(() => { const words=(t)=>t.trim().split(/\\s+/).length; const prose=[...document.querySelectorAll('.prose p, .prose li')].filter(e=>!e.closest('.quiz,.sources,.side')).map(e=>e.textContent).join(' '); const keys=[...document.querySelectorAll('.key')]; const kw=keys.map(k=>words(k.textContent)).reduce((a,b)=>a+b,0); return keys.length+' key sentences, '+kw+' words of '+words(prose)+' prose words ('+(100*kw/words(prose)).toFixed(1)+'%); '+document.querySelectorAll('.pt-k').length+' point labels; '+document.querySelectorAll('.side').length+' side notes'; })()`));
out('overflow', await ev(`document.documentElement.scrollWidth + ' vs ' + document.documentElement.clientWidth`));
out('console', logs.length ? logs : 'clean');
ws.close(); process.exit(0);
