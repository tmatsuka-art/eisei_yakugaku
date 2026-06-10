# -*- coding: utf-8 -*-
# 細分が要るE-2 _subcat（栄養素の機能/食中毒/食品添加物/食物アレルギー）を分割ダンプ
import sys, json, math
sys.stdout.reconfigure(encoding="utf-8")

SUBCATS = {
    'nutrient': ('栄養素の機能', 4),   # 衛I 1-4（概論/ビタミン/ミネラル/三大栄養素）
    'foodpoison': ('食中毒', 2),       # 衛I 10-11（微生物/寄生虫・自然毒・化学物質）
    'additive': ('食品添加物', 1),     # 衛I 14-15（総論/各論）
    'allergy': ('食物アレルギー', 2),  # 衛I 9 or 13
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
        if not o.get('new_corecurri_code', '').startswith('E-2'):
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
        with open(f"_work/e2_{key}_{i+1}.md", "w", encoding="utf-8") as f:
            f.write(f"# {sc} part{i+1}: {len(part)}問\n\n")
            f.write("\n".join(fmt(o) for o in part))
        print(f"e2_{key}_{i+1}: {len(part)}問")
