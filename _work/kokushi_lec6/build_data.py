"""確認ページ用データ（page2/data.json）を作る。kokushi_lec6 で実行。"""
import json, os, shutil
R = '/home/claude/eisei_yakugaku'
os.makedirs('page2/img', exist_ok=True)
fq = {json.loads(l)['problem_id']: json.loads(l) for l in open(f'{R}/future_questions.jsonl')}
pq = {}
for l in open(f'{R}/hygiene_with_images_v4.jsonl'):
    q = json.loads(l); pq[q['problem_id']] = q
lm = json.load(open(f'{R}/lecture_map.json'))['衛I']['lectures']['6']['ids']
ev = {json.loads(l)['id']: json.loads(l) for l in open('existing_eval.jsonl')}
old = {x['id']: x for x in json.load(open('page/lec6_data.json'))}
new = json.load(open('new40_fixed.json'))
fixlog = json.load(open('fix_log.json'))
v = {x['tmp_id']: x for f in ['verify_new_1.json', 'verify_new_2.json'] for x in json.load(open(f))}

def img_of(q):
    a = q.get('assets') or []
    if not a: return None
    src = f'{R}/{a[0]}' if os.path.exists(f'{R}/{a[0]}') else None
    if not src: return None
    name = os.path.basename(src); shutil.copy(src, f'page2/img/{name}'); return f'img/{name}'

def qv(q):
    return {'text': q['problem_text'], 'choices': q['choices'], 'answer': q['answer'], 'comment': q.get('comment', ''), 'section': q.get('section', '')}

def ovl(tid):
    o = v[tid].get('overlap_with_oct8') or []
    ids = []
    for k in o:
        b = k.split('_')[0]
        lab = {'easy': 'やさしい版', 'advanced': '発展版'}.get(k.split('_')[-1], '') if '_' in k else ''
        ids.append(f'{b}{("の" + lab) if lab else ""}')
    return ids

items = []
for i, q in enumerate(new):
    nid = f'NEW{i+1:02d}'
    cons = list(q.get('concerns') or [])
    ov = ovl(q['tmp_id'])
    if ov: cons.append('10月8日の見直し案と論点が近い問題：' + '、'.join(ov) + '（どちらか一方でよければ、片方を「採用しない」に）')
    items.append(dict(id=nid, tmp=q['tmp_id'], group='new', topic=q.get('topic', ''), **qv(q),
                      note=q.get('design_note', ''), sources=q.get('sources', []), concerns=cons,
                      checked='検証係が独立に解いた正答と一致' + ('。検証後に直した点：' + ' / '.join(fixlog[q['tmp_id']]) if q['tmp_id'] in fixlog else '')))

for pid in lm:
    q = fq.get(pid) or pq.get(pid)
    e = ev.get(pid, {}); o = old.get(pid)
    it = dict(id=pid, group='past' if pid[0].isdigit() else 'future', **qv(q), img=img_of(q),
              verdict=e.get('verdict'), fact_errors=e.get('fact_errors', []), quality=e.get('quality', []), fix=e.get('fix_suggestion', ''),
              dup=e.get('duplicate_of', []))
    if o and o['kind'] == 'revised':
        it['vers'] = {'easy': o['easy'], 'adv': o['rev']}
        it['oct8'] = o['note']
    elif o and o['kind'] == 'del':
        it['oct8del'] = o['note']
    items.append(it)

for k, o in old.items():
    if o['kind'] == 'pnew':
        items.append(dict(id=k, group='oct8new', **o['easy'], note=o['note'], sources=o.get('sources', [])))

json.dump(items, open('page2/data.json', 'w'), ensure_ascii=False)
import collections
print(len(items), collections.Counter(x['group'] for x in items), sum(1 for x in items if x.get('vers')), sum(1 for x in items if x.get('img')))
