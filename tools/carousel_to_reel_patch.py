"""Reel versions of carousel slides: remove 'Swipe', slide counters and 'slide 12' wording;
add the gift tag on every slide except the end card (labels moved down to make room)."""
import sys, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
R, OUT = sys.argv[1], sys.argv[2]
FONT = R + '/tools/fonts/DMSans[opsz,wght].ttf'
def font(s): f = ImageFont.truetype(FONT, s); f.set_variation_by_axes([min(s, 40), 400]); return f
def inpaint(img, mask):
    a = np.array(img); bgr = cv2.cvtColor(a, cv2.COLOR_RGB2BGR)
    return Image.fromarray(cv2.cvtColor(cv2.inpaint(bgr, mask, 7, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB))
def erase_text(img, box, thr=110):
    x0, y0, x1, y1 = box; a = np.array(img)
    m = np.zeros(a.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = (a[y0:y1, x0:x1].min(2) > thr).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((5, 5), np.uint8), iterations=2)
    return inpaint(img, m)
def erase_counter(img, box):
    # replace the counter area by a per-column vertical interpolation of the rows just above and below
    x0, y0, x1, y1 = box; a = np.array(img).astype(float)
    top = a[y0 - 2:y0, x0:x1].mean(0); bot = a[y1:y1 + 2, x0:x1].mean(0)
    h = y1 - y0; t = (np.arange(h) / (h - 1))[:, None, None]
    fill = top[None] * (1 - t) + bot[None] * t
    fill = cv2.GaussianBlur(fill, (0, 0), 3)
    # feather the left/right edges
    w = x1 - x0; ramp = np.clip(np.minimum(np.arange(w), w - 1 - np.arange(w)) / 10, 0, 1)[None, :, None]
    a[y0:y1, x0:x1] = fill * ramp + a[y0:y1, x0:x1] * (1 - ramp)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def clone_left(img, box, dx=115):
    x0, y0, x1, y1 = box; a = np.array(img).astype(float)
    src = a[y0:y1, x0 - dx:x1 - dx]
    h, w = y1 - y0, x1 - x0
    fy = np.clip(np.minimum(np.arange(h), h - 1 - np.arange(h)) / 8, 0, 1)
    fx = np.clip(np.minimum(np.arange(w), w - 1 - np.arange(w)) / 8, 0, 1)
    m = (fy[:, None] * fx[None, :])[..., None]
    a[y0:y1, x0:x1] = src * m + a[y0:y1, x0:x1] * (1 - m)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def fsr_rect(img, box):
    x0, y0, x1, y1 = box; a = np.array(img)
    pad = 60; X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(1080, x1 + pad), y1 + pad
    sub = cv2.cvtColor(a[Y0:Y1, X0:X1], cv2.COLOR_RGB2BGR)
    m = np.full(sub.shape[:2], 255, np.uint8); m[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = 0
    out = sub.copy()
    cv2.xphoto.inpaint(sub, m, out, cv2.xphoto.INPAINT_FSR_BEST)
    a[Y0:Y1, X0:X1] = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    # restore grain: add high-frequency detail borrowed from the area just below the hole
    a = a.astype(float); h, w = y1 - y0, x1 - x0
    donor = a[y1 + 4:y1 + 4 + h, x0:x1]
    detail = donor - cv2.GaussianBlur(donor, (0, 0), 2.5)
    fy = np.clip(np.minimum(np.arange(h), h - 1 - np.arange(h)) / 6, 0, 1)
    fx = np.clip(np.minimum(np.arange(w), w - 1 - np.arange(w)) / 6, 0, 1)
    a[y0:y1, x0:x1] += detail * (fy[:, None] * fx[None, :])[..., None]
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))
def fsr_counter(img, box):
    # inpaint only the counter glyphs (tight mask) with FSR so surrounding detail survives
    x0, y0, x1, y1 = box; a = np.array(img); ai = a.astype(int)
    sub = ai[y0:y1, x0:x1]
    # local background estimate: heavy median blur; glyphs differ strongly from it
    bg = cv2.medianBlur(a[y0:y1, x0:x1], 15).astype(int)
    m = (np.abs(sub - bg).sum(2) > 45).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=2)
    pad = 40; X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(1080, x1 + pad), y1 + pad
    full = np.zeros(a.shape[:2], np.uint8); full[y0:y1, x0:x1] = m
    win = cv2.cvtColor(a[Y0:Y1, X0:X1], cv2.COLOR_RGB2BGR); keep = 255 - full[Y0:Y1, X0:X1]
    out = win.copy(); cv2.xphoto.inpaint(win, keep, out, cv2.xphoto.INPAINT_FSR_FAST)
    a[Y0:Y1, X0:X1] = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
    return Image.fromarray(a)
def fix_answers(img):
    a = np.array(img); n = a.copy()
    n[255:1350] = a[195:1290]
    n[195:255] = cv2.resize(a[165:195], (1080, 60), interpolation=cv2.INTER_LINEAR)
    # extend the panel and its gold bar past the overflowing last line (text now ends ~1153)
    straight = n[1090, 44:66].copy()
    n[1098:1180, 44:84] = n[1098:1180, 2:42]           # wipe old bar corner with neighbouring background
    # panel interior is the background darkened by the translucent panel; continue it down to 1172
    reg = n[1098:1172, 58:1029].astype(float)
    text = reg.max(2) > 90
    dark = reg * 0.55
    h, w = reg.shape[:2]
    mk = Image.new('L', (w, h), 0); ImageDraw.Draw(mk).rounded_rectangle((0, -30, w - 1, h - 1), radius=18, fill=255)
    mk = (np.array(mk) / 255.0)[..., None]
    out = np.where(text[..., None], reg, dark * mk + reg * (1 - mk))
    n[1098:1172, 58:1029] = out.clip(0, 255).astype(np.uint8)
    n[1098:1150, 44:66] = np.where((straight.astype(int).max(1) > 120)[None, :, None], straight[None], n[1098:1150, 44:66])
    n[1148:1174, 44:72] = np.where((a[1040:1066, 44:72].astype(int).max(2) > 90)[..., None], a[1040:1066, 44:72], n[1148:1174, 44:72])
    return Image.fromarray(n)
