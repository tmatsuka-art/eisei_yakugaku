# -*- coding: utf-8 -*-
# 毒性学1/2/4回 未配置問題の集計（_subcat=化学物質の体内動態/毒性学総論）
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
from collections import Counter

targets = {"化学物質の体内動態", "毒性学総論"}

qs = []
with open("future_questions.jsonl", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if o.get("_subcat") in targets:
            qs.append(o)

lm = json.load(open("lecture_map.json", encoding="utf-8"))
assigned = set()
def collect(n):
    if isinstance(n, dict):
        for k, v in n.items():
            if k == "ids" and isinstance(v, list):
                assigned.update(v)
            else:
                collect(v)
    elif isinstance(n, list):
        for x in n:
            collect(x)
collect(lm)

unassigned = [o for o in qs if o["problem_id"] not in assigned]
assigned_qs = [o for o in qs if o["problem_id"] in assigned]

print("=== 対象_subcat総数:", len(qs), "===")
for k, v in Counter(o["_subcat"] for o in qs).items():
    print(f"  {k}: {v}")

print("\n=== 配置済み:", len(assigned_qs), "===")
where = Counter()
for subj, sd in lm.items():
    if not isinstance(sd, dict):
        continue
    for lec, ld in sd.get("lectures", {}).items():
        ids = set(ld.get("ids", []))
        for o in assigned_qs:
            if o["problem_id"] in ids:
                where[f"{subj}-{lec} {ld.get('theme','')}"] += 1
for k, v in sorted(where.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")

print("\n=== 未配置(作業対象):", len(unassigned), "===")
for k, v in Counter(o["_subcat"] for o in unassigned).items():
    print(f"  {k}: {v}")

print("\n=== 未配置のコアカリコード内訳 ===")
for k, v in sorted(Counter(o.get("new_corecurri_code", "?") for o in unassigned).items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
