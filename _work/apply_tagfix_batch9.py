# -*- coding: utf-8 -*-
# バッチ9：地球環境9。(1)影響・生態系13問、(4)国際動向5問（バックアップ込み）
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_tagfix_batch9'
A1 = {'_subcat': '地球環境問題', 'new_corecurri_code': 'E-3-2-(1)', 'new_corecurri_code_source': 'manual_review'}
A4 = {'_subcat': '地球環境問題', 'new_corecurri_code': 'E-3-2-(4)', 'new_corecurri_code_source': 'manual_review'}
P1 = ['097136','097137','099136','100023','100135','101135','101136','103136','104021','106023','106137','108021','108022']
P4 = ['101134','106138','108137','110137','111024']
fixes = {p: A1 for p in P1}
fixes.update({p: A4 for p in P4})

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
        o = json.loads(raw); pid = o.get('problem_id')
        if pid in fixes:
            for k, v in fixes[pid].items():
                o[k] = v
            out.append(json.dumps(o, ensure_ascii=False, separators=seps)); changed += 1; seen.add(pid)
        else:
            out.append(raw)

with open(SRC, 'w', encoding='utf-8', newline='') as f:
    f.write('\n'.join(out) + '\n')

print('変更件数:', changed, '/ 期待18')
print('見つからなかったpid:', set(fixes) - seen or 'なし')
