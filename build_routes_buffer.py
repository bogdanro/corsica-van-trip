"""Re-route the days that changed when adding check-in discipline + a buffer day."""
import urllib.request, json, time, math, sys
sys.setrecursionlimit(20000)

def rdp(pts, eps):
    if len(pts)<3: return pts
    def d(p,a,b):
        (y1,x1),(y2,x2),(y0,x0)=a,b,p
        dx,dy=x2-x1,y2-y1
        if dx==0 and dy==0: return math.hypot(x0-x1,y0-y1)
        t=max(0,min(1,((x0-x1)*dx+(y0-y1)*dy)/(dx*dx+dy*dy)))
        return math.hypot(x0-(x1+t*dx), y0-(y1+t*dy))
    dmax,idx=0,0
    for i in range(1,len(pts)-1):
        dd=d(pts[i],pts[0],pts[-1])
        if dd>dmax: dmax,idx=dd,i
    if dmax>eps: return rdp(pts[:idx+1],eps)[:-1]+rdp(pts[idx:],eps)
    return [pts[0],pts[-1]]

def route(pts):
    coords=";".join(f"{lo},{la}" for la,lo in pts)
    url=f"https://router.project-osrm.org/route/v1/driving/{coords}?overview=full&geometries=geojson"
    r=urllib.request.Request(url, headers={"User-Agent":"corsica-planner/1.0"})
    j=json.loads(urllib.request.urlopen(r,timeout=60).read())
    rt=j["routes"][0]
    g=[[round(c[1],5),round(c[0],5)] for c in rt["geometry"]["coordinates"]]
    time.sleep(1.2)
    return {"km":round(rt["distance"]/1000,1),"min":round(rt["duration"]/60),
            "geometry":rdp(g,0.00025)}

BASTIA=(42.69746,9.44977); SANDAMIANO=(42.62938,9.46835); CORTE=(42.30529,9.15119)

# ---- VAN version ----
van = json.load(open("data/routes_simplified.json"))
V = {d["day"]: d for d in van}
# D10: don't move after an 8-hour hike — sleep in Corte a second night
V[10].update(route([CORTE,(42.24828,9.05657),CORTE]),
             title="Restonica: Lac de Melo & Capitello")
# D11: pick Vizzavona up on the way south instead
V[11].update(route([CORTE,(42.12858,9.13376),(42.064,9.05138),(41.96817,8.97132),
                    (41.9264,8.7376),(41.87801,8.59343),(41.9264,8.7376)]),
             title="Vizzavona, Tolla & Ajaccio sunset")
# D15: end near Bastia, not at the ferry gate
V[15].update(route([(41.75585,9.17229),(41.85628,9.39857),(42.10356,9.21228),
                    (42.11357,9.51447),SANDAMIANO]),
             title="Ghisoni, Aleria & down to the coast")
V[16]=dict(day=16, title="Buffer day — Castagniccia, then the ferry",
           **route([SANDAMIANO,(42.37439,9.36813),BASTIA]))
json.dump([V[k] for k in sorted(V)], open("data/routes_simplified.json","w"))
print("VAN")
for k in sorted(V): print(f"  D{k:<2} {V[k]['title'][:44]:46s} {V[k]['km']:6.1f} km {V[k]['min']:4d} min")
print("  total", round(sum(V[k]["km"] for k in V),1),"km |", round(sum(V[k]["min"] for k in V)/60,1),"h")

# ---- HOTEL version ----
hot = json.load(open("data/routes_hotels.json"))
H = {d["day"]: d for d in hot}
H[15].update(route([CORTE,(42.3581,9.05915),(42.32758,9.0145),(42.32782,8.98419),BASTIA]),
             title="The Niolu, then down to Bastia")
H[16]=dict(day=16, title="Buffer day — Cap Corse, then the ferry",
           **route([BASTIA,(42.7736,9.47699),(42.811,9.48852),BASTIA]))
json.dump([H[k] for k in sorted(H)], open("data/routes_hotels.json","w"))
print("HOTEL")
for k in (15,16): print(f"  D{k:<2} {H[k]['title'][:44]:46s} {H[k]['km']:6.1f} km {H[k]['min']:4d} min")
print("  total", round(sum(H[k]["km"] for k in H),1),"km |", round(sum(H[k]["min"] for k in H)/60,1),"h")
