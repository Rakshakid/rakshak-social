"""Week 3 (19-25 Oct 2026) spec -> posts.json. Media are JPEG (quality 93)."""
import json, pathlib, sys

TAGS = "#RakshakID #CultureOfGratitude #IndianVeterans #FaujiParivar #VeerNari #RakshakNari #VijayDiwas #JaiHind"
IGFB = ["Instagram", "Facebook"]
REEL = ["Instagram", "Facebook", "YouTube"]
NOCAP = dict(en="(Stories carry no caption.)", hi="(स्टोरी पर कैप्शन नहीं जाता।)", tags="")

SCRIPT_EN = """FOUNDER VIDEO SCRIPT (English, about 55 seconds)

I am Col Arvind Vannur, Veteran.

In service, no one fought alone. We moved as a section, a platoon, a unit. Together.

Then we retire, and something strange happens. Each of us goes his own way. One veteran talking to a bank, alone. One Veer Nari looking for a school admission, alone. One veteran's business looking for its first customers, alone.

Divided, we lose. United, we get opportunities.

There are 2.5 crore of us. Imagine if we spoke as one parivar. Banks, brands and institutions would have to listen.

And to every veteran and fauji family creating content online: you have built your own communities. Let us bring them together. On Rakshak ID, your voice reaches thousands of verified Rakshaks.

Not another card. A parivar that stands together again.

Register early at rakshakid.com. We launch on Vijay Diwas, 16 December. Jai Hind.

FILMING BRIEF
- Phone held upright (9:16), at eye level, about an arm's length away. Back camera if someone can hold it, otherwise front camera.
- Face a window so daylight falls on your face. Quiet room, fans and AC off.
- Plain wall or bookshelf behind you. Blazer or open collar; no rank insignia or service logos in frame.
- Wait 2 seconds before you speak and after you finish. Two or three full takes; small pauses are fine, I will trim them.
- Speak in English or Hindi, whichever feels natural.
- Send the raw video in a Claude chat. I will trim it, burn in English and Hindi captions, add the lion end card with rakshakid.com, and put it on this board for your approval.

POST CAPTION (once filmed)
Divided, we lose. United, we get opportunities.

In service, no one fought alone. After service, too many of us do. 2.5 crore Rakshaks speaking as one parivar is a voice banks, brands and institutions will listen to.

Register early → https://rakshakid.com (link in bio)"""

SCRIPT_HI = """संस्थापक वीडियो स्क्रिप्ट (हिंदी, लगभग 55 सेकंड)

मैं कर्नल अरविंद वन्नूर, वेटरन।

सर्विस में कोई अकेला नहीं लड़ता था। हम सेक्शन, प्लाटून, यूनिट बनकर चलते थे। साथ-साथ।

फिर हम रिटायर होते हैं, और कुछ अजीब होता है। हर कोई अपने रास्ते चल पड़ता है। एक वेटरन बैंक से अकेले बात करता है। एक वीर नारी स्कूल में दाख़िले के लिए अकेले भटकती है। एक वेटरन का बिज़नेस अपने पहले ग्राहक अकेले ढूँढता है।

बँटे रहेंगे तो हारेंगे। साथ रहेंगे तो अवसर मिलेंगे।

हम 2.5 करोड़ हैं। सोचिए, अगर हम एक परिवार की तरह एक आवाज़ में बोलें, तो बैंक, ब्रांड और संस्थाएँ सुनेंगी।

और जो वेटरन और फ़ौजी परिवार ऑनलाइन कंटेंट बनाते हैं: आपने अपनी कम्युनिटी बनाई है। आइए, सबको जोड़ें। रक्षक ID पर आपकी आवाज़ हज़ारों वेरिफ़ाइड रक्षकों तक पहुँचती है।

एक और कार्ड नहीं। एक परिवार, जो फिर से साथ खड़ा है।

rakshakid.com पर जल्दी रजिस्टर करें। हम विजय दिवस, 16 दिसंबर को लॉन्च कर रहे हैं। जय हिंद।"""

