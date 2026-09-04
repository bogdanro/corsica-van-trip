# -*- coding: utf-8 -*-
"""Day load, counting only what the plan actually asks you to do."""
import json, sys
from pacing import STOP, COMFORT, LIMIT

FAFF, MEALS = 20, 75

def load(path, label, show=True):
    d = json.loads(open(path).read().split("window.TRIP = ", 1)[1].rsplit(";", 1)[0])
    pois = {}
    for p in d["pois"]:
        if p["c"] != "food": pois.setdefault(p["d"], []).append(p)
    rows = []
    for day in d["days"]:
        ps = pois.get(day["day"], [])
        core = [p for p in ps if STOP.get(p["id"], {}).get("pick") == "core"]
        opt  = [p for p in ps if STOP.get(p["id"], {}).get("pick") in ("option", "alt")]
        act  = sum(STOP.get(p["id"], {}).get("m", 0) for p in core)
        faff = sum(FAFF for p in core if STOP.get(p["id"], {}).get("m", 0) > 0)
        total = day["min"] + act + faff + MEALS
        longest = max([STOP.get(p["id"], {}).get("m", 0) for p in core] or [0])
        rows.append(dict(day=day["day"], title=day["title"], drive=day["min"],
                         act=act, total=total, core=len(core), opt=len(opt),
                         longest=longest,
                         clash=day["min"] >= 120 and longest >= 180))
    if show:
        print(f"\n{'='*96}\n{label}   (core stops only; options excluded)\n{'='*96}")
        print(f"{'d':>2}  {'title':38s} {'drive':>6}{'core':>7} {'TOTAL':>7}  {'opts':>4}  verdict")
        for r in rows:
            h = r["total"] / 60
            v = ("RUSHED" if r["total"] > LIMIT else
                 "full"   if r["total"] > COMFORT else
                 "good"   if r["total"] > 4.5 * 60 else "easy")
            flag = " ← drive+big hike" if r["clash"] else ""
            print(f"{r['day']:>2}  {r['title'][:38]:38s} {r['drive']:>5}m{r['act']:>6}m "
                  f"{h:>6.1f}h {r['opt']:>5}  {v}{flag}")
        tot = sum(r["total"] for r in rows) / 60
        bad = [r["day"] for r in rows if r["total"] > LIMIT]
        print(f"\n  {len(rows)} days · mean {tot/len(rows):.1f} h/day · "
              f"rushed days: {bad or 'none'}")
    return rows

if __name__ == "__main__":
    load("assets/js/data.js", "VAN — current 16-day plan")
    load("assets/js/data-hotels.js", "CAR + HOTELS — current 16-day plan")
