"""Build W7 reels: overlays (Playwright) + ffmpeg compose. Usage: python3 build.py w7-r1 [w7-r2 ...]"""
import asyncio, json, sys, subprocess, base64, pathlib, html as H
from playwright.async_api import async_playwright

W = pathlib.Path(__file__).parent
IMG = W / "img"; CLIP = W / "clips"; MUS = W / "music"; OUT = W / "out"; OUT.mkdir(exist_ok=True)
LION = "data:image/png;base64," + base64.b64encode(pathlib.Path("/home/claude/rakshak-social/tools/assets/lion.png").read_bytes()).decode()
SPEC = json.load(open(W / "spec.json"))
XF = 0.45  # crossfade

CSS = """*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;background:transparent;overflow:hidden;font-family:'DM Sans',sans-serif;color:#F6F1E7}
.top{position:absolute;inset:0 0 auto 0;height:520px;background:linear-gradient(180deg,rgba(7,9,13,.62),rgba(7,9,13,0))}
.logo{position:absolute;left:56px;top:96px;display:flex;align-items:center;gap:22px}
.logo img{width:112px;height:112px;border-radius:24px;border:1px solid rgba(232,181,71,.45);box-shadow:0 0 36px rgba(232,181,71,.25)}
.logo b{font-family:'Playfair Display',serif;font-weight:700;font-size:44px;letter-spacing:.08em;color:#F6DFA6;text-shadow:0 2px 12px rgba(0,0,0,.6)}
.ai{position:absolute;right:56px;top:120px;font-family:'DM Mono',monospace;font-size:21px;letter-spacing:.06em;color:#F6F1E7;opacity:.85;text-shadow:0 1px 8px rgba(0,0,0,.8)}
.gift{position:absolute;left:56px;top:236px;display:inline-flex;align-items:center;gap:12px;background:linear-gradient(135deg,#F6DFA6,#E8B547);color:#07090D;border-radius:999px;padding:12px 26px;font-size:26px;font-weight:700;box-shadow:0 4px 18px rgba(0,0,0,.35)}
.gift span{font-weight:500}
.ann{position:absolute;left:56px;top:316px;background:rgba(7,9,13,.62);padding:10px 18px;border-radius:8px;font-family:'DM Mono',monospace;font-size:23px;letter-spacing:.12em;text-transform:uppercase;color:#F6F1E7}
.card{position:absolute;left:56px;right:56px;bottom:400px;background:rgba(14,17,24,.80);border-left:6px solid #E8B547;border-radius:22px;padding:38px 44px 36px;backdrop-filter:blur(6px)}
h1{font-family:'Playfair Display',serif;font-weight:700;font-size:var(--hs);line-height:1.12;color:#F6F1E7}
.sub{font-size:34px;line-height:1.35;color:#F6DFA6;margin-top:16px;font-weight:500}
.hi{font-family:'Tiro Devanagari Hindi',serif;font-size:31px;line-height:1.5;color:#E6E3DC;margin-top:16px}
"""

