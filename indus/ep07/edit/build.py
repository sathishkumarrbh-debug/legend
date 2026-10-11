"""Indus Files #7 (Dancing Girl) assets, built to the EP6 production review. Run from the episode folder."""
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, fxkit as fx
from fxkit import W, H, ease, font, outlined, GOLD2, CHALK
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
I = "images/"; todo = sys.argv[1:] or ["hook", "dig", "look", "bangles", "carved", "wax", "clay", "heat", "pour", "break", "born", "one", "quote", "dancer", "today", "trade", "weights", "ending"]
GA = Image.open(I + "girl_a.jpg").convert("RGB"); GB = Image.open(I + "girl_b.jpg").convert("RGB")
BG_BLUR = {}

def photo_cam(src, cx, cy, ch, z=1.0, key=None):
    """W x H view of a real photo: centre (cx, cy), source height ch / z; out-of-frame filled with a dark blurred copy."""
    ch = ch / z; cw = ch * W / H; x0, y0 = cx - cw / 2, cy - ch / 2
    k = id(src)
    if k not in BG_BLUR: BG_BLUR[k] = Image.blend(fx.cover(src).filter(ImageFilter.GaussianBlur(40)), Image.new("RGB", (W, H)), 0.6)
    out = BG_BLUR[k].copy(); sx0, sy0, sx1, sy1 = max(0, x0), max(0, y0), min(src.width, x0 + cw), min(src.height, y0 + ch)
    part = src.crop((int(sx0), int(sy0), int(sx1), int(sy1))); s = H / ch
    part = part.resize((max(1, int(part.width * s)), max(1, int(part.height * s))), Image.LANCZOS)
    out.paste(part, (int((sx0 - x0) * s), int((sy0 - y0) * s))); return out.convert("RGBA"), (x0, y0, s)

def to_px(p, cam): x0, y0, s = cam; return ((p[0] - x0) * s, (p[1] - y0) * s)

def ai(i): return np.asarray(fx.cover(Image.open(I + f"ai{i}.png").convert("RGB")))
AIT = "ARTIST'S IMPRESSION"
def ai_tag(im): outlined(ImageDraw.Draw(im), (W / 2, 1830), AIT, font(fx.F_TITLE, 26), (230, 230, 230, 190), stroke=2); return im

FACE_A = (996, 330); HIP_A = (700, 880); ARM_B = (1168, 1010); FACE_B = (935, 340)

if "hook" in todo:   # 0.00-4.64: tight bright face crop already moving -> snap out at 0.6 to the small full figure + ruler (2.74)
    def frame(t):
        if t < 0.6:
            im, _ = photo_cam(GA, FACE_A[0], FACE_A[1], 600, 1.0 + 0.05 * t / 0.6); im = ImageEnhance.Contrast(ImageEnhance.Brightness(im.convert("RGB")).enhance(1.35)).enhance(1.1).convert("RGBA")
        else:
            u = ease((t - 0.6) / 0.3); ch = 600 + (4400 - 600) * u
            cy = FACE_A[1] + (1100 - FACE_A[1]) * u; cx = FACE_A[0] + (900 - FACE_A[0]) * u
            im, cam = photo_cam(GA, cx, cy, ch, 1.0 + 0.03 * max(0, t - 0.9))
            if t > 2.6:   # ruler beside her: 10.5 cm (figure ~ y 170..1950 in the source)
                q = ease((t - 2.6) / 0.35); top, bot = to_px((1420, 175), cam), to_px((1420, 1945), cam); d = ImageDraw.Draw(im)
                yb = bot[1]; yt = yb - (yb - top[1]) * q
                d.line((top[0], yb, top[0], yt), fill=GOLD2 + (255,), width=8)
                for yy in (yb, yt): d.line((top[0] - 24, yy, top[0] + 24, yy), fill=GOLD2 + (255,), width=8)
                if q > 0.9: fx.pill(im, "10.5 CM", (top[0] + 10, (yb + yt) / 2), 40, anchor="lm"); fx.pill(im, "SMALLER THAN YOUR HAND", (W / 2 - 80, 1560), 36)
        if 2.7 < t < 4.6: fx.pill(im, "INDUS FILES · CASE 07", (40, 250), 30, int(255 * min(1, (t - 2.7) / 0.2)), anchor="lm")
        return im
    fx.write_mp4(frame, 4.9, I + "c_hook.mp4")

