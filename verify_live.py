from playwright.sync_api import sync_playwright
import json
errs=[]; fails=[]
URL="https://bogdanro.github.io/corsica-van-trip/"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1440,"height":950}, device_scale_factor=2)
    pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.on("requestfailed", lambda r: fails.append(r.url[:90]+" :: "+str(r.failure)[:60]))
    pg.goto(URL, wait_until="load", timeout=60000)
    pg.wait_for_timeout(9000)
    print(json.dumps(pg.evaluate("""()=>({
      title:document.title.slice(0,42),
      days:document.querySelectorAll('.day-btn').length,
      chips:document.querySelectorAll('#chips .chip').length,
      stops:document.querySelectorAll('.stoplist li').length,
      camps:document.querySelectorAll('#campBody tr').length,
      hikes:document.querySelectorAll('#hikeBody tr').length,
      beaches:document.querySelectorAll('#beachGrid .card').length,
      hotels:document.querySelectorAll('#stayGrid .card').length,
      pins:document.querySelectorAll('.leaflet-marker-icon').length,
      tiles:document.querySelectorAll('.leaflet-tile-loaded').length,
      https:location.protocol
    })"""), indent=1))
    pg.click(".day-btn[data-day='10']"); pg.wait_for_timeout(2500)
    print("day-10 pins:", pg.evaluate("()=>document.querySelectorAll('.leaflet-marker-icon').length"))
    ms=pg.query_selector_all(".leaflet-marker-icon")
    if ms:
        ms[0].click(); pg.wait_for_timeout(1200)
        print("popup opens:", pg.evaluate("()=>!!document.querySelector('.leaflet-popup')"))
    pg.evaluate("document.querySelector('#map-section').scrollIntoView()"); pg.wait_for_timeout(2500)
    pg.screenshot(path="shots/16-live.png")
    b.close()
print("page errors:", errs or "none")
print("failed requests:", fails or "none")
