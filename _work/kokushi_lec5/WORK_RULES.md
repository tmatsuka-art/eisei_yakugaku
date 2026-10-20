# 第5回「栄養摂取・エネルギー代謝」改訂・作問の共通ルール

## 必ず読むもの
- 改訂基準：/home/claude/eisei_yakugaku/_work/kokushi_pilot/RUBRIC.md（0, A, B, E, G, H は厳守）
- 診断：/home/claude/eisei_yakugaku/_work/kokushi_lec5/diag_lec5.json（各問題の plan・issues・fact_errors・sources、cross_lecture、unverified）
- 元の問題：/home/claude/eisei_yakugaku/_work/kokushi_lec5/lec5_future.jsonl、過去問：lec5_past.jsonl
- 他の回の問題一覧（重複を避ける）：/home/claude/eisei_yakugaku/_work/kokushi_lec5/overview_other_lectures.txt
- 先生の教科書の該当範囲：/tmp/claude-0/-home-claude-eisei-yakugaku/0cdc883f-e33a-5f78-abd9-6dec70e9de4e/scratchpad/lec5/textbook_lec5.txt（著作物。問題・解説に長く写さない。15字以内の語句のみ。言い換える）

## 根拠資料（これ以外は使わない）
- 食事摂取基準（2025年版）報告書PDF：/root/.claude/uploads/0cdc883f-e33a-5f78-abd9-6dec70e9de4e/9833d977-001316585.pdf
  テキスト抽出不可。Read の pages 指定で画像として読む（1回20ページまで）。印刷ページ＝PDFページ−12。
  総論 PDF 13〜60（指標の定義 p.13〜29、活用・調査法 36〜58）、エネルギー 61〜100、たんぱく質〜炭水化物 100〜165、ビタミン 160〜260、ミネラル 265〜345。
- 建帛社の表（先生指定、正しい前提）：https://www.kenpakusha.co.jp/data/seigo1/005004-05.pdf （WebFetch で狭い質問をする）
- 公的機関（mhlw.go.jp 等）、国際機関、学会の公式の提言・ガイドライン。
  - 令和6年国民健康・栄養調査結果の概要 https://www.mhlw.go.jp/content/10900000/001603146.pdf
  - 身体活動・運動ガイド2023 https://www.mhlw.go.jp/content/001195866.pdf
- 不可：出版社・企業・病院・ニュース・Wikipedia・論文・ブログ。
- 確認できない記述は使わない。どうしても必要なら change_summary に「要先生確認：…」と書く。
- 教科書と報告書が食い違う場合は報告書（公的資料）に従い、change_summary に食い違いを書く。

## 文面（RUBRIC G）
- 各選択肢を単独で読んでも、何の値か・誰（性・年齢区分）か・どの基準（食事摂取基準（2025年版）の推奨量など）か・いつの調査かが一意に分かること。
- 正答は一意。攪乱肢は「中途半端な知識だと迷う」内容。絶対化表現（のみ・必ず・すべて・常に・直ちに 等）と評論的修飾（比較的・かなり 等）を攪乱肢に使わない。
- 選択肢の長さ・文末をそろえる。1つの選択肢に論点は1つ。
- 事例では時期の前後関係、サプリメントは表示量と実際の摂取量を区別。正答だけが受診勧奨・積極策、という形にしない。
- 計算問題は、計算のしかたが一つに決まるように条件を全部書く。解説に計算過程を書く。数値は自分で計算して検算する（python で）。
- 架空のデータは「架空の町」「架空の事業所」などと明記。
- 表を使う場合は problem_text の中に「表」を全角の罫線ではなく、次のような行で書く（アプリはプレーンテキスト表示）：
  「表　〇〇\n項目｜値｜値\n…」（区切りは全角縦線「｜」）
- 日本語は自然な文で。直訳調を避ける。「たんぱく質」と表記をそろえる。

## 書式（RUBRIC B）
- choices は5つ、番号を付けない。answer は文字列の配列。
- comment は「1：正。…」「1：誤。…」を1→5の順に改行区切り。最後に任意で「ポイント：…」（100字以内）。
- 正答位置は内容優先でよい（最後に機械的に散らす）。ただし順序に意味がある選択肢（数値の昇順など）は昇順に並べておく。

## 出力形式（1行1問の jsonl）
改訂：{"problem_id","verdict","section"(必須/理論/実践),"problem_text","choices","answer","comment","new_corecurri_code","drop_image","change_summary","sources"}
新問題：{"problem_id","kind"("gap" or "curri"),"topic","section","problem_text","choices","answer","comment","new_corecurri_code","tags"(新コアカリ対応なら ["新コアカリ対応"]、それ以外は []),"note","sources"}
change_summary / note は先生向けに2〜3文。何を、なぜ変えたか。
sources は実際に確認した資料（報告書PDFのページ番号、URL、教科書の表番号）。
