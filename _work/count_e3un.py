# -*- coding: utf-8 -*-
# E-3未配置問題の_subcat・コード内訳（何が残っているか）
import sys, json
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")

fq = [json.loads(l) for l in open('future_questions.jsonl', encoding='utf-8') if l.strip()]
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

un = [o for o in fq if o['problem_id'] not in assigned and o.get('new_corecurri_code', '').startswith('E-3')]
print(f"E-3 未配置: {len(un)}問")
print("\n_subcat内訳:")
for k, v in Counter(o.get('_subcat', '?') for o in un).most_common():
    print(f"  {k}: {v}")
print("\nコード内訳:")
for k, v in Counter(o.get('new_corecurri_code', '?') for o in un).most_common():
    print(f"  {k}: {v}")
