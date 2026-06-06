# -*- coding: utf-8 -*-
# 環境保健(E-3-2)のカバー確認：環境キーワードを含むが衛II-9〜15に未割当の過去問を洗い出す
import json, re
from collections import Counter

lm = json.load(open('lecture_map.json', encoding='utf-8'))
assigned = set()
for lec, d in lm['衛II']['lectures'].items():
    for pid in d['ids']:
        assigned.add(pid)
print(f"衛II-9〜15 に割当済み（ユニーク）: {len(assigned)}問\n")

ENV = re.compile(
    r'大気汚染|光化学|オキシダント|PM2\.5|微小粒子|浮遊粒子|窒素酸化物|硫黄酸化物|逆転層|ばい煙|'
    r'粉じん|石綿|アスベスト|廃棄物|マニフェスト|バーゼル|リサイクル|放射性|放射線|被ば|被曝|半減期|'
    r'電離放射線|紫外線|オゾン層|温暖化|温室効果|生物濃縮|生態系|POPs|残留性有機|生物多様性|'
    r'上水|下水|浄水|水道|塩素消毒|残留塩素|BOD|COD|溶存酸素|富栄養化|水質汚濁|公共用水域|'
    r'環境基準|典型七公害|環境基本法|公害|シックハウス|室内環境|換気|カタ冷却|必要換気量|'
    r'建築物環境衛生|感覚温度|不快指数|WBGT|暑さ指数|地球環境|オゾン')
CHEM_MGMT = re.compile(r'化審法|化管法|PRTR|特定化学物質の環境への排出')
TOX = re.compile(r'シトクロムP450|CYP|抱合|メタロチオネイン|発がん|変異原|Ames|エームス|'
                 r'覚醒剤|大麻|麻薬|乱用|依存|解毒剤|キレート|農薬|有機リン|パラコート|'
                 r'カドミウム|水銀|鉛|ヒ素|クロム|ダイオキシン|PCB|有機溶剤|ベンゼン')

rows = []
with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line)
        pid = o.get('problem_id')
        if pid in assigned:
            continue
        text = ' '.join([o.get('problem_text') or '', ' '.join(o.get('choices') or []), o.get('comment') or ''])
        if not ENV.search(text):
            continue
        env_hits = Counter(ENV.findall(text))
        rows.append((pid, o.get('display_title'), o.get('new_corecurri_code'),
                     bool(CHEM_MGMT.search(text)), len(TOX.findall(text)),
                     [w for w, _ in env_hits.most_common(4)],
                     (o.get('problem_text') or '').strip()[:52]))

rows.sort(key=lambda r: r[0])
print(f"環境キーワードを含むが 9〜15 に未割当: {len(rows)}件")
print("（[管]=化審法/化管法系の保留候補、tox=毒性学キーワード数）\n")
for pid, title, code, chem, tox, top, q in rows:
    flags = ('[管]' if chem else '') + (f'[tox{tox}]' if tox else '')
    print(f"{pid} {title} | code={code} {flags}")
    print(f"   env語:{top}")
    print(f"   Q: {q}")
