"""第6回（74問、10月23日反映後）の再確認ページ（2026-10-28）。kokushi_lec6 で実行 → page3/review_lec6_v3.html
判断は db collection "lec6v3"：choice = ok / fix / delete / hold、note = コメント。"""
import json, os, shutil
R = '/home/claude/eisei_yakugaku/'
os.makedirs('page3/img', exist_ok=True)
fq = {json.loads(l)['problem_id']: json.loads(l) for l in open(R + 'future_questions.jsonl')}
pq = {json.loads(l)['problem_id']: json.loads(l) for l in open(R + 'hygiene_with_images_v4.jsonl')}
L = json.load(open(R + 'lecture_map.json'))['衛I']['lectures']['6']
items = []
for pid in L['ids']:
    past = pid in pq; q = pq[pid] if past else fq[pid]
    img = None
    if q.get('assets'):
        src = R + q['assets'][0]
        if os.path.exists(src):
            img = 'img/' + os.path.basename(src); shutil.copy(src, 'page3/' + img)
    num = int(pid[1:]) if pid.startswith('F') else 0
    kind = 'past' if past else ('new' if num >= 1538 else 'future')
    ch = (q.get('ai_review') or {}).get('changes_summary') or []
    items.append(dict(id=pid, kind=kind, text=q['problem_text'], choices=q['choices'], answer=q['answer'],
                      comment=q.get('comment', ''), section=q.get('section', ''), img=img,
                      change=ch[0] if ch and (q.get('ai_review') or {}).get('reviewed_at', '') >= '2026-10-08' else ''))
