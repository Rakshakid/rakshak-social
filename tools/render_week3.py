"""Week 3 (19-25 Oct 2026) media for Rakshak ID. Phase 1 close: Culture of Gratitude parts 5 and 6."""
import asyncio, subprocess, wave
import numpy as np
from render_lib import page, top, foot, A, ROOT
from playwright.async_api import async_playwright
import reel_music

OUT = ROOT / "out_w3"; OUT.mkdir(exist_ok=True)
(ROOT / "html").mkdir(exist_ok=True)
S = {}

def cta(tag, n, head, sub, hi):
    return page(top(tag) + f"""
<div class='mid center'>
  <img src='{A}/lion.png' style='width:150px;height:150px;border-radius:34px;border:1px solid rgba(232,181,71,.4);box-shadow:0 0 80px rgba(232,181,71,.3);margin:0 auto 46px'>
  <h2>{head}</h2>
  <div class='hi'>{hi}</div>
  <p class='body' style='margin-top:30px'>{sub}</p>
  <div><span class='cta'>Register · rakshakid.com</span></div>
</div>""" + foot(n, "App launch · Vijay Diwas · 16 Dec"))

def founder_block():
    return f"""<div style='display:flex;align-items:center;gap:30px;margin-top:56px'>
    <img src='{A}/founder.png' style='width:140px;height:140px;border-radius:50%;object-fit:cover;object-position:50% 18%;border:2px solid var(--gold)'>
    <div><div style='font-family:Playfair Display;font-size:36px;font-weight:700'>Col Arvind Vannur, Veteran</div>
    <div style='font-size:26px;color:var(--muted);margin-top:6px'>Founder, Rakshak ID</div></div></div>"""

# ---------- P1 Mon: Culture of Gratitude 5/6 The Change ----------
T = "Part 5 of 6"
p1 = [
 page(top(T) + """<div class='mid'><div class='eyebrow'>Part 5 · The Change</div>
  <h1>Our children are <em>watching.</em></h1>
  <p class='body'>Gen Z and Gen Alpha are learning what Bharat values from <b>how it treats its soldiers.</b></p></div>""" + foot("rakshakid.com", swipe=True)),
 page(top(T) + """<div class='mid'><h2>A whole generation has grown up <em>after Kargil.</em></h2>
  <p class='body'>They never saw the coffins come home. They know the uniform from films and parades.</p>
  <p class='body'><b>The cost of freedom is invisible to them.</b></p></div>""" + foot("02 / 06", swipe=True)),
 page(top(T) + """<div class='mid'><h2>Children don't learn gratitude <em>from speeches.</em></h2>
  <div class='list'><div>They learn it at the shop counter</div><div>In the hospital queue</div><div>At the school gate</div><div>From what their parents do</div></div></div>""" + foot("03 / 06", swipe=True)),
 page(top(T) + """<div class='mid'><h2>Picture a child watching a shopkeeper <em>stand up and thank</em> a veteran.</h2>
  <p class='body'>That one moment teaches more than any textbook.</p>
  <div class='rule'></div></div>""" + foot("04 / 06", swipe=True)),
 page(top(T) + """<div class='mid'><div class='eyebrow'>The change we want</div>
  <h1>Let them inherit a nation <em>that remembers.</em></h1>
  <div class='hi'>आने वाली पीढ़ी को ऐसा भारत दें जो याद रखता है।</div></div>""" + foot("05 / 06", swipe=True)),
 cta(T, "06 / 06", "Teach gratitude.<br><em>Start at home.</em>", "Register early. Early members get <b>extra privileges</b> at launch.", "आप भारत के लिए खड़े रहे। अब भारत आपके साथ खड़ा है।"),
]
for i, h in enumerate(p1, 1): S[f"p1_change_{i}"] = h

# ---------- P2 Tue: Founder quote card, Rakshak Nari ----------
S["p2_samman"] = page(top("From the Founder") + f"""
<div class='mid'>
  <div style='font-family:Playfair Display;font-size:200px;line-height:.6;color:var(--gold);height:90px'>“</div>
  <h2 style='font-size:58px;line-height:1.24;font-weight:600'>Why must we wait until she becomes a Veer Nari <em>to give her samman?</em></h2>
  <div class='hi' style='font-size:36px'>वीर नारी बनने का इंतज़ार क्यों? सम्मान आज क्यों नहीं?</div>
  {founder_block()}
</div>""" + foot("rakshakid.com", "Rakshak Nari"))

