# -*- coding: utf-8 -*-
# 予想問題（廃棄物）20問を 衛II-10 の lecture_map ids に追加（jsonlタグは触らない）
import json

LM = 'lecture_map.json'
PIDS = ['F1056','F1119','F119','F1203','F1287','F194','F201','F202','F208','F678',
        'F679','F680','F709','F800','F883','F884','F885','F886','F887','F888']

lm = json.load(open(LM, encoding='utf-8'))
ids = list(lm['衛II']['lectures']['10']['ids'])
before = len(ids)
for p in PIDS:
    if p not in ids:
        ids.append(p)

# 過去問(数字始まり)を先、予想問題(F始まり)を後ろに整列
def keyf(x):
    return (1, x) if x[:1] == 'F' else (0, x)
lm['衛II']['lectures']['10']['ids'] = sorted(ids, key=keyf)

with open(LM, 'w', encoding='utf-8') as f:
    json.dump(lm, f, ensure_ascii=False, indent=2); f.write('\n')

after = len(lm['衛II']['lectures']['10']['ids'])
kako = sum(1 for x in lm['衛II']['lectures']['10']['ids'] if x[:1] != 'F')
yoso = sum(1 for x in lm['衛II']['lectures']['10']['ids'] if x[:1] == 'F')
print(f"衛II-10: {before}問 → {after}問（過去問{kako}＋予想{yoso}）")
