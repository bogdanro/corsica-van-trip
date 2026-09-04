# -*- coding: utf-8 -*-
import json

from flows_van import FLOW
routes = json.load(open("data/routes_simplified.json"))
try:
    _PH = json.load(open("data/photos.json"))
except FileNotFoundError:
    _PH = {}
# index photos by stop, so they follow a stop when it moves between days
PHOTO_BY_POI = {}
for _d, _lst in _PH.items():
    for _x in _lst:
        PHOTO_BY_POI.setdefault(_x["poi"], []).append(_x)

# ---------------------------------------------------------------- POIs
# cat: town | hike | beach | view | swim | heritage | camp | stay | port
# f (flags): what kind of traveller it serves -> nature / relax / culture
P = lambda **k: k
POIS = [
# ---- DAY 1 -------------------------------------------------------
P(id="bastia", n="Bastia — Vieux Port & Terra Vecchia", c="town", d=1, lat=42.69746, lon=9.44977,
  f=["culture"], vid="01:07",
  t="Your ferry lands here. Don't just drive off — the horseshoe of the Vieux Port under the twin bell towers of St-Jean-Baptiste is one of the best hours in Corsica. Walk up into Terra Vecchia's laundry-strung alleys, then the Citadelle for the view back over the roofs.",
  van="Park the van at Parking du Port / Parking Gaudin (paid, no height issue) and walk. The old streets are not van territory.",
  time="2–3 h"),
P(id="erbalunga", n="Erbalunga & its Genoese tower", c="town", d=1, lat=42.7736, lon=9.47699,
  f=["culture","relax"], vid="01:29",
  t="First stop on the Cap Corse coast road. A tiny fishing harbour with a half-ruined Genoese tower standing in the water, and one of the island's prettiest waterfront cafés.",
  van="Small car park above the village on the D80. Walk down 3 min.", time="45 min"),
P(id="sisco", n="Marine de Sisco", c="beach", d=1, lat=42.811, lon=9.48852,
  f=["relax"], t="Pebble-and-sand cove where the locals swim. Good first dip after the ferry.",
  van="Roadside parking right behind the beach.", time="1 h"),
P(id="macinaggio", n="Macinaggio harbour", c="port", d=1, lat=42.95942, lon=9.45479,
  f=["relax"], t="The end of the road on the east side of the Cap. Working marina, a couple of good fish restaurants, and the trailhead for tomorrow's coastal walk.",
  van="Big flat harbour car park; the campsite is 400 m inland.", time="overnight"),

# ---- DAY 2 -------------------------------------------------------
P(id="douaniers", n="Sentier des Douaniers (Customs Officers' Path)", c="hike", d=2, lat=42.96377, lon=9.45148,
  f=["nature","relax"], vid="01:29",
  t="The best coastal walk in the north, and the video's first hike. The old customs path leaves Macinaggio and loops around the tip of the Cap past Genoese towers, the ruined Santa Maria chapel (closed, but the marker that you are nearly there), beach coves you can swim in alone, and an old shore cannon on the way back. The Tour de Santa Maria stands almost entirely in the water at high tide.",
  hike=dict(dist="10 km circular from Macinaggio (the video's route); or 5 km out-and-back to Plage de Tamarone",
            up="≈180 m", dur="1.5 h short / 3.5 h full loop", grade="Easy, but zero shade — go early"),
  van="Start from the Macinaggio marina car park. A shuttle boat (U Spinu) runs Macinaggio↔Barcaggio in summer if you want to walk it one-way.",
  time="half day"),
P(id="barcaggio", n="Barcaggio & Cala Francese", c="beach", d=2, lat=43.00611, lon=9.40216,
  f=["relax","nature"], t="The northernmost beach in Corsica — pale sand, dunes, cows that wander down onto the sand, and the Giraglia islet offshore. Feels like the edge of the map.",
  van="The D253 down to Barcaggio is narrow with passing places; fine for a van under ~6 m, unpleasant in anything bigger. Park at the village entrance.",
  time="2 h"),
P(id="mattei", n="Moulin Mattei", c="view", d=2, lat=42.97459, lon=9.3648,
  f=["nature","culture"], vid="01:29",
  t="A windmill from the end of the 18th century, struck by lightning in 1836 and never used again, now painted with the old Cap Corse Mattei aperitif advert. 360° over both coasts of the peninsula — the classic photo of the whole Cap.",
  van="Small pull-in on the D80 at the col, then a 5 min walk up the track.", time="30 min"),
P(id="centuri", n="Port de Centuri", c="town", d=2, lat=42.96058, lon=9.36824,
  f=["culture","relax"], vid="01:29",
  t="Green-serpentine houses around a doll's-house harbour. Corsica's lobster capital — this is where you spend money on lunch.",
  van="Descent is steep and tight. Park up on the D80 and walk 10 min down, or use the small harbour lot early.",
  time="1.5 h"),
P(id="nonza", n="Nonza — black beach & tower", c="town", d=2, lat=42.78441, lon=9.34459,
  f=["nature","relax","culture"], vid="01:29",
  t="The single most striking stop on Cap Corse. A village clinging to a 100 m black cliff, and below it a beach of jet-black shingle left by an old asbestos mine — 300 steps down, and the sea shelves off fast. The tower on top is square, unlike every other round Genoese tower on the Cap, and the 16th-century church is dedicated to Santa Giulia, patron saint of Corsica.",
  van="Village car park on the D80 (paid in season). Do the tower first for the view straight down, then the steps.",
  time="2 h"),
P(id="patrimonio", n="Patrimonio vineyards", c="culture", d=2, lat=42.70074, lon=9.36452,
  f=["culture","relax"], t="Corsica's oldest AOC. Schist slopes, Niellucciu reds and mineral whites; several domaines do walk-in tastings — Domaine Gentile, Clos Marfisi, Antoine Arena.",
  van="Wide gravel yards at most domaines. Obvious but: whoever drives, spits.", time="1–2 h"),

# ---- DAY 3 -------------------------------------------------------
P(id="stflorent", n="Saint-Florent", c="town", d=3, lat=42.68129, lon=9.3025,
  f=["culture","relax"], t="The 'Corsican Saint-Tropez', but still small. Not a watchtower this time but a real fort — the citadel was built in 1440 — plus a quay of restaurants and the boats out to the Agriates beaches.",
  van="Two campsites within 2 km and a service point at the port. Provision here — it's the last real supermarket before the Agriates.",
  time="2 h"),
P(id="vezzu", n="Bocca di Vezzu", c="view", d=3, lat=42.66591, lon=9.14144,
  f=["nature"], vid="08:32",
  t="The pass on the D81 where the Désert des Agriates suddenly opens out below you — scrubland running down to a bright blue gulf. Straight from the video.",
  van="Layby at the col, big enough for a van. Best light late afternoon.", time="20 min"),
P(id="lotu", n="Plage du Lotu", c="beach", d=3, lat=42.71989, lon=9.23317,
  f=["relax","nature"], t="White sand, shallow water, no road. Reachable by shuttle boat from Saint-Florent (25 min) or on foot from the Saleccia track.",
  van="No van access — take the Popeye/Le Petit Train boat from Saint-Florent. Book the day before in July/August.",
  time="half day"),
P(id="saleccia", n="Plage de Saleccia", c="beach", d=3, lat=42.72674, lon=9.20555,
  f=["relax","nature"], t="A kilometre of Caribbean-white sand behind a pine forest, in the middle of a desert. Used as the D-Day beach in *The Longest Day*. The best beach in northern Corsica, full stop.",
  van="Do NOT drive the 12 km Casta piste in your own van — it is a rock-strewn 4x4 track and rental contracts void on it. Either the boat from Saint-Florent, or the 4x4 shuttle from Casta. There is one campsite behind the beach (U Paradisu) if you want to sleep there.",
  time="full day"),
P(id="ostriconi", n="Plage de l'Ostriconi", c="beach", d=3, lat=42.66241, lon=9.06103,
  f=["nature","relax"], t="Where a river meets the sea at the far end of the Agriates: dunes, a lagoon, and the mouth of a valley. Wilder and emptier than anything in the Balagne, and reachable without a boat.",
  hike=dict(dist="1.6 km round trip from the car park", up="60 m", dur="35 min", grade="Easy, sandy"),
  van="Park at the signed lot off the N1197; 15 min walk down through the dunes. Big-van friendly.",
  time="3 h"),

# ---- DAY 4 -------------------------------------------------------
P(id="lozari", n="Plage de Lozari", c="beach", d=4, lat=42.64316, lon=9.01937,
  f=["relax"], vid="08:32",
  t="Long, gently curving grey-gold bay at the start of the Balagne. Shallow and safe, with a couple of beach bars. Walk the sand to the rocky end and climb the staircase to the ruined lookout tower above — the contrast of coast against the mountains behind is the shot from the video.",
  van="Large car park behind the beach; two campsites within 1 km.", time="half day"),
P(id="ilerousse", n="L'Île-Rousse", c="town", d=4, lat=42.63448, lon=8.93814,
  f=["culture","relax"], vid="09:55",
  t="Founded by Pascal Paoli to spite Genoese Calvi. The 19th-century covered market hall is a monument in its own right and still trades most mornings — charcuterie, brocciu, chestnut flour. Then cross the causeway onto the red rocks of Île de la Pietra, where a path runs out to the 1857 lighthouse and an old watchtower.",
  van="Aire de camping-car near the port, plus paid parking on the seafront. Market for charcuterie, brocciu and tomatoes.",
  time="3 h"),
P(id="pigna", n="Pigna", c="town", d=4, lat=42.59899, lon=8.90294, vid="11:08",
  f=["culture"], t="Blue-shuttered, cobbled, and almost too perfect — a village rebuilt around craft workshops and Corsican polyphonic music. Instrument makers, a music box shop, and the Casa Musicale for an evening concert.",
  van="Skip the coastal N197 to Calvi and take the higher inland road as the video does — it strings together the Balagne villages and the Corbara monastery. Park in the lot below Pigna and walk up; the lanes are pedestrian.",
  time="1.5 h"),
P(id="santantonino", n="Sant'Antonino", c="town", d=4, lat=42.5889, lon=8.90499,
  f=["culture","nature"], t="One of the oldest inhabited villages in Corsica, a 9th-century eagle's nest on a granite cone. Vaulted stone passageways and a view over the whole Balagne to the sea.",
  van="Car park at the bottom, unavoidable steep 10 min climb.", time="1 h"),
P(id="bodri", n="Plage de Bodri", c="beach", d=4, lat=42.62999, lon=8.91425,
  f=["relax","nature"], t="Pale sand and clear shallow water between rocky points, backed by pines and reached on foot. Better swimming than Lozari and prettier than the town beaches.",
  van="Park at Camping Le Bodri / the signed lot off the N197, then 10 min through the maquis.", time="half day"),

# ---- DAY 5 -------------------------------------------------------
P(id="calvi", n="Calvi — Citadelle & the bay", c="town", d=5, lat=42.56766, lon=8.75887, vid="12:08",
  f=["culture","relax"], t="Roman in origin, Genoese in character: the 13th-century citadel that made Calvi their island stronghold still dominates the skyline. A marina full of masts below, and a 4 km crescent of sand backed by umbrella pines running south. The most complete 'town + beach' day of the trip.",
  van="Park at the Port de Plaisance or the station lot. Bring the van nowhere near the citadel ramp.",
  time="half day"),
P(id="figarella", n="A Figarella river pools, Bonifatu", c="swim", d=5, lat=42.44338, lon=8.8529, vid="13:07",
  f=["nature","relax"], t="The video's second hike, and the one to copy: the first half follows the Figarella river past small waterfalls, the second climbs into the mountains with the Bonifatu range opening up. Granite slabs and deep green plunge pools all the way along — do it in good weather and swim at the turnaround.",
  hike=dict(dist="5 km round trip (the video's route)", up="300 m", dur="2–2.5 h plus swimming",
            grade="Easy–moderate; riverside then rocky"),
  van="Road up from Calenzana is narrow but paved to the Auberge de la Forêt de Bonifatu car park. Fine for a van under ~6.5 m.",
  time="half day"),
P(id="bonifatu", n="Cirque de Bonifatu / Refuge de Carrozzu", c="hike", d=5, lat=42.42598, lon=8.90098,
  f=["nature"], t="A proper mountain hike out of the Bonifatu forest into a red-rock cirque, on a variant of the GR20. The Spasimata suspension bridge above the river is the payoff.",
  hike=dict(dist="11 km round trip to Refuge de Carrozzu", up="750 m", dur="5–6 h", grade="Hard — rocky, some scrambling"),
  van="Park at the Auberge de la Forêt de Bonifatu (paid). Start before 08:00 in summer.", time="full day"),
P(id="calenzana", n="Calenzana — km 0 of the GR20", c="town", d=5, lat=42.51046, lon=8.85082,
  f=["culture","nature"], t="Stone village at the foot of the mountains where Europe's toughest waymarked trail begins. Worth a coffee on the square just to watch the GR20 hopefuls set off looking optimistic.",
  van="Village car park; gîte d'étape has a service point.", time="1 h"),

# ---- DAY 6 -------------------------------------------------------
P(id="galeria", n="Galéria & the Fango valley", c="town", d=6, lat=42.40848, lon=8.64792,
  f=["nature","relax"], t="A single-street village at the mouth of the Fango, inside the Scandola biosphere reserve. The Fango river upstream has enormous natural swimming pools.",
  van="Small campsites and a beach car park. Last fuel for a while — fill up.", time="2 h"),
P(id="senino", n="Monte Senino viewpoint", c="view", d=6, lat=42.31641, lon=8.61077, vid="14:13",
  f=["nature"], t="The video's big reveal, and its toughest short climb. The summit sits between the Gulf of Girolata and the Gulf of Porto, so you get both bays and the whole Scandola reserve in one turn of the head. Same path up and down; the many steep pitches are what eat the time, not the distance.",
  hike=dict(dist="6 km round trip", up="≈500 m", dur="about 4 h", grade="Hard — relentlessly steep, no shade"),
  van="Trailhead is the big roadside car park on the D81 by the village of Osani (42.324, 8.632). Leave the van there — do not drive the track. Start early or go for sunset.",
  time="half day"),
P(id="scandola", n="Réserve Naturelle de Scandola", c="nature", d=6, lat=42.35688, lon=8.56134,
  f=["nature"], t="UNESCO-listed volcanic coast: red porphyry cliffs, sea caves, ospreys. Only reachable by boat — the small-boat trips from Porto or Galéria that go into the caves are worth the money.",
  van="Boats leave from Porto marina (3–4 h trip, usually with a Girolata stop). Book a day ahead.", time="half day"),
P(id="girolata", n="Girolata", c="hike", d=6, lat=42.34969, lon=8.61245,
  f=["nature","relax"], t="A hamlet with no road to it at all — supplies come by boat. Reached on the old mule path from the Col de la Croix, and the best kind of lunch: nowhere else to be.",
  hike=dict(dist="7 km round trip from Col de la Croix", up="380 m", dur="3 h", grade="Moderate; steep on the way back up"),
  van="Park at the Col de la Croix layby on the D81. Or arrive by boat and walk out.", time="half day"),
P(id="porto", n="Porto & the Genoese tower", c="town", d=6, lat=42.26732, lon=8.69633, vid="16:22",
  f=["relax","culture"], t="Base camp for the west coast, and a village of fewer than 500 people. A Genoese tower on a red rock that you can climb for a couple of euros, a wooden footbridge over the river mouth, a eucalyptus-lined marina, and a pebble beach that turns molten at sunset. Boat trips and watersports all leave from here.",
  van="Three campsites in the valley, all van-friendly with service points. Supermarket and laundry in the village.",
  time="overnight"),
P(id="pianella", n="Pont de Pianella & Gorges de la Spelunca", c="swim", d=6, lat=42.25633, lon=8.7612, vid="16:22",
  f=["nature","relax"], t="A perfect 15th-century Genoese arch over green water, at the entrance to the Spelunca gorge. The pools under the bridge are deep enough to jump into.",
  hike=dict(dist="7 km one-way Ota → Évisa on the old mule track", up="600 m", dur="3.5 h", grade="Moderate; paved-slab path, hot"),
  van="Layby on the D124 between Ota and Évisa, 2 min walk to the bridge.", time="2 h"),

# ---- DAY 7 -------------------------------------------------------
P(id="calanches", n="Les Calanches de Piana", c="view", d=7, lat=42.241, lon=8.65242, vid="18:27",
  f=["nature","culture"], t="A UNESCO site and the reason people come to Corsica: wind-eaten orange granite towers rising as much as 400 m straight out of the sea. Drive it once, then walk it — the shapes only work on foot. Time it for sunset, as the video does; the rock goes from orange to blood red.",
  hike=dict(dist="Château Fort loop 2.5 km / Tête de Chien 1.5 km", up="150 m", dur="1–2 h", grade="Easy–moderate, rocky"),
  van="THE PINCH POINT OF THE WHOLE TRIP. The D81 through the Calanches is single-lane in places with rock overhangs and 300 m drops. Vans over ~6 m or 3 m high should not attempt it; anything up to a VW/Ducato size is fine but drive it early morning or after 18:00, never at 11:00 with the tour buses.",
  time="half day"),
P(id="piana", n="Piana village", c="town", d=7, lat=42.23887, lon=8.63706,
  f=["culture","relax"], t="One of France's officially 'most beautiful villages', on a balcony above the gulf. Church square, a couple of good terraces, and the view that put the Calanches on posters.",
  van="Village car park on the D81; fill water here.", time="1.5 h"),
P(id="caporosso", n="Capo Rosso / Tour de Turghiu", c="hike", d=7, lat=42.23525, lon=8.58349, vid="19:03",
  f=["nature"], t="The signature hike of the west coast and, in the video's words, one of the most beautiful walks on the island. A stony path out along a red headland to the Tour de Turghiu, one of the highest Genoese towers on the Corsican coast, with the Calanches behind you and open sea on three sides. The last climb to the tower is the hard bit.",
  hike=dict(dist="8.5 km round trip", up="≈500 m", dur="3–4 h", grade="Hard — fairly challenging, strenuous final climb, no shade at all: 2 L of water each"),
  van="Signed layby on the D824 towards Arone — room for a few vans. Do it at first light as the video did and you will have the tower to yourself.",
  time="half day"),
P(id="arone", n="Plage d'Arone", c="beach", d=7, lat=42.20723, lon=8.58014,
  f=["relax","nature"], t="The reward after Capo Rosso: a wide sandy bay at the end of a dead-end road, so it never gets truly crowded. One beach bar, clear water, good sunsets.",
  van="Beach car park plus a seasonal campsite right behind the sand. The D824 in is windy but wide enough.",
  time="half day"),

# ---- DAY 8 -------------------------------------------------------
P(id="ota", n="Ota", c="town", d=8, lat=42.25783, lon=8.74506,
  f=["culture"], t="Grey stone village pinned under a rock face above the Spelunca. Two gîtes, one bar, and a proper mountain-Corsica feel five minutes off the coast road.",
  van="Tight village; park at the entrance.", time="45 min"),
P(id="evisa", n="Évisa & the chestnut forests", c="town", d=8, lat=42.25349, lon=8.80302,
  f=["nature","culture"], t="Chestnut country — the far end of the Spelunca gorge walk, and the place to eat *pulenta* made from chestnut flour.",
  van="Roadside parking; the D84 from here up to Vergio is wide and beautiful.", time="1 h"),
P(id="cristinacce", n="Cristinacce", c="town", d=8, lat=42.23904, lon=8.84088, vid="20:51",
  f=["culture","nature"], t="A handful of houses on a spur with a huge view back down the valley. In the video it's the moment the trip turns from coast to mountain.",
  van="Small layby below the village.", time="30 min"),
P(id="vergio", n="Col de Vergio (1,478 m)", c="view", d=8, lat=42.29032, lon=8.8784, vid="21:28",
  f=["nature"], t="The highest road pass in Corsica, reached on the D84 from Évisa. You'll know it by the 6 m statue of Christ the King raised on the col in 1984, and the laricio pines. Gateway to the Niolu, and a serious change of climate — bring a fleece.",
  van="Big car park at the ski station / Castel de Vergio. Free overnight parking is often tolerated here at altitude.",
  time="1 h"),
P(id="nino", n="Lac de Nino", c="hike", d=8, lat=42.25517, lon=8.94052,
  f=["nature"], t="A high glacial lake in a plain of *pozzines* — spongy green turf laced with streams, with half-wild horses and pigs grazing. The most otherworldly place on the island.",
  hike=dict(dist="9 km round trip from Fer à Cheval", up="600 m", dur="4–5 h", grade="Moderate; boggy near the top"),
  van="Park at the Fer à Cheval hairpin on the D84 east of Vergio. Do not camp at the lake — it is protected.",
  time="full day"),
P(id="calacuccia", n="Lac de Calacuccia", c="swim", d=8, lat=42.32758, lon=9.0145, vid="22:02",
  f=["relax","nature"], t="A turquoise reservoir created by the 1960 dam, with the 2,706 m wall of Monte Cinto behind it. Swim from the shore near the bridge, then eat in Calacuccia village. The Golo leaves the lake straight into the Canyon di A Ruda.",
  van="Several laybys around the lake road; two campsites on the north shore.", time="half day"),
P(id="aruda", n="Canyon di A Ruda", c="swim", d=8, lat=42.32782, lon=8.98419, vid="22:02",
  f=["nature","relax"], t="Where the Golo leaves the Calacuccia lake it cuts a deep, narrow ravine with sheer walls, and a winding single-track road threads through it — one of the best short drives on the island. Sculpted granite chutes and pools at the bottom: waterslides in early summer, calm swimming holes by August.",
  van="Narrow and twisting with drops; fine for a van taken slowly. Laybys give access to the river — wear something on your feet to scramble down.",
  time="2–3 h"),

# ---- DAY 9 -------------------------------------------------------
P(id="scala", n="Scala di Santa Regina", c="view", d=9, lat=42.3581, lon=9.05915,
  f=["nature"], t="A raw red granite gorge carved by the Golo, with the old mule 'staircase' still visible across the water. Utterly bare, and the sort of driving that makes the trip.",
  van="The D84 is good tarmac but narrow with rock walls — no problem for a normal van, take the corners wide.",
  time="45 min"),
P(id="asco", n="Gorge de l'Asco", c="view", d=9, lat=42.41485, lon=8.94533, vid="44:38",
  f=["nature"], t="A dead-end valley that feels forgotten: 20 km of gorge with mouflon on the crags, ending under the north face of Monte Cinto.",
  van="25 km of road to the roadhead and — unlike the Restonica — completely intact. The D147 narrows to single-track with passing bays for the last 10 km. Doable in a van; slow and gorgeous.",
  time="2 h"),
P(id="hautasco", n="Haut-Asco (1,450 m) & Punta Muvrella", c="hike", d=9, lat=42.40329, lon=8.92356, vid="44:38",
  f=["nature"], t="An abandoned ski station at the roadhead that is now purely a GR20 waypoint. The climb to Punta di la Muvrella gets you a view over the Cinto massif and, on a clear day, the sea on both sides.",
  hike=dict(dist="8 km round trip", up="850 m", dur="5 h", grade="Hard; rocky and steep, GR20 red-and-white waymarks"),
  van="Large flat gravel car park at the roadhead, refuge with showers and a bar. One of the best free van nights on the island.",
  time="full day"),
P(id="corte", n="Corte — Citadelle & the old town", c="town", d=9, lat=42.30529, lon=9.15119, vid="40:00",
  f=["culture"], t="Capital of Corsica during the brief 18th-century republic, and still the island's university town. The citadel stands on a crag straight above the roofs with a view over the whole mountain bowl; below it, the Museu di a Corsica, steep lanes and student bars. The most Corsican town on the island, and the cheapest.",
  van="Parking at the bottom of the old town; three campsites within 2 km on the Restonica road. Restock and do laundry here.",
  time="half day"),

# ---- DAY 10 ------------------------------------------------------
P(id="restonica", n="Gorges de la Restonica", c="swim", d=10, lat=42.24828, lon=9.05657,
  f=["nature","relax"], t="A pine gorge above Corte with a chain of clear pools in white granite, and the way in to the island's most famous hike. The lower valley still has swimming laybys within easy reach of Corte; the water is snowmelt-cold into June.",
  van="READ THIS BEFORE YOU PLAN DAY 10. The storms of November 2023 destroyed the upper D623: bridges collapsed and long sections were shattered by rockfall, and the road is shut beyond the Pont de Tragone, 10 km up. You cannot drive to the Bergeries de Grotelle any more. The trailhead is now the A Frasseta car park, served from 2 May to 30 September by the Navetta Restonica C13 shuttle from Corte station — €4 return, booking compulsory in the M-Ticket Via Corsica Restonica app, no cash and no on-board sales. Re-check the status at the Corte tourist office when you arrive; this is an active repair site.",
  time="half day"),
P(id="melo", n="Lac de Melo & Lac de Capitello", c="hike", d=10, lat=42.21296, lon=9.02266, vid="40:00",
  f=["nature"], t="The most famous hike in Corsica, and since the road collapsed, a serious mountain day rather than a stroll. From the A Frasseta barrier you walk the broken road up the valley — collapsed bridges, rock-shattered tarmac — to the abandoned Bergeries de Grotelle, where one small bar still opens daily for food and drink. Only then does the real climb start: chains and rock steps up to Melo at 1,711 m, and a steeper 45 minutes more to Capitello, a black lake under a granite cirque that holds ice into June. The video's version was over 25 km and eight hours door to door.",
  hike=dict(dist="25+ km round trip from A Frasseta (much less if the shuttle runs higher — verify locally)",
            up="≈1,400 m as walked in the video", dur="8+ h — a full day", grade="Hard — long approach, fixed chains near the lake, alpine weather"),
  van="Take the Navetta C13 from Corte station (see the Restonica entry) and be on the trail at first light. Leave the van at the campsite in Corte. Carry 2–3 L, food, a windproof layer and a head torch — this is a much bigger day than any guidebook written before 2024 suggests.",
  time="full day"),
P(id="vizzavona", n="Vizzavona & the Cascade des Anglais", c="hike", d=10, lat=42.12858, lon=9.13376,
  f=["nature","relax"], t="Beech and laricio forest at 900 m with a tiny railway halt, cut through by the Agnone's waterfalls and pools. The easiest genuinely beautiful walk on the island, and blissfully cool in August.",
  hike=dict(dist="5 km round trip from the Col de Vizzavona", up="250 m", dur="2 h", grade="Easy; GR20 waymarks"),
  van="Park at La Foce / Col de Vizzavona on the N193. Big laybys, shade, and a campsite 3 km away.",
  time="half day"),

# ---- DAY 11 ------------------------------------------------------
P(id="spusata", n="Cascata di u Velu di a Spusata (Bridal Veil Falls)", c="swim", d=11, lat=42.064, lon=9.05138, vid="35:45",
  f=["nature"], t="A 150 m fall spilling down a granite face above Bocognano, at its most dramatic in May and June with the snowmelt. The video's stop; a 20 min walk gets you to the base.",
  hike=dict(dist="1.5 km round trip", up="100 m", dur="40 min", grade="Easy"),
  van="Signed parking off the N193 just north of Bocognano.", time="1.5 h"),
P(id="tolla", n="Lac de Tolla", c="swim", d=11, lat=41.96817, lon=8.97132, vid="36:07",
  f=["relax","nature"], t="An emerald reservoir in the Prunelli gorges, half an hour from Ajaccio and almost empty. Swimming, a lakeside restaurant, and kayaks for rent.",
  van="The D3 in from Bastelicaccia is narrow and twisting with drops — slow going, but fine for a van. Laybys with lake views all along.",
  time="half day"),
P(id="ajaccio", n="Ajaccio — old town & the market", c="town", d=11, lat=41.9264, lon=8.7376, vid="36:42",
  f=["culture","relax"], t="Founded in 1492, the island's capital and Napoleon's birthplace. 70,000 people and still somehow doesn't feel like a city: an ochre old town, the Maison Bonaparte, the Fesch museum's Italian paintings, and a genuinely excellent morning market on the Place Foch.",
  van="Do not drive into the centre. Park at the Parking Diamant or the port and walk. Two campsites south towards Porticcio.",
  time="half day"),
P(id="sanguinaires", n="Îles Sanguinaires & Pointe de la Parata", c="view", d=11, lat=41.87801, lon=8.59343, vid="37:21",
  f=["nature","relax"], t="The sunset of the trip. A chain of red islets off a headland with a Genoese tower, and a coast road out of Ajaccio lined with swimming coves. Walk the Parata loop and stay for the light.",
  hike=dict(dist="1.5 km loop around the Pointe de la Parata", up="60 m", dur="45 min", grade="Easy, paved"),
  van="Large paid car park at the Parata (closes in the evening in season — check the barrier time before you commit to sunset).",
  time="3 h"),

# ---- DAY 12 ------------------------------------------------------
P(id="filitosa", n="Filitosa", c="heritage", d=12, lat=41.7444, lon=8.87094,
  f=["culture","nature"], t="The best prehistoric site in Corsica: 4,000-year-old carved menhirs with faces and swords, in an olive grove by a stream. Small, quiet, and genuinely moving.",
  van="Own car park, easy access off the N196. Allow 1.5 h with the little museum.", time="2 h"),
P(id="propriano", n="Propriano & the Golfe de Valinco", c="town", d=12, lat=41.6759, lon=8.90404,
  f=["relax","culture"],
  t="The port on the Gulf of Valinco, and the obvious place to break the long run south — a working marina, a promenade of restaurants, and fine white-sand beaches either side of town facing west, so the sunsets are the best on this coast.",
  van="Free parking along the seafront and a service point at the marina. Two supermarkets, which makes this the restock point between Ajaccio and Bonifacio.",
  time="2 h"),
P(id="sartene", n="Sartène", c="town", d=12, lat=41.62088, lon=8.97219,
  f=["culture"], t="Prosper Mérimée called it 'the most Corsican of Corsican towns' and it still is — grey granite, vaulted passages, shuttered windows and a slightly forbidding beauty. Base for the Rizzanese wines.",
  van="Park below the Place Porta; the old town is stairs only.", time="2 h"),
P(id="stelucie", n="Sainte-Lucie-de-Tallano", c="town", d=12, lat=41.69765, lon=9.06404, vid="30:45",
  f=["culture","relax"], t="An Alta Rocca village of olive oil and diorite quarries, with a shaded square, a working oil mill and the Genoese Spin'a Cavallu bridge nearby.",
  van="Village car park at the entrance. Buy the olive oil.", time="1.5 h"),
P(id="roccapina", n="Plage de Roccapina & the Lion", c="beach", d=12, lat=41.49582, lon=8.93471,
  f=["nature","relax"], t="A white crescent under a granite outcrop shaped exactly like a crouching lion, with a Genoese tower on top. No development at all.",
  van="The 3.5 km track down from the N196 is rough and rutted — passable slowly in a high-clearance van, but many people park at the top layby and walk 45 min down. Judge it on the day.",
  time="half day"),
P(id="bonifacio", n="Bonifacio — the Haute Ville on the cliffs", c="town", d=12, lat=41.38723, lon=9.15906, vid="31:19",
  f=["culture","nature"], t="The showstopper, and only 12 km from Sardinia. A fortified white town on limestone cliffs undercut by the sea, a fjord-like harbour, and a citadel whose origins go back to the 9th century. The Escalier du Roi d'Aragon drops 187 steps carved into the cliff face — legend says Aragonese troops cut them in a single night in 1420. Take the clifftop viewpoints on the south side of the citadel at dusk, once the day-trippers have gone.",
  van="Park at the top (Parking de la Citadelle / Parking Vallée) and walk — the Haute Ville is not driveable. Four campsites on the Santa Manza road.",
  time="full day"),

# ---- DAY 13 ------------------------------------------------------
P(id="lavezzi", n="Îles Lavezzi", c="beach", d=13, lat=41.36757, lon=9.2647,
  f=["nature","relax"], t="A granite archipelago in the Strait of Bonifacio — boulders, a marine reserve, and water so clear the boat looks like it's floating on air. Bring everything; there is nothing on the island.",
  van="Boats from Bonifacio marina (2–3 sailings a day, ~€35). Leave the van in the harbour lot.", time="full day"),
P(id="rondinara", n="Plage de Rondinara", c="beach", d=13, lat=41.46885, lon=9.26647,
  f=["relax","nature"], t="An almost perfectly circular bay closed by two headlands — shallow, sheltered, blue-green, and the best swim of the south coast.",
  van="4 km paved side road off the N198, then a big car park (paid in season). Campsite right behind the beach.",
  time="half day"),
P(id="santagiulia", n="Plage de Santa Giulia", c="beach", d=13, lat=41.5275, lon=9.27216, vid="29:19",
  f=["relax"], t="Voted one of the most beautiful beaches in France, and it earns it: a horseshoe bay of white sand with translucent water that stays waist-deep for fifty metres, closed by low hills. The video's reward after Bavella, and yours too. Busy and commercial in August, sublime in June or September.",
  van="Several car parks behind the beach; watch the height barriers at the private ones. Go early.",
  time="half day"),
P(id="palombaggia", n="Plage de Palombaggia & Tamaricciu", c="beach", d=13, lat=41.5561, lon=9.3218,
  f=["relax","nature"], t="Red rocks, umbrella pines leaning over pale sand, and the Cerbicale islands offshore. The most photographed beach in Corsica; walk south to Tamaricciu for more room.",
  van="Roadside paid parking along the whole strip — arrive before 10:00 or after 16:00. Overnighting on the beach road is actively policed.",
  time="half day"),
P(id="portovecchio", n="Porto-Vecchio old town", c="town", d=13, lat=41.59114, lon=9.27945,
  f=["culture","relax"], t="Genoese salt town turned resort, but the walled upper town is still charming at night — the Porte Génoise, the Place de la République, and a good evening restaurant scene.",
  van="Park at the port and walk up. Best supermarkets and gas refills in the south.", time="3 h"),

# ---- DAY 14 ------------------------------------------------------
P(id="ospedale", n="Forêt & Lac de l'Ospedale", c="view", d=14, lat=41.66849, lon=9.20744,
  f=["nature","relax"], t="900 m up from the beaches into pine forest and granite boulders, with a reservoir and a 15° temperature drop. The escape valve when the coast gets too hot.",
  van="Plenty of forest laybys on the D368; a gîte and restaurants at the hamlet.", time="2 h"),
P(id="piscia", n="Piscia di Gallu waterfall", c="hike", d=14, lat=41.68696, lon=9.26246,
  f=["nature"], t="A 60 m fall dropping off a granite lip into a chasm below the Ospedale dam. The path in over slabs and through boulders is half the fun.",
  hike=dict(dist="3.5 km round trip", up="200 m", dur="1.5–2 h", grade="Moderate; slippery granite slabs, proper shoes"),
  van="Signed car park with a snack bar on the D368. Best flow in May–June; can be a trickle in August.",
  time="half day"),
P(id="carbini", n="Carbini — San Giovanni Battista", c="heritage", d=14, lat=41.67908, lon=9.14696, vid="29:56",
  f=["culture"], t="A small village at the foot of a hillock, with a view over its own rooftops to the southern mountains. Its 11th–12th-century Romanesque church and detached bell tower, in banded stone, are among the purest medieval buildings in Corsica.",
  van="Roadside parking in the tiny village.", time="45 min"),
P(id="cucuruzzu", n="Casteddu di Cucuruzzu & Capula", c="heritage", d=14, lat=41.71826, lon=9.12867,
  f=["culture","nature"], t="A Bronze Age fortified site inside a holm-oak wood near Levie, with a medieval castle next door. Walked with an audioguide through the trees — a good hot-afternoon alternative.",
  van="Own car park at the site, off the D268.", time="2 h"),
P(id="bavella", n="Col de Bavella (1,218 m)", c="view", d=14, lat=41.79587, lon=9.22496, vid="26:30",
  f=["nature"], t="The mountain heart of the south, and the single most spectacular massif on the island: seven red granite needles, some reaching 1,800 m, above a pass with a Notre-Dame-des-Neiges statue, wind-twisted pines and grazing pigs. Sunrise here is the best in Corsica.",
  van="Large gravel car parks either side of the col, two auberges. The D268 up from Solenzara is a spectacular, narrow, hairpinned climb — go up in the morning, and take it slowly in a van.",
  time="half day"),
P(id="aiguilles", n="Aiguilles de Bavella & the Trou de la Bombe", c="hike", d=14, lat=41.80339, lon=9.21456, vid="27:38",
  f=["nature"], t="Two options from the col. The Trou de la Bombe is an easy walk to a huge wind-blown hole punched clean through a rock wall. The Alpine variant of the GR20 is the one in the video and the one worth the effort: a loop right under the needles, alternating jagged peaks, forest and panoramas, with sections where you climb on fixed chains. The narrator rates it among the most beautiful hikes he has ever done.",
  hike=dict(dist="Trou de la Bombe 6 km round trip; Alpine loop ≈12 km",
            up="300 m / ≈1,000 m", dur="2.5 h / about 4 h", grade="Easy–moderate / Hard, exposed scrambling on fixed chains"),
  van="Both start at the Col de Bavella car parks. Storms build fast here in the afternoon — start early.",
  time="full day"),
P(id="zonza", n="Zonza", c="town", d=14, lat=41.74937, lon=9.17064,
  f=["culture","nature"], t="Granite mountain village under the Bavella needles, all hotels, hiking shops and cold beer. Your base for the Alta Rocca.",
  van="Village car parks, two campsites nearby, service point at the municipal site.", time="overnight"),

P(id="d1d4", n="The D1 & D4 mountain crossing", c="view", d=11, lat=41.95283, lon=8.7808, vid="38:16",
  f=["nature"], t="The video calls the narrow D4 one of the most beautiful roads on the island, and it is: from the outskirts of Ajaccio the D1 runs north, then the D4 threads a tight pass through the massif with the mountains stacked up on every side. No coaches, no traffic, nothing but road.",
  van="Genuinely narrow with unguarded edges — perfectly driveable in a normal van, but not something to rush or to do in the dark. Allow double the time the map claims.",
  time="2–3 h"),

# ---- DAY 15 ------------------------------------------------------
P(id="solenzara", n="Solenzara", c="beach", d=15, lat=41.85628, lon=9.39857,
  f=["relax"], t="Where the Bavella road hits the sea. Long pebble-sand beaches, river pools upstream on the Solenzara, and the last easy swim of the trip.",
  van="Big campsites north and south of town, plus a service point at the marina.", time="2 h"),
P(id="ghisoni", n="Ghisoni & the D69", c="view", d=15, lat=42.10356, lon=9.21228, vid="33:32",
  f=["nature"], t="The video's hidden gem: the D69 climbing from the coast past the Christe Eleison and Kyrie Eleison peaks to Corsica's ski station at 1,600–1,900 m under Monte Renoso. Deserted out of season and all the better for it — in spring the peaks still carry snow. Nobody drives this road; the drive itself is the attraction.",
  van="Narrow but paved with passing places. There is a spring at the village and free forest parking near the ski station.",
  time="half day"),
P(id="aleria", n="Situ Archeologicu d'Aleria", c="heritage", d=15, lat=42.11357, lon=9.51447, vid="25:23",
  f=["culture"], t="Founded by the Greeks in the 6th century BC and taken by Rome three centuries later, Aleria became the capital of the Roman province of Corsica et Sardinia. The forum, baths and temple platforms sit on a hill above a lagoon, with an excellent little museum in the Genoese Fort de Matra. The video's rainy-day plan, and a good one.",
  van="Own car park by the Fort de Matra. Good oyster shacks on the Étang de Diane 2 km away.", time="2 h"),
P(id="campi", n="Campi", c="town", d=15, lat=42.27125, lon=9.42283, vid="24:56",
  f=["culture"], t="One street on a hilltop in the east, with a 17th-century church at the end of it and a view over the ridges. Half the houses are shuttered and empty — the quiet crisis of inland Corsica, and part of why the place still feels unspoilt.",
  van="Park at the village entrance; the street is one van wide and there is nowhere to turn.", time="45 min"),
P(id="orezza", n="Couvent d'Orezza & the Castagniccia", c="heritage", d=16, lat=42.37439, lon=9.36813, vid="23:32",
  f=["culture","nature"], t="Founded in 1485 and for centuries the spiritual centre of the Castagniccia, damaged and rebuilt again and again, then abandoned at the French Revolution. The roofless shell standing in chestnut forest is genuinely eerie. The D71 through the Castagniccia is a slow, green, wonderful detour if you have a spare half day before the ferry.",
  van="The D71 is genuinely narrow and twisty; only worth it in a smaller van, and allow twice the time the map suggests.",
  time="half day"),
]

