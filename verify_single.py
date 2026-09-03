from playwright.sync_api import sync_playwright
import json
errs=[]; fails=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1440,"height":950}, device_scale_factor=2)
    pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.on("requestfailed", lambda r: fails.append(r.url[:80]))
    pg.goto("file:///home/bogdan/corsica/corsica-van-trip.html", wait_until="load")
    pg.wait_for_timeout(8000)
    print(json.dumps(pg.evaluate("""()=>({
      days:document.querySelectorAll('.day-btn').length,
      chips:document.querySelectorAll('#chips .chip').length,
      stops:document.querySelectorAll('.stoplist li').length,
      camps:document.querySelectorAll('#campBody tr').length,
      hikes:document.querySelectorAll('#hikeBody tr').length,
      pins:document.querySelectorAll('.leaflet-marker-icon').length,
      tiles:document.querySelectorAll('.leaflet-tile-loaded').length,
      cluster:typeof L.markerClusterGroup,
      leaflet:typeof L
    })"""), indent=1))
    pg.click(".day-btn[data-day='14']"); pg.wait_for_timeout(2500)
    print("day-14 pins:", pg.evaluate("()=>document.querySelectorAll('.leaflet-marker-icon').length"))
    pg.evaluate("document.querySelector('#map-section').scrollIntoView()"); pg.wait_for_timeout(2500)
    pg.screenshot(path="shots/15-singlefile.png")
    b.close()
print("page errors:", errs or "none")
print("failed requests:", [f for f in fails] or "none")
