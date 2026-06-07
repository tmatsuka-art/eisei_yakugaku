# -*- coding: utf-8 -*-
# 感染症(E-1-2)候補の全文を読みやすく書き出す。06/08/09/10 を1問ずつ手作業で振り分けるための材料。
# 既割当(07ワクチン等)は除外し、未割当の感染症候補だけを対象にする。
import json, re
from collections import defaultdict

SRC = 'hygiene_with_images_v4.jsonl'
LM = 'lecture_map.json'
OUT = '_work/infectious_dump.md'

lm = json.load(open(LM, encoding='utf-8'))
assigned = {}   # pid -> "科目-回 テーマ"
for k, kd in lm.items():
    for l, d in kd['lectures'].items():
        for p in d['ids']:
            assigned[p] = f"{k}-{l} {d['theme']}"

# 感染症らしさ（infectious_map.py と同じ広めの網）
INF = re.compile(r'感染症|病原体|細菌|ウイルス|真菌|原虫|プリオン|感染経路|人畜共通|人獣共通|'
                 r'新興|再興|検疫|結核|サーベイランス|再生産|耐性|院内感染|性感染症|梅毒|HIV|'
                 r'肝炎|インフルエンザ|麻疹|麻しん|風疹|風しん|ノロ|腸管出血|エボラ|MERS|デング|'
                 r'予防接種|ワクチン|日和見|不顕性|淋菌|クラミジア|消毒|滅菌|抗菌|抗ウイルス|'
                 r'感染|ペスト|コレラ|赤痢|百日咳|破傷風|ポリオ|HBV|HCV|HPV|垂直感染|飛沫|空気感染|接触感染')

# 回バケツのヒント（あくまで参考。本文で判断する）
KW = {
 '06病原体': r'病原体|細菌|ウイルス|真菌|原虫|プリオン|人畜共通|人獣共通|新興感染症|再興感染症|日和見|不顕性|性感染症|梅毒|淋菌|クラミジア|尖圭|ヘルペス|エボラ|MERS|デング|宿主|潜伏期',
 '07ワクチン': r'予防接種|ワクチン|生ワクチン|不活化|トキソイド|定期接種|任意接種|集団免疫|副反応',
 '08蔓延再生産': r'基本再生産|実効再生産|記述疫学|アウトブレイク|エンデミック|パンデミック|集団発生|流行曲線|飛沫感染|空気感染|接触感染|垂直感染|感染経路',
 '09治療薬監視': r'サーベイランス|発生動向|抗菌薬|抗ウイルス薬|耐性菌|MRSA|AMR|DOTS|治療薬|抗結核|消毒|滅菌|手指衛生',
 '10法制度': r'感染症法|検疫|一類|二類|三類|四類|五類|指定感染症|蔓延防止|就業制限|全数把握|定点把握|届出',
}
KWc = {k: re.compile(v) for k, v in KW.items()}

# 既に手作業で挙がっている「感染症法そのもの」候補
LAW_HINT = {'098021','099019','100128','102127','105019','107122','108016'}

records = []
with open(SRC, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        pid = o['problem_id']
        text = ' '.join([o.get('problem_text') or '', ' '.join(o.get('choices') or []), o.get('comment') or ''])
        if not INF.search(text):
            continue
        scores = {k: len(c.findall(text)) for k, c in KWc.items()}
        hint = ' '.join(f"{k}:{v}" for k, v in sorted(scores.items(), key=lambda x: -x[1]) if v) or '(無)'
        records.append({
            'pid': pid,
            'assigned': assigned.get(pid),
            'subcat': o.get('_subcat'),
            'code': o.get('new_corecurri_code'),
            'src': o.get('new_corecurri_code_source'),
            'imgs': o.get('num_images') or 0,
            'answer': o.get('answer'),
            'ptext': (o.get('problem_text') or '').strip(),
            'choices': o.get('choices') or [],
            'comment': (o.get('comment') or '').strip(),
            'hint': hint,
            'lawhint': pid in LAW_HINT,
        })

records.sort(key=lambda r: r['pid'])
todo = [r for r in records if not r['assigned']]
done = [r for r in records if r['assigned']]

lines = []
lines.append(f"# 感染症候補 全文ダンプ（{len(records)}問 / 未割当={len(todo)} 既割当={len(done)}）")
lines.append("")
lines.append("未割当を06/08/09/10に1問ずつ振り分ける。07ワクチン・02/03は確定済み。")
lines.append("ヒント列は機械スコア（参考のみ）。lawhint★は感染症法そのものの既出候補。")
lines.append("")
lines.append("---")
lines.append("## ■ 未割当（これを分類する）")
for r in todo:
    star = ' ★法' if r['lawhint'] else ''
    lines.append("")
    lines.append(f"### {r['pid']}{star}  [現:{r['subcat']} / {r['code']} / {r['src']}]  img={r['imgs']}")
    lines.append(f"- ヒント: {r['hint']}")
    lines.append(f"- 問題: {r['ptext']}")
    for i, c in enumerate(r['choices'], 1):
        lines.append(f"    {i}. {c}")
    lines.append(f"- 解答: {r['answer']}")
    if r['comment']:
        cm = r['comment'].replace('\n', ' ')
        lines.append(f"- 解説: {cm}")
lines.append("")
lines.append("---")
lines.append("## ■ 既割当（参考・分類済み）")
for r in done:
    lines.append(f"- {r['pid']}  →  {r['assigned']}   [現:{r['subcat']} / {r['code']}]")

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print('書き出し:', OUT)
print(f'感染症候補 計{len(records)} / 未割当{len(todo)} / 既割当{len(done)}')
print('未割当pid:', ' '.join(r['pid'] for r in todo))
