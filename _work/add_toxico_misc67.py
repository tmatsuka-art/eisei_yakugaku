# -*- coding: utf-8 -*-
# 毒性学 混入分の6/7回回収（法規制・リスコミ→6回、乱用薬物・法中毒→7回）
import sys, json, shutil
sys.stdout.reconfigure(encoding="utf-8")

# 6回（安全性評価・法規制）：法規制15＋リスコミ5
ADD6 = ['F014', 'F021', 'F022', 'F041', 'F042', 'F051', 'F058', 'F064', 'F1093',
        'F1262', 'F170', 'F541', 'F542', 'F560', 'F979',
        'F091', 'F093', 'F097', 'F151', 'F156']
# 7回（乱用薬物・法中毒学）：乱用薬物4＋法中毒5
ADD7 = ['F043', 'F044', 'F045', 'F046', 'F057', 'F059', 'F060', 'F085', 'F088']

shutil.copy('lecture_map.json', 'lecture_map.json.bak_pre_toxico_misc67')

lm = json.load(open('lecture_map.json', encoding='utf-8'))

def add_ids(lec, pids):
    ids = list(lm['衛II']['lectures'][lec]['ids'])
    added = []
    for p in pids:
        if p not in ids:
            ids.append(p)
            added.append(p)
    lm['衛II']['lectures'][lec]['ids'] = sorted(ids, key=lambda x: (1, x) if str(x)[:1] == 'F' else (0, x))
    return added

a6 = add_ids('6', ADD6)
a7 = add_ids('7', ADD7)

with open('lecture_map.json', 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2)
    f.write('\n')

for lec in ['6', '7']:
    arr = lm['衛II']['lectures'][lec]['ids']
    k = sum(1 for x in arr if str(x)[:1] != 'F')
    y = sum(1 for x in arr if str(x)[:1] == 'F')
    print(f"衛II-{lec} {lm['衛II']['lectures'][lec]['theme']}: 計{len(arr)}問（過去問{k}＋予想{y}）")
print(f"6回に追加: {len(a6)}問 / 7回に追加: {len(a7)}問")
if len(a6) != len(ADD6) or len(a7) != len(ADD7):
    print("⚠ 既存と重複したIDがあります（追加数 < 指定数）")
