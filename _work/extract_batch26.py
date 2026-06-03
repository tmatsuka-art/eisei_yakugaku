"""バッチ17 絶対化1hit第4回 20問を自動抽出。

未レビュー(ai_review なし)で、攪乱肢の絶対化ヒットがちょうど1箇所の問題を
problem_id 順に並べ、F330 より後ろから20問を選ぶ。
（scan_quality.py と同じ検出ロジックを使用）
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

THRESHOLD = 1206  # この problem_id 番号より後ろを対象


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


def pid_num(pid):
    m = re.match(r'F(\d+)', pid or '')
    return int(m.group(1)) if m else 10**9


src = Path('future_questions.jsonl')
dst = Path('_work/lecture_batch26_abs.jsonl')

qs = []
with open(src, encoding='utf-8') as f:
    for line in f:
        if line.strip():
            qs.append(json.loads(line))

candidates = []
for q in qs:
    if q.get('ai_review'):
        continue
    pid = q.get('problem_id', '')
    choices = q.get('choices', []) or []
    answer = q.get('answer', []) or []
    if not choices or not answer:
        continue
    ans_idx = set()
    for a in answer:
        try:
            ans_idx.add(int(a))
        except (ValueError, TypeError):
            pass
    hit_total = 0
    hit_choices = []
    for i, c in enumerate(choices, 1):
        if i in ans_idx:
            continue
        h = scan_absolute(c)
        if h:
            hit_total += len(h)
            hit_choices.append((i, h))
    if hit_total == 1:
        candidates.append((pid_num(pid), pid, hit_choices))

candidates.sort()
after = [c for c in candidates if c[0] > THRESHOLD]
batch = after[:20]

qs_by_id = {q.get('problem_id'): q for q in qs}
out_lines = []
print(f'1hit未レビュー総数: {len(candidates)} / F{THRESHOLD}以降: {len(after)}')
print('バッチ26対象:')
for num, pid, hc in batch:
    detail = ', '.join(f'選{i}:{"/".join(h)}' for i, h in hc)
    print(f'  {pid}  [{detail}]')
    out_lines.append(json.dumps(qs_by_id[pid], ensure_ascii=False))

dst.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')
print(f'wrote {dst}: {len(out_lines)} questions')
