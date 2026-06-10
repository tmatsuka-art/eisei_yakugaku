# -*- coding: utf-8 -*-
# 食品E-2予想問題の全体像（_subcat内訳・配置済み/未配置）
import sys, json
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")

e2 = []
with open('future_questions.jsonl', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        code = o.get('new_corecurri_code', '')
        if code.startswith('E-2'):
            e2.append(o)

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

un = [o for o in e2 if o['problem_id'] not in assigned]
print(f"E-2予想 総数:{len(e2)} / 配置済み:{len(e2)-len(un)} / 未配置:{len(un)}")

print("\n=== 未配置の_subcat内訳 ===")
for k, v in Counter(o.get('_subcat', '?') for o in un).most_common():
    print(f"  {k}: {v}")

print("\n=== 未配置のコアカリコード内訳 ===")
for k, v in Counter(o.get('new_corecurri_code', '?') for o in un).most_common():
    print(f"  {k}: {v}")
