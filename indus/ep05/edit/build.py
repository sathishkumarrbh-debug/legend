"""Indus Files #5 assets (unicorn). Run from the episode folder: python3 build.py [names...]"""
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, fxkit as fx
from fxkit import W, H, ease, font, outlined, GOLD, WHITE
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
I = "images/"; todo = sys.argv[1:] or ["prep", "hook", "horn", "tiles", "kish", "split", "horns", "object", "ending"]
MET = I + "unicorn_met_1920.jpg"
HORN = [(1365, 957), (1370, 933), (1377, 911), (1388, 892), (1402, 874), (1420, 857), (1435, 844)]      # real horn on the modern impression
OBJ = (1335, 1015, 1450, 1225)                                                   # the "standard" in front of it
IMP = (900, 720, 1520, 1340)                                                     # the impression

def view(src, box, z_from, z_to, t, dur, out_size=(W, H)):
    """Crop around box centre with zoom (z=1 shows box height = frame height)."""
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2; z = z_from + (z_to - z_from) * ease(t / dur)
    ch = (box[3] - box[1]) / z; cw = ch * W / H
    return src.resize(out_size, Image.LANCZOS, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)), (cx, cy, cw, ch)

def to_screen(p, cam):
    cx, cy, cw, ch = cam; return ((p[0] - (cx - cw / 2)) * W / cw, (p[1] - (cy - ch / 2)) * H / ch)

def glow_line(im, pts, color, width, frac=1.0, dashed=False, alpha=255):
    lay = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(lay); p = fx._partial(pts, frac)
    if len(p) > 1:
        if dashed:
            for i in range(0, len(p) - 1):
                if i % 2 == 0: d.line((p[i], p[i + 1]), fill=color + (alpha,), width=width)
        else: d.line(p, fill=color + (alpha,), width=width, joint="curve")
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10))); im.alpha_composite(lay)

def smooth(pts, n=40):
    pts = np.array(pts, float); t = np.linspace(0, 1, len(pts)); u = np.linspace(0, 1, n)
    return list(zip(np.interp(u, t, pts[:, 0]), np.interp(u, t, pts[:, 1])))

def label(d, text, y, a=255, size=36): outlined(d, (W / 2, y), text, font(fx.F_TITLE, size), (235, 235, 235, a), stroke=2)

if "prep" in todo:   # 9:16 canvas of the Met photo for the hook (both seal + impression visible, impression larger)
    src = Image.open(MET).convert("RGB"); seals = src.crop((240, 470, 1580, 1400))
    bg = ImageEnhance.Brightness(fx.cover(src).filter(ImageFilter.GaussianBlur(30))).enhance(0.8)
    s2 = seals.resize((W, int(seals.height * W / seals.width)), Image.LANCZOS); bg.paste(s2, (0, int(H * 0.55 - s2.height / 2))); bg.save(I + "met_916.jpg", quality=95)
if "hook" in todo:
    fx.punch_hook(I + "met_916.jpg", I + "hook.mp4", focus=(0.66, 0.55), chips_from=(0.55, 0.45, 0.95, 0.65), steam=False, dur=4.0)
if "horn" in todo:   # line 1 "One horn. A unicorn." (2.5 s): push to the head, gold line traces the horn
    src = Image.open(MET).convert("RGB"); hp = smooth(HORN)
    def frame(t):
        im, cam = view(src, (1180, 760, 1560, 1180), 1.0, 1.25, t, 3.0); im = im.convert("RGBA")
        glow_line(im, [to_screen(p, cam) for p in hp], GOLD, 14, ease((t - 0.25) / 0.6))
        if t > 1.5: outlined(ImageDraw.Draw(im), (W / 2, 330), "ONE HORN", font(fx.F_BIG, 120), GOLD + (int(255 * ease((t - 1.5) / 0.25)),), stroke=6)
        return im
    fx.write_mp4(frame, 3.6, I + "horn.mp4")
