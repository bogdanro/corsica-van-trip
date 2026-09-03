import urllib.request, json, time, math, sys
sys.setrecursionlimit(20000)

# Hotel/car version: sleep in 8 bases, drive day-loops out and back.
DAYS = [
 (1,"Bastia & the near Cap",[(42.69746,9.44977),(42.7736,9.47699),(42.811,9.48852),(42.69746,9.44977)]),
 (2,"The whole Cap Corse loop",[(42.69746,9.44977),(42.95942,9.45479),(43.00611,9.40216),(42.97459,9.3648),(42.96058,9.36824),(42.78441,9.34459),(42.70074,9.36452),(42.69746,9.44977)]),
 (3,"Saint-Florent & the Agriates",[(42.69746,9.44977),(42.68129,9.3025),(42.66591,9.14144),(42.68129,9.3025),(42.69746,9.44977)]),
 (4,"Balagne: Ostriconi to Calvi",[(42.69746,9.44977),(42.66241,9.06103),(42.64316,9.01937),(42.63448,8.93814),(42.59899,8.90294),(42.5889,8.90499),(42.62999,8.91425),(42.56766,8.75887)]),
 (5,"Calvi, Calenzana & Bonifatu",[(42.56766,8.75887),(42.51046,8.85082),(42.44338,8.8529),(42.56766,8.75887)]),
 (6,"West coast: Galeria, Senino, Porto",[(42.56766,8.75887),(42.40848,8.64792),(42.31641,8.61077),(42.25633,8.7612),(42.26732,8.69633)]),
 (7,"Calanches, Capo Rosso & Arone",[(42.26732,8.69633),(42.241,8.65242),(42.23887,8.63706),(42.23525,8.58349),(42.20723,8.58014),(42.26732,8.69633)]),
 (8,"Down the west coast to Ajaccio",[(42.26732,8.69633),(42.13436,8.59422),(42.11613,8.69649),(41.9264,8.7376),(41.87801,8.59343),(41.9264,8.7376)]),
 (9,"Mountain day loop from Ajaccio",[(41.9264,8.7376),(41.96817,8.97132),(42.064,9.05138),(42.12858,9.13376),(41.9264,8.7376)]),
 (10,"South-west: Filitosa, Sartene, Bonifacio",[(41.9264,8.7376),(41.7444,8.87094),(41.6759,8.90404),(41.62088,8.97219),(41.49582,8.93471),(41.38723,9.15906)]),
 (11,"Bonifacio & the Lavezzi",[(41.38723,9.15906),(41.46885,9.26647),(41.38723,9.15906)]),
 (12,"White beaches & up to the Ospedale",[(41.38723,9.15906),(41.5275,9.27216),(41.5561,9.3218),(41.59114,9.27945),(41.66849,9.20744),(41.68696,9.26246),(41.74937,9.17064)]),
 (13,"Alta Rocca, Bavella & across to Corte",[(41.74937,9.17064),(41.71826,9.12867),(41.67908,9.14696),(41.79587,9.22496),(41.85628,9.39857),(42.11357,9.51447),(42.30529,9.15119)]),
 (14,"Restonica: Melo & Capitello",[(42.30529,9.15119),(42.24828,9.05657),(42.30529,9.15119)]),
 (15,"The Niolu, then the ferry",[(42.30529,9.15119),(42.3581,9.05915),(42.32758,9.0145),(42.32782,8.98419),(42.69746,9.44977)]),
]
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

out=[]
for num,title,pts in DAYS:
    coords=";".join(f"{lo},{la}" for la,lo in pts)
    url=f"https://router.project-osrm.org/route/v1/driving/{coords}?overview=full&geometries=geojson"
    try:
        r=urllib.request.Request(url, headers={"User-Agent":"corsica-planner/1.0"})
        j=json.loads(urllib.request.urlopen(r,timeout=60).read())
        rt=j["routes"][0]
        g=[[round(c[1],5),round(c[0],5)] for c in rt["geometry"]["coordinates"]]
        g=rdp(g,0.00025)
        out.append({"day":num,"title":title,"km":round(rt["distance"]/1000,1),
                    "min":round(rt["duration"]/60),"geometry":g})
        print(f"Day {num:2d} {title[:42]:44s} {rt['distance']/1000:6.1f} km {rt['duration']/60:5.0f} min  {len(g):>4} pts")
    except Exception as e:
        print("FAIL",num,str(e)[:60])
    time.sleep(1.2)
json.dump(out, open("data/routes_hotels.json","w"))
print("\ntotal", round(sum(d["km"] for d in out),1),"km |",
      round(sum(d["min"] for d in out)/60,1),"h moving")
