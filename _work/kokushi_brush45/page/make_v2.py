"""Unified review page with per-version selection (旧版・改訂版（発展）・やさしい版).
Usage: python3 make_v2.py <config.json>
config: {src_html, data, out, collection, rev_label, new_rev_label, banner, extra_checks, old_err: {id: [..]}}
"""
import json, re, sys

cfg = json.load(open(sys.argv[1]))
src = open(cfg['src_html']).read()
css_end = src.index('</style>') + len('</style>')
head = src[:css_end]
head = head.replace('.ro{', '''.vsel{display:flex;align-items:center;gap:6px;margin-top:8px;font-size:.85rem}
.vsel button{font:inherit;font-size:.85rem;padding:5px 12px;border-radius:6px;border:1px solid var(--line);background:var(--panel);color:var(--fg);cursor:pointer}
.vsel button[aria-pressed="true"]{background:var(--accent);color:var(--panel);border-color:var(--accent)}
.vsel .main{font-size:.75rem;padding:1px 8px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}
.ver.on{outline:2px solid var(--accent);outline-offset:-1px}
.warn{font-size:.8rem;color:var(--badfg);background:var(--bad);padding:4px 8px;border-radius:4px;margin-top:6px}
.outcome{font-size:.86rem;padding:6px 10px;border-radius:6px;background:var(--accent-soft);color:var(--fg)}
.ro{''')
# keep the page's own header / intro / checks sections (everything between <div class="wrap"> and <div class="filters"
m = re.search(r'(<link rel="stylesheet".*?<div class="wrap">.*?)<div class="filters"', src, re.S)
intro = m.group(1)
if cfg.get('banner'):
    intro = re.sub(r'(<section class="box" style="border-color:var\(--accent\);background:var\(--ok\).*?</section>\s*)', '', intro, flags=re.S)
    intro = intro.replace('</header>', '</header>\n  ' + cfg['banner'], 1)
how = '''<section class="box">
    <h2>判断のしかた（10月8日に変更）</h2>
    <p>各問題で、アプリに入れたい版の「この版を使う」を押してください。<b>複数選べます</b>（例：やさしい版と旧版の両方）。</p>
    <p>元の問題番号には、選んだ版のうち <b>やさしい版 → 改訂版（発展） → 旧版</b> の順で最初のものを入れ、残りは新しい番号で追加します（「発展」「旧版」のタグ付き）。何も選ばずに「保留」にした問題は変更しません。</p>
    <p>旧版に事実の誤りや正答の誤りが見つかっている問題には、旧版の欄に注意書きを出しています。旧版を残す場合は、誤りの部分だけ直してから入れます。</p>
  </section>
  '''
intro = intro.replace('<section class="box" id="checks"></section>', how + '<section class="box" id="checks"></section>')

