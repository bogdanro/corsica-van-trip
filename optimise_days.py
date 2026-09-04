# -*- coding: utf-8 -*-
"""Re-pace the trip.

The route is a fixed geographic sequence, so choosing days is a matter of
cutting that sequence into consecutive chunks.  That is a 1-D partition
problem and can be solved exactly by dynamic programming, rather than by
eyeballing it.

Objective: fewest days such that no day exceeds the comfort budget, then
the most even spread.  Constraints:
  * a day must end where you can actually sleep (accommodation within 25 km)
  * a day carrying a big activity (>= 3 h) gets a reduced driving allowance,
    so you never get a long drive and a long hike stacked together
"""
import json, math, urllib.request, os, sys
from pacing import STOP

FAFF, MEALS = 20, 75
BIG         = 180             # an activity this long dominates the day
BIG_DRIVE   = 105             # max driving when the day has a big activity
NORM_DRIVE  = 210             # max driving on an ordinary day
SLEEP_KM    = 25

data = json.loads(open("assets/js/data.js").read().split("window.TRIP = ", 1)[1].rsplit(";", 1)[0])
poi  = {p["id"]: p for p in data["pois"]}
byday = {}
for p in data["pois"]:
    if p["c"] != "food": byday.setdefault(p["d"], []).append(p)

# ---- ordered sequence of stops we intend to do (core only) ----
SEQ = []
for d in sorted(byday):
    for p in byday[d]:
        s = STOP.get(p["id"])
        if s and s["pick"] == "core" and s["m"] > 0:
            SEQ.append(p["id"])
print(f"{len(SEQ)} core stops in route order")

# ---- driving time between consecutive stops, from OSRM ----
CACHE = "data/seq_legs.json"
if os.path.exists(CACHE):
    legs = json.load(open(CACHE))
else:
    legs = []
    for i in range(0, len(SEQ) - 1, 20):          # OSRM caps waypoints per call
        chunk = SEQ[i:i + 21]
        coords = ";".join(f'{poi[s]["lon"]},{poi[s]["lat"]}' for s in chunk)
        u = f"https://router.project-osrm.org/route/v1/driving/{coords}?overview=false"
        j = json.loads(urllib.request.urlopen(
            urllib.request.Request(u, headers={"User-Agent": "corsica/1.0"}), timeout=60).read())
        legs += [round(l["duration"] / 60) for l in j["routes"][0]["legs"]]
        import time; time.sleep(1.1)
    json.dump(legs, open(CACHE, "w"))
# Several stops are lakes, summits or beaches with no road at the coordinate,
# so OSRM snaps them to a distant road and returns a nonsense duration (the
# Melo trailhead came back as 149 min from a point 5 km away).  Cap each leg
# at what the straight-line distance can justify: 45 km/h with a 1.4x factor
# for Corsican roads, floor of 12 min.
def straight_km(a, b):
    import math
    pa, pb = poi[a], poi[b]
    dy = (pa["lat"] - pb["lat"]) * 111.0
    dx = (pa["lon"] - pb["lon"]) * 111.0 * math.cos(math.radians((pa["lat"] + pb["lat"]) / 2))
    return math.hypot(dx, dy)

capped = 0
for k in range(len(legs)):
    plaus = max(12, round(straight_km(SEQ[k], SEQ[k + 1]) * 1.4 / 45 * 60))
    if legs[k] > plaus * 1.8:
        capped += 1
        legs[k] = plaus
print(f"{len(legs)} legs, {capped} implausible ones capped, "
      f"total driving {sum(legs)//60} h {sum(legs)%60} min")

# ---- where can you sleep? ----
sleeps = [(c["lat"], c["lon"]) for c in data["camps"]] + [(s["lat"], s["lon"]) for s in data["stays"]]
def km(a, b):
    dy = (a[0] - b[0]) * 111.0
    dx = (a[1] - b[1]) * 111.0 * math.cos(math.radians((a[0] + b[0]) / 2))
    return math.hypot(dx, dy)
def can_sleep(i):
    p = poi[SEQ[i]]
    return min(km((p["lat"], p["lon"]), s) for s in sleeps) <= SLEEP_KM

N = len(SEQ)

