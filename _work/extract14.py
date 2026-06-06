# -*- coding: utf-8 -*-
import json

# 既存のlecture_map.jsonを読み、id→所属回の逆引きを作る
rev = {}
with open('lecture_map.json', encoding='utf-8') as f:
    lm = json.load(f)
for kamoku, kd in lm.items():
    for lec, ld in kd.get('lectures', {}).items():
        for pid in ld.get('ids', []):
            rev.setdefault(pid, []).append(f"{kamoku}-{lec}")

# 確認したい行番号（候補ID＋キーワードヒットの和集合）
target_lines = {9,43,53,73,111,121,134,148,194,195,217,236,258,277,317,343,362,406,453,499,521,522,540,568,586,587,626}

with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if i not in target_lines:
            continue
        o = json.loads(line)
        pid = o.get('problem_id')
        assigned = rev.get(pid, [])
        flag = ('★既出:' + ','.join(assigned)) if assigned else '（未割当）'
        img = o.get('num_images', 0)
        imgflag = f" [画像{img}枚]" if img else ""
        print(f"=== L{i} | {pid} | {flag}{imgflag} | subcat={o.get('_subcat')} | code={o.get('new_corecurri_code')} ===")
        print("Q:", (o.get('problem_text') or '').strip())
        for j, c in enumerate(o.get('choices') or [], 1):
            print(f"  {j}. {c}")
        print("A:", o.get('answer'))
        cm = (o.get('comment') or '').strip().replace('\n', ' ')
        print("解説:", cm[:260])
        print()
