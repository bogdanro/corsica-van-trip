# -*- coding: utf-8 -*-
"""Hotel/car variant: same stops and photos, different sleeping strategy.

Sleeps in 7 bases over 14 nights instead of moving every night, so the days
become loops out and back rather than one continuous line.
"""
import json, io

# reuse the POI list from the van build without triggering its file write
src = io.open("gen_data.py", encoding="utf-8").read()
src = src.split("# ---------------------------------------------------------------- DAYS")[0]
src = src.replace('routes = json.load(open("data/routes_simplified.json"))', "routes = []")
ns = {}
exec(compile(src, "gen_data.py", "exec"), ns)
POIS = {p["id"]: dict(p) for p in ns["POIS"]}

routes = json.load(open("data/routes_hotels.json"))
photos_van = json.load(open("data/photos.json"))

# ---------------------------------------------------------------- day plan
HOTEL_DAYS = {
 1:  ["bastia","erbalunga","sisco"],
 2:  ["douaniers","macinaggio","barcaggio","mattei","centuri","nonza","patrimonio"],
 3:  ["stflorent","vezzu","lotu","saleccia"],
 4:  ["ostriconi","lozari","ilerousse","pigna","santantonino","bodri"],
 5:  ["calvi","calenzana","figarella","bonifatu"],
 6:  ["galeria","senino","scandola","girolata","porto","pianella"],
 7:  ["calanches","piana","caporosso","arone"],
 8:  ["ajaccio","sanguinaires"],
 9:  ["tolla","spusata","vizzavona","d1d4"],
 10: ["filitosa","sartene","roccapina"],
 11: ["bonifacio","lavezzi","rondinara"],
 12: ["santagiulia","palombaggia","portovecchio","ospedale","piscia","zonza"],
 13: ["cucuruzzu","carbini","bavella","aiguilles","solenzara","aleria"],
 14: ["restonica","melo","corte"],
 15: ["scala","calacuccia","aruda"],
}

DAY_META = {
 1:  dict(base="Bastia", theme="Land, drop the bags, walk the old port", vid="00:00–01:29",
          intro="The ferry docks in the morning. Check in, leave the car, and spend the day on foot between Bastia's old port and the first villages up the Cap."),
 2:  dict(base="Bastia", theme="The whole Cap in one loop", vid="01:29–08:32",
          intro="The big advantage of a base: today is a 137 km circuit of the entire peninsula and you come back to the same bed. No packing."),
 3:  dict(base="Bastia", theme="The Agriates, mostly by boat", vid="08:32",
          intro="Saint-Florent in the morning, then a boat to the beaches you cannot drive to. Back in Bastia for the third and last night."),
 4:  dict(base="Calvi", theme="Along the Balagne to Calvi", vid="08:32–12:08",
          intro="The one long transfer of the first week, broken by a wild beach, a market town and two perched villages."),
 5:  dict(base="Calvi", theme="Citadel, chestnut villages and a river", vid="12:08–13:07",
          intro="Old town in the morning, mountains in the afternoon, and back to Calvi for dinner on the quay."),
 6:  dict(base="Porto", theme="The wild west coast", vid="13:07–16:22",
          intro="105 km that takes over three hours. The most spectacular driving on the island, and the day you understand Corsican distances."),
 7:  dict(base="Porto", theme="Red granite and a beach", vid="18:27–19:03",
          intro="A loop from Porto: the Calanches early, Capo Rosso before it gets hot, Arone all afternoon."),
 8:  dict(base="Ajaccio", theme="South to the capital", vid="36:42–37:21",
          intro="Down the coast through the Greek village of Cargèse, into Ajaccio by mid-afternoon, and out to the Sanguinaires for sunset."),
 9:  dict(base="Ajaccio", theme="A mountain day, then back to the city", vid="35:45–38:16",
          intro="The day a hotel base really pays: a 136 km mountain circuit with no luggage in the car, and a restaurant waiting at the end."),
 10: dict(base="Bonifacio", theme="Menhirs, granite towns, a lion", vid="30:45–31:19",
          intro="The long run south, broken by the best prehistoric site on the island and a beach under a lion-shaped rock."),
 11: dict(base="Bonifacio", theme="Cliffs, and a boat to the Lavezzi", vid="31:19–33:32",
          intro="Almost no driving. The Haute Ville on foot, a boat out to the granite islands, and a swim at Rondinara."),
 12: dict(base="Zonza", theme="White sand in the morning, pine forest by dusk", vid="29:19",
          intro="Three of Europe's best beaches, then 900 m up into the Ospedale forest. The longest day of the trip — start early."),
 13: dict(base="Corte", theme="Bronze Age, then the needles", vid="26:30–29:56 / 25:23",
          intro="A fortified site in an oak wood, the Bavella needles at their best in the morning light, then down to the sea and across to Corte."),
 14: dict(base="Corte", theme="Restonica — the big one", vid="40:00–44:38",
          intro="The hike people come to Corsica for, reached by shuttle since the road collapsed. Corte's citadel in the evening if your legs allow."),
 15: dict(base="ferry", theme="The Niolu, then home", vid="21:28–23:32 / 46:20",
          intro="A last mountain valley on the way north — a red granite gorge and a turquoise reservoir under Monte Cinto — then the ferry gate at Bastia."),
}

