# -*- coding: utf-8 -*-
# 感染症(E-1-2)全体マップ：未割当の感染症問題を 06/08/09/10 に仮分類（07ワクチンは確定済み）
import json, re
from collections import defaultdict

lm = json.load(open('lecture_map.json', encoding='utf-8'))
assigned = set()
for k, kd in lm.items():
    for l, d in kd['lectures'].items():
        for p in d['ids']:
            assigned.add(p)

INF = re.compile(r'感染症|病原体|細菌|ウイルス|真菌|原虫|プリオン|感染経路|人畜共通|人獣共通|'
                 r'新興|再興|検疫|結核|サーベイランス|再生産|耐性|院内感染|性感染症|梅毒|HIV|'
                 r'肝炎|インフルエンザ|麻疹|麻しん|風疹|風しん|ノロ|腸管出血|エボラ|MERS|デング')
KW = {
 '06_病原体(E-1-2-1)': r'病原体|細菌|ウイルス|真菌|原虫|プリオン|感染経路|人畜共通|人獣共通|新興感染症|再興感染症|日和見|不顕性|性感染症|梅毒|淋菌|クラミジア|尖圭|ヘルペス|エボラ|MERS|デング',
 '08_蔓延・再生産数(E-1-2-3)': r'基本再生産|実効再生産|記述疫学|アウトブレイク|エンデミック|パンデミック|集団発生|流行曲線',
 '09_治療薬・サーベイランス': r'サーベイランス|発生動向|抗菌薬|抗ウイルス薬|耐性菌|MRSA|AMR|DOTS|治療薬|抗結核',
 '10_法制度(E-1-2-5)': r'感染症法|検疫|一類|二類|三類|四類|五類|指定感染症|蔓延防止|就業制限|全数把握|定点把握',
}
KWc = {k: re.compile(v) for k, v in KW.items()}

themap = defaultdict(list); unmatched = []
with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line); pid = o['problem_id']
        if pid in assigned:
            continue
        text = ' '.join([o.get('problem_text') or '', ' '.join(o.get('choices') or []), o.get('comment') or ''])
        if not INF.search(text):
            continue
        scores = {k: len(c.findall(text)) for k, c in KWc.items()}
        best = max(scores, key=scores.get)
        if scores[best] == 0:
            unmatched.append(pid); continue
        themap[best].append(pid)

for k in sorted(KW):
    ids = sorted(themap[k])
    print(f"[{k}] {len(ids)}問")
    print('   ', ' '.join(ids))
print(f"\n感染症だが回未判定: {len(unmatched)}問")
print('   ', ' '.join(sorted(unmatched)))
