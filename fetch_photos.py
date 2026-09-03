# -*- coding: utf-8 -*-
"""Curate Creative-Commons photos from Wikimedia Commons for each day of the trip."""
import urllib.request, urllib.parse, json, os, re, time, io as _io, sys

UA = "corsica-trip-planner/1.0 (https://bogdanro.github.io/corsica-van-trip/; claude@bogdanr.ro)"
CACHE = "data/commons_cache.json"
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def api(params, key):
    if key in cache: return cache[key]
    params.update({"format": "json", "formatversion": "2"})
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            r = urllib.request.Request(u, headers={"User-Agent": UA})
            j = json.loads(urllib.request.urlopen(r, timeout=40).read())
            cache[key] = j
            json.dump(cache, open(CACHE, "w"))
            time.sleep(0.35)
            return j
        except Exception as e:
            if attempt == 2:
                print("   API fail:", str(e)[:70]); return {}
            time.sleep(2)

IIPROPS = {"prop": "imageinfo|coordinates", "iiprop": "url|extmetadata|size|mime",
           "iiurlwidth": "1200", "colimit": "5"}

# Corsica, with a little margin. A candidate that carries coordinates must sit inside this.
BBOX = (41.25, 43.15, 8.45, 9.65)

# generic words that must never be treated as a place-identifying token
GENERIC = {"plage","tour","hotel","camping","village","gorge","route","roads","forest",
           "foret","forêt","lac","col","pont","mountain","crossing","beach","old","town",
           "the","and","its","cliffs","needles","white","beaches","market","citadelle",
           "vieux","port","east","tip","desert","river","pools","valley","waterfall",
           "archipel","islands","iles","îles","reserve","naturelle","chestnut","forests",
           "viewpoint","cascade","canyon","station","ski","genoese","peninsula"}

def tokens(name):
    """Distinctive proper-noun-ish tokens from a POI name."""
    import unicodedata
    raw = re.findall(r"[A-Za-zÀ-ÿ'’-]{4,}", name)
    out = []
    for w in raw:
        wl = w.lower().strip("'’-")
        if wl in GENERIC or len(wl) < 4: continue
        n = "".join(c for c in unicodedata.normalize("NFD", wl)
                    if unicodedata.category(c) != "Mn")
        out.append(n)
    return out

BAD = re.compile(r"(map|carte|plan\b|blason|coat[_ ]of[_ ]arms|armoiries|drapeau|flag|logo|"
                 r"diagram|sch[eé]ma|panneau|sign\b|plaque|timbre|stamp|graph|chart|"
                 r"\bgpx\b|topograph|cadastr|localisation|situation|icon|symbol|"
                 r"portrait|buste|statue de|tombe|grave|cimeti|monument aux morts|"
                 r"blazon|orthophoto|satellite|\bIGN\b|\bOSM\b|"
                 # added after reviewing the first pass:
                 r"\bISS\d|from space|interdit|forbidden|echantillonnage|échantillonnage|"
                 r"biofouling|campagne |munisipyo|mairie|municipio|palazzo|"
                 r"\bgare\b|railway station|panorami[oc] ?\(|"
                 r"podarcis|larus|falco|discoglossus|euproctus|sitta |species|"
                 r"tunnel|l[aá]vka|portal|"
                 # second review pass: technically-correct but not gallery material
                 r"greenschist|prasinite|\bmineral|rock sample|\bgeolog|"
                 r"breakfast|d[eé]jeuner|restaurant|pizza|assiette|\brepas\b|"
                 r"\binside\b|int[eé]rieur|\bnave\b|ch(oe|œ)ur|autel|orgue|retable|"
                 r"\bcat in\b|\bchat\b|\bdog\b|\bchien\b|"
                 r"crocus|orchi|\bfleur|\bflore\b|gen[eê]t|\bplant\b|"
                 r"bunker|blockhaus|boutique|\bshop\b|magasin|"
                 r"lavoir|fontaine|abreuvoir|\bbanc\b|\bbench\b|inscription|"
                 r"fractal|tailings|\bpigs?\b|cochon|cimeti|"
                 r"abandonn[eé]e|freigespreng)", re.I)
GOODEXT = re.compile(r"\.(jpe?g|webp)$", re.I)

def in_corsica(p):
    c = (p.get("coordinates") or [])
    if not c: return None                      # unknown
    la, lo = c[0].get("lat"), c[0].get("lon")
    if la is None: return None
    return BBOX[0] <= la <= BBOX[1] and BBOX[2] <= lo <= BBOX[3]

def candidates(poi):
    out = {}
    lat, lon, name = poi["lat"], poi["lon"], poi["n"]
    # 1) geosearch around the coordinate
    j = api(dict(action="query", generator="geosearch", ggscoord=f"{lat}|{lon}",
                 ggsradius="2000", ggslimit="40", ggsnamespace="6", **IIPROPS),
            f"geo2:{lat},{lon}")
    for p in j.get("query", {}).get("pages", []):
        p["_near"] = True; out[p["title"]] = p
    # 2) full-text search on the place name, files only
    q = re.split(r"[—&(/]", name)[0].strip()
    j = api(dict(action="query", generator="search", gsrsearch=f'filetype:bitmap "{q}"',
                 gsrnamespace="6", gsrlimit="30", **IIPROPS), f"srch2:{q}")
    for p in j.get("query", {}).get("pages", []): out.setdefault(p["title"], p)
    return list(out.values())

