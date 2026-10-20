"""PPT掲載問題26問をクイズの問題プールに入れ、第4・5回ゼミ演習セットを組み直すSQLを作る（2026-10-15）。"""
import json

R = '/home/claude/eisei_yakugaku/'
OUT = '/home/claude/eisei_quiz_live/scripts/ppt_pool_and_lec45_seminar_set_2026-10-15.sql'
QUIZ_ID = '2b57dfc5-dbc0-4fc4-9756-f4d72376d25b'
TITLE = '松川_衛生化学I_第４回・第５回ゼミ演習'
SUBCAT = {2: '衛I-02 ビタミンと欠乏症', 3: '衛I-03 ミネラルと欠乏症', 4: '衛I-04 三大栄養素・消化吸収', 5: '衛I-05 栄養摂取・エネルギー代謝'}

SET = ['F611', 'F627', 'F769', 'F1431', 'F612', 'F1527', 'F628', 'F650', 'F613', 'F1531', 'F1501', 'F719', 'F624',
       'F1506', 'F243', 'F1530', 'F1429', 'F1534', 'F1507', 'F1533', 'F1535', 'F1438', 'F1366', 'F1444', 'F1445',
       'F1376', 'F1537', 'F1536',
       'F1513', 'F1515', 'F232', 'F1517', 'F1518', 'F1521', 'F1525', 'F651', 'F1424', 'F1428', 'F1420',
       'F1434']
assert len(SET) == 40 and len(set(SET)) == 40

rows = {json.loads(l)['problem_id']: json.loads(l) for l in open(R + 'future_questions.jsonl')}
lm = json.load(open(R + 'lecture_map.json'))['衛I']['lectures']
lec_of = {i: int(k) for k, v in lm.items() for i in v['ids']}
ppt = [f'F{n}' for n in range(1512, 1538)]


def q(s):
    return "'" + s.replace("'", "''") + "'"


vals = []
for pid in ppt:
    r = rows[pid]
    sel = len(r['answer'])
    tl = (30 if sel == 1 else 50) + (10 if r['assets'] else 0)
    meta = {'origin': 'prediction', 'subcat': SUBCAT[lec_of[pid]], 'corecurri': r['new_corecurri_code'], 'tags': ['PPT掲載']}
    assets = f"ARRAY[{q('/' + r['assets'][0])}]" if r['assets'] else 'NULL::text[]'
    vals.append(f"  ({q(pid)}, {q(r['problem_text'])}, {q(json.dumps(r['choices'], ensure_ascii=False))}::jsonb, "
                f"ARRAY[{','.join(r['answer'])}], {sel}, {tl}, {q(r['comment'])}, {q(json.dumps(meta, ensure_ascii=False))}::jsonb, {assets})")

