# -*- coding: utf-8 -*-
# バッチ6：環境カバーの漏れ6問のタグを整える（バックアップ込み）
import json, shutil, os

SRC = 'hygiene_with_images_v4.jsonl'
BAK = 'hygiene_with_images_v4.jsonl.bak_pre_tagfix_batch6'
MR = 'manual_review'
fixes = {
    '098137': {'_subcat': '大気環境',     'new_corecurri_code': 'E-3-2-(1)', 'new_corecurri_code_source': MR},
    '100139': {'_subcat': '大気環境',     'new_corecurri_code': 'E-3-2-(1)', 'new_corecurri_code_source': MR},
    '100140': {'_subcat': '騒音',         'new_corecurri_code': 'E-3-2-(1)', 'new_corecurri_code_source': MR},
    '109140': {'_subcat': '室内環境',     'new_corecurri_code': 'E-3-2-(1)', 'new_corecurri_code_source': MR},
    '111242': {'_subcat': '室内環境',     'new_corecurri_code': 'E-3-2-(1)', 'new_corecurri_code_source': MR},
    '101136': {'_subcat': '地球環境問題', 'new_corecurri_code': 'E-3-2-(1)', 'new_corecurri_code_source': MR},
}

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

print('変更件数:', changed, '/ 期待6')
miss = set(fixes) - seen
print('見つからなかったpid:', miss if miss else 'なし')
