# -*- coding: utf-8 -*-
"""Vegan eating, day by day.

Every place here exists in OpenStreetMap or HappyCow with the coordinates given.
Nothing is invented. `v` records how strong the evidence is, because that matters
more than usual on an island this hard for vegans:

  vegan    fully vegan / plant-based kitchen
  options  vegan dishes confirmed (OSM diet:vegan=yes, or a HappyCow listing)
  ask      vegetarian-friendly; vegan needs asking for (OSM diet:vegetarian=yes)
  shop     organic supermarket, greengrocer or market — the self-catering backbone
"""

P = lambda **k: k
PLACES = {
# --- Bastia & the north-east
"vg-bastia":    P(n="COMO Cucina · VG", lat=42.7038, lon=9.4528, town="Bastia", v="vegan",
                  t="An entirely plant-based kitchen — bowls, salads, desserts. The single best vegan meal on the island and it happens to be where your ferry lands."),
"ghisoni-cafe": P(n="Ghisoni's Coffee House", lat=42.7016, lon=9.4499, town="Bastia", v="ask",
                  t="Proper coffee and plant milks, a short walk up from the Vieux Port. Good breakfast stop."),
"acantina":     P(n="A Cantina", lat=42.6961, lon=9.4474, town="Bastia", v="ask",
                  t="Vegetarian dishes on the menu in the old town; ask for them without cheese and they will manage it."),
"eauvive":      P(n="Eau Vive", lat=42.6274, lon=9.4368, town="south of Bastia", v="shop",
                  t="Organic supermarket on the way in or out of the city. Tofu, plant milks, pulses — stock the van properly here."),
"laroulotte":   P(n="La Roulotte Magasin Bio", lat=42.6464, lon=9.4397, town="Furiani", v="shop",
                  t="Organic shop just south of Bastia, handy on the ferry run."),
"libertalia":   P(n="Libertalia Bistrot Tropical", lat=42.6978, lon=9.3616, town="near Patrimonio", v="ask",
                  t="Tropical bistro with vegetarian plates, on the road between Bastia and Saint-Florent. Rare thing in Cap Corse: a menu that isn't charcuterie."),
"amadei":       P(n="Épicerie Amadei", lat=42.698, lon=9.3511, town="Saint-Florent", v="shop",
                  t="Greengrocer in town. This is your Saleccia picnic — there is nothing at all on that beach."),
# --- Balagne & Calvi
"vieclaire-ir": P(n="La Vie Claire", lat=42.6119, lon=8.8927, town="Balagne", v="shop",
                  t="Organic supermarket chain — reliable for plant milk, tofu and vegan spreads when village shops are not."),
"fangufood":    P(n="Fangu Food", lat=42.3874, lon=8.7482, town="Balagne", v="ask",
                  t="Casual place with vegetarian options inland from the coast road."),
"buvette":      P(n="Buvette de la Place", lat=42.5666, lon=8.7578, town="Calvi", v="options",
                  t="Tagged for vegan food in OpenStreetMap and right by the citadel steps. Your reliable Calvi lunch."),
"colomb":       P(n="Le Café Colomb", lat=42.56785, lon=8.76093, town="Calvi citadel", v="options",
                  t="Small terrace inside the citadel walls doing a vegan chocolate mousse and plant milks. Worth the climb for the view alone."),
"epicerie-bio": P(n="Épicerie Bio", lat=42.5596, lon=8.7568, town="Calvi", v="shop",
                  t="Organic grocer in town — restock before the west coast, where shops thin out fast."),
# --- The west
"cormoran":     P(n="Gîte Le Cormoran Voyageur", lat=42.3487, lon=8.6126, town="Girolata", v="ask",
                  t="In the village you can only reach on foot or by boat. Vegetarian plates; tell them when you book the boat and they will sort you out."),
"levin150":     P(n="Le Vin150", lat=42.2656, lon=8.7055, town="Porto", v="ask",
                  t="Vegetarian options on the Porto marina — the most useful address on this coast. Ask for dishes sans fromage."),
"tramula":      P(n="A Tramula · Caffé di la Posta", lat=42.2535, lon=8.8031, town="Évisa", v="ask",
                  t="Village café in chestnut country with vegetarian plates. Chestnut-flour things here are often dairy-free — ask."),
# --- The interior
"barcinto":     P(n="Bar du Cinto", lat=42.3344, lon=9.0194, town="Calacuccia", v="ask",
                  t="The bar by the lake, and effectively the only kitchen in the Niolu that will do you a vegetable plate. Ask early in the day."),
"orsu":         P(n="A Casa di l'Orsu", lat=42.3053, lon=9.1506, town="Corte", v="options",
                  t="Tagged for vegan food, in the middle of the old town. Corte is a student town, so it is the most vegan-literate place outside the two cities."),
"idealprimeur": P(n="Idéal Primeur", lat=42.3012, lon=9.1665, town="Corte", v="shop",
                  t="Greengrocer for the Restonica hike food. You will want a lot of it."),
"auchan-corte": P(n="Supermarché, Corte", lat=42.30074, lon=9.1584, town="Corte", v="shop",
                  t="Full-size supermarket — the last proper one before the mountains."),
"petralegnu":   P(n="Petra e Legnu", lat=42.4724, lon=9.1275, town="Ponte Leccia area", v="ask",
                  t="Vegetarian options on the north–south road, useful on a transfer day."),
# --- Ajaccio
"greenfarmer":  P(n="Green Farmer's", lat=41.9216, lon=8.7375, town="Ajaccio", v="vegan",
                  t="Fully plant-based. Between this and A Cantali, Ajaccio is the easiest place to be vegan in Corsica."),
"acantali":     P(n="A Cantali · bio-végétarien", lat=41.9252, lon=8.7373, town="Ajaccio", v="options",
                  t="Organic vegetarian restaurant in the old town — an entirely meat-free menu, with vegan dishes on it."),
"pokawa":       P(n="Pokawa", lat=41.9473, lon=8.7637, town="Ajaccio", v="options",
                  t="Poke bowls, vegan-tagged. Not romantic, but quick, cheap and certain — useful before a sunset drive."),
"biocoop":      P(n="Biocoop", lat=41.92897, lon=8.73769, town="Ajaccio", v="shop",
                  t="The best-stocked organic supermarket on the island. If you are self-catering, do a big shop here."),
"saveurs":      P(n="1001 Saveurs Sauvages", lat=None, lon=None, town="Ajaccio", v="options",
                  t="Repeatedly called the best vegan food in Corsica by HappyCow reviewers. Listed there rather than in OpenStreetMap, so check the current address and hours before you set off."),
# --- The south
"le466":        P(n="Le 466", lat=41.7014, lon=8.8583, town="near Propriano", v="ask",
                  t="Vegetarian options on the road south — a good lunch break between Filitosa and Sartène."),
"airstream":    P(n="Chez Antoine Airstream Pizzeria", lat=41.6946, lon=8.8838, town="Propriano", v="ask",
                  t="Pizza from an Airstream. Ask for a marinara — tomato, garlic, oregano, no cheese — which is vegan by default and the single most reliable meal in rural Corsica."),
"roccaserra":   P(n="Rocca Serra", lat=41.3867, lon=9.1578, town="Bonifacio", v="options",
                  t="Ice cream with vegan sorbets, on the way up to the Haute Ville. Small thing, big morale."),
"lamarine":     P(n="Café La Marine", lat=41.5903, lon=9.28264, town="Porto-Vecchio", v="options",
                  t="On the port, listed on HappyCow for its vegan choices. The most dependable meal in the south-east."),
"vieclaire-pv": P(n="La Vie Claire", lat=41.6021, lon=9.2769, town="Porto-Vecchio", v="shop",
                  t="Organic supermarket — restock here before the Alta Rocca, where you will find very little."),
"abuttega":     P(n="A Buttega", lat=41.5962, lon=9.2796, town="Porto-Vecchio", v="shop",
                  t="Greengrocer in the upper town for beach picnics."),
"produits-zonza": P(n="Produits Corses", lat=41.7494, lon=9.1712, town="Zonza", v="shop",
                  t="Village shop. Thin pickings, so arrive with what you need rather than hoping."),
}

