"""中身レビュー 第1バッチの抽出：『化学物質の体内動態』の未レビューを problem_id 順に先頭15問。"""
import json
from pathlib import Path

qs = []
for line in open('future_questions.jsonl', encoding='utf-8'):
    if line.strip():
        qs.append(json.loads(line))


def pid_key(q):
    s = q.get('problem_id', 'F0')
    try:
        return int(s[1:])
    except ValueError:
        return 0


target = [q for q in qs
          if q.get('_subcat') == '化学物質の体内動態' and not q.get('ai_review')]
target.sort(key=pid_key)
batch = target[:15]

with open('_work/content_batch1.jsonl', 'w', encoding='utf-8') as f:
    for q in batch:
        f.write(json.dumps(q, ensure_ascii=False) + '\n')

lines = []
lines.append(f'抽出: {len(batch)}問（化学物質の体内動態・未レビュー先頭15）')
for q in batch:
    ans = ','.join(q.get('answer') or [])
    lines.append(f"{q['problem_id']}  正答[{ans}]  {q.get('new_corecurri_code','')}  {q.get('problem_text','')[:40]}")
Path('_work/content_batch1_list.txt').write_text('\n'.join(lines), encoding='utf-8')
print(f'wrote _work/content_batch1.jsonl ({len(batch)}問)')
print(f'残り未レビュー（化学物質の体内動態）: {len(target) - len(batch)}問')
