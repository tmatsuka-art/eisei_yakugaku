# -*- coding: utf-8 -*-
# 本体162問(E-3-1-(1)(2))を第1/2/4回キーワードでスコアリング。第4回候補を抽出。
import sys, json
sys.stdout.reconfigure(encoding="utf-8")

targets = {"化学物質の体内動態", "毒性学総論"}
main_codes = {"E-3-1-(1)", "E-3-1-(2)"}

# 第4回（解毒・生体防御）に特化
KW4 = ['メタロチオネイン', '活性酸素', 'スーパーオキシド', 'SOD', 'カタラーゼ',
       'グルタチオンペルオキシダーゼ', 'ペルオキシダーゼ', '抗酸化', 'フリーラジカル', 'ラジカル',
       '生体防御', '酸化ストレス', '過酸化', '一重項酸素', '脂質過酸化', 'グルタチオン抱合', '解毒']
# 第2回（第II相・代謝因子・標的臓器）
KW2 = ['抱合', 'グルクロン酸', '硫酸抱合', 'アセチル化', 'メチル化', '第II相', '第二相',
       '誘導', '阻害', '多型', '標的臓器', '肝毒性', '腎毒性', '神経毒性', '器官毒性']
# 第1回（第I相代謝）
KW1 = ['CYP', 'P450', 'シトクロム', '第I相', '第一相', '水酸化', '脱メチル', '脱アルキル',
       'エポキシ', '加水分解', 'モノオキシゲナーゼ', 'ミクロソーム']

qs = []
with open("future_questions.jsonl", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if o.get("_subcat") in targets and o.get("new_corecurri_code") in main_codes:
            qs.append(o)

def cnt(text, kws):
    return sum(text.count(w) for w in kws)

cand4 = []
for o in qs:
    text = o.get("problem_text", "") + " " + " ".join(o.get("choices", [])) + " " + o.get("comment", "")
    s4 = cnt(text, KW4)
    s2 = cnt(text, KW2)
    s1 = cnt(text, KW1)
    if s4 > 0:
        cand4.append((o["problem_id"], s1, s2, s4, o.get("problem_text", "")[:42]))

print(f"本体{len(qs)}問中、第4回キーワード該当: {len(cand4)}問")
for pid, s1, s2, s4, q in sorted(cand4, key=lambda x: -x[3]):
    print(f"  {pid}: 1={s1} 2={s2} 4={s4} | {q}")
