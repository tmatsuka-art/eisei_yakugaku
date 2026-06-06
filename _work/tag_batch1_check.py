# -*- coding: utf-8 -*-
# 試しバッチ1：授業回10(廃棄物)に振り分け済みの16問のタグ現状を点検する
import json

# lecture_mapから廃棄物(衛II-10)のidsを取得
lm = json.load(open('lecture_map.json', encoding='utf-8'))
ids = set(lm['衛II']['lectures']['10']['ids'])
print(f"対象（衛II-10 廃棄物）: {len(ids)}問\n")

TARGET_CODE = 'E-3-2-(5)'   # 廃棄物の想定コード（要・新コアカリ分類案で確認）

rows = []
with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line)
        if o.get('problem_id') in ids:
            rows.append(o)
rows.sort(key=lambda o: o.get('problem_id'))

need_fix = 0
for o in rows:
    code = o.get('new_corecurri_code')
    sub = o.get('_subcat')
    flag = '' if code == TARGET_CODE else '  ★要修正'
    if code != TARGET_CODE:
        need_fix += 1
    print(f"{o.get('problem_id')} {o.get('display_title')}")
    print(f"    現状: _subcat={sub} | code={code} | src={o.get('new_corecurri_code_source')}{flag}")
    print(f"    本文: {(o.get('problem_text') or '')[:54]}")
print(f"\n現状コードが {TARGET_CODE} でないもの = {need_fix}問 / {len(rows)}問")
