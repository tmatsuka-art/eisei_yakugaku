# -*- coding: utf-8 -*-
# E-3未配置57問の再判定を3科目へ反映（範囲外15問は保留）
import sys, json, shutil
sys.stdout.reconfigure(encoding="utf-8")

PLAN = {
    '衛I': {
        '6': ['F260'], '10': ['F1055', 'F1104', 'F1184', 'F1185'], '11': ['F1079'],
        '12': ['F344'], '13': ['F1143'],
    },
    '衛II': {
        '3': ['F1107', 'F1137', 'F1167', 'F1208', 'F209'], '5': ['F1198'],
        '6': ['F031', 'F032', 'F033', 'F049', 'F1012', 'F1019', 'F1041', 'F1087', 'F1141',
              'F1145', 'F1165', 'F1175', 'F1199'],
        '9': ['F039', 'F1045', 'F1142', 'F1194', 'F1216', 'F1227', 'F164'], '10': ['F028'],
        '11': ['F180'], '12': ['F1112'], '14': ['F1260'], '15': ['F1114', 'F112'],
    },
    '公衆': {
        '1': ['F1307'], '9': ['F1125'],
    },
}
HOLD = ['F038', 'F1144', 'F1146', 'F1290', 'F616', 'F617', 'F618', 'F619', 'F620', 'F621',
        'F622', 'F623', 'F625', 'F658', 'F659']

shutil.copy('lecture_map.json', 'lecture_map.json.bak_pre_e3un')
lm = json.load(open('lecture_map.json', encoding='utf-8'))

total = 0
for subj, lecs in PLAN.items():
    for lec, pids in lecs.items():
        arr = list(lm[subj]['lectures'][lec]['ids'])
        for p in pids:
            if p not in arr:
                arr.append(p)
                total += 1
        lm[subj]['lectures'][lec]['ids'] = sorted(arr, key=lambda x: (1, x) if str(x)[:1] == 'F' else (0, x))
    lm[subj]['lectures'] = {k: lm[subj]['lectures'][k] for k in sorted(lm[subj]['lectures'], key=lambda x: int(x))}

with open('lecture_map.json', 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2)
    f.write('\n')

n = {subj: sum(len(v) for v in lecs.values()) for subj, lecs in PLAN.items()}
print(f"反映: 衛I={n['衛I']} 衛II={n['衛II']} 公衆={n['公衆']} 計{sum(n.values())}問 (追加{total})")
print(f"保留(範囲外): {len(HOLD)}問")
