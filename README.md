# Corsica — a 16-day trip plan, two ways, three views

### → **[Open the trip](https://bogdanro.github.io/corsica-van-trip/)**

Day-by-day view is the front page. The long reference pages are
**[van](https://bogdanro.github.io/corsica-van-trip/van.html)** and
**[hotels](https://bogdanro.github.io/corsica-van-trip/hotels.html)**.

A single-page trip-planning site built from the road-trip film
**[Corsica | An Incredible 10-Day Road Trip](https://www.youtube.com/watch?v=BVLl3bvjSQw)**,
re-paced from the film's 10 days to 15 of content over 16 days away — keeping every
stop, and adding a buffer day before the ferry.

No build step and no framework. Open `index.html` in any browser, or use
`corsica-van-trip.html` — the same site inlined into one 316 KB file you can
email or open offline. Either way the interactive map needs internet access for
Leaflet and the map tiles; everything else works offline.

## Three views

| View | File | For |
|---|---|---|
| **Day view** (landing) | `index.html` | one day at a time — swipe or arrow through a carousel |
| Long reference page | `van.html`, `hotels.html` | reading the whole trip, planning, the reference tables |

The **day view** is the low-clutter reading mode: a left rail of days, and a
carousel where each slide is one day — hero photo, a **mini map of just that
day with start ⚑ and finish 🏁 flags** (a single flag when the day is a loop),
the running order, a photo strip, and stops / eating folded into `<details>`.

Mini maps are deliberately non-interactive (no drag, no wheel zoom) so they
never fight the swipe gesture, and they initialise lazily — only the current
day and its two neighbours, rather than 16 Leaflet instances at once.

It serves both datasets: `/` for the van, `/?v=hotels` for the car-and-hotels
variant, and the rail's Reference links point at whichever long page matches.

`days.html` remains as a redirect (it was the URL before the day view was
promoted), and `index.html` remaps the long page's old anchors — `#day7`
becomes the carousel's `#d7`, and `#camping` and friends go to `van.html` or
`hotels.html`. Slides carry `id="dN"`, so hash deep links scroll the deck
natively.

## Two versions of the same trip

The same stops, coordinates, photos and routing engine, re-planned around a
different constraint — a demonstration that changing *how you sleep* changes the
whole shape of a trip, not just one line of it.

| | Van (`van.html`) | Car + hotels (`hotels.html`) |
|---|---|---|
| Sleeps | 13 campsites + 2 hotels | 7 hotel bases, 15 nights |
| Shape | one continuous anticlockwise loop | 6 of 16 days are closed loops from a base |
| Days | 16 (15 planned + a buffer) | 16 |
| Driving | 1,448 km / 34 h | 1,582 km / 37 h — loops backtrack |
| Stops | 75 (104 map pins with food) | 65 (94 pins) |
| Cost, 2 people | ≈ €2,605 (€81 pp/day) | ≈ €3,907 (€122 pp/day) |
| Gives up | comfort, laundry, a flat bed | the deep interior: Vergio, Nino, Asco, Ghisoni, Ota, Évisa, Orezza and four more |
| Wins | flexibility, cost, sleeping at altitude | no wild-camping law to worry about, unpack once |

## What's in it

| Section | Contents |
|---|---|
| Map | Leaflet map, 16 selectable day-routes drawn on real road geometry, 104 clustered pins across 12 categories, terrain/street basemap switch |
| Itinerary | 16 days, each with a running order, photo gallery, stops, hikes, a van hazard, vegan food and the campsite it sleeps at |
| Eating vegan | Per-day vegan-friendly places, evidence-labelled, plus a strategy section — Corsica is genuinely hard for vegans and the page says so |
| The day, roughly | A guide-style running order per day — soft blocks ("Morning", "After lunch") with slack, and hard clock times only where something won't wait |
| Timing | Every day carries a "be at your bed by" time; day 16 is a deliberate buffer before the ferry |
| Photos | 88 Creative-Commons photos from Wikimedia Commons, 6 per day, with a keyboard/swipe lightbox that credits every photographer |
| Hotels | 5 mid-budget hotels (+1 mountain bonus) in the van version, 7 bases in the hotel version |
| Camping | 31 van-friendly campsites with coordinates, price bands, check-in windows and websites, plus the Corsican wild-camping law |
| Hikes | 17 hikes and walks with distance, ascent, time and grade |
| Beaches | 21 beaches and freshwater swim spots |
| Van logistics | Ferries, real driving speeds, the roads a van should respect, water/waste/gas, when to go |
| Budget | Itemised estimate for two people over 16 days, arithmetic self-checked |

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

## How the two versions relate

Both are generated from **one stop dataset** by two generators:

```
gen_data.py    ──┐                      ┌── assets/js/data.js        → van.html
                 ├─ shared POI list ────┤
gen_hotels.py  ──┘  (exec'd from        └── assets/js/data-hotels.js → hotels.html
                     gen_data.py)
```

`gen_hotels.py` imports the POI list out of `gen_data.py` (by exec'ing the file
up to the DAYS marker, so importing does not trigger a write), then re-groups the
stops into 16 different days, re-routes them, overrides the 34 stop notes that
assumed a van, and drops the 10 stops with no mid-budget bed within an hour.

That is the interesting part of this repo: **changing the accommodation
constraint is a re-plan, not a filter.** Route topology changes (6 of 16 days
become closed loops from a base), coverage changes, and total driving goes *up*
by 135 km because loops backtrack.

The same page renderer (`assets/js/app.js`) drives both; section builders no-op
when a variant omits their section, which is how `hotels.html` simply has no
camping section.

## Files

```
index.html                 the day-by-day carousel (landing page)
van.html, hotels.html      the two long reference pages
days.html                  redirect, kept so older links still resolve
assets/css/style.css       styles
assets/js/data.js          generated: pois, camps, stays, days (+route geometry, +photos)
assets/photos/             88 CC photos, WebP, full + thumb
assets/js/app.js           map, filters and section renderers (long pages)
assets/js/days.js          the day-by-day carousel view
assets/css/days.css        carousel styles
eats.py                    vegan places + per-day eating notes
flows_van.py               per-day running order, van version
flows_hotel.py             per-day running order, car + hotel version
gen_data.py                regenerates assets/js/data.js (van)
gen_hotels.py              regenerates assets/js/data-hotels.js (car + hotels)
build_routes_hotels.py     OSRM routing for the hotel version's day loops
data/                      raw research: routes, geocodes, campsites, transcript
shots/                     rendered screenshots from the verification run
verify.py, shots.py        headless-Chromium checks and screenshots
verify_days.py             checks for the carousel view (run: `.venv/bin/python verify_days.py`)
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
and that the page throws no console errors or failed requests. `verify_gal.py`
exercises the gallery and lightbox; `verify_live.py` runs the same checks
against the deployed GitHub Pages URL rather than localhost.

Driving the UI rather than reading the code caught bugs that review would not
have — most notably that selecting a day fitted the map to the *driven route*
only, so stops reached on foot or by boat (Lac de Melo, Saleccia, the Lavezzi)
fell outside the viewport.

## The running order

Each day carries a **"The day, roughly"** panel: a narrated order of play in the
voice of someone who has done it — wake time, what to see before the heat, where
lunch happens, what to skip if you are behind.

It is deliberately **not** a minute-by-minute schedule. Blocks are soft
("Early", "Late morning", "After lunch") and carry slack, because this is a
holiday. Across both versions there are 212 blocks and only **34 fixed times** —
and those are exactly the things that will not wait for you: boat sailings, the
Restonica shuttle, campsite receptions, sunset, and the ferry. They are marked
`FIXED` and everything else is a suggestion.

Flows live in `flows_van.py` and `flows_hotel.py`, separate from the stop data,
so the narrative can be rewritten without touching coordinates or routing.

## Eating vegan

Corsican cuisine is charcuterie, brocciu, wild boar and fish, and there are
exactly **three fully plant-based or all-vegetarian kitchens on the island** —
VG in Bastia, and Green Farmer's and A Cantali in Ajaccio. The site does not
pretend otherwise.

Every day carries an "Eating vegan today" block. 32 places are named, all of
them existing in OpenStreetMap or HappyCow at the coordinates given — none
invented — and each carries an evidence badge, because the strength of the
source varies a lot:

| Badge | Means |
|---|---|
| **Fully vegan** | plant-based kitchen |
| **Vegan options** | vegan dishes confirmed (OSM `diet:vegan=yes`, or a HappyCow listing) |
| **Veg-friendly — ask** | OSM `diet:vegetarian=yes`; vegan is a conversation |
| **Shop / market** | organic supermarket, greengrocer or market |

On the days where the honest answer is "carry your own" — Saleccia, Piana and
Arone, the Lavezzi, the day-15 east coast — the block says that instead of
inventing a restaurant. The `#vegan` section covers the strategy: pizza
marinara as a floor, self-catering, saying *végétalien* rather than
*végétarien*, and phoning mountain auberges in the morning.

Sourced from an Overpass query for `diet:vegan` / `diet:vegetarian` across
Corsica (`data/vegan_raw.json`, 72 results) plus HappyCow. Data lives in
`eats.py`.

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
