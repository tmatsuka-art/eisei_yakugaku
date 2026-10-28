"""衛生化学I 第6回（特別用途食品・保健機能食品）の判断を future_questions.jsonl・hygiene_with_images_v4.jsonl・lecture_map.json に反映する。
確認ページ https://claude.ai/artifact/1DDmzSC8bXyYFjWBgfwUcN （db collection "lec6"、2026-10-23 読み取り → db/lec6/*.json）
規則：
  今日の新作 NEW01〜40：adopt はそのまま、hold は先生のコメントで直した版（rev_hold.jsonl）を、新しい番号で追加。reject は入れない。
  10月8日の新問題 E6-xx：adopt を新しい番号で追加（lec6_final.json の easy）。
  今ある問題：keep 変更なし／fix 今日の点検の案で直した版（予想問題 fix_future.jsonl、過去問は解説だけ fix_past.jsonl）／
             easy・adv 10月8日のやさしい版・発展版で置き換え／delete 削除。
python3 apply_lec6.py [--apply]
"""
import json, sys, copy, glob, os, shutil
R = '/home/claude/eisei_yakugaku/'
W = R + '_work/kokushi_lec6/'
APPLY = '--apply' in sys.argv
TODAY = '2026-10-23'
BATCH = 'kokushi_lec6_1023'

def load(p): return [json.loads(l) for l in open(p) if l.strip()]
fut = load(R + 'future_questions.jsonl'); fidx = {r['problem_id']: r for r in fut}
past = load(R + 'hygiene_with_images_v4.jsonl'); pidx = {r['problem_id']: r for r in past}
dec = {}
for f in glob.glob(W + 'db/lec6/*.json'):
    d = json.load(open(f)); dec[os.path.basename(f)[:-5]] = d.get('data', d)
page = {x['id']: x for x in json.load(open(W + 'page2/data.json'))}
new40 = {x['tmp_id']: x for x in json.load(open(W + 'new40_fixed.json'))}
oct8 = {x['key']: x for x in json.load(open(W + 'lec6_final.json'))}
hold = {x['page_id']: x for x in load(W + 'rev_hold.jsonl')}
ffix = {x['id']: x for x in load(W + 'fix_future.jsonl')}
pfix = {x['id']: x for x in load(W + 'fix_past.jsonl')}
lm = json.load(open(R + 'lecture_map.json'))
L6 = lm['衛I']['lectures']['6']['ids']

def put(r, c, summary):
    for k in ('problem_text', 'choices', 'answer', 'comment', 'section'):
        r[k] = copy.deepcopy(c[k])
    if c.get('new_corecurri_code'): r['new_corecurri_code'] = c['new_corecurri_code']
    r['has_explanation'] = True
    if c.get('drop_image'):
        r.update(text_only=True, num_images=0, num_images_detected=0, assets=[])
    r['ai_review'] = {'status': 'approved_rewrite', 'reviewed_at': TODAY, 'lecture': '衛I-6', 'batch': BATCH, 'changes_summary': [summary]}

report, delete, new_rows, after = [], set(), [], {}
next_no = max(int(k[1:]) for k in fidx if k[1:].isdigit()) + 1
tmpl = fidx['F256']

def add_new(c, summary, tags, origin):
    global next_no
    nid = f'F{next_no}'; next_no += 1
    nr = copy.deepcopy(tmpl)
    nr.update(problem_id=nid, q_no=int(nid[1:]), display_title=f'予想問題 {nid}', text_only=True, num_images=0,
              num_images_detected=0, assets=[], note=c.get('topic') or '', tags=list(tags or []),
              source={'kind': 'ai_new', 'lecture': '衛I-6', 'origin': origin, 'added': TODAY})
    nr.pop('ai_review', None)
    put(nr, c, summary)
    new_rows.append(nr); return nid

# 今ある問題
for pid in list(L6):
    d = dec.get(pid) or {}; ch = d.get('choice')
    if ch == 'delete':
        delete.add(pid); report.append(f'{pid} 削除'); continue
    if ch == 'keep' or not ch or ch == 'hold':
        report.append(f'{pid} 変更なし'); continue
    if ch in ('easy', 'adv'):
        c = oct8[f'{pid}_{"easy" if ch == "easy" else "advanced"}']
        lab = 'やさしい版' if ch == 'easy' else '発展版'
        put(fidx[pid], c, f'10月8日の{lab}に置き換え（10月23日の確認ページで選択）')
        for t in c.get('tags') or []:
            if t not in (fidx[pid].get('tags') or []): fidx[pid].setdefault('tags', []).append(t)
        report.append(f'{pid} ← 10月8日の{lab}'); continue
    if ch == 'fix':
        if pid in pidx:
            pidx[pid]['comment'] = pfix[pid]['comment']
            pidx[pid]['ai_review'] = {'status': 'approved_rewrite', 'reviewed_at': TODAY, 'lecture': '衛I-6', 'batch': BATCH,
                                      'changes_summary': ['解説を修正（問題文・選択肢・正答は変更なし）：' + pfix[pid]['change_note']]}
            report.append(f'{pid} 過去問の解説を修正')
        else:
            c = ffix[pid]; put(fidx[pid], c, '点検の案で修正：' + c['change_note'])
            report.append(f'{pid} 修正' + ('（図を使わない形に）' if c.get('drop_image') else ''))
        continue
    report.append(f'!! {pid} 判断 {ch} を処理できない')

# 今日の新作
for i in range(1, 41):
    k = f'NEW{i:02d}'; ch = (dec.get(k) or {}).get('choice'); t = page[k]['tmp']
    if ch == 'adopt':
        c = new40[t]; nid = add_new(c, f'新作（{t}、10月23日採用）', c.get('tags'), t)
        report.append(f'{nid} ← 新作{t}（採用）')
    elif ch == 'hold':
        c = hold[k]; nid = add_new(c, f'新作（{t}、先生のコメントで修正：{c["change_note"]}）', new40[t].get('tags'), t)
        report.append(f'{nid} ← 新作{t}（コメントで修正）')
    after.setdefault('new', [])
# 10月8日の新問題
for k in sorted(x for x in dec if x.startswith('E6-')):
    if dec[k].get('choice') == 'adopt':
        c = oct8[f'{k}_easy']; nid = add_new(c, f'10月8日の新問題{k}（10月23日採用）', c.get('tags'), k)
        report.append(f'{nid} ← 10月8日の新問題{k}')

added = [r['problem_id'] for r in new_rows]
assert not (set(added) & set(fidx))
out = [r for r in fut if r['problem_id'] not in delete] + new_rows
lm['衛I']['lectures']['6']['ids'] = [x for x in L6 if x not in delete] + added
print('\n'.join(report))
print(f'予想問題 {len(fut)} → {len(out)}（削除 {len(delete)}、追加 {len(added)}）、第6回 {len(L6)} → {len(lm["衛I"]["lectures"]["6"]["ids"])} 問')
if APPLY:
    for p in ('future_questions.jsonl', 'hygiene_with_images_v4.jsonl', 'lecture_map.json'):
        shutil.copy(R + p, R + p + '.bak_pre_lec6_20261023')
    with open(R + 'future_questions.jsonl', 'w') as f:
        for r in out: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    with open(R + 'hygiene_with_images_v4.jsonl', 'w') as f:
        for r in past: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    json.dump(lm, open(R + 'lecture_map.json', 'w'), ensure_ascii=False, indent=2)
    json.dump({'deleted': sorted(delete), 'added': added, 'report': report}, open(W + 'apply_log_lec6.json', 'w'), ensure_ascii=False, indent=1)
    print('反映しました')
