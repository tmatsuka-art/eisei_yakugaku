"""バッチ14 絶対化1hit上位20問を抽出"""
import json
from pathlib import Path

TARGET_IDS = [
    'F047', 'F054', 'F055', 'F072', 'F073', 'F078', 'F079', 'F080',
    'F094', 'F095', 'F096', 'F098', 'F103', 'F109', 'F121', 'F123',
    'F125', 'F127', 'F128', 'F129'
]

src = Path('future_questions.jsonl')
dst = Path('_work/lecture_batch14_abs.jsonl')

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
