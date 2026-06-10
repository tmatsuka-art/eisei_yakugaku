# -*- coding: utf-8 -*-
# 食品E-2予想を衛Iへ反映（エージェント判定＋食中毒混入再分類＋機械割当、保留6問除外）
import sys, json, shutil
sys.stdout.reconfigure(encoding="utf-8")

# エージェント本文判定（栄養素1-4 / 食中毒10-11 / 添加物14-15 / アレルギーは全て13）
AGENT = {
    '1': ['F1102', 'F1118', 'F1131', 'F134', 'F221', 'F222', 'F1221', 'F229', 'F244', 'F461',
          'F486', 'F487', 'F488', 'F614', 'F653', 'F654', 'F760'],
    '2': ['F1127', 'F1271', 'F1273', 'F225', 'F226', 'F231', 'F232', 'F233', 'F234', 'F235',
          'F237', 'F239', 'F240', 'F241', 'F249', 'F465', 'F466', 'F467', 'F468', 'F469',
          'F470', 'F471', 'F472', 'F473', 'F474', 'F508', 'F509', 'F647', 'F648', 'F649',
          'F660', 'F751', 'F752', 'F762', 'F779', 'F780'],
    '3': ['F228', 'F236', 'F245', 'F246', 'F247', 'F248', 'F475', 'F476', 'F477', 'F478',
          'F479', 'F480', 'F629', 'F630', 'F631', 'F632', 'F651', 'F652', 'F761'],
    '4': ['F223', 'F224', 'F242', 'F243', 'F462', 'F463', 'F464', 'F481', 'F482', 'F483',
          'F484', 'F485', 'F497', 'F500', 'F501', 'F611', 'F612', 'F613', 'F624', 'F627',
          'F628', 'F650', 'F713', 'F718', 'F719', 'F722', 'F769'],
    '10': ['F1246', 'F1247', 'F1250', 'F292', 'F293', 'F294', 'F296', 'F300', 'F304', 'F417',
           'F418', 'F419', 'F420', 'F421', 'F422', 'F423', 'F424', 'F425', 'F427', 'F428',
           'F429', 'F459', 'F757', 'F778', 'F781', 'F782', 'F796'],
    '11': ['F1232', 'F1248', 'F291', 'F297', 'F426', 'F430', 'F431', 'F432', 'F433', 'F434', 'F435', 'F436'],
    '14': ['F1051', 'F1072', 'F1111', 'F1187', 'F309', 'F315', 'F317', 'F320', 'F447', 'F448', 'F774'],
    '15': ['F305', 'F308', 'F311', 'F312', 'F313', 'F314', 'F316', 'F318', 'F319', 'F445',
           'F446', 'F449', 'F450', 'F451', 'F452'],
    '13': ['F1000', 'F1101', 'F259', 'F280', 'F983', 'F321', 'F322', 'F323', 'F324', 'F325',
           'F326', 'F327', 'F329', 'F330', 'F333', 'F981', 'F982', 'F984', 'F985', 'F986',
           'F987', 'F988', 'F989', 'F990', 'F991', 'F992', 'F993', 'F994', 'F995', 'F996',
           'F997', 'F998', 'F999'],
}
# 食中毒_subcat混入の再分類
MISC = {
    '9': ['F1168', 'F299', 'F328'],
    '10': ['F1249', 'F302'],
    '13': ['F1261', 'F278', 'F301', 'F347'],
    '15': ['F307', 'F310'],
    '6': ['F279'],
}
HOLD = {'F1291', 'F1312'}  # 疫学計算（公衆寄り）→保留

# 機械割当（_subcat→衛I回）
SUBCAT_MAP = {
    '食事摂取基準': '5', '国民健康・栄養調査': '5', '保健機能食品': '6',
    '栄養管理・栄養療法': '7', '食品の変質と保存': '9', '食品中の有害物質': '12',
    '遺伝子組換え・ゲノム編集食品': '13', '食品安全行政': '13',
}
HOLD_SUBCAT = {'化学物質の体内動態', '有害化学物質', '感染症の予防・対策'}

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
for lec, ids in MISC.items():
    plan[lec].update(ids)
placed = set()
for s in plan.values():
    placed.update(s)

held = set(HOLD)
unmapped = []
with open('future_questions.jsonl', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if not o.get('new_corecurri_code', '').startswith('E-2'):
            continue
        pid = o['problem_id']
        if pid in assigned or pid in placed or pid in held:
            continue
        sc = o.get('_subcat', '')
        if sc in SUBCAT_MAP:
            plan[SUBCAT_MAP[sc]].add(pid)
        elif sc in HOLD_SUBCAT:
            held.add(pid)
        else:
            unmapped.append((pid, sc))

shutil.copy('lecture_map.json', 'lecture_map.json.bak_pre_e2')
total = 0
for lec in [str(i) for i in range(1, 16)]:
    ids = plan[lec]
    if not ids:
        continue
    arr = list(lm['衛I']['lectures'][lec]['ids'])
    add = 0
    for p in sorted(ids):
        if p not in arr:
            arr.append(p)
            add += 1
    lm['衛I']['lectures'][lec]['ids'] = sorted(arr, key=lambda x: (1, x) if str(x)[:1] == 'F' else (0, x))
    y = sum(1 for x in lm['衛I']['lectures'][lec]['ids'] if str(x)[:1] == 'F')
    total += add
    print(f"衛I-{lec} {lm['衛I']['lectures'][lec]['theme']}: 予想{y} (+{add})")

with open('lecture_map.json', 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2)
    f.write('\n')

print(f"\n反映合計: {total}問 / 保留: {len(held)}問 {sorted(held)}")
if unmapped:
    print(f"⚠ 未マップ {len(unmapped)}問: {unmapped}")
