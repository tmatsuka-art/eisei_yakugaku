# -*- coding: utf-8 -*-
import sys, json
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")

def load(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]

hyg = load("hygiene_with_images_v4.jsonl")

c = Counter()
for o in hyg:
    t = o.get("problem_text", "") + " ".join(o.get("choices", [])) + o.get("comment", "")
    if "土壌汚染" in t or "廃棄物" in t:
        c[o.get("_subcat")] += 1
print("【土壌汚染/廃棄物を含む過去問の _subcat】")
for k, v in c.most_common():
    print(f"  {k}: {v}")

print("\n【過去問の環境系 _subcat 一覧】")
allc = Counter(o.get("_subcat") for o in hyg)
for k, v in allc.most_common():
    if any(w in (k or "") for w in ["環境", "廃棄", "水", "大気", "放射", "室内", "土壌", "地球"]):
        print(f"  {k}: {v}")
