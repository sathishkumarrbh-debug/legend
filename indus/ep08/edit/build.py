"""Indus Files #8 (weights) assets. Run from the episode folder."""
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, fxkit as fx
from fxkit import W, H, ease, font, outlined, GOLD2, CHALK
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
I = "images/"; todo = sys.argv[1:] or ["hook", "merchant", "polish", "scale", "double", "decimal", "map", "bahrain", "market", "twist", "city", "loop"]
BM = Image.open(I + "weights_bm.jpg").convert("RGB")
HOOK = (1000, 560, 760)          # hook crop on the BM photo (cx, cy, source height) -> also the loop's last frame
CUBE = BM.crop((790, 330, 1075, 640))   # one real banded cube (most common size class)
TINY = BM.crop((1415, 450, 1515, 560))
_blur = {}
def photo_cam(src, cx, cy, ch, z=1.0):
    ch = ch / z; cw = ch * W / H; x0, y0 = cx - cw / 2, cy - ch / 2
    if id(src) not in _blur: _blur[id(src)] = Image.blend(fx.cover(src).filter(ImageFilter.GaussianBlur(40)), Image.new("RGB", (W, H)), 0.6)
    out = _blur[id(src)].copy(); sx0, sy0, sx1, sy1 = max(0, x0), max(0, y0), min(src.width, x0 + cw), min(src.height, y0 + ch)
    part = src.crop((int(sx0), int(sy0), int(sx1), int(sy1))); s = H / ch
    part = part.resize((max(1, int(part.width * s)), max(1, int(part.height * s))), Image.LANCZOS)
    out.paste(part, (int((sx0 - x0) * s), int((sy0 - y0) * s))); return out.convert("RGBA"), (x0, y0, s)
def hookframe(t):   # bright tight crop, slowly moving; identical function used for the loop end
    im, _ = photo_cam(BM, HOOK[0] - 20 * t, HOOK[1], HOOK[2], 1.0 + 0.03 * t)
    return ImageEnhance.Brightness(im.convert("RGB")).enhance(1.25).convert("RGBA")
def ai(i): return np.asarray(fx.cover(Image.open(I + f"ai{i}.png").convert("RGB")))
def ai_tag(im): outlined(ImageDraw.Draw(im), (W / 2, 1830), "ARTIST'S IMPRESSION", font(fx.F_TITLE, 26), (230, 230, 230, 190), stroke=2); return im
def pa(im, text, y, t0, t, size=40, color=(245, 240, 230), x=None, anchor="mm"):
    if t > t0: fx.pill(im, text, (x if x is not None else W / 2 - 80, y), size, int(255 * min(1, (t - t0) / 0.15)), color=color, anchor=anchor)