if "dig" in todo:   # 4.64-9.52: AI 1926 dig, parallax + dust; snap punch-in on the trowel at 1.4; pill at 2.6
    src = ai(1)
    def frame(t):
        im = fx.parallax_warp(src, t, 5.0, 1, 26, 6, (1.04, 1.1), (0.4 if t > 1.4 else 0.5, 0.62 if t > 1.4 else 0.5), snap=1.4)
        fx.particles(im, t, "dust", 70, 4, (0, 300, W, 1700), 1.0)
        if t > 2.6: fx.pill(im, "MOHENJO-DARO · 1926", (W / 2 - 80, 330), 38, int(255 * min(1, (t - 2.6) / 0.2)))
        return ai_tag(im)
    fx.write_mp4(frame, 5.1, I + "c_dig.mp4")

if "look" in todo:   # 9.52-12.69: face/shoulders -> HARD CUT hand on hip (1.03, ink ellipse) -> snap to chin (2.24, ink tick)
    def frame(t):
        if t < 1.03:
            im, cam = photo_cam(GA, FACE_A[0], FACE_A[1] - 30, 640, 1.0 + 0.04 * t)
        elif t < 2.24:
            im, cam = photo_cam(GA, HIP_A[0], HIP_A[1], 900, 1.0 + 0.04 * (t - 1.03)); q = (t - 1.1) / 0.45
            c = to_px((756, 890), cam); fx.ink_stroke(im, fx.ink_ellipse(c[0], c[1], 170, 120), q, 13, seed=2)
            if t > 1.4: fx.pill(im, "HAND ON HIP", (W / 2 - 80, 330), 40)
        else:
            z = fx.snapz(t - 2.24, 0.0, (1.0, 1.02), 1.0, 0.15); im, cam = photo_cam(GA, FACE_A[0], FACE_A[1] + 30, 640, z)
            a = to_px((960, 470), cam); b = to_px((1060, 455), cam); fx.ink_stroke(im, [(a[0] - 60, a[1] + 30), a, b, (b[0] + 80, b[1] - 60)], (t - 2.3) / 0.35, 12, seed=3)
            if t > 2.45: fx.pill(im, "CHIN UP", (W / 2 - 80, 330), 40)
        return im
    fx.write_mp4(frame, 3.5, I + "c_look.mp4")

if "bangles" in todo:   # 12.69-18.12: arm crop; ink line runs up the bangles while a counter ticks 1->24 (lands 3.38 = "24"); SEEN card 3.9
    pts_src = [(1190, 1240), (1192, 1120), (1192, 1000), (1188, 880), (1180, 790)]
    def frame(t):
        im, cam = photo_cam(GB, 1250, 840, 880, 1.0 + 0.06 * ease(t / 5.6))
        q = (t - 0.6) / 2.75; fx.ink_stroke(im, [to_px(p, cam) for p in pts_src], q, 14, seed=5)
        n = int(round(24 * ease(min(1, max(0, (t - 0.6) / 2.78)))))
        if t > 0.6: fx.pill(im, f"{n}", (W / 2 + 260, 700), 96 if n < 24 else 110, color=(255, 255, 255) if n < 24 else GOLD2)
        if t > 3.9:
            a = int(255 * min(1, (t - 3.9) / 0.2)); fx.pill(im, "SEEN: 24 BANGLES + 4 ON THE OTHER ARM", (W / 2 - 80, 330), 34, a)
        return im
    fx.write_mp4(frame, 5.7, I + "c_bangles.mp4")

if "carved" in todo:   # 18.12-19.40: "She isn't carved." snap on the bronze face (girl_b)
    def frame(t):
        z = fx.snapz(t, 0.05, (1.0, 1.02), 1.4, 0.14); im, cam = photo_cam(GB, FACE_B[0], FACE_B[1] + 80, 760, z)
        if t > 0.35: fx.pill(im, "NOT CARVED", (W / 2 - 80, 330), 40)
        return im
    fx.write_mp4(frame, 1.6, I + "c_carved.mp4")

