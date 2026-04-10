import json
import re
from collections import Counter

with open('future_questions.jsonl', 'r', encoding='utf-8') as f:
    questions = [json.loads(line.strip()) for line in f if line.strip()]

issues = []

for q in questions:
    pid = q['problem_id']
    choices = q['choices']
    answer = q['answer']
    answer_nums = [int(a) for a in answer if a.isdigit()]
    
    # Skip IMAGES-type questions
    if choices[0] == 'IMAGES':
        continue
    
    # === CHECK 1: 誤答選択肢に同じフレーズが繰り返される（F586パターン） ===
    wrong_choices = [choices[i] for i in range(len(choices)) if (i+1) not in answer_nums]
    
    # 共通する末尾パターン（「設定されていない」「含まれない」等）
    tail_patterns = []
    for wc in wrong_choices:
        # 末尾20文字程度を取得
        tail = wc[-15:] if len(wc) > 15 else wc
        tail_patterns.append(tail)
    
    tail_counts = Counter(tail_patterns)
    for tail, count in tail_counts.items():
        if count >= 3 and len(wrong_choices) >= 3:
            issues.append({
                'pid': pid,
                'type': '誤答パターン重複',
                'detail': f'誤答{count}個が同じ末尾「...{tail}」',
                'severity': 'HIGH'
            })
    
    # === CHECK 2: 誤答選択肢の文が極端に短い（正答だけ詳しい） ===
    correct_choices = [choices[i] for i in range(len(choices)) if (i+1) in answer_nums]
    avg_correct_len = sum(len(c) for c in correct_choices) / max(len(correct_choices), 1)
    avg_wrong_len = sum(len(c) for c in wrong_choices) / max(len(wrong_choices), 1)
    
    if avg_correct_len > 0 and avg_wrong_len > 0:
        ratio = avg_correct_len / avg_wrong_len
        if ratio > 2.5:
            issues.append({
                'pid': pid,
                'type': '正答だけ長い',
                'detail': f'正答平均{avg_correct_len:.0f}文字 vs 誤答平均{avg_wrong_len:.0f}文字 (比率{ratio:.1f}x)',
                'severity': 'MED'
            })
        elif avg_wrong_len / avg_correct_len > 2.5:
            issues.append({
                'pid': pid,
                'type': '正答だけ短い',
                'detail': f'正答平均{avg_correct_len:.0f}文字 vs 誤答平均{avg_wrong_len:.0f}文字',
                'severity': 'LOW'
            })
    
    # === CHECK 3: 選択肢がほぼ同一文（コピペミス） ===
    for i in range(len(choices)):
        for j in range(i+1, len(choices)):
            if choices[i] == choices[j]:
                issues.append({
                    'pid': pid,
                    'type': '選択肢重複',
                    'detail': f'選択肢{i+1}と{j+1}が完全一致',
                    'severity': 'HIGH'
                })
    
    # === CHECK 4: 「正しい/誤り」系で誤答に明らかなキーワードパターン ===
    neg_keywords = ['設定されていない', '規定されていない', '定められていない', '含まれない', '該当しない', '存在しない', '必要ない', '関係ない', '影響しない']
    neg_count = 0
    for wc in wrong_choices:
        for kw in neg_keywords:
            if kw in wc:
                neg_count += 1
                break
    if neg_count >= 3 and len(wrong_choices) >= 3:
        issues.append({
            'pid': pid,
            'type': '否定形パターン集中',
            'detail': f'誤答{neg_count}/{len(wrong_choices)}個が否定形（「...ない」系）→正答が一目瞭然',
            'severity': 'HIGH'
        })
    
    # === CHECK 5: 正答だけが具体的数値を含み、誤答が曖昧 ===
    def has_number(text):
        return bool(re.search(r'\d+\.?\d*\s*(mg|g|kg|μg|ppm|ppb|%|℃|mL|L|mm|cm|m|μm|nm|Bq|Sv|lx|dB|Pa|mol)', text))
    
    correct_has_num = any(has_number(c) for c in correct_choices)
    wrong_has_num = sum(1 for c in wrong_choices if has_number(c))
    
    if correct_has_num and wrong_has_num == 0 and len(wrong_choices) >= 3:
        issues.append({
            'pid': pid,
            'type': '正答のみ数値あり',
            'detail': '正答だけ具体的数値を含み、誤答は数値なし',
            'severity': 'MED'
        })
    
    # === CHECK 6: 選択肢の構造が不揃い（正答だけ明らかに異質） ===
    # 正答が「〜である」で終わり、誤答が全部「〜ない」で終わる等
    correct_ends_positive = all(not c.endswith('ない') for c in correct_choices)
    wrong_all_negative = all(c.endswith('ない') for c in wrong_choices) if wrong_choices else False
    if correct_ends_positive and wrong_all_negative and len(wrong_choices) >= 3:
        issues.append({
            'pid': pid,
            'type': '語尾パターン不一致',
            'detail': '正答だけ肯定形、誤答が全て「...ない」→正答が目立つ',
            'severity': 'HIGH'
        })
    
    # === CHECK 7: 問題文が極端に短い（意味不明の可能性） ===
    if len(q['problem_text']) < 15:
        issues.append({
            'pid': pid,
            'type': '問題文が極短',
            'detail': f'問題文: "{q["problem_text"]}" ({len(q["problem_text"])}文字)',
            'severity': 'MED'
        })
    
    # === CHECK 8: 解説が欠落 or 極短 ===
    comment = q.get('comment', '')
    if not comment or len(comment) < 20:
        issues.append({
            'pid': pid,
            'type': '解説不足',
            'detail': f'解説が{len(comment)}文字しかない',
            'severity': 'MED'
        })
    
    # === CHECK 9: 選択肢が5個未満/超過 ===
    if len(choices) != 5 and choices[0] != 'IMAGES':
        issues.append({
            'pid': pid,
            'type': '選択肢数異常',
            'detail': f'選択肢が{len(choices)}個',
            'severity': 'HIGH'
        })

# Sort by severity
sev_order = {'HIGH': 0, 'MED': 1, 'LOW': 2}
issues.sort(key=lambda x: (sev_order.get(x['severity'], 9), x['pid']))

print(f"=== 予想問題 品質チェック結果 ===")
print(f"総問題数: {len(questions)}")
print(f"検出された問題: {len(issues)}\n")

# Summary by type
type_counts = Counter(i['type'] for i in issues)
print("--- タイプ別集計 ---")
for t, c in type_counts.most_common():
    print(f"  {t}: {c}件")
print()

# Detail
for sev in ['HIGH', 'MED', 'LOW']:
    sev_issues = [i for i in issues if i['severity'] == sev]
    if sev_issues:
        label = {'HIGH': '🔴 重大', 'MED': '🟡 中程度', 'LOW': '🟢 軽微'}[sev]
        print(f"\n{label} ({len(sev_issues)}件)")
        print("-" * 60)
        for i in sev_issues:
            print(f"  {i['pid']}: [{i['type']}] {i['detail']}")
