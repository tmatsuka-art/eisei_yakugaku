# -*- coding: utf-8 -*-
# 試しバッチ1：廃棄物15問のタグを E-3-2-(5) に揃える（バックアップ込み）
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_tagfix_batch1'

PIDS = ['097025','098139','098245','099140','099245','101245','102245','103245',
        '104136','105245','106025','107025','109141','110245','111140']
AFTER = {'_subcat':'廃棄物・リサイクル',
         'new_corecurri_code':'E-3-2-(5)',
         'new_corecurri_code_source':'manual_review'}
fixes = {p: AFTER for p in PIDS}

# 1) バックアップ（既にあれば上書きしない）
if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK)
    print('バックアップ作成:', BAK)
else:
    print('バックアップ既存（温存）:', BAK)

# 元の整形（区切り文字）を検出して、変更行も同じ整形で書く
with open(SRC, encoding='utf-8') as f:
    sample = f.readline().rstrip('\n')
o0 = json.loads(sample)
if json.dumps(o0, ensure_ascii=False) == sample:
    seps = (', ', ': ')
elif json.dumps(o0, ensure_ascii=False, separators=(',', ':')) == sample:
    seps = (',', ':')
else:
    seps = (', ', ': ')
print('検出した整形 separators:', seps)

# 2) 変更行だけ書き換え、無変更行は原文のまま温存
out, changed, seen = [], 0, set()
with open(SRC, encoding='utf-8') as f:
    for line in f:
        raw = line.rstrip('\n')
        if not raw.strip():
            out.append(raw); continue
        o = json.loads(raw)
        pid = o.get('problem_id')
        if pid in fixes:
            for k, v in fixes[pid].items():
                o[k] = v
            out.append(json.dumps(o, ensure_ascii=False, separators=seps))
            changed += 1; seen.add(pid)
        else:
            out.append(raw)  # 触らない

with open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(out) + '\n')

print('変更件数:', changed, '/ 期待15')
miss = set(PIDS) - seen
print('見つからなかったpid:', miss if miss else 'なし')
