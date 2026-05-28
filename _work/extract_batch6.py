"""バッチ6 対象20問を抽出"""
import json
from pathlib import Path

TARGET_IDS = [
    'F1236', 'F1002', 'F1152', 'F1261', 'F805', 'F239', 'F1122', 'F1116',
    'F1196', 'F727', 'F813', 'F824', 'F1263', 'F806', 'F340', 'F574',
    'F728', 'F598', 'F066', 'F951'
]

src = Path('future_questions.jsonl')
dst = Path('_work/lecture_batch6_len.jsonl')

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
