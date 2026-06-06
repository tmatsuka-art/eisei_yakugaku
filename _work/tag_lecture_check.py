# -*- coding: utf-8 -*-
# 汎用：指定した授業回に振り分け済みの問題の、現状タグ＋本文冒頭を一覧する
# 使い方: python _work/tag_lecture_check.py <回番号> [科目キー]  例: python _work/tag_lecture_check.py 12 衛II
import json, sys
from collections import Counter

lec = sys.argv[1] if len(sys.argv) > 1 else '12'
kamoku = sys.argv[2] if len(sys.argv) > 2 else '衛II'

lm = json.load(open('lecture_map.json', encoding='utf-8'))
ids = lm[kamoku]['lectures'][lec]['ids']
ids_set = set(ids)

rows = []
with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line)
        if o.get('problem_id') in ids_set:
            rows.append(o)
rows.sort(key=lambda o: o.get('problem_id'))

cc = Counter(o.get('new_corecurri_code') for o in rows)
src = Counter(o.get('new_corecurri_code_source') for o in rows)
print(f"{kamoku}-{lec}（{lm[kamoku]['lectures'][lec].get('theme')}）: {len(rows)}問")
print(f"現状コード分布: {dict(cc)}")
print(f"出どころ分布: {dict(src)}\n")
for o in rows:
    print(f"{o.get('problem_id')} {o.get('display_title')}")
    print(f"    _subcat={o.get('_subcat')} | code={o.get('new_corecurri_code')} | src={o.get('new_corecurri_code_source')}")
    print(f"    本文 {(o.get('problem_text') or '')[:58]}")
