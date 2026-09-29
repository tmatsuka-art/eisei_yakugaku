# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
lm = json.load(open("lecture_map.json", encoding="utf-8"))
for subj, sdata in lm.items():
    print(f"\n=== {subj} ({sdata.get('label','')}) ===")
    lectures = sdata.get("lectures", {})
    for lec in sorted(lectures.keys(), key=lambda x: int(x) if str(x).isdigit() else 999):
        ldata = lectures[lec]
        theme = ldata.get("theme", "")
        ids = ldata.get("ids", [])
        past = sum(1 for x in ids if str(x)[:1].isdigit())
        pred = len(ids) - past
        print(f"  第{lec}回: {theme} （過去問{past}, 予想{pred}）")
