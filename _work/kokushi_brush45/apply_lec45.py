"""衛生化学I 第4・5回 見直し版を future_questions.jsonl と lecture_map.json に反映する（2026-10-15、松川先生の選択）。
確認ページ https://claude.ai/artifact/R4jXexFTm6kqV5E7UnPzdE （db collection "lec45"）の判断を読む。
規則（ページの「判断のしかた」と同じ）：
  元の問題番号には、選んだ版のうち やさしい版 → 改訂版（発展） → 旧版 の順で最初のものを入れ、
  残りは新しい番号（F1500〜）で追加する（「発展」「旧版」のタグ付き）。何も選ばない・保留は変更しない。
  第4回：今のデータは改訂版（発展）。第5回：今のデータは旧版。
  第5回の新問題（F1437〜F1445）は未反映なので、選ばれた版をその番号で追加する。
  削除案の承認は削除、移動案の承認は lecture_map の公衆第7回へ移す。
python3 apply_lec45.py [--apply]
"""
import json, sys, copy, glob, os, shutil
R = '/home/claude/eisei_yakugaku/'
W = R + '_work/kokushi_brush45/'
APPLY = '--apply' in sys.argv
TODAY = '2026-10-15'
LABEL = {'easy': 'やさしい版', 'rev': '改訂版（発展）', 'old': '旧版'}

rows = [json.loads(l) for l in open(R + 'future_questions.jsonl') if l.strip()]
idx = {r['problem_id']: r for r in rows}
items = {x['id']: x for x in json.load(open(W + 'page/lec45_data.json'))}
dec = {}
for f in glob.glob(W + 'db/lec45/*.json'):
    d = json.load(open(f)); dec[os.path.basename(f)[:-5]] = d.get('data', d)
merged = json.load(open(W + 'merged.json'))
src_easy = {}
for f in ('easy4_final.json', 'easy5_final.json'):
    for x in json.load(open(R + '_work/kokushi_easy/' + f)): src_easy[x['problem_id']] = x
for l in open(R + '_work/kokushi_easy/pilot_easy.jsonl'):
    x = json.loads(l); src_easy.setdefault(x['problem_id'], x)
rev5 = {json.loads(l)['problem_id']: json.loads(l) for l in open(R + '_work/kokushi_lec5/final_lec5.jsonl')}


def easy_content(i):
    e = merged[i]['easy']; s = src_easy.get(i, {})
    return {'problem_text': e['problem_text'], 'choices': e['choices'], 'answer': e['answer'], 'comment': e['comment'],
            'section': e.get('section') or s.get('section'), 'new_corecurri_code': s.get('new_corecurri_code'),
            'drop_image': bool(s.get('drop_image')), 'tags': s.get('tags') or []}


def rev5_content(i):
    s = rev5[i]
    return {k: s.get(k) for k in ('problem_text', 'choices', 'answer', 'comment', 'section', 'new_corecurri_code')} | \
        {'drop_image': bool(s.get('drop_image')), 'image': s.get('image'), 'tags': s.get('tags') or []}


def row_content(r):
    return {k: copy.deepcopy(r.get(k)) for k in ('problem_text', 'choices', 'answer', 'comment', 'section', 'new_corecurri_code')} | \
        {'drop_image': False, 'tags': [t for t in (r.get('tags') or []) if t not in ('発展', '旧版')], 'keep_assets': True}


def put(r, c, lec, summary, batch='kokushi_brush45'):
    for k in ('problem_text', 'choices', 'answer', 'comment', 'section'):
        r[k] = copy.deepcopy(c[k])
    if c.get('new_corecurri_code'): r['new_corecurri_code'] = c['new_corecurri_code']
    r['has_explanation'] = True
    if c.get('drop_image'):
        r['text_only'] = True; r['num_images'] = 0; r['num_images_detected'] = 0; r['assets'] = []
    r['ai_review'] = {'status': 'approved_rewrite', 'reviewed_at': TODAY, 'lecture': f'衛I-{lec}', 'batch': batch,
                      'changes_summary': [summary]}


next_no = max(int(k[1:]) for k in idx if k[1:].isdigit()) + 1
assert next_no >= 1500
delete, moves, new_rows, after, report, images = set(), [], [], {}, [], []


def add_copy(parent, c, lec, tag, summary):
    global next_no
    nid = f'F{next_no}'; next_no += 1
    nr = copy.deepcopy(idx[parent]) if parent in idx else copy.deepcopy(idx['F1361'])
    nr.update(problem_id=nid, q_no=int(nid[1:]), display_title=f'予想問題 {nid}')
    if not c.get('keep_assets') and not c.get('image'):
        nr.update(text_only=True, num_images=0, num_images_detected=0, assets=[])
    put(nr, c, lec, summary)
    nr['tags'] = [t for t in (c.get('tags') or []) if t not in ('発展', '旧版')] + [tag]
    new_rows.append(nr); after.setdefault(parent, []).append(nid)
    return nid


