# -*- coding: utf-8 -*-
# 衛生化学I（食品衛生・栄養 15回）を lecture_map に新設
import sys, json, shutil
sys.stdout.reconfigure(encoding="utf-8")

WAI = {
    '1': '衛生化学概論・栄養と健康', '2': 'ビタミンと欠乏症', '3': 'ミネラルと欠乏症',
    '4': '三大栄養素・消化吸収', '5': '栄養摂取・エネルギー代謝', '6': '機能性食品',
    '7': 'ライフステージ栄養管理・栄養療法', '8': '中間試験・まとめ',
    '9': '食品衛生・食品安全概論・食品の変質', '10': '食中毒1：微生物',
    '11': '食中毒2：寄生虫・自然毒・化学物質', '12': '食品中の有害物質',
    '13': '食品衛生 法制度', '14': '食品添加物 総論', '15': '食品添加物 各論・まとめ',
}

shutil.copy('lecture_map.json', 'lecture_map.json.bak_pre_eisei1')
lm = json.load(open('lecture_map.json', encoding='utf-8'))

if '衛I' in lm:
    print("衛I は既に存在。スキップ。")
else:
    wai = {
        'label': '衛生化学I',
        'icon': '🍎',
        'color': '#f59e0b',
        'lectures': {k: {'theme': v, 'ids': []} for k, v in WAI.items()},
    }
    lm = {'衛I': wai, **lm}  # 先頭（衛I→衛II→公衆）
    with open('lecture_map.json', 'w', encoding='utf-8') as f:
        json.dump(lm, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print("衛I新設完了。科目順:", list(lm.keys()))
