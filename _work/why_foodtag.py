# -*- coding: utf-8 -*-
import json

# 本命＋同じ食品ラベルの大気問題＋108139の隣の問題
targets = ['108136','108137','108138','108139','108140',  # 108回の前後
           '106139','107140',                              # 同じ食品ラベルの大気問題
           '108022','108023','108024','108025']            # 108回の他の環境系(正しく分類?)
targets = set(targets)

fields = ['problem_id','q_no','section','category','_subcat',
          'new_corecurri_code','new_corecurri_code_source',
          'block_id','lead_id','dependent','needs_lead','note','display_title']

rows = []
with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line)
        if o.get('problem_id') in targets:
            rows.append(o)

rows.sort(key=lambda o: o.get('problem_id'))
for o in rows:
    print('-'*70)
    for k in fields:
        v = o.get(k)
        print(f"  {k}: {v}")
    qt = (o.get('problem_text') or '').strip().replace('\n',' ')
    print(f"  Q冒頭: {qt[:70]}")
