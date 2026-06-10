# -*- coding: utf-8 -*-
# 細分が要るE-1 _subcatを分割ダンプ（生活習慣病/感染症系/保健統計）
import sys, json, math
sys.stdout.reconfigure(encoding="utf-8")

SUBCATS = {
    'seikatsu': ('生活習慣病・予防医学', 4),   # 公衆 2(予防) or 7(生活習慣病各論)
    'kansen_yobo': ('感染症の予防・対策', 3),   # 公衆 11+
    'kansen_main': ('主要感染症', 2),           # 公衆 12/13
    'kansen_amr': ('院内感染・薬剤耐性', 2),     # 公衆 11
    'kansen_law': ('感染症の法規・行政', 1),     # 公衆 12/13/14
    'toukei': ('保健統計', 1),                   # 公衆 3/4/5/6
}

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

bysubcat = {}
with open('future_questions.jsonl', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if not o.get('new_corecurri_code', '').startswith('E-1'):
            continue
        if o['problem_id'] in assigned:
            continue
        bysubcat.setdefault(o.get('_subcat', ''), []).append(o)

def fmt(o):
    pid = o['problem_id']
    code = o.get('new_corecurri_code', '?')
    q = o.get('problem_text', '').strip()
    ch = o.get('choices', [])
    ans = o.get('answer', '')
    cm = o.get('comment', '').strip()
    lines = [f"### {pid}  [{code}]", f"Q: {q}"]
    for i, c in enumerate(ch, 1):
        lines.append(f"  {i}. {c}")
    lines.append(f"A: {ans}")
    if cm:
        lines.append(f"解説: {cm[:200]}")
    lines.append("")
    return "\n".join(lines)

for key, (sc, nfiles) in SUBCATS.items():
    qs = sorted(bysubcat.get(sc, []), key=lambda o: o['problem_id'])
    per = math.ceil(len(qs) / nfiles) if qs else 0
    for i in range(nfiles):
        part = qs[i * per:(i + 1) * per]
        if not part:
            continue
        with open(f"_work/e1_{key}_{i+1}.md", "w", encoding="utf-8") as f:
            f.write(f"# {sc} part{i+1}: {len(part)}問\n\n")
            f.write("\n".join(fmt(o) for o in part))
        print(f"e1_{key}_{i+1}: {len(part)}問")
