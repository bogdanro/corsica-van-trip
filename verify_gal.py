from playwright.sync_api import sync_playwright

def click_top_marker(pg, timeout=6000):
    """Click the first marker that is genuinely the top element at its own centre.

    Map pins overlap by nature, so picking `.first` in DOM order can land on one
    that is underneath another. This keeps Playwright's real hit-testing (so a
    genuine overlay bug would still fail) while tolerating normal pin overlap.
    """
    pg.wait_for_timeout(1200)                      # let fitBounds settle
    idx = pg.evaluate("""() => {
      const ms=[...document.querySelectorAll('.leaflet-marker-icon')];
      for (let i=0;i<ms.length;i++){
        const r=ms[i].getBoundingClientRect();
        const el=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
        if (el && (el===ms[i] || ms[i].contains(el))) return i;
      }
      return -1;
    }""")
    if idx < 0: return False
    pg.locator(".leaflet-marker-icon").nth(idx).click(timeout=timeout)
    return True


import json
errs=[];fails=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1440,"height":950}, device_scale_factor=2)
    pg.on("pageerror", lambda e: errs.append(str(e)[:220]))
    pg.on("requestfailed", lambda r: fails.append(r.url.split('/')[-1][:60]+" :: "+str(r.failure)[:50]))
    pg.goto("http://127.0.0.1:8765/van.html", wait_until="load"); pg.wait_for_timeout(6000)
    pg.add_style_tag(content="html{scroll-behavior:auto!important}")
    print(json.dumps(pg.evaluate("""()=>({
      galleries:document.querySelectorAll('.gal').length,
      thumbs:document.querySelectorAll('.gal-i').length,
      lightbox:!!document.getElementById('lightbox'),
      lbHidden:document.getElementById('lightbox').hidden
    })"""), indent=1))
    # scroll to day 7 gallery, force-load images
    y=pg.evaluate("()=>document.getElementById('day7').getBoundingClientRect().top+window.scrollY")
    pg.evaluate(f"window.scrollTo(0,{y}-80)"); pg.wait_for_timeout(2500)
    print("imgs loaded (naturalWidth>0) in view:", pg.evaluate(
      "()=>[...document.querySelectorAll('#day7 .gal-i img')].map(i=>i.naturalWidth)"))
    pg.screenshot(path="shots/17-gallery.png")
    # open lightbox
    pg.click("#day7 .gal-i >> nth=0"); pg.wait_for_timeout(1800)
    print("lightbox open:", pg.evaluate("()=>!document.getElementById('lightbox').hidden"))
    print("caption:", pg.evaluate("()=>document.querySelector('.lb-title').textContent"))
    print("credit :", pg.evaluate("()=>document.querySelector('.lb-credit').textContent")[:90])
    print("img w  :", pg.evaluate("()=>document.querySelector('.lb-img').naturalWidth"))
    pg.screenshot(path="shots/18-lightbox.png")
    # next / prev / esc
    pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(900)
    print("after →:", pg.evaluate("()=>document.querySelector('.lb-sub').textContent"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(600)
    print("closed by Esc:", pg.evaluate("()=>document.getElementById('lightbox').hidden"))
    # popup photo
    y=pg.evaluate("()=>document.getElementById('map-section').getBoundingClientRect().top+window.scrollY")
    pg.evaluate(f"window.scrollTo(0,{y}-60)"); pg.wait_for_timeout(2500)
    pg.click(".day-btn[data-day='12']"); pg.wait_for_timeout(2500)
    if click_top_marker(pg):
        pg.wait_for_timeout(1500)
        print("popup has photo:", pg.evaluate("()=>!!document.querySelector('.pp-img img')"),
              "| loaded:", pg.evaluate("()=>{const i=document.querySelector('.pp-img img');return i?i.naturalWidth:0}"))
        pg.screenshot(path="shots/19-popup-photo.png")
    b.close()
print("page errors:", errs or "none")
print("failed requests:", fails or "none")
