"""Indus Files #6 assets (Pashupati seal). Run from the episode folder: python3 build.py [names...]"""
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, fxkit as fx
from fxkit import W, H, ease, font, outlined, GOLD, WHITE
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
I = "images/"; todo = sys.argv[1:] or ["hook", "horns", "animals", "legs", "comment", "buffalo", "script", "marshall", "girl", "ending"]
SEAL = I + "seal_mold.jpg"
BOX = {"elephant": (74, 125, 266, 262), "tiger": (110, 300, 312, 446), "rhino": (650, 175, 860, 302), "buffalo": (622, 305, 830, 482),
       "horns": (268, 172, 630, 336), "deer": (385, 735, 600, 838), "script": (225, 72, 835, 190), "face": (410, 325, 505, 420)}
LEG_L = [(372, 628), (420, 638), (462, 648)]; LEG_R = [(738, 608), (600, 628), (470, 648)]
src = Image.open(SEAL).convert("RGB")

def view(box, z0, z1, t, dur):
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2; z = z0 + (z1 - z0) * ease(t / dur)
    cw = (box[2] - box[0]) / z; ch = cw * H / W
    if cw < src.width: cx = min(max(cx, cw / 2), src.width - cw / 2)
    if ch < src.height: cy = min(max(cy, ch / 2), src.height - ch / 2)
    return cx, cy, cw, ch

def render(cam, bgcol=(14, 12, 10)):
    cx, cy, cw, ch = cam; im = Image.new("RGB", (W, H), bgcol)
    x0, y0 = cx - cw / 2, cy - ch / 2; sx0, sy0 = max(0, x0), max(0, y0); sx1, sy1 = min(src.width, x0 + cw), min(src.height, y0 + ch)
    part = src.crop((int(sx0), int(sy0), int(sx1), int(sy1))); s = W / cw
    part = part.resize((max(1, int(part.width * s)), max(1, int(part.height * s))), Image.LANCZOS)
    blur = fx.cover(src).filter(ImageFilter.GaussianBlur(40)); im = Image.blend(blur, Image.new("RGB", (W, H)), 0.55)
    im.paste(part, (int((sx0 - x0) * s), int((sy0 - y0) * s))); return im.convert("RGBA")

def scr(p, cam): cx, cy, cw, ch = cam; s = W / cw; return ((p[0] - (cx - cw / 2)) * s, (p[1] - (cy - ch / 2)) * s)

def ring(im, box, cam, q, color=GOLD, pad=18, width=10):
    a, b = scr(box[:2], cam), scr(box[2:], cam); lay = Image.new("RGBA", (W, H))
    ImageDraw.Draw(lay).arc((a[0] - pad, a[1] - pad, b[0] + pad, b[1] + pad), -90, -90 + 360 * q, fill=color + (255,), width=width)
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(7))); im.alpha_composite(lay)

def tag(d, text, xy, a=255, size=44, color=GOLD): outlined(d, xy, text, font(fx.F_BIG, size), color + (int(a),), stroke=4)
FULL = (0, 0, 888, 913)

if "hook" in todo:
    fx.dust_reveal(SEAL, I + "hook.mp4", peek=(0.5, 0.34, 0.24), t_gust=0.15, sweep=1.1, dur=6.0)   # must outlast line 0 (5.06 s) or it loops
if "horns" in todo:   # line 1 (5.06-8.90): push to the figure, ring the horns at "huge horns" (~3.2 s)
    def frame(t):
        cam = view((180, 120, 720, 700), 1.0, 1.25, t, 4.0); im = render(cam); q = ease((t - 3.0) / 0.45)
        if q > 0: ring(im, BOX["horns"], cam, q); tag(ImageDraw.Draw(im), "HUGE HORNS", (W / 2, 300), 255 * q, 96)
        return im
    fx.write_mp4(frame, 4.4, I + "horns.mp4")
