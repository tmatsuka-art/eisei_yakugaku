# -*- coding: utf-8 -*-
# 指定problem_idの本文を表示（過去問・予想問題 両対応）。判定用の汎用ツール。
# 使い方: python _work/show_q.py F003 F517 ...
import sys, json
sys.stdout.reconfigure(encoding="utf-8")

idset = set(sys.argv[1:])
if not idset:
    print("usage: python _work/show_q.py <id> [<id> ...]")
    sys.exit(0)

found = set()
for path in ("future_questions.jsonl", "hygiene_with_images_v4.jsonl"):
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                o = json.loads(line)
                if o.get("problem_id") in idset:
                    found.add(o["problem_id"])
                    print(f"### {o['problem_id']}  [{o.get('new_corecurri_code')}]  [{o.get('_subcat','')}]")
                    print("Q:", o.get("problem_text", "").strip())
                    for i, c in enumerate(o.get("choices", []), 1):
                        print(f"  {i}. {c}")
                    print("A:", o.get("answer"))
                    cm = o.get("comment", "").strip()
                    if cm:
                        print("解説:", cm[:300])
                    print()
    except FileNotFoundError:
        pass

missing = idset - found
if missing:
    print("見つからなかったID:", ", ".join(sorted(missing)))
