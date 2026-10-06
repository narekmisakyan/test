#!/usr/bin/env python3
"""Tag every frame of a PeopleCert WEB ATES exam recording (1920x1008).
Usage: python3 -I tag_frames.py FRAMES_DIR OUT_CSV
Columns: frame,q,type,nrows,sel,rows,box_top,content_hash,left_hash,right_hash,full_hash
type: std | match | unknown (question found, no rows) | pdf (scenario PDF tab) | other
"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ["OMP_THREAD_LIMIT"] = "1"
from multiprocessing import Pool
from PIL import Image, ImageOps
import numpy as np, pytesseract, imagehash
_qcache = {}

def find_timer(a):
    """Red countdown box at x=1710, y in 140..280, height 25..45. Returns (top, bottom) or None."""
    col = a[140:262, 1710, :].astype(int)
    red = (col[:,0] > 190) & (col[:,1] < 100) & (col[:,2] < 100)
    best, start = (0, 0, 0), None
    for i in range(len(red) + 1):
        d = red[i] if i < len(red) else False
        if d and start is None: start = i
        if not d and start is not None:
            if i - start > best[0]: best = (i - start, 140 + start, 140 + i)
            start = None
    return (best[1], best[2]) if 22 <= best[0] <= 50 else None

def find_box(a, y_from=230, y_to=470):
    """Locate the dark question-number box by scanning column x=380 in [y_from, y_to]. Returns (top, bottom) or None."""
    lum = a[y_from:y_to, 380, :].astype(int).sum(axis=1) // 3
    dark = lum < 80
    best, start = (0, 0, 0), None
    for i in range(len(dark) + 1):
        d = dark[i] if i < len(dark) else False
        if d and start is None: start = i
        if not d and start is not None:
            if i - start > best[0]: best = (i - start, y_from + start, y_from + i)
            start = None
    return (best[1], best[2]) if 40 <= best[0] <= 90 else None

from qnum_tm import Recognizer, crop_from_frame
_R = Recognizer(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates.npz"))

def qnum(im, box):
    crop = crop_from_frame(im, *box)
    v, d = _R.recognize(crop)
    if v is not None and d <= 0.08: return v
    inv = ImageOps.invert(Image.fromarray(crop)).resize((268, 256), Image.LANCZOS).point(lambda p: 255 if p > 128 else 0)
    inv = ImageOps.expand(inv, border=40, fill=255)
    for psm in (8, 13):
        t = pytesseract.image_to_string(inv, config=f"--psm {psm} -c tessedit_char_whitelist=0123456789").strip()
        if t.isdigit() and 1 <= int(t) <= 56: return int(t)
    return v

def cls(p):
    r, g, b = p
    if r > 200 and g < 90 and b < 90: return "RED"
    if abs(r-g) < 12 and abs(g-b) < 12 and 200 < r < 245: return "GREY"
    return "X"

def rows(a, y0):
    col = a[y0:1000, 437, :].astype(int)
    out, start, cur = [], 0, cls(col[0])
    for i in range(1, len(col)):
        c = cls(col[i])
        if c != cur:
            if i - start >= 20 and cur in ("RED", "GREY"): out.append((cur, y0+start, y0+i-1))
            cur, start = c, i
    if len(col) - start >= 20 and cur in ("RED", "GREY"): out.append((cur, y0+start, y0+len(col)-1))
    return out

def is_pdf(a):
    l = lambda x, y: int(a[y, x, :].astype(int).sum() // 3)
    toolbar = any(all(l(x, y) < 90 for x in (400, 960, 1200, 1500)) for y in (172, 224))
    sidebar = all(55 <= l(x, y) <= 80 for x in (60, 300, 420) for y in (600, 900))
    page = int(a[700, 600:1800, :].astype(int).sum(axis=1).mean() // 3) > 150
    return toolbar and sidebar and page

def tag(path):
    im = Image.open(path).convert("RGB"); a = np.asarray(im)
    name = os.path.basename(path)
    full = str(imagehash.phash(im, hash_size=8))
    timer = find_timer(a)
    if timer is None:
        typ = "pdf" if is_pdf(a) else "other"
        return [name, "", typ, 0, "", "", "", str(imagehash.phash(im.crop((484, 215, 1875, 1000)), hash_size=12)), "", "", full]
    box = find_box(a, timer[0] + 60, timer[0] + 260)
    q = qnum(im, box) if box else None
    if q is None:  # question page scrolled so the number box is hidden/clipped: still read the option rows
        y0 = timer[1] + 70
        rs = rows(a, y0)
        col2 = a[y0+40:y0+600, 400, :].astype(int)
        orange = int(((col2[:,0] > 230) & (col2[:,1] > 150) & (col2[:,1] < 200) & (col2[:,2] > 110) & (col2[:,2] < 170)).sum())
        typ = "match_scrolled" if orange > 100 else ("scrolled" if rs else "exam")
        sel = "".join(chr(65+i) for i, r in enumerate(rs) if r[0] == "RED") if typ == "scrolled" else ""
        return [name, "", typ, len(rs), sel, ";".join(f"{r[1]}-{r[2]}" for r in rs), "", str(imagehash.phash(im.crop((484, 230, 1875, 945)), hash_size=12)), "", "", full]
    y0 = box[1] + 5
    col2 = a[y0+100:y0+520, 400, :].astype(int)
    orange = int(((col2[:,0] > 230) & (col2[:,1] > 150) & (col2[:,1] < 200) & (col2[:,2] > 110) & (col2[:,2] < 170)).sum())
    rs = rows(a, y0)
    typ = "match" if orange > 100 else ("std" if rs else "unknown")
    sel = "".join(chr(65+i) for i, r in enumerate(rs) if r[0] == "RED") if typ == "std" else ""
    content = str(imagehash.phash(im.crop((484, box[0], 1875, 945)), hash_size=12))
    left = str(imagehash.phash(im.crop((375, y0+120, 1090, 895)), hash_size=8)) if typ == "match" else ""
    right = str(imagehash.phash(im.crop((1130, y0+120, 1845, 895)), hash_size=8)) if typ == "match" else ""
    return [name, q, typ, len(rs), sel, ";".join(f"{r[1]}-{r[2]}" for r in rs), box[0], content, left, right, full]

if __name__ == "__main__":
    d, out = sys.argv[1], sys.argv[2]
    files = sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".jpg"))
    if len(sys.argv) > 3:  # test mode: explicit frame list
        for f in sys.argv[3:]:
            a = np.asarray(Image.open(os.path.join(d, f)).convert("RGB")); tm = find_timer(a)
            print(tag(os.path.join(d, f)), "timer=", tm, "box=", find_box(a, tm[0]+60, tm[0]+260) if tm else None)
        sys.exit()
    with Pool(4) as p: res = p.map(tag, files, chunksize=8)
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["frame","q","type","nrows","sel","rows","box_top","content_hash","left_hash","right_hash","full_hash"]); w.writerows(res)
    print(f"tagged {len(res)} frames -> {out}")
