# -*- coding: utf-8 -*-
import sys, json
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")

lm = json.load(open("lecture_map.json", encoding="utf-8"))

# 過去問ID(6桁) → [ラベル "科目-回 テーマ"]
m = defaultdict(list)
for subj, sdata in lm.items():
    for lec, ldata in sdata.get("lectures", {}).items():
        theme = ldata.get("theme", "")
        try:
            label = f"{subj}-{int(lec):02d} {theme}"
        except ValueError:
            label = f"{subj}-{lec} {theme}"
        for x in ldata.get("ids", []):
            if str(x)[:1].isdigit():  # 過去問(6桁)のみ
                m[str(x)].append(label)

dup = {k: v for k, v in m.items() if len(v) > 1}
print(f"過去問の配置先（ユニークID数）: {len(m)}")
print(f"重複配置（複数授業回に入る過去問）: {len(dup)} 件")
for k, v in list(dup.items())[:40]:
    print(f"  {k}: {v}")

# マッピング保存（重複は配列のまま）
json.dump(m, open("_work/pastq_subcat_map.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\n保存: _work/pastq_subcat_map.json")
