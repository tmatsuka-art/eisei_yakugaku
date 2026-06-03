"""構造注記のある問題について、answerフィールドの実値と解説の正答記述を突き合わせる。"""
import json
import re
from pathlib import Path

IDS = ['F1208', 'F1228, '.strip().strip(',') if False else 'F1228', 'F1253', 'F1244', 'F1278', 'F1336']
IDS = ['F1208', 'F1228', 'F1253', 'F1244', 'F1278', 'F1336', 'F1213', 'F1248']

qs = {}
for line in open('future_questions.jsonl', encoding='utf-8'):
    if line.strip():
        q = json.loads(line)
        qs[q['problem_id']] = q

out = []
for pid in IDS:
    q = qs[pid]
    ans = q.get('answer')
    comment = q.get('comment', '') or ''
    # 解説中の「N:正」を抽出（各選択肢の正誤判定）
    verdicts = []
    for i in range(1, 6):
        # 「1:正」「1：正」「1:誤」などを探す
        m = re.search(rf'{i}\s*[:：]\s*(正|誤)', comment)
        if m:
            verdicts.append(f'選{i}={m.group(1)}')
    out.append(f'{pid}: answerフィールド={ans} / 解説判定={verdicts}')

Path('_work/check_answers_result.txt').write_text('\n'.join(out), encoding='utf-8')
print('done')