def process(i, out, dur, step, extra=None, title=None, snap=None, focus=(0.5, 0.5), direction=1):
    src = ai(i)
    def frame(t):
        im = fx.parallax_warp(src, t, dur, direction, 24, 6, (1.05, 1.12), focus, snap=snap)
        if extra: extra(im, t)
        if step: fx.pill(im, step, (40, 250), 34, int(255 * min(1, t / 0.15)), anchor="lm")
        if title and t > title[1]: fx.pill(im, title[0], (W / 2 - 80, 330), 64, int(255 * min(1, (t - title[1]) / 0.15)), color=GOLD2)
        return ai_tag(im)
    fx.write_mp4(frame, dur, I + out)

if "wax" in todo:   # 19.40-24.65: cast in bronze ... LOST-WAX title at 2.4; step 1 at 3.87
    def ex(im, t): fx.particles(im, t, "dust", 40, 6, (0, 200, W, 1500), 0.7)
    src = ai(2)
    def frame(t):
        im = fx.parallax_warp(src, t, 5.4, 1, 24, 6, (1.05, 1.12), (0.5, 0.5), snap=3.87); ex(im, t)
        if t > 2.4: fx.pill(im, "LOST-WAX", (W / 2 - 80, 330), 70, int(255 * min(1, (t - 2.4) / 0.15)), color=GOLD2)
        if t > 3.87: fx.pill(im, "1 · WAX", (40, 250), 34, anchor="lm")
        return ai_tag(im)
    fx.write_mp4(frame, 5.4, I + "c_wax.mp4")
if "clay" in todo: process(3, "c_clay.mp4", 1.4, "2 · CLAY", lambda im, t: fx.particles(im, t, "dust", 30, 7, (0, 200, W, 1500), 0.6), direction=-1)
if "heat" in todo:
    def ex(im, t):
        fx.particles(im, t, "embers", 70, 8, (150, 500, 950, 1500), 1.0)
    src = ai(4)
    def frame(t):
        im = fx.parallax_warp(src, t, 2.3, 1, 22, 6, (1.05, 1.12)); im = fx.heat_haze(im, t, (200, 200, 900, 760), 3).convert("RGBA"); ex(im, t)
        fx.pill(im, "3 · HEAT", (40, 250), 34, anchor="lm"); return ai_tag(im)
    fx.write_mp4(frame, 2.3, I + "c_heat.mp4")
if "pour" in todo: process(5, "c_pour.mp4", 1.7, "4 · POUR", lambda im, t: fx.particles(im, t, "sparks", 60, 9, (500, 400, 1000, 1200), 1.0), direction=-1)
if "break" in todo: process(6, "c_break.mp4", 1.3, "5 · BREAK", lambda im, t: fx.particles(im, t, "dust", 80, 10, (300, 500, 1000, 1400), 1.2))

if "born" in todo:   # 30.58-31.92: "and she's born" -> snap onto the real face (stone scrape)
    def frame(t):
        z = fx.snapz(t, 0.0, (1.0, 1.02), 1.4, 0.15); im, _ = photo_cam(GA, FACE_A[0], FACE_A[1] + 60, 820, z)
        g = Image.new("RGBA", (W, H), (255, 190, 110, int(70 * max(0, 1 - t / 0.5)))); im.alpha_composite(g); return im
    fx.write_mp4(frame, 1.5, I + "c_born.mp4")

if "one" in todo:   # 31.92-36.16: one mould, one statue, no other like her (girl_b upper body side light, push + rim glow)
    def frame(t):
        im, cam = photo_cam(GB, FACE_B[0] + 30, FACE_B[1] + 40, 700, 1.0 + 0.08 * ease(t / 4.4))
        if t > 0.0: fx.pill(im, "1 MOULD", (W / 2 - 80, 300), 46, int(255 * min(1, t / 0.15)))
        if t > 0.96: fx.pill(im, "= 1 STATUE", (W / 2 - 80, 390), 46, int(255 * min(1, (t - 0.96) / 0.15)))
        if t > 2.37: fx.pill(im, "ONE OF A KIND", (W / 2 - 80, 1600), 50, int(255 * min(1, (t - 2.37) / 0.2)), color=GOLD2)
        return im
    fx.write_mp4(frame, 4.4, I + "c_one.mp4")