# ---------- P3 Thu: Agniveer ----------
T = "Agniveer"
p3 = [
 page(top(T) + """<div class='mid'><div class='eyebrow'>For every Agniveer</div>
  <h1>He wore the uniform.<br><em>That is enough.</em></h1></div>""" + foot("rakshakid.com", swipe=True)),
 page(top(T) + """<div class='mid'><h2>Same oath. Same uniform. <em>Same tricolour.</em></h2>
  <p class='body'>An Agniveer stood where every soldier stands, and served Bharat with the same pride.</p></div>""" + foot("02 / 05", swipe=True)),
 page(top(T) + """<div class='mid'><h2>The first years after service are <em>the hardest.</em></h2>
  <div class='list'><div>A new job to find</div><div>Skills to turn into a career</div><div>Maybe a new city</div><div>A family looking to him</div></div></div>""" + foot("03 / 05", swipe=True)),
 page(top(T) + """<div class='mid'><div class='eyebrow'>Our rule</div>
  <h1><em>Never leave a man behind.</em></h1>
  <p class='body'>In Rakshak ID, an Agniveer gets <b>the same privileges as any veteran</b>, because he wore the uniform. His posts reach thousands of verified Rakshaks.</p></div>""" + foot("04 / 05", swipe=True)),
 cta(T, "05 / 05", "Agniveers and their families:<br><em>you belong here.</em>", "Register early. Early members get <b>extra privileges</b> at launch.", "वर्दी पहनी है, तो आप रक्षक हैं।"),
]
for i, h in enumerate(p3, 1): S[f"p3_agniveer_{i}"] = h

# ---------- Founder video: script card (board preview only, not posted) ----------
S["v1_script"] = page(top("Founder video · Fri") + """<div class='mid'><div class='eyebrow'>Script for you to film · 55 s</div>
 <h1>Divided, we lose. <em>United, we get opportunities.</em></h1>
 <p class='body'>Story 4 from your Story Bank. Speak to camera, phone held upright. Full script and filming brief on the board.</p></div>""" + foot("Col Arvind Vannur, Veteran", "Send the raw video in Claude"))

# ---------- LinkedIn cards ----------
S["li1_thankyou"] = page(top("From the Founder") + """<div class='mid'><div class='eyebrow'>A lesson from abroad</div>
 <h1>The thank-you <em>that costs nothing.</em></h1><p class='body'>What business leaders can do to build a <b>Culture of Gratitude</b> in India.</p></div>""" + foot("Col Arvind Vannur, Veteran", "rakshakid.com"))
S["li2_dependent"] = page(top("From the Founder") + """<div class='mid'><div class='eyebrow'>To India's bankers</div>
 <h1>Every form calls her <em>“dependent”.</em></h1><p class='body'>Why the Rakshak Nari deserves her own identity, and fair credit in her own name.</p></div>""" + foot("Col Arvind Vannur, Veteran", "rakshakid.com"))

# ---------- Reel scenes ----------
RX = ".page{padding:150px 90px} .foot{justify-content:center}"
F = "<div class='foot'><span>rakshakid.com · @rakshakid</span></div>"
def endcard(line):
    return top("") + f"""<div class='mid center'>
   <img src='{A}/lion.png' style='width:200px;height:200px;border-radius:44px;border:1px solid rgba(232,181,71,.4);box-shadow:0 0 110px rgba(232,181,71,.35);margin:0 auto 60px'>
   <h2 style='font-size:80px'>{line}</h2>
   <p class='body' style='font-size:42px'>Early members get <b>extra privileges</b> at launch.</p>
   <div><span class='cta' style='font-size:44px;padding:32px 64px'>rakshakid.com</span></div>
   <div class='eyebrow' style='margin-top:70px;margin-bottom:0'>Launching · Vijay Diwas · 16 December</div></div>""" + F