# ---- cost of doing stops i..j as one day ----
#
# A transfer between two stops is split across the two days that share it:
# you drive part of the way to a base in the evening and finish it next
# morning.  That is what basing actually looks like, and it stops the model
# charging a whole transfer to a day that is already a full mountain hike.
#
# A day is judged on two numbers:
#   total  everything, including the main activity
#   rest   everything EXCEPT the single biggest activity
# `rest` is what stops things being stacked: a day may be long because one
# great thing is long, never because we crammed three things together.
def make_cost(budget):
    """Return a day-cost function for a given daily budget (minutes).

    Two rules do the real work, and they are the difference between a plan
    that reads well and one you can actually follow:

      * total drive + doing + faff must fit the budget
      * at most ONE big activity (>= 3 h) per day, and on such a day the
        driving is capped hard.  This is what stops a 3-hour drive and a
        4-hour hike landing on the same date.
    """
    def cost(i, j):
        act   = sum(STOP[SEQ[k]]["m"] for k in range(i, j + 1))
        faff  = FAFF * (j - i + 1)
        drive = sum(legs[k] for k in range(i, j))
        if i > 0:     drive += legs[i - 1] / 2     # finish yesterday's transfer
        if j < N - 1: drive += legs[j] / 2         # start tomorrow's
        drive = int(drive)
        bigs    = [STOP[SEQ[k]]["m"] for k in range(i, j + 1) if STOP[SEQ[k]]["m"] >= BIG]
        biggest = max([STOP[SEQ[k]]["m"] for k in range(i, j + 1)] or [0])
        if len(bigs) > 1:                       return None, None   # no stacking
        if drive > (BIG_DRIVE if bigs else NORM_DRIVE): return None, None
        total = act + faff + drive
        # one dominant activity may push a day past budget; nothing else may
        allow = max(budget, biggest + 90) if bigs else budget
        if total > allow:                       return None, total
        return total, total
    return cost

# ---- DP: fewest days for a given budget, then the most even spread ----
def solve(budget):
    day_cost = make_cost(budget)
    INF = float("inf")
    best = [(INF, INF, -1)] * (N + 1)
    best[0] = (0, 0, -1)
    for j in range(N):
        for i in range(j + 1):
            if best[i][0] == INF: continue
            if j < N - 1 and not can_sleep(j): continue
            ok, total = day_cost(i, j)
            if ok is None: continue
            cand = (best[i][0] + 1, max(best[i][1], total), i)
            if cand[:2] < best[j + 1][:2]:
                best[j + 1] = cand
    if best[N][0] == INF: return None
    cuts, j = [], N
    while j > 0:
        i = best[j][2]; cuts.append((i, j - 1)); j = i
    cuts.reverse()
    return cuts, best[N][1], day_cost

PACES = [("Relaxed", 7.0), ("Steady", 8.0), ("Standard", 9.0), ("Brisk", 10.5)]
print(f"\n{'pace':10s} {'budget':>7} {'days':>5} {'+ferry/buffer':>14} {'worst day':>10}")
results = {}
for name, hrs in PACES:
    r = solve(int(hrs * 60))
    if not r:
        print(f"{name:10s} {hrs:>6.1f}h    infeasible"); continue
    cuts, worst, _ = r
    results[name] = cuts
    print(f"{name:10s} {hrs:>6.1f}h {len(cuts):>5} {len(cuts)+2:>14} {worst/60:>9.1f}h")

NAME = sys.argv[1] if len(sys.argv) > 1 else "Steady"
cuts, worst, day_cost = solve(int(dict(PACES)[NAME] * 60))
print(f"\n--- {NAME} pace, {len(cuts)} days on the road ---")
print(f"{'d':>3}  {'stops':46s} {'drive':>6} {'do':>6} {'load':>6}")
for n, (i, j) in enumerate(cuts, 1):
    act = sum(STOP[SEQ[k]]["m"] for k in range(i, j + 1))
    drive = sum(legs[k] for k in range(i, j))
    if i > 0:     drive += legs[i - 1] / 2
    if j < N - 1: drive += legs[j] / 2
    drive = int(drive)
    tot = act + drive + FAFF * (j - i + 1)
    names = ", ".join(poi[SEQ[k]]["n"].split("—")[0].split("&")[0].strip()[:16] for k in range(i, j + 1))
    print(f"{n:>3}  {names[:46]:46s} {drive:>5}m {act:>5}m {(tot+MEALS)/60:>5.1f}h")
json.dump({"seq": SEQ, "legs": legs,
           "paces": {k: v for k, v in results.items()}}, open("data/optimised.json", "w"))
