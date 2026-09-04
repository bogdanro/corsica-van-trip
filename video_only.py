import json, sys
exec(open("optimiser_core.py").read())
from pacing import STOP

d = json.loads(open("assets/js/data.js").read().split("window.TRIP = ",1)[1].rsplit(";",1)[0])
vid = {p["id"] for p in d["pois"] if p.get("vid")}

full_seq, full_legs = SEQ[:], legs[:]
keep = [k for k, s in enumerate(SEQ) if s in vid]
SEQ[:] = [full_seq[k] for k in keep]
# rebuild legs by summing the skipped hops
newlegs = []
for a, b in zip(keep, keep[1:]):
    newlegs.append(sum(full_legs[a:b]))
legs[:] = newlegs
globals()["N"] = len(SEQ)

act = sum(STOP[s]["m"] for s in SEQ)
print(f"\nThe film's own {len(SEQ)} core stops")
print(f"  activity {act/60:.0f} h + driving {sum(legs)/60:.0f} h + faff/meals ≈ "
      f"{(act+sum(legs)+20*len(SEQ))/60:.0f} h of trip")
print(f"\n  his pace, 10 days  -> {(act+sum(legs)+20*len(SEQ))/10/60:.1f} h/day  "
      f"(a filming road-tripper's day: early, long, always moving)")
import optimiser_core as _oc
def sweep(label, big_drive, norm_drive, stack_ok):
    globals()["BIG_DRIVE"] = big_drive
    globals()["NORM_DRIVE"] = norm_drive
    globals()["ALLOW_STACK"] = stack_ok
    print(f"\n{label}")
    print(f"  {'pace':10s} {'budget':>7} {'days':>6} {'+2':>5} {'worst':>7}")
    for name, hrs in [("Relaxed",7.0),("Steady",8.0),("Standard",9.0),
                      ("Brisk",10.5),("Film pace",12.5)]:
        r = solve(int(hrs*60))
        if not r: print(f"  {name:10s} {hrs:>6.1f}h   infeasible"); continue
        cuts, worst, _ = r
        print(f"  {name:10s} {hrs:>6.1f}h {len(cuts):>6} {len(cuts)+2:>5} {worst/60:>6.1f}h")

sweep("RULE OFF — stacking allowed, as the film actually does it", 300, 300, True)
sweep("RULE ON  — one big thing a day, driving capped when there is one", 105, 210, False)
