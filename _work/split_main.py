# -*- coding: utf-8 -*-
# 本体162問(E-3-1-(1)(2))を6ファイルに分割（エージェント分担判定用）
import sys, json, math
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
        if o.get("_subcat") in targets and o.get("new_corecurri_code") in main_codes:
            qs.append(o)
qs.sort(key=lambda o: o["problem_id"])

def fmt(o):
    pid = o["problem_id"]
    q = o.get("problem_text", "").strip()
    ch = o.get("choices", [])
    ans = o.get("answer", "")
    cm = o.get("comment", "").strip()
    lines = [f"### {pid}", f"Q: {q}"]
    for i, c in enumerate(ch, 1):
        lines.append(f"  {i}. {c}")
    lines.append(f"A: {ans}")
    if cm:
        lines.append(f"解説: {cm[:250]}")
    lines.append("")
    return "\n".join(lines)

N = 6
per = math.ceil(len(qs) / N)
for i in range(N):
    part = qs[i * per:(i + 1) * per]
    if not part:
        continue
    with open(f"_work/main_part{i+1}.md", "w", encoding="utf-8") as f:
        f.write(f"# 本体 part{i+1}: {len(part)}問\n\n")
        f.write("\n".join(fmt(o) for o in part))
    print(f"part{i+1}: {len(part)}問 ({part[0]['problem_id']}〜{part[-1]['problem_id']})")
print(f"合計 {len(qs)}問")
