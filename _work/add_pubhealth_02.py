# -*- coding: utf-8 -*-
# 公衆衛生 第2回（人口統計）11問を登録＋タグを E-1-1-(4) に
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_pubhealth02'
LM = 'lecture_map.json'
PIDS = ['097125','098018','098125','100018','103125','104020','105129','107120','109123','109124','111121']
AFTER = {'_subcat': '人口統計', 'new_corecurri_code': 'E-1-1-(4)', 'new_corecurri_code_source': 'manual_review'}

# 1) lecture_map 公衆-2
lm = json.load(open(LM, encoding='utf-8'))
lm['公衆']['lectures']['2'] = {'theme': '人口統計', 'ids': sorted(PIDS)}
with open(LM, 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2); f.write('\n')
print('公衆-2:', len(lm['公衆']['lectures']['2']['ids']), '問 / 公衆の回:', sorted(lm['公衆']['lectures'].keys()))

# 2) jsonl タグ（バックアップ）
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
