# -*- coding: utf-8 -*-
"""The unrushed variant: re-solve the whole route at a steady pace."""
import json, sys, math
exec(open("optimiser_core.py").read())
from pacing import STOP

# padding I added on top of the film's trip, cut to pay for the extra days
CUT = {"ostriconi","bodri","santantonino","galeria","evisa","portovecchio",
       "ospedale","solenzara","piana","lotu","rondinara","palombaggia"}

full_seq, full_legs = SEQ[:], legs[:]
keep = [k for k,s in enumerate(SEQ) if s not in CUT]
SEQ[:] = [full_seq[k] for k in keep]
legs[:] = [sum(full_legs[a:b]) for a,b in zip(keep, keep[1:])]
globals()["N"] = len(SEQ)
globals()["ALLOW_STACK"] = False
globals()["BIG_DRIVE"], globals()["NORM_DRIVE"] = 105, 210

print(f"{len(full_seq)} core stops - {len(CUT)} cut = {len(SEQ)}")
print(f"driving {sum(legs)//60} h {sum(legs)%60} m\n")
for name,hrs in [("Relaxed",7.0),("Steady",8.0),("Standard",9.0)]:
    r = solve(int(hrs*60))
    print(f"  {name:9s} {hrs}h -> {len(r[0]) if r else '—'} days on the road, "
          f"worst {r[1]/60:.1f}h" if r else f"  {name}: infeasible")

cuts, worst, _ = solve(int(8.0*60))
print(f"\n=== STEADY: {len(cuts)} days on the road (+ferry arrival +buffer = {len(cuts)+1}) ===")
plan=[]
for n,(i,j) in enumerate(cuts,1):
    ids=[SEQ[k] for k in range(i,j+1)]
    act=sum(STOP[s]["m"] for s in ids)
    drv=sum(legs[k] for k in range(i,j))
    if i>0: drv+=legs[i-1]/2
    if j<N-1: drv+=legs[j]/2
    drv=int(drv); tot=act+drv+20*len(ids)+75
    plan.append(dict(n=n, ids=ids, act=act, drive=drv, load=tot))
    print(f"{n:>3}. {', '.join(ids):50s} {drv:>4}m {act:>4}m {tot/60:>5.1f}h")
json.dump(plan, open("data/paced_plan.json","w"), indent=1)
