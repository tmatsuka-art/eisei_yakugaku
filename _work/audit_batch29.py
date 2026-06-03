"""バッチ29 評論的修飾の一掃。対象5問の選択肢＋絶対化/評論ヒット＋解説をファイル出力。
評論的修飾（比較的/概ね/やや等）を具体的表現に置換するための確認用。F691は年代の事実誤りも要確認。
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
EVAL_WORDS = ['比較的', '概ね', '相当に', '割と', 'やや', 'かなり', 'ある程度']


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


def scan_eval(text):
    return [w for w in EVAL_WORDS if w in text]


IDS = ['F215', 'F265', 'F691', 'F1210', 'F1300']

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
    for i, c in enumerate(q.get('choices', []) or [], 1):
        tag = '★正答' if i in ans else '  攪乱'
        marks = []
        if i not in ans:
            ah = scan_absolute(c)
            eh = scan_eval(c)
            if ah:
                marks.append('絶対化: ' + '/'.join(ah))
            if eh:
                marks.append('評論: ' + '/'.join(eh))
        mm = ('  [' + ' ; '.join(marks) + ']') if marks else ''
        out.append(f'  {tag}選{i}: {c}{mm}')
    out.append('  --- 解説 ---')
    out.append('  ' + (q.get('comment', '') or '').replace('\n', '\n  '))
    out.append('')

Path('_work/audit_batch29_result.txt').write_text('\n'.join(out), encoding='utf-8')
print('wrote _work/audit_batch29_result.txt', len(IDS), 'problems')
