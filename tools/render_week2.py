"""Week 2 (12-18 Oct 2026) media for Rakshak ID."""
import asyncio, subprocess, pathlib
from render_lib import page, top, foot, A, ROOT
from playwright.async_api import async_playwright

OUT = ROOT / "out_w2"; OUT.mkdir(exist_ok=True)
STORY_X = ".page{padding:140px 90px}"
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

# ---------- P1 Mon: Culture of Gratitude 3/6 The How ----------
T = "Part 3 of 6"
p1 = [
 page(top(T) + """<div class='mid'><div class='eyebrow'>Part 3 · The How</div>
  <h1>Respect that stays silent <em>changes nothing.</em></h1>
  <p class='body'>Everyone respects the uniform. Very few ever get a chance to show it.</p></div>""" + foot("rakshakid.com", swipe=True)),
 page(top(T) + """<div class='mid'><h2>Gratitude needs a <em>way to show up.</em></h2>
  <div class='list'><div>A shopkeeper who knows you served</div><div>A bank that values your service, not just a score</div><div>A school desk that welcomes a fauji parivar</div><div>A stranger who says thank you</div></div></div>""" + foot("02 / 05", swipe=True)),
 page(top(T) + """<div class='mid'><h2>Not <em>another card.</em></h2>
  <p class='body'>You already carry ECHS, CSD and veteran cards. Rakshak ID is not one more card for the wallet.</p>
  <p class='body'>It is the fauji parivar, <b>2.5 crore strong</b>, made visible, so that brands, banks and institutions can finally honour it.</p></div>""" + foot("03 / 05", swipe=True)),
 page(top(T) + """<div class='mid'><h2>Silent respect. <em>Visible action.</em></h2>
  <div class='list'><div>A thank-you at the counter</div><div>A fair rate when you need a loan</div><div>A door opened for your child</div></div>
  <p class='body'>This is what we are building towards.</p></div>""" + foot("04 / 05", swipe=True)),
 cta(T, "05 / 05", "You stood for Bharat.<br><em>Now Bharat stands with you.</em>", "Register early. Early members get <b>extra privileges</b> at launch.", "आप भारत के लिए खड़े रहे। अब भारत आपके साथ खड़ा है।"),
]
for i, h in enumerate(p1, 1): S[f"p1_how_{i}"] = h

# ---------- P3 Wed: Beyond discounts ----------
T = "Beyond discounts"
p3 = [
 page(top(T) + """<div class='mid'><h1>A discount on coffee is nice.</h1>
  <h2 style='margin-top:30px'><em>It is not what keeps a fauji family awake at night.</em></h2></div>""" + foot("rakshakid.com", swipe=True)),
 page(top(T) + """<div class='mid'><h2>What really weighs on a <em>fauji home:</em></h2>
  <div class='list'><div>A child's higher education</div><div>A son's or daughter's wedding</div><div>Medical bills ECHS does not cover</div><div>Building the house after retirement</div><div>A fair loan, without a wall of paperwork</div></div></div>""" + foot("02 / 06", swipe=True)),
 page(top(T) + """<div class='mid'><h2>These are the <em>big moments.</em></h2>
  <p class='body'>Government provides pension, ECHS and CSD. For the big moments beyond that, every family is on its own.</p>
  <div class='rule'></div></div>""" + foot("03 / 06", swipe=True)),
 page(top(T) + """<div class='mid'><h2>What Rakshak ID is <em>working on:</em></h2>
  <div class='list'><div>Education loans and fee support</div><div>Wedding needs at fair prices</div><div>Medical support beyond ECHS</div><div>Home-building materials at community rates</div><div>Financial products made for fauji families</div></div>
  <p class='body' style='font-size:28px'>We are in talks with banks and partners. Nothing is promised until it is signed, and we will tell you when it is.</p></div>""" + foot("04 / 06", swipe=True)),
 page(top(T) + """<div class='mid'><h2>The bigger the parivar, <em>the stronger the bargain.</em></h2>
  <p class='body'>One fauji family is a customer. <b>2.5 crore families together</b> are a voice no bank or brand can ignore.</p>
  <div class='hi'>जितना बड़ा परिवार, उतनी मज़बूत आवाज़।</div></div>""" + foot("05 / 06", swipe=True)),
 page(top(T) + f"""<div class='mid center'>
  <img src='{A}/lion.png' style='width:150px;height:150px;border-radius:34px;border:1px solid rgba(232,181,71,.4);margin:0 auto 46px'>
  <h2>What else should we <em>fight for?</em></h2>
  <p class='body'>Tell us in the comments. The founder reads every one.</p>
  <div class='hi'>आपके परिवार को और क्या चाहिए? कमेंट में बताइए।</div>
  <div><span class='cta'>Register · rakshakid.com</span></div></div>""" + foot("06 / 06", "App launch · Vijay Diwas · 16 Dec")),
]
for i, h in enumerate(p3, 1): S[f"p3_beyond_{i}"] = h

