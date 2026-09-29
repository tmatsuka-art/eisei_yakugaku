# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding="utf-8")
fq = [json.loads(l) for l in open("future_questions.jsonl", encoding="utf-8") if l.strip()]
for o in fq:
    t = o.get("problem_text", "") + " ".join(o.get("choices", [])) + o.get("comment", "")
    if "形質変更" in t:
        print(f"[{o['problem_id']}] _subcat={o.get('_subcat')} code={o.get('new_corecurri_code')}")
        print(f"  {o.get('problem_text','')[:130]}")
        print()