items.sort(key=lambda x: ['past', 'future', 'new'].index(x['kind']))
src = open(R + '_work/kokushi_brush45/page/src_lec45.html').read()
css = src[src.index('<style>'):src.index('</style>') + 8].replace('</style>', '''.sec{font-family:var(--f-head);font-size:1.15rem;margin:8px 0 0}
.chg{font-size:.82rem;color:var(--muted)}
</style>''')
body = r'''<div class="wrap">
<header><h1>第6回 特別用途食品・保健機能食品 再確認</h1>
<p class="lead">衛生化学I 第6回の今の74問（10月23日に先生方の判断を反映した版）です。不具合のある問題に「直す」または「削除する」を選び、どこをどう直すかをコメント欄に書いてください。書いた内容は自動で保存されます。</p></header>
<section class="box"><h2>使い方</h2>
<p>問題ごとに「このままでよい」「直す」「削除する」「保留」のどれかを押してください。「直す」のときは、どの選択肢・解説をどう直すかをコメント欄に書き、「コメントを保存」を押してください。全部の問題に判断を入れなくてもかまいません。判断のない問題は、今のまま残します。</p>
<p>正解の選択肢は緑色で表示しています。解説は「解説」を押すと開きます。</p></section>
<div class="filters" id="filters"></div>
<div class="tally" id="tally"></div>
<p class="ro" id="dbstate" hidden></p>
<div id="list" style="display:grid;gap:16px"></div>
</div>
<script id="data" type="application/json">__DATA__</script>
<script>
const ITEMS = JSON.parse(document.getElementById('data').textContent);
const COLL='lec6v3'; const dec={}; let db=null, canWrite=true, filter='all';
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const BTN=[['ok','このままでよい'],['fix','直す'],['delete','削除する'],['hold','保留']];
const LBL=Object.fromEntries(BTN);
const KIND={past:'過去問',future:'予想問題',new:'新しく加えた予想問題（F1538〜）'};
const SEC={past:'過去問（問題文は本試験のまま。解説を直せます）',future:'予想問題（もとからある問題）',new:'新しく加えた予想問題（10月23日）'};
function card(it,i){ const d=dec[it.id]||{}; const a=new Set(it.answer||[]);
  return `<article id="c-${it.id}" class="${d.choice?'done':''}" data-id="${it.id}">
   <div class="head"><span class="pid">${esc(it.id)}</span><span class="chip">${i}／${ITEMS.length}</span><span class="chip ${it.kind==='new'?'n':''}">${KIND[it.kind]}</span>
   <span class="chip">${esc((it.section?it.section+'・':'')+((it.answer||[]).length===2?'2つ選べ':'1つ選べ'))}</span></div>
   ${it.change?`<p class="chg">今回の見直しで：${esc(it.change)}</p>`:''}
   <div class="ver"><p class="stem">${esc(it.text)}</p>${it.img?`<img src="${esc(it.img)}" alt="問題の図" style="max-width:100%;background:#fff;border:1px solid var(--line);border-radius:4px">`:''}
    <ol class="ch">${(it.choices||[]).map((c,k)=>`<li class="${a.has(String(k+1))?'ok':''}"><span>${k+1}</span><span>${esc(c)}</span></li>`).join('')}</ol>
    <details><summary>解説</summary><p class="cm">${esc(it.comment)}</p></details></div>
   <div class="outcome">${d.choice?'判断：'+esc(LBL[d.choice]):'未判断'}</div>
   <div class="decide"><div class="opts" role="group" aria-label="判断">${BTN.map(([k,l])=>`<button type="button" data-choice="${k}" aria-pressed="${d.choice===k}">${l}</button>`).join('')}</div>
    <textarea id="note-${it.id}" placeholder="直す点・コメント（例：選択肢3を「〜」に。解説2の「〜」は誤り）">${esc(d.note||'')}</textarea>
    <div class="save"><button type="button" data-save>コメントを保存</button><span data-msg></span></div></div></article>`; }
function visible(it){ const d=dec[it.id]||{}; if(['past','future','new'].includes(filter)) return it.kind===filter;
  if(filter==='todo') return !d.choice; if(filter==='marked') return d.choice==='fix'||d.choice==='delete'||!!d.note; return true; }
function render(){ const F=[['all','すべて'],['past','過去問'],['future','予想問題'],['new','新しく加えた問題'],['marked','直す・削除・コメントあり'],['todo','未判断']];
  document.getElementById('filters').innerHTML=F.map(([k,l])=>`<button type="button" data-f="${k}" aria-pressed="${filter===k}">${l}</button>`).join('');
  let h='', last=null; ITEMS.forEach((it,i)=>{ if(!visible(it)) return; if(it.kind!==last){ h+=`<h2 class="sec">${SEC[it.kind]}</h2>`; last=it.kind; } h+=card(it,i+1); });
  document.getElementById('list').innerHTML=h||'<p>該当する問題はありません。</p>'; tally();
  if(!canWrite) document.querySelectorAll('.decide button,.decide textarea').forEach(e=>e.disabled=true); }
function tally(){ const c=k=>ITEMS.filter(x=>(dec[x.id]||{}).choice===k).length;
  document.getElementById('tally').innerHTML=`<span>全${ITEMS.length}問</span><span>このままでよい ${c('ok')}</span><span>直す ${c('fix')}</span><span>削除 ${c('delete')}</span><span>保留 ${c('hold')}</span><span>コメントあり ${ITEMS.filter(x=>(dec[x.id]||{}).note).length}</span>`; }
async function save(id,patch,msg){ dec[id]=Object.assign({},dec[id]||{},patch); if(!db||!canWrite) return;
  try{ await db.collection(COLL).doc(id).set(Object.assign({choice:null,note:''},dec[id],{updatedAt:new Date().toISOString()})); if(msg) msg.textContent='保存しました'; }
  catch(e){ if(msg) msg.textContent='保存できませんでした（'+(e&&e.code||'不明')+'）。もう一度押してください。'; } }
function rerender(id){ const i=ITEMS.findIndex(x=>x.id===id); const el=document.getElementById('c-'+id); if(i<0||!el) return;
  const note=document.getElementById('note-'+id)?.value; el.outerHTML=card(ITEMS[i],i+1); if(note!=null) document.getElementById('note-'+id).value=note; tally(); }
document.addEventListener('click',e=>{ const t=e.target.closest('button'); if(!t) return;
  if(t.dataset.f){ filter=t.dataset.f; render(); return; }
  const box=t.closest('article[data-id]'); if(!box) return; const id=box.dataset.id;
  if(t.dataset.choice){ const c=(dec[id]?.choice===t.dataset.choice)?null:t.dataset.choice;
    const note=document.getElementById('note-'+id).value; save(id,{choice:c,note},box.querySelector('[data-msg]')); rerender(id); return; }
  if(t.hasAttribute('data-save')) save(id,{note:document.getElementById('note-'+id).value},box.querySelector('[data-msg]')); });
render();
(async()=>{ try{ db=await window.claude.use('db');
  if(!db){ const s=document.getElementById('dbstate'); s.hidden=false; s.textContent='判断の保存は、claude.ai にサインインして開いたときに使えます。'; canWrite=false; render(); return; }
  db.collection(COLL).onSnapshot(snap=>{ snap.docs.forEach(d=>{ dec[d.id]=d.data(); });
    const act=document.activeElement&&document.activeElement.tagName==='TEXTAREA'; if(!act) render(); else tally(); },()=>{});
 }catch(e){ const s=document.getElementById('dbstate'); s.hidden=false; s.textContent='判断を保存する機能に接続できませんでした。ページを開き直してください。'; } })();
</script>'''
html = '<title>第6回 再確認</title>\n' + css + '\n' + body.replace('__DATA__', json.dumps(items, ensure_ascii=False).replace('</', '<\\/'))
open('page3/review_lec6_v3.html', 'w').write(html)
import collections
print(len(items), collections.Counter(x['kind'] for x in items), [x['img'] for x in items if x['img']])
