#!/usr/bin/env python3
"""endcheck.py FINAL.json OUT.json : for every std question, decode the last 3 s of its final visit at 30 fps and
record the selection on the last frame that still shows this question. Prints a table."""
import sys, os, json, subprocess, tempfile, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from tag_frames import find_timer, find_box, rows, qnum
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VID = {"big": (f"{S}/downloads/big_1sFIpb.mp4", 0), "small": (f"{S}/downloads/small_1IeE9d.mp4", 7208)}
info = json.load(open(sys.argv[1])); out = {}
for q in sorted(info, key=int):
    d = info[q]
    if d["type"] != "std": continue
    src = d["sel_frame"].split(":")[0] if d.get("sel_frame") else d["view_frame"].split(":")[0]
    end_t = d["last_t"]; path, off = VID[src]; local = end_t - off
    tmp = tempfile.mkdtemp(prefix=f"ec{q}_", dir=f"{S}/endcheck")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", f"{max(local-2.5,0):.3f}", "-i", path, "-t", "3.5", "-vf", "fps=30", "-q:v", "3", f"{tmp}/%04d.jpg"], check=True)
    seq = []
    for f in sorted(glob.glob(f"{tmp}/*.jpg")):
        im = Image.open(f).convert("RGB"); a = np.asarray(im)
        tm = find_timer(a)
        if not tm: seq.append(("-", "", 0)); continue
        box = find_box(a, tm[0]+60, tm[0]+260)
        qq = qnum(im, box) if box else None
        y0 = (box[1] + 5) if box else (tm[1] + 70)
        rs = rows(a, y0)
        sel = "".join(chr(65+i) for i, r in enumerate(rs) if r[0] == "RED")
        seq.append((str(qq) if qq else ("scr" if rs else "?"), sel, len(rs)))
    # last frame showing this q (or scrolled continuation before a different q appears)
    last_sel, last_n, last_idx = None, 0, -1
    for i, (qq, sel, n) in enumerate(seq):
        if qq == q or (qq == "scr" and last_idx >= 0 and seq[last_idx][0] in (q, "scr")) or (qq == "scr" and i > 0 and last_idx == i-1):
            last_sel, last_n, last_idx = sel, n, i
        elif qq not in ("-", "?") and qq != q and qq != "scr":
            break
    changes = []
    for i, (qq, sel, n) in enumerate(seq[:last_idx+1]):
        if n == 4 and (not changes or changes[-1][1] != sel): changes.append((i, sel))
    out[q] = {"final_sel_1fps": d.get("final_sel", ""), "final_sel_30fps": last_sel, "nrows": last_n, "changes": changes, "frames": len(seq), "last_idx": last_idx}
    flag = "" if (last_sel == d.get("final_sel", "") or last_sel is None) else "  <-- DIFFERS"
    print(f"q{q:>2}: 1fps={d.get('final_sel','') or '-'} 30fps={last_sel if last_sel is not None else 'n/a'} rows={last_n} changes={changes}{flag}", flush=True)
json.dump(out, open(sys.argv[2], "w"), indent=1)
