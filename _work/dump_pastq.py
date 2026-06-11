# -*- coding: utf-8 -*-
# 過去問の未配置271問を領域別にダンプ（全科目判定用）
import sys, json, math
sys.stdout.reconfigure(encoding="utf-8")

hyg = [json.loads(l) for l in open('hygiene_with_images_v4.jsonl', encoding='utf-8') if l.strip()]
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
groups = {'e2': [], 'e3': [], 'e1': [], 'other': []}
for o in un:
    code = o.get('new_corecurri_code') or ''
    if code.startswith('E-2'):
        groups['e2'].append(o)
    elif code.startswith('E-3'):
        groups['e3'].append(o)
    elif code.startswith('E-1'):
        groups['e1'].append(o)
    else:
        groups['other'].append(o)

def fmt(o):
    pid = o['problem_id']
    code = o.get('new_corecurri_code', '?')
    sc = o.get('_subcat', '')
    img = o.get('num_images', 0)
    q = o.get('problem_text', '').strip()
    ch = o.get('choices', [])
    ans = o.get('answer', '')
    cm = o.get('comment', '').strip()
    tag = f" [図{img}枚]" if img else ""
    lines = [f"### {pid}  [{code}] [{sc}]{tag}", f"Q: {q}"]
    for i, c in enumerate(ch, 1):
        lines.append(f"  {i}. {c}")
    lines.append(f"A: {ans}")
    if cm:
        lines.append(f"解説: {cm[:200]}")
    lines.append("")
    return "\n".join(lines)

SPLIT = {'e2': 7, 'e3': 4, 'e1': 1, 'other': 1}
for g, qs in groups.items():
    if not qs:
        continue
    qs.sort(key=lambda o: o['problem_id'])
    nf = SPLIT.get(g, 1)
    per = math.ceil(len(qs) / nf)
    for i in range(nf):
        part = qs[i * per:(i + 1) * per]
        if not part:
            continue
        with open(f"_work/pq_{g}_{i+1}.md", "w", encoding="utf-8") as f:
            f.write(f"# {g} part{i+1}: {len(part)}問\n\n")
            f.write("\n".join(fmt(o) for o in part))
        print(f"pq_{g}_{i+1}: {len(part)}問")
print(f"\n領域別: e2={len(groups['e2'])} e3={len(groups['e3'])} e1={len(groups['e1'])} other={len(groups['other'])}")