if "animals" in todo:   # line 2 (9.36-15.46): tiger 10.19, elephant 11.02, rhino 12.06, buffalo ~12.9, deer 14.87
    seq = [("tiger", 0.83, "TIGER"), ("elephant", 1.66, "ELEPHANT"), ("rhino", 2.70, "RHINO"), ("buffalo", 3.45, "BUFFALO"), ("deer", 5.45, "2 DEER")]
    def frame(t):
        cam = view((-40, 0, 928, 913), 1.0, 1.04, t, 6.5); im = render(cam); d = ImageDraw.Draw(im)
        for k, (name, tt, lab) in enumerate(seq):
            q = ease((t - tt) / 0.3)
            if q <= 0: continue
            ring(im, BOX[name], cam, q, pad=10, width=8); b = BOX[name]; p = scr(((b[0] + b[2]) / 2, b[3]), cam)
            if name == "deer": p = scr(((b[0] + b[2]) / 2, b[1]), cam); p = (p[0], p[1] - 100)
            tag(d, lab, (p[0], p[1] + 42), 255 * q, 46)
            if name in ("tiger", "elephant") and t > tt + 0.3: tag(d, "SEEN IN PART 5", (p[0], p[1] + 86), 255 * ease((t - tt - 0.3) / 0.3), 28, WHITE)
        return im
    fx.write_mp4(frame, 6.8, I + "animals.mp4")
if "legs" in todo:   # line 4 (21.86-25.86): "heels pressed together" 23.28 (1.42), "knees wide apart" 24.71 (2.85)
    def frame(t):
        cam = view((300, 480, 800, 760), 1.0, 1.15, t, 4.5); im = render(cam); d = ImageDraw.Draw(im)
        for pts, t0 in ((LEG_L, 1.3), (LEG_R, 1.3)):
            p = fx._partial([scr(x, cam) for x in pts], ease((t - t0) / 0.6))
            if len(p) > 1:
                lay = Image.new("RGBA", (W, H)); ImageDraw.Draw(lay).line(p, fill=GOLD + (255,), width=14, joint="curve")
                im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(8))); im.alpha_composite(lay)
        if t > 1.5: tag(d, "HEELS TOGETHER", (W / 2, 300), 255 * ease((t - 1.5) / 0.25), 90)
        if t > 2.85:
            q = ease((t - 2.85) / 0.25)
            for k in (LEG_L[0], LEG_R[0]):
                c = scr(k, cam); d.ellipse((c[0] - 26, c[1] - 26, c[0] + 26, c[1] + 26), outline=GOLD + (int(255 * q),), width=8)
            tag(d, "KNEES WIDE APART", (W / 2, 410), 255 * q, 70, WHITE)
        return im
    fx.write_mp4(frame, 4.8, I + "legs.mp4")
if "comment" in todo:   # lines 5-6 (26.43-35.47): viewer's comment card + MULABANDHASANA + McEvilley label (33.55 -> 7.12)
    def frame(t):
        cam = view((280, 380, 820, 760), 1.0, 1.12, t, 9.5); im = render(cam)
        for pts in (LEG_L, LEG_R):
            lay = Image.new("RGBA", (W, H)); ImageDraw.Draw(lay).line([scr(x, cam) for x in pts], fill=GOLD + (255,), width=14, joint="curve")
            im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(8))); im.alpha_composite(lay)
        top = Image.new("RGBA", (W, H)); ImageDraw.Draw(top).rectangle((0, 0, W, 640), fill=(0, 0, 0, 150)); im.alpha_composite(top.filter(ImageFilter.GaussianBlur(40)))
        d = ImageDraw.Draw(im)
        q = ease((t - 0.2) / 0.35); y = 120 - (1 - q) * 300
        if q > 0:
            d.rounded_rectangle((70, y, W - 70, y + 330), 28, fill=(28, 28, 30, int(235 * q)), outline=(90, 90, 95, int(255 * q)), width=3)
            d.ellipse((110, y + 40, 190, y + 120), fill=(200, 120, 60, int(255 * q))); outlined(d, (150, y + 80), "G", font(fx.F_BIG, 50), WHITE + (int(255 * q),), stroke=0)
            d.text((215, y + 48), "@guharup  ·  Part 5", font=font(fx.F_TITLE, 36), fill=(200, 200, 205, int(255 * q)))
            for k, ln in enumerate(("Yogi sitting in moolbandhasan, very", "tough practically impossible to get into")):
                d.text((110, y + 140 + k * 62), ln, font=font(fx.F_TITLE, 38), fill=(245, 245, 245, int(255 * q)))
        q2 = ease((t - 1.95) / 0.3)
        if q2 > 0: tag(d, "MULABANDHASANA", (W / 2, 560), 255 * q2, int(104 * (1 + 0.2 * max(0, 1 - (t - 1.95) / 0.25))))
        q3 = ease((t - 7.15) / 0.3)
        if q3 > 0: tag(d, "T. McEVILLEY, 1981: SAME POSE", (W / 2, 660), 255 * q3, 50, WHITE)
        return im
    fx.write_mp4(frame, 9.6, I + "comment.mp4")
