# -*- coding: utf-8 -*-
# 放射線の臨床（核医学・放射性医薬品）で、まだどの授業回にも入っていない問題を洗い出す
import json, re

lm = json.load(open('lecture_map.json', encoding='utf-8'))
assigned = set()
for k, kd in lm.items():
    for l, d in kd['lectures'].items():
        for p in d['ids']:
            assigned.add(p)

RAD = re.compile(r'放射性医薬品|シンチ|PET|SPECT|FDG|核医学|放射線治療|外部照射|内用療法|'
                 r'ストロンチウム|放射性同位体|テクネチウム|ヨウ素|\^\{131\}I|\^\{99m\}Tc|'
                 r'\^\{18\}F|\^\{90\}|\^\{89\}|オクトレオチド|ラジオ')

rows = []
with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line); pid = o['problem_id']
        if pid in assigned:
            continue
        text = ' '.join([o.get('problem_text') or '', ' '.join(o.get('choices') or []), o.get('comment') or ''])
        if RAD.search(text):
            rows.append(o)

rows.sort(key=lambda o: o['problem_id'])
print(f"放射線の臨床っぽい未割当: {len(rows)}件\n")
for o in rows:
    print(f"{o['problem_id']} {o.get('display_title')} | code={o.get('new_corecurri_code')} _subcat={o.get('_subcat')}")
    print(f"   Q: {(o.get('problem_text') or '').strip()[:62]}")
