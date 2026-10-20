# やさしい改訂版（教育効果重視・衛生薬学の視点）作成の共通ルール

先生の方針（2026-10-07）：「国家試験を見据えた教育効果が高い改訂。あくまで衛生薬学の問題。今の改訂版は難しすぎ・生化学のよう」。試作10問の難しさで暫定決定。

## 必ず読むもの
- 基準：/home/claude/eisei_yakugaku/_work/kokushi_easy/calibration.md（最優先）
- 試作10問の完成形（お手本）：/home/claude/eisei_yakugaku/_work/kokushi_easy/pilot_easy.jsonl
- 今の改訂版の評価と置き換え案（事実は未確認）：assessment.json
- 旧版と今の改訂版：revised_pairs.jsonl（新作は new23.jsonl）
- 過去問：past_lec2to5.jsonl
- 書式・根拠：/home/claude/eisei_yakugaku/_work/kokushi_pilot/RUBRIC.md の 0, A-3, B, G（ただし年版・年齢区分の条件は選択肢に繰り返さずリード文に1回）
- 根拠資料の場所：/home/claude/eisei_yakugaku/_work/kokushi_lec5/WORK_RULES.md の「根拠資料」。食品の含有量は文部科学省の日本食品標準成分表（食品成分データベース）で確認可。教科書全体：/tmp/claude-0/-home-claude-eisei-yakugaku/0cdc883f-e33a-5f78-abd9-6dec70e9de4e/scratchpad/src/textbook.txt（15字以内の語句しか写さない）
- 重複チェック：/home/claude/eisei_yakugaku/future_questions.jsonl と /home/claude/eisei_yakugaku/lecture_map.json（衛I lectures の ids）。同じ回の他の問題・試作10問・他の担当分（グループ表は grp_A/B/C.json）と、同じ知識点を同じ角度で問わない。

## 作り方
- 出発点は旧版の論点。今の改訂版で直した事実の誤りは引き継ぐ（旧版の誤りを復活させない）。
- 衛生の視点：欠乏症・過剰症、多く含む食品、リスクの高い人（妊婦・高齢者・乳児・飲酒・薬剤）、食事摂取基準の指標の意味と使い方、保健機能食品、疾病予防。生化学は国試に出た代表的な分子名まで、欠乏症・食品・医薬品・事例の理由として、1問に2肢まで。
- 長さ：必須の選択肢は語句、理論・実践は20〜35字（45字まで）、事例150〜250字。1肢1論点。計算は3段階以内、値は問題文で与える。
- 1回の中での形式のバランス：必須・理論・実践を混ぜ、2つ選べは理論・実践の半分程度。
- 今の改訂版がすでに国試並み（assessment で biochem≤1 かつ too_hard=0、または読んで国試並みと判断）なら、無理に変えない："unchanged": true とし、今の改訂版をそのまま（必要なら選択肢の条件をリード文に移す程度の小修正）で出力する。
- 解説は学生が学べるよう各選択肢の理由を短く（1行60〜100字）。最後に「ポイント：」で覚えるべきこと1つ（100字以内）。
- 事実はすべて根拠資料で確かめ、sources に書く。確かめられないことは使わない。
- 図つきの問題（F225 など、FUTURE/F225.png）は図を使わない形にしてよい（drop_image: true）。

## 出力（1行1問の jsonl）
{"problem_id","lecture","base"("revised" or "new"),"unchanged"(true/false),"section","problem_text","choices","answer","comment","new_corecurri_code","tags"(新作は元のtagsを引き継ぐ。改訂は[]),"drop_image","design_note"(先生向け2〜3文：何を変え、なぜ衛生らしく国試並みになったか),"sources"}
最後に python で書式チェック（選択肢5、answer数と「2つ選べ」、解説の正誤と answer の一致、ポイント100字以内、誤答に絶対化・評論的修飾なし）と字数表を作り、報告に含める。
