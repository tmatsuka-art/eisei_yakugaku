"""授業スライド掲載問題（PPT掲載問題）26問を future_questions.jsonl と lecture_map.json に追加する（2026-10-15）。
python3 apply_ppt.py [--apply]
"""
import json, sys, copy, shutil, os
sys.path.insert(0, os.path.dirname(__file__))
from ppt_items import ITEMS

R = '/home/claude/eisei_yakugaku/'
W = R + '_work/ppt_lec2to5/'
FIG = '/tmp/claude-0/-home-claude/0cdc883f-e33a-5f78-abd9-6dec70e9de4e/scratchpad/ppt/'
APPLY = '--apply' in sys.argv
TODAY = '2026-10-15'
SUB = {2: '栄養素の機能', 3: '栄養素の機能', 4: '栄養素の機能', 5: '食事摂取基準'}
OLD = {2: 'D-2-a', 3: 'D-2-a', 4: 'D-2-a', 5: 'D-2-b'}

rows = [json.loads(l) for l in open(R + 'future_questions.jsonl') if l.strip()]
ids = {r['problem_id'] for r in rows}
tmpl = next(r for r in rows if r['problem_id'] == 'F1503')
no = max(int(i[1:]) for i in ids) + 1
new, log = [], []
for it in ITEMS:
    pid = f'F{no}'; no += 1
    r = copy.deepcopy(tmpl)
    r.pop('ai_review', None)
    fig = it.get('fig')
    sel = len(it['answer'])
    assert all(1 <= a <= len(it['choices']) for a in it['answer'])
    assert (f'{sel}つ選べ' in it['text']), (it['key'], it['text'])
    note = f"衛生化学I 演習問題集（授業スライド掲載問題）{it['src']}"
    if it.get('past'):
        note += f"。国試 第{int(it['past'][:3])}回 問{int(it['past'][3:])}と同じ（または一部改変）"
    r.update(problem_id=pid, q_no=no - 1, display_title=f'予想問題 {pid}', problem_text=it['text'], choices=it['choices'],
             answer=[str(a) for a in it['answer']], comment=it['comment'], note=note, section='理論',
             text_only=not fig, num_images=1 if fig else 0, num_images_detected=1 if fig else 0,
             assets=[f'FUTURE/{pid}.png'] if fig else [], _category='栄養',
             _subcat=it.get('subcat') or SUB[it['lec']], corecurri_code=OLD[it['lec']], new_corecurri_code=it['code'],
             has_explanation=True, tags=['PPT掲載'])
    r['source'] = {'kind': 'ppt_slide', 'lecture': f"衛I-{it['lec']}", 'item': it['src'], 'added': TODAY}
    if it.get('fixed'):
        r['source']['changed'] = it['fixed']
    new.append((it, r))
    log.append(f"{pid} 第{it['lec']}回 {it['src']}{' 図あり' if fig else ''}{'（' + it['fixed'] + '）' if it.get('fixed') else ''}")

lm = json.load(open(R + 'lecture_map.json'))
L = lm['衛I']['lectures']
for it, r in new:
    L[str(it['lec'])]['ids'].append(r['problem_id'])

print('\n'.join(log))
print('追加', len(new), '→ 合計', len(rows) + len(new))
json.dump({it['key']: r['problem_id'] for it, r in new}, open(W + 'id_map.json', 'w'), ensure_ascii=False, indent=1)
if APPLY:
    shutil.copy(R + 'future_questions.jsonl', R + 'future_questions.jsonl.bak_pre_ppt_20261015')
    shutil.copy(R + 'lecture_map.json', R + 'lecture_map.json.bak_pre_ppt_20261015')
    with open(R + 'future_questions.jsonl', 'a') as f:
        for _, r in new:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    json.dump(lm, open(R + 'lecture_map.json', 'w'), ensure_ascii=False, indent=2)
    for it, r in new:
        if it.get('fig'):
            shutil.copy(FIG + it['fig'], R + f"FUTURE/{r['problem_id']}.png")
    print('反映しました')
