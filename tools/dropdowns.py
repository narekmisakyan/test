#!/usr/bin/env python3
"""Detect the dropdown bars in the right pane of matching questions, OCR the letter in each, and the statement above it."""
import os, sys, json, re
os.environ["OMP_THREAD_LIMIT"] = "1"
from multiprocessing import Pool
import numpy as np
from PIL import Image
import pytesseract
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANCH = {
 "14": ["commitments|pilot for Resource", "AccurateReports|off-the-shelf", "easy to use|5 minutes|100%"],
 "17": ["Business project", "Project executive", "Supplier project"],
 "20": ["satisfier|performance need|speed of data", "'must'|must' be able|internal and external", "codes|high' in value|ease of"],
 "24": ["Approve the time|operational use", "specialist software|personal data|data protection", "Develop the time|utilisation, as specified"],
 "27": ["escalated to the project board|very-high|likelihood", "discuss with the Head|being effective|additional responses", "Decide whether|sufficient features|resource utilization"],
 "30": ["Advise on how|alternative solutions|system performance", "Approve the procedure|before any changes|change authority for approval", "Review whether|escalated correctly|report on this"],
 "33": ["minimum viable|part of timebox 1", "record the following|date, time spent|expected completion", "must-have features|additional defects|continue to use"],
}
def bars(a, y0, y1):
    col = a[y0:y1, 1400, :].astype(int)
    peach = (col[:,0] > 235) & (col[:,1] > 210) & (col[:,1] < 250) & (col[:,2] > 195) & (col[:,2] < 240) & ((col[:,0] - col[:,2]) > 10)
    out, start = [], None
    for i in range(len(peach) + 1):
        d = peach[i] if i < len(peach) else False
        if d and start is None: start = i
        if not d and start is not None:
            if i - start >= 22: out.append((y0 + start, y0 + i))
            start = None
    return out
def work(item):
    q, t, src, name, box_top = item
    im = Image.open(os.path.join(S, f"frames_{src}", name)).convert("RGB"); a = np.asarray(im)
    y0, y1 = box_top + 190, 905
    res = []
    prev_bot = y0
    for (bt, bb) in bars(a, y0, y1):
        letter_img = im.crop((1440, bt + 2, 1500, bb - 2)).convert("L").resize((240, (bb - bt - 4) * 4), Image.LANCZOS)
        L = pytesseract.image_to_string(letter_img, config="--psm 10 -c tessedit_char_whitelist=ABCDE").strip()[:1]
        txt = ""
        if bt - prev_bot > 18:
            c = im.crop((1140, prev_bot + 2, 1830, bt - 2)); c = c.resize((c.width*2, c.height*2), Image.LANCZOS)
            txt = " ".join(pytesseract.image_to_string(c, config="--psm 6").split())
        idx = None
        for i, pat in enumerate(ANCH[q]):
            if re.search(pat, txt): idx = i; break
        res.append({"q": q, "t": t, "frame": f"{src}:{name}", "bar": (bt, bb), "letter": L, "stmt": idx, "text": txt[:80]})
        prev_bot = bb
    return res
if __name__ == "__main__":
    ms = json.load(open(sys.argv[1])); final = json.load(open(sys.argv[2]))
    items = []
    for q, states in ms.items():
        for st in states:
            src, name = st["frame"].split(":")
            items.append((q, st["t"], src, name, 300))
    # box_top per frame from tags
    import csv
    bt = {}
    for r in csv.DictReader(open(os.path.join(S, "tags_all.csv"))):
        if r["box_top"]: bt[f'{r["src"]}:{r["frame"]}'] = int(r["box_top"])
    items = [(q, t, src, name, bt.get(f"{src}:{name}", 300)) for q, t, src, name, _ in items]
    with Pool(4) as p: res = p.map(work, items, chunksize=4)
    flat = [x for r in res for x in r]
    json.dump(flat, open(sys.argv[3], "w"), indent=0)
    # summarize per statement
    for q in sorted(ANCH, key=int):
        print(f"\n=== Q{q} ===")
        for i in range(3):
            obs = [(x["t"], x["letter"]) for x in flat if x["q"] == q and x["stmt"] == i and x["letter"]]
            obs.sort()
            seq = []
            for t, L in obs:
                if not seq or seq[-1][1] != L: seq.append((t, L))
            print(f"  S{i+1}: " + (" -> ".join(f"{L}@{t}" for t, L in seq) if seq else "never seen"))
        unk = [(x["t"], x["letter"], x["text"][:40]) for x in flat if x["q"] == q and x["stmt"] is None and x["letter"]]
        print(f"  unmatched bars: {len(unk)} e.g. {unk[-3:]}")
