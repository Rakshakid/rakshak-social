"""Animated-text Reel/Short: 5 scenes -> crossfaded 1080x1920 MP4 with ambient pad."""
import asyncio, subprocess, sys
sys.path.insert(0, ".")
from render_week1 import page, top, A, ROOT
from playwright.async_api import async_playwright

X = ".page{padding:150px 90px} .foot{justify-content:center}"
F = "<div class='foot'><span>rakshakid.com · @rakshakid</span></div>"
scenes = [
 top("") + """<div class='mid center'><h1 style='font-size:110px'>You stood<br>for <em>Bharat.</em></h1>
   <div class='hi' style='font-size:52px;margin-top:50px'>आप भारत के लिए खड़े रहे।</div></div>""" + F,
 top("") + """<div class='mid center'><h1 style='font-size:110px'>Now Bharat<br><em>stands with you.</em></h1>
   <div class='hi' style='font-size:52px;margin-top:50px'>अब भारत आपके साथ खड़ा है।</div></div>""" + F,
 top("") + f"""<div class='mid center'><img src='{A}/card.png' style='width:420px;border-radius:26px;margin:0 auto 70px;box-shadow:0 30px 90px rgba(232,181,71,.3)'>
   <h2 style='font-size:76px'>One app for India's<br><em>Armed Forces family.</em></h2></div>""" + F,
 top("") + """<div class='mid center'>
   <h1 style='font-size:104px;line-height:1.3'>Privileges.<br><em>Brotherhood.</em><br>Opportunity.</h1>
   <div class='hi' style='font-size:50px;margin-top:50px'>सुविधाएँ · बिरादरी · नए अवसर</div></div>""" + F,
 top("") + f"""<div class='mid center'>
   <img src='{A}/lion.png' style='width:200px;height:200px;border-radius:44px;border:1px solid rgba(232,181,71,.4);box-shadow:0 0 110px rgba(232,181,71,.35);margin:0 auto 60px'>
   <h2 style='font-size:80px'>Register early.</h2>
   <p class='body' style='font-size:42px'>Early members get <b>extra privileges</b> at launch.</p>
   <div><span class='cta' style='font-size:44px;padding:32px 64px'>rakshakid.com</span></div>
   <div class='eyebrow' style='margin-top:70px;margin-bottom:0'>Launching · Vijay Diwas · 16 December</div></div>""" + F,
]

async def shots():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for i, s in enumerate(scenes):
            pg = await b.new_page(viewport={"width": 1080, "height": 1920})
            f = ROOT / "html" / f"reel_{i}.html"; f.write_text(page(s, 1080, 1920, X))
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(ROOT / "out" / f"reel_{i}.png")); await pg.close()
        await b.close()
asyncio.run(shots())

D, T = 3.4, 0.6  # scene length, crossfade
n = len(scenes); total = n * D - (n - 1) * T
inp = [];
for i in range(n): inp += ["-loop", "1", "-t", str(D), "-i", f"out/reel_{i}.png"]
# gentle slow zoom per scene, then chain crossfades
fl = []
for i in range(n):
    fl.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(1+0.0009*on,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(D*30)}:s=1080x1920:fps=30,format=yuv420p,setsar=1[v{i}]")
prev = "v0"
for i in range(1, n):
    off = i * (D - T)
    fl.append(f"[{prev}][v{i}]xfade=transition=fade:duration={T}:offset={off:.2f}[x{i}]"); prev = f"x{i}"
fl.append(f"[{prev}]fade=t=in:st=0:d=0.5,fade=t=out:st={total-0.6:.2f}:d=0.6[vout]")
# ambient pad: soft D-major-ish chord with tremolo, faded
audio = (f"aevalsrc='0.10*sin(2*PI*146.83*t)+0.07*sin(2*PI*220*t)+0.06*sin(2*PI*293.66*t)+0.04*sin(2*PI*369.99*t)"
         f"*(0.6+0.4*sin(2*PI*0.25*t))':s=44100:d={total:.2f},lowpass=f=1800,afade=t=in:d=1.5,afade=t=out:st={total-2:.2f}:d=2[aout]")
fl.append(audio)
cmd = ["ffmpeg", "-y", "-loglevel", "error", *inp, "-filter_complex", ";".join(fl), "-map", "[vout]", "-map", "[aout]",
       "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "128k",
       "-movflags", "+faststart", "-t", f"{total:.2f}", "out/reel_you_stood_for_bharat.mp4"]
subprocess.run(cmd, check=True)
print("video", round(total, 1), "s")
