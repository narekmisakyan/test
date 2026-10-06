#!/usr/bin/env python3
"""Merge tag CSVs with time offsets: merge_tags.py OUT.csv big.csv:0 small.csv:7208  (frame i -> t = offset + i - 1)"""
import sys, csv
out = sys.argv[1]; rows = []
for spec in sys.argv[2:]:
    path, off = spec.split(":"); off = float(off); src = path.replace("tags_", "").replace(".csv", "")
    for r in csv.DictReader(open(path)):
        r["t"] = str(int(off + int(r["frame"].split(".")[0]) - 1)); r["src"] = src; rows.append(r)
rows.sort(key=lambda r: int(r["t"]))
with open(out, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["src", "t"] + [k for k in rows[0] if k not in ("src", "t")]); w.writeheader(); w.writerows(rows)
print(f"merged {len(rows)} rows -> {out}")