body = intro + '''<div class="filters" id="filters"></div>
  <div class="tally" id="tally"></div>
  <p class="ro" id="dbstate" hidden></p>
  <div id="list" style="display:grid;gap:16px"></div>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>
const ITEMS = JSON.parse(document.getElementById('data').textContent);
const CHECKS = __CHECKS__;
const OLDERR = __OLDERR__;
const REV_LABEL = __REVLABEL__, NEWREV_LABEL = __NEWREVLABEL__;
const COLL = __COLL__;
const dec = {}; let db=null, canWrite=true, filter='all';
const esc = s => String(s ?? '').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt = q => (q.section? q.section+'・':'') + (q.answer.length===2?'2つ選べ':'1つ選べ');
const len = q => { const cl=q.choices.map(c=>c.length); return `問題文${q.text.length}字・選択肢${Math.min(...cl)}〜${Math.max(...cl)}字`; };
// legacy single-choice -> version set
const LEGACY = {easy_keep:['easy','rev'], easy_only:['easy'], rev:['rev'], old:['old'], add:['rev','easy'], replace:['easy'], keep:['rev'], orig:['rev'], adopt:['easy']};
function vers(it){ const d=dec[it.id]||{}; if(d.versions) return d.versions; if(d.choice && LEGACY[d.choice] && !['del','move'].includes(it.kind)) return LEGACY[d.choice]; return []; }
function isDel(it){ return it.kind==='del'||it.kind==='move'; }
function avail(it){
  if(isDel(it)) return [];
  if(it.kind==='pnew') return ['easy'];
  if(it.kind==='new'||it.kind==='new5') return it.unchanged?['rev']:['easy','rev'];
  return it.unchanged?['rev','old']:['easy','rev','old'];
}
function label(it,k){
  if(k==='old') return '旧版';
  if(k==='easy') return it.kind==='pnew'?'新問題':'やさしい版';
  if(it.kind==='new') return '元の新作（承認済み）';
  if(it.kind==='new5') return NEWREV_LABEL;
  return it.unchanged? REV_LABEL+'（変更なし）' : REV_LABEL;
}
function mainOf(it, vs){ for(const k of ['easy','rev','old']) if(vs.includes(k)) return k; return null; }
function ver(it, q, k, show){
  if(!q) return '';
  const a=new Set(q.answer); const vs=vers(it); const on=vs.includes(k); const main=mainOf(it,vs)===k;
  const err = (k==='old' && OLDERR[it.id]) ? `<div class="warn">旧版には誤りが見つかっています：${esc(OLDERR[it.id].join(' / '))}</div>` : '';
  const sel = isDel(it) ? '' : `<div class="vsel"><button type="button" data-v="${k}" aria-pressed="${on}">${on?'✓ この版を使う':'この版を使う'}</button>${main?'<span class="main">元の番号に入る版</span>':(on?'<span class="main">新しい番号で追加</span>':'')}</div>`;
  return `<div class="ver ${k==='easy'?'easy':''} ${on?'on':''}" data-v="${k}" ${show?'':'hidden'}>
    <h3>${label(it,k)}</h3><div class="meta">${esc(fmt(q))}</div><div class="len">${len(q)}</div>
    <p class="stem">${esc(q.text)}</p>${q.img?`<img src="${q.img}" alt="図" style="max-width:100%;border:1px solid var(--line);border-radius:4px;background:#fff">`:''}
    <ol class="ch">${q.choices.map((c,i)=>`<li class="${a.has(String(i+1))?'ok':''}"><span>${i+1}</span><span>${esc(c)}</span></li>`).join('')}</ol>
    <details><summary>解説</summary><p class="cm">${esc(q.comment)}</p></details>${err}${sel}</div>`;
}
function outcome(it){
  const d=dec[it.id]||{};
  if(isDel(it)){ const m={delete:'削除する',keep:'残す',move:'移動する',hold:'保留'}; return d.choice?`判断：${m[d.choice]||d.choice}`:'未判断'; }
  if(d.choice==='hold') return '判断：保留（変更しない）';
  const vs=vers(it); if(!vs.length) return '未判断';
  const main=mainOf(it,vs); const rest=vs.filter(k=>k!==main);
  if(it.kind==='pnew') return '判断：採用する';
  return `判断：元の番号に「${label(it,main)}」` + (rest.length?`、新しい番号で「${rest.map(k=>label(it,k)).join('」「')}」を追加`:'');
}
function card(it){
  const d=dec[it.id]||{};
  const del=isDel(it), isNew=['new','new5','pnew'].includes(it.kind);
  const av=avail(it);
  const order=['easy','rev','old'].filter(k=>av.includes(k));
  const tabs = (!del && order.length>1) ? `<div class="tabs" role="group" aria-label="表示する版">${order.map((k,i)=>`<button type="button" data-show="${k}" aria-pressed="${i===0}">${label(it,k)}</button>`).join('')}</div>` : '';
  const cols = del ? ver(it,it.old,'old',true) : order.map((k,i)=>ver(it,it[k],k,i===0)).join('');
  const ncol = del?1:order.length;
  const btns = del ? (it.kind==='move'?[['move','移動を承認'],['keep','この回に残す'],['hold','保留']]:[['delete','削除を承認'],['keep','残す（旧版のまま）'],['hold','保留']]) : [['hold','保留']];
  const done = (d.choice && d.choice!=='hold') || (d.versions&&d.versions.length) || (!del && vers(it).length);
  return `<article id="c-${it.id}" class="${done?'done':''}" data-id="${it.id}">
    <div class="head"><span class="pid">${it.id}</span>
      <span class="chip">第${it.lec}回</span>${it.brushed?'<span class="chip n">見直しで変更</span>':''}${isNew?'<span class="chip n">'+(it.kind==='new'?'新作':'新問題')+'</span>':''}${it.kind==='del'?'<span class="chip t">削除案</span>':''}${it.kind==='move'?'<span class="chip t">移動案</span>':''}
      ${(it.tags||[]).map(t=>`<span class="chip t">${esc(t)}</span>`).join('')}${it.pilot?'<span class="chip">試作から移動</span>':''}</div>
    ${it.unchanged&&!del?`<div class="same">${isNew?'元の問題がすでに国試並みのため、やさしい版は作っていません。':'改訂版がすでに国試並みのため、やさしい版は作っていません。'}</div>`:''}
    <div class="note"><b>${del?(it.kind==='move'?'移動の理由':'削除・統合の理由'):(it.unchanged?'補足':'作り直しの要点')}：</b>${esc(it.note)}</div>
    ${tabs}
    <div class="cols" style="--n:${ncol}">${cols}</div>
    <div class="outcome" data-out>${esc(outcome(it))}</div>
    <details><summary>根拠の資料（${(it.sources||[]).length}件）</summary><ul>${(it.sources||[]).map(s=>`<li>${esc(s)}</li>`).join('')}</ul></details>
    <div class="decide">
      <div class="opts" role="group" aria-label="判断">${btns.map(([k,l])=>`<button type="button" data-choice="${k}" aria-pressed="${d.choice===k}">${l}</button>`).join('')}</div>
      <textarea id="note-${it.id}" placeholder="直してほしい点・コメント（任意。何度でも書き直せます）">${esc(d.note||'')}</textarea>
      <div class="save"><button type="button" data-save>コメントを保存</button><span data-msg></span></div>
    </div></article>`;
}
function judged(it){ const d=dec[it.id]||{}; return !!(d.choice || (d.versions&&d.versions.length)); }
function visible(it){ const d=dec[it.id]||{};
  if(filter==='l4') return it.lec===4; if(filter==='l5') return it.lec===5; if(filter==='brushed') return !!it.brushed; if(filter==='rev') return it.kind==='revised'; if(filter==='new') return ['new','new5','pnew'].includes(it.kind);
  if(filter==='del') return isDel(it); if(filter==='todo') return !judged(it); if(filter==='hold') return d.choice==='hold'; return true; }
function filters(){ const F=[['all','すべて'],['l4','第4回'],['l5','第5回'],['brushed','見直しで変更'],['rev','改訂'],['new','新作・新問題'],['del','削除・移動案'],['todo','未判断'],['hold','保留']].filter(([k])=>k!=='del'||ITEMS.some(isDel));
  document.getElementById('filters').innerHTML=F.map(([k,l])=>`<button type="button" data-f="${k}" aria-pressed="${filter===k}">${l}</button>`).join(''); }
function checks(){ const el=document.getElementById('checks'); if(el) el.innerHTML = CHECKS.length?`<h2>先生にご確認いただきたい点</h2><ul>${CHECKS.map(c=>`<li>${esc(c)}</li>`).join('')}</ul>`:''; if(el && !CHECKS.length) el.hidden=true; }
function tally(){ const n=ITEMS.filter(judged).length;
  document.getElementById('tally').innerHTML=`<span>全${ITEMS.length}問</span><span>判断済み ${n}</span><span>未判断 ${ITEMS.length-n}</span>`; }
function render(){ checks(); filters(); document.getElementById('list').innerHTML=ITEMS.filter(visible).map(card).join('')||'<p>該当する問題はありません。</p>'; tally();
  if(!canWrite) document.querySelectorAll('.decide button,.decide textarea,.vsel button').forEach(e=>e.disabled=true); }
async function save(id, patch, msgEl){
  dec[id]=Object.assign({},dec[id]||{},patch);
  if(!db||!canWrite) return;
  try{ await db.collection(COLL).doc(id).set(Object.assign({choice:null,versions:[],note:''},dec[id],{updatedAt:new Date().toISOString()}));
       if(msgEl) msgEl.textContent='保存しました'; }
  catch(e){ if(msgEl) msgEl.textContent='保存できませんでした（'+(e&&e.code||'不明')+'）'; }
}
function rerender(id){ const it=ITEMS.find(x=>x.id===id); const el=document.getElementById('c-'+id); if(!it||!el) return;
  const shown=[...el.querySelectorAll('.ver')].find(v=>!v.hidden)?.dataset.v; const note=document.getElementById('note-'+id)?.value;
  el.outerHTML=card(it); const nel=document.getElementById('c-'+id);
  if(shown){ nel.querySelectorAll('.tabs button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.show===shown)); nel.querySelectorAll('.ver').forEach(v=>v.hidden=v.dataset.v!==shown); }
  if(note!=null) document.getElementById('note-'+id).value=note; tally(); }
document.addEventListener('click',e=>{
  const t=e.target.closest('button'); if(!t) return;
  if(t.dataset.f){ filter=t.dataset.f; render(); return; }
  const box=t.closest('article[data-id]'); if(!box) return; const id=box.dataset.id; const it=ITEMS.find(x=>x.id===id);
  if(t.dataset.show){ box.querySelectorAll('.tabs button').forEach(b=>b.setAttribute('aria-pressed',b===t));
    box.querySelectorAll('.ver').forEach(v=>v.hidden=v.dataset.v!==t.dataset.show); return; }
  if(t.closest('.vsel') && t.dataset.v){ const k=t.dataset.v; let vs=[...vers(it)]; vs = vs.includes(k)? vs.filter(x=>x!==k) : [...vs,k];
    save(id,{versions:vs, choice: vs.length?'versions':null},box.querySelector('[data-msg]')); rerender(id); return; }
  if(t.dataset.choice){ const c=(dec[id]?.choice===t.dataset.choice)?null:t.dataset.choice;
    const patch = isDel(it)? {choice:c} : {choice:c, versions: c==='hold'?[]:vers(it)};
    save(id,patch,box.querySelector('[data-msg]')); rerender(id); return; }
  if(t.hasAttribute('data-save')){ save(id,{note:document.getElementById('note-'+id).value},box.querySelector('[data-msg]')); }
});
render();
(async()=>{ try{
  db = await window.claude.use('db');
  if(!db){ const s=document.getElementById('dbstate'); s.hidden=false; s.textContent='判断の保存は、claude.ai にサインインして開いたときに使えます。'; canWrite=false; render(); return; }
  db.collection(COLL).onSnapshot(snap=>{
    snap.docs.forEach(d=>{ dec[d.id]=d.data(); });
    const act=document.activeElement&&document.activeElement.tagName==='TEXTAREA';
    if(!act) render(); else tally();
  }, ()=>{});
}catch(e){ const s=document.getElementById('dbstate'); s.hidden=false; s.textContent='判断を保存する機能に接続できませんでした。ページを開き直してください。'; } })();
</script>
'''
data = json.load(open(cfg['data']))
checks = cfg.get('checks')
if checks is None:
    mm = re.search(r'const CHECKS = (\[.*?\]);', src, re.S)
    checks = json.loads(mm.group(1)) if mm else []
html = (head + body).replace('__DATA__', json.dumps(data, ensure_ascii=False).replace('</', '<\\/')) \
    .replace('__CHECKS__', json.dumps(checks, ensure_ascii=False)) \
    .replace('__OLDERR__', json.dumps(cfg.get('old_err', {}), ensure_ascii=False)) \
    .replace('__REVLABEL__', json.dumps(cfg['rev_label'], ensure_ascii=False)) \
    .replace('__NEWREVLABEL__', json.dumps(cfg.get('new_rev_label', '元の新問題'), ensure_ascii=False)) \
    .replace('__COLL__', json.dumps(cfg['collection']))
open(cfg['out'], 'w').write(html)
print('wrote', cfg['out'], len(data))
