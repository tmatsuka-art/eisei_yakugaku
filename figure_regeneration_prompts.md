# Gemini画像生成用プロンプト集

各プロンプトは日本語テキストが正確に描画されるGeminiモデル（Gemini 2.5 Flash Image / nano-banana等）向けに設計。1024×768px程度、白背景、教科書的なモノクロ〜淡グレーの配色を想定。

---

## 2026-04-10 第2ラウンド目視確認の結果

前セッションでGemini再生成した5枚（F261/F218/F211/F163/F1004）のうち、**F218** は完璧。他4枚について以下の指摘事項あり:

| 図 | 重要度 | 問題点 |
|---|---|---|
| F261 | 中 | 左上に「栄養ア」という謎のテキスト断片が浮いている（「栄養アセスメント」の生成残骸） |
| F163 | 中 | (A)槽のすぐ横に「曝気（空気供給）」と書かれており、正答「A:曝気」のヒントになっている |
| F1004 | 軽 | 図中の分岐に「遺伝子組換え（義務表示）」とあるが、問題文の選択肢4「遺伝子組換え不分別」と用語不一致 → **問題文側を修正する方針のためプロンプト修正不要** |
| F211 | 軽 | (B)(C)が並列配置だが解説は直列順で記述 → **解説側を修正する方針のためプロンプト修正不要** |

本ラウンドで更新したプロンプト: **F261（第2版）**、**F163（第2版）**。下記「第2版」プロンプトを使用してGeminiで再生成してください。

---

## 【最優先】F261：栄養補給法の選択フローチャート

### 旧図の問題点
- (D)(E) の中にすでに「末梢静脈」「中心静脈」と語句が書かれており、問題文の「(A)〜(E)に当てはまる語句」と矛盾している
- 小さな注釈ラベル（「経鼻胃管/胃瘻/腸瘻」等）が宙に浮いていて汚い

### Gemini用プロンプト

```
Create a clean black-and-white Japanese medical textbook flowchart titled "図　栄養補給法の選択フローチャート" with the following exact structure. Use simple rounded rectangles with thin black borders, white or very light grey fill, and black Japanese text. All connecting arrows should be solid black lines with arrowheads.

Layout (top to bottom):

1. TOP BOX: "栄養アセスメント"

2. Arrow down to a DIAMOND or rounded rectangle: "（A）が機能しているか？"
   - This box has TWO outgoing arrows: left labeled "はい" and right labeled "いいえ"

3. LEFT branch (under はい): rounded rectangle labeled exactly "（B）" (nothing else inside)
   - From this box, two arrows go down to two child boxes:
     - Child 1: "経口摂取"
     - Child 2: "経管栄養（経鼻胃管・胃瘻（PEG）・腸瘻）"

4. RIGHT branch (under いいえ): rounded rectangle labeled exactly "（C）" (nothing else inside)
   - From this box, two arrows go down to two child boxes:
     - Child 1: "（D）" (label exactly as "（D）", nothing else)  -- below this box, small annotation: "2週間以内"
     - Child 2: "（E）" (label exactly as "（E）", nothing else)  -- below this box, small annotation: "2週間以上"

CRITICAL REQUIREMENTS:
- The boxes (A), (B), (C), (D), and (E) must contain ONLY the parenthesized letter labels. DO NOT write any words like "消化管", "経腸栄養", "経静脈栄養", "末梢静脈", "中心静脈", "PPN", or "TPN" inside these labeled boxes.
- Use clean textbook layout with generous spacing, clear alignment, and no floating or misplaced text.
- All Japanese characters must be rendered correctly and legibly.
- Use a standard sans-serif Japanese font (e.g., Noto Sans JP).
- Background: white. Border colors: black. Box fill: white or very light grey (#F5F5F5).
- Size: approximately 1200×900 pixels.
```

---

## F218：環境リスク管理のPDCAサイクル

### 旧図の問題点
- 各ボックス内にすでに "Plan", "Do", "Check", "Act" と英語が書かれており、答えを問う意味がない

### Gemini用プロンプト

