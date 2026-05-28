"""バッチ13 絶対化2hit残＋1hit補充 20問を抽出"""
import json
from pathlib import Path

TARGET_IDS = [
    # 2hit残り15問
    'F1167', 'F1188', 'F1195', 'F1199', 'F1209', 'F1216', 'F1249',
    'F1265', 'F1283', 'F1284', 'F1355', 'F1391', 'F1409', 'F1412', 'F1413',
    # 1hit上位5問
    'F006', 'F012', 'F022', 'F027', 'F046'
]

src = Path('future_questions.jsonl')
dst = Path('_work/lecture_batch13_abs.jsonl')

qs_by_id = {}
with open(src, encoding='utf-8') as f:
    for line in f:
        if line.strip():
            q = json.loads(line)
            qs_by_id[q.get('problem_id')] = q

out_lines = []
for pid in TARGET_IDS:
    if pid not in qs_by_id:
        print(f'WARN: {pid} not found')
        continue
    out_lines.append(json.dumps(qs_by_id[pid], ensure_ascii=False))

dst.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')
print(f'wrote {dst}: {len(out_lines)} questions')
