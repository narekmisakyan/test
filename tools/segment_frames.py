#!/usr/bin/env python3
"""Group sampled video frames into stable screen segments and OCR one frame per segment.

Usage: python3 -I segment_frames.py FRAMES_DIR OUT_DIR [--fps N] [--thresh T] [--no-ocr]

FRAMES_DIR holds frames named %06d.jpg sampled at N frames/second (default 1).
Consecutive frames whose perceptual hash differs by <= T bits are one segment.
For every segment the LAST frame is kept (final state of that screen) and OCR'd.
Writes OUT_DIR/segments.csv and OUT_DIR/ocr/<seg>.txt
"""
import csv, os, sys, argparse
from PIL import Image
import imagehash

ap = argparse.ArgumentParser()
ap.add_argument("frames_dir"); ap.add_argument("out_dir")
ap.add_argument("--fps", type=float, default=1.0)
ap.add_argument("--thresh", type=int, default=6)
ap.add_argument("--no-ocr", action="store_true")
a = ap.parse_args()

files = sorted(f for f in os.listdir(a.frames_dir) if f.lower().endswith(".jpg"))
os.makedirs(os.path.join(a.out_dir, "ocr"), exist_ok=True)
segs, cur = [], None
for i, f in enumerate(files):
    h = imagehash.phash(Image.open(os.path.join(a.frames_dir, f)), hash_size=16)
    if cur is None or (h - cur["hash"]) > a.thresh:
        if cur: segs.append(cur)
        cur = {"start": i, "end": i, "hash": h, "first": f, "last": f}
    else:
        cur["end"] = i; cur["last"] = f; cur["hash"] = h
if cur: segs.append(cur)

if not a.no_ocr:
    import pytesseract
with open(os.path.join(a.out_dir, "segments.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["seg", "t_start_s", "t_end_s", "frames", "last_frame", "ocr_file"])
    for n, s in enumerate(segs):
        ocr_path = ""
        if not a.no_ocr:
            txt = pytesseract.image_to_string(Image.open(os.path.join(a.frames_dir, s["last"])), config="--psm 4")
            ocr_path = os.path.join("ocr", f"{n:05d}.txt")
            open(os.path.join(a.out_dir, ocr_path), "w").write(txt)
        w.writerow([n, round(s["start"]/a.fps, 1), round(s["end"]/a.fps, 1), s["end"]-s["start"]+1, s["last"], ocr_path])
print(f"{len(files)} frames -> {len(segs)} segments")
