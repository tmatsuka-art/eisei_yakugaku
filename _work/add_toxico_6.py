# -*- coding: utf-8 -*-
# 毒性学 本体判定のうち第6回（安全性評価・法規制）51問を衛II-6へ追加
import sys, json, shutil
sys.stdout.reconfigure(encoding="utf-8")

ADD6 = ['F004', 'F007', 'F010', 'F023', 'F027', 'F029', 'F050', 'F053', 'F069',
        'F094', 'F095', 'F096', 'F098', 'F099', 'F1039', 'F1140', 'F1215', 'F1231', 'F1237',
        'F1266', 'F1294', 'F1299', 'F1315', 'F1316', 'F1317', 'F1318', 'F1319',
        'F152', 'F153', 'F154', 'F155', 'F157', 'F160', 'F211', 'F213', 'F217', 'F218', 'F306',
        'F540', 'F549', 'F714', 'F720', 'F729', 'F767', 'F793', 'F971', 'F972', 'F974', 'F975', 'F976', 'F980']

shutil.copy('lecture_map.json', 'lecture_map.json.bak_pre_toxico6')
lm = json.load(open('lecture_map.json', encoding='utf-8'))
ids = list(lm['衛II']['lectures']['6']['ids'])
added = 0
for p in ADD6:
    if p not in ids:
        ids.append(p)
        added += 1
lm['衛II']['lectures']['6']['ids'] = sorted(ids, key=lambda x: (1, x) if str(x)[:1] == 'F' else (0, x))

with open('lecture_map.json', 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2)
    f.write('\n')

arr = lm['衛II']['lectures']['6']['ids']
k = sum(1 for x in arr if str(x)[:1] != 'F')
y = sum(1 for x in arr if str(x)[:1] == 'F')
print(f"衛II-6 {lm['衛II']['lectures']['6']['theme']}: 計{len(arr)}問（過去問{k}＋予想{y}）, 今回追加{added}/{len(ADD6)}")
if added != len(ADD6):
    print("⚠ 重複あり（追加数 < 指定数）")