for i, it in items.items():
    d = dec.get(i) or {}
    lec = it['lec']; kind = it['kind']
    if kind == 'del':
        if d.get('choice') == 'delete':
            delete.add(i); report.append(f'{i} 削除（削除案を承認）')
        continue
    if kind == 'move':
        if d.get('choice') == 'move':
            moves.append(i); report.append(f'{i} 公衆衛生学 第7回へ移動（内容は変えない）')
        continue
    vs = d.get('versions') or []
    if d.get('choice') != 'versions' or not vs:
        report.append(f'{i} 変更なし（{"保留" if d.get("choice") == "hold" else "未選択"}）'); continue
    main = [k for k in ('easy', 'rev', 'old') if k in vs][0]

    if kind == 'new5':      # 第5回の新問題：まだデータにない → その番号で追加
        c = easy_content(i) if main == 'easy' else rev5_content(i)
        nr = copy.deepcopy(idx['F1361'])
        nr.update(problem_id=i, q_no=int(i[1:]), display_title=f'予想問題 {i}', text_only=True, num_images=0,
                  num_images_detected=0, assets=[], note='', corecurri_code=nr.get('corecurri_code'))
        put(nr, c, lec, f'新問題（{LABEL[main] if main == "easy" else "元の新問題"}を採用）')
        nr['tags'] = list(c.get('tags') or [])
        new_rows.append(nr); after.setdefault('__lec5_new__', []).append(i)
        report.append(f'{i} 追加（新問題・{"やさしい版" if main == "easy" else "元の新問題"}）')
        if main == 'easy' and 'rev' in vs:
            nid = add_copy(i, rev5_content(i), lec, '発展', f'{i}の元の新問題（「発展」として追加）')
            report.append(f'{nid} ← {i}の元の新問題（「発展」タグ）')
        continue

    r = idx[i]
    cur = 'rev' if lec == 4 else 'old'          # 今のデータの版
    if kind == 'new': cur = 'rev'
    cur_c = row_content(r)
    if main == cur:
        report.append(f'{i} 今の版（{LABEL[cur] if kind != "new" else "元の新作"}）のまま')
    else:
        c = easy_content(i) if main == 'easy' else rev5_content(i)
        put(r, c, lec, f'{LABEL[main]}を採用（10月15日の確認ページで選択）')
        if r.get('tags'): r['tags'] = [t for t in r['tags'] if t not in ('発展', '旧版')]
        for t in c.get('tags') or []:
            if t not in (r.get('tags') or []): r.setdefault('tags', []).append(t)
        if c.get('image'): images.append((i, c['image']))
        report.append(f'{i} ← {LABEL[main]}')
    # 残りの版を追加
    for v in ('rev', 'old'):
        if v in vs and v != main:
            if v == cur: c = cur_c
            elif v == 'rev': c = rev5_content(i)
            else: c = None
            if c is None:
                report.append(f'!! {i} の {v} の内容が見つからない'); continue
            tag = '発展' if v == 'rev' else '旧版'
            nid = add_copy(i, c, lec, tag, f'{i}の{LABEL[v]}（「{tag}」として追加、10月15日の選択）')
            report.append(f'{nid} ← {i}の{LABEL[v]}（「{tag}」タグ）')

# 旧版を残す場合、旧版の誤りが指摘されている問題は知らせる
olderr = json.load(open(W + 'page/extra.json'))['old_err_all']
for i, it in items.items():
    vs = (dec.get(i) or {}).get('versions') or []
    if 'old' in vs and i in olderr:
        report.append(f'要確認：{i} の旧版を残すが、旧版の誤りの指摘あり → {olderr[i][0][:60]}…')

ids_new = {r['problem_id'] for r in new_rows}
assert not (ids_new & set(idx)), ids_new & set(idx)
out = [r for r in rows if r['problem_id'] not in delete] + new_rows

lm = json.load(open(R + 'lecture_map.json'))
L5 = lm['衛I']['lectures']['5']['ids']; P7 = lm['公衆']['lectures']['7']['ids']
for k in ('4', '5'):
    ids = lm['衛I']['lectures'][k]['ids']; nv = []
    for x in ids:
        if x in delete or x in moves: continue
        nv.append(x); nv.extend(after.get(x, []))
    if k == '5':
        for x in after.get('__lec5_new__', []):
            nv.append(x); nv.extend(after.get(x, []))
    lm['衛I']['lectures'][k]['ids'] = nv
for x in moves:
    if x not in P7: P7.append(x)

mapped = set()
def coll(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'ids' and isinstance(v, list): mapped.update(v)
            else: coll(v)
    elif isinstance(o, list):
        for v in o: coll(v)
coll(lm)
assert ids_new <= mapped, ids_new - mapped
assert not (delete & mapped)
print('\n'.join(report))
print(f'行数 {len(rows)} → {len(out)}（削除 {len(delete)}、追加 {len(new_rows)}、移動 {len(moves)}）')
print('図の差し替え:', images)
if APPLY:
    shutil.copy(R + 'future_questions.jsonl', R + 'future_questions.jsonl.bak_pre_brush45_20261015')
    shutil.copy(R + 'lecture_map.json', R + 'lecture_map.json.bak_pre_brush45_20261015')
    with open(R + 'future_questions.jsonl', 'w') as f:
        for r in out: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    json.dump(lm, open(R + 'lecture_map.json', 'w'), ensure_ascii=False, indent=2)
    for i, img in images:
        shutil.copy(R + img, R + f'FUTURE/{i}.png')
    json.dump({'deleted': sorted(delete), 'moved': moves, 'added': after, 'images': images, 'report': report},
              open(W + 'apply_log_lec45.json', 'w'), ensure_ascii=False, indent=1)
    print('反映しました')