# ---------- P4 Fri: Rakshak Nari "Dependent" ----------
T = "Rakshak Nari"
p4 = [
 page(top(T) + """<div class='mid'><h1>22 years. 14 postings.</h1>
  <h2 style='margin-top:26px'><em>She packed the house 14 times.</em></h2></div>""" + foot("rakshakid.com", swipe=True)),
 page(top(T) + """<div class='mid'><h2>And 14 times, she built a <em>home</em> again.</h2>
  <p class='body'>New city. New school. New neighbours. It felt like home before the last box was empty.</p></div>""" + foot("02 / 07", swipe=True)),
 page(top(T) + """<div class='mid'><h2>2 am. A child with fever. <em>She is alone.</em></h2>
  <p class='body'>3 am. The phone rings. Her heart stops. Every single time.</p></div>""" + foot("03 / 07", swipe=True)),
 page(top(T) + """<div class='mid'><h2>On the call, she says only: <em>sab theek hai.</em></h2>
  <div class='list'><div>The roof was leaking</div><div>The school admission was stuck</div><div>His mother was in hospital</div><div>She had fever herself</div></div>
  <div class='hi'>सब ठीक है।</div></div>""" + foot("04 / 07", swipe=True)),
 page(top(T) + """<div class='mid'><h2>She pinned the medals on his chest.</h2>
  <h2 style='margin-top:20px'><em>Nothing was ever pinned on hers.</em></h2></div>""" + foot("05 / 07", swipe=True)),
 page(top(T) + """<div class='mid'><h2>Every form calls her <em>"dependent".</em></h2>
  <p class='body'>The truth is, <b>he depended on her.</b> Every posting. Every silence.</p></div>""" + foot("06 / 07", swipe=True)),
 page(top(T) + f"""<div class='mid center'>
  <img src='{A}/lion.png' style='width:140px;height:140px;border-radius:32px;border:1px solid rgba(232,181,71,.4);margin:0 auto 40px'>
  <h1 style='font-size:76px'>She is a <em>Rakshak Nari.</em></h1>
  <p class='body'>Every wife and mother who stands behind a protector. Rakshak ID is being built for her too: her own verified identity, and support we are working on for admissions, insurance and her own business.</p>
  <div class='hi'>वह रक्षक नारी है।</div>
  <p class='body' style='font-size:30px'><b>Tag your Rakshak Nari and write "Thank you".</b></p>
  <div><span class='cta'>Register · rakshakid.com</span></div></div>""" + foot("07 / 07", "App launch · Vijay Diwas · 16 Dec")),
]
for i, h in enumerate(p4, 1): S[f"p4_nari_{i}"] = h

# ---------- Stories ----------
def story(name, tag, body, left="@rakshakid", right="Link in bio"):
    S[name] = page(top(tag) + f"<div class='mid center'>{body}</div>" + foot(left, right), 1080, 1920, STORY_X)

story("s1_count65", "Countdown", """<div class='big-num'>65</div><h2 style='margin-top:20px'>days to <em>Vijay Diwas.</em></h2>
 <p class='body'>Rakshak ID launches on <b>16 December 2026.</b></p><div class='hi'>विजय दिवस तक 65 दिन</div><div><span class='cta'>Register early · rakshakid.com</span></div>""")
story("s2_matters", "Your voice", """<h2>What matters most to <em>your family?</em></h2>
 <div class='list' style='text-align:left;margin:50px auto 0;width:fit-content'><div>1 · Children's education</div><div>2 · Medical costs</div><div>3 · Building a home</div><div>4 · A child's wedding</div></div>
 <p class='body'>Reply with a number. We read every message.</p><div class='hi'>नंबर लिखकर जवाब दीजिए।</div>""", right="Reply to this story")
story("s4_capf", "One parivar", """<h2>CAPF families <em>belong here too.</em></h2>
 <div class='list' style='text-align:left;margin:50px auto 0;width:fit-content'><div>BSF · CRPF · CISF</div><div>ITBP · SSB · NDRF</div><div>Assam Rifles · Coast Guard · DSC</div></div>
 <p class='body'>Same uniform spirit. Same honour. Same privileges.</p><div class='hi'>एक वर्दी, एक परिवार।</div><div><span class='cta'>Register · rakshakid.com</span></div>""")
story("s5_nari_teaser", "Tonight · 7:30 PM", """<h2>Tonight: a story about the woman <em>every fauji depends on.</em></h2>
 <p class='body'>Watch our feed at <b>7:30 PM.</b></p><div class='hi'>आज शाम 7:30 बजे</div>""", right="Turn on notifications")
story("s6_who", "Who can join", """<h2>Who can join <em>Rakshak ID?</em></h2>
 <div class='list' style='text-align:left;margin:50px auto 0;width:fit-content'><div>Veterans: Army, Navy, Air Force, CAPF, Assam Rifles, Coast Guard, DSC</div><div>Veer Naris</div><div>Rakshak Naris</div><div>Agniveers who completed tenure</div><div>Parents, spouse and children</div></div>
 <p class='body'><b>Free to register.</b></p><div><span class='cta'>Register · rakshakid.com</span></div>""")
