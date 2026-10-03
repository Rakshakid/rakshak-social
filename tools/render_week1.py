"""Render Rakshak ID Week 1 social images (1080x1350 feed, 1080x1920 stories)."""
import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out"; OUT.mkdir(exist_ok=True)
A = (ROOT / "assets").as_uri()

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#07090D;--ivory:#F6F1E7;--muted:#B9BDC7;--gold:#E8B547;--gold-hi:#F6DFA6;--line:rgba(232,181,71,.30)}
html,body{width:__W__;height:__H__;background:var(--bg);overflow:hidden}
body{font-family:'DM Sans',sans-serif;color:var(--ivory);position:relative}
.glow{position:absolute;inset:0;background:radial-gradient(ellipse 70% 45% at 50% 0%,rgba(232,181,71,.16),transparent 70%),radial-gradient(ellipse 60% 40% at 50% 110%,rgba(232,181,71,.08),transparent 70%)}
.frame{position:absolute;inset:28px;border:1.5px solid var(--line);border-radius:44px}
.page{position:absolute;inset:28px;padding:84px 86px;display:flex;flex-direction:column}
.top{display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:22px}
.brand img{width:112px;height:112px;border-radius:26px;box-shadow:0 0 50px rgba(232,181,71,.28);border:1px solid var(--line)}
.brand b{font-family:'Playfair Display',serif;font-weight:700;letter-spacing:.3em;font-size:34px;color:var(--gold-hi)}
.brand i{font-style:normal;font-family:'DM Sans';font-weight:800;font-size:22px;background:linear-gradient(135deg,#F6DFA6,#E8B547);color:#07090D;padding:3px 9px;border-radius:7px;letter-spacing:.04em;margin-left:-6px}
.tag{font-family:'DM Mono',monospace;font-size:21px;letter-spacing:.18em;color:var(--gold);text-transform:uppercase}
.mid{flex:1;display:flex;flex-direction:column;justify-content:center}
.eyebrow{font-family:'DM Mono',monospace;font-size:24px;letter-spacing:.2em;color:var(--gold);text-transform:uppercase;margin-bottom:34px}
h1{font-family:'Playfair Display',serif;font-weight:700;font-size:84px;line-height:1.08;letter-spacing:-.01em}
h1 em,h2 em{font-style:italic;color:var(--gold)}
h2{font-family:'Playfair Display',serif;font-weight:700;font-size:66px;line-height:1.14}
p.body{font-size:36px;line-height:1.5;color:var(--muted);margin-top:38px}
p.body b{color:var(--ivory);font-weight:700}
.hi{font-family:'Tiro Devanagari Hindi',serif;font-size:38px;line-height:1.5;color:var(--gold-hi);margin-top:30px}
.rule{width:96px;height:3px;background:linear-gradient(90deg,#F6DFA6,#E8B547);margin:44px 0 0}
.foot{display:flex;align-items:center;justify-content:space-between;font-family:'DM Mono',monospace;font-size:20px;letter-spacing:.14em;color:#8A8F9C;text-transform:uppercase}
.swipe{color:var(--gold)}
.cta{display:inline-block;margin-top:48px;padding:26px 52px;border-radius:999px;background:linear-gradient(135deg,#F6DFA6,#E8B547);color:#07090D;font-weight:800;font-size:34px;box-shadow:0 0 60px rgba(232,181,71,.35)}
.list{margin-top:40px;display:flex;flex-direction:column;gap:22px}
.list div{font-size:38px;color:var(--ivory);padding-left:44px;position:relative;line-height:1.35}
.list div:before{content:'';position:absolute;left:0;top:20px;width:20px;height:2px;background:var(--gold)}
.center{align-items:center;text-align:center}
.big-num{font-family:'Playfair Display',serif;font-weight:800;font-size:300px;line-height:1;background:linear-gradient(180deg,#F6DFA6,#E8B547);-webkit-background-clip:text;color:transparent}
"""

def page(body, w=1080, h=1350, extra=""):
    css = CSS.replace("__W__", f"{w}px").replace("__H__", f"{h}px")
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}{extra}</style></head><body><div class='glow'></div><div class='frame'></div><div class='page'>{body}</div></body></html>"

def top(tag):
    return f"<div class='top'><div class='brand'><img src='{A}/lion.png'><b>RAKSHAK</b><i>ID</i></div><div class='tag'>{tag}</div></div>"

def foot(left, right="", swipe=False):
    r = f"<span class='swipe'>Swipe →</span>" if swipe else f"<span>{right}</span>"
    return f"<div class='foot'><span>{left}</span>{r}</div>"

CTA_SLIDE = lambda tag, n: page(top(tag) + f"""
<div class='mid center'>
  <img src='{A}/lion.png' style='width:150px;height:150px;border-radius:34px;border:1px solid rgba(232,181,71,.4);box-shadow:0 0 80px rgba(232,181,71,.3);margin:0 auto 46px'>
  <h2>You stood for Bharat.<br><em>Now Bharat stands with you.</em></h2>
  <div class='hi'>आप भारत के लिए खड़े रहे। अब भारत आपके साथ खड़ा है।</div>
  <p class='body' style='margin-top:30px'>Register early — early members get <b>extra privileges</b> at launch.</p>
  <div><span class='cta'>Register · rakshakid.com</span></div>
</div>""" + foot(n, "App launch · Vijay Diwas · 16 Dec"))

SERIES = "Culture of Gratitude"

slides = {}

# ---------- Post 1: Carousel — THE WORLD ----------
p1 = [
 page(top("Part 1 of 6") + """
<div class='mid'>
  <div class='eyebrow'>Part 1 · The World</div>
  <h1>In many nations, a veteran hears <em>“Thank you for your service”</em> every day.</h1>
  <p class='body'>In Bharat, we say it on a few days of the year.</p>
</div>""" + foot("rakshakid.com", swipe=True)),
 page(top("Part 1 of 6") + """
<div class='mid'>
  <h2>There, gratitude is a <em>habit.</em><br>Not a ceremony.</h2>
  <div class='list'><div>At the shop counter</div><div>At the hospital desk</div><div>In the school queue</div><div>At the airport gate</div></div>
  <p class='body'>Small, everyday acts that say: <b>we remember what you gave.</b></p>
</div>""" + foot("02 / 06", swipe=True)),
 page(top("Part 1 of 6") + """
<div class='mid'>
  <h2>Bharat's respect for the uniform runs <em>deeper</em> than anyone's.</h2>
  <p class='body'>But it shows up on Republic Day. On Independence Day. On Vijay Diwas.</p>
  <p class='body'><b>And then it goes quiet.</b></p>
</div>""" + foot("03 / 06", swipe=True)),
 page(top("Part 1 of 6") + """
<div class='mid'>
  <h2>A soldier gives his <em>best years</em> to the nation.</h2>
  <p class='body'>The nation's thank-you should last <b>his whole life</b> — not one day a year.</p>
  <div class='rule'></div>
</div>""" + foot("04 / 06", swipe=True)),
 page(top("Part 1 of 6") + """
<div class='mid'>
  <div class='eyebrow'>This is the idea</div>
  <h1>A <em>Culture of Gratitude.</em></h1>
  <p class='body'>Respect that is <b>visible</b> — at every shop, school, hospital and boardroom. Every single day.</p>
  <div class='hi'>वर्दी की शान, हर जगह सम्मान।</div>
</div>""" + foot("05 / 06", swipe=True)),
 CTA_SLIDE("Part 1 of 6", "06 / 06"),
]
for i, h in enumerate(p1, 1): slides[f"p1_world_{i}"] = h

# ---------- Post 2: Founder quote card ----------
slides["p2_founder"] = page(top("From the Founder") + f"""
<div class='mid'>
  <div style='font-family:Playfair Display;font-size:200px;line-height:.6;color:var(--gold);height:90px'>“</div>
  <h2 style='font-size:56px;line-height:1.24;font-weight:600'>I want our children to watch Bharat thank its soldiers <em>at every shop and every counter,</em> every single day.</h2>
  <div style='display:flex;align-items:center;gap:30px;margin-top:56px'>
    <img src='{A}/founder.png' style='width:140px;height:140px;border-radius:50%;object-fit:cover;object-position:50% 18%;border:2px solid var(--gold)'>
    <div><div style='font-family:Playfair Display;font-size:36px;font-weight:700'>Col Arvind Vannur, Veteran</div>
    <div style='font-size:26px;color:var(--muted);margin-top:6px'>Founder, Rakshak ID</div></div>
  </div>
</div>""" + foot("rakshakid.com", "Culture of Gratitude"))

# ---------- Post 3: Air Force Day ----------
slides["p3_airforce"] = page(top("8 October") + """
<div class='mid center'>
  <div class='eyebrow'>Indian Air Force Day</div>
  <div style='font-family:Tiro Devanagari Hindi;font-size:64px;color:var(--gold-hi)'>नभः स्पृशं दीप्तम्</div>
  <div style='font-size:26px;color:#8A8F9C;letter-spacing:.12em;text-transform:uppercase;margin-top:10px'>Touch the sky with glory</div>
  <h2 style='margin-top:60px'>To every air warrior who served Bharat —<br><em>and every family that waited,</em></h2>
  <h1 style='margin-top:40px;font-size:110px'>thank you.</h1>
  <div class='hi' style='margin-top:36px'>हर वायु योद्धा और उनके परिवार को — धन्यवाद।</div>
</div>""" + foot("rakshakid.com", "#AirForceDay"))

# ---------- Post 4: Carousel — THE WHY ----------
p4 = [
 page(top("Part 2 of 6") + """
<div class='mid'>
  <div class='eyebrow'>Part 2 · The Why</div>
  <h1>Why should a soldier's thank-you last <em>only one day?</em></h1>
</div>""" + foot("rakshakid.com", swipe=True)),
 page(top("Part 2 of 6") + """
<div class='mid'>
  <h2>Service is never a <em>solo act.</em></h2>
  <div class='list'><div>A new posting every few years</div><div>Children changing schools again and again</div><div>A spouse holding the home together through every silence</div><div>Parents who sent their son to the border</div></div>
</div>""" + foot("02 / 05", swipe=True)),
 page(top("Part 2 of 6") + """
<div class='mid'>
  <h2>The whole family <em>serves.</em></h2>
  <p class='body'>So the thank-you must reach all of them — the <b>Veteran</b>, the <b>Veer Nari</b>, the <b>Rakshak Nari</b>, the <b>children</b> and the <b>parents.</b></p>
  <div class='hi'>पूरा परिवार देश की सेवा करता है।</div>
</div>""" + foot("03 / 05", swipe=True)),
 page(top("Part 2 of 6") + """
<div class='mid'>
  <h2>And it must last a <em>lifetime.</em></h2>
  <p class='body'>Not a speech on one day. A <b>visible thank-you</b> — every time a Rakshak walks into a shop, a hospital or a school.</p>
  <div class='rule'></div>
</div>""" + foot("04 / 05", swipe=True)),
 CTA_SLIDE("Part 2 of 6", "05 / 05"),
]
for i, h in enumerate(p4, 1): slides[f"p4_why_{i}"] = h

# ---------- Stories 1080x1920 ----------
STORY_X = ".page{padding:140px 90px}"
slides["s1_countdown"] = (page(top("Countdown") + """
<div class='mid center'>
  <div class='big-num'>72</div>
  <h2 style='margin-top:20px'>days to <em>Vijay Diwas.</em></h2>
  <p class='body'>Rakshak ID launches on <b>16 December 2026.</b></p>
  <div class='hi'>विजय दिवस तक 72 दिन</div>
  <div><span class='cta'>Register early · rakshakid.com</span></div>
</div>""" + foot("@rakshakid", "Link in bio"), 1080, 1920, STORY_X))
slides["s2_register"] = (page(top("Register Early") + f"""
<div class='mid center'>
  <img src='{A}/card.png' style='width:440px;border-radius:28px;margin:0 auto 60px;box-shadow:0 30px 90px rgba(232,181,71,.25)'>
  <h2>One app for India's <em>Armed Forces family.</em></h2>
  <p class='body'>Privileges · Brotherhood · Opportunity</p>
  <div class='hi'>सुविधाएँ · बिरादरी · नए अवसर</div>
  <div><span class='cta'>Register · rakshakid.com</span></div>
</div>""" + foot("@rakshakid", "Free to register"), 1080, 1920, STORY_X))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, html in slides.items():
            w, h = (1080, 1920) if name.startswith("s") else (1080, 1350)
            pg = await b.new_page(viewport={"width": w, "height": h})
            f = ROOT / "html" / f"{name}.html"; f.parent.mkdir(exist_ok=True); f.write_text(html)
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f"{name}.png"))
            await pg.close()
        await b.close()
    print(len(slides), "rendered")

asyncio.run(main())
