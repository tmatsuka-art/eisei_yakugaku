# -*- coding: utf-8 -*-
# 公衆衛生学 lecture_map を実物の回構成へ再配置（旧2/3/6/7/9/10 → 新3/4/5/11/12/13/14）
import json, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
path = 'lecture_map.json'
m = json.load(open(path, encoding='utf-8'))
pub = m['公衆']['lectures']
old2, old3, old6 = pub['2']['ids'], pub['3']['ids'], pub['6']['ids']
old7, old9, old10 = pub['7']['ids'], pub['9']['ids'], pub['10']['ids']

new_lectures = {
    '3':  {'theme': '保健統計① 人口統計',
           'ids': old2 + ['099126', '104122', '110016']},
    '4':  {'theme': '保健統計② 出生・死亡・年齢調整',
           'ids': ['099018', '100124', '101126', '102124', '103126', '105128']},
    '5':  {'theme': '保健統計③ 生命表・平均寿命・死因',
           'ids': ['100125', '106016']},
    '11': {'theme': '感染症概論・病原体・基本予防',
           'ids': old6 + ['098128', '099230', '102233', '103233', '105232', '107228',
                          '108228', '109228', '110233', '111228', '111229', '111232']},
    '12': {'theme': '感染症法① 一〜三類',
           'ids': ['098021', '099019', '100128', '102127', '105019']},
    '13': {'theme': '感染症法② 四〜五類・発生時対応',
           'ids': ['102235', '103235', '107122', '108016', '108123', '109121']},
    '14': {'theme': 'ワクチン・予防接種',
           'ids': old7},
}

old_all = old2 + old3 + old6 + old7 + old9 + old10
new_all = []
for v in new_lectures.values():
    new_all += v['ids']
missing = set(old_all) - set(new_all)
extra = set(new_all) - set(old_all)
dup = sorted({x for x in new_all if new_all.count(x) > 1})
print('旧', len(old_all), 'uniq', len(set(old_all)), '| 新', len(new_all), 'uniq', len(set(new_all)))
print('欠落', missing, '| 余分', extra, '| 重複', dup)

if not missing and not extra and not dup:
    shutil.copy(path, path + '.bak_pre_pubhealth_realign')
    m['公衆']['lectures'] = new_lectures
    json.dump(m, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('=> 書き込み完了 (backup: lecture_map.json.bak_pre_pubhealth_realign)')
    for k in sorted(new_lectures, key=int):
        print(f'   新{k} {new_lectures[k]["theme"]}: {len(new_lectures[k]["ids"])}問')
else:
    print('=> 不整合のため中止（書き込みせず）')