# ---------------------------------------------------------------- CAMPSITES (curated from OSM, verified coords)
CHECKIN_CAMP = "Reception typically 08:00–12:00 and 15:00–19:30; earlier at altitude and out of season."

CAMPS = [
 dict(id="c-stazzu", n="Camping U Stazzu", lat=42.96439, lon=9.44788, d=1, w="https://camping-u-stazzu.jimdo.com",
      t="Simple, shaded, 400 m from Macinaggio harbour and the start of the Sentier des Douaniers.", price="€€", mh=True),
 dict(id="c-pietra", n="Camping La Pietra", lat=42.84011, lon=9.47332, d=1, w="https://www.la-pietra.com/",
      t="Terraced pitches above the sea on the Cap Corse east coast; good fallback if you stop short of Macinaggio.", price="€€", mh=True),
 dict(id="c-solemarinu", n="Camping U Sole Marinu", lat=42.71786, lon=9.33009, d=2, w="https://www.usolemarinu.com",
      t="On the Gulf of Saint-Florent under the Patrimonio vines. Big pitches, easy access for a long van.", price="€€", mh=True),
 dict(id="c-tollare", n="Tollare camper aire", lat=43.00577, lon=9.38547, d=2, w=None,
      t="Bare-bones motorhome aire at the very tip of the Cap — no frills, unbeatable position.", price="€", mh=True),
 dict(id="c-kalliste", n="Camping Kalliste", lat=42.67371, lon=9.29781, d=3, w="https://www.camping-saintflorent.com",
      t="Walking distance into Saint-Florent, shaded by eucalyptus, service point and pool.", price="€€", mh=True),
 dict(id="c-ostriconi", n="Village de l'Ostriconi", lat=42.65547, lon=9.0681, d=3, w="https://www.village-ostriconi.com/",
      t="Big terraced site at the Agriates end, 15 min walk from the wild Ostriconi beach. The best-placed site in the north.", price="€€", mh=True),
 dict(id="c-bodri", n="Camping Le Bodri", lat=42.62643, lon=8.91494, d=4, w="https://www.campinglebodri.com",
      t="Pine shade, direct path to Bodri beach, halfway between Île-Rousse and the Balagne villages.", price="€€", mh=True),
 dict(id="c-closdeschenes", n="Camping Le Clos des Chênes", lat=42.63297, lon=9.0119, d=4, w="https://www.le-closdeschenes.com/",
      t="Roomy oak-shaded pitches near Lozari beach; quieter than the Île-Rousse strip.", price="€€", mh=True),
 dict(id="c-bellavista", n="Camping Bella Vista", lat=42.55175, lon=8.7549, d=5, w="https://www.camping-calvi-bellavista.com/",
      t="Behind the Calvi pine beach, walkable into town and to the citadel. Fills fast in August.", price="€€", mh=True),
 dict(id="c-paradella", n="Camping Paradella", lat=42.50368, lon=8.78952, d=5, w="https://www.camping-paradella.fr",
      t="Eucalyptus and pines between Calvi and Calenzana — the practical base for the Bonifatu hikes.", price="€€", mh=True),
 dict(id="c-solevista", n="Camping Sole e Vista", lat=42.26376, lon=8.71158, d=6, w="https://www.camping-sole-e-vista.fr/",
      t="Terraced above Porto with a big view; direct back gate into the village. Reliable water and dump point.", price="€€", mh=True),
 dict(id="c-oliviersporto", n="Camping Les Oliviers, Porto", lat=42.26182, lon=8.71235, d=6, w=None,
      t="Riverside pitches under olives with a pool and a good restaurant; the most comfortable option in Porto.", price="€€€", mh=True),
 dict(id="c-arone", n="Camping Plage d'Arone", lat=42.21142, lon=8.58462, d=7, w=None,
      t="Seasonal site 300 m from the sand at Arone — sleep, swim, repeat. High season only.", price="€€", mh=True),
 dict(id="c-montecintu", n="Camping Monte Cintu", lat=42.34924, lon=9.0092, d=8, w="https://camping-u-monte-cintu.com/",
      t="Riverside under the Niolu peaks, cold clear swimming pools on site. Cool nights at 800 m.", price="€€", mh=True),
 dict(id="c-acquaviva", n="Camping Acqua Viva", lat=42.33265, lon=9.01066, d=8, w="https://www.acquaviva-corse.fr",
      t="Right by Lac de Calacuccia with Monte Cinto filling the window. Small, friendly, walkable to the village.", price="€€", mh=True),
 dict(id="c-vergio", n="Castel de Vergio", lat=42.28688, lon=8.89486, d=8, w=None,
      t="Hotel-and-camping at 1,400 m on the col — the highest legal overnight on the road network, and the GR20 crosses it.", price="€€", mh=True),
 dict(id="c-montecinto-asco", n="Camping Monte Cinto (Asco)", lat=42.41485, lon=8.94533, d=9, w="https://www.campingmontecinto-asco.com/",
      t="In the Asco gorge by the river; the only site in the valley and a perfect mouflon-spotting base.", price="€€", mh=True),
 dict(id="c-restonica", n="Camping Restonica", lat=42.30168, lon=9.15219, d=9, w=None,
      t="On the Restonica road at the edge of Corte — walk into the old town, drive nothing.", price="€€", mh=True),
 dict(id="c-alivetu", n="Camping Alivetu", lat=42.29847, lon=9.14913, d=9, w="http://www.camping-alivetu.com/",
      t="Olive terraces by the Tavignano, 10 min walk from Corte's citadel. Good showers, laundry, service point.", price="€€", mh=True),
 dict(id="c-lesoleil", n="Camping Le Soleil, Vivario", lat=42.15262, lon=9.15088, d=10, w="https://camping-lesoleil.fr/",
      t="Shaded pitches near Vizzavona at 700 m — the coolest night you'll have in August.", price="€€", mh=True),
 dict(id="c-mimosas", n="Camping Les Mimosas, Ajaccio", lat=41.93715, lon=8.72769, d=11, w="https://www.camping-lesmimosas.com",
      t="Closest site to Ajaccio, on the hill above town with a bus into the centre. Fine for a night of city and market.", price="€€", mh=True),
 dict(id="c-prunelli", n="Camping U Prunelli", lat=41.91078, lon=8.82392, d=11, w="https://camping-prunelli.com/",
      t="By the Prunelli river towards Porticcio — greener and quieter than the Ajaccio sites, on the way to Tolla.", price="€€", mh=True),
 dict(id="c-desiles", n="Camping des Îles, Bonifacio", lat=41.37987, lon=9.21124, d=12, w="https://www.camping-desiles.com/",
      t="Closest site to Bonifacio with a view to Sardinia; walk or short drive to the Haute Ville.", price="€€€", mh=True),
 dict(id="c-pertamina", n="Camping Pertamina — U Farniente", lat=41.41596, lon=9.18073, d=12, w="https://www.camping-pertamina.com/",
      t="Large, well-run site under cork oaks 4 km from Bonifacio. Pool, restaurant, proper motorhome facilities.", price="€€€", mh=True),
 dict(id="c-rondinara", n="Camping La Rondinara", lat=41.47339, lon=9.2605, d=13, w="https://www.rondinara.fr/",
      t="Behind the Rondinara bay — first on the beach in the morning, which in Corsica is everything.", price="€€€", mh=True),
 dict(id="c-pirellu", n="Camping U Pirellu", lat=41.58877, lon=9.32997, d=13, w="https://camping-palombaggia.corsica/",
      t="On the Palombaggia road with a pool and a shuttle to the beach; the best base for the white-sand day.", price="€€€", mh=True),
 dict(id="c-bavellavista", n="Camping Bavella Vista", lat=41.75585, lon=9.17229, d=14, w="https://www.campingbavellavista.fr",
      t="In Zonza with the needles on the skyline. Chestnut shade, mountain-cold nights, 20 min from the Bavella trailheads.", price="€€", mh=True),
 dict(id="c-municipalzonza", n="Camping Municipal de Zonza", lat=41.75061, lon=9.19577, d=14, w=None,
      t="Cheap, plain municipal site with a service point — the budget mountain night.", price="€", mh=True),
 dict(id="c-nacres", n="Camping Côte des Nacres", lat=41.86349, lon=9.39739, d=15, w="https://www.campingdesnacres.fr/",
      t="At Solenzara where the Bavella road meets the sea; last beach night before the drive north.", price="€€", mh=True),
 dict(id="c-sandamiano", n="Camping San Damiano", lat=42.62938, lon=9.46835, d=15,
      w="https://www.campingsandamiano.com",
      t="Pine and eucalyptus behind a long sand beach on the Marana, 15 minutes from the Bastia ferry gate. The right last night: close enough that nothing can go wrong in the morning.", price="€€", mh=True),
 dict(id="c-marinaaleria", n="Camping Marina d'Aleria", lat=42.10879, lon=9.54928, d=15, w="https://www.marina-aleria.com/",
      t="Huge sandy site on the east-coast plain — flat, easy, and 90 min from the Bastia ferry gate.", price="€€", mh=True),
]

