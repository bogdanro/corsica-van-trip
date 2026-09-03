# -*- coding: utf-8 -*-
"""Download the curated Commons photos, make thumb+full WebP, record attribution."""
import json, os, re, io, urllib.request, urllib.parse, time, unicodedata
from PIL import Image

UA = "corsica-trip-planner/1.0 (https://bogdanro.github.io/corsica-van-trip/; claude@bogdanr.ro)"
OUT = "assets/photos"
os.makedirs(OUT, exist_ok=True)
picks = json.load(open("data/photo_picks.json"))

def slug(t):
    t = re.sub(r"^File:", "", t); t = re.sub(r"\.[A-Za-z]+$", "", t)
    t = unicodedata.normalize("NFD", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-").lower()
    return t[:52]

def strip_html(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    s = s.replace("&amp;", "&").replace("&#039;", "'").replace("&quot;", '"')
    return re.sub(r"\s+", " ", s).strip()

def meta(titles):
    """Batch imageinfo for up to 50 files."""
    out = {}
    for i in range(0, len(titles), 25):
        batch = titles[i:i+25]
        p = {"action": "query", "titles": "|".join(batch), "format": "json",
             "formatversion": "2", "prop": "imageinfo",
             "iiprop": "url|extmetadata|size", "iiurlwidth": "1400"}
        u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)
        r = urllib.request.Request(u, headers={"User-Agent": UA})
        j = json.loads(urllib.request.urlopen(r, timeout=60).read())
        for pg in j.get("query", {}).get("pages", []):
            out[pg["title"]] = pg
        time.sleep(0.4)
    return out

all_titles = sorted({x["title"] for v in picks.values() for x in v})
print("fetching metadata for", len(all_titles), "files")
M = meta(all_titles)

photos = {}
seen_files = set()
for day, items in sorted(picks.items(), key=lambda x: int(x[0])):
    lst = []
    for it in items:
        pg = M.get(it["title"])
        if not pg or not pg.get("imageinfo"):
            print("  !! no imageinfo:", it["title"]); continue
        ii = pg["imageinfo"][0]; em = ii.get("extmetadata", {})
        base = slug(it["title"])
        if base in seen_files: base += "-2"
        seen_files.add(base)
        fp_full  = f"{OUT}/{base}.webp"
        fp_thumb = f"{OUT}/{base}-t.webp"
        if not os.path.exists(fp_full):
            try:
                r = urllib.request.Request(ii["thumburl"], headers={"User-Agent": UA})
                raw = urllib.request.urlopen(r, timeout=90).read()
                im = Image.open(io.BytesIO(raw)).convert("RGB")
                f = im.copy(); f.thumbnail((1400, 1400), Image.LANCZOS)
                f.save(fp_full, "WEBP", quality=76, method=5)
                t = im.copy(); t.thumbnail((560, 560), Image.LANCZOS)
                t.save(fp_thumb, "WEBP", quality=72, method=5)
                time.sleep(0.25)
            except Exception as e:
                print("  !! download fail:", it["title"][:50], str(e)[:60]); continue
        author = strip_html(em.get("Artist", {}).get("value", "")) or "Unknown"
        if len(author) > 46: author = author[:44].rstrip() + "…"
        lst.append({
            "f": base,
            "cap": strip_html(em.get("ObjectName", {}).get("value", "")) or
                   re.sub(r"^File:|\.[A-Za-z]+$", "", it["title"]),
            "poi": it["poi"],
            "by": author,
            "lic": strip_html(em.get("LicenseShortName", {}).get("value", "")) or "see source",
            "src": pg.get("descriptionurl") or ii.get("descriptionurl", ""),
        })
    photos[day] = lst
    print(f"day {day:>2}: {len(lst)} photos")

json.dump(photos, open("data/photos.json", "w"), indent=1, ensure_ascii=False)
tot = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
print(f"\n{len(os.listdir(OUT))} files, {tot/1024/1024:.1f} MB total")
