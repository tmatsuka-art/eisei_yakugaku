# -*- coding: utf-8 -*-
# バッチ5：室内大気(衛II-15) 20問を E-3-2-(1)/室内環境 に統一（バックアップ込み）
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_tagfix_batch5'

AFTER = {'_subcat':'室内環境', 'new_corecurri_code':'E-3-2-(1)', 'new_corecurri_code_source':'manual_review'}
PIDS = ['097243','098138','099025','099139','101140','102024','102140','103140',
        '104024','104135','104244','106140','107141','107243','107244','107245',
        '108140','110242','111139','111243']
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

print('変更件数:', changed, '/ 期待20')
miss = set(PIDS) - seen
print('見つからなかったpid:', miss if miss else 'なし')