if "quote" in todo:   # 36.16-41.84: aged-paper quote card; types on 38.72-41.28 (t 2.56-5.12)
    txt = ["“Perfectly confident", "of herself", "and the world.”"]
    rng = np.random.default_rng(3); paper = np.clip(np.stack([226 + rng.normal(0, 6, (520, 900)), 210 + rng.normal(0, 6, (520, 900)), 170 + rng.normal(0, 6, (520, 900))], -1), 0, 255).astype(np.uint8)
    paper = Image.fromarray(paper).filter(ImageFilter.GaussianBlur(1.2)).convert("RGBA")
    pd = ImageDraw.Draw(paper); pd.rectangle((0, 0, 899, 519), outline=(120, 90, 50, 255), width=6)
    def frame(t):
        im, _ = photo_cam(GA, FACE_A[0], FACE_A[1] + 40, 760, 1.05 + 0.08 * ease(t / 5.8)); im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), 0.45)
        q = ease((t - 0.2) / 0.4)
        if q > 0:
            card = paper.copy(); d = ImageDraw.Draw(card); f = font(fx.F_TITLE, 64)
            nchar = int(sum(len(l) for l in txt) * min(1, max(0, (t - 2.56) / 2.5))); k = 0
            for j, l in enumerate(txt):
                show = l[:max(0, nchar - k)]; k += len(l); d.text((60, 70 + j * 95), show, font=f, fill=(45, 30, 15, 255))
            d.text((60, 400), "SIR MORTIMER WHEELER, 1973", font=font(fx.F_BIG, 40), fill=(120, 40, 30, 255))
            card = card.rotate(-2, expand=True, resample=Image.BICUBIC); y = int(560 + (1 - q) * 500)
            sh = Image.new("RGBA", card.size, (0, 0, 0, 0)); sh.putalpha(card.getchannel("A").point(lambda v: v // 2)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), ((W - card.width) // 2 - 70, y + 14))
            im.alpha_composite(card, ((W - card.width) // 2 - 80, y))
        return im
    fx.write_mp4(frame, 5.8, I + "c_quote.mp4")

if "dancer" in todo:   # 41.84-46.44: hand-on-hip pose; twist at 2.22 (44.06): one red stamp DANCER? + THEORY pill
    def frame(t):
        im, cam = photo_cam(GA, HIP_A[0] + 30, HIP_A[1] - 120, 900, 1.0 + 0.06 * ease(t / 4.8))
        if t > 2.22:
            q = min(1, (t - 2.22) / 0.11); s = 2.0 - ease(q); f = font(fx.F_BIG, int(150 * s)); lay = Image.new("RGBA", (W, H)); ld = ImageDraw.Draw(lay)
            c = (W / 2 - 80, 700); tw = ld.textlength("DANCER?", font=f)
            ld.rounded_rectangle((c[0] - tw / 2 - 30, c[1] - 110 * s, c[0] + tw / 2 + 30, c[1] + 110 * s), 24, fill=(15, 8, 6, 160), outline=(225, 45, 40, 255), width=14)
            ld.text(c, "DANCER?", font=f, fill=(225, 45, 40, 255), anchor="mm"); im.alpha_composite(lay.rotate(-7, center=c, resample=Image.BICUBIC))
            if t > 2.5: fx.pill(im, "THEORY, NOT PROOF", (W / 2 - 80, 900), 40, int(255 * min(1, (t - 2.5) / 0.2)))
        return im
    fx.write_mp4(frame, 4.8, I + "c_dancer.mp4")

if "today" in todo:   # 46.44-50.80: split: top Dancing Girl c.2500 BC | bottom Dhokra casting today -> (1.63) Dhokra rhino
    cast = fx.cover(Image.open(I + "dhokra_casting.jpg").convert("RGB"), W, H // 2 - 4); rh = Image.open(I + "dhokra_rhino.jpg").convert("RGB")
    rhino = fx.cover(rh, W, H // 2 - 4)
    def zoomed(img, z):
        im = img.resize((int(img.width * z), int(img.height * z)), Image.LANCZOS); x0, y0 = (im.width - img.width) // 2, (im.height - img.height) // 2
        return im.crop((x0, y0, x0 + img.width, y0 + img.height))
    def frame(t):
        top, _ = photo_cam(GA, FACE_A[0], FACE_A[1] + 30, 1100, 1.0 + 0.05 * ease(t / 4.5)); top = top.crop((0, H // 4, W, H // 4 + H // 2 - 4))
        im = Image.new("RGBA", (W, H), (0, 0, 0, 255)); im.paste(top, (0, 0))
        bot = zoomed(cast, 1.0 + 0.08 * ease(t / 1.7)) if t < 1.63 else zoomed(rhino, 1.0 + 0.06 * ease((t - 1.63) / 2.8))
        im.paste(bot, (0, H // 2 + 4)); d = ImageDraw.Draw(im); d.rectangle((0, H // 2 - 4, W, H // 2 + 4), fill=GOLD2 + (255,))
        fx.pill(im, "c. 2500 BC · MOHENJO-DARO", (40, 120), 34, anchor="lm")
        fx.pill(im, "TODAY · DHOKRA, ODISHA" if t < 1.63 else "SAME LOST-WAX METHOD", (40, H // 2 + 70), 34, anchor="lm", color=GOLD2 if t >= 1.63 else (245, 240, 230))
        if t < 0.1: im = Image.blend(im, Image.new("RGBA", (W, H), (255, 240, 220, 255)), 0.3 * (1 - t / 0.1))
        return im
    fx.write_mp4(frame, 4.5, I + "c_today.mp4")

if "trade" in todo:   # 50.80-53.66: AI merchant balance, parallax, snap at "weigh it" (1.65)
    src = ai(7)
    def frame(t):
        im = fx.parallax_warp(src, t, 3.0, -1, 24, 6, (1.05, 1.1), (0.5, 0.6 if t > 1.65 else 0.5), snap=1.65)
        fx.particles(im, t, "dust", 50, 12, (0, 200, W, 1500), 0.7); return ai_tag(im)
    fx.write_mp4(frame, 3.0, I + "c_trade.mp4")

if "weights" in todo:   # 53.66-56.5: REAL Indus cube weights (BM), snap punch-in + ink circle on "exact"
    src = Image.open(I + "weights_bm.jpg").convert("RGB")
    def frame(t):
        z = fx.snapz(t, 0.0, (1.0, 1.03), 3.0, 0.12); im, cam = photo_cam(src, 980, 640, 1000, z)
        if t > 0.98: c = to_px((1000, 560), cam); fx.ink_stroke(im, fx.ink_ellipse(c[0], c[1], 420, 260), (t - 0.98) / 0.5, 13, seed=9)
        fx.pill(im, "REAL: INDUS WEIGHTS · BRITISH MUSEUM", (W / 2 - 80, 1600), 34)
        return im
    fx.write_mp4(frame, 3.0, I + "c_weights.mp4")

if "ending" in todo:   # card over the weights, then dissolve to the first face crop (loop)
    src = Image.open(I + "weights_bm.jpg").convert("RGB")
    face, _ = photo_cam(GA, FACE_A[0], FACE_A[1], 600, 1.0); face = ImageEnhance.Brightness(face.convert("RGB")).enhance(1.12).convert("RGBA")
    def frame(t):
        im, _ = photo_cam(src, 980, 640, 1000, 1.12 + 0.03 * t); im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), 0.55); d = ImageDraw.Draw(im)
        a = ease(t / 0.3)
        outlined(d, (W / 2 - 80, 640), "THESE AREN'T DICE…", font(fx.F_BIG, 110), (255, 255, 255, int(255 * a)), stroke=5)
        b = ease((t - 0.7) / 0.3)
        if b > 0:
            outlined(d, (W / 2 - 80, 800), "4,000-YEAR-OLD", font(fx.F_BIG, 110), GOLD2 + (int(255 * b),), stroke=5)
            outlined(d, (W / 2 - 80, 930), "WEIGHTS", font(fx.F_BIG, 110), GOLD2 + (int(255 * b),), stroke=5)
            fx.pill(im, "INDUS FILES #8 · COMMENT YOUR GUESS", (W / 2 - 80, 1080), 34, int(255 * b))
        if t > 3.2: im = Image.blend(im, face, ease((t - 3.2) / 0.45))
        return im
    fx.write_mp4(frame, 4.2, I + "c_ending.mp4")
