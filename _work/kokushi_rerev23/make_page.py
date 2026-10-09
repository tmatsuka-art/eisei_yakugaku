"""第2・3回 再改訂版の確認ページを作る。python3 make_page.py"""
import json, re
B = '/home/claude/eisei_yakugaku/_work/'
src = open(B + 'kokushi_easy/page/review_lec23.html').read()
style = src[src.index('<style>'):src.index('</style>') + len('</style>')]
style = style.replace('</style>', '''
.diff{background:var(--warn);color:var(--warnfg);border-radius:3px;padding:0 2px}
ol.ch li.chg{box-shadow:inset 3px 0 0 var(--warnfg)}
ol.ch li.ok.chg{box-shadow:inset 3px 0 0 var(--okfg)}
.req{font-size:.9rem;border-left:3px solid var(--accent);padding:6px 10px;background:var(--accent-soft);border-radius:0 6px 6px 0}
.req b{font-family:var(--f-head)}
.chk{font-size:.85rem;background:var(--warn);color:var(--warnfg);padding:6px 10px;border-radius:6px}
.acts{font-size:.85rem;margin:0;padding-left:1.2em;color:var(--muted)}
.ver.after{border-color:var(--accent)}
.ver.after h3{color:var(--accent)}
td.a{font-size:.82rem}
tr.hl td{background:var(--accent-soft)}
</style>''')
items = json.load(open(B + 'kokushi_rerev23/page/rerev23_data.json'))
plan = json.load(open(B + 'kokushi_rerev23/apply_plan.json'))
LAB = {'easy': 'やさしい版', 'rev': '発展版', 'old': '旧版'}
for p in plan:
    p['selLabel'] = '・'.join(LAB[v] for v in p['sel']) if p['sel'] else ('（判断なし）' if not p['touched'] else ('不要' if p['note'] == '不要' else '（選択なし）'))

n_rerev = sum(1 for x in items if x['type'] == 'rerev')
n_cmt = sum(1 for x in items if x['type'] == 'rerev' and x['commented'])
n_copy_del = sum(1 for p in plan for a in p['acts'] if '発展版のコピー）を削除' in a)

