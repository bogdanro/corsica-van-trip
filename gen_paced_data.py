# -*- coding: utf-8 -*-
"""Emit assets/js/data-paced.js — the unrushed variant."""
import json, math, io, sys
sys.setrecursionlimit(20000)

def rdp(pts, eps=0.00025):
    if len(pts) < 3: return pts
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
from pacing import STOP, access
from eats import PLACES as EAT

plan   = json.load(open("data/paced_plan.json"))
routes = {r["day"]: r for r in json.load(open("data/paced_routes.json"))}
src    = json.loads(open("assets/js/data.js").read().split("window.TRIP = ",1)[1].rsplit(";",1)[0])
poi    = {p["id"]: p for p in src["pois"]}
camps  = {c["id"]: c for c in src["camps"]}
photos_by_poi = {}
for d in src["days"]:
    for ph in d["photos"]:
        photos_by_poi.setdefault(ph["poi"], []).append(ph)

def km(a,b):
    dy=(a[0]-b[0])*111.0
    dx=(a[1]-b[1])*111.0*math.cos(math.radians((a[0]+b[0])/2))
    return math.hypot(dx,dy)

# --- day headline: theme + intro, hand-written where the day has a character
TITLE = {
 ("bastia","erbalunga"):        ("Ashore, and up the Cap", "Arrival & the old port",
   "The ferry docks mid-morning. Nothing today is far: Bastia on foot, then the coast road north as the light comes round."),
 ("douaniers","barcaggio","mattei"): ("The tip of Cap Corse", "A coastal walk and the northernmost sand",
   "The customs path early while it is cool, cows on the beach at Barcaggio, and both coasts at once from the Moulin Mattei."),
 ("centuri","nonza","stflorent"): ("Down the west side of the Cap", "Lobster port, black beach, citadel",
   "Three good stops and no hurry between them. Nonza's black shingle is the one you will remember."),
 ("vezzu","saleccia"):          ("The Agriates by boat", "A desert, and the best beach in the north",
   "The boat sets the shape of the day, which is the point: you cannot rush a beach you can only reach by sea."),
 ("ilerousse",):                ("L'Île-Rousse", "Market morning, then nothing",
   "A deliberately small day. The covered market before eleven, the causeway to the lighthouse, and an afternoon doing very little."),
 ("pigna","calvi"):             ("Balagne village to Calvi citadel", "Craft village, then the Genoese town",
   "Pigna's workshops in the morning, Calvi's ramparts in the afternoon, dinner on the marina."),
 ("figarella",):                ("The Figarella pools", "River, pines and cold water",
   "One walk, five kilometres, with granite plunge pools the whole way. Take lunch and stay in the water."),
 ("senino",):                   ("Monte Senino", "Four hours up, two gulfs at the top",
   "A single steep climb and the finest coastal view on the island. Nothing else is asked of you today."),
 ("scandola",):                 ("Scandola by boat", "Red cliffs, sea caves, ospreys",
   "A half-day on the water into the reserve, usually with a stop at Girolata. The afternoon is yours."),
 ("porto","pianella"):          ("Porto and the Spelunca", "A Genoese tower and a green river",
   "Climb the tower, then up the gorge road to the Pianella bridge and a swim under the arch."),
 ("calanches","caporosso"):     ("Calanches and Capo Rosso", "Red granite, all day",
   "In the Calanches by eight before the coaches. Capo Rosso from late morning — 8.5 km, no shade, and a tower on a cliff at the end."),
 ("arone",):                    ("Plage d'Arone", "The day off",
   "Sand at the end of a dead-end road. Swim, eat at the beach bar, sleep. You have earned it and you will need it."),
 ("vergio","nino"):             ("Col de Vergio and Lac de Nino", "The highest pass, and the pozzines",
   "Over the top into the Niolu, then five hours to a high lake ringed by green turf and half-wild horses."),
 ("calacuccia",):               ("Lac de Calacuccia", "A reservoir under Monte Cinto",
   "A short day at 800 m. Swim off the shore by the bridge, eat in the village, feel the temperature drop after dark."),
 ("aruda","scala","asco"):      ("A Ruda, the Scala and the Asco", "Three gorges in a day",
   "Granite chutes below the lake, the bare red Scala di Santa Regina, then the dead-end Asco valley."),
 ("corte","restonica"):         ("Corte and the lower Restonica", "The old capital",
   "The citadel and the museum in the morning, the gorge pools in the afternoon. Book the Melo shuttle tonight."),
 ("melo",):                     ("Lac de Melo", "The big one — and only this",
   "Eight hours, and the reason this day carries nothing else. Shuttle up, the broken road, the chains, the lake."),
 ("vizzavona","spusata"):       ("Vizzavona and the Bridal Veil", "Recovery, in the forest",
   "Deliberately gentle after Melo. Beech and laricio pines at 900 m, waterfalls, and cool air all day."),
 ("tolla","ajaccio"):           ("Lac de Tolla to Ajaccio", "Mountain lake, then the capital",
   "Swim in the Prunelli gorges, then down into Ajaccio in time to walk the old town before dinner."),
 ("sanguinaires","filitosa"):   ("Sanguinaires, then south", "Red islands and older stones",
   "The Parata headland in the morning light rather than fighting for sunset, then south to the menhirs of Filitosa."),
 ("sartene","bonifacio"):       ("Sartène to Bonifacio", "Granite town, limestone cliffs",
   "The most Corsican of towns at midday, then the cliffs at dusk once the day boats have gone."),
 ("lavezzi",):                  ("Îles Lavezzi", "A boat, and nothing else",
   "Granite boulders in impossibly clear water. Take everything with you; there is nothing on the islands."),
 ("santagiulia",):              ("Plage de Santa Giulia", "Shallow, translucent, horizontal",
   "One beach, all day. Go early for the water before the wind gets up."),
 ("piscia",):                   ("Up to the Alta Rocca", "A waterfall and a long climb inland",
   "The transfer day of the south: up out of the heat through the Ospedale forest, with the Piscia di Gallu walk on the way."),
 ("bavella","aiguilles"):       ("Col de Bavella", "Seven needles",
   "At the col for first light. The Trou de la Bombe is the easy one; the Alpine loop on chains is the real thing."),
 ("ghisoni","aleria"):          ("The D69 and Aleria", "An empty road, then the Romans",
   "The mountain road nobody drives, then the Greek and Roman capital on its hill above the lagoon."),
}
def headline(ids):
    k = tuple(ids)
    if k in TITLE: return TITLE[k]
    names = " & ".join(poi[i]["n"].split("—")[0].split("&")[0].strip() for i in ids)
    return (names, "", poi[ids[0]]["t"][:150])

