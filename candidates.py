# -*- coding: utf-8 -*-
"""Places the guides rate that our plan doesn't have at all."""
import json, re, unicodedata
texts = json.load(open("data/sources.json"))
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", s)

# candidate Corsican places, drawn from the search results and general knowledge
CAND = {
 "Revellata peninsula":"revellata", "Speloncato":"speloncato", "Corbara":"corbara",
 "Algajola":"algajola", "Lumio":"lumio", "Montemaggiore":"montemaggiore",
 "Désert des Agriates":"agriates", "Plage de Ghignu":"ghignu",
 "Erbalunga":"erbalunga", "Tour de Seneque":"seneque", "Pino":"pino",
 "Canari":"canari", "Sisco":"sisco", "Luri":"luri",
 "Gorges de l'Inzecca":"inzecca", "Boziu":"boziu", "Castagniccia":"castagniccia",
 "Cascade de Radule":"radule", "Lac de Creno":"creno", "Monte Cinto":"monte cinto",
 "Vizzavona":"vizzavona", "Cascade des Anglais":"cascade des anglais",
 "Gorges du Prunelli":"prunelli", "Bastelica":"bastelica",
 "Cargese":"cargese", "Sagone":"sagone", "Tiuccia":"tiuccia",
 "Golfe de Valinco":"valinco", "Propriano":"propriano", "Campomoro":"campomoro",
 "Tour de Campomoro":"campomoro", "Serra-di-Ferro":"serra di ferro",
 "Plage de Cupabia":"cupabia", "Plage de Chevanu":"chevanu",
 "Plage de San Giovanni":"san giovanni", "Baie de Figari":"figari",
 "Cala Rossa":"cala rossa", "Pinarellu":"pinarellu", "Fautea":"fautea",
 "Plage de Tamaricciu":"tamaricciu", "Cerbicale":"cerbicale",
 "Aiguilles de Bavella":"bavella", "Cascade Piscia di Gallu":"piscia",
 "Levie / Pianu di Levie":"levie", "Quenza":"quenza", "Aullene":"aullene",
 "Sartene":"sartene", "Pont de Spin'a Cavallu":"spin a cavallu",
 "Cauria menhirs / Palaggiu":"palaggiu", "Cucuruzzu":"cucuruzzu",
 "Bocca di Larone":"larone", "Col de Larone":"larone",
 "Solenzara river pools":"solenzara", "Ghisonaccia":"ghisonaccia",
 "Etang de Diane":"diane", "Etang d'Urbino":"urbino",
 "Erbajolo":"erbajolo", "Venaco":"venaco", "Vivario":"vivario",
 "Pont de Muricciolu":"muricciolu", "Albertacce":"albertacce",
 "Calasima":"calasima", "Casamaccioli":"casamaccioli",
 "Tour de la Parata":"parata", "Capitello":"capitello",
 "Plage de Verghia":"verghia", "Porticcio":"porticcio",
 "Plage du Loto":"loto", "Ile de Cavallo":"cavallo",
 "Genoese bridge Ota":"pont de zaglia", "Zaglia":"zaglia",
 "Foret de l'Ospedale":"ospedale", "Barrage de Tolla":"tolla",
 "Sant'Antonino":"sant antonino", "Pigna":"pigna",
 "Golfe de Girolata":"girolata", "Punta Palazzu":"palazzu",
 "Capu Rossu":"capu rossu", "Plage de Bussaglia":"bussaglia",
 "Plage de Gradelle":"gradelle", "Osani":"osani",
 "Marine de Davia":"davia", "Plage de Petra Muna":"petra muna",
}
src = json.loads(open("assets/js/data.js").read().split("window.TRIP = ",1)[1].rsplit(";",1)[0])
have = norm(" ".join(p["n"] for p in src["pois"]))
rows=[]
for label, key in CAND.items():
    hits = sum(1 for t in texts.values() if key in t)
    already = key in have
    rows.append((hits, already, label, key))
rows.sort(key=lambda r: -r[0])
print("Places rated by 4+ guides that our plan does NOT include:\n")
print(f"{'src':>5}  place")
n=0
for h,a,label,key in rows:
    if a or h < 4: continue
    print(f"{h:>3}/10  {label}")
    n+=1
print(f"\n({n} candidates)")
print("\nAlready in the plan, for reference — top corroborated:")
for h,a,label,key in rows[:12]:
    if a: print(f"{h:>3}/10  {label}  (have it)")
