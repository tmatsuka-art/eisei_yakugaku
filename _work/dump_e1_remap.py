# -*- coding: utf-8 -*-
# 公衆E-1の混入62問（再判定対象）を全科目判定用にダンプ
import sys, json, math
sys.stdout.reconfigure(encoding="utf-8")

ids = json.load(open('_work/e1_remap_ids.json', encoding='utf-8'))
idset = set(ids)
byid = {}
with open('future_questions.jsonl', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if o['problem_id'] in idset:
            byid[o['problem_id']] = o
qs = [byid[i] for i in ids if i in byid]

def fmt(o):
    pid = o['problem_id']
    code = o.get('new_corecurri_code', '?')
    sc = o.get('_subcat', '')
    q = o.get('problem_text', '').strip()
    ch = o.get('choices', [])
    ans = o.get('answer', '')
    cm = o.get('comment', '').strip()
    lines = [f"### {pid}  [{code}] [{sc}]", f"Q: {q}"]
    for i, c in enumerate(ch, 1):
        lines.append(f"  {i}. {c}")
    lines.append(f"A: {ans}")
    if cm:
        lines.append(f"解説: {cm[:200]}")
    lines.append("")
    return "\n".join(lines)

N = 2
per = math.ceil(len(qs) / N)
for i in range(N):
    part = qs[i * per:(i + 1) * per]
    if not part:
        continue
    with open(f"_work/e1_remap_{i+1}.md", "w", encoding="utf-8") as f:
        f.write(f"# remap part{i+1}: {len(part)}問\n\n")
        f.write("\n".join(fmt(o) for o in part))
    print(f"e1_remap_{i+1}: {len(part)}問")
print(f"合計 {len(qs)}問")
