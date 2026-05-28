"""バッチ15 絶対化1hit第2回 20問を抽出"""
import json
from pathlib import Path

TARGET_IDS = [
    'F130', 'F132', 'F133', 'F135', 'F138', 'F152', 'F153', 'F154',
    'F157', 'F160', 'F167', 'F182', 'F187', 'F200', 'F212', 'F221',
    'F232', 'F242', 'F245', 'F250'
]

src = Path('future_questions.jsonl')
dst = Path('_work/lecture_batch15_abs.jsonl')

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
