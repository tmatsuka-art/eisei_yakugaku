# -*- coding: utf-8 -*-
# 毒性学241問を本文付きでダンプ。本体(E-3-1-(1)(2))と混入候補(他コード)に分割。
import sys, json
sys.stdout.reconfigure(encoding="utf-8")

targets = {"化学物質の体内動態", "毒性学総論"}
main_codes = {"E-3-1-(1)", "E-3-1-(2)"}

qs = []
with open("future_questions.jsonl", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if o.get("_subcat") in targets:
            qs.append(o)

def fmt(o):
    pid = o["problem_id"]
    code = o.get("new_corecurri_code", "?")
    sub = o.get("_subcat", "")
    q = o.get("problem_text", "").strip()
    ch = o.get("choices", [])
    ans = o.get("answer", "")
    cm = o.get("comment", "").strip()
    lines = [f"### {pid}  [{code}] [{sub}]", f"Q: {q}"]
    for i, c in enumerate(ch, 1):
        lines.append(f"  {i}. {c}")
    lines.append(f"A: {ans}")
    if cm:
        lines.append(f"解説: {cm[:250]}")
    lines.append("")
    return "\n".join(lines)

main = [o for o in qs if o.get("new_corecurri_code") in main_codes]
misc = [o for o in qs if o.get("new_corecurri_code") not in main_codes]
main.sort(key=lambda o: o["problem_id"])
misc.sort(key=lambda o: (o.get("new_corecurri_code", ""), o["problem_id"]))

with open("_work/toxico_main.md", "w", encoding="utf-8") as f:
    f.write(f"# 毒性学 本体 {len(main)}問（E-3-1-(1)(2)＝第1/2/4回判定対象）\n\n")
    f.write("\n".join(fmt(o) for o in main))

with open("_work/toxico_misc.md", "w", encoding="utf-8") as f:
    f.write(f"# 毒性学 混入候補 {len(misc)}問（他回・他科目の可能性。コード順）\n\n")
    f.write("\n".join(fmt(o) for o in misc))

print(f"main(本体): {len(main)}問 → _work/toxico_main.md")
print(f"misc(混入候補): {len(misc)}問 → _work/toxico_misc.md")
