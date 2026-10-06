#!/usr/bin/env python3
"""timeline.py TAGS_ALL.csv OUT.json [--visits]
Frames of type scrolled/match_scrolled/exam/unknown with no q inherit the previous q (same page, scrolled).
Final selection (std): last frame of the final visit with nrows==4; else last non-empty sel in the final visit (flag '?').
Match questions: distinct right-pane states across all visits (chronological) for manual reading.
"""
import sys, csv, json
args = [a for a in sys.argv[1:] if not a.startswith("--")]
rows = list(csv.DictReader(open(args[0])))
EXAM = {"std", "match", "unknown", "scrolled", "match_scrolled", "exam"}
last_q = ""
for r in rows:
    r["t"] = int(r["t"]); r["nrows"] = int(r["nrows"] or 0)
    if r["type"] in EXAM and not r["q"]: r["q"] = last_q; r["inherited"] = True
    else: r["inherited"] = False
    if r["q"]: last_q = r["q"]
visits, cur = [], None
for r in rows:
    if not r["q"]: continue
    q = int(r["q"])
    if cur and cur["q"] == q: cur["rows"].append(r)
    else:
        if cur: visits.append(cur)
        cur = {"q": q, "rows": [r]}
if cur: visits.append(cur)
def hd(a, b):
    return bin(int(a, 16) ^ int(b, 16)).count("1") if a and b else 99
info = {}
for v in visits:
    q = v["q"]; rs = v["rows"]
    d = info.setdefault(q, {"q": q, "type": "std", "visits": 0, "first_t": rs[0]["t"], "match_states": []})
    d["visits"] += 1; d["last_t"] = rs[-1]["t"]
    if any(r["type"] in ("match", "match_scrolled") for r in rs): d["type"] = "match"
    # std final selection from this visit (overwritten by later visits)
    full = [r for r in rs if r["nrows"] == 4]
    if full:
        d["final_sel"] = full[-1]["sel"]; d["sel_frame"] = f'{full[-1]["src"]}:{full[-1]["frame"]}'; d["sel_flag"] = ""
    else:
        ne = [r for r in rs if r["sel"]]
        if ne: d["final_sel"] = ne[-1]["sel"]; d["sel_frame"] = f'{ne[-1]["src"]}:{ne[-1]["frame"]}'; d["sel_flag"] = "?"
        elif "final_sel" not in d: d["final_sel"] = ""; d["sel_frame"] = ""; d["sel_flag"] = "?"
    boxed = [r for r in rs if r["box_top"]]
    if boxed: d["view_frame"] = f'{boxed[-1]["src"]}:{boxed[-1]["frame"]}'; d["box_top"] = int(boxed[-1]["box_top"]); d["rows"] = boxed[-1]["rows"]
    # match pane states (dedupe consecutive by right_hash)
    for r in rs:
        if r["type"] == "match" and r["right_hash"]:
            st = d["match_states"]
            if st and hd(st[-1]["right_hash"], r["right_hash"]) <= 4 and hd(st[-1]["left_hash"], r["left_hash"]) <= 4:
                st[-1].update(t=r["t"], frame=f'{r["src"]}:{r["frame"]}'); st[-1]["n"] += 1
            else:
                st.append({"t": r["t"], "frame": f'{r["src"]}:{r["frame"]}', "right_hash": r["right_hash"], "left_hash": r["left_hash"], "n": 1, "box_top": int(r["box_top"] or 0)})
json.dump(info, open(args[1], "w"), indent=1)
if "--visits" in sys.argv:
    for v in visits:
        rs = v["rows"]; sels = "".join(sorted({r["sel"] for r in rs if r["sel"]}))
        print(f'{v["q"]:>3} {rs[0]["t"]:5d}-{rs[-1]["t"]:<5d} {rs[0]["src"]}:{rs[0]["frame"]}..{rs[-1]["frame"]} n={len(rs):3d} sels={sels} inh={sum(r["inherited"] for r in rs)}')
print("q,type,final_sel,flag,visits,first_t,last_t,sel_frame,view_frame,match_states")
for q in sorted(info):
    d = info[q]
    print(f'{q},{d["type"]},{d.get("final_sel","")},{d.get("sel_flag","")},{d["visits"]},{d["first_t"]},{d["last_t"]},{d.get("sel_frame","")},{d.get("view_frame","")},{len(d["match_states"])}')