# --- days where the honest answer is "carry your own"
N = lambda t: t
VAN_EAT = {
 1:  (["vg-bastia","ghisoni-cafe","acantina"], None),
 2:  (["libertalia"], N("Centuri is the lobster village and Barcaggio has a beach shack — neither is a vegan lunch. Buy bread, tomatoes, olives and fruit in Macinaggio before you set off and eat on the coastal path. This is the pattern for the whole Cap.")),
 3:  (["amadei"], N("There is nothing whatsoever at Saleccia — no bar, no shack, no water. Whatever you carry onto that boat is what you eat. Buy it in Saint-Florent.")),
 4:  (["vieclaire-ir"], N("The Île-Rousse covered market before eleven is the best self-catering stop of the trip: tomatoes, peaches, olives, bread, chestnut flour. The Balagne villages are craft shops and cafés rather than kitchens.")),
 5:  (["buvette","colomb","epicerie-bio"], None),
 6:  (["cormoran","levin150"], None),
 7:  ([], N("A genuinely thin day: Piana has two terraces, Arone has one beach bar, and neither will have a vegan main. Shop in Porto the evening before and picnic at Capo Rosso and on the beach. Any pizzeria will do you a marinara — no cheese, and vegan by default.")),
 8:  (["tramula","barcinto"], N("You are at 800 m in the Niolu with a handful of village bars. Bar du Cinto will do a plate of vegetables if you ask at lunchtime rather than at nine at night.")),
 9:  (["orsu","idealprimeur","auchan-corte"], None),
 10: (["orsu"], N("Eight hours on the trail with one small bar at the Bergeries. Carry everything: bread, nut butter, dried fruit, nuts, plenty of salt. Buy it in Corte the night before.")),
 11: (["greenfarmer","acantali","pokawa","saveurs","biocoop"], N("The easiest vegan day of the trip. Eat properly tonight and do a big shop at Biocoop for the south.")),
 12: (["le466","airstream","roccaserra"], None),
 13: (["lamarine","vieclaire-pv","abuttega","roccaserra"], N("Bring everything to the Lavezzi — there is nothing on the islands at all, which is rather the point of them.")),
 14: (["produits-zonza"], N("Mountain auberges here are wild boar, charcuterie and cheese, and Bavella's are the most meat-heavy on the island. Ring L'Aiglon in Zonza in the morning and ask — given notice they will cook you something; given none, they will shrug.")),
 15: ([], N("A thin stretch: Solenzara has beach cafés, Ghisoni has a village bar, Aleria has oyster shacks. Carry a picnic and eat it at the ski station under Monte Renoso, which is a better lunch spot than any of them.")),
 16: (["vg-bastia","eauvive","laroulotte"], N("Last chance to load up on Corsican things that happen to be vegan: chestnut flour, olive oil, honey if you eat it, canistrelli biscuits (check — many are made with wine and oil, not butter), clementines, myrtle liqueur.")),
}

