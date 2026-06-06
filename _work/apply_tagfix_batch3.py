# -*- coding: utf-8 -*-
# バッチ3：下水。23問→E-3-2-(1)/下水、110139→E-3-2-(5)/環境法規（バックアップ込み）
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_tagfix_batch3'

AFTER_A = {'_subcat':'下水', 'new_corecurri_code':'E-3-2-(1)', 'new_corecurri_code_source':'manual_review'}
AFTER_B = {'_subcat':'環境法規', 'new_corecurri_code':'E-3-2-(5)', 'new_corecurri_code_source':'manual_review'}
PIDS_A = ['097139','097241','098136','099137','100024','100137','100138','101025',
          '101137','102138','103138','104023','104025','104133','105025','105138',
          '107024','108024','109137','109138','111025','111136','111137']
fixes = {p: AFTER_A for p in PIDS_A}
fixes['110139'] = AFTER_B

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
