# -*- coding: utf-8 -*-
# バッチ2：上水29問を E-3-2-(1) / _subcat=上水 に統一（バックアップ込み）
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_tagfix_batch2'

PIDS = ['097023','097138','097239','098024','098242','099020','099023','100136',
        '101243','102137','102242','102243','103024','103137','104132','105137',
        '106024','106244','107139','108023','108138','108243','109242','110023',
        '110024','110138','110206','111240','111241']
AFTER = {'_subcat':'上水',
         'new_corecurri_code':'E-3-2-(1)',
         'new_corecurri_code_source':'manual_review'}
fixes = {p: AFTER for p in PIDS}

if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK); print('バックアップ作成:', BAK)
else:
    print('バックアップ既存（温存）:', BAK)

# 元の整形を踏襲
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

print('変更件数:', changed, '/ 期待29')
miss = set(PIDS) - seen
print('見つからなかったpid:', miss if miss else 'なし')
