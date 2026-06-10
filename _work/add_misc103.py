# -*- coding: utf-8 -*-
# 対象外88問を公衆/衛II/衛Iの各回へ反映（範囲外15問は除外）
import sys, json, shutil
sys.stdout.reconfigure(encoding="utf-8")

PLAN = {
    '公衆': {
        '1': ['F020', 'F101', 'F102', 'F103', 'F104', 'F105', 'F106', 'F109', 'F110', 'F181',
              'F182', 'F184', 'F185', 'F186', 'F559', 'F1281', 'F1308', 'F1313'],
        '2': ['F121', 'F124', 'F125', 'F138', 'F1241', 'F1264', 'F1336', 'F1337'],
        '4': ['F1240'],
        '5': ['F122'],
        '6': ['F107', 'F108', 'F1338', 'F1339'],
        '7': ['F123', 'F129'],
        '8': ['F130'],
        '10': ['F065', 'F117', 'F142', 'F143', 'F144', 'F145', 'F146', 'F147', 'F149', 'F150'],
    },
    '衛II': {
        '9': ['F161', 'F167', 'F169', 'F187', 'F191', 'F196', 'F198', 'F199', 'F200', 'F212', 'F973', 'F1283'],
        '11': ['F171'],
        '12': ['F116'],
        '13': ['F163'],
        '14': ['F011'],
        '15': ['F016', 'F113', 'F139', 'F190', 'F1298'],
        '6': ['F100', 'F158', 'F189', 'F195', 'F215', 'F977', 'F978'],
    },
    '衛I': {
        '1': ['F1274'],
        '9': ['F1207'],
        '12': ['F437', 'F439', 'F440', 'F441', 'F442', 'F443', 'F444'],
        '13': ['F092', 'F133', 'F1213', 'F1243', 'F1286', 'F1289'],
    },
}

KOSHU_THEME = {
    '1': '公衆衛生学概論・疫学', '2': '環境要因と予防', '3': '保健統計① 人口統計',
    '4': '保健統計② 出生・死亡・年齢調整', '5': '保健統計③ 生命表・平均寿命・死因',
    '6': '保健統計④ 傷病統計・受療率・罹患率', '7': '社会的影響・国際動向', '8': '母子保健',
    '9': '学校保健・高齢者保健', '10': '産業保健',
}

shutil.copy('lecture_map.json', 'lecture_map.json.bak_pre_misc103')
lm = json.load(open('lecture_map.json', encoding='utf-8'))

for subj, lecs in PLAN.items():
    lectures = lm[subj]['lectures']
    for lec, pids in lecs.items():
        if lec not in lectures:
            theme = KOSHU_THEME.get(lec, '') if subj == '公衆' else ''
            lectures[lec] = {'theme': theme, 'ids': []}
            print(f"  （{subj}-{lec} を新設: {theme}）")
        ids = list(lectures[lec]['ids'])
        added = 0
        for p in pids:
            if p not in ids:
                ids.append(p)
                added += 1
        lectures[lec]['ids'] = sorted(ids, key=lambda x: (1, x) if str(x)[:1] == 'F' else (0, x))
        arr = lectures[lec]['ids']
        y = sum(1 for x in arr if str(x)[:1] == 'F')
        k = len(arr) - y
        print(f"{subj}-{lec} {lectures[lec]['theme']}: 計{len(arr)}（過去問{k}＋予想{y}）+{added}")
    lm[subj]['lectures'] = {k: lectures[k] for k in sorted(lectures, key=lambda x: int(x))}

with open('lecture_map.json', 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2)
    f.write('\n')
print("反映完了（88問）")
