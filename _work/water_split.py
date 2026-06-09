# -*- coding: utf-8 -*-
# _subcat=水環境 の予想問題を、本文キーワードで上水(12)/下水(13)に仮振り分け
import json, re

UP = re.compile(r'浄水|上水道|水道水|残留塩素|塩素消毒|塩素処理|次亜塩素|クロラミン|クリプトスポリジウム|'
                r'凝集沈殿|急速ろ過|緩速ろ過|不連続点|トリハロメタン|硬度|軟水|飲料水|水道法|水質基準|ジアルジア')
DOWN = re.compile(r'活性汚泥|下水道|下水処理|BOD|生物化学的酸素|COD|化学的酸素|溶存酸素|富栄養化|水質汚濁|'
                  r'公共用水域|曝気|硝化|脱窒|高度処理|赤潮|アオコ|放流|嫌気|浮遊物質|SS|総窒素|総リン')

res = {'上水': [], '下水': [], '要確認': []}
with open('future_questions.jsonl', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        o = json.loads(line)
        if o.get('_subcat') != '水環境': continue
        text = ' '.join([o.get('problem_text') or '', ' '.join(o.get('choices') or []), o.get('comment') or ''])
        u = len(UP.findall(text)); d = len(DOWN.findall(text))
        pid = o['problem_id']; q = (o.get('problem_text') or '').strip()[:46]
        if u > d:   res['上水'].append((pid, q))
        elif d > u: res['下水'].append((pid, q))
        else:       res['要確認'].append((pid, u, d, q))

print(f"=== 上水(12) 仮: {len(res['上水'])}問 ===")
for pid, q in res['上水']: print(f"  {pid} | {q}")
print(f"=== 下水(13) 仮: {len(res['下水'])}問 ===")
for pid, q in res['下水']: print(f"  {pid} | {q}")
print(f"=== 要確認(同点) {len(res['要確認'])}問 ===")
for pid, u, d, q in res['要確認']: print(f"  {pid} (上{u}/下{d}) | {q}")
