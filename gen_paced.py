# -*- coding: utf-8 -*-
"""Generate the unrushed variant from the optimiser's day partition."""
import json, math, urllib.request, time, os, io

plan = json.load(open("data/paced_plan.json"))
src  = json.loads(open("assets/js/data.js").read().split("window.TRIP = ",1)[1].rsplit(";",1)[0])
poi  = {p["id"]: p for p in src["pois"]}
camps = src["camps"]; stays = src["stays"]
from pacing import STOP, access

def km(a,b):
    dy=(a[0]-b[0])*111.0
    dx=(a[1]-b[1])*111.0*math.cos(math.radians((a[0]+b[0])/2))
    return math.hypot(dx,dy)

# ---- pick tonight's base ----
# Straight-line distance lies in Corsica: Bonifatu and the Asco valley are 8 km
# apart with a mountain range and no road between them.  Shortlist by crow-fly,
# then ask OSRM for the real drive and take the shortest.
def drive_min(a, b):
    u=(f"https://router.project-osrm.org/route/v1/driving/"
       f"{a[1]},{a[0]};{b[1]},{b[0]}?overview=false")
    try:
        j=json.loads(urllib.request.urlopen(
            urllib.request.Request(u,headers={"User-Agent":"c/1.0"}),timeout=40).read())
        time.sleep(1.0)
        return round(j["routes"][0]["duration"]/60)
    except Exception:
        return 999

BASECACHE="data/paced_bases.json"
if os.path.exists(BASECACHE):
    chosen=json.load(open(BASECACHE))
else:
    chosen={}
    for d in plan:
        lp = access(poi, d["ids"][-1])
        nxt = plan[plan.index(d)+1] if plan.index(d)+1 < len(plan) else None
        np_ = access(poi, nxt["ids"][0]) if nxt else None
        shortlist=sorted(camps,key=lambda c: km(lp,(c["lat"],c["lon"])))[:6]
        scored=[]
        for c in shortlist:
            cp=(c["lat"],c["lon"])
            a=drive_min(lp,cp)                      # get to bed tonight
            b=drive_min(cp,np_) if np_ else 0        # and away in the morning
            scored.append((a+b, a, c["id"]))
        _, mins, cid = min(scored)
        chosen[str(d["n"])]={"id":cid,"min":mins}
        print(f"  day {d['n']:>2} -> {cid} ({mins} min drive)")
    json.dump(chosen,open(BASECACHE,"w"))

byid={c["id"]:c for c in camps}
for d in plan:
    c=byid[chosen[str(d["n"])]["id"]]
    d["camp"]=c["id"]; d["campname"]=c["n"]
    d["base"]=c["n"].replace("Camping ","").replace("Village de l'","")
    d["baselat"],d["baselon"]=c["lat"],c["lon"]
    d["basemin"]=chosen[str(d["n"])]["min"]
    d["basekm"]=round(km((poi[d["ids"][-1]]["lat"],poi[d["ids"][-1]]["lon"]),(c["lat"],c["lon"])),1)

FERRY = (42.69746, 9.44977)
print("\nday  base                              drive from last stop")
for d in plan: print(f"{d['n']:>3}  {d['base'][:32]:34s} {d['basemin']:>4} min")

# ---- route each day: last night's base -> the day's stops -> tonight's base ----
CACHE="data/paced_routes.json"
if os.path.exists(CACHE):
    routes=json.load(open(CACHE))
else:
    routes=[]
    prev=FERRY
    for d in plan:
        pts=[prev]+[access(poi,s) for s in d["ids"]]+[(d["baselat"],d["baselon"])]
        coords=";".join(f"{lo},{la}" for la,lo in pts)
        u=f"https://router.project-osrm.org/route/v1/driving/{coords}?overview=full&geometries=geojson"
        j=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"c/1.0"}),timeout=60).read())
        rt=j["routes"][0]
        routes.append({"day":d["n"],
                       "km":round(rt["distance"]/1000,1),
                       "min":round(rt["duration"]/60),
                       "geometry":[[round(c[1],5),round(c[0],5)] for c in rt["geometry"]["coordinates"]]})
        prev=(d["baselat"],d["baselon"])
        time.sleep(1.1)
    json.dump(routes,open(CACHE,"w"))
print(f"\nrouted {len(routes)} days, {sum(r['km'] for r in routes):.0f} km, "
      f"{sum(r['min'] for r in routes)/60:.1f} h")

# --- re-check every day against the REAL routed drive time ---
print(f"\n{'d':>3} {'drive':>6} {'do':>5} {'load':>6}  stops")
bad=[]
for d,r in zip(plan,routes):
    act=sum(STOP[s]["m"] for s in d["ids"])
    load=r["min"]+act+20*len(d["ids"])+75
    d["realload"]=load; d["realdrive"]=r["min"]
    flag=""
    if load>10*60: flag=" RUSHED"; bad.append(d["n"])
    elif load>9*60: flag=" full"
    biggest=max(STOP[s]["m"] for s in d["ids"])
    if biggest>=180 and r["min"]>135: flag+=" ← drive+big"; bad.append(d["n"])
    print(f"{d['n']:>3} {r['min']:>5}m {act:>4}m {load/60:>5.1f}h  {', '.join(d['ids'])[:44]}{flag}")
print(f"\nmean {sum(d['realload'] for d in plan)/len(plan)/60:.1f} h/day · "
      f"problem days: {sorted(set(bad)) or 'none'}")
json.dump(plan,open("data/paced_plan.json","w"),indent=1)
