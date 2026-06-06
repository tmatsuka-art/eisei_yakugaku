# -*- coding: utf-8 -*-
# 過去問タグ(new_corecurri_code)の機械推定状況と、本文との明らかな食い違いの規模を測る
import json, re
from collections import Counter, defaultdict

# 領域別の代表キーワード（本文＝problem_text+choices+comment を対象に粗く判定）
KW = {
 'E-3': r'大気汚染|光化学|オキシダント|逆転層|窒素酸化物|硫黄酸化物|浮遊粒子|微小粒子|PM2\.5|ばい煙|粉じん|石綿|廃棄物|マニフェスト|バーゼル|３Ｒ|3R|放射性|放射線|被ば|被曝|半減期|オゾン層|温暖化|地球環境|生物濃縮|POPs|水質汚濁|下水|上水|浄水|塩素消毒|残留塩素|BOD|COD|溶存酸素|富栄養化|ダイオキシン|有機溶剤|化審法|化管法|シックハウス|ホルムアルデヒド|カタ冷却',
 'E-2': r'食中毒|細菌性食中毒|ウイルス性|ノロ|サルモネラ|カンピロ|ボツリヌス|自然毒|フグ毒|テトロドトキシン|マイコトキシン|アフラトキシン|食品添加物|保存料|甘味料|防カビ|酸化防止剤|発色剤|着色料|変質|腐敗|メイラード|油脂|過酸化物価|酸価|栄養|ビタミン|ミネラル|アミノ酸スコア|生物価|特定保健用|機能性表示|HACCP|遺伝子組換え食品',
 'E-1': r'疫学|罹患率|有病率|オッズ比|相対危険|寄与危険|コホート|症例対照|感染症法|予防接種|ワクチン|再生産数|人口動態|出生率|合計特殊|死亡率|年齢調整|平均寿命|健康日本21|母子保健|学校保健|産業保健|労働安全衛生|職業性|受動喫煙',
}
KWc = {k: re.compile(v) for k,v in KW.items()}

def code_domain(code):
    if not code: return None
    m = re.match(r'(E-\d)', code)
    return m.group(1) if m else None

def text_domain(text):
    # 各領域キーワードのヒット数を数え、最多領域を推定（差が無ければNone）
    counts = {k: len(c.findall(text)) for k,c in KWc.items()}
    best = max(counts, key=counts.get)
    if counts[best] == 0: return None, counts
    # 2位と差が無い（同点）なら判定保留
    ordered = sorted(counts.values(), reverse=True)
    if len(ordered) > 1 and ordered[0] == ordered[1]: return None, counts
    return best, counts

src_counter = Counter()
sec_src = defaultdict(Counter)
mismatches = []
total = 0
with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line)
        total += 1
        src = o.get('new_corecurri_code_source')
        src_counter[src] += 1
        sec_src[o.get('section')][src] += 1
        text = ' '.join([o.get('problem_text') or '',
                         ' '.join(o.get('choices') or []),
                         o.get('comment') or ''])
        cd = code_domain(o.get('new_corecurri_code'))
        td, counts = text_domain(text)
        if cd and td and cd != td:
            mismatches.append((o.get('problem_id'), o.get('display_title'),
                               cd, td, o.get('_subcat'), src,
                               (o.get('problem_text') or '')[:46]))

print(f"総問題数: {total}")
print(f"タグの出どころ内訳: {dict(src_counter)}")
print(f"section×出どころ: ", {s: dict(c) for s,c in sec_src.items()})
print(f"\n本文と明らかに食い違うコード（粗い自動検出）: {len(mismatches)}問")
print("内訳(コード領域→本文推定領域):", Counter((m[2],m[3]) for m in mismatches))
print("\n--- 例（最大25件）---")
for pid, title, cd, td, sub, src, q in sorted(mismatches)[:25]:
    print(f"{pid} {title} | コード={cd} 本文推定={td} | _subcat={sub} | {src}")
    print(f"     {q}")
