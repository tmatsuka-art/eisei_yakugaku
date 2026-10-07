# 公衆衛生学 第1回「公衆衛生学概論・疫学」改訂の共通ルール（2026-10-08）

先生の方針：衛I第2〜5回と同じ。国家試験を見据えた教育効果の高い改訂。各問題に
- 「やさしい改訂版」（国試並みの基本を確実に問う。アプリの主となる版）
- 「発展版」（国試の理論・実践の難しめの問題。計算の手順が多い、事例が長い、概念の比較が細かい等）
を用意し、抜けている知識点の新問題と、新コアカリ対応問題（4問）を作る。

## 読むもの
- 改訂基準：/home/claude/eisei_yakugaku/_work/kokushi_pilot/RUBRIC.md の A-3（攪乱肢）、B（書式）、G（文面の厳密さ）、E（新コアカリ）、H（タグ）
- 衛Iで作った難しさの基準（考え方の参考。栄養固有の部分は読み替える）：/home/claude/eisei_yakugaku/_work/kokushi_easy/calibration.md
- 対象：/home/claude/eisei_yakugaku/_work/kokushi_pub1/pub1_future.jsonl（予想問題70問）、pub1_past.jsonl（過去問31問）
- 他の回・科目の問題一覧（重複・範囲外の判断用）：/home/claude/eisei_yakugaku/_work/kokushi_pub1/overview_others.txt
- 新コアカリ E-1-1：/home/claude/eisei_yakugaku/_work/kokushi_pub1/corecurri_E-1-1.txt（学修事項(1)疫学、(4)保健統計・疫学的手法による解析。評価の指針の重点1・7）
- 診断：/home/claude/eisei_yakugaku/_work/kokushi_pub1/diag_pub1.json（診断後）

## 根拠にしてよい資料（先生の指示：公的機関・学会・先生指定の資料のみ）
- 薬剤師国家試験の過去問と正答（厚生労働省公表）：pub1_past.jsonl と /home/claude/eisei_yakugaku/hygiene_with_images_v4.jsonl。概念の定義・計算方法の根拠として使ってよい。
- 公的機関（go.jp 等）：厚生労働省、国立保健医療科学院、国立がん研究センター（がん情報サービス、多目的コホート研究 JPHC）、環境省（エコチル調査）、国立感染症研究所、e-Stat、「人を対象とする生命科学・医学系研究に関する倫理指針」（文部科学省・厚生労働省・経済産業省）。国際機関（WHO 等）。
- 学会の公式資料（日本疫学会など）。
- 計算は python で必ず検算する（計算そのものが根拠）。
- 不可：出版社・企業・病院・ニュース・Wikipedia・論文・個人ブログ。先生の教科書（栄養分野）は疫学を含まない。
- 疫学の用語の定義で上の資料に見つからないものは、国試過去問の正答肢・解説で裏づけるか、使わない。どうしても必要なら design_note に「要先生確認：…」と書く。

## 書き方
- 1肢1論点。必須の選択肢は語句、理論・実践は20〜35字（45字まで）、事例150〜250字。
- 計算は数値を問題文で与え、やさしい版は2〜3段階、発展版は3〜4段階まで。数値の選択肢は昇順に並べる。
- 攪乱肢に絶対化（のみ・必ず・すべて・常に 等）・評論的修飾（比較的・かなり 等）を使わない。正答だけ長くしない。
- 解説は「1：正。…」「1：誤。…」を1→5の順に改行区切り。各行60〜100字程度、最後に「ポイント：」1行（100字以内）。
- 日本語は自然な文で。用語は国試の表記（相対危険・寄与危険・オッズ比・症例対照研究・コホート研究・交絡・バイアス 等。過去問の表記に合わせる）。
- 図つきの旧問題は、図を使わない形にしてよい（drop_image: true）。

## 出力（1行1問の jsonl）
{"problem_id","lecture":"公衆1","base":"revised" または "new","variant":"easy" または "advanced","unchanged":bool,"section","problem_text","choices","answer","comment","new_corecurri_code","tags","drop_image","design_note","sources"}
- 改訂の問題は、1問につき easy と advanced の2行を出す（今の問題がすでにどちらかの水準なら、その variant は unchanged:true で今の問題を整えて出す）。
- 新問題の problem_id は仮番号（"K1-N01" のように）とし、先生の承認後に正式番号を振る。新コアカリ対応は tags ["新コアカリ対応"]。