html = '<title>第2・3回 再改訂版</title>\n' + style + '''
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;600;700&family=Zen+Kaku+Gothic+New:wght@700&display=swap">
<div class="wrap">
<header>
  <h1>衛生化学I 第2・3回　再改訂版（鈴木先生のご意見の反映）</h1>
  <p class="lead">「第2・3回 やさしい改訂版」のページで鈴木先生が選んだ版とコメントをもとに作り直しました。まだアプリには反映していません。</p>
</header>
<section class="box" style="border-color:var(--accent);background:var(--ok);color:var(--okfg)"><p><b>✔ 反映済み（10月9日、review ブランチ）。</b>鈴木先生・松川先生のご判断（再改訂版はすべて採用、不要の3問は削除、選ばれなかった発展版のコピーは削除、F1417 はやさしい版）を予想問題のデータに反映しました。旧版の追加分は F1497（F226）・F1498（F247）・F1499（F629）です。</p></section>
<section class="box">
  <h2>このページでお願いしたいこと</h2>
  <p>コメントをいただいた<b>__NCMT__問</b>は、ご意見どおりに選択肢・解説を直しました。旧版を選ばれた問題（コメントなし）も、旧版の解説の書き方や小さな誤りを直しています（合わせて__NRR__問）。各問題の「この再改訂版でよい／直してほしい／保留」を押してください。直してほしい点は、下の欄に書いて「メモを保存」を押してください。</p>
  <p>変更前の版と再改訂版を並べています。<span class="diff">黄色の印</span>の選択肢が変わったところ、緑が正答です。</p>
  <p>判断がそろったら、Claudeに「第2・3回の再改訂版を反映して」とお伝えください。このページの判断どおりにアプリのデータを更新します。</p>
</section>
<section class="box" id="global">
  <h2>まとめてご判断いただきたいこと</h2>
  <p>鈴木先生が<b>やさしい版だけ</b>（または旧版だけ）を選んだ問題では、10月8日に「発展」として追加した発展版のコピーが__NCOPY__問あります。前のページの説明（「アプリに入れたい版を押す」）に従うと、これらは<b>削除</b>になります。先生は以前「発展版もアプリに残したい」とおっしゃっていたので、どちらにするか選んでください。</p>
  <div class="opts" id="copyopts">
    <button type="button" data-copy="remove" aria-pressed="false">選ばれなかった発展版は削除する（鈴木先生の選択どおり）</button>
    <button type="button" data-copy="keep" aria-pressed="false">発展版は残す（「発展」タグのまま）</button>
  </div>
  <p class="save"><span data-gmsg></span></p>
</section>
<section class="box" id="checks"></section>
<section class="box">
  <h2>アプリへの反映案（全62問）</h2>
  <p class="why">再改訂版のある問題は色を付けています。「判断なし」は鈴木先生が触れていない問題で、今のまま（10月8日の反映のまま）にします。</p>
  <div class="tw"><table><thead><tr><th>問題</th><th>回</th><th>鈴木先生の選択</th><th>反映の内容</th></tr></thead><tbody id="plan"></tbody></table></div>
</section>
<div class="filters" id="filters"></div>
<div class="tally" id="tally"></div>
<p class="ro" id="dbstate" hidden></p>
<div id="list" style="display:grid;gap:16px"></div>
</div>
<script id="data" type="application/json">__DATA__</script>
<script id="plandata" type="application/json">__PLAN__</script>
<script>
const ITEMS = JSON.parse(document.getElementById('data').textContent);
const PLAN = JSON.parse(document.getElementById('plandata').textContent);
const CHECKS = __CHECKS__;
const COLL = 'rerev23';
const LAB = {easy:'やさしい版',rev:'発展版',old:'旧版'};
const dec = {}; let db=null, canWrite=true, filter='all';
const esc = s => String(s ?? '').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt = q => (q.section? q.section+'・':'') + (/2つ選べ/.test(q.text)?'2つ選べ':'1つ選べ') + (/誤っている/.test(q.text)?'（誤りを選ぶ）':'');
const OPTS = {
  rerev:[['ok','この再改訂版でよい'],['fix','直してほしい'],['hold','保留']],
  del:[['ok','削除でよい'],['keep','残す（やさしい版を使う）'],['hold','保留']],
  hold:[['easy','やさしい版を使う'],['rev','元の新作を使う'],['del','削除する'],['hold','保留']]
};
function judged(it){ return !!(dec[it.id]&&dec[it.id].choice); }
function visible(it){ if(filter==='all') return true; if(filter==='todo') return !judged(it); if(filter==='cmt') return it.type==='rerev'&&it.commented; if(filter==='old') return it.type==='rerev'&&!it.commented; return it.type!=='rerev'; }
function filters(){ const f=[['all','すべて'],['todo','未判断'],['cmt','コメントへの対応'],['old','旧版の手直し'],['other','削除・保留']];
  document.getElementById('filters').innerHTML=f.map(([k,l])=>`<button type="button" data-f="${k}" aria-pressed="${filter===k}">${l}</button>`).join(''); }
function tally(){ const n=ITEMS.filter(judged).length;
  document.getElementById('tally').innerHTML=`<span>全${ITEMS.length}問</span><span>判断済み ${n}</span><span>未判断 ${ITEMS.length-n}</span>`; }
function planTable(){ document.getElementById('plan').innerHTML=PLAN.map(p=>`<tr class="${p.rerev?'hl':''}"><td class="n">${p.id}</td><td class="n">${p.lec}</td><td class="a">${esc(p.selLabel)}</td><td class="a">${p.acts.map(esc).join('<br>')}</td></tr>`).join(''); }
function checks(){ const el=document.getElementById('checks'); el.innerHTML=`<h2>先生にご確認いただきたい点</h2><ul>${CHECKS.map(c=>`<li>${esc(c)}</li>`).join('')}</ul>`; }
function ver(q, title, cls, other){
  if(!q) return '';
  const a=new Set(q.answer);
  const norm = t => String(t).replace(/[。\\s]/g,''); const chg = i => other && !other.choices.some(c=>norm(c)===norm(q.choices[i]));
  return `<div class="ver ${cls}"><h3>${title}</h3><div class="meta">${esc(fmt(q))}</div>
    <p class="stem">${other&&norm(other.text)!==norm(q.text)?'<span class="diff">'+esc(q.text)+'</span>':esc(q.text)}</p>
    <ol class="ch">${q.choices.map((c,i)=>`<li class="${a.has(String(i+1))?'ok':''} ${chg(i)?'chg':''}"><span>${i+1}</span><span>${chg(i)?'<span class="diff">'+esc(c)+'</span>':esc(c)}</span></li>`).join('')}</ol>
    <details ${cls==='after'?'open':''}><summary>解説</summary><p class="cm">${esc(q.comment)}</p></details></div>`;
}
function card(it){
  const d=dec[it.id]||{};
  const sel = it.sel.length? it.sel.map(v=>LAB[v]).join('・') : 'なし';
  let body='';
  if(it.type==='rerev'){
    body = `${it.request?`<div class="req"><b>鈴木先生のコメント：</b>${esc(it.request)}</div>`:''}
      <p class="why"><b>変更点：</b>${esc(it.change)}</p>${it.check?`<div class="chk">${esc(it.check)}</div>`:''}
      <div class="cols" style="--n:2">${ver(it.before,'変更前（'+LAB[it.target]+'）','',it.after)}${ver(it.after,'再改訂版（'+LAB[it.target]+'）','after',it.before)}</div>`;
  } else {
    body = `${it.request?`<div class="req"><b>鈴木先生のコメント：</b>${esc(it.request)}</div>`:''}
      <p class="why">${it.type==='del'?'鈴木先生は「不要」とされました（どの版も選択なし）。':'鈴木先生はどの版も選ばず、コメントもありませんでした。'}</p>
      <div class="cols" style="--n:2">${ver(it.before,'やさしい版','easy')}${ver(it.trial,'元の新作','')}</div>`;
  }
  return `<article id="c-${it.id}" data-id="${it.id}" class="${judged(it)?'done':''}">
    <div class="head"><span class="pid">${it.id}</span><span class="chip">第${it.lec}回</span><span class="chip n">鈴木先生の選択：${esc(sel)}</span>
    ${it.type==='rerev'?(it.commented?'<span class="chip t">コメントへの対応</span>':'<span class="chip">旧版の手直し</span>'):(it.type==='del'?'<span class="chip t">削除案</span>':'<span class="chip t">保留</span>')}</div>
    ${body}
    <ul class="acts">${it.acts.map(a=>`<li>${esc(a)}</li>`).join('')}</ul>
    <div class="decide"><div class="opts">${OPTS[it.type].map(([k,l])=>`<button type="button" data-choice="${k}" aria-pressed="${d.choice===k}">${l}</button>`).join('')}</div>
    <textarea id="note-${it.id}" placeholder="直してほしい点・ご意見（任意）">${esc(d.note||'')}</textarea>
    <div class="save"><button type="button" data-save>メモを保存</button><span data-msg></span></div></div></article>`;
}
function globalOpts(){ const g=dec._settings||{}; document.querySelectorAll('#copyopts button').forEach(b=>b.setAttribute('aria-pressed', g.copies===b.dataset.copy)); }
function render(){ filters(); globalOpts(); document.getElementById('list').innerHTML=ITEMS.filter(visible).map(card).join('')||'<p>該当する問題はありません。</p>'; tally();
  if(!canWrite) document.querySelectorAll('.decide button,.decide textarea,#copyopts button').forEach(e=>e.disabled=true); }
async function save(id, patch, msgEl){
  dec[id]=Object.assign({},dec[id]||{},patch);
  if(!db||!canWrite) return;
  try{ await db.collection(COLL).doc(id).set(Object.assign({choice:null,note:''},dec[id],{updatedAt:new Date().toISOString()}));
       if(msgEl) msgEl.textContent='保存しました'; }
  catch(e){ if(msgEl) msgEl.textContent='保存できませんでした（'+(e&&e.code||'不明')+'）'; }
}
function rerender(id){ const it=ITEMS.find(x=>x.id===id); const el=document.getElementById('c-'+id); if(!it||!el) return;
  const note=document.getElementById('note-'+id)?.value; el.outerHTML=card(it);
  if(note!=null) document.getElementById('note-'+id).value=note; tally(); }
document.addEventListener('click',e=>{
  const t=e.target.closest('button'); if(!t) return;
  if(t.dataset.f){ filter=t.dataset.f; render(); return; }
  if(t.dataset.copy){ const c=(dec._settings&&dec._settings.copies===t.dataset.copy)?null:t.dataset.copy;
    save('_settings',{copies:c},document.querySelector('[data-gmsg]')); globalOpts(); return; }
  const box=t.closest('article[data-id]'); if(!box) return; const id=box.dataset.id;
  if(t.dataset.choice){ const c=(dec[id]?.choice===t.dataset.choice)?null:t.dataset.choice;
    save(id,{choice:c,note:document.getElementById('note-'+id).value},box.querySelector('[data-msg]')); rerender(id); return; }
  if(t.hasAttribute('data-save')){ save(id,{note:document.getElementById('note-'+id).value},box.querySelector('[data-msg]')); }
});
planTable(); checks(); render();
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
checks = [
  '問題の形が変わるもの：F232 は鈴木先生ご指定の5肢だと正しい文が3つになるため「誤っているのはどれか。2つ選べ」に、F241（発展版）は正答だった肢2を旧版の誤りの肢に替えたため「1つ選べ」に、F469 はご指定どおり「2つ選べ」にしました。',
  'F249：表の画像を文中の表にし、基準値を日本臨床検査標準協議会（JCCLS）の共用基準範囲（男性）にそろえました（画像のHbは女性の値でした）。',
  'F660（発展版）：入れ替えた肢2「血中ビタミンB1濃度の結果を待ってから投与する」は臨床の一般的な内容で、公的資料・学会資料での確認ができていません。',
  'F231：肢5「腸内細菌によって合成されるため欠乏症は現れにくい」（ご指定の文）の解説は、食事摂取基準で確かめられる範囲（B1は食事からとる必要があり貯蔵量が少ない）で書きました。',
  'F1417（新作・ビタミンD欠乏の予防）とF475（鉄欠乏性貧血）は、鈴木先生が版を選ばず、コメントもありませんでした。F475 は変更なしの問題なので今のままにします。F1417 は下の「保留」のカードでご判断ください。',
  '旧版を選ばれた問題で、以前の診断で指摘していた弱い攪乱肢（「起こらない」「報告されていない」「不要である」などの言い切り）は、選ばれた版を尊重して残しました（各問題の注意書きを参照）。',
]
out = html.replace('__DATA__', json.dumps(items, ensure_ascii=False).replace('</', '<\\/')) \
    .replace('__PLAN__', json.dumps(plan, ensure_ascii=False).replace('</', '<\\/')) \
    .replace('__CHECKS__', json.dumps(checks, ensure_ascii=False)) \
    .replace('__NCMT__', str(n_cmt)).replace('__NRR__', str(n_rerev)).replace('__NCOPY__', str(n_copy_del))
open(B + 'kokushi_rerev23/page/review_rerev23.html', 'w').write(out)
print('ok', len(items), n_cmt, n_rerev, n_copy_del, len(out))
