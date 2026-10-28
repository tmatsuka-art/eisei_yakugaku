"""verify_fix3 の minor 指摘を rev_hold / fix_future / fix_past に反映（2026-10-23）。
NEW37・NEW38・F746・F747・F749 の指摘は、教科書（表III-3-6・III-3-7、GABA・CoQ10の項）で確認できるため変更しない。"""
import json
def L(p): return [json.loads(l) for l in open(p)]
def S(p, rows):
    with open(p, 'w') as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
def rp(s, a, b):
    assert s.count(a) == 1, a; return s.replace(a, b)
h = L('rev_hold.jsonl'); H = {r['page_id']: r for r in h}
q = H['NEW17']; assert q['choices'][3].startswith('難消化性デキストリンは、脂肪')
q['choices'][3] = '難消化性デキストリンは、食後の血中中性脂肪の上昇をおだやかにする。'
q = H['NEW26']; q['choices'][1] = 'ビタミンAは、妊娠を希望する女性では過剰摂取にならないよう注意が必要です。'
S('rev_hold.jsonl', h)
f = L('fix_future.jsonl'); F = {r['id']: r for r in f}
F['F255']['comment'] = rp(F['F255']['comment'], '販売予定日の60日前までに', '販売予定日の60日前まで（行政機関の休日を除いて数える）に')
F['F276']['comment'] = rp(F['F276']['comment'], 'ポイント：特保の表示は「〜が気になる方に適する」の形で、疾病の治療・予防はうたえない。疾病リスク低減表示はカルシウム・葉酸・DHA・EPAに限って認められている。',
    'ポイント：特保の表示は「〜が気になる方に適する」などの形で、疾病の治療・予防はうたえない。疾病リスク低減表示は、カルシウム・葉酸（規格基準）とDHA・EPA（個別審査）で認められている。')
F['F1128']['comment'] = rp(F['F1128']['comment'], '共通して強い抗酸化作用をもつ', '抗酸化作用をもつ')
S('fix_future.jsonl', f)
p = L('fix_past.jsonl'); P = {r['id']: r for r in p}
P['099229']['comment'] = rp(P['099229']['comment'], '区分は個別許可・規格基準型・疾病リスク低減表示・条件付き。', '区分は個別許可・規格基準型・疾病リスク低減表示・再許可等・条件付き。')
P['099229']['comment'] = rp(P['099229']['comment'], '疾病リスク低減表示、条件付き特定保健用食品の区分', '疾病リスク低減表示、再許可等、条件付き特定保健用食品の区分')
c = P['108019']['comment']
c = rp(c, '1：誤（対象成分ではない＝これが答え）。ナトリウムは栄養機能食品の対象成分ではなく、栄養機能表示はできない。', '1：正（これが答え）。ナトリウムは栄養機能食品の対象成分ではなく、栄養機能表示はできない。')
for n in '2345': c = rp(c, f'{n}：正（対象成分）。', f'{n}：誤。')
P['108019']['comment'] = c
P['111127']['comment'] = rp(P['111127']['comment'], 'メラニンの生合成を促進する作用はない。', 'メラニンの生合成を促進する成分として用いられるものではない。')
P['109129']['comment'] = rp(P['109129']['comment'], 'コンニャクはグルコマンナン。', 'コンニャクはグルコマンナン。脂肪の燃焼を促す成分ではない。')
S('fix_past.jsonl', p)
print('ok')