if "tiles" in todo:   # line 2 "nearly seven of every ten seals" (2.7 s): 10 tiles flip in, 7 unicorns turn gold
    src = Image.open(MET).convert("RGB"); uni = src.crop(IMP).resize((250, 250), Image.LANCZOS)
    ele = Image.open(I + "elephant_seal.jpg").convert("RGB"); ele = ele.crop((int(ele.width * 0.5), 0, ele.width, ele.height))
    ele = fx.cover(ele, 250, 250); tig = fx.cover(Image.open(I + "tiger_seal_mold.jpg").convert("RGB").crop((420, 380, 1180, 1220)), 250, 250)
    order = [uni, uni, ele, uni, uni, tig, uni, uni, ele, uni]; is_u = [o is uni for o in order]
    bg = Image.blend(fx.cover(Image.open(I + "ai1.png").convert("RGB")).filter(ImageFilter.GaussianBlur(14)), Image.new("RGB", (W, H)), 0.6)
    def frame(t):
        im = bg.copy().convert("RGBA"); d = ImageDraw.Draw(im)
        for k, tile in enumerate(order):
            r, c = divmod(k, 3) if k < 9 else (3, 1); x = 115 + c * 290; y = 520 + r * 290
            q = ease((t - 0.08 * k) / 0.18)
            if q <= 0: continue
            w = max(2, int(250 * q)); tt = tile.resize((w, 250)).convert("RGBA")
            if is_u[k] and t > 1.3:
                g = ease((t - 1.3 - 0.05 * k) / 0.25); ov = Image.new("RGBA", tt.size, GOLD + (int(90 * g),)); tt.alpha_composite(ov)
                d.rounded_rectangle((x + 125 - w / 2 - 8, y - 8, x + 125 + w / 2 + 8, y + 258), 14, outline=GOLD + (int(255 * g),), width=8)
            im.alpha_composite(tt, (int(x + 125 - w / 2), y))
        if t > 1.5: outlined(d, (W / 2, 360), "7 OF EVERY 10", font(fx.F_BIG, 120), GOLD + (int(255 * ease((t - 1.5) / 0.25)),), stroke=6)
        return im
    fx.write_mp4(frame, 3.8, I + "tiles.mp4")
if "kish" in todo:   # line 3 callback to Part 2
    fx.zoom_rings(I + "kish_unicorn.jpg", I + "kish.mp4", (0, 0, 500, 500), (0, 80, 500, 480),
                  rings=[{"box": (55, 165, 365, 345), "t": 2.2, "color": "gold"}], top_text="FROM PART 2: FOUND IN IRAQ",
                  label="REAL: INDUS UNICORN SEAL FOUND AT KISH, IRAQ", push=(0.1, 1.5), dur=4.5)
