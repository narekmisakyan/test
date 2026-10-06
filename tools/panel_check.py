#!/usr/bin/env python3
"""Cross-check tagged question numbers against the left panel's highlighted 'Question N' item."""
import os, sys, csv, re
os.environ["OMP_THREAD_LIMIT"] = "1"
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageOps
import pytesseract
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def panel_q(path):
    im = Image.open(path).convert("RGB"); a = np.asarray(im)
    col = a[225:945, 88, :].astype(int)
    dark = (col.sum(axis=1) // 3) < 90
    runs, start = [], None
    for i in range(len(dark) + 1):
        d = dark[i] if i < len(dark) else False
        if d and start is None: start = i
        if not d and start is not None:
            if i - start >= 25: runs.append((225 + start, 225 + i))
            start = None
    if not runs: return None
    top, bot = max(runs, key=lambda r: r[1] - r[0])
    crop = ImageOps.invert(im.crop((80, top, 260, bot)).convert("L")).resize((540, (bot - top) * 3))
    t = pytesseract.image_to_string(crop, config="--psm 7").strip()
    m = re.search(r"(\d+)", t)
    return int(m.group(1)) if m else None
def work(item):
    src, frame, q = item
    return (src, frame, q, panel_q(os.path.join(S, f"frames_{src}", frame)))
if __name__ == "__main__":
    rows = list(csv.DictReader(open(sys.argv[1])))
    EXAM = {"std","match","unknown","scrolled","match_scrolled","exam"}
    last = ""; items = []; cur = None
    for r in rows:
        if r["type"] in EXAM and not r["q"]: r["q"] = last
        if r["q"]: last = r["q"]
        if not r["q"]: cur = None; continue
        if cur and cur[0] == r["q"]: cur[1].append(r)
        else:
            cur = (r["q"], [r]); items.append(cur)
    jobs = []
    for q, rs in items:
        picks = {rs[len(rs)//2]["frame"]: rs[len(rs)//2], rs[-1]["frame"]: rs[-1]}
        for r in picks.values(): jobs.append((r["src"], r["frame"], int(q)))
    with Pool(4) as p: res = p.map(work, jobs, chunksize=4)
    bad = [r for r in res if r[3] != r[2]]
    print(f"checked {len(res)} frames over {len(items)} visits; mismatches: {len(bad)}")
    for src, frame, q, pq in bad: print(f"  {src}:{frame} tagged={q} panel={pq}")
