#!/usr/bin/env python3
"""match_extract.py TAGS_ALL.csv FINAL.json OUT.json : OCR both panes of every distinct matching-question state.
For each match question: list of states (t, frame, left_text, right_text) in time order, deduped by pane hashes.
"""
import sys, os, csv, json
os.environ["OMP_THREAD_LIMIT"] = "1"
from multiprocessing import Pool
from PIL import Image
import pytesseract
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def hd(a, b): return bin(int(a, 16) ^ int(b, 16)).count("1")
def ocr(im, box):
    c = im.crop(box); c = c.resize((c.width*2, c.height*2), Image.LANCZOS)
    return pytesseract.image_to_string(c, config="--psm 4")
def work(item):
    q, t, src, name, box_top = item
    im = Image.open(os.path.join(S, f"frames_{src}", name)).convert("RGB")
    bt = int(box_top)
    left = ocr(im, (380, bt + 195, 1090, 900)); right = ocr(im, (1135, bt + 195, 1840, 900))
    return {"q": q, "t": t, "frame": f"{src}:{name}", "left": " ".join(left.split()), "right": right}
rows = list(csv.DictReader(open(sys.argv[1]))); info = json.load(open(sys.argv[2]))
matchq = {int(q) for q, d in info.items() if d["type"] == "match"}
EXAM = {"std","match","unknown","scrolled","match_scrolled","exam"}
last_q = ""
items = []; last = {}
for r in rows:
    if r["type"] in EXAM and not r["q"]: r["q"] = last_q
    if r["q"]: last_q = r["q"]
    if r["type"] != "match" or not r["q"] or int(r["q"]) not in matchq: continue
    q = int(r["q"]); key = (r["left_hash"], r["right_hash"])
    if q in last and hd(last[q][0], key[0]) <= 3 and hd(last[q][1], key[1]) <= 3: items[-1] = (q, int(r["t"]), r["src"], r["frame"], r["box_top"]); continue
    last[q] = key; items.append((q, int(r["t"]), r["src"], r["frame"], r["box_top"]))
print("states to OCR:", len(items), flush=True)
with Pool(4) as p: res = p.map(work, items, chunksize=4)
out = {}
for d in res: out.setdefault(str(d["q"]), []).append(d)
json.dump(out, open(sys.argv[3], "w"), indent=1)
print({q: len(v) for q, v in out.items()})
