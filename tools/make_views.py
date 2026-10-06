#!/usr/bin/env python3
"""make_views.py FINAL.json OUT_DIR : crop per-question views and OCR them.
std: OUT/qNN.jpg (content area of view_frame) [+ qNN_sel.jpg if the selection frame differs], qNN.txt (OCR stem+options)
match: OUT/qNN_mK.jpg for each distinct pane state, qNN.txt (OCR stem + panes of the last state)
"""
import sys, os, json
os.environ["OMP_THREAD_LIMIT"] = "1"
from PIL import Image
import pytesseract
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def frame(ref):
    src, name = ref.split(":"); return Image.open(os.path.join(S, f"frames_{src}", name)).convert("RGB")
def ocr(im, box, psm=6):
    c = im.crop(box); c = c.resize((c.width*2, c.height*2), Image.LANCZOS)
    return " ".join(pytesseract.image_to_string(c, config=f"--psm {psm}").split())
info = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
for q in sorted(info, key=int):
    d = info[q]; n = int(q)
    if not d.get("view_frame"): print(q, "NO VIEW FRAME"); continue
    im = frame(d["view_frame"]); top = d["box_top"]
    if d["type"] == "std":
        im.crop((365, top - 8, 1880, 945)).save(f"{out}/q{n:02d}.jpg", quality=88)
        rows = [tuple(map(int, x.split("-"))) for x in d.get("rows", "").split(";") if x]
        lines = ["STEM: " + ocr(im, (495, top + 7, 1845, (rows[0][0] - 45) if rows else 945))]
        for i, (rt, rb) in enumerate(rows):
            nxt = rows[i+1][0] - 20 if i+1 < len(rows) else min(rb + 70, 945)
            lines.append(f"{chr(65+i)}: " + ocr(im, (492, rt - 4, 1845, nxt)))
        if d.get("sel_frame") and d["sel_frame"] != d["view_frame"]:
            frame(d["sel_frame"]).crop((365, 225, 1880, 945)).save(f"{out}/q{n:02d}_sel.jpg", quality=88)
            lines.append(f"[selection frame {d['sel_frame']}: sel={d.get('final_sel')}{d.get('sel_flag','')}]")
        open(f"{out}/q{n:02d}.txt", "w").write("\n".join(lines) + "\n")
    else:
        lines = ["STEM: " + ocr(im, (495, top + 7, 1845, top + 160))]
        for k, st in list(enumerate(d["match_states"]))[-4:]:
            fm = frame(st["frame"]); bt = st.get("box_top") or top
            fm.crop((365, bt - 8, 1880, 945)).save(f"{out}/q{n:02d}_m{k}.jpg", quality=88)
            lines.append(f"[state {k} {st['frame']} t={st['t']} held {st['n']}s] LEFT: " + ocr(fm, (380, bt + 195, 1090, 900), 4) + " || RIGHT: " + ocr(fm, (1135, bt + 195, 1840, 900), 4))
        open(f"{out}/q{n:02d}.txt", "w").write("\n".join(lines) + "\n")
    print(q, d["type"], "ok")
