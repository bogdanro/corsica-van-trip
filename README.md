# Corsica by Van — a 15-day trip plan

A single-page, self-contained trip-planning site built from the road-trip film
**[Corsica | An Incredible 10-Day Road Trip](https://www.youtube.com/watch?v=BVLl3bvjSQw)**.

Open `index.html` in a browser. No build step, no server required (though the
interactive map needs internet access for Leaflet and map tiles).

## What's in it

| Section | Contents |
|---|---|
| Map | Leaflet map, 15 selectable day-routes drawn on real road geometry, 111 filterable pins across 11 categories, terrain/street basemap switch |
| Itinerary | 15 days, each with its stops, a hike, a van hazard and the campsite it sleeps at |
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
- **Restonica access** — verified by web search: the D623 has been closed beyond
  the Pont de Tragone since the November 2023 storms; the trailhead is now the
  A Frasseta car park, served by the Navetta Restonica C13 shuttle from Corte
  (2 May – 30 Sep, €4 return, app booking only). This materially changes day 10
  and the page says so.

## Files

```
index.html                 the page
assets/css/style.css       styles
assets/js/data.js          generated: pois, camps, stays, days (+route geometry)
assets/js/app.js           map, filters and section renderers
gen_data.py                regenerates assets/js/data.js
data/                      raw research: routes, geocodes, campsites, transcript
shots/                     rendered screenshots from the verification run
verify.py, shots.py        headless-Chromium checks and screenshots
```

## Regenerating

```bash
python3 gen_data.py                       # rewrite assets/js/data.js
python3 -m http.server 8765               # then open http://127.0.0.1:8765
.venv/bin/python verify.py                # DOM/console/interaction checks + screenshots
```

`verify.py` asserts the day list, chips, itinerary, tables, pins and popups all
render, that day- and category-filtering actually changes the visible pin count,
and that the page throws no console errors or failed requests.

## Caveats

Coordinates, road routes and campsite existence are machine-verified. Prices,
opening hours, shuttle timetables and road closures are not — they change.
Confirm the Restonica situation locally. Wild camping is illegal in Corsica.
