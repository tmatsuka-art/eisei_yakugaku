# -*- coding: utf-8 -*-
# フェーズ2a: 未割当E-1問題のうち、_subcatが新回に明確対応するものを機械割当
import json, sys, collections, shutil
sys.stdout.reconfigure(encoding='utf-8')
path = 'lecture_map.json'
m = json.load(open(path, encoding='utf-8'))
pub = m['公衆']['lectures']

assigned = set()
for sub in m.values():
    for v in sub['lectures'].values():
        assigned.update(v['ids'])

rows = [json.loads(l) for l in open('hygiene_with_images_v4.jsonl', encoding='utf-8') if l.strip()]
e1 = [r for r in rows if str(r.get('new_corecurri_code') or '').startswith('E-1')]
un = [r for r in e1 if r['problem_id'] not in assigned]

# _subcat → 新回（1対1で明確なもののみ。曖昧な生活習慣病/保健統計は精査保留）
subcat_map = {'疫学': '1', '産業保健': '10', '母子保健': '8',
              '学校保健': '9', '国際保健': '7', '主要感染症': '11', '感染症総論': '11'}
theme = {'1': '公衆衛生学概論・疫学', '7': '社会的影響・国際動向', '8': '母子保健',
         '9': '学校保健・高齢者保健', '10': '産業保健', '11': '感染症概論・病原体・基本予防'}

add = collections.defaultdict(list)
left = []
for r in un:
    sc = r.get('_subcat')
    if sc in subcat_map:
        add[subcat_map[sc]].append(r['problem_id'])
    else:
        left.append(r)

shutil.copy(path, path + '.bak_pre_pubhealth_phase2a')
for k, ids in add.items():
    if k in pub:
        for i in ids:
            if i not in pub[k]['ids']:
                pub[k]['ids'].append(i)
    else:
        pub[k] = {'theme': theme[k], 'ids': sorted(ids)}
json.dump(m, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print('=== 機械割当（フェーズ2a） ===')
for k in sorted(add, key=int):
    print(f'  新{k} {theme[k]}: +{len(add[k])}問 (回計{len(pub[k]["ids"])}問)')
print(f'割当合計 {sum(len(v) for v in add.values())}問 / 精査保留 {len(left)}問')
print('--- 精査保留の_subcat別 ---')
for k, v in collections.Counter(r.get('_subcat') for r in left).most_common():
    print(f'  {k}: {v}')