if "buffalo" in todo:   # line 8 (38.95-44.98): "buffalo horns" ~41.7 -> stamp 2.6 s; names
    st = None
    def frame(t):
        cam = view((180, 60, 720, 560), 1.05, 1.15, t, 6.4); im = render(cam); d = ImageDraw.Draw(im)
        if t > 2.5:
            q = min(1, (t - 2.5) / 0.11); s = 2.0 - ease(q); fnt = font(fx.F_BIG, int(120 * s))
            ring(im, BOX["horns"], cam, ease((t - 2.5) / 0.3), pad=14); hc = scr(((BOX["horns"][0] + BOX["horns"][2]) / 2, BOX["horns"][1]), cam)
            c = (W / 2, 250)
            ay = 360 + 10 * math.sin(t * 8); d.polygon([(W / 2 - 34, ay), (W / 2 + 34, ay), (W / 2, ay + 46)], fill=GOLD + (255,))
            lay = Image.new("RGBA", (W, H)); ld = ImageDraw.Draw(lay)
            tw = ld.textlength("BUFFALO HORNS?", font=fnt); ld.rounded_rectangle((c[0] - tw / 2 - 30, c[1] - 90 * s, c[0] + tw / 2 + 30, c[1] + 90 * s), 24, fill=(15, 8, 6, 170), outline=(240, 50, 45, 255), width=12)
            ld.text(c, "BUFFALO HORNS?", font=fnt, fill=(240, 50, 45, 255), anchor="mm"); im.alpha_composite(lay.rotate(-6, center=c, resample=Image.BICUBIC))
            tag(d, "D. SRINIVASAN · G. POSSEHL", (W / 2, 1560), 255 * ease((t - 2.9) / 0.3), 46, WHITE)
        return im
    fx.write_mp4(frame, 6.7, I + "buffalo.mp4")
if "script" in todo:   # line 9 (45.62-48.37)
    def frame(t):
        cam = view((150, 30, 900, 520), 1.0, 1.15, t, 3.4); im = render(cam); d = ImageDraw.Draw(im); q = ease((t - 0.5) / 0.4)
        if q > 0: ring(im, BOX["script"], cam, q, pad=14)
        q2 = ease((t - 1.6) / 0.3)
        if q2 > 0:
            tag(d, "STILL UNREAD", (W / 2, 300), 255 * q2, 96)
            outlined(d, (W / 2, 1560), "YOUR GUESS? COMMENT", font(fx.F_BIG, int(70 * (1 + 0.05 * math.sin((t - 1.6) * 8)))), GOLD + (int(255 * q2),), stroke=4)
            ay = 1650 + 10 * math.sin((t - 1.6) * 8); d.polygon([(W / 2 - 32, ay), (W / 2 + 32, ay), (W / 2, ay + 40)], fill=GOLD + (int(255 * q2),))
        return im
    fx.write_mp4(frame, 3.6, I + "script.mp4")
if "marshall" in todo:   # line 3 (16.08-21.22): AI dig 0-2.2 then Marshall portrait card; PASHUPATI = LORD OF THE ANIMALS from 2.8
    dig = fx.cover(Image.open(I + "ai2.png").convert("RGB")); por = Image.open(I + "marshall.jpg").convert("L").convert("RGB")
    por = por.resize((380, int(por.height * 380 / por.width)), Image.LANCZOS)
    def frame(t):
        z = 1 + 0.08 * t / 5.4; im = dig.resize((int(W * z), int(H * z)), Image.LANCZOS); x0, y0 = (im.width - W) // 2, (im.height - H) // 2
        im = im.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA"); d = ImageDraw.Draw(im)
        outlined(d, (W / 2, 1830), "ARTIST'S IMPRESSION", font(fx.F_TITLE, 28), (230, 230, 230, 200), stroke=2)
        q = ease((t - 1.2) / 0.35)
        if q > 0:
            im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), 0.45 * q); d = ImageDraw.Draw(im)
            x, y = (W - por.width) // 2, int(300 + (1 - q) * 120); d.rectangle((x - 14, y - 14, x + por.width + 14, y + por.height + 14), fill=(235, 225, 205, int(255 * q)))
            p = por.copy().convert("RGBA"); p.putalpha(int(255 * q)); im.alpha_composite(p, (x, y))
            tag(d, "JOHN MARSHALL", (W / 2, y + por.height + 60), 255 * q, 60, WHITE)
            outlined(d, (W / 2, y + por.height + 112), "REAL PHOTO, 1906 · ARCHAEOLOGICAL SURVEY OF INDIA", font(fx.F_TITLE, 26), (220, 220, 220, int(255 * q)), stroke=2)
        q2 = ease((t - 2.85) / 0.3)
        if q2 > 0:
            tag(d, "PASHUPATI", (W / 2, 1060), 255 * q2, 112); tag(d, "= LORD OF THE ANIMALS", (W / 2, 1165), 255 * q2, 56, WHITE)
        return im
    fx.write_mp4(frame, 5.6, I + "marshall.mp4")
