# -*- coding: utf-8 -*-
# 全予想問題の配置状況（達成確認）
import sys, json
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")

with open('future_questions.jsonl', encoding='utf-8') as f:
    fq = [json.loads(l) for l in f if l.strip()]

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

un = [o for o in fq if o['problem_id'] not in assigned]
print(f"予想問題 総数:{len(fq)} / 配置済み:{len(fq)-len(un)} / 未配置:{len(un)}")
print(f"配置率: {100*(len(fq)-len(un))/len(fq):.1f}%")

print("\n未配置のコアカリ領域内訳:")
for k, v in Counter(o.get('new_corecurri_code', '?')[:3] for o in un).most_common():
    print(f"  {k}: {v}")

# 科目別の予想問題数
print("\n科目別の配置済み予想問題数:")
for subj in ('衛I', '衛II', '公衆'):
    if subj not in lm:
        continue
    n = 0
    for lec in lm[subj]['lectures'].values():
        n += sum(1 for x in lec.get('ids', []) if str(x)[:1] == 'F')
    print(f"  {subj}: {n}問")