# ---------------------------------------------------------------- HOTELS (top 5 medium budget)
STAYS = [
 dict(id="s-mariana", n="Le Mariana, Calvi", lat=42.56445, lon=8.75301, d=5, rank=1,
      price="€110–160 B&B (shoulder season)", w="https://www.hotel-mariana.com",
      t="Calvi's best value by common consent: big, spotless rooms, a pool, a rooftop terrace and a 10 min walk to both the citadel and the pine beach.",
      why="Night 5 is the right moment for a real bed — you've done Cap Corse, the Agriates and the Bonifatu hike. Park the van on site, use the laundry, sleep flat."),
 dict(id="s-dunord", n="Hôtel du Nord, Corte", lat=42.30729, lon=9.15066, d=9, rank=2,
      price="€85–120 B&B", w="https://www.hoteldunord-corte.com",
      t="Right on the Cours Paoli in the middle of the old town, family-run, generous breakfast, and the cheapest good bed on the island.",
      why="Perfect the night before the Lac de Melo hike: shower, carb-load in a student town, walk to the trailhead shuttle in the morning."),
 dict(id="s-legolfe", n="Hôtel Le Golfe, Porto", lat=42.26763, lon=8.69375, d=6, rank=3,
      price="€95–150, sea-view rooms", w="https://www.hotel-le-golfe.com",
      t="On the marina at the foot of the Genoese tower, with balconies straight onto the Gulf of Porto and the Scandola boats leaving below you.",
      why="Book this for the night you do the Calanches at sunset — you won't want to be pitching a van in the dark on the D81."),
 dict(id="s-napoleon", n="Hôtel Napoléon, Ajaccio", lat=41.92092, lon=8.73609, d=11, rank=4,
      price="€100–140", w="https://www.hotelnapoleonajaccio.com",
      t="A quiet courtyard hotel in a lane off the Cours Napoléon, two minutes from the Place Foch market and the old port.",
      why="The one urban night of the trip. Leave the van in a secure lot, eat properly, do the museums, catch the Sanguinaires sunset by bus."),
 dict(id="s-sangiovanni", n="Hôtel San Giovanni, Porto-Vecchio", lat=41.57992, lon=9.25487, d=13, rank=5,
      price="€120–170 B&B", w="https://www.hotel-san-giovanni.com",
      t="Three hectares of garden with a pool, 3 km outside Porto-Vecchio, halfway to Palombaggia. Calm, green, and far cheaper than anything on the beach road.",
      why="The beach-lazing night. Van in the shade, hammock, pool, and Santa Giulia and Palombaggia both 15 min away."),
 dict(id="s-bavella", n="Auberge du Col de Bavella", lat=41.79483, lon=9.22903, d=14, rank=6, bonus=True,
      price="€75–110 half-board / dorms from €25", w=None,
      t="A wooden mountain inn at the pass itself, doing charcuterie, wild boar stew and hikers' breakfasts. Rooms are basic; the position is priceless.",
      why="Bonus pick: if you want to be at the Aiguilles for sunrise without a 5 a.m. drive, sleep at 1,218 m."),
]