ids_sql = ','.join(q(i) for i in SET)
sql = f"""


-- 衛生化学I 授業スライド掲載問題（PPT掲載問題）26問をクイズの問題プールに入れ、
-- 演習セット「{TITLE}」を組み直す（2026-10-15、松川の依頼）。
-- Supabase の SQL Editor に全部貼り付けて、Run を1回押す。
--   ① PPT掲載問題26問（F1512〜F1537、図9枚）を問題プールに入れる（すでにあれば新しい内容に書き換える）
--   ② 演習セットの40問を入れ替える（第4・5回 29問＋第2・3回の復習 11問。最後の40問目は得点2倍）
--      ・このセットでまだ誰も解答していなければ、同じセットの中身を入れ替える
--      ・すでに解答の記録があれば、記録を消さないよう、元のセットは残して「（見直し版）」という新しいセットを作る
--   ③ 最後に、できた演習セットの40問を一覧で表示する（40行出れば完了）
-- 何度実行しても同じ結果になる。

-- ① 問題プールへ
WITH v(sid, t, opts, corr, sel, tl, expl, meta, assets) AS (VALUES
{(','+chr(10)).join(vals)}
),
upd AS (
  UPDATE questions q
     SET text = v.t, options = v.opts, correct_indices = v.corr, select_count = v.sel, explanation = v.expl, assets = v.assets
    FROM v
   WHERE q.source_id = v.sid
  RETURNING q.source_id
)
INSERT INTO questions (quiz_id, question_no, text, options, correct_indices, select_count,
                       time_limit_seconds, difficulty_multiplier, explanation, source_id, metadata, assets)
SELECT NULL, 1, v.t, v.opts, v.corr, v.sel, v.tl, 1.2, v.expl, v.sid, v.meta, v.assets
  FROM v
 WHERE NOT EXISTS (SELECT 1 FROM questions q WHERE q.source_id = v.sid AND q.quiz_id IS NULL);

-- ② 演習セットの入れ替え
DO $$
DECLARE
  set_id    uuid   := '{QUIZ_ID}';
  set_title text   := '{TITLE}';
  set_desc  text   := '第4回（三大栄養素・消化吸収）・第5回（栄養摂取・エネルギー代謝）29問＋第2・3回（ビタミン・ミネラル）の復習11問。授業スライド掲載問題を含む。同じ論点の問題が重ならないように選んだ（2026-10-15 見直し）。';
  ids       text[] := ARRAY[{ids_sql}];
  missing   text;
  played    boolean;
  target    uuid;
BEGIN
  IF NOT EXISTS (SELECT 1 FROM quizzes WHERE id = set_id) THEN
    RAISE EXCEPTION '演習セット「%」が見つかりません', set_title;
  END IF;

  SELECT string_agg(x, ', ') INTO missing FROM unnest(ids) AS x
   WHERE NOT EXISTS (SELECT 1 FROM questions q WHERE q.quiz_id IS NULL AND q.source_id = x);
  IF missing IS NOT NULL THEN
    RAISE EXCEPTION '問題プールに見つからない問題があります：%', missing;
  END IF;

  SELECT EXISTS (SELECT 1 FROM answers a JOIN questions q ON q.id = a.question_id WHERE q.quiz_id = set_id)
      OR EXISTS (SELECT 1 FROM buzzes b JOIN questions q ON q.id = b.question_id WHERE q.quiz_id = set_id)
    INTO played;

  IF played THEN
    SELECT id INTO target FROM quizzes WHERE title = set_title || '（見直し版）';
    IF target IS NULL THEN
      INSERT INTO quizzes (title, description, source) VALUES (set_title || '（見直し版）', set_desc, 'pool-builder')
      RETURNING id INTO target;
    ELSE
      -- 見直し版をすでに作っていて、まだ解答がなければ作り直す
      IF EXISTS (SELECT 1 FROM answers a JOIN questions q ON q.id = a.question_id WHERE q.quiz_id = target) THEN
        RAISE EXCEPTION '「%（見直し版）」にも解答の記録があるため、変更しませんでした', set_title;
      END IF;
      DELETE FROM questions WHERE quiz_id = target;
    END IF;
    RAISE NOTICE '元のセットには解答の記録があるので、新しいセット「%（見直し版）」を作りました', set_title;
  ELSE
    target := set_id;
    DELETE FROM questions WHERE quiz_id = target;
    UPDATE quizzes SET description = set_desc WHERE id = target;
  END IF;

  INSERT INTO questions (quiz_id, question_no, text, options, correct_indices, select_count,
                         time_limit_seconds, difficulty_multiplier, explanation, source_id, assets, metadata)
  SELECT target, o.n, p.text, p.options, p.correct_indices, p.select_count,
         p.time_limit_seconds, p.difficulty_multiplier, p.explanation, p.source_id, p.assets, p.metadata
    FROM unnest(ids) WITH ORDINALITY AS o(sid, n)
    CROSS JOIN LATERAL (
      SELECT * FROM questions q
       WHERE q.quiz_id IS NULL AND q.source_id = o.sid
       ORDER BY q.created_at DESC LIMIT 1
    ) AS p
   ORDER BY o.n;
END $$;

-- ③ 確認（40行出れば完了）
SELECT z.title AS "演習セット", q.question_no AS "順番", q.source_id AS "問題番号",
       CASE WHEN q.select_count = 2 THEN '2つ選べ' ELSE '1つ選べ' END AS "形式",
       CASE WHEN q.assets IS NOT NULL AND cardinality(q.assets) > 0 THEN '図あり' ELSE '' END AS "図",
       left(q.text, 36) AS "問題文（先頭）"
  FROM questions q JOIN quizzes z ON z.id = q.quiz_id
 WHERE z.title IN ('{TITLE}', '{TITLE}（見直し版）')
   AND z.description LIKE '%2026-10-15 見直し%'
 ORDER BY z.title, q.question_no;
"""
open(OUT, 'w').write(sql)
print(OUT, len(sql))
