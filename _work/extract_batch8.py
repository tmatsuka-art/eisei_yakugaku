"""バッチ8 対象20問を抽出"""
import json
from pathlib import Path

TARGET_IDS = [
    'F610', 'F987', 'F692', 'F1001', 'F1233', 'F1222', 'F825', 'F501',
    'F524', 'F1224', 'F337', 'F835', 'F745', 'F895', 'F075', 'F860',
    'F1256', 'F534', 'F821', 'F1060'
]

src = Path('future_questions.jsonl')
dst = Path('_work/lecture_batch8_len.jsonl')

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
