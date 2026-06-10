# -*- coding: utf-8 -*-
# 毒性学 本体162問の判定反映：第1/2/4回(新設)＋第3/5/7回(回収)
import sys, json, shutil
sys.stdout.reconfigure(encoding="utf-8")

PLAN = {
    '1': ('毒性学概論・第I相代謝',
          ['F002', 'F006', 'F009', 'F511', 'F512', 'F513', 'F514', 'F515', 'F737', 'F739', 'F771', 'F1196', 'F1265']),
    '2': ('第II相・代謝因子・標的臓器',
          ['F001', 'F003', 'F008', 'F516', 'F517', 'F519', 'F520', 'F521', 'F524', 'F726', 'F727', 'F728',
           'F730', 'F731', 'F732', 'F733', 'F735', 'F736', 'F740', 'F799', 'F1275']),
    '4': ('解毒・生体防御',
          ['F518', 'F522', 'F523', 'F768', 'F1081', 'F1276']),
    '3': (None, ['F012', 'F013', 'F017', 'F019', 'F438', 'F1065', 'F1255']),
    '5': (None, ['F005', 'F1234']),
    '7': (None, ['F047', 'F048', 'F054', 'F070', 'F074', 'F075', 'F076', 'F080', 'F090']),
}

shutil.copy('lecture_map.json', 'lecture_map.json.bak_pre_toxico_main')
lm = json.load(open('lecture_map.json', encoding='utf-8'))
lectures = lm['衛II']['lectures']

for lec, (theme, pids) in PLAN.items():
    if lec not in lectures:
        lectures[lec] = {'theme': theme or '', 'ids': []}
        print(f"  （衛II-{lec} を新設）")
    elif theme and not lectures[lec].get('theme'):
        lectures[lec]['theme'] = theme
    ids = list(lectures[lec]['ids'])
    added = 0
    for p in pids:
        if p not in ids:
            ids.append(p)
            added += 1
    lectures[lec]['ids'] = sorted(ids, key=lambda x: (1, x) if str(x)[:1] == 'F' else (0, x))
    arr = lectures[lec]['ids']
    k = sum(1 for x in arr if str(x)[:1] != 'F')
    y = sum(1 for x in arr if str(x)[:1] == 'F')
    print(f"衛II-{lec} {lectures[lec]['theme']}: 計{len(arr)}問（過去問{k}＋予想{y}）, 今回追加{added}")

# 回番号順に整列
lm['衛II']['lectures'] = {k: lectures[k] for k in sorted(lectures, key=lambda x: int(x))}

with open('lecture_map.json', 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2)
    f.write('\n')
print("反映完了")
