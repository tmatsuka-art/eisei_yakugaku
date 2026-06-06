# -*- coding: utf-8 -*-
# 公衆衛生(E-1)の全体マップ（粗い仮分類）：未割当問題を15回キーワードで仮振り分け
import json, re
from collections import defaultdict

lm = json.load(open('lecture_map.json', encoding='utf-8'))
assigned = set()
for k, kd in lm.items():
    for l, d in kd['lectures'].items():
        for p in d['ids']:
            assigned.add(p)

KW = {
 '01_健康/統計/疫学概論': r'公衆衛生|健康の定義|プライマリ・?ヘルスケア|ヘルスプロモーション|オタワ憲章|包括的医療|罹患率|有病率|受療率|国民生活基礎調査|患者調査',
 '02_人口統計': r'人口統計|人口動態|人口静態|国勢調査|年齢3区分|人口ピラミッド|老年人口|生産年齢人口|総人口',
 '03_出生死亡寿命': r'出生率|合計特殊出生率|粗死亡率|年齢調整死亡率|標準化死亡比|平均寿命|平均余命|乳児死亡|周産期死亡|死因',
 '04_疫学デザイン': r'症例対照|コホート|要因対照|横断研究|介入研究|オッズ比|相対危険|寄与危険|交絡|バイアス|スクリーニング|敏感度|特異度|疫学の3要因',
 '05_予防/健康増進': r'一次予防|二次予防|三次予防|健康日本21|健康増進法|行動変容|特定健康診査|特定保健指導|メタボリック',
 '06_感染症病原体': r'人畜共通|人獣共通|新興感染症|再興感染症|日和見感染|プリオン|不顕性感染',
 '07_予防接種ワクチン': r'予防接種|ワクチン|生ワクチン|不活化ワクチン|定期接種|任意接種|トキソイド|集団免疫',
 '08_感染蔓延/再生産数': r'基本再生産|実効再生産|パンデミック|記述疫学|飛沫感染|空気感染|接触感染|垂直感染',
 '09_治療薬/サーベイランス': r'サーベイランス|発生動向調査|抗菌薬|抗ウイルス薬|耐性菌|院内感染',
 '10_感染症法制度': r'感染症法|検疫|一類感染症|二類感染症|三類感染症|四類感染症|五類感染症|結核|指定感染症|蔓延防止',
 '11_生活習慣病/喫煙飲酒': r'悪性新生物|心疾患|脳血管疾患|高血圧|糖尿病|脂質異常|喫煙|受動喫煙|ニコチン|飲酒|アルコール|ブリンクマン',
 '12_母子保健': r'母子保健|健やか親子|新生児マススクリーニング|母子感染|妊産婦|乳幼児健診|母子健康手帳',
 '13_社会環境要因': r'学校保健安全法|学校薬剤師|地域包括ケア|社会的決定要因',
 '14_産業保健法制度': r'労働基準法|労働安全衛生法|職業性疾[病患]|作業環境測定|特殊健康診断|じん肺|VDT|過労死|労災|トルエン',
}
KWc = {k: re.compile(v) for k, v in KW.items()}

themap = defaultdict(list)
unmatched = []
with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line); pid = o['problem_id']
        if pid in assigned:
            continue
        text = ' '.join([o.get('problem_text') or '', ' '.join(o.get('choices') or []), o.get('comment') or ''])
        scores = {k: len(c.findall(text)) for k, c in KWc.items()}
        best = max(scores, key=scores.get)
        if scores[best] == 0:
            unmatched.append(pid); continue
        themap[best].append(pid)

total = 0
for k in sorted(KW):
    ids = sorted(themap[k]); total += len(ids)
    print(f"[{k}] {len(ids)}問")
    print('   ', ' '.join(ids))
print(f"\n仮分類できた合計: {total}問 / 未マッチ(公衆衛生外＝衛I・毒性学など): {len(unmatched)}問")
