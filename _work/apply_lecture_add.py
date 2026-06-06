# -*- coding: utf-8 -*-
# 環境カバーの漏れ6問を、該当授業回のidsに追加（昇順維持）
import json

SRC = 'lecture_map.json'
lm = json.load(open(SRC, encoding='utf-8'))
lec = lm['衛II']['lectures']

add = {
    '9':  ['101136'],                       # 地球環境（環境中の水・水圏・生態系）
    '14': ['098137', '100139'],             # 室外大気（NOx/SOx測定法）
    '15': ['109140', '111242', '100140'],   # 室内（WBGT・教室CO/NO2・騒音）
}
for l, pids in add.items():
    ids = list(lec[l]['ids'])
    for p in pids:
        if p not in ids:
            ids.append(p)
    lec[l]['ids'] = sorted(ids)

with open(SRC, 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2)
    f.write('\n')

for l in ['9', '14', '15']:
    print(f"衛II-{l} {lec[l]['theme']}: {len(lec[l]['ids'])}問")
