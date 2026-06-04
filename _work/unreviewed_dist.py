"""未レビュー問題の分野別分布。中身レビューのバッチ選定用。"""
import json
from collections import Counter, defaultdict
from pathlib import Path

qs = []
for line in open('future_questions.jsonl', encoding='utf-8'):
    if line.strip():
        qs.append(json.loads(line))

unrev = [q for q in qs if not q.get('ai_review')]
subcat = Counter()
subcat_ids = defaultdict(list)
for q in unrev:
    sc = q.get('_subcat', '(なし)')
    subcat[sc] += 1
    subcat_ids[sc].append(q['problem_id'])

out = []
out.append(f'未レビュー問題: {len(unrev)} / 全{len(qs)}')
out.append('')
out.append('=== 分野(_subcat)別 未レビュー数（多い順）===')
for sc, n in subcat.most_common():
    ids = subcat_ids[sc]
    sample = ', '.join(ids[:6]) + ('...' if len(ids) > 6 else '')
    out.append(f'{n:3d}問  {sc}  （{sample}）')

Path('_work/unreviewed_dist_result.txt').write_text('\n'.join(out), encoding='utf-8')
print('未レビュー:', len(unrev), '/ 分野数:', len(subcat))
for sc, n in subcat.most_common(12):
    print(f'  {n:3d}  {sc}')
