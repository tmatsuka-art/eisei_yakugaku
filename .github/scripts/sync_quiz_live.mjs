/**
 * 問題JSON（過去問・予想問題）の修正を、クイズ（Eisei Quiz Live）のデータベースへ反映する。
 *
 * 2026-10-09 先生の依頼：「JSON を直したらクイズのデータベースにも自動で反映する仕組み」。
 *
 * しくみ
 *   - 2つの版（直す前 BASE と直した後 HEAD）の JSON を比べ、中身が変わった問題番号だけを選ぶ。
 *     （クイズ側で先生が手で直した問題を、関係のない JSON の更新で上書きしないため）
 *   - クイズの questions 表のうち、source_id がその問題番号の行（問題プールと、
 *     すでに作った演習セットの両方）を、JSON の内容に書き換える。
 *   - 書き換えるのは 問題文・選択肢・正答・選択数・解説 だけ。新しい問題の追加や削除はしない
 *     （追加は従来どおりクイズの「JSON取込」から。削除された問題番号は報告だけする）。
 *   - JSON → クイズの対応はクイズ側の取込み（ImportForm.tsx の normalize）と同じ：
 *     problem_text→text, choices→options, answer→correct_indices, comment→explanation。
 *     選択肢が画像の中にある問題（choices=["IMAGES"]）は選択肢を書き換えない。
 *
 * 使い方
 *   node sync_quiz_live.mjs --base <コミット> --head <コミット> [--apply]
 *   node sync_quiz_live.mjs --ids 101021,F225 [--apply]     （指定した問題を今の JSON で反映）
 *   --apply を付けないと、変更点を表示するだけ（データベースは書き換えない）。
 *
 * 環境変数：QUIZ_SUPABASE_URL, QUIZ_SUPABASE_SERVICE_ROLE_KEY（GitHub の Secrets に登録）
 */
import { execFileSync } from 'node:child_process';
import { readFileSync, appendFileSync } from 'node:fs';

const FILES = ['hygiene_with_images_v4.jsonl', 'future_questions.jsonl'];
const FIELDS = ['text', 'options', 'correct_indices', 'select_count', 'explanation'];

const args = process.argv.slice(2);
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
const APPLY = args.includes('--apply');
const BASE = opt('--base');
const HEAD = opt('--head') ?? 'HEAD';
const IDS = opt('--ids');

const out = [];
const log = (s = '') => {
  console.log(s);
  out.push(s);
};

function readJsonl(text) {
  const map = new Map();
  for (const line of text.split('\n')) {
    if (!line.trim()) continue;
    const r = JSON.parse(line);
    if (r.problem_id) map.set(String(r.problem_id), r);
  }
  return map;
}
function loadAt(rev) {
  const all = new Map();
  for (const f of FILES) {
    let text = '';
    try {
      text = rev
        ? execFileSync('git', ['show', `${rev}:${f}`], { encoding: 'utf8', maxBuffer: 1 << 28 })
        : readFileSync(f, 'utf8');
    } catch {
      continue; // その版にファイルがない
    }
    for (const [k, v] of readJsonl(text)) all.set(k, v);
  }
  return all;
}

/** JSON の1問 → クイズの questions の列（クイズ側の取込みと同じ変換） */
function toQuiz(r) {
  const correct = (Array.isArray(r.answer) ? r.answer : [])
    .map((v) => (typeof v === 'number' ? v : parseInt(String(v), 10)))
    .filter((n) => Number.isInteger(n));
  const imageChoices =
    Array.isArray(r.choices) && r.choices.length === 1 && r.choices[0] === 'IMAGES';
  const q = {
    text: typeof r.problem_text === 'string' ? r.problem_text : null,
    correct_indices: [...new Set(correct)],
    select_count: new Set(correct).size,
    explanation: typeof r.comment === 'string' ? r.comment : null,
  };
  if (!imageChoices) q.options = Array.isArray(r.choices) ? r.choices : null;
  return q;
}
const same = (a, b) => JSON.stringify(a ?? null) === JSON.stringify(b ?? null);

/** 反映してよい内容か（クイズの表の決まり：選択肢2〜5、選択数は選択肢より少ない） */
function problemOf(q, nOptions) {
  if (!q.text || !q.text.trim()) return '問題文が空';
  const n = q.options ? q.options.length : nOptions;
  if (q.options && (n < 2 || n > 5)) return `選択肢が${n}個（クイズは2〜5個まで）`;
  if (q.correct_indices.length === 0) return '正答がない';
  if (q.correct_indices.some((i) => i < 1 || i > n)) return '正答の番号が選択肢の数を超えている';
  if (q.select_count >= n) return '選択数が選択肢の数以上';
  return null;
}