if "split" in todo:   # line 4 (14.42-20.99): seal | real animal pairs, then unicorn | fog silhouette, "REAL... OR MYTH?"
    met = Image.open(MET).convert("RGB")
    pairs = [(0.0, fx.cover(Image.open(I + "elephant_seal.jpg").convert("RGB"), W, H // 2), fx.cover(Image.open(I + "live_elephant.jpg").convert("RGB"), W, H // 2), "ELEPHANT: REAL"),
             (1.0, fx.cover(Image.open(I + "tiger_seal_mold.jpg").convert("RGB").crop((300, 250, 1300, 1350)), W, H // 2), fx.cover(Image.open(I + "live_tiger.jpg").convert("RGB"), W, H // 2), "TIGER: REAL"),
             (3.4, fx.cover(met.crop((880, 700, 1540, 1360)), W, H // 2), fx.cover(Image.open(I + "ai5.png").convert("RGB"), W, H // 2), "UNICORN: ???")]
    def frame(t):
        k = max(i for i, p in enumerate(pairs) if t >= p[0]); t0, top, bot, lab = pairs[k]; u = t - t0
        z = 1 + 0.06 * u
        def zz(img):
            im = img.resize((int(W * z), int(H // 2 * z)), Image.LANCZOS); x0, y0 = (im.width - W) // 2, (im.height - H // 2) // 2
            return im.crop((x0, y0, x0 + W, y0 + H // 2))
        im = Image.new("RGBA", (W, H)); im.paste(zz(top), (0, 0)); bb = zz(bot)
        im.paste(bb, (0, H // 2)); d = ImageDraw.Draw(im); d.rectangle((0, H // 2 - 4, W, H // 2 + 4), fill=GOLD + (255,))
        a = int(255 * ease(u / 0.15)); outlined(d, (W / 2, H // 2 + 70), lab, font(fx.F_BIG, 70), (GOLD if k == 2 else WHITE) + (a,), stroke=4)
        if k == 2: label(d, "ARTIST'S IMPRESSION", H - 60, a, 30)
        if u < 0.12: im = Image.blend(im, Image.new("RGBA", (W, H), (255, 245, 225, 255)), 0.5 * (1 - u / 0.12))
        if t > 5.55:
            q = ease((t - 5.55) / 0.25); dd = ImageDraw.Draw(im)
            outlined(dd, (W / 2, H // 2 - 110), "REAL... OR MYTH?", font(fx.F_BIG, 130), WHITE + (int(255 * q),), stroke=7)
        return im
    fx.write_mp4(frame, 7.2, I + "split.mp4")
if "horns" in todo:   # lines 5-6 (21.63-27.88): "a bull, one horn hiding the other" -> dashed 2nd horn; "clay figures with one horn" -> real horn glows
    src = Image.open(MET).convert("RGB"); hp = smooth(HORN); hp2 = smooth([(x - 32, y + 6) for x, y in HORN])
    def frame(t):
        im, cam = view(src, (1180, 760, 1560, 1180), 1.15, 1.35, t, 6.5); im = im.convert("RGBA"); d = ImageDraw.Draw(im)
        a1 = 1 - ease((t - 3.2) / 0.3)
        if a1 > 0:
            glow_line(im, [to_screen(p, cam) for p in hp2], WHITE, 10, ease((t - 0.7) / 0.7), dashed=True, alpha=int(255 * a1))
            if t > 0.6: outlined(d, (W / 2, 330), "A BULL FROM THE SIDE?", font(fx.F_BIG, 96), WHITE + (int(255 * ease((t - 0.6) / 0.25) * a1),), stroke=5)
        if t > 3.35:
            g = ease((t - 3.35) / 0.3); pulse = 0.75 + 0.25 * math.sin((t - 3.35) * 6)
            glow_line(im, [to_screen(p, cam) for p in hp], GOLD, 16, 1.0, alpha=int(255 * g * pulse))
            outlined(d, (W / 2, 330), "OR TRULY ONE HORN?", font(fx.F_BIG, 96), GOLD + (int(255 * g),), stroke=5)
            outlined(d, (W / 2, 1580), "CLAY FIGURES: ONE HORN", font(fx.F_BIG, 64), GOLD + (int(255 * g),), stroke=4)
        return im
    fx.write_mp4(frame, 6.9, I + "horns.mp4")
if "object" in todo:   # line 7 (27.88-34.56): ring on the object; incense burner? 3.1; sacred filter? 4.36; no one knows 5.8
    src = Image.open(MET).convert("RGB"); bx = OBJ
    def frame(t):
        im, cam = view(src, (1180, 900, 1560, 1300), 1.0, 1.2, t, 7.0); im = im.convert("RGBA"); d = ImageDraw.Draw(im)
        a, b = to_screen(bx[:2], cam), to_screen(bx[2:], cam); q = ease((t - 1.2) / 0.5)
        if q > 0:
            lay = Image.new("RGBA", (W, H)); ImageDraw.Draw(lay).arc((a[0] - 40, a[1] - 40, b[0] + 40, b[1] + 40), -90, -90 + 360 * q, fill=GOLD + (255,), width=12)
            im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(8))); im.alpha_composite(lay)
        for k, (txt, tt) in enumerate((("INCENSE BURNER?", 3.1), ("SACRED FILTER?", 4.36))):
            p = ease((t - tt) / 0.2)
            if p <= 0: continue
            y = 330 + k * 150; s = 1 + 0.25 * max(0.0, 1 - (t - tt) / 0.22)
            outlined(d, (W / 2, y), txt, font(fx.F_BIG, int(92 * s)), GOLD + (int(255 * p),), stroke=5)
        p = ease((t - 5.8) / 0.3)
        if p > 0:
            outlined(d, (W / 2, 1520), "YOUR GUESS? COMMENT", font(fx.F_BIG, int(70 * (1 + 0.05 * math.sin((t - 5.8) * 8)))), GOLD + (int(255 * p),), stroke=4)
            ay = 1610 + 10 * math.sin((t - 5.8) * 8); d.polygon([(W / 2 - 32, ay), (W / 2 + 32, ay), (W / 2, ay + 40)], fill=GOLD + (int(255 * p),))
        return im
    fx.write_mp4(frame, 7.4, I + "object.mp4")
if "ending" in todo:
    fx.ending(I + "ai4.png", I + "ending.mp4", [], ["INDIA'S", "OLDEST GOD?"], "INDUS FILES  #6  ·  COMMENT YOUR GUESS", q_at=0.15, dur=4.6)