def cube_img(scale):
    c = CUBE.resize((max(8, int(CUBE.width * scale)), max(8, int(CUBE.height * scale))), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle((2, 2, c.width - 3, c.height - 3), max(3, c.width // 14), fill=255)
    c.putalpha(m.filter(ImageFilter.GaussianBlur(1.5))); return c
def drop(im, c, xy, a=1.0):
    sh = Image.new("RGBA", c.size, (0, 0, 0, 0)); sh.putalpha(c.getchannel("A").point(lambda v: int(v * 0.5 * a)))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (int(xy[0] + 12), int(xy[1] + 16)))
    if a < 1: c = c.copy(); c.putalpha(c.getchannel("A").point(lambda v: int(v * a)))
    im.alpha_composite(c, (int(xy[0]), int(xy[1])))

if "hook" in todo:   # 0-5.33: tight bright crop moving; snap out 0.6; die pops 3.79 ("not dice" 3.97) and gets chalk-struck
    def frame(t):
        if t < 0.6: im = hookframe(t)
        else:
            u = ease((t - 0.6) / 0.3); im, _ = photo_cam(BM, HOOK[0] + (960 - HOOK[0]) * u, HOOK[1] + (640 - HOOK[1]) * u, HOOK[2] + (1250 - HOOK[2]) * u, 1.0 + 0.03 * max(0, t - 0.9))
        if t > 3.75:
            q = ease((t - 3.75) / 0.25); s = 260; die = Image.new("RGBA", (s, s)); d = ImageDraw.Draw(die)
            d.rounded_rectangle((4, 4, s - 4, s - 4), 34, fill=(248, 246, 240, 255), outline=(30, 30, 30, 255), width=5)
            for (x, y) in ((0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)): d.ellipse((x * s - 20, y * s - 20, x * s + 20, y * s + 20), fill=(25, 25, 25, 255))
            die = die.rotate(-12 + 20 * (1 - q), expand=True, resample=Image.BICUBIC); drop(im, die, (W / 2 - 80 - die.width / 2, 900 - die.height / 2 + (1 - q) * 300), q)
            if t > 4.0: fx.ink_stroke(im, [(W / 2 - 300, 1040), (W / 2 + 140, 740)], (t - 4.0) / 0.25, 22, color=(230, 60, 50), seed=2)
            pa(im, "NOT DICE", 1560, 4.1, t, 56, GOLD2)
        if 2.7 < t: pa(im, "INDUS FILES · CASE 08", 250, 2.7, t, 30, x=40, anchor="lm")
        return im
    fx.write_mp4(frame, 5.6, I + "c_hook.mp4")

if "merchant" in todo:   # 5.33-6.36 "their weights": AI merchant on the balance, snap
    src = ai(1)
    def frame(t):
        im = fx.parallax_warp(src, t, 1.3, 1, 24, 6, (1.05, 1.1), (0.4, 0.62), snap=0.05); fx.particles(im, t, "dust", 40, 3, (0, 200, W, 1500), 0.7)
        pa(im, "WEIGHTS", 330, 0.1, t, 70, GOLD2); return ai_tag(im)
    fx.write_mp4(frame, 1.3, I + "c_merchant.mp4")
if "polish" in todo:   # 6.36-10.11: polishing banded stone; pill sites at 1.6
    src = ai(2)
    def frame(t):
        im = fx.parallax_warp(src, t, 4.0, -1, 24, 6, (1.05, 1.12), (0.45, 0.55), snap=2.2); fx.particles(im, t, "dust", 70, 5, (200, 500, 1000, 1400), 1.0)
        pa(im, "BANDED STONE CUBES", 330, 0.3, t, 44); pa(im, "HARAPPA · MOHENJO-DARO", 420, 1.6, t, 36, GOLD2); return ai_tag(im)
    fx.write_mp4(frame, 4.0, I + "c_polish.mp4")

def bg_blur(src_img, dim=0.55):
    return Image.blend(fx.cover(src_img).filter(ImageFilter.GaussianBlur(26)), Image.new("RGB", (W, H)), dim).convert("RGBA")
if "scale" in todo:   # 10.11-14.67: tiny cube on a scale readout 0.86 g (1.0), big cube 13.7 g (2.83)
    bg = bg_blur(BM)
    def readout(im, val, y, a):
        d = ImageDraw.Draw(im); d.rounded_rectangle((W / 2 - 330, y - 70, W / 2 + 170, y + 70), 18, fill=(12, 18, 14, int(230 * a)), outline=(70, 90, 70, int(255 * a)), width=4)
        d.text((W / 2 - 80, y), val, font=font(fx.F_BIG, 110), fill=(120, 255, 160, int(255 * a)), anchor="mm")
    def frame(t):
        z = 1 + 0.04 * t / 4.6; im = bg.copy(); d = ImageDraw.Draw(im)
        d.rounded_rectangle((W / 2 - 400, 1180, W / 2 + 240, 1230), 12, fill=(60, 60, 64, 255)); d.rectangle((W / 2 - 110, 1230, W / 2 - 50, 1330), fill=(45, 45, 48, 255))
        if t < 2.75:
            q = ease((t - 0.3) / 0.3); c = TINY.resize((120, 132)).convert("RGBA")
            if q > 0: drop(im, c, (W / 2 - 140, 1180 - 132 - (1 - q) * 260), q)
            n = 0.86 * ease(min(1, max(0, (t - 0.6) / 0.6)))
            readout(im, f"{n:.2f} g", 820, 1.0); pa(im, "LESS THAN A GRAM", 980, 1.1, t, 44, GOLD2)
        else:
            q = ease((t - 2.75) / 0.25); c = cube_img(1.15); drop(im, c, (W / 2 - 80 - c.width / 2, 1180 - c.height - (1 - q) * 300), q)
            n = 13.7 * ease(min(1, max(0, (t - 2.9) / 0.5))); readout(im, f"{n:.1f} g", 620, 1.0); pa(im, "THE MOST COMMON", 780, 3.0, t, 44, GOLD2)
        pa(im, "REAL WEIGHTS: SMALLEST ≈ 0.86 g · COMMON ≈ 13.7 g", 1580, 0.2, t, 30)
        return im
    fx.write_mp4(frame, 4.8, I + "c_scale.mp4")

if "double" in todo:   # 14.67-23.12: numbers at 3.17 3.82 4.50 5.14 5.66 6.57 7.33 (1..64); cube side ~ ratio^(1/3)
    bg = bg_blur(Image.open(I + "ai1.png").convert("RGB"), 0.62); nums = [1, 2, 4, 8, 16, 32, 64]; ts = [3.17, 3.82, 4.50, 5.14, 5.66, 6.57, 7.33]
    base = 0.32
    def frame(t):
        im = bg.copy(); fx.particles(im, t, "dust", 40, 8, (0, 0, W, H), 0.6); d = ImageDraw.Draw(im)
        pa(im, "EACH ONE DOUBLES", 330, 1.25, t, 64, GOLD2)
        shown = [k for k in range(7) if t >= ts[k] - 0.05]
        if t < ts[0] - 0.05:   # waiting cube 1 + "?" so the trick line is never empty
            q = ease((t - 0.25) / 0.3); c = cube_img(base * 2.2); x0 = W / 2 - 80 - c.width / 2; y0 = 1150 - c.height
            if q > 0: drop(im, c, (x0, y0 + (1 - q) * 200), q)
            if t > 1.0: fx.ink_stroke(im, fx.ink_ellipse(x0 + c.width / 2, y0 + c.height / 2, c.width * 0.75, c.height * 0.72), (t - 1.0) / 0.5, 12, seed=4)
            p = 1 + 0.08 * math.sin(t * 6); outlined(d, (W / 2 - 80, 1250), "?", font(fx.F_BIG, int(110 * p)), GOLD2 + (int(255 * q),), stroke=5)
            return fx._place(im, 1 + 0.06 * t / 3.2, W / 2, H * 0.55).convert("RGBA")
        # layout: row along a baseline, camera slides left as cubes grow
        sizes = [base * (n ** (1 / 3)) for n in nums]; xs = []; x = 60
        for s in sizes: xs.append(x); x += CUBE.width * s + 34
        k_last = shown[-1] if shown else 0; right = xs[k_last] + CUBE.width * sizes[k_last]
        shift = max(0, right - (W - 140)) * ease(min(1, (t - (ts[k_last] if shown else 0)) / 0.3)) if shown else 0
        prev_shift = 0
        if len(shown) > 1: pk = shown[-2]; prev_shift = max(0, xs[pk] + CUBE.width * sizes[pk] - (W - 140))
        shift = prev_shift + (max(0, right - (W - 140)) - prev_shift) * (ease(min(1, (t - ts[k_last]) / 0.3)) if shown else 0)
        for k in shown:
            q = ease((t - ts[k]) / 0.18); c = cube_img(sizes[k] * (1.25 - 0.25 * q)); bx = xs[k] - shift; by = 1250 - c.height
            drop(im, c, (bx, by), q)
            outlined(d, (bx + c.width / 2, 1300 + 0 * k), str(nums[k]), font(fx.F_BIG, 70 if k < 6 else 86), (GOLD2 if k == len(shown) - 1 else (255, 255, 255)) + (int(255 * q),), stroke=4)
            if k > 0 and q > 0.5: outlined(d, (bx - 17, 1190), "×2", font(fx.F_BIG, 34), (230, 230, 230, int(255 * q)), stroke=3)
        return im
    fx.write_mp4(frame, 8.7, I + "c_double.mp4")

if "decimal" in todo:   # 23.12-27.74: true-scale cubes (side ~ weight^(1/3)): 64 -> ×10 = 160 (1.3) -> ×100 = 1,600 (2.0)
    bg = bg_blur(BM, 0.5); k = 0.15
    def frame(t):
        im = bg.copy(); d = ImageDraw.Draw(im); base_y = 1130
        c64 = cube_img(k * 64 ** (1 / 3)); a64 = 1 - ease((t - 1.1) / 0.3)
        if a64 > 0:
            x = W / 2 - 80 - c64.width / 2 - 200 * ease(min(1, t / 1.1)); drop(im, c64, (x, base_y - c64.height), a64)
            outlined(d, (x + c64.width / 2, base_y - c64.height - 45), "64", font(fx.F_BIG, 64), (255, 255, 255, int(255 * a64)), stroke=4)
        for j, (lab, tt, n, cx) in enumerate((("16 × 10 = 160", 1.3, 160, 240), ("16 × 100 = 1,600", 2.0, 1600, 650))):
            if t > tt:
                q = min(1, (t - tt) / 0.12); c = cube_img(k * n ** (1 / 3) * (1.15 - 0.15 * ease(q)))
                x = cx - c.width / 2; drop(im, c, (x, base_y - c.height))
                outlined(d, (cx, base_y - c.height - 50), lab, font(fx.F_BIG, 50 if j == 0 else 60), GOLD2 + (255,), stroke=4)
        pa(im, "THEN TENS AND HUNDREDS", 330, 0.2, t, 54, GOLD2); pa(im, "SEEN: BINARY, THEN DECIMAL", 1560, 2.77, t, 40)
        pa(im, "TRUE SCALE", 1640, 2.2, t, 28)
        return fx._place(im, 1 + 0.05 * t / 4.9, W / 2, H / 2).convert("RGBA")
    fx.write_mp4(frame, 4.9, I + "c_decimal.mp4")

CITIES = {"HARAPPA": (72.86, 30.63), "MOHENJO-DARO": (68.14, 27.33), "DHOLAVIRA": (70.21, 23.89), "LOTHAL": (72.25, 22.52)}
if "map" in todo:   # 27.74-31.15: four cities pop with the same cube icon
    P = fx.Proj(64.5, 79.0, 21.5, 31.5, top=470, bottom=1130); bgm = fx.base_map(P); icon = cube_img(0.22); tt = [0.25, 0.65, 1.05, 1.45]
    def frame(t):
        im = bgm.copy().convert("RGBA"); d = ImageDraw.Draw(im)
        for k, (n, ll) in enumerate(CITIES.items()):
            q = ease((t - tt[k]) / 0.2)
            if q <= 0: continue
            c = P(*ll); ic = icon.resize((max(2, int(icon.width * q)), max(2, int(icon.height * q))))
            drop(im, ic, (c[0] - ic.width / 2, c[1] - ic.height / 2)); fx.map_label(d, (c[0] + 42, c[1] + 4) if n == "LOTHAL" else (c[0], c[1] + 60), n, 32, anchor="lm" if n == "LOTHAL" else "mm", alpha=q)
        pa(im, "SAME SET · 1,000 KM APART", 330, 0.1, t, 46, GOLD2)
        z = 1 + 0.12 * ease(min(1, t / 2.0)) + 0.02 * t; return fx._place(im, z, W / 2, H / 2).convert("RGBA")
    fx.write_mp4(frame, 3.6, I + "c_map.mp4")

if "bahrain" in todo:   # 31.15-36.47: arc map 0-1.1, AI harbour 1.1-2.9, REAL mounds 2.9-5.32
    P = fx.Proj(46.0, 76.0, 18.0, 33.0, top=520, bottom=1450); bgm = fx.base_map(P); src = ai(3); mounds = Image.open(I + "mounds.jpg").convert("RGB")
    A = P(68.5, 26.5); B = P(50.55, 26.07)
    arc = [(A[0] + (B[0] - A[0]) * u, A[1] + (B[1] - A[1]) * u - 220 * math.sin(math.pi * u)) for u in np.linspace(0, 1, 60)]
    def frame(t):
        if t < 1.5:
            im = bgm.copy().convert("RGBA"); d = ImageDraw.Draw(im); p = fx._partial(arc, ease(t / 0.7))
            if len(p) > 1:
                for i in range(0, len(p) - 1, 2): d.line((p[i], p[i + 1]), fill=(255, 255, 255, 255), width=9)
            fx.map_label(d, (A[0], A[1] + 60), "INDUS", 44, GOLD2, "mm")
            fx.map_label(d, (B[0] + 40, B[1] + 70), "BAHRAIN (DILMUN)", 40, anchor="lm", alpha=ease(t / 0.25))
            if t > 0.7: fx._pin(d, B, t)
            return fx._place(im, 1 + 0.08 * t, W / 2, H / 2).convert("RGBA")
        if t < 2.9:
            im = fx.parallax_warp(src, t - 1.5, 1.8, 1, 24, 6, (1.05, 1.1)); fx.particles(im, t, "dust", 30, 9, (0, 300, W, 1500), 0.5); return ai_tag(im)
        im, _ = photo_cam(mounds, 980 + 120 * ease((t - 2.9) / 2.4), 700, 1400, 1.0 + 0.05 * (t - 2.9))
        pa(im, "REAL: DILMUN BURIAL MOUNDS, BAHRAIN (1918)", 1600, 2.95, t, 30); pa(im, "WEIGHTS THAT MATCH", 330, 3.2, t, 56, GOLD2)
        return im
    fx.write_mp4(frame, 5.6, I + "c_bahrain.mp4")

if "market" in todo:   # 36.47-42.76: AI market, callback pills
    src = ai(4)
    def frame(t):
        im = fx.parallax_warp(src, t, 6.5, -1, 26, 6, (1.04, 1.12), (0.5, 0.5), snap=2.75); fx.particles(im, t, "dust", 50, 10, (0, 200, W, 1600), 0.6)
        pa(im, "NO KING (PART 4)", 300, 0.05, t, 38); pa(im, "UNREAD WRITING (PART 3)", 390, 1.3, t, 38); pa(im, "SAME WEIGHTS EVERYWHERE", 500, 2.75, t, 46, GOLD2)
        return ai_tag(im)
    fx.write_mp4(frame, 6.6, I + "c_market.mp4")

if "twist" in todo:   # 42.76-45.73: night stall; flickering lamp; at 1.78 ("We don't know") THEORY card + comment
    src = ai(5)
    def frame(t):
        im = fx.parallax_warp(src, t, 3.2, 1, 18, 5, (1.08, 1.16), (0.45, 0.6))
        fl = 0.92 + 0.08 * math.sin(t * 23) * math.sin(t * 7.3); im = ImageEnhance.Brightness(im.convert("RGB")).enhance(fl).convert("RGBA")
        fx.particles(im, t, "embers", 20, 11, (300, 600, 700, 1100), 0.5)
        if t > 1.78:
            pa(im, "THEORY?", 330, 1.78, t, 70, (225, 60, 50)); pa(im, "INSPECTORS? GUILDS? TEMPLES?", 440, 1.95, t, 42)
            pa(im, "YOUR GUESS? COMMENT ↓", 1560, 2.2, t, 46, GOLD2)
        return ai_tag(im)
    fx.write_mp4(frame, 3.2, I + "c_twist.mp4")

if "city" in todo:   # 45.73-52.50: AI drain street (water shimmer) 0-3.35, REAL Mohenjo-daro street 3.35-4.7, REAL Lothal drain 4.7-6.77
    src = ai(6); st = Image.open(I + "mjd_street.jpg").convert("RGB"); dr = Image.open(I + "lothal_drain.jpg").convert("RGB")
    def frame(t):
        if t < 3.35:
            im = fx.parallax_warp(src, t, 3.35, 1, 26, 6, (1.04, 1.12), (0.55, 0.6)); im = fx.heat_haze(im, t, (700, 1050, 1080, 1700), 2.2).convert("RGBA")
            pa(im, "ORDER, BUILT INTO THE CITY", 330, 0.3, t, 44); return ai_tag(im)
        if t < 4.7:
            im, _ = photo_cam(st, 960, 1400, 2400, fx.snapz(t - 3.35, 0.0, (1.0, 1.03), 1.4, 0.12)); pa(im, "REAL: MOHENJO-DARO STREET", 1600, 3.4, t, 32); return im
        im, _ = photo_cam(dr, 800 + 60 * (t - 4.7), 640, 1150, fx.snapz(t - 4.7, 0.0, (1.0, 1.04), 2.1, 0.12))
        pa(im, "REAL: HARAPPAN DRAIN, LOTHAL", 1600, 4.75, t, 32); pa(im, "PART 9: TOILETS 4,500 YEARS AGO?", 330, 5.0, t, 40, GOLD2)
        return im
    fx.write_mp4(frame, 7.0, I + "c_city.mp4")

if "loop" in todo:   # 52.50-end (~56.2): AI cube close (0-1.4) then glide into the exact hook framing; last frame == hook frame 0
    src = ai(1); END = 3.45
    def frame(t):
        if t < 1.4:
            im = fx.parallax_warp(src, t, 1.4, -1, 18, 5, (1.15, 1.28), (0.35, 0.62), snap=0.05); pa(im, "WHO CHECKED THEM? COMMENT ↓", 330, 0.1, t, 40, GOLD2); return ai_tag(im)
        u = ease((t - 1.4) / (END - 1.4 - 0.25)); a = min(1, (t - 1.4) / 0.25)
        im, _ = photo_cam(BM, 960 + (HOOK[0] - 960) * u, 640 + (HOOK[1] - 640) * u, 1250 + (HOOK[2] - 1250) * u, 1.0)
        im = Image.blend(im.convert("RGB"), hookframe(0).convert("RGB"), ease((t - (END - 0.6)) / 0.6)).convert("RGBA") if t > END - 0.6 else im
        return im
    fx.write_mp4(frame, END + 0.2, I + "c_loop.mp4")
