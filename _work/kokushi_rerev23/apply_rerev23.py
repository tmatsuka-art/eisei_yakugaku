"""第2・3回 再改訂版を future_questions.jsonl と lecture_map.json に反映する（2026-10-09、松川先生・鈴木先生の承認）。
決定：再改訂版23問はすべて採用、不要3問（F1414・F1415・F1425）は削除、
選ばれなかった発展版のコピーは削除、F1417 はやさしい版を使う。
python3 apply_rerev23.py [--apply]
"""
import json, sys, copy, shutil
R = '/home/claude/eisei_yakugaku/'
W = R + '_work/kokushi_rerev23/'
APPLY = '--apply' in sys.argv
rows = [json.loads(l) for l in open(R + 'future_questions.jsonl')]
idx = {r['problem_id']: r for r in rows}
plan = {p['id']: p for p in json.load(open(W + 'apply_plan.json'))}
rerev = {x['id']: x for x in json.load(open(W + 'rerev_draft.json'))}
log = json.load(open(R + '_work/kokushi_easy/apply_log_lec23.json'))
copy_of = {o: n for o, a, n in log if a == '発展'}
added = {o: n for o, a, n in log if a == 'add'}
TODAY = '2026-10-09'
delete, new_rows, after, report = set(), [], {}, []

def set_content(r, x, summary, batch='kokushi_rerev23'):
    r['problem_text'] = x['problem_text']; r['choices'] = x['choices']; r['answer'] = x['answer']
    r['comment'] = x['comment']; r['section'] = x['section']; r['has_explanation'] = True
    if x.get('drop_image'):
        r['text_only'] = True; r['num_images'] = 0; r['num_images_detected'] = 0; r['assets'] = []
    lec = (r.get('ai_review') or {}).get('lecture')
    r['ai_review'] = {'status': 'approved_rewrite', 'reviewed_at': TODAY, 'lecture': lec, 'batch': batch,
                      'changes_summary': [summary]}

def take_from(dst, src, summary):
    """src レコードの問題内容を dst（元の番号）へ移す。"""
    for k in ('problem_text', 'choices', 'answer', 'comment', 'section', 'new_corecurri_code', 'note'):
        if k in src: dst[k] = copy.deepcopy(src[k])
    lec = (dst.get('ai_review') or {}).get('lecture') or (src.get('ai_review') or {}).get('lecture')
    dst['ai_review'] = {'status': 'approved_rewrite', 'reviewed_at': TODAY, 'lecture': lec,
                        'batch': 'kokushi_rerev23', 'changes_summary': [summary]}
    if dst.get('tags'): dst['tags'] = [t for t in dst['tags'] if t != '発展']

