# -*- coding: utf-8 -*-
# バッチ7：放射線・電磁波(衛II-11) 23問を E-3-2-(2)/放射線 に統一（バックアップ込み）
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_tagfix_batch7'

AFTER = {'_subcat': '放射線', 'new_corecurri_code': 'E-3-2-(2)', 'new_corecurri_code_source': 'manual_review'}
PIDS = ['098134','099022','099131','099239','100022','100134','101024','101241','102023',
        '102136','103135','103225','104131','105136','106136','107138','108136','108240',
        '109023','109024','110022','110136','111135']
fixes = {p: AFTER for p in PIDS}

if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK); print('バックアップ作成:', BAK)
else:
    print('バックアップ既存（温存）:', BAK)

with open(SRC, encoding='utf-8') as f:
    sample = f.readline().rstrip('\n')
o0 = json.loads(sample)
if json.dumps(o0, ensure_ascii=False) == sample:
    seps = (', ', ': ')
elif json.dumps(o0, ensure_ascii=False, separators=(',', ':')) == sample:
    seps = (',', ':')
else:
    seps = (', ', ': ')

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
            out.append(raw)

with open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(out) + '\n')

print('変更件数:', changed, '/ 期待23')
miss = set(PIDS) - seen
print('見つからなかったpid:', miss if miss else 'なし')
