// 衛生薬学 国試対策 — 学生フィードバック日次ダイジェスト
//
// 過去24時間に投稿された予想問題への報告（vote_type='report'）をまとめて
// GitHub Issue として作成する。pg_cron から毎朝8時(JST)に呼ばれる。
//
// 必要なシークレット:
//   - GITHUB_TOKEN      : GitHub fine-grained PAT (Issues: Read and write)
//   - GITHUB_REPO       : "tmatsuka-art/eisei_yakugaku"
//   - CRON_SECRET       : pg_cron からの呼び出しを検証する共有秘密
// 自動注入されるシークレット:
//   - SUPABASE_URL
//   - SUPABASE_SERVICE_ROLE_KEY

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const SUPABASE_URL = Deno.env.get('SUPABASE_URL')!;
const SERVICE_ROLE_KEY = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const GITHUB_TOKEN = Deno.env.get('GITHUB_TOKEN');
const GITHUB_REPO = Deno.env.get('GITHUB_REPO') ?? 'tmatsuka-art/eisei_yakugaku';
const CRON_SECRET = Deno.env.get('CRON_SECRET');

const ADMIN_URL = 'https://tmatsuka-art.github.io/eisei_yakugaku/admin.html';

const KIND_LABELS: Record<string, string> = {
  answer_wrong: '正解が違うと思う',
  choices: '選択肢が不適切',
  wording: '問題文がわかりにくい',
  figure: '図表がおかしい',
  explanation: '解説が不十分',
  other: 'その他',
};

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

Deno.serve(async (req) => {
  // 共有秘密の検証
  const provided = req.headers.get('x-cron-secret');
  if (!CRON_SECRET || provided !== CRON_SECRET) {
    return jsonResponse({ error: 'unauthorized' }, 401);
  }
  if (!GITHUB_TOKEN) {
    return jsonResponse({ error: 'GITHUB_TOKEN not configured' }, 500);
  }

  try {
    const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

    // 過去24時間の reports を取得
    const since = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
    const { data: reports, error } = await supabase
      .from('question_feedback')
      .select('*')
      .eq('vote_type', 'report')
      .gte('created_at', since)
      .order('created_at', { ascending: true });

    if (error) {
      return jsonResponse({ error: error.message }, 500);
    }
    if (!reports || reports.length === 0) {
      return jsonResponse({ status: 'no_reports' });
    }

    // 問題ID毎にグループ化
    const grouped: Record<string, typeof reports> = {};
    for (const r of reports) {
      (grouped[r.question_id] ??= []).push(r);
    }

    const today = new Date().toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      timeZone: 'Asia/Tokyo',
    });
    const qids = Object.keys(grouped).sort();

    // Issue 本文構築
    const lines: string[] = [];
    lines.push('## 📋 過去24時間の学生報告ダイジェスト');
    lines.push('');
    lines.push(`- 受信数: **${reports.length} 件**`);
    lines.push(`- 対象問題数: **${qids.length} 問**`);
    lines.push('');
    lines.push(`🔗 管理画面: ${ADMIN_URL}`);
    lines.push('');
    lines.push('---');
    lines.push('');

    for (const qid of qids) {
      const items = grouped[qid];
      lines.push(`### ${qid} (${items.length}件)`);
      for (const r of items) {
        const kind = KIND_LABELS[r.report_kind] || r.report_kind || '(未指定)';
        const time = new Date(r.created_at).toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });
        lines.push(`- **${kind}** — ${time}`);
        if (r.comment) {
          const safeComment = String(r.comment).replace(/\n/g, ' ').slice(0, 500);
          lines.push(`  - コメント: ${safeComment}`);
        }
      }
      lines.push('');
    }

    lines.push('---');
    lines.push('');
    lines.push('対応完了後、このIssueをCloseしてください。');

    const body = lines.join('\n');
    const title = `📋 学生報告ダイジェスト ${today}（${reports.length}件）`;

    // GitHub Issue 作成
    const ghRes = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/issues`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Content-Type': 'application/json',
        'User-Agent': 'eisei-yakugaku-digest/1.0',
      },
      body: JSON.stringify({ title, body, assignees: ['tmatsuka-art'] }),
    });

    if (!ghRes.ok) {
      const errText = await ghRes.text();
      return jsonResponse(
        { error: 'GitHub API failed', status: ghRes.status, detail: errText },
        500,
      );
    }

    const issue = await ghRes.json();
    return jsonResponse({
      status: 'success',
      issue_url: issue.html_url,
      issue_number: issue.number,
      reports_count: reports.length,
    });
  } catch (e) {
    return jsonResponse({ error: String(e) }, 500);
  }
});