next_no = max(int(r['problem_id'][1:]) for r in rows) + 1
for i, p in plan.items():
    if not p['touched'] or p['main'] == '今のまま':
        continue
    r = idx[i]; vs = p['sel']; rr = rerev.get(i)
    if p['kind'] == 'new':
        if p['main'] == '削除':
            delete.add(i); report.append(f'{i} 削除（鈴木先生：不要）')
            if i in added: delete.add(added[i]); report.append(f'{added[i]} 削除（{i}のやさしい版）')
        elif p['main'] == '保留':      # F1417 → 松川先生のご判断でやさしい版を使う
            take_from(r, idx[added[i]], 'やさしい版を採用（元の新作と入れ替え）'); delete.add(added[i])
            report.append(f'{i} ← やさしい版（{added[i]}から移し、{added[i]}は削除）')
        elif vs == ['easy']:
            take_from(r, idx[added[i]], 'やさしい版を採用（鈴木先生の選択）'); delete.add(added[i])
            report.append(f'{i} ← やさしい版（{added[i]}から移し、{added[i]}は削除）')
        elif vs == ['rev']:
            r['ai_review'] = dict(r.get('ai_review') or {}, reviewed_at=TODAY, changes_summary=['元の新作を採用（鈴木先生の選択）'])
            if i in added: delete.add(added[i]); report.append(f'{i} 元の新作のまま／{added[i]}（やさしい版）削除')
        continue
    main = [k for k in ('easy', 'rev', 'old') if k in vs][0]
    # 元の番号
    if rr and rr['target'] == main:
        set_content(r, rr, f'再改訂版（鈴木先生のご意見を反映、{ {"easy":"やさしい版","rev":"発展版","old":"旧版"}[main]}）')
        if r.get('tags'): r['tags'] = [t for t in r['tags'] if t != '発展']
        report.append(f'{i} ← 再改訂版（{main}）')
    elif main == 'rev':
        take_from(r, idx[copy_of[i]], '発展版を採用（鈴木先生の選択）'); report.append(f'{i} ← 発展版（{copy_of[i]}から移す）')
    else:
        report.append(f'{i} やさしい版のまま')
    if i == 'F249': r['note'] = '胃全摘後のビタミンB12欠乏（実践）'
    # 発展版のコピー
    if i in copy_of:
        c = copy_of[i]
        if 'rev' in vs and main != 'rev':
            if rr and rr['target'] == 'rev':
                set_content(idx[c], rr, f'{i}の発展版の再改訂版（鈴木先生のご意見を反映）', 'kokushi_hatten')
                idx[c]['tags'] = ['発展']; report.append(f'{c} ← 発展版の再改訂版')
            else:
                report.append(f'{c} 発展版のまま')
        else:
            delete.add(c); report.append(f'{c} 削除（選ばれなかった発展版のコピー）')
    # 旧版の追加
    if 'old' in vs and main != 'old':
        nr = copy.deepcopy(r); nid = f'F{next_no}'; next_no += 1
        nr.update(problem_id=nid, q_no=int(nid[1:]), display_title=f'予想問題 {nid}')
        set_content(nr, rr, f'{i}の旧版（鈴木先生の選択で追加、書き方を手直し）')
        nr['tags'] = ['旧版']
        new_rows.append((i, nr)); after.setdefault(i, []).append(nid)
        report.append(f'{nid} ← {i}の旧版（「旧版」タグ）')

out = []
for r in rows:
    if r['problem_id'] in delete: continue
    out.append(r)
    for parent, nr in new_rows:
        if parent == r['problem_id']: pass
for parent, nr in new_rows: out.append(nr)
# lecture_map
lm = json.load(open(R + 'lecture_map.json'))
def fix(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'ids' and isinstance(v, list):
                nv = []
                for x in v:
                    if x in delete: continue
                    nv.append(x); nv.extend(after.get(x, []))
                o[k] = nv
            else: fix(v)
    elif isinstance(o, list):
        for v in o: fix(v)
fix(lm)
mapped = set();
def coll(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'ids' and isinstance(v, list): mapped.update(v)
            else: coll(v)
    elif isinstance(o, list):
        for v in o: coll(v)
coll(lm)
ids_out = {r['problem_id'] for r in out}
assert not (delete & ids_out)
assert all(n in mapped for ns in after.values() for n in ns), 'new id not in lecture_map'
assert not (delete & mapped), 'deleted id still in lecture_map'
print('\n'.join(report))
print(f'行数 {len(rows)} → {len(out)}（削除 {len(delete)}、追加 {len(new_rows)}）')
if APPLY:
    shutil.copy(R + 'future_questions.jsonl', R + 'future_questions.jsonl.bak_pre_rerev23_20261009')
    with open(R + 'future_questions.jsonl', 'w') as f:
        for r in out: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    json.dump(lm, open(R + 'lecture_map.json', 'w'), ensure_ascii=False, indent=2)
    json.dump({'deleted': sorted(delete), 'added': after, 'report': report}, open(W + 'apply_log_rerev23.json', 'w'), ensure_ascii=False, indent=1)
    print('反映しました')