```
Create a clean black-and-white Japanese textbook diagram titled "図　環境リスク管理のPDCAサイクル" showing a PDCA cycle with four rounded rectangles arranged in a 2x2 grid, with a circle in the center.

Layout:
- Top-left box: "（A）" (label only, no other text)
- Top-right box: "（B）" (label only)
- Bottom-right box: "（C）" (label only)
- Bottom-left box: "（D）" (label only)
- Center circle: "リスク\nコミュニケーション" (two lines)

Arrows (forming a clockwise cycle):
- (A) → (B) with horizontal arrow
- (B) → (C) with vertical arrow going down
- (C) → (D) with horizontal arrow
- (D) → (A) with vertical arrow going up

CRITICAL:
- Do NOT write "Plan", "Do", "Check", "Act", "計画", "実施", "点検", "改善" inside the boxes.
- Only the letter labels (A), (B), (C), (D) should appear inside the four boxes.
- The center circle must contain only "リスクコミュニケーション".
- Clean textbook style, white background, black lines, Noto Sans JP font.
- Size: approximately 1000×800 pixels.
```

---

## F211：化学物質の環境リスク評価の流れ

### 旧図の問題点
- (A)(B)(C)のボックス内にすでに「ハザードの特定」「用量反応評価」「曝露評価」と書かれており、答えが丸見え
- しかも正答は「A：有害性評価」となっており、図の「ハザードの特定」と呼び方が一致しない（混乱のもと）

### Gemini用プロンプト

```
Create a clean black-and-white Japanese textbook flowchart titled "図　化学物質の環境リスク評価の流れ" with the following structure.

Layout (top to bottom, with some horizontal arrangement):

1. Top box: "（A）" (label only)
2. Arrow down to box: "（B）" (label only)
3. To the right of (B), on the same horizontal level: box "（C）" (label only)
4. Arrows from both (B) and (C) converge downward to a box labeled: "リスクの判定\nPEC／PNEC比較"
5. Arrow from the judgment box down to: "（D）" (label only)

On the right side of the diagram, a vertical bracket labeled "リスク評価" spans boxes (A), (B), (C), and the judgment box (but NOT box D).

On the far right, a vertical double-headed arrow labeled "リスクコミュニケーション" spans the entire diagram.

CRITICAL REQUIREMENTS:
- Boxes (A), (B), (C), and (D) must contain ONLY the letter labels. DO NOT write "有害性評価", "ハザードの特定", "用量反応評価", "曝露評価", or "リスク管理" inside these boxes.
- Only the center "リスクの判定 PEC／PNEC比較" box has explanatory text.
- Clean textbook style, white background, thin black borders, Noto Sans JP.
- Size: approximately 1200×900 pixels.
```

---

## F163：活性汚泥法の処理フロー

### 旧図の問題点
- (C)ラベルの位置が不明瞭で、どの流れを指しているか分かりにくい
- 「余剰汚泥」の矢印の向きが混乱している

### Gemini用プロンプト

```
Create a clean black-and-white Japanese textbook process flow diagram titled "図　活性汚泥法の処理フロー" showing horizontal left-to-right flow with the following elements:

Main flow (left to right, five rectangular boxes connected by horizontal arrows):
1. "流入下水" (incoming arrow from left)
2. "最初沈殿池"
3. "（A）槽" (box with label "（A）槽")
4. "（B）池" (box with label "（B）池")
5. "消毒槽"
6. "放流" (outgoing arrow to right)

Additional elements:
- Above the (A)槽 box: downward arrow labeled "曝気（空気供給）"
- From the (B)池 box: an arrow curves BACK (right to left) below the main flow, labeled "（C）" with a dashed or thin arrow, ending at the (A)槽 box (this represents sludge return)
- From the same (B)池 box: a separate downward arrow labeled "余剰汚泥" pointing downward and out of the system (NOT connected to (A)槽)

CRITICAL:
- The return-flow arrow labeled "（C）" must clearly go from (B)池 BACK to (A)槽.
- The "余剰汚泥" arrow must clearly point DOWNWARD away from (B)池 (to disposal), not connect to any box.
- Letter labels (A), (B), (C) must stand alone; do NOT write "曝気", "最終沈殿", "返送汚泥" inside or as labels for (A), (B), (C).
- The "曝気（空気供給）" arrow at the top is a different thing and CAN be labeled (it's not a blank).
- Clean textbook style, white background, Noto Sans JP.
- Size: approximately 1400×700 pixels (landscape).
```

---

## F1004：遺伝子組換え食品の表示区分フローチャート