# ---------------------------------------------------------------- car notes
# Every stop whose van note assumed a van, rewritten for a car + hotel trip.
CAR = {
"bastia": "Hotels in the old town mostly have no parking; use Parking du Port or Parking Gaudin and walk. Leave the car there for the whole first day — everything is walkable.",
"macinaggio": "Free harbour car park. If you want the coastal walk one-way, the U Spinu shuttle boat runs Macinaggio↔Barcaggio in summer.",
"barcaggio": "The D253 is narrow with passing places but completely fine in a car — this is one of the roads a van has to think twice about. Park at the village entrance.",
"stflorent": "Paid parking by the port. Buy your Saleccia/Lotu boat tickets here the day before in July–August.",
"vezzu": "Layby at the col with room for a few cars. Best light late afternoon.",
"lotu": "No road access at all. Take the Popeye or Le Petit Train boat from Saint-Florent, 25 minutes.",
"saleccia": "The 12 km Casta piste is a rock-strewn 4x4 track and almost every rental contract forbids it — a normal hire car will be damaged and uninsured. Take the boat from Saint-Florent or the 4x4 shuttle from Casta.",
"ostriconi": "Signed car park off the N1197, then 15 minutes down through the dunes.",
"lozari": "Large free car park behind the beach.",
"ilerousse": "Paid parking along the seafront; the market is two minutes' walk. Go before 11:00.",
"bodri": "Small signed car park off the N197, then 10 minutes through the maquis. It fills by 10:30 in August.",
"calvi": "Park at the Port de Plaisance or the station and walk up to the citadel — the ramp is not for cars. Most Calvi hotels have their own parking; confirm when booking.",
"figarella": "Paved all the way from Calenzana to the Auberge de la Forêt de Bonifatu car park (paid). Easy in a car.",
"calenzana": "Free village car park on the square.",
"galeria": "Small beach car park. Last fuel before the west coast — fill up here.",
"senino": "Big roadside car park on the D81 by Osani (42.324, 8.632). The track beyond it is for walking, not driving.",
"porto": "Paid parking by the marina. Porto is small enough to leave the car for two days and walk everywhere.",
"arone": "Free beach car park at the end of the D824.",
"calacuccia": "Laybys all round the lake road; the best swimming access is near the bridge.",
"aruda": "Narrow, twisting, with drops — slow but straightforward in a car. Laybys give access down to the river; wear something on your feet.",
"scala": "Good tarmac, narrow, rock walls on one side. Take the corners wide and enjoy it.",
"corte": "Paid parking below the old town, or leave the car at the hotel — Corte is entirely walkable and the Restonica shuttle leaves from the station.",
"melo": "Drive nothing. Take the Navetta C13 from Corte station (€4 return, booked in the M-Ticket Via Corsica app) and be on the trail at first light.",
"vizzavona": "Big free laybys at La Foce / Col de Vizzavona on the N193, with shade.",
"tolla": "The D3 in from Bastelicaccia is narrow and twisting with drops — slow, but no problem in a car. Laybys with lake views the whole way.",
"ajaccio": "Do not drive into the centre. Parking Diamant is the easy option, and most old-town hotels will point you at a garage rate.",
"roccapina": "The 3.5 km track down from the N196 is rutted and rocky. A low-slung hire car will scrape and your contract probably excludes it — park at the top layby and walk down in 45 minutes.",
"bonifacio": "Park at the Parking de la Citadelle or Parking Vallée and walk; the Haute Ville is pedestrian. Marina hotels have valet or reserved spaces — ask, because parking here is genuinely hard in August.",
"lavezzi": "Boats from Bonifacio marina, 2–3 sailings a day, around €35. Leave the car in the harbour car park.",
"rondinara": "4 km of paved side road off the N198, then a big paid car park.",
"bavella": "The D268 up from Solenzara is a spectacular hairpinned climb and a pleasure in a car. Large gravel car parks either side of the col.",
"zonza": "Free village car parks; the hotels here all have their own.",
"d1d4": "Narrow with unguarded edges, but this is exactly the road a car is built for and a van is not. Allow double the time the map claims, and don't do it after dark.",
"solenzara": "Free parking along the seafront and at the marina.",
}