async function main() {
  // 1. 変わった問題番号を決める
  const head = loadAt(HEAD === 'WORKTREE' ? null : HEAD);
  let ids;
  if (IDS) {
    ids = IDS.split(',').map((s) => s.trim()).filter(Boolean);
  } else {
    if (!BASE) throw new Error('--base か --ids を指定してください');
    const base = loadAt(BASE);
    ids = [];
    for (const [id, r] of head) {
      const b = base.get(id);
      if (b && !same(toQuiz(b), toQuiz(r))) ids.push(id);
    }
    const removed = [...base.keys()].filter((id) => !head.has(id));
    if (removed.length) log(`JSON から消えた問題（クイズ側は変えません）：${removed.join(', ')}`);
  }
  log(`JSON で中身が変わった問題：${ids.length} 問`);
  if (ids.length === 0) return;

  // 末尾の / や /rest/v1/ が付いていても動くようにする
  const URL_ = (process.env.QUIZ_SUPABASE_URL ?? '').trim().replace(/\/+$/, '').replace(/\/rest\/v1$/, '');
  const KEY_RAW = process.env.QUIZ_SUPABASE_SERVICE_ROLE_KEY;
  const KEY = (KEY_RAW ?? '').trim();
  if (!URL_ || !KEY) throw new Error('QUIZ_SUPABASE_URL / QUIZ_SUPABASE_SERVICE_ROLE_KEY が設定されていません');
  const H = { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' };

  // 2. クイズ側の該当行を読む（100件ずつ）
  const rows = [];
  for (let i = 0; i < ids.length; i += 100) {
    const chunk = ids.slice(i, i + 100).map((s) => `"${s}"`).join(',');
    const res = await fetch(
      `${URL_}/rest/v1/questions?select=id,quiz_id,source_id,${FIELDS.join(',')}&source_id=in.(${encodeURIComponent(chunk)})`,
      { headers: H }
    );
    if (!res.ok) throw new Error(`クイズのデータベースを読めません（${res.status} ${await res.text()}）`);
    rows.push(...(await res.json()));
  }

  // 3. 書き換え
  let updated = 0, skipped = 0, unchanged = 0;
  const notInQuiz = ids.filter((id) => !rows.some((r) => r.source_id === id));
  for (const row of rows) {
    const q = toQuiz(head.get(row.source_id));
    const bad = problemOf(q, Array.isArray(row.options) ? row.options.length : 0);
    const where = row.quiz_id ? `演習セット ${row.quiz_id.slice(0, 8)}` : '問題プール';
    if (bad) {
      log(`- ${row.source_id}（${where}）：反映しません（${bad}）`);
      skipped++;
      continue;
    }
    const patch = {};
    for (const f of FIELDS) if (f in q && !same(q[f], row[f])) patch[f] = q[f];
    if (Object.keys(patch).length === 0) {
      unchanged++;
      continue;
    }
    log(`- ${row.source_id}（${where}）：${Object.keys(patch).join('・')} を更新${APPLY ? '' : '（下見）'}`);
    if (APPLY) {
      const res = await fetch(`${URL_}/rest/v1/questions?id=eq.${row.id}`, {
        method: 'PATCH',
        headers: { ...H, Prefer: 'return=minimal' },
        body: JSON.stringify(patch),
      });
      if (!res.ok) throw new Error(`${row.source_id} を書き換えられません（${res.status} ${await res.text()}）`);
    }
    updated++;
  }
  log('');
  log(`更新 ${updated} 行${APPLY ? '' : '（下見のみ・未反映）'}／すでに同じ ${unchanged} 行／反映しない ${skipped} 行`);
  if (notInQuiz.length) log(`クイズに入っていない問題（何もしません）：${notInQuiz.length} 問`);
}

main()
  .catch((e) => {
    log(`エラー：${e.message}`);
    if (process.env.GITHUB_ACTIONS) console.log(`::error::${e.message.replace(/\n/g, ' ')}`);
    process.exitCode = 1;
  })
  .finally(() => {
    // 結果の要約を注釈にも出す（Actions の画面の一番上に表示される）
    if (process.env.GITHUB_ACTIONS && out.length)
      console.log(`::notice title=クイズへの反映::${out.filter(Boolean).slice(-3).join(' / ')}`);
    if (process.env.GITHUB_STEP_SUMMARY)
      appendFileSync(process.env.GITHUB_STEP_SUMMARY, '## クイズへの反映\n\n```\n' + out.join('\n') + '\n```\n');
  });
