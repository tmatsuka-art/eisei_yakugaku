# -*- coding: utf-8 -*-
# 対象外103問を分野別（公衆47/環境28/食品・生化学28）に本文ダンプ
import sys, json
sys.stdout.reconfigure(encoding="utf-8")

GROUPS = {
    'public': ['F101', 'F102', 'F105', 'F106', 'F113', 'F104', 'F107', 'F108', 'F110', 'F122',
               'F124', 'F1264', 'F1233', 'F139', 'F065', 'F117', 'F142', 'F143', 'F144', 'F145',
               'F146', 'F147', 'F149', 'F150', 'F186', 'F020', 'F103', 'F109', 'F121', 'F123',
               'F125', 'F129', 'F130', 'F138', 'F182', 'F184', 'F185', 'F1240', 'F1241', 'F1281',
               'F1308', 'F1313', 'F1336', 'F1337', 'F1338', 'F1339', 'F559'],
    'env': ['F011', 'F016', 'F116', 'F161', 'F163', 'F189', 'F190', 'F198', 'F171', 'F1283',
            'F181', 'F169', 'F199', 'F973', 'F195', 'F158', 'F100', 'F215', 'F977', 'F978',
            'F167', 'F187', 'F191', 'F196', 'F200', 'F212', 'F1290', 'F1298'],
    'food': ['F615', 'F626', 'F092', 'F1286', 'F440', 'F133', 'F437', 'F439', 'F441', 'F442',
             'F443', 'F444', 'F1207', 'F1213', 'F1243', 'F1274', 'F1289', 'F616', 'F617', 'F618',
             'F619', 'F620', 'F621', 'F622', 'F623', 'F625', 'F658', 'F659'],
}

byid = {}
with open('future_questions.jsonl', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        byid[o['problem_id']] = o

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

total = 0
for g, ids in GROUPS.items():
    with open(f"_work/group_{g}.md", "w", encoding="utf-8") as f:
        f.write(f"# {g}: {len(ids)}問\n\n")
        f.write("\n".join(fmt(byid[i]) for i in ids if i in byid))
    missing = [i for i in ids if i not in byid]
    total += len(ids)
    print(f"{g}: {len(ids)}問 → _work/group_{g}.md" + (f"  ⚠missing:{missing}" if missing else ""))
print(f"合計 {total}問")
