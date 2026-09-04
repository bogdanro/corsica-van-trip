# -*- coding: utf-8 -*-
"""How many independent guides mention each of our stops?"""
import urllib.request, re, json, unicodedata, time, os

SOURCES = {
 "voyagetips-2wk":   "https://www.voyagetips.com/en/2-weeks-in-corsica/",
 "voyagetips-35":    "https://www.voyagetips.com/en/things-to-do-in-corsica/",
 "voyagetips-road":  "https://www.voyagetips.com/en/road-trip-corsica/",
 "corsicalovers-2wk":"https://corsicalovers.fr/en/2-weeks-corsica-14-days-itinerary/",
 "corsicalovers-gem":"https://corsicalovers.fr/en/hidden-gems-corsica-off-beaten-path/",
 "coolcorsica-gems": "https://coolcorsica.com/15-hidden-gems-in-corsica-discover-the-islands-best-kept-secrets/",
 "thinkingtraveller":"https://www.thethinkingtraveller.com/blog/things-to-do-in-corsica",
 "lamariniere":      "https://lamariniereenvoyage.com/en/best-places-visit-corsica/",
 "bontraveler":      "https://www.bontraveler.com/corsica-itinerary/",
 "visitcorsica":     "https://www.visit-corsica.com/en/Explore-Corsica/Our-inspirations/Cultural-inspirations/Secret-Corsica-an-off-season-road-trip",
}
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", s)

CACHE = "data/sources.json"
if os.path.exists(CACHE):
    texts = json.load(open(CACHE))
else:
    texts = {}
    for k, u in SOURCES.items():
        try:
            r = urllib.request.Request(u, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
                "Accept-Language": "en"})
            html = urllib.request.urlopen(r, timeout=45).read().decode("utf-8", "ignore")
            html = re.sub(r"(?is)<(script|style|nav|footer)[^>]*>.*?</\1>", " ", html)
            texts[k] = norm(re.sub(r"<[^>]+>", " ", html))
            print(f"  {k:20s} {len(texts[k]):>7} chars")
        except Exception as e:
            print(f"  {k:20s} FAILED {str(e)[:50]}")
        time.sleep(1.0)
    json.dump(texts, open(CACHE, "w"))
print(f"{len(texts)} sources fetched\n")

# aliases so we match how guides actually write the names
ALIAS = {
 "douaniers":["sentier des douaniers","customs officers","macinaggio"],
 "calanches":["calanche","calanque de piana","calanques de piana","piana"],
 "caporosso":["capo rosso","capu rossu","turghiu"],
 "senino":["senino","capo senino"],
 "saleccia":["saleccia"], "lotu":["lotu","loto"],
 "melo":["melo","capitello"], "nino":["nino"],
 "restonica":["restonica"], "aiguilles":["bavella","aiguilles"],
 "bavella":["bavella"], "lavezzi":["lavezzi"],
 "santagiulia":["santa giulia"], "palombaggia":["palombaggia"],
 "rondinara":["rondinara"], "roccapina":["roccapina"],
 "scandola":["scandola"], "girolata":["girolata"],
 "spusata":["voile de la mariee","bridal veil","spusata"],
 "aruda":["a ruda","ruda"], "scala":["scala di santa regina"],
 "vergio":["vergio"], "hautasco":["asco","muvrella"], "asco":["asco"],
 "piscia":["piscia di gall","piscia"], "ospedale":["ospedale"],
 "cucuruzzu":["cucuruzzu"], "carbini":["carbini"],
 "filitosa":["filitosa"], "sartene":["sartene"], "stelucie":["sainte lucie de tallano","tallano"],
 "bonifacio":["bonifacio"], "ajaccio":["ajaccio"], "sanguinaires":["sanguinaires","parata"],
 "corte":["corte"], "calvi":["calvi"], "ilerousse":["ile rousse","l ile rousse"],
 "pigna":["pigna"], "santantonino":["sant antonino","sant antonin"],
 "bodri":["bodri"], "ostriconi":["ostriconi"], "lozari":["lozari"],
 "stflorent":["saint florent","st florent"], "vezzu":["bocca di vezzu","vezzu"],
 "nonza":["nonza"], "centuri":["centuri"], "barcaggio":["barcaggio"],
 "mattei":["moulin mattei","mattei"], "erbalunga":["erbalunga"], "bastia":["bastia"],
 "sisco":["sisco"], "macinaggio":["macinaggio"], "patrimonio":["patrimonio"],
 "porto":["porto ota","gulf of porto","golfe de porto"], "pianella":["spelunca","pianella"],
 "arone":["arone"], "piana":["piana"], "evisa":["evisa"], "ota":["ota"],
 "cristinacce":["cristinacce"], "calacuccia":["calacuccia","niolu"],
 "galeria":["galeria"], "calenzana":["calenzana"], "figarella":["bonifatu","figarella"],
 "bonifatu":["bonifatu"], "vizzavona":["vizzavona","cascade des anglais"],
 "tolla":["tolla"], "d1d4":["d4","d1"], "ghisoni":["ghisoni"],
 "aleria":["aleria"], "campi":["campi"], "orezza":["orezza","castagniccia"],
 "solenzara":["solenzara"], "portovecchio":["porto vecchio"],
 "zonza":["zonza"], "lozari":["lozari"],
}
src = json.loads(open("assets/js/data.js").read().split("window.TRIP = ",1)[1].rsplit(";",1)[0])
pois = {p["id"]: p for p in src["pois"] if p["c"] != "food"}
from pacing import STOP

rows=[]
for pid, p in pois.items():
    keys = ALIAS.get(pid) or [norm(p["n"].split("—")[0].split("&")[0])[:22].strip()]
    hits = sum(1 for t in texts.values() if any(k in t for k in keys))
    invid = bool(p.get("vid"))
    rows.append((hits, invid, pid, p["n"], STOP.get(pid,{}).get("pick","-")))
rows.sort(key=lambda r: (-r[0], r[1]))
print(f"{'src':>3} {'film':>5} {'pick':>7}  stop")
for h,v,pid,n,pick in rows:
    print(f"{h:>3}/{len(texts)} {'yes' if v else '  -':>5} {pick:>7}  {n[:52]}")
json.dump({r[2]: r[0] for r in rows}, open("data/corroboration.json","w"), indent=1)
