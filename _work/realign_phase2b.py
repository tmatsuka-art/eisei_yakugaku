# -*- coding: utf-8 -*-
# フェーズ2b: 精査53問のうち明確分34問を新回へ割当、範囲外19問は保留記録
import json, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
path = 'lecture_map.json'
m = json.load(open(path, encoding='utf-8'))
pub = m['公衆']['lectures']

assign = {
    '2':  ['097018', '098127', '098235', '100239', '101232', '105237', '106120',
           '106240', '107230', '107231', '109239', '111016', '111123', '111124'],
    '5':  ['097017', '102128', '105021', '107125', '108122', '111122'],
    '7':  ['097233', '098129', '100235', '102020', '103237', '107124', '108124', '110125'],
    '8':  ['107232', '108236'],
    '9':  ['104019', '109226', '111245'],
    '10': ['111236'],
}
theme = {'2': '環境要因と予防', '5': '保健統計③ 生命表・平均寿命・死因',
         '7': '社会的影響・国際動向', '8': '母子保健',
         '9': '学校保健・高齢者保健', '10': '産業保健'}
hold = ['097232', '097235', '100245', '101124', '101231', '102231', '103016', '103224',
        '105119', '105123', '105226', '105228', '105229', '106020', '107127', '109019',
        '109135', '109237', '111126']

assigned = set()
for sub in m.values():
    for v in sub['lectures'].values():
        assigned.update(v['ids'])
allnew = [i for ids in assign.values() for i in ids]
dup = sorted({i for i in allnew if allnew.count(i) > 1})
conflict = [i for i in allnew if i in assigned]
overlap = sorted(set(allnew) & set(hold))
print('割当', len(allnew), '保留', len(hold), '| 重複', dup, '既割当衝突', conflict, '割当×保留', overlap)

if not dup and not conflict and not overlap:
    shutil.copy(path, path + '.bak_pre_pubhealth_phase2b')
    for k, ids in assign.items():
        if k in pub:
            for i in ids:
                if i not in pub[k]['ids']:
                    pub[k]['ids'].append(i)
        else:
            pub[k] = {'theme': theme[k], 'ids': ids}
    json.dump(m, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    db = {r['problem_id']: r for r in (json.loads(l) for l in open('hygiene_with_images_v4.jsonl', encoding='utf-8') if l.strip())}
    with open('_work/pubhealth_hold_outofscope.md', 'w', encoding='utf-8') as f:
        f.write('# 公衆衛生学 範囲外で保留した過去問（lecture_map未登録）\n\n')
        f.write('new_corecurri_codeはE-1だが、実物の公衆衛生学では扱わない領域（栄養・食品=衛生化学I／薬物治療／化学物質=衛II相当）。\n')
        f.write('将来 衛生化学I の回を整備する際に再検討する。\n\n')
        for pid in hold:
            r = db.get(pid, {})
            f.write(f'- {pid} [{r.get("_subcat")} / {r.get("new_corecurri_code")}] {(r.get("problem_text") or "")[:60]}\n')
    print('=> 書き込み完了 (backup: lecture_map.json.bak_pre_pubhealth_phase2b)')
    print('--- 公衆衛生学 全回の問題数（最終） ---')
    for k in sorted(pub, key=int):
        print(f'   新{k} {pub[k]["theme"]}: {len(pub[k]["ids"])}問')
else:
    print('=> 不整合のため中止（書き込みせず）')