REELS = {
 "r1_safe": [
  top("") + """<div class='mid center'><h1 style='font-size:120px'>Is Rakshak ID <em>safe?</em></h1><div class='hi' style='font-size:52px;margin-top:50px'>क्या रक्षक ID सुरक्षित है?</div></div>""" + F,
  top("") + """<div class='mid center'><h1 style='font-size:110px'>Free to <em>register.</em></h1><p class='body' style='font-size:44px'>No fee to join the parivar.</p><div class='hi' style='font-size:50px;margin-top:40px'>रजिस्ट्रेशन मुफ़्त है।</div></div>""" + F,
  top("") + """<div class='mid center'><h1 style='font-size:104px'>Verified<br><em>in the app.</em></h1><p class='body' style='font-size:44px'>Your documents are <b>deleted within 72 hours.</b></p><div class='hi' style='font-size:50px;margin-top:40px'>दस्तावेज़ 72 घंटे में डिलीट।</div></div>""" + F,
  top("") + """<div class='mid center'><h1 style='font-size:104px'>Your data is <em>never sold.</em></h1><p class='body' style='font-size:38px'>A private initiative. Not affiliated with the Ministry of Defence.</p><div class='hi' style='font-size:50px;margin-top:40px'>आपका डेटा कभी बेचा नहीं जाता।</div></div>""" + F,
  endcard("Register early."),
 ],
 "r2_goal": [
  top("") + """<div class='mid center'><h1 style='font-size:112px'>A soldier must never <em>fade away.</em></h1><div class='hi' style='font-size:52px;margin-top:50px'>सैनिक को कभी भुलाया न जाए।</div></div>""" + F,
  top("") + """<div class='mid center'><h1 style='font-size:110px;line-height:1.25'>In service,<br>he <em>earned</em> respect.</h1></div>""" + F,
  top("") + """<div class='mid center'><h1 style='font-size:110px;line-height:1.25'>For life,<br>he should <em>command</em> it.</h1></div>""" + F,
  top("") + """<div class='mid center'><h1 style='font-size:104px'>Not a memory.<br><em>A role model.</em></h1><p class='body' style='font-size:42px'>For every child who is watching.</p><div class='hi' style='font-size:52px;margin-top:40px'>यादों में नहीं, आदर्श बनकर।</div></div>""" + F,
  endcard("Culture of Gratitude."),
 ],
}

async def shots():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        items = list(S.items())
        for r, scenes in REELS.items():
            items += [(f"{r}_s{i}", page(s, 1080, 1920, RX)) for i, s in enumerate(scenes)]
        for name, html in items:
            tall = name.startswith("r")
            w, h = (1080, 1920) if tall else (1080, 1350)
            pg = await b.new_page(viewport={"width": w, "height": h})
            f = ROOT / "html" / f"w3_{name}.html"; f.write_text(html)
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f"{name}.png")); await pg.close()
        await b.close()

def make_reel(r, n):
    """Crossfaded scenes with slow zoom; music = arpeggio track the founder chose on 10 Oct."""
    D, Tr = 3.4, 0.6; total = n * D - (n - 1) * Tr
    inp = []
    for i in range(n): inp += ["-loop", "1", "-t", str(D), "-i", str(OUT / f"{r}_s{i}.png")]
    fl = [f"[{i}:v]scale=1188:2112,zoompan=z='min(1+0.0009*on,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(D*30)}:s=1080x1920:fps=30,format=yuv420p,setsar=1[v{i}]" for i in range(n)]
    prev = "v0"
    for i in range(1, n):
        fl.append(f"[{prev}][v{i}]xfade=transition=fade:duration={Tr}:offset={i*(D-Tr):.2f}[x{i}]"); prev = f"x{i}"
    fl.append(f"[{prev}]fade=t=in:st=0:d=0.5,fade=t=out:st={total-0.6:.2f}:d=0.6[vout]")
    wav = OUT / f"{r}_music.wav"; a = reel_music.make(total)
    with wave.open(str(wav), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(reel_music.SR); w.writeframes(np.repeat(a[:, None], 2, axis=1).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-i", str(wav), "-filter_complex", ";".join(fl),
        "-map", "[vout]", "-map", f"{n}:a", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-t", f"{total:.2f}", str(OUT / f"{r}.mp4")], check=True)
    wav.unlink()

if __name__ == "__main__":
    asyncio.run(shots())
    for r, sc in REELS.items(): make_reel(r, len(sc))
    print("done", len(S), "images,", len(REELS), "reels")
