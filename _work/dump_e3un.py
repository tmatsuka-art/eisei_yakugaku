# -*- coding: utf-8 -*-
# E-3未配置57問を全科目判定用にダンプ（2分割）
import sys, json, math
sys.stdout.reconfigure(encoding="utf-8")

fq = [json.loads(l) for l in open('future_questions.jsonl', encoding='utf-8') if l.strip()]
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

un = [o for o in fq if o['problem_id'] not in assigned and o.get('new_corecurri_code', '').startswith('E-3')]
un.sort(key=lambda o: o['problem_id'])

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
per = math.ceil(len(un) / N)
for i in range(N):
    part = un[i * per:(i + 1) * per]
    if not part:
        continue
    with open(f"_work/e3un_{i+1}.md", "w", encoding="utf-8") as f:
        f.write(f"# E-3未配置 part{i+1}: {len(part)}問\n\n")
        f.write("\n".join(fmt(o) for o in part))
    print(f"e3un_{i+1}: {len(part)}問")
print(f"合計 {len(un)}問")
# IDリスト保存
with open('_work/e3un_ids.json', 'w', encoding='utf-8') as f:
    json.dump([o['problem_id'] for o in un], f, ensure_ascii=False)
