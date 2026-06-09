# -*- coding: utf-8 -*-
# _subcat=水環境 の予想問題を 上水(12)/下水(13) に割当（water_split.py と同じ判定）
import json, re

UP = re.compile(r'浄水|上水道|水道水|残留塩素|塩素消毒|塩素処理|次亜塩素|クロラミン|クリプトスポリジウム|'
                r'凝集沈殿|急速ろ過|緩速ろ過|不連続点|トリハロメタン|硬度|軟水|飲料水|水道法|水質基準|ジアルジア')
DOWN = re.compile(r'活性汚泥|下水道|下水処理|BOD|生物化学的酸素|COD|化学的酸素|溶存酸素|富栄養化|水質汚濁|'
                  r'公共用水域|曝気|硝化|脱窒|高度処理|赤潮|アオコ|放流|嫌気|浮遊物質|SS|総窒素|総リン')

up, down = [], []
with open('future_questions.jsonl', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        o = json.loads(line)
        if o.get('_subcat') != '水環境': continue
        text = ' '.join([o.get('problem_text') or '', ' '.join(o.get('choices') or []), o.get('comment') or ''])
        u = len(UP.findall(text)); d = len(DOWN.findall(text))
        if u > d:   up.append(o['problem_id'])
        elif d > u: down.append(o['problem_id'])

lm = json.load(open('lecture_map.json', encoding='utf-8'))
for lec, pids in [('12', up), ('13', down)]:
    ids = list(lm['衛II']['lectures'][lec]['ids'])
    for p in pids:
        if p not in ids:
            ids.append(p)
    lm['衛II']['lectures'][lec]['ids'] = sorted(ids, key=lambda x: (1, x) if str(x)[:1] == 'F' else (0, x))

with open('lecture_map.json', 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2); f.write('\n')

for lec in ['12', '13']:
    arr = lm['衛II']['lectures'][lec]['ids']
    k = sum(1 for x in arr if str(x)[:1] != 'F'); y = sum(1 for x in arr if str(x)[:1] == 'F')
    print(f"衛II-{lec} {lm['衛II']['lectures'][lec]['theme']}: 計{len(arr)}問（過去問{k}＋予想{y}）")
print(f"上水追加 {len(up)}問 / 下水追加 {len(down)}問")
