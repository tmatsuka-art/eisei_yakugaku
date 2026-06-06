# -*- coding: utf-8 -*-
# 環境の漏れ候補の本文を精査する
import json

targets = ['098137','100139','109140','111242','101136','100140','109244','111244']
rev = {}
lm = json.load(open('lecture_map.json', encoding='utf-8'))
for kamoku, kd in lm.items():
    for lec, ld in kd['lectures'].items():
        for pid in ld['ids']:
            rev.setdefault(pid, []).append(f"{kamoku}-{lec}")

rows = []
with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line)
        if o.get('problem_id') in targets:
            rows.append(o)
rows.sort(key=lambda o: o.get('problem_id'))

for o in rows:
    pid = o.get('problem_id')
    print(f"=== {pid} {o.get('display_title')} | code={o.get('new_corecurri_code')} _subcat={o.get('_subcat')} | 現割当:{rev.get(pid,'なし')} ===")
    print('Q:', (o.get('problem_text') or '').strip()[:130])
    for i, c in enumerate(o.get('choices') or [], 1):
        print(f'  {i}. {(c or "")[:62]}')
    print('A:', o.get('answer'))
    print()
