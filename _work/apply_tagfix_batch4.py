# -*- coding: utf-8 -*-
# バッチ4：室外大気。22問→E-3-2-(1)/大気環境、106139→(5)/環境法規、109024→(2)/放射線
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_tagfix_batch4'

AFTER_A = {'_subcat':'大気環境', 'new_corecurri_code':'E-3-2-(1)', 'new_corecurri_code_source':'manual_review'}
AFTER_LAW = {'_subcat':'環境法規', 'new_corecurri_code':'E-3-2-(5)', 'new_corecurri_code_source':'manual_review'}
AFTER_RAD = {'_subcat':'放射線', 'new_corecurri_code':'E-3-2-(2)', 'new_corecurri_code_source':'manual_review'}

PIDS_A = ['097024','097245','098025','098140','099138','099240','100025','101138',
          '101139','102025','102139','103025','103139','104134','105139','107140',
          '108139','109025','109139','110025','110140','111138']
fixes = {p: AFTER_A for p in PIDS_A}
fixes['106139'] = AFTER_LAW
fixes['109024'] = AFTER_RAD

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

print('変更件数:', changed, '/ 期待24')
miss = set(fixes) - seen
print('見つからなかったpid:', miss if miss else 'なし')