# ---------------------------------------------------------------- hotels
STAYS = [
 dict(id="h-gouverneurs", n="Hôtel des Gouverneurs, Bastia", lat=42.69327, lon=9.4522,
      d=1, nights="1–3", rank=1, price="€95–135 B&B",
      w="https://www.hotel-desgouverneurs.com",
      t="A restored 16th-century house inside the Bastia citadel, with a roof terrace over the old port and rooms in the thick original walls.",
      why="Three nights here cover the whole north-east: the old town on foot, the Cap Corse circuit, and the Agriates by boat — without moving your bags once."),
 dict(id="h-mariana", n="Le Mariana, Calvi", lat=42.56445, lon=8.75301,
      d=4, nights="4–5", rank=2, price="€110–160 B&B",
      w="https://www.hotel-mariana.com",
      t="Calvi's best value by common consent: big, spotless rooms, a pool, a rooftop terrace, on-site parking, and 10 minutes' walk to both the citadel and the pine beach.",
      why="The Balagne and the Bonifatu mountains are both inside an hour, so two nights is plenty — and after the day-4 transfer you will want the pool."),
 dict(id="h-legolfe", n="Hôtel Le Golfe, Porto", lat=42.26763, lon=8.69375,
      d=6, nights="6–7", rank=3, price="€95–150, sea-view rooms",
      w="https://www.hotel-le-golfe.com",
      t="On the marina at the foot of the Genoese tower, with balconies straight onto the Gulf of Porto and the Scandola boats leaving below you.",
      why="The Calanches are 15 minutes away, which means you can be there for sunset and still have dinner. Doing this stretch without a bed nearby is the classic mistake."),
 dict(id="h-napoleon", n="Hôtel Napoléon, Ajaccio", lat=41.92092, lon=8.73609,
      d=8, nights="8–9", rank=4, price="€100–140",
      w="https://www.hotelnapoleonajaccio.com",
      t="A quiet courtyard hotel in a lane off the Cours Napoléon, two minutes from the Place Foch market and the old port, with a garage rate for the car.",
      why="Two nights buys you a proper city evening and a full mountain day with an empty boot. Ajaccio is also the best restaurant town on the island."),
 dict(id="h-nautique", n="Hôtel Centre Nautique, Bonifacio", lat=41.38971, lon=9.16431,
      d=10, nights="10–11", rank=5, price="€140–200",
      w="https://www.centre-nautique.com",
      t="A converted boathouse on the marina quay, looking straight up at the Haute Ville on its cliff. Split-level rooms, and the ramparts are a ten-minute climb.",
      why="The most expensive bed of the trip and the one worth paying for: Bonifacio empties at dusk when the day-trippers leave, and you get the ramparts almost to yourself."),
 dict(id="h-aiglon", n="Hôtel L'Aiglon, Zonza", lat=41.75044, lon=9.17156,
      d=12, nights="12", rank=6, price="€80–120, half-board available",
      w=None,
      t="A granite village inn under the Bavella needles, doing wild boar, chestnut and river trout. Simple rooms, log fire out of season, hikers everywhere.",
      why="One mountain night at 800 m between the beaches and Corte. It also puts you 20 minutes from the Bavella trailheads for a dawn start."),
 dict(id="h-dunord", n="Hôtel du Nord, Corte", lat=42.30729, lon=9.15066,
      d=14, nights="13–14", rank=7, price="€85–120 B&B",
      w="https://www.hoteldunord-corte.com",
      t="Right on the Cours Paoli in the middle of the old town, family-run, generous breakfast, and the cheapest good bed on the island.",
      why="Walk to the Restonica shuttle in the morning, walk to dinner at night. After the Melo hike you will not want to drive anywhere."),
]

# ---------------------------------------------------------------- assemble
poi_photo = {}
for d, lst in photos_van.items():
    for ph in lst:
        poi_photo.setdefault(ph["poi"], []).append(ph)

pois_out, seen_photo = [], set()
for day, ids in HOTEL_DAYS.items():
    for pid in ids:
        p = dict(POIS[pid]); p["d"] = day
        if pid in CAR: p["van"] = CAR[pid]
        pois_out.append(p)

days = []
for r in routes:
    m = DAY_META[r["day"]]
    ph = []
    for pid in HOTEL_DAYS[r["day"]]:
        for x in poi_photo.get(pid, []):
            if x["f"] in seen_photo: continue
            seen_photo.add(x["f"]); ph.append(x)
            if len(ph) >= 6: break
        if len(ph) >= 6: break
    days.append(dict(day=r["day"], title=r["title"], km=r["km"], min=r["min"],
                     geometry=r["geometry"], base=m["base"], theme=m["theme"],
                     vid=m["vid"], intro=m["intro"], photos=ph))

out = dict(pois=pois_out, camps=[], stays=STAYS, days=days)
with open("assets/js/data-hotels.js", "w") as f:
    f.write("// Generated by gen_hotels.py — hotel/car variant of the Corsica route.\n")
    f.write("window.TRIP = ")
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    f.write(";\n")

import os
dropped = sorted(set(POIS) - {p["id"] for p in pois_out})
print("pois", len(pois_out), "| stays", len(STAYS), "| days", len(days),
      "| photos", sum(len(d["photos"]) for d in days))
print("data-hotels.js %.1f KB" % (os.path.getsize("assets/js/data-hotels.js")/1024))
print("total", round(sum(d["km"] for d in days), 1), "km |",
      round(sum(d["min"] for d in days)/60, 1), "h moving")
print("dropped vs van version:", dropped)
json.dump(dropped, open("data/hotels_dropped.json", "w"))
