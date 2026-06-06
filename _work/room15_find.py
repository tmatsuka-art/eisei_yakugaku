# -*- coding: utf-8 -*-
# 室内大気(衛II-15)候補の吟味：指定行の問題を、既存の授業回割当つきで読む
import json

rev = {}
lm = json.load(open('lecture_map.json', encoding='utf-8'))
for kamoku, kd in lm.items():
    for lec, ld in kd.get('lectures', {}).items():
        for pid in ld.get('ids', []):
            rev.setdefault(pid, []).append(f"{kamoku}-{lec}")

target_lines = {333,407,454,468,469,470,500,517,536,551,580,597,620,627,646}

with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if i not in target_lines:
            continue
        o = json.loads(line)
        pid = o.get('problem_id')
        assigned = rev.get(pid, [])
        flag = ('★既出:' + ','.join(assigned)) if assigned else '（未割当）'
        print(f"L{i} | {pid} {o.get('display_title')} | {flag} | _subcat={o.get('_subcat')} | code={o.get('new_corecurri_code')}")
        print(f"   Q: {(o.get('problem_text') or '').strip()[:82]}")
