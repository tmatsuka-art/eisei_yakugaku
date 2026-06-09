# -*- coding: utf-8 -*-
# 予想問題E-3系：明確な4回(放射線/大気/室内/地球環境)を、_subcatと期待コードの整合でチェック
import json
from collections import defaultdict

# _subcat → (授業回, 期待コード接頭)
MAP = {
    '放射線':       ('11', ('E-3-2-(2)',)),
    '大気環境':     ('14', ('E-3-2-(1)',)),
    '室内環境':     ('15', ('E-3-2-(1)',)),
    '地球環境問題': ('9',  ('E-3-2-(1)', 'E-3-2-(4)')),
}
res = defaultdict(lambda: {'ok': [], 'check': []})
with open('future_questions.jsonl', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line: continue
        o = json.loads(line); s = o.get('_subcat')
        if s not in MAP: continue
        lec, exp = MAP[s]; code = o.get('new_corecurri_code', '')
        pid = o['problem_id']; q = (o.get('problem_text') or '').strip()[:42]
        if code in exp:
            res[s]['ok'].append(pid)
        else:
            res[s]['check'].append((pid, code, q))

for s in MAP:
    lec, _ = MAP[s]; r = res[s]
    print(f"=== {s} → 衛II-{lec}: 整合{len(r['ok'])}問 ＋ 要確認{len(r['check'])}問 ===")
    for pid, code, q in r['check']:
        print(f"  [要確認] {pid} | {code} | {q}")
