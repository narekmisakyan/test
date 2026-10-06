#!/usr/bin/env python3
"""OCR the question stem and option rows of one exam frame.
Usage: python3 -I extract_q.py FRAME.jpg "ROWS" (rows string from tags csv, e.g. "570-619;641-691;713-763;830-880")
"""
import sys
from PIL import Image
import pytesseract
im = Image.open(sys.argv[1]).convert("RGB")
rows = [tuple(map(int, x.split("-"))) for x in sys.argv[2].split(";") if x] if len(sys.argv) > 2 and sys.argv[2] else []
box_top = int(sys.argv[3]) if len(sys.argv) > 3 else 298
def ocr(box, psm=6):
    c = im.crop(box); c = c.resize((c.width*2, c.height*2), Image.LANCZOS)
    return " ".join(pytesseract.image_to_string(c, config=f"--psm {psm}").split())
stem_bottom = (rows[0][0] - 45) if rows else 945
print("STEM:", ocr((495, box_top + 7, 1845, stem_bottom)))
for i, (top, bot) in enumerate(rows):
    nxt = rows[i+1][0] - 20 if i+1 < len(rows) else min(bot + 70, 945)
    print(f"{chr(65+i)}:", ocr((492, top - 4, 1845, nxt)))
