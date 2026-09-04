from playwright.sync_api import sync_playwright
SECS=[("stay","06-hotels"),("camping","07-camping"),("hikes","08-hikes"),
      ("water","08b-beaches"),("logistics","09-logistics"),("money","10-budget")]
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={"width":1440,"height":950}, device_scale_factor=2)
    pg.goto("http://127.0.0.1:8765/van.html", wait_until="load")
    pg.add_style_tag(content="html{scroll-behavior:auto!important}*{animation:none!important;transition:none!important}")
    pg.wait_for_timeout(4000)
    for sid,name in SECS:
        y=pg.evaluate(f"()=>document.getElementById('{sid}').getBoundingClientRect().top+window.scrollY")
        pg.evaluate(f"window.scrollTo(0,{y}-70)")
        pg.wait_for_timeout(1400)
        pg.screenshot(path=f"shots/{name}.png")
    # footer
    pg.evaluate("window.scrollTo(0,document.body.scrollHeight)"); pg.wait_for_timeout(1200)
    pg.screenshot(path="shots/13-footer.png")
    # full-page tall render of one itinerary day for proof
    m=b.new_page(viewport={"width":390,"height":844}, device_scale_factor=2, is_mobile=True)
    m.goto("http://127.0.0.1:8765/van.html", wait_until="load"); m.wait_for_timeout(5000)
    m.add_style_tag(content="html{scroll-behavior:auto!important}")
    m.screenshot(path="shots/11-mobile.png")
    y=m.evaluate("()=>document.getElementById('map-section').getBoundingClientRect().top+window.scrollY")
    m.evaluate(f"window.scrollTo(0,{y}-60)"); m.wait_for_timeout(3000)
    m.screenshot(path="shots/12-mobile-map.png")
    y=m.evaluate("()=>document.getElementById('camping').getBoundingClientRect().top+window.scrollY")
    m.evaluate(f"window.scrollTo(0,{y}-60)"); m.wait_for_timeout(1200)
    m.screenshot(path="shots/14-mobile-camping.png")
    b.close()
print("shots done")