### 旧図の問題点
- （A）のボックスの下に「（義務表示）」と注釈があり、選択肢のうち義務表示に該当するものを選ぶヒントになっている
- 全体のレイアウトがやや詰まっている

### Gemini用プロンプト

```
Create a clean black-and-white Japanese textbook flowchart titled "遺伝子組換え食品の表示区分" with the following structure.

Start (leftmost): rounded rectangle "遺伝子組換え農作物を使用した加工食品"
→ Arrow right to DIAMOND: "加工後にDNA・タンパク質が検出可能か？"

From the diamond:
- "いいえ" branch goes DOWN to box: "表示義務なし\n（例：大豆油、しょう油、コーンフレーク）"
- "はい" branch goes RIGHT to another DIAMOND: "分別生産流通管理（IPハンドリング）を実施しているか？"

From the second diamond:
- "していない" branch goes DOWN to box labeled "（A）" (LETTER LABEL ONLY, NO OTHER TEXT, NO HINT)
- "している" branch goes RIGHT to another DIAMOND: "遺伝子組換え農作物の混入状況は？"

From the third diamond:
- "混入なし" branch: box "遺伝子組換えではない\n（任意表示）"
- "5%以下に抑制" branch: box "分別生産流通管理済\n（任意表示）"
- "遺伝子組換え使用" branch: box "遺伝子組換え\n（義務表示）"

CRITICAL REQUIREMENTS:
- The box labeled "（A）" must contain ONLY "（A）" — do NOT add "（義務表示）", "（任意表示）", or any other hint.
- Other terminal boxes may show their full labels as described above.
- Use diamonds (rotated squares) for decision nodes and rounded rectangles for process/terminal nodes.
- Clean textbook style, white background, Noto Sans JP font.
- Size: approximately 1400×900 pixels (landscape).
```

---

## 【第2版】F261：栄養補給法の選択フローチャート（2026-04-10 再修正）

### 前版（第1版）の残存問題
- 本体のフロー構造・(A)〜(E)のラベルのみ表示・ロジックは正しい
- **ただし左上領域に「栄養ア」という謎のテキスト断片が浮いている**（「栄養アセスメント」の一部が誤って独立配置されたもの）

### Gemini用プロンプト（第2版）

```
Create a clean black-and-white Japanese medical textbook flowchart titled "図　栄養補給法の選択フローチャート". The title appears at the top-left, above the diagram area. Use simple rounded rectangles with thin black borders, white fill, and black Japanese text. All connecting arrows are solid black with arrowheads.

CRITICAL: The ONLY text that appears anywhere in the image is:
- The title "図　栄養補給法の選択フローチャート" at the very top
- The text inside the boxes listed below
- The arrow labels "はい" and "いいえ"
- The small annotations "2週間以内" and "2週間以上"
There must be NO other floating, stray, orphaned, or leftover text ANYWHERE in the image. Specifically, do NOT put "栄養ア", "栄養アセスメント", or any similar fragment outside its designated box.

Layout (top to bottom, centered):

1. TOP BOX (centered, first real element below the title): rounded rectangle containing exactly "栄養アセスメント"

2. Arrow straight down to a rounded rectangle containing exactly: "（A）が機能しているか？"
   - This box has TWO outgoing arrows:
     - LEFT arrow labeled "はい"
     - RIGHT arrow labeled "いいえ"

3. LEFT branch (from "はい"): rounded rectangle labeled exactly "（B）" — nothing else inside this box
   - From (B), two arrows go down to two child boxes arranged side by side:
     - Left child: "経口摂取"
     - Right child: "経管栄養（経鼻胃管・胃瘻（PEG）・腸瘻）"

4. RIGHT branch (from "いいえ"): rounded rectangle labeled exactly "（C）" — nothing else inside this box
   - From (C), two arrows go down to two child boxes arranged side by side:
     - Left child: box labeled exactly "（D）" — below this box, a small annotation "2週間以内"
     - Right child: box labeled exactly "（E）" — below this box, a small annotation "2週間以上"

ABSOLUTE REQUIREMENTS:
- Boxes (A), (B), (C), (D), (E) must contain ONLY the parenthesized letter label. No extra words like "消化管", "経腸栄養", "経静脈栄養", "末梢静脈", "中心静脈", "PPN", "TPN".
- There must be NO floating or stray text fragments anywhere (especially NOT "栄養ア" or any partial string). Every text element must be either inside a defined box or be one of the specified arrow labels / annotations.
- The title "図　栄養補給法の選択フローチャート" appears once, at the top, outside all boxes.
- Clean textbook layout with generous whitespace, clear alignment.
- Japanese rendering must be correct; use Noto Sans JP or similar.
- Background: white. Borders: thin black. Box fill: white or very light grey.
- Size: approximately 1200×900 pixels.
```

