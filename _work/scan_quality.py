"""
全1413問の選択肢に対して、品質チェック3項目を一括検出するスクリプト。

検出項目:
1. 絶対化表現 — 量的(のみ/だけ/全く/必ず/絶対/すべて/あらゆる/ない[末尾])
              時間的(直ちに/常に/決して/即座に/最優先で)
              当為的(しなければならない/すべきではない/する義務がある)
2. 評論的修飾 — 比較的/概ね/相当に/割と/やや/かなり/ある程度
3. 長さアンバランス — 正答と攪乱肢の長さ差
4. 正答位置の偏り

出力: _work/quality_scan_report.md
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

# 絶対化キーワード（誤答選択肢に出現したら警告）
ABS_QUANT = ['のみ', 'だけ', '全く', '必ず', '絶対', 'すべて', 'あらゆる']
ABS_TIME = ['直ちに', 'ただちに', '即座に', '常に', '決して', '最優先で']
ABS_DUTY = ['しなければならない', 'すべきではない', '義務がある', '禁じられている']
# 「ない」型 — 文末や強い否定を捉える正規表現
ABS_NEG_PATTERNS = [
    r'存在しない',
    r'認められていない',
    r'含まれない[。\s]?$',
    r'設定されていない',
    r'設けられていない',
    r'規定されていない',
    r'指定されていない',
    r'対象では?ない',
    r'関係(?:が)?ない',
    r'影響(?:が|は)?ない',
    r'必要(?:が|は)?ない',
    r'問題(?:が|は)?ない',
    r'関与しない',
    r'効果(?:が|は)?ない',
]

EVAL_WORDS = ['比較的', '概ね', '相当に', '割と', 'やや', 'かなり', 'ある程度']


def scan_absolute(text):
    """選択肢テキストから絶対化キーワード／パターンを検出"""
    hits = []
    for kw in ABS_QUANT + ABS_TIME + ABS_DUTY:
        if kw in text:
            hits.append(kw)
    for pat in ABS_NEG_PATTERNS:
        if re.search(pat, text):
            hits.append(re.search(pat, text).group(0))
    return hits


def scan_evaluative(text):
    return [w for w in EVAL_WORDS if w in text]


def main():
    jsonl_path = Path('future_questions.jsonl')
    qs = []
    with open(jsonl_path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                qs.append(json.loads(line))

    # 集計用
    abs_issues = []           # 絶対化を含む攪乱肢のリスト
    eval_issues = []          # 評論的修飾を含む攪乱肢
    length_issues = []        # 長さアンバランス
    pos_single = Counter()    # 1つ選べの正答位置
    pos_multi = Counter()     # 複数選べの正答位置
    reviewed_count = 0
    unreviewed_count = 0

    for q in qs:
        pid = q.get('problem_id', '')
        choices = q.get('choices', []) or []
        answer = q.get('answer', []) or []
        if not choices or not answer:
            continue

        is_reviewed = bool(q.get('ai_review'))
        if is_reviewed:
            reviewed_count += 1
        else:
            unreviewed_count += 1

        # 正答インデックス（1始まり）
        ans_idx = set()
        for a in answer:
            try:
                ans_idx.add(int(a))
            except (ValueError, TypeError):
                pass

        # 位置分布
        if len(ans_idx) == 1:
            (idx,) = list(ans_idx)
            pos_single[idx] += 1
        else:
            for idx in ans_idx:
                pos_multi[idx] += 1

        # 絶対化／評論的修飾の検出（攪乱肢のみ）
        for i, c in enumerate(choices, 1):
            if i in ans_idx:
                continue  # 正答は除外
            abs_hits = scan_absolute(c)
            if abs_hits:
                abs_issues.append({
                    'pid': pid, 'choice_no': i,
                    'reviewed': is_reviewed,
                    'hits': abs_hits, 'text': c
                })
            eval_hits = scan_evaluative(c)
            if eval_hits:
                eval_issues.append({
                    'pid': pid, 'choice_no': i,
                    'reviewed': is_reviewed,
                    'hits': eval_hits, 'text': c
                })

        # 長さアンバランス（正答が他より±20字以上違う場合のみ）
        ans_lens = [len(choices[i-1]) for i in ans_idx if 0 < i <= len(choices)]
        other_lens = [len(c) for i, c in enumerate(choices, 1) if i not in ans_idx]
        if ans_lens and other_lens:
            ans_mean = sum(ans_lens) / len(ans_lens)
            other_mean = sum(other_lens) / len(other_lens)
            diff = ans_mean - other_mean
            if abs(diff) >= 20:
                length_issues.append({
                    'pid': pid, 'reviewed': is_reviewed,
                    'ans_mean': round(ans_mean, 1),
                    'other_mean': round(other_mean, 1),
                    'diff': round(diff, 1),
                    'direction': '正答が長い' if diff > 0 else '正答が短い'
                })

    # ===== レポート出力 =====
    out_lines = []
    out_lines.append('# 全問題 品質スキャン レポート')
    out_lines.append('')
    out_lines.append(f'対象問題数: **{len(qs)}** （ai_review済: {reviewed_count}、未レビュー: {unreviewed_count}）')
    out_lines.append('')

    # 1. 正答位置の偏り
    out_lines.append('## 1. 正答位置の偏り')
    out_lines.append('')
    out_lines.append('### 1つ選べ問題')
    single_total = sum(pos_single.values())
    out_lines.append('| 位置 | 件数 | 割合 |')
    out_lines.append('|---:|---:|---:|')
    for p in sorted(pos_single):
        n = pos_single[p]
        pct = n / single_total * 100
        out_lines.append(f'| pos {p} | {n} | {pct:.1f}% |')
    out_lines.append(f'| **合計** | **{single_total}** | 100.0% |')
    out_lines.append('')
    out_lines.append('### 複数選べ問題（正答数で重複カウント）')
    multi_total = sum(pos_multi.values())
    out_lines.append('| 位置 | 件数 | 割合 |')
    out_lines.append('|---:|---:|---:|')
    for p in sorted(pos_multi):
        n = pos_multi[p]
        pct = n / multi_total * 100 if multi_total else 0
        out_lines.append(f'| pos {p} | {n} | {pct:.1f}% |')
    out_lines.append(f'| **合計** | **{multi_total}** | 100.0% |')
    out_lines.append('')

    # 2. 絶対化表現
    out_lines.append('## 2. 絶対化表現（誤答選択肢のみ）')
    out_lines.append('')
    abs_unrev = [x for x in abs_issues if not x['reviewed']]
    abs_rev = [x for x in abs_issues if x['reviewed']]
    out_lines.append(f'検出件数: **{len(abs_issues)}** 件（未レビュー: {len(abs_unrev)}、レビュー済: {len(abs_rev)}）')
    out_lines.append('')
    out_lines.append('※レビュー済で残っているものは「姉さんが見落とした」か「相対化が不十分」の候補')
    out_lines.append('')

    # 絶対化キーワードの頻度
    kw_counter = Counter()
    for x in abs_issues:
        for h in x['hits']:
            kw_counter[h] += 1
    out_lines.append('### キーワード頻度（上位20）')
    out_lines.append('| キーワード | 件数 |')
    out_lines.append('|---|---:|')
    for kw, n in kw_counter.most_common(20):
        out_lines.append(f'| {kw} | {n} |')
    out_lines.append('')

    # 問題ID×ヒット数で集約（同一問題に複数攪乱肢で絶対化が多いものを優先）
    pid_counter = Counter()
    for x in abs_issues:
        pid_counter[(x['pid'], x['reviewed'])] += 1
    out_lines.append('### 同一問題内の絶対化集中（上位30、3箇所以上）')
    out_lines.append('| problem_id | 該当攪乱肢数 | レビュー済 |')
    out_lines.append('|---|---:|:-:|')
    for (pid, rev), n in pid_counter.most_common(30):
        if n < 3:
            break
        out_lines.append(f'| {pid} | {n} | {"✓" if rev else ""} |')
    out_lines.append('')

    # 3. 評論的修飾
    out_lines.append('## 3. 評論的・主観的修飾')
    out_lines.append('')
    out_lines.append(f'検出件数: **{len(eval_issues)}** 件')
    out_lines.append('')
    if eval_issues:
        out_lines.append('| problem_id | 選肢 | キーワード | テキスト（先頭40字） | レビュー済 |')
        out_lines.append('|---|---:|---|---|:-:|')
        for x in eval_issues[:30]:
            txt = x['text'][:40].replace('|', '｜')
            out_lines.append(f'| {x["pid"]} | {x["choice_no"]} | {"/".join(x["hits"])} | {txt} | {"✓" if x["reviewed"] else ""} |')
    out_lines.append('')

    # 4. 長さアンバランス
    out_lines.append('## 4. 選択肢長さアンバランス（±20字以上）')
    out_lines.append('')
    len_unrev = [x for x in length_issues if not x['reviewed']]
    len_rev = [x for x in length_issues if x['reviewed']]
    out_lines.append(f'検出件数: **{len(length_issues)}** 件（未レビュー: {len(len_unrev)}、レビュー済: {len(len_rev)}）')
    out_lines.append('')
    # 上位（差が大きい順、未レビューを先に）
    length_issues_sorted = sorted(length_issues, key=lambda x: (x['reviewed'], -abs(x['diff'])))
    out_lines.append('### 上位30件（差の大きい順）')
    out_lines.append('| problem_id | 正答平均字数 | 他平均字数 | 差 | 方向 | レビュー済 |')
    out_lines.append('|---|---:|---:|---:|---|:-:|')
    for x in length_issues_sorted[:30]:
        out_lines.append(f'| {x["pid"]} | {x["ans_mean"]} | {x["other_mean"]} | {x["diff"]:+.1f} | {x["direction"]} | {"✓" if x["reviewed"] else ""} |')
    out_lines.append('')

    # 5. 全絶対化問題リスト（未レビューのみ、後段でバッチ組み立てに使う）
    out_lines.append('## 5. 未レビュー × 絶対化問題リスト（バッチ組み立て用）')
    out_lines.append('')
    out_lines.append(f'件数: **{len(abs_unrev)}** 件 / 問題数: **{len(set(x["pid"] for x in abs_unrev))}** 問')
    out_lines.append('')
    out_lines.append('<details><summary>全件展開（クリック）</summary>')
    out_lines.append('')
    out_lines.append('| problem_id | 選肢 | キーワード | テキスト（先頭60字） |')
    out_lines.append('|---|---:|---|---|')
    for x in abs_unrev:
        txt = x['text'][:60].replace('|', '｜').replace('\n', ' ')
        out_lines.append(f'| {x["pid"]} | {x["choice_no"]} | {"/".join(x["hits"])} | {txt} |')
    out_lines.append('')
    out_lines.append('</details>')

    # 出力
    out_path = Path('_work/quality_scan_report.md')
    out_path.write_text('\n'.join(out_lines), encoding='utf-8')
    print(f'wrote {out_path}')
    print(f'  全問題: {len(qs)} / 未レビュー: {unreviewed_count}')
    print(f'  絶対化検出: {len(abs_issues)} 件 (未レビュー: {len(abs_unrev)})')
    print(f'  評論的修飾検出: {len(eval_issues)} 件')
    print(f'  長さアンバランス: {len(length_issues)} 件 (未レビュー: {len(len_unrev)})')


if __name__ == '__main__':
    main()
