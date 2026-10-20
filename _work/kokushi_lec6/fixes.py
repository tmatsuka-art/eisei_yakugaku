"""検証係の指摘を new40.json に反映する。usage: python3 fixes.py  （new40.json → new40_fixed.json、変更記録 fix_log.json）"""
import json
qs = json.load(open('new40.json'))
by = {q['tmp_id']: q for q in qs}
log = {}
def rep(tid, field, old, new, idx=None):
    q = by[tid]
    if field == 'choices':
        assert q['choices'][idx] == old, (tid, idx, q['choices'][idx])
        q['choices'][idx] = new
    else:
        assert q[field].count(old) == 1, (tid, field, old)
        q[field] = q[field].replace(old, new)
    log.setdefault(tid, []).append(f'{field}{"" if idx is None else idx+1}：「{old}」→「{new}」')

# --- verify_new_1 ---
rep('A13', 'choices', '規格基準型として、消費者委員会の個別審査を経ずに許可された。', '規格基準型として、部会の個別審査を経ずに許可された。', 2)
rep('B06', 'choices', '関与成分は吸収されない成分なので、服用中の薬に影響することはありません。', '関与成分は消化されない食物繊維なので、薬と同じ時刻に飲んでも差し支えありません。', 0)
rep('B06', 'comment', '1：誤。食物繊維を含む食品は、薬をからめとって吸収を低下させたり、糖尿病の薬と作用が重なったりすることがある。影響がないとは言えない。',
    '1：誤。食物繊維を含む食品は、薬をからめとって吸収を低下させたり、糖尿病の薬と作用が重なったりすることがある。飲む時刻も含めて主治医・薬剤師に相談する。')
rep('A02', 'choices', '両リストに未収載の新規成分は、都道府県を通じて厚生労働省に判断を求められる。', '両リストに未収載の新規成分は、都道府県を通じて厚生労働省に判断を求めることができる。', 1)
rep('A09', 'comment', '5：誤。許可を受けた特別用途食品は、指定された許可証票を表示できる。', '5：誤。許可を受けた特別用途食品には、指定された許可証票が表示される。')
rep('A14', 'choices', 'インスリンの分泌を促して、血糖値を下げる。', '歯を丈夫で健康にする。', 4)
rep('A14', 'comment', '5：誤。「血糖値を下げる」など身体の機能に直接作用する医薬品的な表現は、医薬品と誤認されるおそれがあり、特定保健用食品では認められない。',
    '5：誤。歯の健康維持の用途は、キシリトールやCPP-ACPなどで許可されたものである。難消化性デキストリンの規格基準に歯の用途はない。')

exec(open('fixes2.py').read()) if __import__('os').path.exists('fixes2.py') else None
json.dump(qs, open('new40_fixed.json', 'w'), ensure_ascii=False, indent=1)
json.dump(log, open('fix_log.json', 'w'), ensure_ascii=False, indent=1)
print('fixed', len(log), 'questions')
