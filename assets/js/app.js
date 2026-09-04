/* ==========================================================
   Corsica by Van — map + itinerary renderer
   ========================================================== */
(function () {
  'use strict';
  var T = window.TRIP;

  var CATS = {
    town:     { label: 'Old towns & villages', color: '#c4562f', icon: '🏘️' },
    hike:     { label: 'Hikes',                color: '#3f7d3a', icon: '🥾' },
    beach:    { label: 'Beaches',              color: '#2ea7ba', icon: '🏖️' },
    swim:     { label: 'Rivers & waterfalls',  color: '#1b8a9c', icon: '💦' },
    view:     { label: 'Viewpoints & passes',  color: '#7a4b8f', icon: '🔭' },
    heritage: { label: 'Ruins & prehistory',   color: '#8a6a3a', icon: '🗿' },
    nature:   { label: 'Nature reserves',      color: '#2f6b4f', icon: '🌿' },
    culture:  { label: 'Wine & food',          color: '#9a7b2f', icon: '🍷' },
    port:     { label: 'Ports',                color: '#5b6b78', icon: '⚓' },
    camp:     { label: 'Campsites',            color: '#2f6b2a', icon: '⛺' },
    stay:     { label: 'Hotels (mid-budget)',  color: '#b5305e', icon: '🛏️' },
    food:     { label: 'Vegan-friendly food',  color: '#4a8a2b', icon: '🌱' }
  };
  var TRAV = { nature: 'Nature & hiking', relax: 'Beach & chill', culture: 'Towns & culture' };
  var VEG = {
    vegan:   { l: 'Fully vegan',        c: '#2f6b2a' },
    options: { l: 'Vegan options',      c: '#4a8a2b' },
    ask:     { l: 'Veg-friendly — ask', c: '#8a6a3a' },
    shop:    { l: 'Shop / market',      c: '#5b6b78' }
  };

  /* --------------------------------------------- unified point list */
  var PTS = [];
  T.pois.forEach(function (p) { PTS.push(Object.assign({ kind: 'poi' }, p)); });
  T.camps.forEach(function (c) {
    PTS.push({ kind: 'camp', c: 'camp', id: c.id, n: c.n, lat: c.lat, lon: c.lon, d: c.d,
               t: c.t, w: c.w, price: c.price, checkin: c.checkin, f: [] });
  });
  T.stays.forEach(function (s) {
    PTS.push({ kind: 'stay', c: 'stay', id: s.id, n: s.n, lat: s.lat, lon: s.lon, d: s.d,
               t: s.t, w: s.w, price: s.price, why: s.why, rank: s.rank,
               nights: s.nights, checkin: s.checkin, bonus: s.bonus, f: [] });
  });
  var byId = {}; PTS.forEach(function (p) { byId[p.id] = p; });

  /* first photo per stop, for the map popups */
  var photoByPoi = {}, allPhotos = [];
  T.days.forEach(function (d) {
    (d.photos || []).forEach(function (ph) {
      ph.day = d.day;
      allPhotos.push(ph);
      if (!photoByPoi[ph.poi]) photoByPoi[ph.poi] = ph;
    });
  });
  var PDIR = 'assets/photos/';
  var poisByDay = {};
  PTS.forEach(function (p) { (poisByDay[p.d] = poisByDay[p.d] || []).push(p); });

  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (m) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m];
    });
  };
  var host = function (u) { try { return new URL(u).hostname.replace(/^www\./, ''); } catch (e) { return 'website'; } };
  var hrs = function (m) {
    var h = Math.floor(m / 60), r = m % 60;
    return (h ? h + ' h ' : '') + (r ? r + ' min' : (h ? '' : '0 min'));
  };

  /* ============================================================ MAP */
  var map, layers = {}, markers = {}, routeLines = {}, activeDay = null, activePin = null;
  var offSet = {};   // categories currently switched OFF

  /* cluster group if the plugin loaded, plain layer group otherwise */
  function makeGroup() {
    if (!L.markerClusterGroup) return L.layerGroup();
    return L.markerClusterGroup({
      maxClusterRadius: 46,
      disableClusteringAtZoom: 11,
      showCoverageOnHover: false,
      spiderfyOnMaxZoom: true,
      iconCreateFunction: function (cl) {
        var n = cl.getChildCount();
        return L.divIcon({
          html: '<div class="cl' + (n > 9 ? ' big' : '') + '">' + n + '</div>',
          className: 'marker-cluster', iconSize: n > 9 ? [32, 32] : [27, 27]
        });
      }
    });
  }

  function pinHtml(cat, small) {
    var c = CATS[cat] || CATS.town;
    return '<div class="pin' + (small ? ' sm' : '') + '" style="background:' + c.color + '">' +
           '<span>' + c.icon + '</span></div>';
  }

  function popupHtml(p) {
    var c = CATS[p.c] || CATS.town, h = '';
    var ph = photoByPoi[p.id];
    if (ph) {
      h += '<div class="pp-img"><img loading="lazy" alt="" src="' + PDIR + esc(ph.f) + '-t.webp">' +
           '<span>© ' + esc(ph.by) + ' · ' + esc(ph.lic) + '</span></div>';
    }
    h += '<div class="pp">';
    h += '<div class="pp-cat" style="color:' + c.color + '">' + esc(c.label) +
         (p.d ? ' &middot; Day ' + p.d : '') + '</div>';
    h += '<h5>' + esc(p.n) + '</h5>';
    if (p.t) h += '<p>' + esc(p.t) + '</p>';
    if (p.eatv && VEG[p.eatv]) {
      h += '<div class="hk" style="border-color:' + VEG[p.eatv].c + ';background:#eef6ea;color:#2a4d27">' +
           '<b>🌱 ' + esc(VEG[p.eatv].l) + '</b></div>';
    }
    if (p.hike) {
      h += '<div class="hk"><b>Hike &mdash; ' + esc(p.hike.grade) + '</b><br>' +
           esc(p.hike.dist) + ' &middot; ' + esc(p.hike.up) + ' ascent &middot; ' + esc(p.hike.dur) + '</div>';
    }
    if (p.van) h += '<div class="van"><b>🚐 Van note</b><br>' + esc(p.van) + '</div>';
    if (p.why) h += '<div class="van"><b>Why book it here</b><br>' + esc(p.why) + '</div>';
    var row = [];
    if (p.time) row.push('⏱ ' + esc(p.time));
    if (p.price) row.push('💰 ' + esc(p.price));
    if (p.vid) row.push('▶ video ' + esc(p.vid));
    row.push('<a class="ext" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=' +
             p.lat + ',' + p.lon + '">Directions ↗</a>');
    if (p.w) row.push('<a class="ext" target="_blank" rel="noopener" href="' + esc(p.w) + '">' + esc(host(p.w)) + ' ↗</a>');
    h += '<div class="row">' + row.join('<span style="color:#ccc">|</span>') + '</div></div>';
    return h;
  }

  function initMap() {
    map = L.map('map', { zoomControl: true, scrollWheelZoom: true, minZoom: 6 });
    L.control.scale({ imperial: false, position: 'bottomleft', maxWidth: 120 }).addTo(map);

    var terrain = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
      maxZoom: 17, subdomains: 'abc',
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
                   '<a href="https://viewfinderpanoramas.org">SRTM</a> | Tiles &copy; ' +
                   '<a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
    });
    var plain = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
    terrain.addTo(map);
    L.control.layers({ 'Terrain (relief)': terrain, 'Plain street map': plain }, null,
                     { position: 'topright', collapsed: true }).addTo(map);

    /* routes: every day drawn faint, plus a highlight layer */
    T.days.forEach(function (d) {
      var cas  = L.polyline(d.geometry, { color: '#ffffff', weight: 6,   opacity: 0.62, lineJoin: 'round', lineCap: 'round' });
      var base = L.polyline(d.geometry, { color: '#26454f', weight: 2.6, opacity: 0.95, lineJoin: 'round' });
      var halo = L.polyline(d.geometry, { color: '#ffffff', weight: 11,  opacity: 0.92, lineJoin: 'round', lineCap: 'round' });
      var hi   = L.polyline(d.geometry, { color: '#d64d1f', weight: 5.5, opacity: 1,    lineJoin: 'round' });
      routeLines[d.day] = { cas: cas, base: base, hi: hi, halo: halo };
      cas.addTo(map); base.addTo(map);
      base.bindTooltip('Day ' + d.day + ' — ' + d.title + ' · ' + d.km + ' km · ' + hrs(d.min),
                       { sticky: true });
      base.on('click', function () { selectDay(d.day); });
      cas.on('click', function () { selectDay(d.day); });
    });

    /* markers */
    PTS.forEach(function (p) {
      var m = L.marker([p.lat, p.lon], {
        icon: L.divIcon({
          className: 'pin-w', html: pinHtml(p.c, p.kind !== 'poi'),
          iconSize: [26, 26], iconAnchor: [13, 26], popupAnchor: [0, -24]
        }),
        title: p.n, riseOnHover: true
      });
      m.bindPopup(popupHtml(p), { maxWidth: 320, autoPanPadding: [30, 30] });
      m.on('popupopen', function () { setActivePin(p.id); });
      m.on('popupclose', function () { setActivePin(null); });
      markers[p.id] = m;
      layers[p.c] = layers[p.c] || makeGroup();
      layers[p.c].addLayer(m);
    });
    Object.keys(layers).forEach(function (k) { layers[k].addTo(map); });

    resetView();
  }

  function setActivePin(id) {
    if (activePin && markers[activePin]) {
      var e0 = markers[activePin].getElement();
      if (e0) { var d0 = e0.querySelector('.pin'); if (d0) d0.classList.remove('act'); }
    }
    activePin = id;
    if (id && markers[id]) {
      var e = markers[id].getElement();
      if (e) { var d = e.querySelector('.pin'); if (d) d.classList.add('act'); }
    }
  }

  function allBounds() {
    var b = L.latLngBounds([]);
    T.days.forEach(function (d) { d.geometry.forEach(function (c) { b.extend(c); }); });
    return b;
  }

  function resetView() {
    activeDay = null;
    T.days.forEach(function (d) {
      var r = routeLines[d.day];
      map.removeLayer(r.hi); map.removeLayer(r.halo);
      if (!map.hasLayer(r.cas)) r.cas.addTo(map);
      if (!map.hasLayer(r.base)) r.base.addTo(map);
      r.cas.setStyle({ opacity: 0.62, weight: 6 });
      r.base.setStyle({ opacity: 0.95, weight: 2.6 });
    });
    applyFilters();
    map.fitBounds(allBounds(), { padding: [26, 26] });
    document.querySelectorAll('.day-btn').forEach(function (b) { b.classList.remove('on'); });
    var rb = document.getElementById('mapReset'); if (rb) rb.textContent = 'Whole route · ' + T.days.length + ' days';
  }

  function selectDay(n) {
    if (activeDay === n) { resetView(); return; }
    activeDay = n;
    T.days.forEach(function (d) {
      var r = routeLines[d.day];
      map.removeLayer(r.hi); map.removeLayer(r.halo);
      var off = d.day === n;
      r.cas.setStyle({ opacity: off ? 0 : 0.30, weight: 5 });
      r.base.setStyle({ opacity: off ? 0 : 0.34, weight: 2.4 });
    });
    var r = routeLines[n];
    r.halo.addTo(map); r.hi.addTo(map);
    r.halo.bringToFront(); r.hi.bringToFront();
    applyFilters();
    var day = T.days.filter(function (d) { return d.day === n; })[0];
    /* fit the road route AND that day's stops — several (Lac de Melo, Saleccia,
       the Lavezzi) are reached on foot or by boat and sit well off the driven line */
    var bounds = L.latLngBounds(day.geometry);
    PTS.forEach(function (p) {
      if (p.d === n && !offSet[p.c]) bounds.extend([p.lat, p.lon]);
    });
    map.fitBounds(bounds, { padding: [56, 56] });
    document.querySelectorAll('.day-btn').forEach(function (b) {
      b.classList.toggle('on', +b.dataset.day === n);
    });
    var rb = document.getElementById('mapReset');
    if (rb) rb.textContent = '← Back to whole route';
  }

  /* show/hide markers per category filter AND per selected day */
  function applyFilters() {
    PTS.forEach(function (p) {
      var m = markers[p.id];
      var show = !offSet[p.c] && (activeDay === null || p.d === activeDay);
      var lg = layers[p.c];
      if (show) { if (!lg.hasLayer(m)) lg.addLayer(m); }
      else { if (lg.hasLayer(m)) lg.removeLayer(m); }
    });
  }

  /* ============================================================ UI build */
  function buildChips() {
    var box = document.getElementById('chips');
    if (!box) return;
    Object.keys(CATS).forEach(function (k) {
      if (!PTS.some(function (p) { return p.c === k; })) return;
      var n = PTS.filter(function (p) { return p.c === k; }).length;
      var b = document.createElement('button');
      b.className = 'chip on'; b.type = 'button';
      b.style.color = CATS[k].color;
      b.innerHTML = '<i></i>' + esc(CATS[k].label) + ' <span style="opacity:.6">' + n + '</span>';
      b.setAttribute('aria-pressed', 'true');
      b.onclick = function () {
        offSet[k] = !offSet[k];
        b.classList.toggle('on', !offSet[k]);
        b.setAttribute('aria-pressed', String(!offSet[k]));
        b.style.color = offSet[k] ? '' : CATS[k].color;
        applyFilters();
      };
      box.appendChild(b);
    });
  }

  function buildDayList() {
    var box = document.getElementById('dayList');
    if (!box) return;
    T.days.forEach(function (d) {
      var b = document.createElement('button');
      b.className = 'day-btn'; b.type = 'button'; b.dataset.day = d.day;
      b.innerHTML = '<span class="day-num">' + d.day + '</span><span>' +
        '<span class="day-t">' + esc(d.title) + '</span>' +
        '<span class="day-m">' + d.km + ' km · ' + hrs(d.min) + ' driving · sleep ' + esc(d.base) + '</span></span>';
      b.onclick = function () { selectDay(d.day); };
      box.appendChild(b);
    });
  }

  /* How many of 10 independent guides mention this stop.  Low is not the same
     as bad -- a 0 that the source film raves about is a find, not a dud -- so
     the label says which it is. */
  function srcChip(p) {
    if (typeof p.src !== 'number') return '';
    var cls = p.src >= 7 ? 'hi' : p.src >= 4 ? 'mid' : 'lo';
    var txt = p.src >= 7 ? p.src + '/10 guides'
            : p.src >= 4 ? p.src + '/10 guides'
            : p.src >= 1 ? p.src + '/10 guides'
            : (p.vid ? "the film's own find" : 'unlisted');
    var tip = p.src === 0 && p.vid
      ? "No guidebook we checked mentions this; it comes from the source film"
      : p.src + ' of 10 independent Corsica guides mention this stop';
    return '<span class="srcchip ' + cls + '" title="' + esc(tip) + '">' + esc(txt) + '</span>';
  }

  function buildItinerary() {
    var box = document.getElementById('itinerary');
    if (!box) return;
    T.days.forEach(function (d) {
      var stops = (poisByDay[d.day] || []).filter(function (p) { return p.kind === 'poi'; });
      var camps = (poisByDay[d.day] || []).filter(function (p) { return p.kind === 'camp'; });
      var stays = (poisByDay[d.day] || []).filter(function (p) { return p.kind === 'stay'; });

      var h = '<article class="day" id="day' + d.day + '">';
      h += '<div class="day-rail"><div class="n">' + d.day + '</div><div class="l">Day</div>' +
           '<div class="drive"><b>' + d.km + ' km</b>' + hrs(d.min) + ' moving<br>' +
           '<span style="color:var(--muted)">video ' + esc(d.vid) + '</span>' +
           (d.bed ? '<br><span class="bedby">at your bed by ' + esc(d.bed) + '</span>' : '') +
           '</div></div>';
      h += '<div class="day-body"><h3>' + esc(d.title) + '</h3>' +
           '<div class="theme">' + esc(d.theme) + '</div>' +
           '<p class="intro">' + esc(d.intro) + '</p>';

      /* the running order below now carries the timing guidance; the standalone
         tip is only shown when there is no flow for the day */
      if (d.tip && !(d.flow && d.flow.length))
        h += '<div class="note time"><b>Timing:</b> ' + esc(d.tip) + '</div>';

      if (d.flow && d.flow.length) {
        h += '<div class="flow"><div class="flow-hd">The day, roughly</div><ol>';
        d.flow.forEach(function (s) {
          h += '<li' + (s.fix ? ' class="fix"' : '') + '>' +
               '<span class="fw">' + esc(s.w) + '</span>' +
               '<span class="ft">' + esc(s.t) + '</span></li>';
        });
        h += '</ol><p class="flow-ft">Soft blocks, not a schedule — everything here has slack in it. ' +
             'Only the <b>marked</b> times are fixed: boats, shuttles, receptions, sunset and the ferry.</p>' +
             '</div>';
      }
      if (d.eat && ((d.eat.places && d.eat.places.length) || d.eat.note)) {
        h += '<div class="eat"><div class="eat-hd">Eating vegan today</div>';
        if (d.eat.places && d.eat.places.length) {
          h += '<ul class="eat-l">';
          d.eat.places.forEach(function (e) {
            var g = VEG[e.v] || VEG.ask;
            h += '<li><div class="eat-n">' + esc(e.n) +
                 '<span class="eat-b" style="background:' + g.c + '">' + esc(g.l) + '</span>' +
                 '<span class="eat-t">' + esc(e.town) + '</span></div>' +
                 '<div class="eat-x">' + esc(e.t) +
                 (e.lat ? ' <a target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=' +
                          e.lat + ',' + e.lon + '">map ↗</a>' : '') +
                 '</div></li>';
          });
          h += '</ul>';
        }
        if (d.eat.note) h += '<p class="eat-note">' + esc(d.eat.note) + '</p>';
        h += '</div>';
      }
      if (d.photos && d.photos.length) {
        h += '<div class="gal" role="list" aria-label="Photos from day ' + d.day + '">';
        d.photos.forEach(function (ph, i) {
          var stop = byId[ph.poi];
          var label = (stop ? stop.n : ph.cap);
          h += '<button class="gal-i" type="button" role="listitem" ' +
               'data-day="' + d.day + '" data-i="' + i + '" ' +
               'aria-label="Open photo: ' + esc(label) + '">' +
               '<img loading="lazy" decoding="async" alt="' + esc(label) + '" ' +
               'src="' + PDIR + esc(ph.f) + '-t.webp">' +
               '<span class="gal-cap">' + esc(label) + '</span></button>';
        });
        h += '</div>';
      }
      h += '<ul class="stoplist">';
      stops.forEach(function (p) {
        var c = CATS[p.c] || CATS.town;
        h += '<li><span class="ic" style="background:' + c.color + '">' + c.icon + '</span><div>';
        h += '<div class="nm">' + esc(p.n) + srcChip(p) +
             (p.f && p.f.length ? p.f.map(function (x) { return '<span class="tag">' + esc(TRAV[x] || x) + '</span>'; }).join('') : '') +
             '</div>';
        h += '<div class="tx">' + esc(p.t) + '</div>';
        var mt = [];
        if (p.time) mt.push('<b>Time:</b> ' + esc(p.time));
        if (p.vid) mt.push('<b>In the video:</b> ' + esc(p.vid));
        mt.push('<a href="#map-section" data-focus="' + p.id + '">Show on map →</a>');
        h += '<div class="meta">' + mt.join('') + '</div>';
        if (p.hike) {
          h += '<div class="note hike"><b>Hike:</b> ' + esc(p.hike.dist) + ' &middot; ' +
               esc(p.hike.up) + ' ascent &middot; ' + esc(p.hike.dur) + ' &middot; ' + esc(p.hike.grade) + '</div>';
        }
        if (p.van) {
          var warn = /NOT|CRITICAL|PINCH|not attempt|closed|void/i.test(p.van);
          h += '<div class="note' + (warn ? ' warn' : '') + '"><b>🚐 Van:</b> ' + esc(p.van) + '</div>';
        }
        h += '</div></li>';
      });
      h += '</ul>';

      if (camps.length || stays.length) {
        h += '<div class="sleep-row"><span class="k">Sleep</span>';
        var parts = camps.map(function (c) {
          return (c.w ? '<a target="_blank" rel="noopener" href="' + esc(c.w) + '">' + esc(c.n) + '</a>' : esc(c.n)) +
                 ' <span style="opacity:.55">' + esc(c.price) + '</span>';
        }).concat(stays.map(function (s) {
          return '🛏️ ' + (s.w ? '<a target="_blank" rel="noopener" href="' + esc(s.w) + '">' + esc(s.n) + '</a>' : esc(s.n));
        }));
        h += '<span>' + parts.join(' &nbsp;·&nbsp; ') + '</span>';
        var ci = (camps[0] || stays[0] || {}).checkin;
        if (ci) h += '<span class="ci">' + esc(ci) + '</span>';
        h += '</div>';
      }
      h += '</div></article>';
      box.insertAdjacentHTML('beforeend', h);
    });

    box.addEventListener('click', function (e) {
      var a = e.target.closest('[data-focus]');
      if (!a) return;
      var p = byId[a.dataset.focus];
      if (!p) return;
      offSet[p.c] = false;
      document.querySelectorAll('#chips .chip').forEach(function (b) {
        if (b.textContent.indexOf(CATS[p.c].label) === 0) { b.classList.add('on'); b.style.color = CATS[p.c].color; }
      });
      selectDay(p.d);
      setTimeout(function () {
        map.setView([p.lat, p.lon], 13, { animate: true });
        markers[p.id].openPopup();
      }, 480);
    });
  }

  /* ------------------------------------------------ lightbox */
  var lb = { day: null, i: 0, opener: null };

  function lbEl() { return document.getElementById('lightbox'); }

  function lbRender() {
    var day = T.days.filter(function (d) { return d.day === lb.day; })[0];
    if (!day) return;
    var ph = day.photos[lb.i];
    var stop = byId[ph.poi];
    var el = lbEl();
    el.querySelector('.lb-img').src = PDIR + ph.f + '.webp';
    el.querySelector('.lb-img').alt = (stop ? stop.n : ph.cap);
    el.querySelector('.lb-title').textContent = stop ? stop.n : ph.cap;
    el.querySelector('.lb-sub').textContent =
      'Day ' + day.day + ' · ' + day.title + '  ·  ' + (lb.i + 1) + ' / ' + day.photos.length;
    var cr = el.querySelector('.lb-credit');
    cr.innerHTML = 'Photo © ' + esc(ph.by) + ' — ' + esc(ph.lic) +
      (ph.src ? ' · <a target="_blank" rel="noopener" href="' + esc(ph.src) + '">Wikimedia Commons ↗</a>' : '');
  }

  function lbOpen(dayNum, i, opener) {
    lb.day = dayNum; lb.i = i; lb.opener = opener || null;
    var el = lbEl();
    el.hidden = false;
    document.body.style.overflow = 'hidden';
    lbRender();
    el.querySelector('.lb-close').focus();
  }

  function lbClose() {
    lbEl().hidden = true;
    document.body.style.overflow = '';
    if (lb.opener) { try { lb.opener.focus(); } catch (e) {} }
  }

  function lbStep(n) {
    var day = T.days.filter(function (d) { return d.day === lb.day; })[0];
    if (!day) return;
    lb.i = (lb.i + n + day.photos.length) % day.photos.length;
    lbRender();
  }

  function initLightbox() {
    var el = document.createElement('div');
    el.id = 'lightbox'; el.hidden = true;
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'true');
    el.setAttribute('aria-label', 'Photo viewer');
    el.innerHTML =
      '<div class="lb-back"></div>' +
      '<figure class="lb-box">' +
        '<img class="lb-img" alt="">' +
        '<figcaption>' +
          '<div class="lb-title"></div>' +
          '<div class="lb-sub"></div>' +
          '<div class="lb-credit"></div>' +
        '</figcaption>' +
        '<button class="lb-close" type="button" aria-label="Close photo viewer">✕</button>' +
        '<button class="lb-prev" type="button" aria-label="Previous photo">‹</button>' +
        '<button class="lb-next" type="button" aria-label="Next photo">›</button>' +
      '</figure>';
    document.body.appendChild(el);
    el.querySelector('.lb-back').onclick = lbClose;
    el.querySelector('.lb-close').onclick = lbClose;
    el.querySelector('.lb-prev').onclick = function (e) { e.stopPropagation(); lbStep(-1); };
    el.querySelector('.lb-next').onclick = function (e) { e.stopPropagation(); lbStep(1); };
    document.addEventListener('keydown', function (e) {
      if (lbEl().hidden) return;
      if (e.key === 'Escape') { e.preventDefault(); lbClose(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); lbStep(-1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); lbStep(1); }
    });
    /* swipe on touch */
    var x0 = null;
    el.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    el.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) lbStep(dx < 0 ? 1 : -1);
      x0 = null;
    }, { passive: true });
    /* open from any gallery thumb */
    var itin = document.getElementById('itinerary');
    if (!itin) return;
    itin.addEventListener('click', function (e) {
      var b = e.target.closest('.gal-i');
      if (!b) return;
      lbOpen(+b.dataset.day, +b.dataset.i, b);
    });
  }

  function buildStays() {
    var box = document.getElementById('stayGrid');
    if (!box) return;
    T.stays.forEach(function (s) {
      var bonus = !!s.bonus;
      var h = '<div class="card">';
      h += '<span class="rank' + (bonus ? ' alt' : '') + '">' + (bonus ? 'Bonus' : 'No. ' + s.rank) + '</span>';
      h += '<h3>' + esc(s.n) + '</h3>';
      var nightLbl = s.nights
        ? (/[–-]/.test(s.nights) ? 'Nights ' : 'Night ') + esc(s.nights)
        : 'Night ' + s.d;
      h += '<div class="sub">' + nightLbl +
           ' &middot; <span class="price">' + esc(s.price) + '</span></div>';
      h += '<p>' + esc(s.t) + '</p>';
      h += '<div class="why"><b>Why here, on this night</b>' + esc(s.why) + '</div>';
      if (s.checkin) h += '<div class="cicard">' + esc(s.checkin) + '</div>';
      var links = ['<a href="#map-section" data-focus="' + s.id + '">Show on map →</a>'];
      if (s.w) links.push('<a target="_blank" rel="noopener" href="' + esc(s.w) + '">Website ↗</a>');
      h += '<div class="meta" style="display:flex;gap:.9rem;font-size:.82rem;margin-top:.7rem">' + links.join('') + '</div>';
      h += '</div>';
      box.insertAdjacentHTML('beforeend', h);
    });
    box.addEventListener('click', focusHandler);
  }

  function focusHandler(e) {
    var a = e.target.closest('[data-focus]');
    if (!a) return;
    var p = byId[a.dataset.focus]; if (!p) return;
    offSet[p.c] = false; applyFilters();
    selectDay(p.d);
    setTimeout(function () { map.setView([p.lat, p.lon], 13); markers[p.id].openPopup(); }, 480);
  }

  function buildCampTable() {
    var tb = document.getElementById('campBody');
    if (!tb || !T.camps.length) return;
    T.camps.slice().sort(function (a, b) { return a.d - b.d; }).forEach(function (c) {
      var d = T.days.filter(function (x) { return x.day === c.d; })[0];
      tb.insertAdjacentHTML('beforeend',
        '<tr><td class="n">' + esc(c.n) + '<small>' + esc(c.t) + '</small></td>' +
        '<td><span class="badge b-d">Day ' + c.d + '</span><small>' + esc(d ? d.base : '') + '</small></td>' +
        '<td><span class="price">' + esc(c.price) + '</span>' +
        (c.checkin ? '<small>' + esc(c.checkin) + '</small>' : '') + '</td>' +
        '<td>' + (c.w ? '<a target="_blank" rel="noopener" href="' + esc(c.w) + '">' + esc(host(c.w)) + ' ↗</a>' : '<span style="color:var(--muted)">—</span>') +
        '<br><a href="#map-section" data-focus="' + c.id + '">map →</a></td>' +
        '<td><a target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=' + c.lat + ',' + c.lon + '">' +
        c.lat.toFixed(4) + ', ' + c.lon.toFixed(4) + ' ↗</a></td></tr>');
    });
    tb.closest('table').addEventListener('click', focusHandler);
  }

  function buildHikeTable() {
    var tb = document.getElementById('hikeBody');
    if (!tb) return;
    var hikes = T.pois.filter(function (p) { return p.hike; }).sort(function (a, b) { return a.d - b.d; });
    hikes.forEach(function (p) {
      var g = p.hike.grade, cls = /^Hard/i.test(g) ? 'b-hard' : /^Easy/i.test(g) ? 'b-easy' : 'b-mod';
      var short = g.split(/[;,—-]/)[0].trim();
      tb.insertAdjacentHTML('beforeend',
        '<tr><td class="n">' + esc(p.n) + '<small>Day ' + p.d + ' &middot; ' + esc(p.t.slice(0, 96)) + '…</small></td>' +
        '<td>' + esc(p.hike.dist) + '</td><td>' + esc(p.hike.up) + '</td><td>' + esc(p.hike.dur) + '</td>' +
        '<td><span class="badge ' + cls + '">' + esc(short) + '</span></td>' +
        '<td><a href="#map-section" data-focus="' + p.id + '">map →</a></td></tr>');
    });
    tb.closest('table').addEventListener('click', focusHandler);
  }

  function buildBeachList() {
    var box = document.getElementById('beachGrid');
    if (!box) return;
    T.pois.filter(function (p) { return p.c === 'beach' || p.c === 'swim'; })
      .sort(function (a, b) { return a.d - b.d; })
      .forEach(function (p) {
        box.insertAdjacentHTML('beforeend',
          '<div class="card"><h3>' + esc(p.n) + '</h3>' +
          '<div class="sub" style="color:' + CATS[p.c].color + '">' + CATS[p.c].icon + ' ' +
          (p.c === 'beach' ? 'Beach' : 'Freshwater') + ' &middot; Day ' + p.d + '</div>' +
          '<p>' + esc(p.t) + '</p>' +
          (p.van ? '<div class="note"><b>🚐</b> ' + esc(p.van) + '</div>' : '') +
          '<div style="margin-top:.7rem;font-size:.82rem"><a href="#map-section" data-focus="' + p.id + '">Show on map →</a></div></div>');
      });
    box.addEventListener('click', focusHandler);
  }

  function buildStats() {
    var km = T.days.reduce(function (a, d) { return a + d.km; }, 0);
    var mn = T.days.reduce(function (a, d) { return a + d.min; }, 0);
    var set = function (id, v) { var e = document.getElementById(id); if (e) e.textContent = v; };
    set('sDays', T.days.length);
    set('sKm', Math.round(km).toLocaleString('en-GB'));
    set('sDrive', (mn / 60).toFixed(0) + ' h');
    set('sStops', T.pois.length);
    set('sCamps', T.camps.length);
    set('sHikes', T.pois.filter(function (p) { return p.hike; }).length);
  }

  function navSpy() {
    var links = Array.prototype.slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
    var secs = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        var i = secs.indexOf(en.target);
        links.forEach(function (l, j) { l.classList.toggle('on', i === j); });
      });
    }, { rootMargin: '-64px 0px -70% 0px' });
    secs.forEach(function (s) { if (s) io.observe(s); });
  }

  document.addEventListener('DOMContentLoaded', function () {
    buildStats();
    buildChips();
    buildDayList();
    buildItinerary();
    buildStays();
    buildCampTable();
    buildHikeTable();
    buildBeachList();
    initLightbox();
    navSpy();
    if (window.L) {
      initMap();
      document.getElementById('mapReset').onclick = resetView;
    } else {
      document.getElementById('map').innerHTML =
        '<div style="padding:2rem;color:#fff;font:15px/1.6 var(--sans)">' +
        'The interactive map needs the Leaflet library and map tiles, which load from the internet. ' +
        'Everything else on this page works offline — the itinerary, campsites, hikes and coordinates are all below.</div>';
    }
  });
})();
