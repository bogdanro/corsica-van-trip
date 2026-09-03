# -*- coding: utf-8 -*-
"""Inline CSS + JS into one self-contained HTML file."""
import io, re

html = io.open("index.html", encoding="utf-8").read()
css  = io.open("assets/css/style.css", encoding="utf-8").read()
data = io.open("assets/js/data.js", encoding="utf-8").read()
app  = io.open("assets/js/app.js", encoding="utf-8").read()

# swap unpkg -> cdnjs (cdnjs is the CDN allowed inside claude.ai artifacts)
html = html.replace(
  '''<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
      integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css">''',
  '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/MarkerCluster.min.css">''')
html = html.replace('<link rel="preconnect" href="https://unpkg.com">',
                    '<link rel="preconnect" href="https://cdnjs.cloudflare.com">')
html = html.replace(
  '''<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>''',
  '''<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>''')
html = html.replace(
  '<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>',
  '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.markercluster/1.5.3/leaflet.markercluster.min.js"></script>')

# inline the local stylesheet
html = html.replace('<link rel="stylesheet" href="assets/css/style.css">',
                    '<style>\n' + css + '\n</style>')

# inline the local scripts (guard against a stray </script> in the data)
def guard(s): return s.replace('</script>', '<\\/script>')
html = html.replace('<script src="assets/js/data.js"></script>',
                    '<script>\n' + guard(data) + '\n</script>')
html = html.replace('<script src="assets/js/app.js"></script>',
                    '<script>\n' + guard(app) + '\n</script>')

assert 'assets/' not in html, "a local asset reference survived: " + \
    str(re.findall(r'[^"\']*assets/[^"\']*', html))
assert 'unpkg.com' not in html, "unpkg reference survived"

io.open("corsica-van-trip.html", "w", encoding="utf-8").write(html)
print("corsica-van-trip.html  %.0f KB" % (len(html.encode()) / 1024))
print("external deps left:", sorted(set(re.findall(r'https://([a-z0-9.-]+)/', html))))
