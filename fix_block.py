import json, sys
exec(open("optimiser_core.py").read())
from pacing import STOP

d = json.loads(open("assets/js/data.js").read().split("window.TRIP = ",1)[1].rsplit(";",1)[0])
poiById = {p["id"]: p for p in d["pois"]}
byday = {}
for p in d["pois"]:
    if p["c"] != "food": byday.setdefault(p["d"], []).append(p)

print("CURRENT days 9–12, core stops:")
blk = []
for day in (9, 10, 11, 12):
    dd = [x for x in d["days"] if x["day"] == day][0]
    cs = [p for p in byday[day] if STOP.get(p["id"], {}).get("pick") == "core" and STOP[p["id"]]["m"] > 0]
    opts = [p for p in byday[day] if STOP.get(p["id"], {}).get("pick") in ("option","alt")]
    act = sum(STOP[p["id"]]["m"] for p in cs)
    print(f"  D{day}  drive {dd['min']:>3}m  do {act:>4}m  = {(dd['min']+act+20*len(cs)+75)/60:.1f} h"
          f"   {', '.join(p['id'] for p in cs)}")
    if opts: print(f"        + options: {', '.join(p['id']+'('+str(STOP[p['id']]['m'])+'m)' for p in opts)}")
    blk += [p["id"] for p in cs]

# the block, plus the option we actually want to make room for
FULL = ["scala","asco","hautasco","corte","restonica","melo","vizzavona",
        "spusata","tolla","ajaccio","sanguinaires","filitosa","sartene","bonifacio"]
i0 = SEQ.index("scala")
full_seq, full_legs = SEQ[:], legs[:]
idx = [SEQ.index(s) for s in FULL if s in SEQ]
missing = [s for s in FULL if s not in SEQ]
print(f"\n(not in the core sequence, adding back: {missing})")

# rebuild a contiguous sub-problem, summing legs across anything skipped
keep = sorted(set(idx))
SEQ[:] = [full_seq[k] for k in keep]
for s in missing:                       # slot options back in at the right place
    pos = FULL.index(s)
    ref = FULL[pos-1]
    SEQ.insert(SEQ.index(ref)+1, s)
newlegs = []
for a, b in zip(SEQ, SEQ[1:]):
    ia, ib = full_seq.index(a) if a in full_seq else None, full_seq.index(b) if b in full_seq else None
    if ia is not None and ib is not None and ib > ia:
        newlegs.append(sum(full_legs[ia:ib]))
    else:
        newlegs.append(30)              # option slotted next to its neighbour
legs[:] = newlegs
globals()["N"] = len(SEQ)
globals()["ALLOW_STACK"] = False
globals()["BIG_DRIVE"], globals()["NORM_DRIVE"] = 105, 210

print(f"\nRe-solving this stretch ({len(SEQ)} stops, {sum(legs)} min driving):")
for name, hrs in [("Relaxed",7.0),("Steady",8.0),("Standard",9.0)]:
    r = solve(int(hrs*60))
    if not r: print(f"  {name}: infeasible"); continue
    cuts, worst, _ = r
    print(f"\n  --- {name} ({hrs}h budget): {len(cuts)} days, worst {worst/60:.1f}h ---")
    for n,(i,j) in enumerate(cuts,1):
        act = sum(STOP[SEQ[k]]["m"] for k in range(i,j+1))
        drv = sum(legs[k] for k in range(i,j))
        if i>0: drv += legs[i-1]/2
        if j<N-1: drv += legs[j]/2
        drv=int(drv); tot=act+drv+20*(j-i+1)+75
        print(f"     {n}. {', '.join(SEQ[i:j+1]):46s} drive {drv:>3}m  do {act:>4}m  {tot/60:.1f}h")
