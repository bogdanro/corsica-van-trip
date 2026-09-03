# Corsica by Van — a 15-day trip plan

### → **[Van version](https://bogdanro.github.io/corsica-van-trip/)** · **[Hotel version](https://bogdanro.github.io/corsica-van-trip/hotels.html)**

A single-page trip-planning site built from the road-trip film
**[Corsica | An Incredible 10-Day Road Trip](https://www.youtube.com/watch?v=BVLl3bvjSQw)**,
re-paced from the film's 10 days to 15 for van travel while keeping every stop.

No build step and no framework. Open `index.html` in any browser, or use
`corsica-van-trip.html` — the same site inlined into one 223 KB file you can
email or open offline. Either way the interactive map needs internet access for
Leaflet and the map tiles; everything else works offline.

## Two versions of the same trip

The same stops, coordinates, photos and routing engine, re-planned around a
different constraint — a demonstration that changing *how you sleep* changes the
whole shape of a trip, not just one line of it.

| | Van (`index.html`) | Car + hotels (`hotels.html`) |
|---|---|---|
| Sleeps | 13 campsites + 2 hotels | 7 hotel bases, 15 nights |
| Shape | one continuous anticlockwise loop | 6 of 16 days are closed loops from a base |
| Driving | 1,448 km / 34 h | 1,582 km / 37 h — loops backtrack |
| Stops | 75 | 65 |
| Cost, 2 people | ≈ €2,605 (€81 pp/day) | ≈ €3,907 (€122 pp/day) |
| Gives up | comfort, laundry, a flat bed | the deep interior: Vergio, Nino, Asco, Ghisoni, Ota, Évisa, Orezza and four more |
| Wins | flexibility, cost, sleeping at altitude | no wild-camping law to worry about, unpack once |

## What's in it

| Section | Contents |
|---|---|
| Map | Leaflet map, 15 selectable day-routes drawn on real road geometry, 111 filterable pins across 11 categories, terrain/street basemap switch |
| Itinerary | 15 days, each with a photo gallery, its stops, a hike, a van hazard and the campsite it sleeps at |
| Timing | Every day carries a "be at your bed by" time; day 16 is a deliberate buffer before the ferry |
| Photos | 88 Creative-Commons photos from Wikimedia Commons, 6 per day, with a keyboard/swipe lightbox that credits every photographer |
| Hotels | 5 mid-budget hotels (+1 mountain bonus), each tied to the night it makes sense on |
| Camping | 30 van-friendly campsites with coordinates, price bands and websites, plus the Corsican wild-camping law |
| Hikes | 17 hikes and walks with distance, ascent, time and grade |
| Beaches | 21 beaches and freshwater swim spots |
| Van logistics | Ferries, real driving speeds, the roads a van should respect, water/waste/gas, when to go |
| Budget | Itemised estimate for two people over 15 days |

## Where the data came from

- **Stops and pacing** — the film's timestamped chapter list plus its narration.
  The transcript was fetched with `youtube-transcript-api` and is kept in
  `data/transcript.txt`. Where the narrator gives his own hike figures
  (Capo Rosso 8.5 km / 500 m / 3–4 h, Monte Senino 6 km / ~4 h, Bavella ~12 km /
  ~1,000 m, Figarella 5 km / 300 m, Melo 25 km / 8 h) those numbers are used in
  preference to guidebook figures.
- **Coordinates** — [Nominatim](https://nominatim.openstreetmap.org/) / OpenStreetMap.
  Every one of the 111 points is inside the Corsica bounding box; the validator
  in `gen_data.py` output checks this.
- **Campsites** — an [Overpass](https://overpass-api.de/) query for
  `tourism=camp_site` and `tourism=caravan_site` across `ISO3166-2=FR-20R`
  returned 254 sites (242 named); 30 were curated to match the route. Raw
  results in `data/campsites_raw.json`.
- **Routes** — [OSRM](https://project-osrm.org/) driving directions between each
  day's waypoints, so the lines follow actual roads and the distances and times
  are real. Geometry simplified with Ramer–Douglas–Peucker (55,249 → 6,067
  points) to keep `data.js` at ~163 KB.
- **Photos** — [Wikimedia Commons](https://commons.wikimedia.org/), selected per stop by
  geosearch around its coordinates plus a name search, then scored on licence,
  resolution, aspect ratio and title relevance. Candidates carrying coordinates
  outside the Corsica bounding box are rejected outright, which is what caught a
  Slovak tunnel, a Normandy forest and a Tuscan town hall matching on place-name
  alone. Each day keeps its 6 best, one per stop before any stop gets a second.
  Downloaded and re-encoded locally to WebP (1200 px full, 560 px thumb, 16 MB
  total) so the site serves its own images. Photographer and licence are recorded
  per photo in `data/photos.json` and shown in the lightbox, as CC-BY/CC-BY-SA
  require.
- **Restonica access** — verified by web search: the D623 has been closed beyond
  the Pont de Tragone since the November 2023 storms; the trailhead is now the
  A Frasseta car park, served by the Navetta Restonica C13 shuttle from Corte
  (2 May – 30 Sep, €4 return, app booking only). This materially changes day 10
  and the page says so.

## Files

```
index.html                 the page
assets/css/style.css       styles
assets/js/data.js          generated: pois, camps, stays, days (+route geometry, +photos)
assets/photos/             88 CC photos, WebP, full + thumb
assets/js/app.js           map, filters and section renderers
gen_data.py                regenerates assets/js/data.js (van)
gen_hotels.py              regenerates assets/js/data-hotels.js (car + hotels)
build_routes_hotels.py     OSRM routing for the hotel version's day loops
data/                      raw research: routes, geocodes, campsites, transcript
shots/                     rendered screenshots from the verification run
verify.py, shots.py        headless-Chromium checks and screenshots
```

## Regenerating

```bash
python3 fetch_photos.py                   # re-curate photo picks from Commons
python3 download_photos.py                # download + re-encode them
python3 gen_data.py                       # rewrite assets/js/data.js
python3 gen_hotels.py                     # rewrite assets/js/data-hotels.js
python3 -m http.server 8765               # then open http://127.0.0.1:8765
.venv/bin/python verify.py                # DOM/console/interaction checks + screenshots
```

`verify.py` asserts the day list, chips, itinerary, tables, pins and popups all
render, that day- and category-filtering actually changes the visible pin count,
and that the page throws no console errors or failed requests.

## Why 16 days for 15 days of content

Both versions are **15 days of plan plus a buffer day**, and night 15 is spent
20 minutes from the ferry gate. Ferries, mountain weather and hire cars will
take a day off you sooner or later; without a buffer that day comes out of the
crossing you already paid for.

The same realism drives the per-day timing. Corsican campsite receptions run
roughly 08:00–12:00 and 15:00–19:30 (earlier at altitude, earlier out of
season) and hotels check in from 15:00 — so every day states a target arrival,
generally 18:00, and the driving is sized to hit it. Days whose payoff is a
sunset (the Calanches, the Sanguinaires, Nonza) check in *first* and go back
out. Van day 10 sleeps in Corte a second time for the same reason: an
eight-hour hike and a 19:30 reception deadline cannot share a day.

These windows are typical, not per-property facts, and the page says so.

## Caveats

Coordinates, road routes and campsite existence are machine-verified. Prices,
opening hours, shuttle timetables and road closures are not — they change.
Confirm the Restonica situation locally. Wild camping is illegal in Corsica.
