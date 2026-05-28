"""バッチ10 絶対化2hit 20問を抽出"""
import json
from pathlib import Path

TARGET_IDS = [
    'F090', 'F099', 'F156', 'F237', 'F263', 'F272', 'F279', 'F309', 'F310', 'F319',
    'F327', 'F332', 'F338', 'F339', 'F403', 'F405', 'F440', 'F447', 'F460', 'F468'
]

src = Path('future_questions.jsonl')
dst = Path('_work/lecture_batch10_abs.jsonl')

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
