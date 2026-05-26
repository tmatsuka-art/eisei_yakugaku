"""
ai_review_log_第N回 のバッチ承認結果を future_questions.jsonl に反映する汎用スクリプト

使い方:
    python3 apply_decisions.py --decisions _work/decisions_batchN.json --lecture 第9回 --batch batchN

各問題のレコードに ai_review メタデータを追加する。
"""
import json
import argparse
import shutil
from datetime import datetime
from pathlib import Path


def apply_changes(problem: dict, changes: dict) -> tuple[dict, list[str]]:
    """Return (updated_problem, list_of_change_summaries)."""
    summaries = []

    # problem text
    if changes.get("problem_text_new"):
        problem["problem_text"] = changes["problem_text_new"]
        summaries.append("問題文書き換え")

    # choices (1..5)
    for i in range(1, 6):
        key = f"choice_{i}"
        new_val = changes.get(key)
        if new_val is not None:  # None や 省略は変更しない
            if i - 1 < len(problem["choices"]):
                problem["choices"][i - 1] = new_val
                summaries.append(f"選択肢{i}書き換え")

    # answer
    if changes.get("answer_new"):
        problem["answer"] = changes["answer_new"]
        summaries.append(f"正答位置変更→{','.join(changes['answer_new'])}")

    # comment
    if changes.get("comment_replace"):
        problem["comment"] = changes["comment_replace"]
        summaries.append("解説全面書き換え")
    elif changes.get("comment_append"):
        problem["comment"] = (problem.get("comment") or "") + changes["comment_append"]
        summaries.append("解説追記")

    # new_corecurri_code
    if changes.get("new_corecurri_code"):
        old = problem.get("new_corecurri_code", "")
        problem["new_corecurri_code"] = changes["new_corecurri_code"]
        summaries.append(f"コアカリ {old}→{changes['new_corecurri_code']}")

    # note
    if changes.get("note_new"):
        problem["note"] = changes["note_new"]
        summaries.append("note更新")

    return problem, summaries


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--decisions", required=True, help="decisions JSON file")
    p.add_argument("--lecture", required=True, help="例: 第9回")
    p.add_argument("--batch", required=True, help="例: batch1")
    p.add_argument("--jsonl", default="future_questions.jsonl")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    decisions_path = Path(args.decisions)
    jsonl_path = Path(args.jsonl)

    with open(decisions_path, encoding="utf-8") as f:
        decisions = json.load(f)

    # backup
    if not args.dry_run:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = jsonl_path.with_suffix(jsonl_path.suffix + f".bak_apply_{args.batch}_{ts}")
        shutil.copy(jsonl_path, bak)
        print(f"backup created: {bak}")

    # read all lines
    with open(jsonl_path, encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    applied = []
    skipped = []
    not_found = set(decisions.keys())

    for line in lines:
        q = json.loads(line)
        pid = q.get("problem_id")

        if pid in decisions:
            not_found.discard(pid)
            decision = decisions[pid]

            if decision["status"] == "skipped":
                # 変更せず ai_review だけ付ける
                q["ai_review"] = {
                    "status": "skipped",
                    "reviewed_at": decision.get("decision_at", datetime.now().strftime("%Y-%m-%d")),
                    "lecture": args.lecture,
                    "batch": args.batch,
                    "changes_summary": []
                }
                skipped.append(pid)
            else:
                q, summaries = apply_changes(q, decision["changes"])
                q["ai_review"] = {
                    "status": decision["status"],
                    "reviewed_at": decision.get("decision_at", datetime.now().strftime("%Y-%m-%d")),
                    "lecture": args.lecture,
                    "batch": args.batch,
                    "changes_summary": summaries
                }
                applied.append((pid, summaries))

        updated_lines.append(json.dumps(q, ensure_ascii=False) + "\n")

    if not_found:
        print(f"WARNING: not found in jsonl: {sorted(not_found)}")

    print(f"\nApplied: {len(applied)} problems")
    for pid, summaries in applied:
        print(f"  {pid}: {', '.join(summaries)}")
    if skipped:
        print(f"\nSkipped (recorded as checked): {len(skipped)} problems")
        for pid in skipped:
            print(f"  {pid}")

    if args.dry_run:
        print("\n[DRY RUN] no file written")
    else:
        with open(jsonl_path, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
        print(f"\nWrote {jsonl_path} ({len(updated_lines)} lines)")


if __name__ == "__main__":
    main()
