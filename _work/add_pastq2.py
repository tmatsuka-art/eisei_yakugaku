# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
PLAN = {
 '衛I': {'3': ['097226'], '4': ['107019', '108233'], '5': ['111019'], '9': ['108127'], '11': ['101229'], '12': ['104121'], '15': ['104119']},
 '衛II': {'5': ['101132'], '12': ['111238']},
}
lm = json.load(open('lecture_map.json', encoding='utf-8'))
total = 0
for subj, lecs in PLAN.items():
    for lec, ids in lecs.items():
        arr = list(lm[subj]['lectures'][lec]['ids'])
        for p in ids:
            if p not in arr:
                arr.append(p)
                total += 1
        lm[subj]['lectures'][lec]['ids'] = sorted(arr, key=lambda x: (1, x) if str(x)[:1] == 'F' else (0, x))
with open('lecture_map.json', 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(f"追加: {total}問")
