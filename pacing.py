# -*- coding: utf-8 -*-
"""Realistic time per stop, and whether it is the spine of the day or an extra.

`m`    minutes you actually spend there, doing it properly but not lingering
`pick` "core"   — the reason the day exists; the plan assumes you do it
       "option" — worth it if you have the time, the legs or the weather
       "alt"    — an alternative to a core stop, not an addition

Durations are the *doing* time. Parking, walking in and back is added
separately (20 min a stop), as are meals.
"""
S = lambda m, pick, note=None: dict(m=m, pick=pick, note=note)

STOP = {
# --- Cap Corse
"bastia":      S(150, "core"),
"erbalunga":   S(45,  "core"),
"sisco":       S(60,  "option", "only if it's hot and you're ahead"),
"macinaggio":  S(0,   "core",   "you sleep here"),
"douaniers":   S(210, "core",   "the short out-and-back is 90 min if you'd rather"),
"barcaggio":   S(120, "core"),
"mattei":      S(30,  "core"),
"centuri":     S(90,  "core"),
"nonza":       S(120, "core"),
"patrimonio":  S(75,  "option", "a tasting, not an obligation"),
# --- Agriates & Balagne
"stflorent":   S(120, "core"),
"vezzu":       S(20,  "core"),
"lotu":        S(240, "alt",    "the shorter boat; Saleccia is the better beach"),
"saleccia":    S(330, "core",   "boat out and back sets the day"),
"ostriconi":   S(150, "core"),
"lozari":      S(120, "option"),
"ilerousse":   S(150, "core"),
"pigna":       S(90,  "core"),
"santantonino":S(60,  "core"),
"bodri":       S(150, "core"),
# --- Calvi
"calvi":       S(180, "core"),
"calenzana":   S(45,  "option"),
"figarella":   S(210, "core",   "walk plus a swim"),
"bonifatu":    S(360, "alt",    "the big cirque hike instead of the river walk — not both"),
# --- West coast
"galeria":     S(90,  "core"),
"senino":      S(240, "core",   "4 h of steep, and the whole point of this stretch"),
"scandola":    S(240, "core",   "boat from Porto, usually with a Girolata stop"),
"girolata":    S(180, "alt",    "on foot from the Col de la Croix if you skip the boat"),
"porto":       S(90,  "core"),
"pianella":    S(120, "core",   "the bridge and a swim; the full gorge walk is 3.5 h"),
# --- Piana
"calanches":   S(120, "core"),
"piana":       S(60,  "core"),
"caporosso":   S(210, "core"),
"arone":       S(180, "core",   "this is the afternoon off"),
# --- Niolu
"ota":         S(30,  "option"),
"evisa":       S(60,  "core"),
"cristinacce": S(20,  "option"),
"vergio":      S(45,  "core"),
"nino":        S(300, "core",   "a real mountain day on its own"),
"calacuccia":  S(150, "core"),
"aruda":       S(120, "core"),
# --- Asco & Corte
"scala":       S(45,  "core"),
"asco":        S(90,  "core"),
"hautasco":    S(300, "option", "Punta Muvrella — a 5 h day, only if you want it"),
"corte":       S(180, "core"),
"restonica":   S(120, "core"),
"melo":        S(480, "core",   "eight hours; nothing else fits"),
"vizzavona":   S(120, "core"),
# --- Ajaccio side
"spusata":     S(75,  "core"),
"tolla":       S(150, "core"),
"ajaccio":     S(180, "core"),
"sanguinaires":S(120, "core"),
"d1d4":        S(150, "option", "a drive for its own sake"),
# --- South-west
"filitosa":    S(105, "core"),
"sartene":     S(105, "core"),
"stelucie":    S(75,  "option"),
"roccapina":   S(180, "option", "the track down is rough; many just look from the road"),
"bonifacio":   S(240, "core"),
# --- Far south
"lavezzi":     S(300, "core",   "a boat day"),
"rondinara":   S(180, "alt"),
"santagiulia": S(180, "core"),
"palombaggia": S(180, "alt",    "pick one white-sand beach a day, not three"),
"portovecchio":S(120, "core"),
# --- Alta Rocca & Bavella
"ospedale":    S(75,  "core"),
"piscia":      S(120, "core"),
"carbini":     S(45,  "option"),
"cucuruzzu":   S(105, "option"),
"bavella":     S(90,  "core"),
"aiguilles":   S(240, "core",   "Trou de la Bombe is 150 min; the Alpine loop 240"),
"zonza":       S(0,   "core",   "you sleep here"),
# --- East and home
"solenzara":   S(90,  "core"),
"ghisoni":     S(150, "core"),
"aleria":      S(105, "core"),
"campi":       S(30,  "option"),
"orezza":      S(120, "option"),
}

# how full a day should feel, in minutes of drive + doing + faff + meals
COMFORT = 8 * 60      # a good full day
LIMIT   = 10 * 60     # above this it is rushed

# ---------------------------------------------------------------------------
# Road access points.
#
# Several stops are lakes, summits, beaches or waterfalls with no road at the
# coordinate, so a router snaps them to whatever tarmac it can find -- often
# absurdly far.  These are where you actually leave the vehicle.
ACCESS = {
 "melo":       (42.26467, 9.05556),   # A Frasseta car park (shuttle terminus)
 "restonica":  (42.28900, 9.10600),   # lower gorge laybys
 "nino":       (42.28800, 8.90200),   # Fer a Cheval hairpin on the D84
 "saleccia":   (42.68129, 9.30250),   # boat from Saint-Florent
 "lotu":       (42.68129, 9.30250),   # same boat
 "lavezzi":    (41.38900, 9.16200),   # Bonifacio marina
 "scandola":   (42.26732, 8.69633),   # boat from Porto
 "girolata":   (42.33500, 8.65500),   # Col de la Croix
 "senino":     (42.32376, 8.63202),   # roadside car park by Osani
 "caporosso":  (42.24400, 8.60600),   # D824 layby
 "piscia":     (41.69470, 9.24930),   # signed car park on the D368
 "douaniers":  (42.95942, 9.45479),   # Macinaggio marina
 "aiguilles":  (41.79587, 9.22496),   # Col de Bavella
 "bonifatu":   (42.44338, 8.85290),   # Auberge de la Foret car park
 "figarella":  (42.44338, 8.85290),
 "hautasco":   (42.40329, 8.92356),   # Haut-Asco roadhead
 "ostriconi":  (42.66241, 9.06103),
 "bodri":      (42.62643, 8.91494),
 "vizzavona":  (42.12858, 9.13376),   # Col de Vizzavona
 "spusata":    (42.08350, 9.06382),   # Bocognano
 "arone":      (42.20723, 8.58014),
 "barcaggio":  (43.00611, 9.40216),
}
def access(poi_dict, pid):
    """Where you actually park for a stop."""
    if pid in ACCESS: return ACCESS[pid]
    p = poi_dict[pid]
    return (p["lat"], p["lon"])
