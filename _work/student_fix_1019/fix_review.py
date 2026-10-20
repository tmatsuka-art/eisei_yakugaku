"""2026-10-19 学生の指摘への対応（先生承認）：F1377 の選択肢3を誤りの文に、111019・104227 の解説を修正。
review ブランチの future_questions.jsonl / hygiene_with_images_v4.jsonl を書き換える。"""
import json, shutil, sys
R = '/home/claude/eisei_yakugaku/'
TODAY = '2026-10-19'

def load(p): return [json.loads(l) for l in open(R + p) if l.strip()]
def save(p, rows):
    shutil.copy(R + p, R + p + '.bak_pre_studentfix_20261019')
    with open(R + p, 'w') as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')

fut = load('future_questions.jsonl')
r = next(x for x in fut if x['problem_id'] == 'F1377')
assert r['choices'][2] == '集団の摂取基準を評価する場合、個人間変動が重要である'
r['choices'][2] = '個人の習慣的な摂取量を評価する場合、日間変動は考慮しなくてよい'
lines = r['comment'].split('\n')
assert lines[2].startswith('3：誤。')
lines[2] = '3：誤。1日だけの調査では日間変動の影響が大きいため、個人の習慣的な摂取量を評価するには、複数日の調査を行うなどして日間変動を考慮する必要がある。'
r['comment'] = '\n'.join(lines)
r['ai_review'] = {'status': 'approved_rewrite', 'reviewed_at': TODAY, 'lecture': '衛I-5', 'batch': 'student_fix_1019',
                  'changes_summary': ['学生の指摘（選択肢3も正しい内容）により、3を誤りの文に替えた（先生承認）']}

past = load('hygiene_with_images_v4.jsonl')
p1 = next(x for x in past if x['problem_id'] == '111019')
old = 'ナトリウムは目安量で、むしろ過剰摂取を防ぐ必要がある。'
assert old in p1['comment']
p1['comment'] = p1['comment'].replace(old, '成人のナトリウムには、推定平均必要量（600 mg/日、食塩相当量1.5 g/日）と、摂取量を減らすことを目指す目標量が設定されている。目安量が設定されているのは乳児のみである。')
old2 = 'これには食物繊維、カリウム、カルシウムなど、現在の摂取量が不足している栄養素が含まれる。'
assert old2 in p1['comment']
p1['comment'] = p1['comment'].replace(old2, '摂取量を増やすことを目指して目標量が設定されているのは、食物繊維とカリウムである（カルシウムには目標量はなく、推定平均必要量・推奨量が設定されている）。')

p2 = next(x for x in past if x['problem_id'] == '104227')
assert p2['comment'].rstrip().endswith('吸収効率が低い。')
p2['comment'] = p2['comment'].rstrip() + '\n' + '\n'.join([
    '2:正', 'マルターゼは、マルトースのα-1,4結合を加水分解するα-グルコシダーゼである。',
    '3:誤', 'スクロースは、グルコースとフルクトースがα1→β2結合した二糖で、還元性を示さない。α1→4結合した二糖はマルトースである。',
    '4:正', '消化されない二糖類が小腸にとどまると浸透圧が高まり、浸透圧性の下痢を起こしやすい。',
    '5:誤', 'ボグリボースは、二糖類を分解するα-グルコシダーゼを阻害して、糖の消化・吸収を遅らせる。ラクトースを分解するラクターゼはβ-ガラクトシダーゼで、ボグリボースの主な標的ではない。'])

if '--apply' in sys.argv:
    save('future_questions.jsonl', fut); save('hygiene_with_images_v4.jsonl', past); print('反映しました')
print(r['choices'][2]); print(p1['comment']); print(p2['comment'][-400:])
