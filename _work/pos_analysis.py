"""正答位置シャッフルの設計用分析。
複数選べ問題の正答位置分布を出し、「pos4/5を含まず動かす余地のある問題」と
「順序に意味がありそうな問題（年代順・数値順＝動かしてはいけない）」を仕分ける。
※この段階では一切変更しない。設計材料の収集のみ。
"""
import json
import re
from collections import Counter
from pathlib import Path

qs = []
for line in open('future_questions.jsonl', encoding='utf-8'):
    if line.strip():
        qs.append(json.loads(line))


def is_pure_number(c):
    """選択肢が数値・単位のみ（例: '0.5', '33.3 mL', '20 mg/kg食品'）か"""
    s = c.strip()
    # 数字を含み、かつ日本語の文章性が薄い（短い）
    return bool(re.search(r'\d', s)) and len(s) <= 12 and not re.search(r'[。、）]', s)


multi = []
for q in qs:
    ans = [int(a) for a in (q.get('answer') or []) if str(a).isdigit()]
    if len(ans) < 2:
        continue
    choices = q.get('choices') or []
    year_like = sum(1 for c in choices if re.search(r'(18|19|20)\d{2}\s*年?', c))
    pure_num = sum(1 for c in choices if is_pure_number(c))
    reviewed = bool(q.get('ai_review'))
    has_45 = any(a in (4, 5) for a in ans)
    order_risk = pure_num >= 3 or year_like >= 3
    multi.append({
        'pid': q['problem_id'], 'ans': ans, 'n': len(choices),
        'year': year_like, 'pnum': pure_num,
        'reviewed': reviewed, 'has_45': has_45, 'order_risk': order_risk,
        'title': q.get('display_title', ''),
    })

pos = Counter()
for m in multi:
    for a in m['ans']:
        pos[a] += 1
total = sum(pos.values())

out = []
out.append(f'複数選べ問題: {len(multi)}問（正答延べ {total}）')
out.append('正答位置分布: ' + ', '.join(f'pos{p}={pos[p]}({pos[p]/total*100:.1f}%)' for p in sorted(pos)))
out.append('')

movable = [m for m in multi if not m['has_45'] and not m['order_risk']]
order_problems = [m for m in multi if m['order_risk']]
out.append(f'■ 動かす候補（pos4/5を含まず・順序意味なし）: {len(movable)}問')
out.append(f'■ 順序に意味がありそう（除外候補）: {len(order_problems)}問')
out.append(f'■ 既にpos4/5を含む（対応不要）: {sum(1 for m in multi if m["has_45"])}問')
out.append('')
out.append('=== 動かす候補（正答を後方へ寄せられる）===')
for m in movable:
    out.append(f"{m['pid']}  正答{m['ans']}  選択肢{m['n']}  {m['title']}  {'[済]' if m['reviewed'] else '[未]'}")
out.append('')
out.append('=== 順序に意味がありそう（要人手確認・原則動かさない）===')
for m in order_problems:
    out.append(f"{m['pid']}  正答{m['ans']}  純数値{m['pnum']}/年代{m['year']}  {m['title']}")

Path('_work/pos_analysis_result.txt').write_text('\n'.join(out), encoding='utf-8')
print('複数選べ:', len(multi), '/ 動かす候補:', len(movable), '/ 順序意味:', len(order_problems))
print('pos:', {p: pos[p] for p in sorted(pos)})
