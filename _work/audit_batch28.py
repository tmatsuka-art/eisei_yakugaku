"""バッチ28 対象7問を精密監査。選択肢＋絶対化ヒット＋解説を文字化け回避でファイル出力。
絶対化シリーズの最終バッチ。F1223型（絶対化語を外すと攪乱肢が正答化）を見抜くため全選択肢・解説を確認。
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


IDS = ['F1389', 'F1394', 'F1395', 'F1397', 'F1400', 'F1406', 'F1411']

qs = {}
for line in open('future_questions.jsonl', encoding='utf-8'):
    if line.strip():
        q = json.loads(line)
        qs[q['problem_id']] = q

out = []
for pid in IDS:
    q = qs[pid]
    ans = {int(a) for a in (q.get('answer') or []) if str(a).isdigit()}
    out.append(f'=== {pid}  正答{sorted(ans)}  「{q.get("problem_text", "")}」')
    distractor_hits = []
    for i, c in enumerate(q.get('choices', []) or [], 1):
        tag = '★正答' if i in ans else '  攪乱'
        h = scan_absolute(c) if i not in ans else []
        hh = ('  [絶対化: ' + '/'.join(h) + ']') if h else ''
        out.append(f'  {tag}選{i}: {c}{hh}')
        if h:
            distractor_hits.append(i)
    out.append(f'  → 絶対化ヒット攪乱肢: {distractor_hits}')
    out.append('  --- 解説 ---')
    out.append('  ' + (q.get('comment', '') or '').replace('\n', '\n  '))
    out.append('')

Path('_work/audit_batch28_result.txt').write_text('\n'.join(out), encoding='utf-8')
print('wrote _work/audit_batch28_result.txt', len(IDS), 'problems')
