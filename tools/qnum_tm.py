"""Digit template matching for the WEB ATES question-number box.
build(frames_dir, {frame: number}) -> templates.npz ; recognize(crop_gray_np) -> int|None
"""
import numpy as np, os, sys
from PIL import Image
TW, TH = 16, 24

def segments(crop):
    """crop: HxW uint8 grayscale of the number region (white digits on dark). Returns list of binary digit images."""
    b = crop > 128
    cols = b.any(axis=0)
    segs, start = [], None
    for i in range(len(cols) + 1):
        c = cols[i] if i < len(cols) else False
        if c and start is None: start = i
        if not c and start is not None:
            if i - start >= 4: segs.append((start, i))
            start = None
    out = []
    for s, e in segs:
        sub = b[:, s:e]
        rws = sub.any(axis=1)
        ys = np.where(rws)[0]
        if len(ys) == 0: continue
        sub = sub[ys[0]:ys[-1]+1, :]
        if sub.shape[0] < 12: continue  # noise
        im = Image.fromarray((sub * 255).astype(np.uint8)).resize((TW, TH), Image.LANCZOS)
        out.append((np.asarray(im).astype(np.float32) / 255.0, e - s, sub.shape[0]))
    return out

def crop_from_frame(im, box_top, box_bot):
    top = max(box_top + 6, box_bot - 69)
    return np.asarray(im.crop((372, top, 439, box_bot - 5)).convert("L"))

def build(frames_dir, truth, out):
    from tag_frames import find_box
    acc = {}
    for f, num in truth.items():
        im = Image.open(os.path.join(frames_dir, f)).convert("RGB")
        box = find_box(np.asarray(im))
        segs = segments(crop_from_frame(im, *box))
        digits = str(num)
        if len(segs) != len(digits):
            print("skip", f, num, "segments:", len(segs)); continue
        for (t, w, h), d in zip(segs, digits):
            acc.setdefault(d, []).append(t)
    keys = sorted(acc)
    np.savez(out, keys=np.array(keys), **{f"t{k}": np.mean(acc[k], axis=0) for k in keys})
    print("templates built for digits:", keys, {k: len(acc[k]) for k in keys})

class Recognizer:
    def __init__(self, path):
        z = np.load(path)
        self.keys = [str(k) for k in z["keys"]]
        self.T = {k: z[f"t{k}"] for k in self.keys}
    def match(self, t):
        best, bd = None, 1e9
        for k, T in self.T.items():
            d = float(((t - T) ** 2).mean())
            if d < bd: best, bd = k, d
        return best, bd
    def recognize(self, crop):
        segs = segments(crop)
        if not segs or len(segs) > 2: return None, 9
        digits, worst = "", 0
        for t, w, h in segs:
            k, d = self.match(t); digits += k; worst = max(worst, d)
        v = int(digits)
        return (v if 1 <= v <= 56 else None), round(worst, 3)

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    truth = {"000010.jpg":49,"000040.jpg":50,"000250.jpg":51,"000300.jpg":52,"000500.jpg":53,"000600.jpg":54,"000680.jpg":55,"000750.jpg":56,
             "000900.jpg":2,"000950.jpg":3,"001000.jpg":4,"001060.jpg":7,"001083.jpg":8,"001100.jpg":14,"001160.jpg":15,"001180.jpg":17,
             "001350.jpg":20,"001420.jpg":24,"001455.jpg":26,"001500.jpg":27,"001620.jpg":30,"001700.jpg":33,"001840.jpg":36}
    build(sys.argv[1], truth, sys.argv[2])
