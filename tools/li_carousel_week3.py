"""LinkedIn w3-l1 as a 4-slide document carousel (1080x1350)."""
import asyncio, pathlib
from playwright.async_api import async_playwright
from render_lib import page, top, foot

OUT = pathlib.Path(__file__).parent / "out"; OUT.mkdir(exist_ok=True)
F = lambda n: foot("Col Arvind Vannur, Veteran", f"{n} / 4")

slides = {
"li1_c1": page(top("From the founder") + """
<div class='mid'>
  <div class='eyebrow'>A lesson from abroad</div>
  <h1>The thank-you <em>that costs nothing.</em></h1>
  <p class='body'>What business leaders can do to build a <b>Culture of Gratitude</b> in India.</p>
</div>""" + foot("Col Arvind Vannur, Veteran", "Swipe →")),
"li1_c2": page(top("1 · Four words") + """
<div class='mid'>
  <div class='eyebrow'>What my friends saw in the US</div>
  <h1><em>“Thank you for your service.”</em></h1>
  <p class='body'>At a coffee shop, an airport counter, a hardware store. The discount was small. <b>That was never the point.</b></p>
  <p class='body'>The point was being honoured by a stranger, in the middle of an ordinary day.</p>
</div>""" + F(2)),
"li1_c3": page(top("2 · The silence") + """
<div class='mid'>
  <div class='eyebrow'>In India</div>
  <h2>Our respect for the uniform runs deep. But it shows up <em>a few days a year.</em></h2>
  <div class='list'><div>Republic Day</div><div>Independence Day</div><div>Vijay Diwas</div></div>
  <p class='body'>Then it goes quiet. A generation has grown up after Kargil. <b>Children learn values from what they watch adults do.</b></p>
</div>""" + F(3)),
"li1_c4": page(top("3 · Your role") + """
<div class='mid'>
  <div class='eyebrow'>For business leaders</div>
  <h2>Small acts. Together, a <em>Culture of Gratitude.</em></h2>
  <div class='list'><div>A bank that recognises service at its counter</div><div>A retailer whose staff know how to say thank you</div><div>A hospital desk that makes room for a Veer Nari</div></div>
  <p class='body'>Rakshak ID gives organisations a <b>verified</b> way to do this, for 2.5 crore who served and their families. Launch: Vijay Diwas, 16 December.</p>
  <div><span class='cta' style='font-size:30px;padding:22px 44px'>partners@rakshakid.com</span></div>
</div>""" + F(4)),
}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for k, html in slides.items():
            f = OUT / f"{k}.html"; f.write_text(html)
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(OUT / f"{k}.png"))
        await b.close()
asyncio.run(main())
