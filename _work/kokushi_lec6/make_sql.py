"""衛生化学I 第6回（特別用途食品・保健機能食品）の見直しをクイズの問題プールに反映するSQLを作る（2026-10-23）。"""
import json
R = '/home/claude/eisei_yakugaku/'
OUT = '/home/claude/eisei_quiz_live/scripts/lec6_pool_update_2026-10-23.sql'
SUBCAT = '衛I-06 特別用途食品・保健機能食品'
fq = {json.loads(l)['problem_id']: json.loads(l) for l in open(R + 'future_questions.jsonl')}
pq = {json.loads(l)['problem_id']: json.loads(l) for l in open(R + 'hygiene_with_images_v4.jsonl')}
ids = json.load(open(R + 'lecture_map.json'))['衛I']['lectures']['6']['ids']
log = json.load(open(R + '_work/kokushi_lec6/apply_log_lec6.json'))
DELETED = log['deleted']
PAST_FIXED = [i for i in ids if i in pq and pq[i].get('ai_review', {}).get('batch') == 'kokushi_lec6_1023']
q = lambda s: "'" + s.replace("'", "''") + "'"

vals = []
for pid in [i for i in ids if i in fq]:
    r = fq[pid]; sel = len(r['answer'])
    tl = (30 if sel == 1 else 50)
    meta = {'origin': 'prediction', 'subcat': SUBCAT, 'corecurri': r.get('new_corecurri_code'), 'tags': r.get('tags') or []}
    vals.append(f"  ({q(pid)}, {q(r['problem_text'])}, {q(json.dumps(r['choices'], ensure_ascii=False))}::jsonb, "
                f"ARRAY[{','.join(r['answer'])}], {sel}, {tl}, {q(r['comment'])}, {q(json.dumps(meta, ensure_ascii=False))}::jsonb)")
pvals = [f"  ({q(pid)}, {q(pq[pid]['comment'])})" for pid in PAST_FIXED]
dl = ','.join(q(i) for i in DELETED)
fut_ids = ','.join(q(i) for i in ids if i in fq)
sql = f"""


-- 衛生化学I 第6回（特別用途食品・保健機能食品）の見直しを、クイズの問題プールに反映する（2026-10-23、松川の依頼）。
-- Supabase の SQL Editor に全部貼り付けて、Run を1回押す。何度実行しても同じ結果になる。
--   ① 第6回から削除した予想問題{len(DELETED)}問を、問題プールから消す
--      （すでに作った演習セットの中の同じ問題は、解答の記録を守るため消さない。最後の表で数を示す）
--   ② 第6回の予想問題{len(vals)}問を、問題プールに入れる／新しい内容に書き換える（新しい問題36問 F1538〜F1573 を含む）
--      単元は「{SUBCAT}」にそろえる。プールと演習セットの両方の行の中身を書き換える（GitHub の自動反映と同じ）。
--   ③ 解説を直した過去問{len(PAST_FIXED)}問の解説を書き換える
--   ④ 最後に結果を表示する

-- ① 削除した予想問題を問題プールから消す（解答の記録が付いている行は残す）
DELETE FROM questions q
 WHERE q.quiz_id IS NULL AND q.source_id IN ({dl})
   AND NOT EXISTS (SELECT 1 FROM answers a WHERE a.question_id = q.id)
   AND NOT EXISTS (SELECT 1 FROM buzzes b WHERE b.question_id = q.id);

-- ② 第6回の予想問題
WITH v(sid, t, opts, corr, sel, tl, expl, meta) AS (VALUES
{(','+chr(10)).join(vals)}
),
upd AS (
  UPDATE questions q
     SET text = v.t, options = v.opts, correct_indices = v.corr, select_count = v.sel, explanation = v.expl,
         assets = NULL,
         metadata = CASE WHEN q.quiz_id IS NULL
                         THEN jsonb_set(COALESCE(q.metadata, '{{}}'::jsonb), '{{subcat}}', to_jsonb({q(SUBCAT)}::text))
                         ELSE q.metadata END
    FROM v
   WHERE q.source_id = v.sid
  RETURNING q.source_id
)
INSERT INTO questions (quiz_id, question_no, text, options, correct_indices, select_count,
                       time_limit_seconds, difficulty_multiplier, explanation, source_id, metadata, assets)
SELECT NULL, 1, v.t, v.opts, v.corr, v.sel, v.tl, 1.2, v.expl, v.sid, v.meta, NULL
  FROM v
 WHERE NOT EXISTS (SELECT 1 FROM questions q WHERE q.source_id = v.sid AND q.quiz_id IS NULL);

-- ③ 過去問の解説
WITH v(sid, expl) AS (VALUES
{(','+chr(10)).join(pvals)}
)
UPDATE questions q SET explanation = v.expl FROM v WHERE q.source_id = v.sid;

-- ④ 結果
SELECT '問題プールの第6回の予想問題' AS "項目", count(*) AS "数（{len(vals)}なら完了）"
  FROM questions WHERE quiz_id IS NULL AND source_id IN ({fut_ids})
UNION ALL
SELECT '問題プールに残った削除済みの問題（0なら完了）', count(*)
  FROM questions WHERE quiz_id IS NULL AND source_id IN ({dl})
UNION ALL
SELECT '演習セットの中にある削除済みの問題（消していません）', count(*)
  FROM questions WHERE quiz_id IS NOT NULL AND source_id IN ({dl});
"""
open(OUT, 'w').write(sql)
print(OUT, len(vals), len(PAST_FIXED), len(DELETED))
