"""バッチ26 対象20問を精密監査。結果をファイルに書き出す（文字化け回避）。
- 各攪乱肢（正答除く）の絶対化ヒットを scan_quality.py と同一ロジックで列挙
- 「2つ選べ」で解説に正答注記（=正答以外に正しい選択肢の疑い）がある問題を検出
"""
import json
import re
from pathlib import Path

ABS_QUANT = ['のみ', 'だけ', '全く', '必ず', '絶対', 'すべて', 'あらゆる']
ABS_TIME = ['直ちに', 'ただちに', '即座に', '常に', '決して', '最優先で']
ABS_DUTY = ['しなければならない', 'すべきではない', '義務がある', '禁じられている']
ABS_NEG_PATTERNS = [
    r'存在しない', r'認められていない', r'含まれない[。\s]?$', r'設定されていない',
    r'設けられていない', r'規定されていない', r'指定されていない', r'対象では?ない',
    r'関係(?:が)?ない', r'影響(?:が|は)?ない', r'必要(?:が|は)?ない',
    r'問題(?:が|は)?ない', r'関与しない', r'効果(?:が|は)?ない',
]


def scan_absolute(text):
    hits = []
    for kw in ABS_QUANT + ABS_TIME + ABS_DUTY:
        if kw in text:
            hits.append(kw)
    for pat in ABS_NEG_PATTERNS:
        m = re.search(pat, text)
        if m:
            hits.append(m.group(0))
    return hits


IDS = ['F1208','F1212','F1213','F1217','F1218','F1228','F1234','F1244','F1245','F1248',
       'F1253','F1262','F1264','F1278','F1287','F1306','F1314','F1318','F1336','F1338']

qs = {}
for line in open('future_questions.jsonl', encoding='utf-8'):
    if line.strip():
        q = json.loads(line)
        qs[q['problem_id']] = q

out = []
for pid in IDS:
    q = qs[pid]
    ans = {int(a) for a in (q.get('answer') or []) if str(a).isdigit()}
    comment = q.get('comment', '') or ''
    # 構造問題の検出：解説に「正答以外が正しい」ことを示す注記
    struct_flag = ('本問の正答' in comment) or ('正ではない' in comment)
    out.append(f'=== {pid}  正答{sorted(ans)} {"<<構造注記あり>>" if struct_flag else ""}')
    distractor_hits = []
    for i, c in enumerate(q.get('choices', []) or [], 1):
        tag = '★正答' if i in ans else '  攪乱'
        h = scan_absolute(c) if i not in ans else []
        hh = ('  [絶対化: ' + '/'.join(h) + ']') if h else ''
        out.append(f'  {tag}選{i}: {c}{hh}')
        if h:
            distractor_hits.append(i)
    out.append(f'  → 改修すべき攪乱肢: {distractor_hits if distractor_hits else "なし（誤抽出）"}')
    out.append('')

Path('_work/audit_batch26_result.txt').write_text('\n'.join(out), encoding='utf-8')
print('wrote _work/audit_batch26_result.txt')
