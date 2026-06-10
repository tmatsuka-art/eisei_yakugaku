# -*- coding: utf-8 -*-
# 公衆E-1混入62問の再判定を3科目へ反映（範囲外7問は保留）
import sys, json, shutil
sys.stdout.reconfigure(encoding="utf-8")

PLAN = {
    '衛I': {
        '1': ['F1130'], '7': ['F1129'], '11': ['F1078'], '13': ['F1036', 'F1038', 'F1050', 'F1090'],
    },
    '衛II': {
        '1': ['F1058', 'F1096', 'F1197'], '2': ['F1098', 'F1099'], '3': ['F1064', 'F1109'],
        '4': ['F1082'], '5': ['F1053'], '6': ['F1071', 'F1097', 'F1147', 'F1157', 'F159', 'F1075'],
        '7': ['F1149'], '9': ['F1103'], '10': ['F1267'], '12': ['F1074', 'F1166', 'F1268'],
        '13': ['F1067', 'F1113'], '14': ['F1150'],
        '15': ['F1059', 'F1076', 'F1120', 'F1155', 'F1162', 'F1200'],
    },
    '公衆': {
        '1': ['F1073', 'F1156', 'F1300'], '2': ['F1163'], '5': ['F1069'], '6': ['F1173'],
        '7': ['F1066', 'F1091', 'F128', 'F140'],
        '9': ['F1032', 'F1117', 'F1123', 'F1161', 'F1189', 'F137'], '11': ['F1057', 'F1134'],
    },
}
HOLD = ['F1126', 'F1148', 'F1159', 'F1160', 'F1288', 'F830', 'F840']

shutil.copy('lecture_map.json', 'lecture_map.json.bak_pre_e1remap')
lm = json.load(open('lecture_map.json', encoding='utf-8'))

total = 0
for subj, lecs in PLAN.items():
    for lec, pids in lecs.items():
        arr = list(lm[subj]['lectures'][lec]['ids'])
        add = 0
        for p in pids:
            if p not in arr:
                arr.append(p)
                add += 1
        lm[subj]['lectures'][lec]['ids'] = sorted(arr, key=lambda x: (1, x) if str(x)[:1] == 'F' else (0, x))
        total += add
    lm[subj]['lectures'] = {k: lm[subj]['lectures'][k] for k in sorted(lm[subj]['lectures'], key=lambda x: int(x))}

with open('lecture_map.json', 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2)
    f.write('\n')

# 検算
n = {subj: sum(len(v) for v in lecs.values()) for subj, lecs in PLAN.items()}
print(f"反映: 衛I={n['衛I']} 衛II={n['衛II']} 公衆={n['公衆']} 計{sum(n.values())}問 (追加{total})")
print(f"保留(範囲外): {len(HOLD)}問 {HOLD}")
