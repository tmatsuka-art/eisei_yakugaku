# -*- coding: utf-8 -*-
# 公衆衛生学を新設し、第3回（出生・死亡・寿命）11問を登録＋タグを E-1-1-(4) に
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_pubhealth03'
LM = 'lecture_map.json'
PIDS = ['099018','099126','100124','100125','101126','102124','103126','104122','105128','106016','110016']
AFTER = {'_subcat': '出生・死亡・寿命', 'new_corecurri_code': 'E-1-1-(4)', 'new_corecurri_code_source': 'manual_review'}

# 1) lecture_map に「公衆」科目を新設＋第3回
lm = json.load(open(LM, encoding='utf-8'))
if '公衆' not in lm:
    lm['公衆'] = {'label': '公衆衛生学', 'icon': '📊', 'color': '#10b981', 'lectures': {}}
lm['公衆']['lectures']['3'] = {'theme': '出生・死亡・寿命', 'ids': sorted(PIDS)}
with open(LM, 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2); f.write('\n')
print('科目:', list(lm.keys()), '/ 公衆-3:', len(lm['公衆']['lectures']['3']['ids']), '問')

# 2) jsonl タグ修正（バックアップ）
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
