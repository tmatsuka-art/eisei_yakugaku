"""バッチ7 対象20問を抽出"""
import json
from pathlib import Path

TARGET_IDS = [
    'F807', 'F959', 'F1198', 'F818', 'F973', 'F333', 'F593', 'F729',
    'F829', 'F256', 'F843', 'F849', 'F076', 'F749', 'F521', 'F1024',
    'F085', 'F1095', 'F1144', 'F584'
]

src = Path('future_questions.jsonl')
dst = Path('_work/lecture_batch7_len.jsonl')

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
