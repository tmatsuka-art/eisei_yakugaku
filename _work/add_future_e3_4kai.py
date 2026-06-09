# -*- coding: utf-8 -*-
# 予想問題E-3系 明確4回を lecture_map に割当（放射線/大気/室内/地球環境）
import json

EXPECT = {
    '放射線':       ('11', ('E-3-2-(2)',)),
    '大気環境':     ('14', ('E-3-2-(1)',)),
    '室内環境':     ('15', ('E-3-2-(1)',)),
    '地球環境問題': ('9',  ('E-3-2-(1)', 'E-3-2-(4)')),
}
ADD14 = {'F136','F188','F192','F204','F1013','F1020','F1238','F1259'}  # 大気の公害・法規（要確認から採用）
buckets = {'9': set(), '11': set(), '14': set(), '15': set()}

with open('future_questions.jsonl', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        o = json.loads(line); s = o.get('_subcat'); pid = o['problem_id']; code = o.get('new_corecurri_code','')
        if s in EXPECT:
            lec, exp = EXPECT[s]
            if code in exp:
                buckets[lec].add(pid)
        if pid in ADD14:
            buckets['14'].add(pid)

lm = json.load(open('lecture_map.json', encoding='utf-8'))
for lec, pids in buckets.items():
    ids = list(lm['衛II']['lectures'][lec]['ids'])
    for p in pids:
        if p not in ids:
            ids.append(p)
    lm['衛II']['lectures'][lec]['ids'] = sorted(ids, key=lambda x: (1, x) if str(x)[:1] == 'F' else (0, x))

with open('lecture_map.json', 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2); f.write('\n')

for lec in ['9', '11', '14', '15']:
    arr = lm['衛II']['lectures'][lec]['ids']
    k = sum(1 for x in arr if str(x)[:1] != 'F'); y = sum(1 for x in arr if str(x)[:1] == 'F')
    print(f"衛II-{lec} {lm['衛II']['lectures'][lec]['theme']}: 計{len(arr)}問（過去問{k}＋予想{y}）")