# ---------------------------------------------------------------- DAYS
DAY_META = {
 1:  dict(base="Macinaggio", theme="Arrival & the east side of Cap Corse", vid="00:00–01:29",
          bed="18:00", tip='Everything today hangs off the ferry. If the crossing runs late, drop Sisco and go straight up the Cap — the campsite is the fixed point, not the sightseeing.', intro="Roll off the ferry, resist the motorway, and turn left up the Cap. Tonight you sleep at the end of the road."),
 2:  dict(base="Patrimonio / St-Florent", theme="Round the tip: towers, cows, and a black beach", vid="01:29–08:32",
          bed="18:00", tip="Nonza's tower at sunset is one of the best hours on the Cap. Check in at Patrimonio first — it is 12 minutes away, and you can go back out with the pitch already yours.", intro="A coastal walk in the morning, the northernmost sand in Corsica at lunch, and Nonza's black shingle in the evening light."),
 3:  dict(base="Ostriconi", theme="The Désert des Agriates", vid="08:32–09:55",
          bed="18:00", intro="Corsica's empty quarter. You cannot drive to the good beaches — that's exactly why they're good."),
 4:  dict(base="Bodri / Balagne", theme="Balagne: market town, hill villages, easy sand", vid="09:55–11:08",
          bed="18:00", intro="The gentlest day of the trip. A market, three perched villages, and a beach you walk to through the maquis."),
 5:  dict(base="Calvi", theme="Citadel, river pools and a mountain cirque", vid="12:08–13:07",
          bed="18:30", intro="Old town in the morning, granite plunge pools at midday, and as much of the Bonifatu cirque as your legs want."),
 6:  dict(base="Porto", theme="The wild west coast", vid="13:07–16:22",
          bed="18:00", tip='This day does not fit as written: 3¼ hours of driving plus a 4-hour hike up Monte Senino. Either leave Calvi at 07:00, or do Senino tomorrow morning and reach Porto in daylight. Do not arrive at 20:30 hoping someone is on reception.', intro="The most spectacular driving day and, at 105 km in over 3 hours of moving time, a lesson in Corsican distances."),
 7:  dict(base="Porto / Arone", theme="Red granite at dawn, sand by lunchtime", vid="18:27–19:03",
          bed="17:30", tip='The Calanches at sunset is the whole point of today — so check into Arone by 17:30 first, then drive the 20 minutes back. Sunset in late May is around 21:00; no Corsican campsite is taking a new arrival then.', intro="UNESCO granite at dawn, a cliff-top Genoese tower by late morning, and the rest of the day horizontal on a beach."),
 8:  dict(base="Calacuccia", theme="Over the top into the Niolu", vid="20:51–22:02",
          bed="18:00", tip='Calacuccia sits at 800 m and its receptions shut earlier than the coast. Aim for 17:30.', intro="Leave the sea behind. Chestnut villages, the highest pass on the island, and a swim under a 2,700 m mountain."),
 9:  dict(base="Corte", theme="Asco gorge & the old capital", vid="44:38–46:20 / 40:00",
          bed="18:00", intro="A dead-end valley in the morning, a citadel and a proper dinner in the evening."),
 10: dict(base="Corte / Vizzavona", theme="Restonica — the big one, and it got bigger", vid="40:00–44:38",
          tip='No move tonight — you are already checked in. That is precisely why day 10 sleeps in Corte a second time: an eight-hour hike and a 19:00 reception deadline cannot share a day.', intro="The hike people come to Corsica for. Since the 2023 storms wrecked the valley road it is a 25 km, eight-hour mountain day reached by shuttle — plan it as the hardest day of the trip, then drop south into the beech forest to cool off."),
 11: dict(base="Ajaccio", theme="Waterfalls, a lake, and the capital", vid="35:45–38:16",
          bed="17:30", tip='Check in at Ajaccio, then go out to the Sanguinaires. Also check when the Parata car park barrier closes before you commit to sunset — it is earlier than sunset for much of the year.', intro="Snowmelt in the morning, an empty reservoir at lunch, Napoleon's old town in the afternoon, red islands at sunset — and the D1/D4 pass if you want one more mountain road."),
 12: dict(base="Bonifacio", theme="South through prehistory to the cliffs", vid="30:45–31:19",
          bed="18:00", tip='181 km, the longest drive of the trip. Leave Ajaccio by 09:00 and treat Roccapina as optional, not assumed.', intro="The longest drive of the trip (180 km), broken by menhirs, granite towns and a lion-shaped rock, ending on the most dramatic clifftop in the Mediterranean."),
 13: dict(base="Porto-Vecchio", theme="A day off: sand, shallow water, a boat", vid="29:19",
          bed="18:00", intro="A pure relax day. Three of the best beaches in Europe and a boat out to the Lavezzi if you want one."),
 14: dict(base="Zonza", theme="Up to the needles of Bavella", vid="26:30–29:56",
          bed="18:00", intro="From sea level to 1,218 m: a waterfall, a Pisan church, and the granite spires that close the island's spine."),
 15: dict(base="near Bastia", theme="The D69, and down to the coast", vid="33:32 / 25:23",
          bed="18:00",
          tip="You are not catching a boat today. Get to the coast, check in, and sleep 20 minutes from the port.",
          intro="One last mountain road nobody drives, oysters on a lagoon, and a pitch 20 minutes from the ferry gate — with the crossing still a whole day away."),
 16: dict(base="ferry", theme="The day you hope you don't need", vid="23:32",
          tip="The buffer. If the last two weeks went to plan, spend the morning in the Castagniccia and roll up to the ferry relaxed. If they did not — a breakdown, a closed road, a day lost to weather, a hike that ran three hours over — this is the day you spend it, and you still make the boat.",
          intro="A day with nothing load-bearing in it. That is the entire point: fifteen days of mountain roads, ferries and weather will eat one of them sooner or later, and this is the one they get to eat."),
}

