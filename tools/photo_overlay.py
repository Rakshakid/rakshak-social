"""Photo story-carousel slides and stories with Rakshak overlays.
Usage: python3 overlay.py <spec.json>
spec: {"items":[{"kind":"slide"|"story", "bg":path, "out":stem, "focus":[fx,fy] (0-1 crop centre),
        "tag":..., "n":"1/4", "head":..., "hi":..., "body":..., "cta":..., "swipe":bool,
        "states":[{"head","hi","cta"}...] (story only)}]}
Writes <out>.png (slide still) or <out>_bg.png + <out>_s<i>.png overlay layers (story)."""
import asyncio, json, sys, pathlib, base64
from PIL import Image
from playwright.async_api import async_playwright

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
LION = "data:image/png;base64," + base64.b64encode((HERE / "assets/lion.png").read_bytes()).decode()

CSS = """*{margin:0;padding:0;box-sizing:border-box}
html,body{width:__W__px;height:__H__px;background:transparent;overflow:hidden;font-family:'DM Sans',sans-serif;color:#F6F1E7}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,9,13,.55) 0%,rgba(7,9,13,0) 16%,rgba(7,9,13,0) 46%,rgba(7,9,13,.82) 70%,rgba(7,9,13,.96) 100%)}
.logo{position:absolute;left:52px;top:__LT__px;display:flex;align-items:center;gap:22px}
.logo img{width:112px;height:112px;border-radius:24px;border:1px solid rgba(232,181,71,.35);box-shadow:0 0 40px rgba(232,181,71,.25)}
.logo span{background:rgba(7,9,13,.62);padding:10px 16px;border-radius:10px;font-family:'DM Mono',monospace;font-size:22px;font-weight:500;letter-spacing:.16em;color:#E8B547;text-transform:uppercase}
.logo b{font-family:'DM Sans';font-weight:700;font-size:38px;letter-spacing:.01em;color:#F6F1E7}
.n{position:absolute;right:56px;top:__NT__px;background:rgba(7,9,13,.55);padding:8px 14px;border-radius:10px;font-family:'DM Mono',monospace;font-size:22px;letter-spacing:.12em;color:#F6F1E7;opacity:.8}
.txt{position:absolute;left:62px;right:62px;bottom:__BOT__px}
.rule{width:76px;height:4px;background:#E8B547;margin-bottom:34px}
h1{font-family:'Playfair Display',serif;font-weight:700;font-size:__HS__px;line-height:1.12;text-shadow:0 2px 18px rgba(0,0,0,.5)}
.hi{font-family:'Tiro Devanagari Hindi',serif;font-size:__HIS__px;line-height:1.45;color:#F6DFA6;margin-top:18px}
.body{font-size:30px;line-height:1.45;color:#E6E3DC;margin-top:30px}
.cta{display:inline-block;margin-top:36px;padding:20px 30px;border-radius:12px;background:#F6A623;background:linear-gradient(135deg,#F6C04A,#F09A1A);color:#07090D;font-weight:700;font-size:33px}
.cta small{font-size:22px;font-weight:600;margin-left:8px}
.swipe{position:absolute;right:62px;bottom:52px;font-size:26px;font-weight:600;color:#F6F1E7}
"""

def html(w, h, inner, story):
    css = (CSS.replace("__W__", str(w)).replace("__H__", str(h))
           .replace("__LT__", "150" if story else "44").replace("__NT__", "84" if story else "80")
           .replace("__BOT__", "300" if story else "120").replace("__HS__", "70" if story else "62")
           .replace("__HIS__", "40" if story else "34"))
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{inner}</body></html>"

def textblock(s, story):
    t = "<div class='txt'><div class='rule'></div>"
    t += f"<h1>{s['head']}</h1>"
    if s.get("hi"): t += f"<div class='hi'>{s['hi']}</div>"
    if s.get("body"): t += f"<div class='body'>{s['body']}</div>"
    if s.get("cta"): t += f"<div><span class='cta'>{s['cta']}</span></div>"
    return t + "</div>"

def crop(src, w, h, focus, dst, zoom=1.0):
    im = Image.open(src).convert("RGB")
    W, H = im.size; r = w / h
    cw, ch = (W, W / r) if W / H < r else (H * r, H)
    cw, ch = cw / zoom, ch / zoom
    fx, fy = focus
    x = min(max(fx * W - cw / 2, 0), W - cw); y = min(max(fy * H - ch / 2, 0), H - ch)
    im.crop((int(x), int(y), int(x + cw), int(y + ch))).resize((w, h), Image.LANCZOS).save(dst)

async def main(spec):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for it in spec["items"]:
            story = it["kind"] == "story"
            w, h = (1080, 1920) if story else (1080, 1350)
            pg = await b.new_page(viewport={"width": w, "height": h})
            bg = OUT / f"{it['out']}_bg.png"
            crop(it["bg"], w, h, it.get("focus", [.5, .5]), bg, it.get("zoom", 1.0))
            async def shot(inner, path):
                f = OUT / "tmp.html"; f.write_text(html(w, h, inner, story))
                await pg.goto(f.as_uri()); await pg.wait_for_timeout(400)
                await pg.screenshot(path=str(path), omit_background=True)
            if story:
                await shot(f"<div class='shade'></div><div class='logo'><img src='{LION}'><b>Rakshak ID</b></div>", OUT / f"{it['out']}_base.png")
                for i, s in enumerate(it["states"]):
                    await shot(textblock(s, True), OUT / f"{it['out']}_s{i}.png")
            else:
                inner = "<div class='shade'></div>"
                inner += f"<div class='logo'><img src='{LION}'>" + (f"<span>{it['tag']}</span>" if it.get('tag') else '') + "</div>"
                inner += f"<div class='n'>{it['n']}</div>" + textblock(it, False)
                if it.get("swipe"): inner += "<div class='swipe'>Swipe →</div>"
                ov = OUT / f"{it['out']}_ov.png"; await shot(inner, ov)
                base = Image.open(bg).convert("RGBA"); base.alpha_composite(Image.open(ov).convert("RGBA"))
                base.convert("RGB").save(OUT / f"{it['out']}.jpg", quality=93)
            await pg.close()
        await b.close()

asyncio.run(main(json.loads(pathlib.Path(sys.argv[1]).read_text())))
