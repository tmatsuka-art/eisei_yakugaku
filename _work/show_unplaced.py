# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
hyg = [json.loads(l) for l in open('hygiene_with_images_v4.jsonl', encoding='utf-8') if l.strip()]
lm = json.load(open('lecture_map.json', encoding='utf-8'))
assigned = set()
def collect(n):
    if isinstance(n, dict):
        for k, v in n.items():
            if k == 'ids' and isinstance(v, list):
                assigned.update(v)
            else:
                collect(v)
    elif isinstance(n, list):
        for x in n:
            collect(x)
collect(lm)
un = [o for o in hyg if o['problem_id'] not in assigned]
for o in un:
    img = o.get('num_images', 0)
    tag = f"[図{img}]" if img else ""
    print(f"{o['problem_id']} [{o.get('new_corecurri_code')}][{o.get('_subcat')}]{tag}: {o.get('problem_text','')[:70]}")