def score(p, poi):
    ii = (p.get("imageinfo") or [{}])[0]
    if not ii.get("thumburl"): return -99
    t = p["title"]
    if BAD.search(t): return -99
    # --- provenance gate: the photo must credibly be OF this place ---
    geo = in_corsica(p)
    if geo is False: return -99                    # has coordinates, and they are elsewhere
    if not p.get("_near"):                         # came from name search, not geosearch
        import unicodedata
        tl = "".join(c for c in unicodedata.normalize("NFD", t.lower())
                     if unicodedata.category(c) != "Mn")
        toks = tokens(poi["n"])
        if not any(tk in tl for tk in toks): return -99
        if geo is None and "cors" not in tl:       # no coords and no Corsica marker
            return -99
    if not GOODEXT.search(t): return -99
    if (ii.get("mime") or "") not in ("image/jpeg", "image/webp"): return -99
    w, h = ii.get("width", 0), ii.get("height", 0)
    if w < 1100 or h < 700: return -99
    if w / max(h, 1) > 3.2: return -99          # stitched panoramas crop badly
    em = ii.get("extmetadata", {})
    lic = (em.get("LicenseShortName", {}).get("value") or "")
    if "fair use" in lic.lower() or "non-free" in lic.lower(): return -99
    s = 0.0
    cats = (em.get("Categories", {}).get("value") or "")
    if "Featured pictures" in cats: s += 6
    if "Quality images" in cats: s += 4
    if "Valued images" in cats: s += 2
    if 1.2 <= w / max(h, 1) <= 2.0: s += 3      # landscape reads best in a strip
    elif w > h: s += 1.5
    if w >= 2400: s += 1.5
    elif w >= 1600: s += 0.8
    import unicodedata
    tl = "".join(c for c in unicodedata.normalize("NFD", t.lower())
                 if unicodedata.category(c) != "Mn")
    if any(tk in tl for tk in tokens(poi["n"])): s += 3
    if p.get("_near"): s += 1.5
    if in_corsica(p): s += 1
    if "corse" in tl or "corsica" in tl: s += 0.6
    if "panoramio" in tl: s -= 1.2
    return s

def prefix(t):
    """Collapse near-identical series: 'Foo (1).jpg', 'Foo (2).jpg' -> 'foo'."""
    t = re.sub(r"^File:", "", t)
    t = re.sub(r"\.[a-z]+$", "", t, flags=re.I)
    t = re.sub(r"[\s_]*\(?\d+\)?$", "", t)
    return re.sub(r"[^a-z]", "", t.lower())[:26]

def strip_html(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s).strip()

if __name__ == "__main__":
    import importlib.util
    spec = importlib.util.spec_from_file_location("gd", "gen_data.py")
    # gen_data writes a file on import; read its POIS via exec in a guarded namespace instead
    src = open("gen_data.py", encoding="utf-8").read()
    src = src.split("# ---------------------------------------------------------------- DAYS")[0]
    src = src.replace('routes = json.load(open("data/routes_simplified.json"))', "routes = []")
    ns = {}
    exec(compile(src, "gen_data.py", "exec"), ns)
    POIS = ns["POIS"]

    # how many photos we want per day, and which POIs are worth photographing
    SKIP = {"port"}
    SKIP_IDS = {"d1d4"}          # "D1 & D4" matches road names all over Europe
    picked = {}
    used = set()                 # global: never use the same file on two stops
    for poi in POIS:
        if poi["c"] in SKIP or poi["id"] in SKIP_IDS: continue
        cs = candidates(poi)
        scored = sorted(((score(c, poi), c) for c in cs), key=lambda x: -x[0])
        keep, seen = [], set()
        for s, c in scored:
            if s < 2.5: break
            pf = prefix(c["title"])
            if pf in seen or pf in used or c["title"] in used: continue
            seen.add(pf); used.add(pf); used.add(c["title"])
            keep.append((s, c))
            if len(keep) == 2: break
        if keep:
            picked[poi["id"]] = (poi, keep)
        print(f'{poi["d"]:>3}  {poi["n"][:44]:46s} {len(cs):>3} cand -> {len(keep)}')
    # --- cap each day at PER_DAY, taking one photo per stop before any second ---
    PER_DAY = 6
    byday = {}
    for pid, (poi, keep) in picked.items():
        byday.setdefault(poi["d"], []).append((poi, keep))
    final = {}
    for d, entries in byday.items():
        entries.sort(key=lambda e: -e[1][0][0])          # strongest stop first
        chosen, rnd = [], 0
        while len(chosen) < PER_DAY and rnd < 2:
            for poi, keep in entries:
                if rnd < len(keep) and len(chosen) < PER_DAY:
                    chosen.append((poi, keep[rnd][1], keep[rnd][0]))
            rnd += 1
        final[d] = chosen
    out = {}
    for d, ch in final.items():
        for poi, c, sc in ch:
            out.setdefault(str(d), []).append({"poi": poi["id"], "poi_name": poi["n"],
                                               "title": c["title"], "score": round(sc, 1)})
    json.dump(out, open("data/photo_picks.json", "w"), indent=1, ensure_ascii=False)
    json.dump({d: [c for _, c, _ in ch] for d, ch in final.items()},
              open("data/photo_pages.json", "w"), indent=1, ensure_ascii=False)
    n = sum(len(v) for v in out.values())
    print("\nPOIs matched:", len(picked), "/", len(POIS), "| photos kept:", n)
    print("per day:", {d: len(v) for d, v in sorted(out.items(), key=lambda x: int(x[0]))})
