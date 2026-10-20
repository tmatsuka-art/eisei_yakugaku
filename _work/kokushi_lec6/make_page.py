"""第6回（特別用途食品・保健機能食品）確認ページ。
usage: python3 make_page.py page_data.json cfg.json out.html
page_data: [{id, group:'new'|'past'|'future', topic, section, text, choices, answer, comment, note, sources, concerns, fact_errors, verdict, fix}]
cfg: {title, checks:[..], rename:{...}}
"""
import json, re, sys
data = json.load(open(sys.argv[1])); cfg = json.load(open(sys.argv[2])); out = sys.argv[3]
src = open('/home/claude/eisei_yakugaku/_work/kokushi_brush45/page/src_lec45.html').read()
css = src[src.index('<style>'):src.index('</style>') + 8]
css = css.replace('</style>', '''.vbad{font-size:.82rem;color:var(--badfg);background:var(--bad);padding:6px 10px;border-radius:6px}
.vfix{font-size:.82rem;color:var(--warnfg);background:var(--warn);padding:6px 10px;border-radius:6px}
.outcome{font-size:.86rem;padding:6px 10px;border-radius:6px;background:var(--accent-soft);color:var(--fg)}
.sec{font-family:var(--f-head);font-size:1.2rem;margin:10px 0 0}
</style>''')
body = '''<div class="wrap">
<header><h1>__TITLE__</h1><p class="lead">教科書 pp.284–299・授業スライドの範囲。今日の新作40問、今ある第6回の48問、10月8日に作った新問題12問を並べています。判断は自動で保存されます。</p></header>
<section class="box" id="rename"></section>
<section class="box"><h2>判断のしかた</h2>
<p><b>新作</b>：「採用」「保留」「採用しない」から選んでください。直してほしい点はコメント欄へ。採用した問題は新しい番号で第6回に入れます。</p>
<p><b>今ある問題</b>：今日の点検結果を見て選んでください。10月8日に改訂案（やさしい版・発展版）を作った21問は、版を並べて表示し、どの版にするかを選べます。過去問は問題文を変えず、解説だけ直します。</p>
<p><b>10月8日の新問題</b>（12問）：前回の確認ページでまだ判断されていなかったので、ここに並べました。今日の新作と重なるものは、片方だけ採用してください。</p></section>
<section class="box" id="checks"></section>
<div class="filters" id="filters"></div>
<div class="tally" id="tally"></div>
<p class="ro" id="dbstate" hidden></p>
<div id="list" style="display:grid;gap:16px"></div>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>
const ITEMS = JSON.parse(document.getElementById('data').textContent);
const CFG = __CFG__;
const COLL = 'lec6';
const dec = {}; let db=null, canWrite=true, filter='all';
const esc = s => String(s ?? '').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const isNew = it => it.group==='new'||it.group==='oct8new';
const BTN_NEW=[['adopt','採用'],['hold','保留'],['reject','採用しない']];
const BTN_OLD=[['keep','このまま残す'],['fix','直して残す（点検の案のとおり）'],['delete','削除する'],['hold','保留']];
const BTN_VER=[['easy','やさしい版に替える'],['adv','発展版に替える'],['both','やさしい版＋発展版'],['fix','旧版を直して残す'],['delete','削除する'],['hold','保留']];
const GLBL={new:'今日の新作',past:'過去問',future:'今ある予想問題',oct8new:'10月8日の新問題'};
const LBL2={easy:'やさしい版に替える',adv:'発展版に替える',both:'やさしい版＋発展版（発展版は新しい番号で追加）'};
const LBL = Object.assign(Object.fromEntries([...BTN_NEW,...BTN_OLD]),LBL2);
const VERD = {keep:'点検結果：このままでよい', fix:'点検結果：直す必要あり', delete_candidate:'点検結果：削除候補'};
function qhtml(q){ const a=new Set(q.answer||[]);
  return `<p class="stem">${esc(q.text)}</p>${q.img?`<img src="${esc(q.img)}" alt="問題の図" style="max-width:100%;background:#fff;border:1px solid var(--line);border-radius:4px">`:''}
    <ol class="ch">${(q.choices||[]).map((c,i)=>`<li class="${a.has(String(i+1))?'ok':''}"><span>${i+1}</span><span>${esc(c)}</span></li>`).join('')}</ol>
    <details><summary>解説</summary><p class="cm">${esc(q.comment)}</p></details>`; }
const two = q => ((q.section?q.section+'・':'') + ((q.answer||[]).length===2?'2つ選べ':'1つ選べ'));
function card(it){
  const d=dec[it.id]||{};
  const btns = isNew(it)?BTN_NEW:(it.vers?BTN_VER:BTN_OLD);
  const list=(t,arr,cls)=>(arr||[]).length?`<div class="${cls}"><b>${t}</b><ul>${arr.map(e=>`<li>${esc(e)}</li>`).join('')}</ul></div>`:'';
  let body;
  if(it.vers){
    const V=[['old','今の版',it],['easy','やさしい版（10月8日）',it.vers.easy],['adv','発展版（10月8日）',it.vers.adv]];
    body=`<div class="tabs" role="group" aria-label="表示する版">${V.map(([k,l],i)=>`<button type="button" data-show="${k}" aria-pressed="${i===0}">${l}</button>`).join('')}</div>
      <div class="cols" style="--n:3">${V.map(([k,l,q],i)=>`<div class="ver ${k==='easy'?'easy':''}" data-v="${k}" ${i===0?'':'hidden'}><h3>${l}</h3><div class="meta">${esc(two(q))}</div>${qhtml(q)}</div>`).join('')}</div>`;
  } else body=`<div class="ver"><div class="meta">${esc(two(it))}</div>${qhtml(it)}</div>`;
  return `<article id="c-${it.id}" class="${d.choice?'done':''}" data-id="${it.id}">
   <div class="head"><span class="pid">${esc(it.group==='new'?'新作'+it.id.slice(3):it.id)}</span>
    <span class="chip ${isNew(it)?'n':''}">${GLBL[it.group]}</span>${it.topic?`<span class="chip">${esc(it.topic)}</span>`:''}
    ${it.vers?'<span class="chip n">10月8日の改訂案あり</span>':''}${it.oct8del?'<span class="chip t">10月8日に削除案</span>':''}
    ${!isNew(it)&&it.verdict?`<span class="chip t">${esc(VERD[it.verdict]||it.verdict)}</span>`:''}</div>
   ${it.note?`<div class="note"><b>ねらい：</b>${esc(it.note)}</div>`:''}
   ${it.checked?`<div class="same">${esc(it.checked)}</div>`:''}
   ${body}
   ${list('今の版の事実の誤り・古い記述（今日の点検）：',it.fact_errors,'vbad')}${list('問題の質（今日の点検）：',it.quality,'vfix')}
   ${it.fix?`<div class="note"><b>今の版の直し方の案：</b>${esc(it.fix)}</div>`:''}
   ${it.oct8?`<details><summary>10月8日の改訂の要点</summary><p class="cm">${esc(it.oct8)}</p></details>`:''}
   ${it.oct8del?`<div class="vfix"><b>10月8日の削除・統合案の理由：</b>${esc(it.oct8del)}</div>`:''}
   ${list('ご確認ください：',it.concerns,'vfix')}
   ${(it.sources||[]).length?`<details><summary>根拠の資料（${it.sources.length}件）</summary><ul>${it.sources.map(s=>`<li>${esc(s)}</li>`).join('')}</ul></details>`:''}
   <div class="outcome">${d.choice?'判断：'+esc(LBL[d.choice]||d.choice):'未判断'}</div>
   <div class="decide"><div class="opts" role="group" aria-label="判断">${btns.map(([k,l])=>`<button type="button" data-choice="${k}" aria-pressed="${d.choice===k}">${l}</button>`).join('')}</div>
    <textarea id="note-${it.id}" placeholder="直してほしい点・コメント（任意）">${esc(d.note||'')}</textarea>
    <div class="save"><button type="button" data-save>コメントを保存</button><span data-msg></span></div></div></article>`;
}
function visible(it){ const d=dec[it.id]||{};
  if(filter==='new') return it.group==='new'; if(filter==='oct8') return it.group==='oct8new'; if(filter==='old') return !isNew(it);
  if(filter==='err') return !isNew(it)&&it.verdict!=='keep'; if(filter==='todo') return !d.choice; if(filter==='hold') return d.choice==='hold'; return true; }
function filters(){ const F=[['all','すべて'],['new','今日の新作'],['oct8','10月8日の新問題'],['old','今ある問題'],['err','直す・削除の候補'],['todo','未判断'],['hold','保留']];
  document.getElementById('filters').innerHTML=F.map(([k,l])=>`<button type="button" data-f="${k}" aria-pressed="${filter===k}">${l}</button>`).join(''); }
function tops(){ const r=document.getElementById('rename'); r.innerHTML=CFG.rename||''; if(!CFG.rename) r.hidden=true;
  const el=document.getElementById('checks'); el.innerHTML=CFG.checks.length?`<h2>先生にご確認いただきたい点</h2><ul>${CFG.checks.map(c=>`<li>${esc(c)}</li>`).join('')}</ul>`:''; el.hidden=!CFG.checks.length; }
function tally(){ const nn=ITEMS.filter(isNew), oo=ITEMS.filter(x=>!isNew(x)); const c=(arr,k)=>arr.filter(x=>(dec[x.id]||{}).choice===k).length;
  const done=ITEMS.filter(x=>(dec[x.id]||{}).choice).length;
  document.getElementById('tally').innerHTML=`<span>判断済み ${done}／${ITEMS.length}</span><span>新問題${nn.length}問：採用 ${c(nn,'adopt')}・保留 ${c(nn,'hold')}・不採用 ${c(nn,'reject')}</span><span>今ある${oo.length}問：残す ${c(oo,'keep')}・直す ${c(oo,'fix')}・版を替える ${c(oo,'easy')+c(oo,'adv')+c(oo,'both')}・削除 ${c(oo,'delete')}・保留 ${c(oo,'hold')}</span>`; }
const SEC={new:'1. 今日の新作（教科書 pp.284–299・授業スライドの範囲）',past:'2. 今ある第6回の問題（過去問・予想問題）',oct8new:'3. 10月8日に作った新問題（まだ判断されていません）'};
function render(){ filters(); let html='', last=null; ITEMS.filter(visible).forEach(it=>{ const g=it.group==='future'?'past':it.group; if(g!==last){ html+=`<h2 class="sec">${SEC[g]}</h2>`; last=g; } html+=card(it); });
  document.getElementById('list').innerHTML=html||'<p>該当する問題はありません。</p>'; tally();
  if(!canWrite) document.querySelectorAll('.decide button,.decide textarea').forEach(e=>e.disabled=true); }
async function save(id, patch, msgEl){
  dec[id]=Object.assign({},dec[id]||{},patch);
  if(!db||!canWrite) return;
  try{ await db.collection(COLL).doc(id).set(Object.assign({choice:null,note:''},dec[id],{updatedAt:new Date().toISOString()})); if(msgEl) msgEl.textContent='保存しました'; }
  catch(e){ if(msgEl) msgEl.textContent='保存できませんでした（'+(e&&e.code||'不明')+'）'; }
}
function rerender(id){ const it=ITEMS.find(x=>x.id===id); const el=document.getElementById('c-'+id); if(!it||!el) return;
  const note=document.getElementById('note-'+id)?.value; el.outerHTML=card(it); if(note!=null) document.getElementById('note-'+id).value=note; tally(); }
document.addEventListener('click',e=>{ const t=e.target.closest('button'); if(!t) return;
  if(t.dataset.f){ filter=t.dataset.f; render(); return; }
  const box=t.closest('article[data-id]'); if(!box) return; const id=box.dataset.id;
  if(t.dataset.show){ box.querySelectorAll('.tabs button').forEach(b=>b.setAttribute('aria-pressed',b===t)); box.querySelectorAll('.ver').forEach(v=>v.hidden=v.dataset.v!==t.dataset.show); return; }
  if(t.dataset.choice){ const c=(dec[id]?.choice===t.dataset.choice)?null:t.dataset.choice; save(id,{choice:c},box.querySelector('[data-msg]')); rerender(id); return; }
  if(t.hasAttribute('data-save')) save(id,{note:document.getElementById('note-'+id).value},box.querySelector('[data-msg]')); });
tops(); render();
(async()=>{ try{ db = await window.claude.use('db');
  if(!db){ const s=document.getElementById('dbstate'); s.hidden=false; s.textContent='判断の保存は、claude.ai にサインインして開いたときに使えます。'; canWrite=false; render(); return; }
  db.collection(COLL).onSnapshot(snap=>{ snap.docs.forEach(d=>{ dec[d.id]=d.data(); });
    const act=document.activeElement&&document.activeElement.tagName==='TEXTAREA'; if(!act) render(); else tally(); }, ()=>{});
 }catch(e){ const s=document.getElementById('dbstate'); s.hidden=false; s.textContent='判断を保存する機能に接続できませんでした。ページを開き直してください。'; } })();
</script>'''
html = '<title>' + cfg['title'] + '</title>\n' + css + '\n' + body
html = html.replace('__TITLE__', cfg['title']).replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/')).replace('__CFG__', json.dumps(cfg, ensure_ascii=False).replace('</', '<\\/'))
open(out, 'w').write(html); print('wrote', out, len(data))
