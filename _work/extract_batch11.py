"""バッチ11 絶対化2hit第2回 20問を抽出"""
import json
from pathlib import Path

TARGET_IDS = [
    'F469', 'F489', 'F491', 'F493', 'F520', 'F566', 'F576', 'F590', 'F596', 'F597',
    'F600', 'F615', 'F633', 'F732', 'F733', 'F809', 'F811', 'F820', 'F832', 'F842'
]

src = Path('future_questions.jsonl')
dst = Path('_work/lecture_batch11_abs.jsonl')

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
