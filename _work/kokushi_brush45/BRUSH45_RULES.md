# 衛生化学I 第4・5回 やさしい版の見直し（2026-10-15）

先生の依頼：「第4回・第5回の予想問題も、第2回・第3回のような感じでブラッシュアップしてほしい」。
第4・5回のやさしい版（10月8日作成、まだ誰も判断していない）を、第2・3回で鈴木先生から受けたコメントの教訓で見直す。

## 入力
- 対象の問題（旧版 old・改訂版 rev（発展）・やさしい版 easy、作成メモ note、根拠 sources）：
  `/home/claude/eisei_yakugaku/_work/kokushi_brush45/input_items.json`（id で引く。lec=4 または 5）
- 担当の割り振り：`groups.json`
- 作り方の共通ルール（必ず読む）：`/home/claude/eisei_yakugaku/_work/kokushi_easy/EASY_RULES.md`
- 難しさの基準（必ず読む）：`/home/claude/eisei_yakugaku/_work/kokushi_easy/calibration.md`
- 書式・根拠の基準：`/home/claude/eisei_yakugaku/_work/kokushi_pilot/RUBRIC.md` の 0, A-3, B, G
- 鈴木先生のコメント全文と、それを受けた第2・3回の再改訂版（お手本）：
  `/home/claude/eisei_yakugaku/_work/kokushi_rerev23/suzuki_decisions.json`、`rerev_draft.json`、`work_items.md`
- 過去問（形式の参考）：`/home/claude/eisei_yakugaku/_work/kokushi_easy/past_lec2to5.jsonl`
- 重複チェック：`/home/claude/eisei_yakugaku/future_questions.jsonl`、`/home/claude/eisei_yakugaku/lecture_map.json`（衛I lectures）、input_items.json の同じ回の他の問題

## 根拠資料（これ以外は使わない）
- 先生の教科書（テキスト化）：`/tmp/claude-0/-home-claude-eisei-yakugaku/0cdc883f-e33a-5f78-abd9-6dec70e9de4e/scratchpad/src/textbook.txt`（著作物。問題や解説に15字を超えて写さない）
- 日本人の食事摂取基準（2025年版）報告書：テキスト `/tmp/claude-0/-home-claude-eisei-yakugaku/0cdc883f-e33a-5f78-abd9-6dec70e9de4e/scratchpad/src/dri2025.txt`、
  PDF `/root/.claude/uploads/0cdc883f-e33a-5f78-abd9-6dec70e9de4e/9833d977-001316585.pdf`（Read の pages 指定で読む。印刷ページ＝PDFページ−12）
- 公的機関（mhlw.go.jp、caa.go.jp、mext.go.jp の食品成分表 など go.jp）、国際機関、学会の公式の提言・ガイドライン（WebFetch 可）
- 不可：出版社・企業・病院・ニュース・Wikipedia・論文・ブログ。確かめられないことは使わない（どうしても必要なら concerns に「要先生確認：…」）。

## 鈴木先生のコメントから分かった見直しの観点（最重要）
第2・3回では、鈴木先生は「やさしい版」を基本に選び（25問）、旧版を選んだ問題も多かった（12問）。コメントは次の型に集中していた。
1. **誤答が「あまりに間違いすぎる」**（F231）：常識で消せる誤答、「多い⇔少ない」「ある⇔ない」の単純な反転だけの誤答は避ける。
   中途半端な知識だと「正しそう」に見えるもっともらしい誤り（例：「B1は腸内細菌で合成されるので欠乏症は現れにくい」）にする。
2. **正答が明らかすぎる**（F509）：正答だけが具体的・詳しい、誤答が雑、などで正答が浮かないように。誤答にも本物らしい具体性を持たせる。
3. **同じことを言っている選択肢**（F649、F660）：言い換えただけの肢、ほぼ同じ知識点の肢が2つあれば、別の論点に替える。
4. **難解すぎる肢**（F241「発展2は難解」）：生化学の細目・機序の細部は1問に多くて1肢、国試に出た水準まで。
5. **解説の余計な話・不正確な話**（F249「解説から悪性貧血は削除」）：解説は各肢の正誤の理由に絞り、紛らわしい周辺知識を足さない。
6. **正答の対象の偏り**（F466「正解の選択肢をビタミンAに」）：同じ回で正答が同じ物質・同じ論点に偏らないよう、回全体で散らす。
7. **旧版の良い肢を活かす**（F232、F234、F241、F630）：旧版・発展版に良い肢があれば、やさしい版に取り込んでよい（事実の誤りは直してから）。
8. **2つ選べ化**（F469）：正しい内容が2つ自然に立つなら「2つ選べ」も可（回全体で2つ選べは理論・実践の半分程度まで）。
9. 不要な問題（F1414・F1415・F1425）は削除が選ばれた：同じ回の他の問題と論点がほぼ同じ問題は、concerns に「削除候補：理由」と書く。

## 作業
担当の各問題について、やさしい版（easy）を上の観点で点検し、必要なら直す。
- 直す必要がなければ action "keep"（easy をそのまま）。
- 直すときは action "fix" で、直した easy 全体（problem_text, choices[5], answer, comment, section）を出す。
- 正答位置は、直した結果で偏らないよう意識する（順序に意味のある選択肢は動かさない）。
- 事実はすべて根拠資料で確かめる。新しく入れた事実は sources に追記する。
- 文面：誤答に絶対化（のみ・だけ・必ず・すべて・決して 等）と評論的修飾（比較的・やや・かなり 等）を使わない。全選択肢の文末をそろえる。年版・年齢区分などの条件は選択肢ごとに繰り返さずリード文に1回。
- 解説：各肢「n：正。…」「n：誤。…」の形で1行60〜100字、最後に「ポイント：」（100字以内）。
- 旧版・発展版はさわらない（先生は版ごとに選ぶ）。ただし旧版に事実の誤りを見つけたら old_errors に書く。

## 出力（担当ごとに1ファイル、1行1問の jsonl）
`/home/claude/eisei_yakugaku/_work/kokushi_brush45/out_<担当>.jsonl`
{"id", "action": "keep"|"fix",
 "easy": {"problem_text","choices","answer","comment","section"}（keep でも現行の easy をそのまま入れる）,
 "change_note": "先生向けに1〜3文。何を直したか・なぜか（鈴木先生の観点の番号を添える）。keep なら『変更なし：理由』",
 "sources": [...]（現行の sources＋追加分）,
 "old_errors": [...]（旧版の事実の誤り。なければ []）,
 "concerns": [...]（要先生確認・削除候補など。なければ []）}
最後に python で書式チェック（選択肢5つ、「2つ選べ」と answer の数、解説の正誤と answer の一致、ポイント100字以内、誤答の絶対化・評論的修飾）を行い、報告の最後に結果と「fix の数・主な直し方」を3〜6行でまとめる。