story("s7_count59", "Countdown", """<div class='big-num'>59</div><h2 style='margin-top:20px'>days to <em>Vijay Diwas.</em></h2>
 <p class='body'>Early members get <b>extra privileges</b> at launch.</p><div class='hi'>विजय दिवस तक 59 दिन</div><div><span class='cta'>Register early · rakshakid.com</span></div>""")

# ---------- LinkedIn cards (1080x1350) ----------
S["li1_brands"] = page(top("From the Founder") + """<div class='mid'><div class='eyebrow'>Building Rakshak ID</div>
 <h1>Brands trust <em>the uniform.</em></h1><p class='body'>My biggest fear was that brands would not come. In two days, <b>more than 100</b> said yes.</p></div>""" + foot("Col Arvind Vannur, Veteran", "rakshakid.com"))
S["li2_soldier"] = page(top("From the Founder") + """<div class='mid'><div class='eyebrow'>A question from a banker</div>
 <h1>Who is <em>a soldier?</em></h1><p class='body'>Why I included every uniformed force, BSF to Coast Guard, in Rakshak ID.</p></div>""" + foot("Col Arvind Vannur, Veteran", "rakshakid.com"))

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
 "r1_who": [
  top("") + """<div class='mid center'><h1 style='font-size:120px'>Who is a <em>Rakshak?</em></h1><div class='hi' style='font-size:52px;margin-top:50px'>रक्षक कौन है?</div></div>""" + F,
  top("") + """<div class='mid center'><h1 style='font-size:96px'>Everyone who <em>wore the uniform.</em></h1><p class='body' style='font-size:40px'>Army · Navy · Air Force · CAPF<br>Assam Rifles · Coast Guard · DSC</p></div>""" + F,
  top("") + """<div class='mid center'><h1 style='font-size:96px'>And everyone who <em>stood behind them.</em></h1><p class='body' style='font-size:40px'>Veer Naris · Rakshak Naris<br>Parents · Children · Agniveers</p></div>""" + F,
  top("") + """<div class='mid center'><div class='big-num' style='font-size:240px'>2.5 Cr</div><h1 style='font-size:100px'>One <em>parivar.</em></h1><div class='hi' style='font-size:52px;margin-top:40px'>एक परिवार।</div></div>""" + F,
  endcard("Register early."),
 ],
 "r2_where": [
  top("") + """<div class='mid center'><h1 style='font-size:110px'>Where should a soldier <em>be thanked?</em></h1><div class='hi' style='font-size:52px;margin-top:50px'>सैनिक का धन्यवाद कहाँ हो?</div></div>""" + F,
  top("") + """<div class='mid center'><h1 style='font-size:110px;line-height:1.3'>At the chemist.<br><em>At the school desk.</em></h1></div>""" + F,
  top("") + """<div class='mid center'><h1 style='font-size:110px;line-height:1.3'>At the hospital.<br><em>In the boardroom.</em></h1></div>""" + F,
  top("") + """<div class='mid center'><h1 style='font-size:104px'>Everywhere life <em>takes him.</em></h1><div class='hi' style='font-size:56px;margin-top:50px'>वर्दी की शान, हर जगह सम्मान।</div></div>""" + F,
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
            tall = name.startswith("s") or name.startswith("r")
            w, h = (1080, 1920) if tall else (1080, 1350)
            pg = await b.new_page(viewport={"width": w, "height": h})
            f = ROOT / "html" / f"w2_{name}.html"; f.write_text(html)
            await pg.goto(f.as_uri()); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(OUT / f"{name}.png")); await pg.close()
        await b.close()

def make_reel(r, n):
    D, Tr = 3.4, 0.6; total = n * D - (n - 1) * Tr
    inp = []
    for i in range(n): inp += ["-loop", "1", "-t", str(D), "-i", str(OUT / f"{r}_s{i}.png")]
    fl = [f"[{i}:v]scale=1188:2112,zoompan=z='min(1+0.0009*on,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(D*30)}:s=1080x1920:fps=30,format=yuv420p,setsar=1[v{i}]" for i in range(n)]
    prev = "v0"
    for i in range(1, n):
        fl.append(f"[{prev}][v{i}]xfade=transition=fade:duration={Tr}:offset={i*(D-Tr):.2f}[x{i}]"); prev = f"x{i}"
    fl.append(f"[{prev}]fade=t=in:st=0:d=0.5,fade=t=out:st={total-0.6:.2f}:d=0.6[vout]")
    fl.append(f"aevalsrc='0.10*sin(2*PI*146.83*t)+0.07*sin(2*PI*220*t)+0.06*sin(2*PI*293.66*t)+0.04*sin(2*PI*369.99*t)*(0.6+0.4*sin(2*PI*0.25*t))':s=44100:d={total:.2f},lowpass=f=1800,afade=t=in:d=1.5,afade=t=out:st={total-2:.2f}:d=2[aout]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-filter_complex", ";".join(fl), "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
        "-t", f"{total:.2f}", str(OUT / f"{r}.mp4")], check=True)

if __name__ == "__main__":
    asyncio.run(shots())
    for r, sc in REELS.items(): make_reel(r, len(sc))
    print("done", len(S), "images,", len(REELS), "reels")