def erase_rect(img, box):
    a = np.array(img); m = np.zeros(a.shape[:2], np.uint8); x0, y0, x1, y1 = box; m[y0:y1, x0:x1] = 255
    return inpaint(img, m)
def pill_patch(src, box):
    x0, y0, x1, y1 = box; p = src.crop(box)
    mk = Image.new('L', p.size, 0); h = y1 - y0
    ImageDraw.Draw(mk).rounded_rectangle((1, 1, p.size[0] - 2, p.size[1] - 2), radius=h // 2 - 1, fill=255)
    return p, mk
def move_label(img, y_from, y_to, xmax=None):
    a = np.array(img).astype(int)
    # label = dark rounded box starting at the gold bar (x~52); find its right edge on the row just below the text
    edges = []
    for yy in (y_from + 3, y_from + 43):
        row = a[yy].max(1); ref = np.median(row[60:70]); x = 60
        while x < 900 and abs(row[x] - ref) < 35: x += 1
        edges.append(x)
    x1 = min(min(edges) + 1, xmax or 900)
    box = (50, y_from - 1, x1 + 1, y_from + 49)
    patch = img.crop(box)
    mk = Image.new('L', patch.size, 0)
    ImageDraw.Draw(mk).rounded_rectangle((0, 0, patch.size[0] - 1, patch.size[1] - 1), radius=8, fill=255)
    img = erase_rect(img, box)
    img.paste(patch, (50, y_to - 1), mk)
    return img
def jpg(img, name): img.save(f'{OUT}/{name}.jpg', quality=95)
def load(wk, n): return Image.open(f'{R}/weeks/{wk}/{n}.jpg').convert('RGB')

# ---------- w5-c3 (5 slides; pill on 1-2; dark counter pill top-right; Swipe bottom-right on 1-4)
src = load('2026-w5', 'w5-c3_2'); pill = pill_patch(src, (52, 171, 879, 223))
for i in range(1, 6):
    im = load('2026-w5', f'w5-c3_{i}')
    im = fsr_rect(im, (936, 74, 1034, 126))   # "i/5" counter pill
    if i <= 4: im = erase_text(im, (910, 1270, 1024, 1308))  # Swipe ->
    if i in (3, 4): im.paste(pill[0], (52, 171), pill[1])
    jpg(im, f'w5-c3_{i}')

# ---------- w6 carousels: gold mono counter "NN/NN" at ~(925..1035, 62..95); pill y182-228; labels at 182 move to 250
def w6(c, n, pillbox, labelled, line_fix=None, xmax={}, nopill=()):
    src = load('2026-w6', f'{c}_2'); pill = pill_patch(src, pillbox)
    for i in range(1, n + 1):
        im = load('2026-w6', f'{c}_{i}')
        im = fsr_counter(im, (905, 62, 1050, 96))
        if line_fix: im = line_fix(im, i)
        if c == 'w6-c3' and i == 12: im = fix_answers(im)
        if 3 <= i <= n - 1 and i not in nopill:
            if i in labelled: im = move_label(im, 182, 250, xmax.get(i))
            im.paste(pill[0], (pillbox[0], pillbox[1]), pill[1])
        jpg(im, f'{c}_{i}')

def c1_fix(im, i):
    if i == 1:
        im = erase_text(im, (470, 526, 835, 562))
        ImageDraw.Draw(im).text((474, 521), 'One force at a time.', font=font(30), fill=(216, 218, 217))
    return im
def c2_fix(im, i):
    if i == 1: im = erase_text(im, (517, 886, 615, 928))
    return im
def c3_fix(im, i):
    if i == 1:
        im = erase_text(im, (90, 931, 590, 967))
        ImageDraw.Draw(im).text((95, 926), '10 forces. Answers at the end.', font=font(30), fill=(220, 218, 214))
    elif 2 <= i <= 11:
        full = 'Finish the line. Answer on slide 12.'; keep = 'Finish the line. Answer '
        best = min(range(24, 34), key=lambda s: abs(font(s).getlength(full) - (539 - 96)))
        f = font(best); sc = (539 - 96) / f.getlength(full)
        cut = int(96 + f.getlength(keep) * sc) - 1
        im = erase_text(im, (cut, 929, 546, 962))
        top = f.getbbox('F')[1]
        ImageDraw.Draw(im).text((cut + 1, 935 - top), 'at the end.', font=f, fill=(220, 218, 214))
    return im
w6('w6-c1', 10, (52, 181, 962, 229), labelled=set(range(3, 9)), line_fix=c1_fix)
w6('w6-c2', 8, (52, 181, 965, 229), labelled=set(), line_fix=c2_fix)
w6('w6-c3', 13, (52, 181, 857, 227), labelled=set(range(3, 12)), line_fix=c3_fix, xmax={4: 330})
print('done')