WHEN = [(0,"Morning"),(150,"Late morning"),(260,"Midday"),(330,"Afternoon"),
        (450,"Late afternoon"),(560,"Evening")]
def when(mins_in):
    lab = "Morning"
    for t,l in WHEN:
        if mins_in >= t: lab = l
    return lab

days, all_camps, seen_ph = [], {}, set()
for d in plan:
    r = routes[d["n"]]
    ids = d["ids"]
    title, theme, intro = headline(ids)
    load = r["min"] + sum(STOP[i]["m"] for i in ids) + 20*len(ids) + 75

    # running order, derived from the day's actual composition
    flow, cursor = [], 0
    if d["n"] == 1:
        flow.append(dict(w="≈08:00", fix=True,
                         t="Ferry docks in Bastia. Coffee on board before you join the queue for the ramp."))
        cursor = 60
    for i in ids:
        p, m = poi[i], STOP[i]["m"]
        note = STOP[i].get("note")
        txt = p["t"].split(". ")[0] + "."
        txt += f"  Allow about {m//60} h{'' if m%60==0 else str(m%60)}." if m >= 90 else f"  About {m} min."
        if note: txt += "  " + note[0].upper() + note[1:] + "."
        flow.append(dict(w=when(cursor), fix=False, t=txt))
        cursor += m + 20
        if cursor > 260 and not any(f["w"] == "Lunch" for f in flow):
            flow.append(dict(w="Lunch", fix=False, t="Wherever you have got to — see the eating notes below."))
            cursor += 60
    c = camps[d["camp"]]
    flow.append(dict(w="By 18:30", fix=True,
                     t=f"Into {c['n']} and check in — {r['min']} min of driving today, so this is comfortable. "
                       f"Receptions here shut around 19:30."))
    all_camps[c["id"]] = dict(c, d=d["n"])

    ph = []
    for i in ids:
        for x in photos_by_poi.get(i, []):
            if x["f"] in seen_ph: continue
            seen_ph.add(x["f"]); ph.append(x)
            if len(ph) >= 6: break
        if len(ph) >= 6: break

    # eating: verified places within 25 km of a stop or tonight's base
    pts = [access(poi,i) for i in ids] + [(c["lat"], c["lon"])]
    near = []
    for k,e in EAT.items():
        if e["lat"] is None: continue
        if min(km(pt,(e["lat"],e["lon"])) for pt in pts) <= 25:
            near.append(dict(id=k, n=e["n"], town=e["town"], v=e["v"], t=e["t"],
                             lat=e["lat"], lon=e["lon"]))
    near.sort(key=lambda e: {"vegan":0,"options":1,"ask":2,"shop":3}[e["v"]])

    days.append(dict(day=d["n"], title=title, theme=theme, intro=intro,
                     km=r["km"], min=r["min"], geometry=rdp(r["geometry"]),
                     base=c["n"].replace("Camping ",""), bed="18:30",
                     vid="", flow=flow, photos=ph,
                     eat=dict(places=near[:4],
                              note=None if near else
                              "Nothing verified within reach today — carry a picnic, bought the evening before."),
                     load=round(load/60,1)))

pois_out = []
for d in plan:
    for i in d["ids"]:
        p = dict(poi[i]); p["d"] = d["n"]; p["mins"] = STOP[i]["m"]; pois_out.append(p)
seen=set()
for k,e in EAT.items():
    if e["lat"] is None: continue
    for d in days:
        if any(x["id"]==k for x in d["eat"]["places"]) and k not in seen:
            seen.add(k)
            pois_out.append(dict(id="eat-"+k, n=e["n"], c="food", d=d["day"],
                                 lat=e["lat"], lon=e["lon"], t=e["t"]+"  ("+e["town"]+")",
                                 f=[], eatv=e["v"]))
            break

out = dict(pois=pois_out, camps=list(all_camps.values()), stays=[], days=days)
with io.open("assets/js/data-paced.js","w",encoding="utf-8") as f:
    f.write("// Generated by gen_paced_data.py — the unrushed variant.\n")
    f.write("window.TRIP = "); json.dump(out, f, ensure_ascii=False, separators=(",",":")); f.write(";\n")
import os
print(f"days {len(days)} · stops {len([p for p in pois_out if p['c']!='food'])} · "
      f"food pins {len([p for p in pois_out if p['c']=='food'])} · camps {len(all_camps)} · "
      f"photos {sum(len(d['photos']) for d in days)} · flow blocks {sum(len(d['flow']) for d in days)}")
print(f"km {sum(d['km'] for d in days):.0f} · drive {sum(d['min'] for d in days)/60:.1f} h · "
      f"mean load {sum(d['load'] for d in days)/len(days):.1f} h · worst {max(d['load'] for d in days)} h")
print(f"data-paced.js {os.path.getsize('assets/js/data-paced.js')/1024:.0f} KB")
