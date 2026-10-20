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
<header><h1>__TITLE__</h1><p class="lead">教科書 pp.284–299・授業スライドの範囲。新作の問題と、今ある第6回の問題を並べています。判断は自動で保存されます。</p></header>
<section class="box" id="rename"></section>
<section class="box"><h2>判断のしかた</h2>
<p><b>新作</b>：「採用」「保留」「採用しない」から選んでください。直してほしい点はコメント欄へ。採用した問題は新しい番号で第6回に入れます。</p>
<p><b>今ある問題</b>：点検結果を見て「このまま残す」「直して残す（案のとおり）」「削除する」「保留」から選んでください。過去問は問題文を変えず、解説だけ直します。</p></section>
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
const isNew = it => it.group==='new';
const BTN_NEW=[['adopt','採用'],['hold','保留'],['reject','採用しない']];
const BTN_OLD=[['keep','このまま残す'],['fix','直して残す（案のとおり）'],['delete','削除する'],['hold','保留']];
const LBL = Object.fromEntries([...BTN_NEW,...BTN_OLD]);
const VERD = {keep:'点検結果：このままでよい', fix:'点検結果：直す必要あり', delete_candidate:'点検結果：削除候補'};
function card(it){
  const d=dec[it.id]||{}; const a=new Set(it.answer||[]);
  const btns = isNew(it)?BTN_NEW:BTN_OLD;
  const two = (it.answer||[]).length===2?'2つ選べ':'1つ選べ';
  const errs = (it.fact_errors||[]).length?`<div class="vbad"><b>事実の誤り・古い記述：</b><ul>${it.fact_errors.map(e=>`<li>${esc(e)}</li>`).join('')}</ul></div>`:'';
  const qual = (it.quality||[]).length?`<div class="vfix"><b>問題の質：</b><ul>${it.quality.map(e=>`<li>${esc(e)}</li>`).join('')}</ul></div>`:'';
  const fix = it.fix?`<div class="note"><b>直し方の案：</b>${esc(it.fix)}</div>`:'';
  const conc = (it.concerns||[]).length?`<div class="vfix"><b>ご確認ください：</b><ul>${it.concerns.map(e=>`<li>${esc(e)}</li>`).join('')}</ul></div>`:'';
  return `<article id="c-${it.id}" class="${d.choice?'done':''}" data-id="${it.id}">
   <div class="head"><span class="pid">${esc(it.id)}</span>
    <span class="chip ${isNew(it)?'n':''}">${isNew(it)?'新作':(it.group==='past'?'過去問':'今ある予想問題')}</span>
    ${it.topic?`<span class="chip">${esc(it.topic)}</span>`:''}<span class="chip">${esc((it.section?it.section+'・':'')+two)}</span>
    ${!isNew(it)&&it.verdict?`<span class="chip t">${esc(VERD[it.verdict]||it.verdict)}</span>`:''}</div>
   ${it.note?`<div class="note"><b>${isNew(it)?'ねらい':'点検の要点'}：</b>${esc(it.note)}</div>`:''}
   <div class="ver"><p class="stem">${esc(it.text)}</p>${it.img?`<img src="${esc(it.img)}" alt="問題の図" style="max-width:100%">`:''}
    <ol class="ch">${(it.choices||[]).map((c,i)=>`<li class="${a.has(String(i+1))?'ok':''}"><span>${i+1}</span><span>${esc(c)}</span></li>`).join('')}</ol>
    <details><summary>解説</summary><p class="cm">${esc(it.comment)}</p></details></div>
   ${errs}${qual}${fix}${conc}
   ${(it.sources||[]).length?`<details><summary>根拠の資料（${it.sources.length}件）</summary><ul>${it.sources.map(s=>`<li>${esc(s)}</li>`).join('')}</ul></details>`:''}
   <div class="outcome">${d.choice?'判断：'+esc(LBL[d.choice]||d.choice):'未判断'}</div>
   <div class="decide"><div class="opts" role="group" aria-label="判断">${btns.map(([k,l])=>`<button type="button" data-choice="${k}" aria-pressed="${d.choice===k}">${l}</button>`).join('')}</div>
    <textarea id="note-${it.id}" placeholder="直してほしい点・コメント（任意）">${esc(d.note||'')}</textarea>
    <div class="save"><button type="button" data-save>コメントを保存</button><span data-msg></span></div></div></article>`;
}
function visible(it){ const d=dec[it.id]||{};
  if(filter==='new') return isNew(it); if(filter==='old') return !isNew(it);
  if(filter==='err') return !isNew(it)&&it.verdict!=='keep'; if(filter==='todo') return !d.choice; if(filter==='hold') return d.choice==='hold'; return true; }
function filters(){ const F=[['all','すべて'],['new','新作'],['old','今ある問題'],['err','直す・削除の候補'],['todo','未判断'],['hold','保留']];
  document.getElementById('filters').innerHTML=F.map(([k,l])=>`<button type="button" data-f="${k}" aria-pressed="${filter===k}">${l}</button>`).join(''); }
function tops(){ const r=document.getElementById('rename'); r.innerHTML=CFG.rename||''; if(!CFG.rename) r.hidden=true;
  const el=document.getElementById('checks'); el.innerHTML=CFG.checks.length?`<h2>先生にご確認いただきたい点</h2><ul>${CFG.checks.map(c=>`<li>${esc(c)}</li>`).join('')}</ul>`:''; el.hidden=!CFG.checks.length; }
function tally(){ const nn=ITEMS.filter(isNew), oo=ITEMS.filter(x=>!isNew(x)); const c=(arr,k)=>arr.filter(x=>(dec[x.id]||{}).choice===k).length;
  document.getElementById('tally').innerHTML=`<span>新作${nn.length}問：採用 ${c(nn,'adopt')}・保留 ${c(nn,'hold')}・不採用 ${c(nn,'reject')}</span><span>今ある${oo.length}問：残す ${c(oo,'keep')}・直す ${c(oo,'fix')}・削除 ${c(oo,'delete')}・保留 ${c(oo,'hold')}</span>`; }
function render(){ filters(); document.getElementById('list').innerHTML=ITEMS.filter(visible).map(card).join('')||'<p>該当する問題はありません。</p>'; tally();
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
