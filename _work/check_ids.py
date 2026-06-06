# -*- coding: utf-8 -*-
# 指定 problem_id の本文・選択肢・現タグを表示（公衆衛生の回確定の精査用）
import json, sys

# 03 出生・死亡・寿命の仮分類11問
targets = sys.argv[1:] if len(sys.argv) > 1 else [
    '099018','099126','100124','100125','101126','102124','103126','104122','105128','106016','110016'
]
targets = set(targets)

rows = []
with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line)
        if o.get('problem_id') in targets:
            rows.append(o)
rows.sort(key=lambda o: o['problem_id'])

for o in rows:
    print(f"{o['problem_id']} {o.get('display_title')} | code={o.get('new_corecurri_code')} _subcat={o.get('_subcat')}")
    print(f"  Q: {(o.get('problem_text') or '').strip()[:78]}")
    for i, c in enumerate(o.get('choices') or [], 1):
        print(f"    {i}. {(c or '')[:52]}")
    print()
