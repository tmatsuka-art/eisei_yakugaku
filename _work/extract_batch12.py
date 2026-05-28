"""バッチ12 絶対化2hit第3回 20問を抽出"""
import json
from pathlib import Path

TARGET_IDS = [
    'F845', 'F868', 'F903', 'F954', 'F958', 'F961', 'F962', 'F965', 'F967', 'F971',
    'F1000', 'F1034', 'F1035', 'F1087', 'F1101', 'F1112', 'F1125', 'F1134', 'F1142', 'F1146'
]

src = Path('future_questions.jsonl')
dst = Path('_work/lecture_batch12_abs.jsonl')

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