if "girl" in todo:   # line 10 (49.00-55.91): night lane, then the Dancing Girl as a dark backlit silhouette from "a girl" (3.72)
    lane = fx.cover(Image.open(I + "ai3.png").convert("RGB")); g = Image.open(I + "dancing_girl.jpg").convert("RGB")
    g = g.crop((int(g.width * 0.12), 0, int(g.width * 0.88), int(g.height * 0.82)))
    gs = g.resize((int(g.width * 1500 / g.height), 1500), Image.LANCZOS)
    lum = np.asarray(gs.convert("L")).astype(np.float32)
    m = (lum < 120).astype(np.uint8) * 255
    import cv2
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)); n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA])); m = np.where(lab == keep, 255, 0).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    inv = 255 - m; n2, lab2, st2, _ = cv2.connectedComponentsWithStats(inv)
    for k in range(1, n2):
        x, y, w_, h_, area = st2[k]
        if area < 4000 and x > 0 and y > 0 and x + w_ < m.shape[1] and y + h_ < m.shape[0]: m[lab2 == k] = 255   # fill specks only
    m = cv2.GaussianBlur(m, (5, 5), 0)
    body = Image.new("RGBA", gs.size, (10, 8, 6, 255)); body.putalpha(Image.fromarray(m))
    rim = Image.new("RGBA", gs.size, (255, 180, 90, 0)); rim.putalpha(Image.fromarray(m).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6)))
    sil = Image.new("RGBA", gs.size); sil.alpha_composite(rim); sil.alpha_composite(body)
    def frame(t):
        z = 1 + 0.22 * ease(t / 7.2); im = lane.resize((int(W * z), int(H * z)), Image.LANCZOS); x0, y0 = (im.width - W) // 2, int((im.height - H) * 0.7)
        im = im.crop((x0, y0, x0 + W, y0 + H)).convert("RGBA")
        em = Image.new("RGBA", (W, H)); ed = ImageDraw.Draw(em)
        for k in range(70):
            ph = (k * 0.37) % 1; x = (k * 157) % W + 40 * math.sin(t * 1.3 + k); y = H - ((t * (60 + k % 40) + ph * H) % H)
            r_ = 2 + k % 4; ed.ellipse((x - r_, y - r_, x + r_, y + r_), fill=(255, 170 + k % 60, 80, 150 + k % 90))
        im.alpha_composite(em.filter(ImageFilter.GaussianBlur(1.2)))
        q = ease((t - 3.6) / 0.5)
        if q > 0:
            im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), 0.6 * q)
            glow = Image.new("RGBA", (W, H)); ImageDraw.Draw(glow).ellipse((W / 2 - 420, 360, W / 2 + 420, 1560), fill=(255, 170, 70, int(120 * q)))
            im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
            s = sil.copy(); s.putalpha(s.getchannel("A").point(lambda v: int(v * q))); im.alpha_composite(s, ((W - s.width) // 2, 260))
        d = ImageDraw.Draw(im)
        outlined(d, (W / 2, 1830), "REAL: BRONZE, MOHENJO-DARO" if q > 0.5 else "ARTIST'S IMPRESSION", font(fx.F_TITLE, 28), (230, 230, 230, 200), stroke=2)
        return im
    fx.write_mp4(frame, 7.4, I + "girl.mp4")
if "ending" in todo:
    fx.ending(I + "ai3.png", I + "ending.mp4", [], ["SHE'S 4,000 YEARS OLD…", "AND STILL HAS ATTITUDE"], "INDUS FILES  #7  ·  COMMENT YOUR GUESS", q_at=0.15, dur=4.6)
