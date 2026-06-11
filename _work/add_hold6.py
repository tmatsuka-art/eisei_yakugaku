# -*- coding: utf-8 -*-
import sys, json, shutil
sys.stdout.reconfigure(encoding="utf-8")
shutil.copy("lecture_map.json", "lecture_map.json.bak_pre_hold6")
lm = json.load(open("lecture_map.json", encoding="utf-8"))
PLAN = {"公衆": {"10": ["F141", "F148"], "1": ["F1291", "F1312"]}, "衛I": {"9": ["F1106"], "12": ["F1152"]}}
added = 0
for subj, lecs in PLAN.items():
    for lec, ids in lecs.items():
        arr = list(lm[subj]["lectures"][lec]["ids"])
        for p in ids:
            if p not in arr:
                arr.append(p)
                added += 1
        lm[subj]["lectures"][lec]["ids"] = sorted(arr, key=lambda x: (1, x) if str(x)[:1] == "F" else (0, x))
with open("lecture_map.json", "w", encoding="utf-8") as f:
    json.dump(lm, f, ensure_ascii=False, indent=2)
    f.write("\n")

def load(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
fq = load("future_questions.jsonl")
hyg = load("hygiene_with_images_v4.jsonl")
lm2 = json.load(open("lecture_map.json", encoding="utf-8"))
asg = set()
for s in lm2.values():
    for lec in s.get("lectures", {}).values():
        asg.update(lec.get("ids", []))
fqu = [o for o in fq if o["problem_id"] not in asg]
hu = [o for o in hyg if o["problem_id"] not in asg]
print(f"配置追加={added}")
print(f"予想 配置{len(fq)-len(fqu)}/{len(fq)} 未配置{len(fqu)}")
print(f"過去問 配置{len(hyg)-len(hu)}/{len(hyg)} 未配置{len(hu)}")
