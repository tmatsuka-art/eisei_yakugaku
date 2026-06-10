# -*- coding: utf-8 -*-
# 公衆E-1の確実分389問を反映（エージェント判定＋機械割当）。混入62・異物4は除外。
import sys, json, shutil
sys.stdout.reconfigure(encoding="utf-8")

AGENT = {
    '2': ['F1223', 'F290', 'F573', 'F574', 'F575', 'F576', 'F590', 'F595', 'F605', 'F777',
          'F795', 'F895', 'F899'],
    '3': ['F571', 'F594'],
    '4': ['F568', 'F569', 'F589', 'F609', 'F776'],
    '5': ['F570', 'F572', 'F599', 'F600', 'F723'],
    '7': ['F1217', 'F1220', 'F1279', 'F1282', 'F1285', 'F1301', 'F1302', 'F1303', 'F1304',
          'F1305', 'F1306', 'F1309', 'F1310', 'F1311', 'F1314', 'F494', 'F495', 'F496', 'F503',
          'F504', 'F506', 'F577', 'F578', 'F579', 'F580', 'F597', 'F603', 'F606', 'F734', 'F765',
          'F893', 'F894', 'F896', 'F897', 'F898'],
    '11': ['F1028', 'F1094', 'F1136', 'F1218', 'F1239', 'F1252', 'F1320', 'F1321', 'F1322', 'F1323',
           'F364', 'F365', 'F387', 'F801', 'F802', 'F803', 'F804', 'F805', 'F806', 'F755',
           'F811', 'F832', 'F848', 'F1132', 'F357', 'F360', 'F361', 'F400', 'F831',
           'F040', 'F1021', 'F1022', 'F1023', 'F1027', 'F1195', 'F1263', 'F127', 'F1284', 'F359',
           'F405', 'F807', 'F808', 'F809', 'F810', 'F813', 'F814', 'F824', 'F834', 'F842',
           'F941', 'F942', 'F943', 'F944', 'F945', 'F946', 'F947', 'F948', 'F949', 'F950',
           'F951', 'F953', 'F954', 'F955', 'F956', 'F957', 'F958', 'F959', 'F960', 'F961',
           'F962', 'F963', 'F964', 'F965', 'F966', 'F967', 'F968', 'F970', 'F1024', 'F1025',
           'F1046', 'F1236', 'F135', 'F371'],
    '12': ['F372', 'F373', 'F374', 'F375', 'F406', 'F407', 'F819', 'F836', 'F847', 'F849',
           'F850', 'F969', 'F1062', 'F1191', 'F131', 'F366', 'F367', 'F369', 'F370', 'F399',
           'F754', 'F844'],
    '13': ['F389', 'F390', 'F401', 'F812', 'F362', 'F376', 'F377', 'F378', 'F379', 'F380',
           'F381', 'F382', 'F383', 'F384', 'F385', 'F386', 'F388', 'F397', 'F398', 'F815',
           'F816', 'F817', 'F820', 'F821', 'F822', 'F823', 'F825', 'F826', 'F827', 'F833',
           'F837', 'F838', 'F839', 'F841', 'F845', 'F846', 'F952', 'F1026', 'F1135', 'F1186',
           'F368', 'F402', 'F772'],
    '14': ['F1340', 'F358', 'F391', 'F392', 'F393', 'F394', 'F403', 'F408', 'F409', 'F410',
           'F756', 'F766', 'F773', 'F828', 'F829', 'F843', 'F901', 'F902', 'F903', 'F904',
           'F905', 'F906', 'F907', 'F908', 'F909', 'F910', 'F818', 'F1092', 'F1251', 'F132',
           'F395', 'F396', 'F404'],
}

SUBCAT_MAP = {  # 機械割当（_subcat→公衆回）
    '疫学': '1', '国際保健': '7', '母子保健': '8', '学校保健': '9', '産業保健': '10', '感染症総論': '11',
}
HOLD_SUBCAT = {'有害化学物質', '食中毒', '化学物質の体内動態'}  # 異物→保留

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

plan = {str(i): set() for i in range(1, 16)}
for lec, ids in AGENT.items():
    plan[lec].update(ids)
placed = set()
for s in plan.values():
    placed.update(s)

held = set()
remap = []  # 混入＝再判定対象
with open('future_questions.jsonl', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if not o.get('new_corecurri_code', '').startswith('E-1'):
            continue
        pid = o['problem_id']
        if pid in assigned or pid in placed:
            continue
        sc = o.get('_subcat', '')
        if sc in SUBCAT_MAP:
            plan[SUBCAT_MAP[sc]].add(pid)
        elif sc in HOLD_SUBCAT:
            held.add(pid)
        else:
            remap.append(pid)  # 生活習慣病part1,2の混入＋感染症X

shutil.copy('lecture_map.json', 'lecture_map.json.bak_pre_e1')
total = 0
for lec in [str(i) for i in range(1, 16)]:
    ids = plan[lec]
    if not ids:
        continue
    arr = list(lm['公衆']['lectures'][lec]['ids'])
    add = 0
    for p in sorted(ids):
        if p not in arr:
            arr.append(p)
            add += 1
    lm['公衆']['lectures'][lec]['ids'] = sorted(arr, key=lambda x: (1, x) if str(x)[:1] == 'F' else (0, x))
    y = sum(1 for x in lm['公衆']['lectures'][lec]['ids'] if str(x)[:1] == 'F')
    total += add
    print(f"公衆-{lec} {lm['公衆']['lectures'][lec]['theme']}: 予想{y} (+{add})")

with open('lecture_map.json', 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2)
    f.write('\n')

print(f"\n反映合計: {total}問")
print(f"再判定(混入): {len(remap)}問")
print(f"保留(異物): {len(held)}問 {sorted(held)}")
# 再判定リストを保存
with open('_work/e1_remap_ids.json', 'w', encoding='utf-8') as f:
    json.dump(sorted(remap), f, ensure_ascii=False)
