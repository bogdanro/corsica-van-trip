"""Checks for the day-by-day carousel view — now the landing page."""
from playwright.sync_api import sync_playwright
import json, sys

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765"
fails = []

def check(cond, label, extra=""):
    print(("  PASS  " if cond else "  FAIL  ") + label + ("  " + str(extra) if extra else ""))
    if not cond: fails.append(label)

with sync_playwright() as p:
    b = p.chromium.launch()
    for variant, q in (("van", ""), ("hotels", "?v=hotels")):
        errs, reqfail = [], []
        pg = b.new_page(viewport={"width": 1440, "height": 900})
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        pg.on("requestfailed", lambda r: reqfail.append(r.url.split("/")[-1][:40]))
        pg.goto(f"{BASE}/index.html{q}#d7", wait_until="load", timeout=60000)
        pg.wait_for_timeout(7000)
        print(f"\n=== {variant} ===")
        r = pg.evaluate("""()=>({
          slides:document.querySelectorAll('.slide').length,
          rail:document.querySelectorAll('.rail-d').length,
          maps:document.querySelectorAll('.sl-map.leaflet-container').length,
          flows:document.querySelectorAll('.sl-flow').length,
          flags:document.querySelectorAll('#d7 .flag').length,
          routes:document.querySelectorAll('#d7 .sl-map path').length,
          active:document.querySelector('.rail-d.on').dataset.day,
          pos:document.getElementById('poslbl').textContent.trim(),
          overflow:document.documentElement.scrollWidth<=innerWidth
        })""")
        days = 16
        check(r["slides"] == days, "all days rendered", r["slides"])
        check(r["rail"] == days, "rail complete", r["rail"])
        check(r["flows"] == days, "running order on every day", r["flows"])
        check(r["maps"] >= 1, "mini maps initialise lazily", r["maps"])
        check(r["flags"] >= 1, "start/finish flags on day 7", r["flags"])
        check(r["routes"] >= 2, "route drawn on the mini map", r["routes"])
        check(r["active"] == "7", "deep link #d7 selects day 7", r["active"])
        check(r["overflow"], "no horizontal overflow")

        pg.click("#next"); pg.wait_for_timeout(1600)
        check(pg.evaluate("()=>document.getElementById('poslbl').textContent.trim()") == "8 / 16", "next advances")
        pg.keyboard.press("ArrowLeft"); pg.wait_for_timeout(1600)
        check(pg.evaluate("()=>document.getElementById('poslbl').textContent.trim()") == "7 / 16", "arrow keys work")
        pg.click(".rail-d[data-day='12']"); pg.wait_for_timeout(1800)
        check(pg.evaluate("()=>document.getElementById('poslbl').textContent.trim()") == "12 / 16", "rail jump works")

        pg.click("#d12 .sl-th >> nth=0"); pg.wait_for_timeout(1400)
        check(pg.evaluate("()=>!document.getElementById('lightbox').hidden"), "lightbox opens from strip")
        check(bool(pg.evaluate("()=>document.querySelector('.lb-credit').textContent.trim()")), "photo credit shown")
        pg.keyboard.press("Escape"); pg.wait_for_timeout(600)
        check(pg.evaluate("()=>document.getElementById('lightbox').hidden"), "lightbox closes on Esc")

        pg.click("#d12 .sl-more details:first-of-type summary"); pg.wait_for_timeout(600)
        check(pg.evaluate("()=>document.querySelector('#d12 .sl-more details').open"), "folded detail expands")
        check(not errs, "no console errors", errs)
        check(not reqfail, "no failed requests", reqfail)
        pg.close()

    # narrow viewport
    m = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    m.goto(f"{BASE}/index.html#d7", wait_until="load"); m.wait_for_timeout(6000)
    print("\n=== mobile 390 ===")
    r = m.evaluate("""()=>({ovf:document.documentElement.scrollWidth<=innerWidth,
        w:Math.round(document.querySelector('#d7').getBoundingClientRect().width), vw:innerWidth,
        railScrolled:document.querySelector('.rail-list').scrollLeft>0,
        maps:document.querySelectorAll('.sl-map.leaflet-container').length})""")
    check(r["ovf"], "no horizontal overflow at 390px")
    check(r["w"] == r["vw"], "slide matches viewport width", f'{r["w"]} vs {r["vw"]}')
    check(r["railScrolled"], "rail scrolls to the active day")
    check(r["maps"] >= 1, "maps render on mobile", r["maps"])
    b.close()

print("\n" + ("ALL PASS" if not fails else f"{len(fails)} FAILURE(S): {fails}"))
sys.exit(1 if fails else 0)