def scene_html(seg, s):
    n = len(s["head"]); hs = 66 if n < 34 else 58 if n < 52 else 52
    sub = f"<div class='sub'>{H.escape(s['sub'])}</div>" if s.get("sub") else ""
    hi = f"<div class='hi'>{H.escape(s['hi'])}</div>" if s.get("hi") else ""
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body style='--hs:{hs}px'>
<div class='top'></div><div class='logo'><img src='{LION}'><b>RAKSHAK ID</b></div>
<div class='ai'>AI-generated visuals</div>
<div class='gift'>🎁 {H.escape(seg)}: first 500 get exclusive brand vouchers <span>· Details at the end</span></div>
<div class='ann'>{H.escape(s['ann'])}</div>
<div class='card'><h1>{H.escape(s['head'])}</h1>{sub}{hi}</div></body></html>"""

def end_html(spec):
    seg, seg_hi, e = spec["seg"], spec["seg_hi"], spec.get("end", {})
    lseg = seg if seg[0].isupper() and seg not in ("Fauji brats",) else seg
    pre = f"<div class='pre'>{H.escape(e['pre'])}</div><div class='prehi'>{H.escape(e['pre_hi'])}</div>" if e.get("pre") else ""
    low = seg.lower() if seg in ("Veterans", "Agniveers", "Fauji brats") else seg
    return f"""<!doctype html><html><head><meta charset='utf-8'><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;background:radial-gradient(ellipse at 50% 30%,#1a1408 0%,#07090D 60%);font-family:'DM Sans',sans-serif;color:#F6F1E7;text-align:center}}
.wrap{{position:absolute;left:80px;right:80px;top:230px}}
img{{width:200px;height:200px;border-radius:40px;border:2px solid rgba(232,181,71,.5);box-shadow:0 0 70px rgba(232,181,71,.35)}}
.brand{{font-family:'Playfair Display',serif;font-weight:700;font-size:54px;letter-spacing:.1em;color:#F6DFA6;margin-top:26px}}
.pre{{font-family:'Playfair Display',serif;font-style:italic;font-size:44px;line-height:1.25;color:#F6F1E7;margin-top:44px}}
.prehi{{font-family:'Tiro Devanagari Hindi',serif;font-size:32px;color:#E6E3DC;margin-top:10px}}
h1{{font-family:'Playfair Display',serif;font-weight:700;font-size:70px;line-height:1.1;margin-top:50px}}
h1 em{{color:#E8B547;font-style:normal}}
.offer{{font-size:38px;line-height:1.4;margin-top:28px;color:#F6F1E7}}
.offer b{{color:#F6DFA6}}
.hi{{font-family:'Tiro Devanagari Hindi',serif;font-size:33px;line-height:1.5;color:#E6E3DC;margin-top:22px}}
.cta{{display:inline-block;margin-top:44px;padding:26px 46px;border-radius:999px;background:linear-gradient(135deg,#F6DFA6,#E8B547);color:#07090D;font-weight:700;font-size:44px}}
.bio{{font-family:'DM Mono',monospace;font-size:26px;letter-spacing:.12em;color:#AEB3BE;margin-top:20px;text-transform:uppercase}}
.fine{{position:absolute;left:0;right:0;bottom:420px;font-size:22px;color:#7D8391}}
</style></head><body><div class='wrap'><img src='{LION}'><div class='brand'>RAKSHAK ID</div>{pre}
<h1><em>{H.escape(seg)}</em>, this one's yours.</h1>
<div class='offer'>The first 500 {H.escape(low)} to register get <b>exclusive brand vouchers</b>, curated for {H.escape(low)}.</div>
<div class='hi'>पहले 500 {H.escape(seg_hi)} को मिलेंगे ख़ास ब्रांड वाउचर।</div>
<div class='cta'>Register early · rakshakid.com</div><div class='bio'>Link in bio</div></div>
<div class='fine'>Not affiliated with the Ministry of Defence · AI-generated visuals</div></body></html>"""

async def render(rid):
    spec = SPEC[rid]; d = OUT / rid; d.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for i, s in enumerate(spec["scenes"]):
            await pg.set_content(scene_html(spec["seg"], s)); await pg.wait_for_timeout(400)
            await pg.screenshot(path=str(d / f"ov{i}.png"), omit_background=True)
        await pg.set_content(end_html(spec)); await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(d / "end.png"))
        await b.close()

def sh(c): subprocess.run(c, shell=True, check=True)

def compose(rid):
    spec = SPEC[rid]; d = OUT / rid
    grade = {"cold": ",eq=saturation=0.9:contrast=1.04", "film": ",eq=contrast=1.03"}.get(spec.get("grade"), "")
    segs = []
    for i, s in enumerate(spec["scenes"]):
        dur = s["dur"]; src = s["src"]; seg = d / f"s{i}.mp4"
        if src.endswith(".mp4"):
            # stretch the 4 s clip gently to fill, max 1.2x slow
            f = min(dur / 4.0, 1.2)
            base = (f"[0:v]setpts={f:.3f}*PTS,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,"
                    f"tpad=stop_mode=clone:stop_duration=2{grade}[bg]")
            inp = f"-i {CLIP/src}"
        else:
            fr = int(dur * 30)
            base = (f"[0:v]scale=2160:3870,crop=2160:3840,zoompan=z='1+0.07*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30{grade}[bg]")
            inp = f"-loop 1 -i {IMG/src}"
        sh(f"ffmpeg -loglevel error -y {inp} -loop 1 -i {d}/ov{i}.png -filter_complex "
           f"\"{base};[1:v]format=rgba{'' if i==0 else ',fade=in:st=0.25:d=0.45:alpha=1'}[ov];[bg][ov]overlay=0:0,format=yuv420p[v]\" "
           f"-map [v] -t {dur} -r 30 -c:v libx264 -crf 18 -preset medium {seg}")
        segs.append((seg, dur))
    end = d / "send.mp4"; ed = 5.0
    sh(f"ffmpeg -loglevel error -y -loop 1 -i {d}/end.png -filter_complex \"[0:v]scale=1080:1920,zoompan=z='1+0.03*on/150':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1080x1920:fps=30,format=yuv420p[v]\" -map [v] -t {ed} -r 30 -c:v libx264 -crf 18 {end}")
    segs.append((end, ed))
    # xfade chain
    ins = " ".join(f"-i {p}" for p, _ in segs); fc = []; off = 0; prev = "[0:v]"
    for k in range(1, len(segs)):
        off += segs[k - 1][1] - XF
        lab = f"[x{k}]"; fc.append(f"{prev}[{k}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}{lab}"); prev = lab
    total = sum(x for _, x in segs) - XF * (len(segs) - 1)
    sh(f"ffmpeg -loglevel error -y {ins} -filter_complex \"{';'.join(fc)}\" -map {prev} -c:v libx264 -crf 19 -preset medium {d}/silent.mp4")
    sh(f"ffmpeg -loglevel error -y -i {d}/silent.mp4 -i {MUS/spec['music']} -filter_complex \"[1:a]atrim=0:{total:.2f},afade=t=in:d=0.05,afade=t=out:st={total-1.6:.2f}:d=1.6,loudnorm=I=-14:TP=-1.5[a]\" "
       f"-map 0:v -map [a] -c:v copy -c:a aac -b:a 192k -movflags +faststart -shortest {OUT}/{rid}.mp4")
    sh(f"ffmpeg -loglevel error -y -ss 2.2 -i {OUT}/{rid}.mp4 -frames:v 1 -q:v 3 {OUT}/{rid}_s0.jpg")
    print(rid, f"{total:.1f}s")

if __name__ == "__main__":
    for rid in [a for a in sys.argv[1:] if not a.startswith("--")]:
        asyncio.run(render(rid))
        if "--ov" not in sys.argv: compose(rid)