POSTS = [
 dict(id="w3-p1", day="Mon 19 Oct", date="2026-10-19", time="19:30", format="Carousel · 6 slides", nets=IGFB,
  title="Culture of Gratitude 5/6: The Change",
  why="The key message: Gen Z and Gen Alpha are watching. Teaching gratitude to the next generation.",
  media=[f"p1_change_{i}.jpg" for i in range(1, 7)], ig_type="POST", fb_type="POST",
  en="Our children are watching.\n\nA whole generation has grown up after Kargil. They never saw the coffins come home. They know the uniform from films and parades.\n\nChildren don't learn gratitude from speeches. They learn it at the shop counter, in the hospital queue, at the school gate, and from what their parents do. One moment of a shopkeeper standing up to thank a veteran teaches more than any textbook.\n\nLet them inherit a nation that remembers.\n\nPart 5 of 6, Culture of Gratitude. Parents: share this with your children.\nRegister early → https://rakshakid.com (link in bio)",
  hi="हमारे बच्चे देख रहे हैं।\n\nकारगिल के बाद पूरी एक पीढ़ी बड़ी हुई है, जिसने आज़ादी की क़ीमत कभी अपनी आँखों से नहीं देखी।\n\nबच्चे भाषणों से कृतज्ञता नहीं सीखते। वे सीखते हैं दुकान के काउंटर पर, अस्पताल की कतार में, और अपने माता-पिता को देखकर।\n\nआने वाली पीढ़ी को ऐसा भारत दें जो याद रखता है।",
  tags=TAGS),
 dict(id="w3-l1", day="Tue 20 Oct", date="2026-10-20", time="09:30", format="LinkedIn · your voice", nets=["LinkedIn"],
  title="The thank-you that costs nothing (Story 1)",
  why="For business leaders: what an everyday Culture of Gratitude looks like, and their role in it. No partners named.",
  media=["li1_thankyou.jpg"], li=True,
  en="Friends of mine who trained in the United States told me something I have never forgotten. Wherever they showed a military ID, at a coffee shop, an airport counter, a hardware store, someone would look up and say: \"Thank you for your service.\"\n\nThe discount, when there was one, was small. That was never the point. The point was being honoured by a stranger, in the middle of an ordinary day.\n\nIn India, our respect for the uniform runs deep. But it shows up on a few days of the calendar. Republic Day. Independence Day. Vijay Diwas. Then it goes quiet.\n\nThat silence has a cost. A generation has grown up after Kargil without seeing what service costs. Children learn values from what they watch adults do, not from what we tell them.\n\nThis is where business leaders have a role. A bank that recognises service at its branch counter. A retailer whose staff know how to say thank you. A hospital desk that makes room for a Veer Nari. Small acts. Together, they build a Culture of Gratitude.\n\nRakshak ID gives organisations a verified way to do this for those who served and their families, 2.5 crore strong.\n\nWe launch on Vijay Diwas, 16 December. If your organisation wants to be part of it, write to partners@rakshakid.com\n\n#RakshakID #CultureOfGratitude #Veterans #Leadership",
  hi="(LinkedIn: English only.)", tags=""),
 dict(id="w3-p2", day="Tue 20 Oct", date="2026-10-20", time="19:30", format="Image · founder quote", nets=IGFB,
  title="Rakshak Nari: \"Why wait?\" (founder quote)",
  why="Your quote card on 6 Oct had our best reach so far, so this week leads with your voice again. Story 3, with the ask for ideas in the comments.",
  media=["p2_samman.jpg"], ig_type="POST", fb_type="POST",
  en="\"Why must we wait until she becomes a Veer Nari to give her samman?\"\nCol Arvind Vannur, Veteran · Founder, Rakshak ID\n\nThe Rakshak Nari lives with a daily fear of the unknown, and carries the home through every posting. Yet every form calls her a dependent.\n\nOn Rakshak ID she gets her own verified identity, not a dependent card. And we are working on fair loans for the many enterprising wives who run a business of their own.\n\nRakshak Naris: what should Rakshak ID do for you? Write it in the comments. I read every one.\nRegister early → https://rakshakid.com (link in bio)",
  hi="\"वीर नारी बनने का इंतज़ार क्यों? उसे सम्मान आज क्यों नहीं?\"\nकर्नल अरविंद वन्नूर, वेटरन · संस्थापक, रक्षक ID\n\nरक्षक ID पर रक्षक नारी को अपनी वेरिफ़ाइड पहचान मिलेगी, डिपेंडेंट कार्ड नहीं।\n\nरक्षक नारियाँ: आपके लिए रक्षक ID क्या करे? कमेंट में लिखिए। मैं हर कमेंट पढ़ता हूँ।",
  tags=TAGS),
 dict(id="w3-r1", day="Wed 21 Oct", date="2026-10-21", time="19:30", format="Reel + YouTube Short · 15 s", nets=REEL,
  title="Is Rakshak ID safe?",
  why="Animated, no filming. Trust and FAQ: free to register, verified in the app, documents deleted within 72 hours, data never sold. Uses the arpeggio music you picked.",
  media=["r1_safe.mp4"], video=True, story=True, poster="r1_safe_s0.jpg", ig_type="REEL", fb_type="REEL",
  yt_title="Is Rakshak ID safe? | Rakshak ID #Shorts", yt={"title": "Is Rakshak ID safe? | Rakshak ID #Shorts", "tags": ["Rakshak ID", "veterans", "Indian Army", "fauji parivar", "Culture of Gratitude"]},
  en="Is Rakshak ID safe? The questions we hear most:\n\nFree to register. Verified in the app. Your documents are deleted within 72 hours. Your data is never sold.\n\nRakshak ID is a private initiative, not affiliated with the Ministry of Defence.\n\nRegister early → https://rakshakid.com",
  hi="क्या रक्षक ID सुरक्षित है? रजिस्ट्रेशन मुफ़्त। ऐप में वेरिफ़िकेशन। दस्तावेज़ 72 घंटे में डिलीट। आपका डेटा कभी बेचा नहीं जाता।",
  tags=TAGS),
 dict(id="w3-l2", day="Thu 22 Oct", date="2026-10-22", time="09:30", format="LinkedIn · your voice", nets=["LinkedIn"],
  title="Every form calls her \"dependent\" (Story 3, for bankers)",
  why="For bank and fintech heads: the Rakshak Nari as an unserved, verified customer, and an open invitation to talk about fair credit. No outcomes promised.",
  media=["li2_dependent.jpg"], li=True,
  en="Every form in a fauji home has a column for the wife. It reads: dependent.\n\nAcross every posting, I saw the opposite. She moves the house every two or three years. She finds the school, runs the home, manages the money, and carries the fear of a phone call at 3 am.\n\nMany of these women are enterprising. They tutor, bake, stitch, run boutiques and small businesses, often starting again in a new city each time.\n\nYet when she walks into a bank for a loan, she often has little financial record in her own name. Her identity is a line on her husband's card.\n\nWe call her a Rakshak Nari. Why must we wait until she becomes a Veer Nari to give her samman?\n\nOn Rakshak ID, every Rakshak Nari gets her own verified identity, not a dependent card. For lenders, that is a verified, disciplined and stable community that is largely unserved.\n\nTo the bankers and fintech leaders here: I would like to talk about fair credit for these women. My inbox is open.\n\nRakshak ID launches on Vijay Diwas, 16 December. https://rakshakid.com\n\n#RakshakID #RakshakNari #FinancialInclusion #WomenEntrepreneurs",
  hi="(LinkedIn: English only.)", tags=""),
 dict(id="w3-p3", day="Thu 22 Oct", date="2026-10-22", time="19:30", format="Carousel · 5 slides", nets=IGFB,
  title="Agniveer: He wore the uniform. That is enough.",
  why="Story 5: same privileges as any veteran, \"never leave a man behind\". Does not debate the scheme.",
  media=[f"p3_agniveer_{i}.jpg" for i in range(1, 6)], ig_type="POST", fb_type="POST",
  en="He wore the uniform. That is enough.\n\nSame oath. Same uniform. Same tricolour. An Agniveer stood where every soldier stands.\n\nThe first years after service are the hardest: a new job to find, skills to turn into a career, maybe a new city, and a family looking to him.\n\nOur rule is simple: never leave a man behind. On Rakshak ID, an Agniveer gets the same privileges as any veteran, and his posts reach thousands of verified Rakshaks.\n\nAgniveers and their families: you belong here. Tag an Agniveer you know.\nRegister early → https://rakshakid.com (link in bio)",
  hi="उसने वर्दी पहनी है। इतना काफ़ी है।\n\nवही शपथ, वही वर्दी, वही तिरंगा।\n\nहमारा नियम: किसी को पीछे नहीं छोड़ना। रक्षक ID पर अग्निवीर को किसी भी वेटरन जैसी ही सुविधाएँ मिलेंगी।\n\nअग्निवीर और उनके परिवार: आप इस परिवार का हिस्सा हैं।",
  tags=TAGS + " #Agniveer"),
 dict(id="w3-r3", day="Fri 23 Oct", date="2026-10-23", time="19:30", format="Founder video reel · 45-60 s · script to film", nets=REEL,
  title="Founder video: Divided, we lose. United, we get opportunities. (Story 4)",
  why="This week's filmed reel. Approve = script approved. Nothing is scheduled until you send the video and approve the edited cut here. Full script, Hindi version and filming brief are in the English and Hindi tabs.",
  media=["v1_script.jpg"], ig_type="REEL", fb_type="REEL", awaiting_video=True,
  status_note="Script only. Do not schedule: the edited founder video replaces the script card after filming.",
  en=SCRIPT_EN, hi=SCRIPT_HI, tags=TAGS),
 dict(id="w3-r2", day="Sun 25 Oct", date="2026-10-25", time="11:00", format="Reel + YouTube Short · 15 s", nets=REEL,
  title="Culture of Gratitude 6/6: The Goal",
  why="Animated finale of the series and of Phase 1: earning respect in service, commanding it for life.",
  media=["r2_goal.mp4"], video=True, story=True, poster="r2_goal_s0.jpg", ig_type="REEL", fb_type="REEL",
  yt_title="A soldier must never fade away | Rakshak ID #Shorts", yt={"title": "A soldier must never fade away | Rakshak ID #Shorts", "tags": ["Rakshak ID", "veterans", "Culture of Gratitude", "fauji parivar", "Vijay Diwas"]},
  en="A soldier must never fade away.\n\nIn service, he earned respect. For life, he should command it. Not a memory. A role model, for every child who is watching.\n\nPart 6 of 6, Culture of Gratitude.\nRegister early → https://rakshakid.com",
  hi="सैनिक को कभी भुलाया न जाए। सेवा में उसने सम्मान कमाया, अब जीवन भर वह सम्मान का हक़दार है। यादों में नहीं, आदर्श बनकर।",
  tags=TAGS),
]

if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "posts.json")
    out.write_text(json.dumps(POSTS, ensure_ascii=False, indent=1))
    print("wrote", out, len(POSTS), "items")