HOTEL_EAT = {
 1:  (["vg-bastia","ghisoni-cafe","acantina"], None),
 2:  (["libertalia"], N("Nothing on the Cap loop will feed you well. Pack a picnic in Bastia before you leave — you pass back through Patrimonio at the end of the day anyway.")),
 3:  (["amadei"], N("Nothing at all at Saleccia. Whatever you carry onto the boat is lunch.")),
 4:  (["vieclaire-ir","fangufood"], N("Hit the Île-Rousse covered market before eleven — the best produce stop on the route.")),
 5:  (["buvette","colomb","epicerie-bio"], None),
 6:  (["cormoran","levin150"], None),
 7:  ([], N("Thin. Piana and Arone will not do you a vegan main, so buy lunch in Porto in the morning and eat it at Capo Rosso. Dinner back in Porto at Le Vin150.")),
 8:  (["greenfarmer","acantali","pokawa","saveurs","biocoop"], None),
 9:  (["biocoop"], N("A mountain loop with village bars only. Make a picnic at breakfast or shop at Biocoop on the way out — Vizzavona and Bocognano will offer you an omelette at best.")),
 10: (["le466","airstream","roccaserra"], None),
 11: (["roccaserra","lamarine"], N("Take everything to the Lavezzi. Bonifacio itself is a tourist port, so there is pizza and pasta on the quay if the day goes wrong.")),
 12: (["lamarine","vieclaire-pv","abuttega","produits-zonza"], N("Restock in Porto-Vecchio before you climb — the Alta Rocca has almost nothing, and you arrive at a mountain inn where dinner is at half seven.")),
 13: (["orsu","auchan-corte"], N("Ring ahead about dinner at Zonza or eat in Corte. Bavella's auberges are charcuterie and boar.")),
 14: (["orsu","idealprimeur"], N("Eight hours on the trail with one small bar at the top. Carry everything, bought in Corte the evening before.")),
 15: (["barcinto","vg-bastia"], None),
 16: (["vg-bastia","eauvive","laroulotte"], N("Last chance for chestnut flour, olive oil, clementines and canistrelli to take home — check the biscuits, as many are made with oil and wine rather than butter.")),
}
