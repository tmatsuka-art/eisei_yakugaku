# -*- coding: utf-8 -*-
# 核医学・放射線臨床11問を 放射線11 に追加（lecture_map）＋タグを E-3-2-(2)/放射線 に統一
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_tagfix_batch8'
LM = 'lecture_map.json'
PIDS = ['097236','097237','100242','100243','104240','105242','105243',
        '106242','106243','109240','109241']
AFTER = {'_subcat': '放射線', 'new_corecurri_code': 'E-3-2-(2)', 'new_corecurri_code_source': 'manual_review'}

# 1) lecture_map 11 に追加（昇順）
lm = json.load(open(LM, encoding='utf-8'))
ids = list(lm['衛II']['lectures']['11']['ids'])
for p in PIDS:
    if p not in ids:
        ids.append(p)
lm['衛II']['lectures']['11']['ids'] = sorted(ids)
with open(LM, 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2); f.write('\n')
print('lecture_map 衛II-11:', len(lm['衛II']['lectures']['11']['ids']), '問')

# 2) jsonl タグ修正（バックアップ→該当行のみ書換）
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
fixes = {p: AFTER for p in PIDS}
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
print('タグ変更:', changed, '/ 期待11')
print('見つからなかったpid:', set(PIDS) - seen or 'なし')