---

## 【第2版】F163：活性汚泥法の処理フロー（2026-04-10 再修正）

### 前版（第1版）の残存問題
- フロー構造・矢印の向き・返送汚泥の還流・余剰汚泥の下向き矢印はすべて正しい
- **ただし (A)槽のすぐ横に「曝気（空気供給）」というラベル矢印があり、正答「A:曝気」のヒントになっている**。前版プロンプトでは「(A)槽の曝気ラベルは別要素だからOK」としていたが、問題の公平性を考えると削除すべきと判断

### Gemini用プロンプト（第2版）

```
Create a clean black-and-white Japanese textbook process flow diagram titled "図　活性汚泥法の処理フロー" showing horizontal left-to-right flow.

Main flow (left to right, rectangular boxes connected by horizontal arrows):
1. Incoming arrow labeled "流入下水" from the far left
2. Rectangular box: "最初沈殿池"
3. Rectangular box: "（A）槽"    ← contains ONLY "（A）槽", no other text
4. Rectangular box: "（B）池"    ← contains ONLY "（B）池", no other text
5. Rectangular box: "消毒槽"
6. Outgoing arrow labeled "放流" to the far right

Above the (A)槽 box: a small downward arrow pointing into the top of (A)槽. This arrow is labeled "空気" ONLY. DO NOT use the word "曝気" or "曝気（空気供給）" anywhere in the diagram — the question asks the student to identify what (A)槽 is (the answer being 曝気槽), so that specific keyword must not appear as a hint.

Sludge return loop:
- From the (B)池 box, a thin/dashed line curves BACK (right to left) below the main flow, with an arrowhead ending at the (A)槽 box. This return line is labeled "（C）". The label "（C）" must contain ONLY the letter, no words like "返送汚泥".

Excess sludge discharge:
- From the (B)池 box, a separate SOLID downward arrow exits the bottom of the box and points down/out of the system (not connected to any other box). This arrow is labeled "余剰汚泥".

ABSOLUTE REQUIREMENTS:
- The words "曝気", "最終沈殿", "返送汚泥" must NOT appear anywhere in the diagram. These are the answers the student must choose, so they must not leak into the figure.
- The label above (A)槽 must be just "空気" (not "曝気" and not "曝気（空気供給）").
- Letter labels (A), (B), (C) must stand alone — no accompanying words.
- The "余剰汚泥" label is acceptable because it is a distinct concept from (C) 返送汚泥 and is explicitly separated in the question.
- Clean textbook style, white background, thin black borders, Noto Sans JP.
- Size: approximately 1400×700 pixels (landscape orientation).
```

### 補足
生成後のチェックで「曝気」という文字が図中のどこにも残っていないことを確認してください。もし残っている場合は再生成。

---

## 共通の注意事項（Gemini使用時）

1. **日本語フォント**: Gemini 2.5 Flash Image / nano-banana は日本語描画が比較的得意ですが、複雑な漢字で崩れる場合があります。生成後に必ず目視確認してください。

2. **ファイル名**: 生成した画像は `FUTURE/F{番号}.png` として `eisei_yakugaku` フォルダに保存してください（例：`FUTURE/F261.png`）。既存ファイルを上書きする形で問題ありません。

3. **サイズ**: 元の画像と同程度（横長のフローチャートは1400px幅程度、縦長のものは900px幅程度）を目安に。

4. **スタイル統一**: 教科書風のモノクロ～淡グレー配色、細い黒線の枠、白背景、Noto Sans JPフォントで統一すると全問題で見た目が揃います。

5. **生成後チェックポイント**:
   - (A)(B)(C)等の空欄ボックスに「余計な語句」が書かれていないか
   - 矢印の向きが正しいか
   - 日本語テキストに文字化けがないか
   - 問題文と図の整合性（問題文が要求する構造と一致しているか）
