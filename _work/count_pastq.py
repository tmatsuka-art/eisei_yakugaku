# -*- coding: utf-8 -*-
# 過去問(hygiene_with_images_v4.jsonl)の配置状況・構造確認
import sys, json
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")

hyg = [json.loads(l) for l in open('hygiene_with_images_v4.jsonl', encoding='utf-8') if l.strip()]
print("総数:", len(hyg))
print("サンプルのキー:", list(hyg[0].keys()))

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
print(f"配置済み:{len(hyg)-len(un)} / 未配置:{len(un)}")

print("\n=== 未配置のコアカリ領域(new_corecurri_code先頭3字) ===")
for k, v in Counter((o.get('new_corecurri_code') or 'なし')[:3] for o in un).most_common():
    print(f"  {k}: {v}")

print("\n=== 未配置の_subcat内訳 ===")
for k, v in Counter(o.get('_subcat', 'なし') for o in un).most_common(25):
    print(f"  {k}: {v}")
