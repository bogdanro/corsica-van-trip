from playwright.sync_api import sync_playwright
import sys, json
errs, reqfail, console = [], [], []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":950}, device_scale_factor=2)
    pg.on("console", lambda m: console.append((m.type, m.text[:200])))
    pg.on("pageerror", lambda e: errs.append(str(e)[:300]))
    pg.on("requestfailed", lambda r: reqfail.append(r.url[:120]+" :: "+str(r.failure)[:80]))
    pg.goto("http://127.0.0.1:8765/index.html", wait_until="load", timeout=60000)
    pg.wait_for_timeout(6000)
    res = pg.evaluate("""() => ({
      days: document.querySelectorAll('.day-btn').length,
      chips: document.querySelectorAll('#chips .chip').length,
      itinDays: document.querySelectorAll('#itinerary .day').length,
      stops: document.querySelectorAll('.stoplist li').length,
      stayCards: document.querySelectorAll('#stayGrid .card').length,
      campRows: document.querySelectorAll('#campBody tr').length,
      hikeRows: document.querySelectorAll('#hikeBody tr').length,
      beachCards: document.querySelectorAll('#beachGrid .card').length,
      pins: document.querySelectorAll('.leaflet-marker-icon').length,
      paths: document.querySelectorAll('#map path').length,
      tiles: document.querySelectorAll('.leaflet-tile-loaded').length,
      statKm: (document.getElementById('sKm')||{}).textContent,
      statHikes: (document.getElementById('sHikes')||{}).textContent,
      leaflet: typeof window.L,
      docH: document.body.scrollHeight
    })""")
    print(json.dumps(res, indent=1))
    pg.screenshot(path="shots/01-hero.png", clip={"x":0,"y":0,"width":1440,"height":950})
    pg.evaluate("document.querySelector('#map-section').scrollIntoView()")
    pg.wait_for_timeout(3500)
    pg.screenshot(path="shots/02-map-all.png")
    # click day 7
    pg.click(".day-btn[data-day='7']"); pg.wait_for_timeout(2800)
    pg.screenshot(path="shots/03-map-day7.png")
    d7 = pg.evaluate("() => document.querySelectorAll('.leaflet-marker-icon').length")
    print("pins visible after selecting day 7:", d7)
    # open a popup
    pg.evaluate("document.querySelector('#mapReset').click()"); pg.wait_for_timeout(1500)
    pg.click(".day-btn[data-day='10']"); pg.wait_for_timeout(2500)
    ms = pg.query_selector_all(".leaflet-marker-icon")
    if ms:
        ms[0].click(); pg.wait_for_timeout(1200)
        pg.screenshot(path="shots/04-popup.png")
        print("popup open:", pg.evaluate("()=>!!document.querySelector('.leaflet-popup')"))
    # chip toggle
    pg.evaluate("document.querySelector('#mapReset').click()"); pg.wait_for_timeout(1200)
    before = pg.evaluate("()=>document.querySelectorAll('.leaflet-marker-icon').length")
    pg.query_selector_all("#chips .chip")[0].click(); pg.wait_for_timeout(800)
    after = pg.evaluate("()=>document.querySelectorAll('.leaflet-marker-icon').length")
    print("chip filter pins:", before, "->", after)
    # itinerary + other sections
    pg.evaluate("document.querySelector('#itinerary-section').scrollIntoView()"); pg.wait_for_timeout(900)
    pg.screenshot(path="shots/05-itinerary.png")
    pg.evaluate("document.querySelector('#stay').scrollIntoView()"); pg.wait_for_timeout(900)
    pg.screenshot(path="shots/06-hotels.png")
    pg.evaluate("document.querySelector('#camping').scrollIntoView()"); pg.wait_for_timeout(900)
    pg.screenshot(path="shots/07-camping.png")
    pg.evaluate("document.querySelector('#hikes').scrollIntoView()"); pg.wait_for_timeout(900)
    pg.screenshot(path="shots/08-hikes.png")
    pg.evaluate("document.querySelector('#logistics').scrollIntoView()"); pg.wait_for_timeout(900)
    pg.screenshot(path="shots/09-logistics.png")
    pg.evaluate("document.querySelector('#money').scrollIntoView()"); pg.wait_for_timeout(900)
    pg.screenshot(path="shots/10-budget.png")
    # mobile
    m = b.new_page(viewport={"width":390,"height":844}, device_scale_factor=2, is_mobile=True)
    m.goto("http://127.0.0.1:8765/index.html", wait_until="load"); m.wait_for_timeout(5000)
    m.screenshot(path="shots/11-mobile.png")
    m.evaluate("document.querySelector('#map-section').scrollIntoView()"); m.wait_for_timeout(2500)
    m.screenshot(path="shots/12-mobile-map.png")
    b.close()
print("\nPAGE ERRORS:", errs or "none")
print("FAILED REQUESTS:", reqfail or "none")
bad=[c for c in console if c[0] in ("error","warning")]
print("CONSOLE err/warn:", bad or "none")
