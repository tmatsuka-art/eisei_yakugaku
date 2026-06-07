# -*- coding: utf-8 -*-
# 公衆衛生 感染症ブロック 第06/09/10回を lecture_map に登録＋タグを manual_review に。
# 08は過去問0のため作らない（予想問題で補う）。母子感染の病原体5問は06に入れ、12構築時に重複登録する（下記メモ）。
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_pubhealth_inf06-10'
LM = 'lecture_map.json'

# 回ごとの (theme, code, subcat, ids)
LECT = {
 '6':  ('感染症の病原体', 'E-1-2-(1)', '感染症の病原体', [
    '097129','097130','098124','099128','099233','100127','100237','101129','102018',
    '103129','104018','105130','106121','107123','110017','110230','109229',
    '100019','102019','105020','106123','108125',   # 母子感染の病原体5（06+12両方／12は後日）
    '105234','110124','104234',                      # サーベイ図06分2＋感染経路104234
 ]),
 '9':  ('感染症治療薬・サーベイランス', 'E-1-2-(7)', '感染症治療薬・サーベイランス', [
    '098128','099230','103233','109228','110233','111228',
    '108123','109121',                               # サーベイ図09分2
    '108228','111229','111232',                      # 境界D（結核臨床・MRSA・ノロ処理）
    '105232','107228',                               # インフル治療薬の実務
    '102233',                                        # 空気感染対策（院内）
 ]),
 '10': ('感染症 法制度', 'E-1-2-(5)', '感染症 法制度', [
    '098021','099019','100128','102127','105019','107122','108016',
    '102235',                                        # 全数把握対象（届出制度）
    '103235',                                        # インフル（法の比重大）
 ]),
}

# 1) lecture_map 更新
lm = json.load(open(LM, encoding='utf-8'))
for l, (theme, code, subcat, ids) in LECT.items():
    assert len(ids) == len(set(ids)), f'回{l} に重複pid'
    lm['公衆']['lectures'][l] = {'theme': theme, 'ids': sorted(ids)}
with open(LM, 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2); f.write('\n')
print('公衆の回:', sorted(lm['公衆']['lectures'].keys(), key=int))
for l in ['6','9','10']:
    print(f'  公衆-{l} {lm["公衆"]["lectures"][l]["theme"]}: {len(lm["公衆"]["lectures"][l]["ids"])}問')

# 2) タグ修正用 fixes 辞書
fixes = {}
for l, (theme, code, subcat, ids) in LECT.items():
    for pid in ids:
        fixes[pid] = {'_subcat': subcat, 'new_corecurri_code': code, 'new_corecurri_code_source': 'manual_review'}
print('タグ修正対象:', len(fixes), '問')

# 3) バックアップ
if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK); print('バックアップ作成:', BAK)
else:
    print('バックアップ既存（温存）:', BAK)

# 4) 区切り文字を検出（jsonl の体裁を保つ）
with open(SRC, encoding='utf-8') as f:
    sample = f.readline().rstrip('\n')
o0 = json.loads(sample)
if json.dumps(o0, ensure_ascii=False) == sample:
    seps = (', ', ': ')
elif json.dumps(o0, ensure_ascii=False, separators=(',', ':')) == sample:
    seps = (',', ':')
else:
    seps = (', ', ': ')

# 5) 該当行のみ書換
out, changed, seen = [], 0, set()
with open(SRC, encoding='utf-8') as f:
    for line in f:
        raw = line.rstrip('\n')
        if not raw.strip():
            out.append(raw); continue
        o = json.loads(raw); pid = o.get('problem_id')
        if pid in fixes:
            for k, v in fixes[pid].items():
                o[k] = v
            out.append(json.dumps(o, ensure_ascii=False, separators=seps)); changed += 1; seen.add(pid)
        else:
            out.append(raw)
with open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(out) + '\n')
print('タグ変更:', changed, '/ 期待', len(fixes))
print('見つからなかったpid:', set(fixes) - seen or 'なし')

# メモ: 12母子保健 構築時に必ず入れる母子感染（06と重複登録5＋12のみ5）
print('\n[12へ回す母子感染メモ]')
print('  06+12両方:', '100019 102019 105020 106123 108125')
print('  12のみ   :', '101130 103019 104125 107232 107233')