_seen_photo = set()
def _photos_for(day):
    out = []
    for p in POIS:
        if p["d"] != day: continue
        for x in PHOTO_BY_POI.get(p["id"], []):
            if x["f"] in _seen_photo: continue
            _seen_photo.add(x["f"]); out.append(x)
            if len(out) >= 6: return out
    return out


# ---- vegan eating -------------------------------------------------------
from eats import PLACES as EAT_PLACES
def _eat_days(EAT_MAP):
    """Attach the day's eating notes, and emit each place once as a map pin."""
    day_eat, pins, first = {}, [], {}
    for d in sorted(EAT_MAP):
        ids, note = EAT_MAP[d]
        lst = []
        for k in ids:
            p = EAT_PLACES[k]
            lst.append(dict(id=k, n=p["n"], town=p["town"], v=p["v"], t=p["t"],
                            lat=p["lat"], lon=p["lon"]))
            if k not in first and p["lat"] is not None:
                first[k] = d
                pins.append(dict(id="eat-"+k, n=p["n"], c="food", d=d,
                                 lat=p["lat"], lon=p["lon"],
                                 t=p["t"] + "  (" + p["town"] + ")", f=[], eatv=p["v"]))
        day_eat[d] = dict(places=lst, note=note)
    return day_eat, pins
