# -*- coding: utf-8 -*-
"""What actually fits in a normal holiday?  Pace x scope."""
import json, sys
sys.argv = ["x"]
exec(open("optimiser_core.py").read())

REGIONS = {
 "Whole island":      (0, len(SEQ) - 1),
 "North + west":      (0, SEQ.index("sanguinaires")),
 "North only":        (0, SEQ.index("vizzavona")),
 "South + centre":    (SEQ.index("corte"), len(SEQ) - 1),
}
print(f"\n{'scope':16s} {'stops':>6}", end="")
PACES = [("Relaxed", 7.0), ("Steady", 8.0), ("Standard", 9.0), ("Brisk", 10.5)]
for n, _ in PACES: print(f"{n:>10s}", end="")
print("      (days on the road; add 2 for ferry + buffer)")
for label, (a, bnd) in REGIONS.items():
    sub = SEQ[a:bnd + 1]
    print(f"{label:16s} {len(sub):>6}", end="")
    for _, hrs in PACES:
        saveS, saveL, saveN = SEQ[:], legs[:], N
        SEQ[:] = sub
        legs[:] = legs[a:bnd]
        globals()["N"] = len(SEQ)
        r = solve(int(hrs * 60))
        print(f"{(len(r[0]) if r else '—'):>10}", end="")
        SEQ[:] = saveS; legs[:] = saveL; globals()["N"] = saveN
    print()
