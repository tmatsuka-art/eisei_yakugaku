"""バッチ9 混合構成20問を抽出"""
import json
from pathlib import Path

TARGET_IDS = [
    # 長さアンバランス残10件
    'F1145', 'F1165', 'F512', 'F608', 'F1106', 'F837', 'F996', 'F423', 'F626', 'F823',
    # 評論的修飾4件
    'F048', 'F265', 'F284', 'F428',
    # 絶対化2hit 6件
    'F019', 'F029', 'F069', 'F077', 'F084', 'F086'
]

src = Path('future_questions.jsonl')
dst = Path('_work/lecture_batch9_mix.jsonl')

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
