/* ==========================================================
   Corsica — day-by-day carousel view
   One day per slide: hero photo, mini map with start/finish
   flags, the running order, and the detail folded away.
   ========================================================== */
(function () {
  'use strict';
  var T = window.TRIP;
  var PDIR = 'assets/photos/';
  /* which long reference page this variant belongs to */
  var VARIANT = (location.search.match(/[?&]v=([a-z]+)/) || [])[1];
  var LONG = VARIANT === 'hotels' ? 'hotels.html'
           : VARIANT === 'paced'  ? 'paced.html' : 'van.html';

  var CATS = {
    town:     { c: '#c4562f', i: '🏘️' }, hike:  { c: '#3f7d3a', i: '🥾' },
    beach:    { c: '#2ea7ba', i: '🏖️' }, swim:  { c: '#1b8a9c', i: '💦' },
    view:     { c: '#7a4b8f', i: '🔭' }, heritage:{ c: '#8a6a3a', i: '🗿' },
    nature:   { c: '#2f6b4f', i: '🌿' }, culture:{ c: '#9a7b2f', i: '🍷' },
    port:     { c: '#5b6b78', i: '⚓' }, camp:  { c: '#2f6b2a', i: '⛺' },
    stay:     { c: '#b5305e', i: '🛏️' }, food:  { c: '#4a8a2b', i: '🌱' }
  };
  var VEG = { vegan: ['Fully vegan', '#2f6b2a'], options: ['Vegan options', '#4a8a2b'],
              ask: ['Veg-friendly — ask', '#8a6a3a'], shop: ['Shop / market', '#5b6b78'] };

  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (m) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m];
    });
  };
  var hrs = function (m) {
    var h = Math.floor(m / 60), r = m % 60;
    return (h ? h + ' h ' : '') + (r ? r + ' min' : (h ? '' : '0 min'));
  };

  function srcChip(p) {
    if (typeof p.src !== 'number') return '';
    var cls = p.src >= 7 ? 'hi' : p.src >= 4 ? 'mid' : 'lo';
    var txt = p.src >= 1 ? p.src + '/10' : (p.vid ? "film's find" : 'unlisted');
    return '<span class="srcchip ' + cls + '">' + esc(txt) + '</span>';
  }

  /* stops belonging to each day, in the categories we want on a mini map */
  var byDay = {};
  T.pois.forEach(function (p) { (byDay[p.d] = byDay[p.d] || []).push(p); });
  var campByDay = {}, stayByDay = {};
  (T.camps || []).forEach(function (c) { (campByDay[c.d] = campByDay[c.d] || []).push(c); });
  (T.stays || []).forEach(function (s) { (stayByDay[s.d] = stayByDay[s.d] || []).push(s); });

  var maps = {};       // day -> Leaflet map, created lazily
  var current = 1;

  /* ---------------------------------------------------- build */
  function slideHtml(d) {
    var stops = (byDay[d.day] || []).filter(function (p) { return p.c !== 'food'; });
    var hero = d.photos && d.photos[0];
    var h = '<article class="slide" id="d' + d.day + '" data-day="' + d.day + '">';

    /* hero */
    h += '<header class="sl-hero' + (hero ? '' : ' nohero') + '">';
    if (hero) h += '<img class="sl-heroimg" loading="lazy" alt="" src="' + PDIR + esc(hero.f) + '.webp">';
    h += '<div class="sl-heroin"><span class="sl-day">Day ' + d.day + ' of ' + T.days.length + '</span>' +
         '<h2>' + esc(d.title) + '</h2><p>' + esc(d.theme) + '</p></div></header>';

    /* two columns: map + facts | running order */
    h += '<div class="sl-body"><div class="sl-left">';
    h += '<div class="sl-map" id="map' + d.day + '" aria-label="Route map for day ' + d.day + '"></div>';
    h += '<dl class="sl-facts">' +
         '<div><dt>Drive</dt><dd>' + d.km + ' km · ' + hrs(d.min) + '</dd></div>' +
         (d.bed ? '<div><dt>Be in by</dt><dd>' + esc(d.bed) + '</dd></div>' : '') +
         '<div><dt>Sleep</dt><dd>' + esc(d.base) + '</dd></div>' +
         '</dl>';
    var sleeps = (campByDay[d.day] || []).concat(stayByDay[d.day] || []);
    if (sleeps.length) {
      h += '<p class="sl-sleep">' + sleeps.map(function (s) {
        return s.w ? '<a target="_blank" rel="noopener" href="' + esc(s.w) + '">' + esc(s.n) + '</a>' : esc(s.n);
      }).join(' · ') + '</p>';
    }
    h += '<a class="sl-full" href="' + LONG + '#day' + d.day + '">Full detail for this day ↗</a>';
    h += '</div><div class="sl-right">';

    h += '<p class="sl-intro">' + esc(d.intro) + '</p>';
    if (d.flow && d.flow.length) {
      h += '<ol class="sl-flow">';
      d.flow.forEach(function (s) {
        h += '<li' + (s.fix ? ' class="fix"' : '') + '><span class="w">' + esc(s.w) +
             '</span><span class="t">' + esc(s.t) + '</span></li>';
      });
      h += '</ol>';
    }
    h += '</div></div>';

    /* photo strip */
    if (d.photos && d.photos.length > 1) {
      h += '<div class="sl-strip">';
      d.photos.forEach(function (ph, i) {
        h += '<button class="sl-th" data-day="' + d.day + '" data-i="' + i + '" type="button" ' +
             'aria-label="Open photo ' + (i + 1) + '"><img loading="lazy" alt="" src="' +
             PDIR + esc(ph.f) + '-t.webp"></button>';
      });
      h += '</div>';
    }

    /* folded detail */
    h += '<div class="sl-more">';
    if (stops.length) {
      h += '<details><summary>Stops <b>' + stops.length + '</b></summary><ul class="sl-stops">';
      stops.forEach(function (p) {
        var c = CATS[p.c] || CATS.town;
        h += '<li><span class="ic" style="background:' + c.c + '">' + c.i + '</span><div>' +
             '<b>' + esc(p.n) + '</b>' + srcChip(p) +
             (p.time ? ' <i>' + esc(p.time) + '</i>' : '') +
             '<span>' + esc(p.t) + '</span>' +
             (p.hike ? '<span class="mini hike">🥾 ' + esc(p.hike.dist) + ' · ' + esc(p.hike.up) +
                       ' · ' + esc(p.hike.dur) + ' · ' + esc(p.hike.grade) + '</span>' : '') +
             (p.van ? '<span class="mini van">🚐 ' + esc(p.van) + '</span>' : '') +
             '</div></li>';
      });
      h += '</ul></details>';
    }
    var eat = d.eat || {};
    if ((eat.places && eat.places.length) || eat.note) {
      h += '<details><summary>Eating vegan <b>' + ((eat.places || []).length || '—') + '</b></summary><ul class="sl-eat">';
      (eat.places || []).forEach(function (e) {
        var g = VEG[e.v] || VEG.ask;
        h += '<li><b>' + esc(e.n) + '</b><span class="tag" style="background:' + g[1] + '">' + esc(g[0]) + '</span>' +
             '<i>' + esc(e.town) + '</i><span>' + esc(e.t) + '</span></li>';
      });
      h += '</ul>' + (eat.note ? '<p class="sl-eatnote">' + esc(eat.note) + '</p>' : '') + '</details>';
    }
    h += '</div></article>';
    return h;
  }

  /* ---------------------------------------------------- mini map */
  function flag(kind) {
    var o = { start: ['#2f6b2a', '⚑'], end: ['#c4562f', '🏁'], both: ['#7a4b8f', '⚑'] }[kind];
    return L.divIcon({ className: 'flagw', iconSize: [30, 30], iconAnchor: [15, 30],
      html: '<div class="flag" style="background:' + o[0] + '"><span>' + o[1] + '</span></div>' });
  }

  function initMap(day) {
    if (maps[day] || !window.L) return;
    var d = T.days.filter(function (x) { return x.day === day; })[0];
    if (!d || !d.geometry.length) return;
    var el = document.getElementById('map' + day);
    if (!el) return;
    var m = L.map(el, {
      zoomControl: false, attributionControl: true,
      dragging: false, scrollWheelZoom: false, doubleClickZoom: false,
      boxZoom: false, keyboard: false, touchZoom: false, tap: false
    });
    L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
      maxZoom: 17, subdomains: 'abc',
      attribution: '&copy; <a href="https://opentopomap.org">OpenTopoMap</a>'
    }).addTo(m);

    L.polyline(d.geometry, { color: '#fff', weight: 7, opacity: .85, lineCap: 'round' }).addTo(m);
    L.polyline(d.geometry, { color: '#d64d1f', weight: 3.5, opacity: 1, lineCap: 'round' }).addTo(m);

    var b = L.latLngBounds(d.geometry);
    (byDay[day] || []).forEach(function (p) {
      var c = CATS[p.c] || CATS.town;
      L.marker([p.lat, p.lon], { icon: L.divIcon({ className: 'dotw', iconSize: [16, 16],
        html: '<i class="dot" style="background:' + c.c + '"></i>' }), interactive: false }).addTo(m);
      b.extend([p.lat, p.lon]);
    });

    var s = d.geometry[0], e = d.geometry[d.geometry.length - 1];
    var loop = Math.abs(s[0] - e[0]) < 0.004 && Math.abs(s[1] - e[1]) < 0.004;
    if (loop) {
      L.marker(s, { icon: flag('both'), title: 'Start and finish', interactive: false }).addTo(m);
    } else {
      L.marker(s, { icon: flag('start'), title: 'Start', interactive: false }).addTo(m);
      L.marker(e, { icon: flag('end'), title: 'Finish', interactive: false }).addTo(m);
    }
    m.fitBounds(b, { padding: [28, 28] });
    maps[day] = m;
    setTimeout(function () { m.invalidateSize(); m.fitBounds(b, { padding: [28, 28] }); }, 260);
  }

  /* ---------------------------------------------------- navigation */
  var deck;
  function go(day, smooth) {
    day = Math.max(1, Math.min(T.days.length, day));
    var el = document.getElementById('d' + day);
    if (!el) return;
    deck.scrollTo({ left: el.offsetLeft, behavior: smooth === false ? 'auto' : 'smooth' });
    setActive(day);
  }
  function setActive(day) {
    if (current === day && maps[day]) return;
    current = day;
    document.querySelectorAll('.rail-d').forEach(function (b) {
      var on = +b.dataset.day === day;
      b.classList.toggle('on', on);
      if (on) b.scrollIntoView({ block: 'nearest', inline: 'nearest' });
    });
    var p = document.getElementById('prog');
    if (p) p.style.width = (day / T.days.length * 100) + '%';
    var lbl = document.getElementById('poslbl');
    if (lbl) lbl.textContent = day + ' / ' + T.days.length;
    initMap(day);
    initMap(day + 1); initMap(day - 1);       // pre-warm neighbours
    if (history.replaceState) history.replaceState(null, '', '#d' + day);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var v = VARIANT;
    var sw = document.getElementById('deckver');
    if (sw) {
      var VARIANTS = [['', '🚐 Van'], ['hotels', '🛏 Hotels'], ['paced', '🐢 Unrushed']];
      sw.innerHTML = VARIANTS.map(function (x) {
        var on = (v || '') === x[0] ? ' class="on"' : '';
        return '<a href="' + (x[0] ? '?v=' + x[0] : './') + '"' + on + '>' + x[1] + '</a>';
      }).join('');
    }
    document.querySelectorAll('[data-ref]').forEach(function (a) {
      a.href = LONG + '#' + a.dataset.ref;
    });

    deck = document.getElementById('deck');
    var rail = document.getElementById('rail');
    T.days.forEach(function (d) {
      deck.insertAdjacentHTML('beforeend', slideHtml(d));
      rail.insertAdjacentHTML('beforeend',
        '<button class="rail-d" type="button" data-day="' + d.day + '">' +
        '<span class="n">' + d.day + '</span><span class="x"><b>' + esc(d.title) + '</b>' +
        '<i>' + d.km + ' km · ' + esc(d.base) + '</i></span></button>');
    });
    rail.addEventListener('click', function (e) {
      var b = e.target.closest('.rail-d'); if (b) go(+b.dataset.day);
    });
    document.getElementById('prev').onclick = function () { go(current - 1); };
    document.getElementById('next').onclick = function () { go(current + 1); };
    document.addEventListener('keydown', function (e) {
      if (e.target.closest('input,textarea') || !document.getElementById('lightbox').hidden) return;
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(current - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); go(current + 1); }
    });

    /* keep the rail in sync with native swipe / scroll */
    var t = null;
    deck.addEventListener('scroll', function () {
      clearTimeout(t);
      t = setTimeout(function () {
        var i = Math.round(deck.scrollLeft / deck.clientWidth) + 1;
        setActive(Math.max(1, Math.min(T.days.length, i)));
      }, 90);
    }, { passive: true });

    initLightbox();
    var start = +(location.hash.match(/#d(\d+)/) || [])[1] || 1;
    go(start, false);
    setTimeout(function () { go(start, false); }, 120);
  });

  /* ---------------------------------------------------- lightbox */
  var lb = { day: 1, i: 0 };
  function lbEl() { return document.getElementById('lightbox'); }
  function lbRender() {
    var d = T.days.filter(function (x) { return x.day === lb.day; })[0];
    var ph = d.photos[lb.i], el = lbEl();
    el.querySelector('.lb-img').src = PDIR + ph.f + '.webp';
    el.querySelector('.lb-title').textContent = ph.cap;
    el.querySelector('.lb-sub').textContent = 'Day ' + d.day + ' · ' + (lb.i + 1) + ' / ' + d.photos.length;
    el.querySelector('.lb-credit').innerHTML = 'Photo © ' + esc(ph.by) + ' — ' + esc(ph.lic) +
      (ph.src ? ' · <a target="_blank" rel="noopener" href="' + esc(ph.src) + '">Commons ↗</a>' : '');
  }
  function initLightbox() {
    var el = document.createElement('div');
    el.id = 'lightbox'; el.hidden = true;
    el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true');
    el.innerHTML = '<div class="lb-back"></div><figure class="lb-box"><img class="lb-img" alt="">' +
      '<figcaption><div class="lb-title"></div><div class="lb-sub"></div><div class="lb-credit"></div></figcaption>' +
      '<button class="lb-close" type="button" aria-label="Close">✕</button>' +
      '<button class="lb-prev" type="button" aria-label="Previous">‹</button>' +
      '<button class="lb-next" type="button" aria-label="Next">›</button></figure>';
    document.body.appendChild(el);
    var close = function () { el.hidden = true; document.body.style.overflow = ''; };
    var step = function (n) {
      var d = T.days.filter(function (x) { return x.day === lb.day; })[0];
      lb.i = (lb.i + n + d.photos.length) % d.photos.length; lbRender();
    };
    el.querySelector('.lb-back').onclick = close;
    el.querySelector('.lb-close').onclick = close;
    el.querySelector('.lb-prev').onclick = function (e) { e.stopPropagation(); step(-1); };
    el.querySelector('.lb-next').onclick = function (e) { e.stopPropagation(); step(1); };
    document.addEventListener('keydown', function (e) {
      if (el.hidden) return;
      if (e.key === 'Escape') { e.preventDefault(); close(); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
    });
    document.getElementById('deck').addEventListener('click', function (e) {
      var b = e.target.closest('.sl-th'); if (!b) return;
      lb.day = +b.dataset.day; lb.i = +b.dataset.i;
      el.hidden = false; document.body.style.overflow = 'hidden';
      lbRender(); el.querySelector('.lb-close').focus();
    });
  }
})();