from eats import VAN_EAT
DAY_EAT, EAT_PINS = _eat_days(VAN_EAT)

days=[]
for r in routes:
    m=DAY_META[r["day"]]
    days.append(dict(day=r["day"], title=r["title"], km=r["km"], min=r["min"],
                     geometry=r["geometry"], base=m["base"], theme=m["theme"],
                     vid=m["vid"], intro=m["intro"],
                     bed=m.get("bed"), tip=m.get("tip"), flow=FLOW.get(r["day"], []),
                     eat=DAY_EAT.get(r["day"]),
                     photos=_photos_for(r["day"])))

for _c in CAMPS: _c.setdefault("checkin", CHECKIN_CAMP)
for _s in STAYS: _s.setdefault("checkin", "Check-in from 15:00, checkout 10:00–11:00 (typical).")
# how many of 10 independent guides mention each stop; `None` = not checked
try:
    CORROB = json.load(open("data/corroboration.json"))
except FileNotFoundError:
    CORROB = {}
for _p in (POIS if "POIS" in dir() else pois_out):
    if _p.get("c") != "food" and _p["id"] in CORROB:
        _p["src"] = CORROB[_p["id"]]
out = dict(pois=POIS + EAT_PINS, camps=CAMPS, stays=STAYS, days=days)
with open("assets/js/data.js","w") as f:
    f.write("// Generated. Coordinates from OpenStreetMap/Nominatim; routes from OSRM (real road geometry).\n")
    f.write("window.TRIP = ")
    json.dump(out, f, ensure_ascii=False, separators=(",",":"))
    f.write(";\n")
print("pois",len(POIS),"camps",len(CAMPS),"stays",len(STAYS),"days",len(days),
      "photos",sum(len(d["photos"]) for d in days))
import os
print("data.js", round(os.path.getsize("assets/js/data.js")/1024,1),"KB")
print("total km", round(sum(d["km"] for d in days),1), "total drive h", round(sum(d["min"] for d in days)/60,1))
