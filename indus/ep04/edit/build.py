"""Indus Files #4 assets. Run from the episode folder."""
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, fxkit as fx
from fxkit import W, H, ease, font, outlined, GOLD, WHITE, RED
from PIL import Image, ImageDraw, ImageFilter
I = "images/"
todo = sys.argv[1:] or ["hook", "who", "map", "nos", "bricks", "ratio", "options"]

def stamp_layer(text, color=(240, 50, 45), size=150):
    fnt = font(fx.F_BIG, size); tw = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(text, font=fnt)) + 100
    st = Image.new("RGBA", (tw, size + 110)); sd = ImageDraw.Draw(st)
    sd.rounded_rectangle((8, 8, st.width - 8, st.height - 8), 26, fill=(15, 8, 6, 170), outline=color + (255,), width=14)
    sd.text((st.width / 2, st.height / 2 + 4), text, font=fnt, fill=color + (255,), anchor="mm")
    grit = Image.effect_noise(st.size, 70).point(lambda v: 255 if v > 75 else 0)
    st.putalpha(Image.composite(st.getchannel("A"), Image.new("L", st.size, 0), grit))
    return st.rotate(-8, expand=True, resample=Image.BICUBIC)

def multi_stamp(bg_img, out, items, dur, dim=0.5, top=None, zoom=0.06, size=150):
    """items: (text, t_stamp, strike_t or None, y_frac). Each slams in with a shake; optional white strike-out."""
    bg = fx.cover(Image.open(bg_img).convert("RGB")); layers = [stamp_layer(t, size=size) for t, *_ in items]
    def frame(t):
        z = 1 + zoom * t / dur; im = bg.resize((int(W * z), int(H * z)), Image.LANCZOS)
        x0, y0 = (im.width - W) // 2, (im.height - H) // 2; dx = dy = 0
        for _, ts, *_r in items:
            if 0 <= t - ts < 0.3: a = 20 * (1 - (t - ts) / 0.3); dx += int(a * math.sin(t * 90)); dy += int(a * math.cos(t * 70))
        im = im.crop((x0 + dx, y0 + dy, x0 + dx + W, y0 + dy + H))
        im = Image.blend(im, Image.new("RGB", (W, H)), dim).convert("RGBA")
        if top: outlined(ImageDraw.Draw(im), (W / 2, 330), top, font(fx.F_TITLE, 54), WHITE + (int(255 * ease(t / 0.3)),), stroke=3)
        for L, (text, ts, strike, yf) in zip(layers, items):
            if t < ts: continue
            q = min(1, (t - ts) / 0.11); sc = 2.0 - 1.0 * ease(q); s2 = L.resize((int(L.width * sc), int(L.height * sc)), Image.BICUBIC)
            cx, cy = W // 2, int(H * yf); im.alpha_composite(s2, (cx - s2.width // 2, cy - s2.height // 2))
            if strike is not None and t > strike:
                p = ease((t - strike) / 0.25); d = ImageDraw.Draw(im); hw = L.width * 0.55
                d.line((cx - hw, cy + 40, cx - hw + 2 * hw * p, cy + 40 - 80 * p), fill=(255, 255, 255, 255), width=20)
        return im
    fx.write_mp4(frame, dur, out)

if "hook" in todo:
    fx.punch_hook(I + "priest_king_lic.jpg", I + "hook.mp4", focus=(0.5, 0.42), chips_from=(0.32, 0.5, 0.72, 0.68), steam=False, dur=3.6)
if "who" in todo:   # line 2: "Nothing says he was a priest... or a king."  (line starts 4.79; priest ~5.9, king ~7.1)
    multi_stamp(I + "priest_king_lic.jpg", I + "who.mp4", [("PRIEST?", 1.0, 1.55, 0.60), ("KING?", 2.2, 2.6, 0.75)], dur=4.0, dim=0.35)

# map: approximate extents (hand-drawn from site distributions; labelled APPROXIMATE)
INDUS = [(61.6, 25.4), (64.5, 29.5), (66.8, 31.6), (69.5, 34.0), (72.6, 34.0), (74.8, 32.6), (76.6, 31.3), (78.2, 29.9), (77.9, 28.4),
         (76.3, 27.0), (74.6, 25.0), (74.0, 22.6), (73.0, 20.9), (71.2, 20.7), (69.0, 21.9), (68.3, 23.1), (66.6, 24.6), (63.8, 25.1)]
MESO = [(38.3, 36.9), (40.8, 37.3), (43.6, 37.2), (45.4, 35.3), (46.6, 33.6), (48.1, 31.2), (48.2, 29.9), (46.9, 30.3), (45.2, 31.5),
        (43.8, 32.4), (42.4, 33.6), (40.6, 34.5), (38.9, 35.6)]
nile = [(31.0, 30.1), (31.1, 29.4), (30.9, 28.4), (30.8, 27.6), (31.3, 27.1), (32.2, 26.2), (32.6, 25.9), (32.8, 25.3), (32.9, 24.1)]
EGYPT = [(29.9, 31.3), (31.0, 31.6), (32.3, 31.3), (31.3, 30.0)] + [(x + 0.35, y) for x, y in nile] + [(x - 0.35, y) for x, y in reversed(nile)]
if "map" in todo:
    B = (22.0, 84.0, 12.0, 42.0); P = fx.Proj(*B, top=420, bottom=1560); bg = fx.base_map(P)
    def frame(t):
        im = bg.copy().convert("RGBA"); ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
        a1 = ease((t - 0.05) / 0.35)
        for poly, name, xy in ((EGYPT, "EGYPT", (31.5, 21.3)), (MESO, "MESOPOTAMIA", (41.5, 39.6))):
            d.polygon([P(*p) for p in poly], fill=(235, 235, 235, int(120 * a1)), outline=(255, 255, 255, int(255 * a1)))
            fx.map_label(d, P(*xy), name, 38, alpha=a1, anchor="mm")
        a2 = ease((t - 0.9) / 0.5)
        if a2 > 0:
            g = Image.new("RGBA", (W, H)); ImageDraw.Draw(g).polygon([P(*p) for p in INDUS], fill=GOLD + (int(150 * a2),)); ov.alpha_composite(g.filter(ImageFilter.GaussianBlur(10)))
            d.polygon([P(*p) for p in INDUS], fill=GOLD + (int(120 * a2),), outline=GOLD + (int(255 * a2),))
            fx.map_label(d, P(70.0, 18.6), "INDUS", 56, GOLD, "mm", a2)
        a3 = ease((t - 1.8) / 0.4)
        if a3 > 0: fx.map_label(d, (W / 2, 330), "MORE LAND THAN BOTH COMBINED", 44, anchor="mm", alpha=a3)
        fx.map_label(d, (W / 2, 1600), "APPROXIMATE EXTENT, c. 2500 BC", 30, (200, 200, 200), "mm")
        im.alpha_composite(ov)
        z = 1 + 0.05 * t / 4.5; im = im.resize((int(W * z), int(H * z)), Image.LANCZOS); x0, y0 = (im.width - W) // 2, (im.height - H) // 2
        return im.crop((x0, y0, x0 + W, y0 + H))
    fx.write_mp4(frame, 4.5, I + "map.mp4")
if "nos" in todo:   # line 7 starts 20.81: palace ~21.9, tomb 22.78, conqueror 24.10, battle 26.02
    multi_stamp(I + "ai2.png", I + "nos.mp4", [("NO PALACE", 1.05, None, 0.24), ("NO ROYAL TOMB", 1.97, None, 0.38),
                                               ("NO CONQUEROR", 3.29, None, 0.52), ("NO BATTLES", 5.21, None, 0.66)], dur=7.6, dim=0.45, size=120)
if "bricks" in todo:   # line 9 starts 30.53: same brick at cities hundreds of km apart (2.3 s)
    B = (65.5, 79.0, 20.5, 33.0); P = fx.Proj(*B, top=420, bottom=1550); bg = fx.base_map(P)
    cities = {"HARAPPA": (72.86, 30.63), "MOHENJO-DARO": (68.14, 27.33), "RAKHIGARHI": (76.11, 29.29),
              "DHOLAVIRA": (70.21, 23.89), "LOTHAL": (72.25, 22.52)}
    def brick_icon(s):
        b = Image.new("RGBA", (int(s * 2.4), int(s * 1.5))); d = ImageDraw.Draw(b); w, h, dp = s * 1.9, s * 0.5, s * 0.45
        d.polygon([(0, dp), (w, dp), (w, dp + h), (0, dp + h)], fill=(176, 92, 52, 255), outline=(60, 25, 10, 255))
        d.polygon([(0, dp), (dp, 0), (w + dp, 0), (w, dp)], fill=(205, 120, 72, 255), outline=(60, 25, 10, 255))
        d.polygon([(w, dp), (w + dp, 0), (w + dp, h), (w, dp + h)], fill=(140, 70, 38, 255), outline=(60, 25, 10, 255)); return b
    ic = brick_icon(34)
    def frame(t):
        im = bg.copy().convert("RGBA"); d = ImageDraw.Draw(im)
        for k, (n, xy) in enumerate(cities.items()):
            q = ease((t - 0.1 - 0.22 * k) / 0.2)
            if q <= 0: continue
            c = P(*xy); s = ic.resize((max(2, int(ic.width * q)), max(2, int(ic.height * q))))
            im.alpha_composite(s, (int(c[0] - s.width / 2), int(c[1] - s.height / 2)))
            fx.map_label(d, (c[0], c[1] + 52), n, 30, anchor="mm", alpha=q)
        fx.map_label(d, (W / 2, 330), "HUNDREDS OF KM APART", 46, anchor="mm", alpha=ease(t / 0.3))
        return im
    fx.write_mp4(frame, 3.0, I + "map_bricks.mp4")
if "ratio" in todo:   # line 9 "the bricks were made the same shape. One, two, four." starts 32.80; 1 @34.58, 2 @35.21, 4 @35.89
    src = Image.open(I + "harappan_brick_ROM.jpg").convert("RGB")
    bg = Image.blend(fx.cover(src).filter(ImageFilter.GaussianBlur(18)), Image.new("RGB", (W, H)), 0.6)
    ph = src.copy(); ph.thumbnail((900, 640)); 
    def frame(t):
        im = bg.copy().convert("RGBA"); d = ImageDraw.Draw(im)
        a = ease(t / 0.3); p2 = ph.copy(); p2.putalpha(int(255 * a)); im.alpha_composite(p2, (W // 2 - ph.width // 2, 380))
        outlined(d, (W / 2, 330), "REAL: HARAPPAN BRICK (ROYAL ONTARIO MUSEUM)", font(fx.F_TITLE, 32), (235, 235, 235, int(255 * a)), stroke=2)
        # code brick, proportions 1 : 2 : 4 (height : width : length)
        u = 62; L, Wd, Hh = 4 * u, 2 * u, 1 * u; ox, oy = 250, 1590; k = 0.55
        top = [(ox, oy), (ox + L, oy), (ox + L + Wd * k, oy - Wd * k), (ox + Wd * k, oy - Wd * k)]
        front = [(ox, oy), (ox + L, oy), (ox + L, oy + Hh), (ox, oy + Hh)]
        side = [(ox + L, oy), (ox + L + Wd * k, oy - Wd * k), (ox + L + Wd * k, oy - Wd * k + Hh), (ox + L, oy + Hh)]
        b = ease((t - 0.5) / 0.4)
        if b > 0:
            for poly, col in ((front, (176, 92, 52)), (top, (205, 120, 72)), (side, (140, 70, 38))):
                d.polygon(poly, fill=col + (int(255 * b),), outline=(40, 18, 6, int(255 * b)))
        f = font(fx.F_BIG, 96)
        for txt, tt, pos in (("1", 1.78, (ox - 50, oy + Hh / 2)), ("2", 2.41, (ox + L + Wd * k / 2 + 50, oy - Wd * k / 2 - 30)), ("4", 3.09, (ox + L / 2, oy + Hh + 70))):
            q = ease((t - tt) / 0.18)
            if q > 0:
                s = int(96 * (1.6 - 0.6 * q)); outlined(d, pos, txt, font(fx.F_BIG, s), GOLD + (int(255 * q),), stroke=5)
        if t > 3.5: outlined(d, (W / 2, 1840), "THE SAME RATIO EVERYWHERE", font(fx.F_TITLE, 46), WHITE + (int(255 * ease((t - 3.5) / 0.3)),), stroke=3)
        return im
    fx.write_mp4(frame, 5.0, I + "ratio.mp4")
if "options" in todo:   # line 10 starts 36.75: merchants 38.25, priests 39.33, council 40.15, argue 41.28
    bg = fx.cover(Image.open(I + "ai3.png").convert("RGB"))
    opts = [("RICH MERCHANTS?", 1.5), ("PRIESTS?", 2.58), ("A COUNCIL?", 3.4)]
    def frame(t):
        z = 1 + 0.08 * t / 6.5; im = bg.resize((int(W * z), int(H * z)), Image.LANCZOS); x0, y0 = (im.width - W) // 2, (im.height - H) // 2
        im = Image.blend(im.crop((x0, y0, x0 + W, y0 + H)), Image.new("RGB", (W, H)), 0.5).convert("RGBA"); d = ImageDraw.Draw(im)
        outlined(d, (W / 2, 360), "WHO GAVE THE ORDERS?", font(fx.F_BIG, 92), WHITE + (int(255 * ease(t / 0.3)),), stroke=5)
        for k, (txt, tt) in enumerate(opts):
            q = ease((t - tt) / 0.2)
            if q <= 0: continue
            y = 640 + k * 190; bw = 760; x = W / 2 - bw / 2 + (1 - q) * 300
            d.rounded_rectangle((x, y - 70, x + bw, y + 70), 36, fill=(20, 16, 12, int(215 * q)), outline=GOLD + (int(255 * q),), width=6)
            outlined(d, (x + bw / 2, y), txt, font(fx.F_BIG, 84), GOLD + (int(255 * q),), stroke=3)
        q = ease((t - 4.53) / 0.3)
        if q > 0:
            outlined(d, (W / 2, 1290), "ARCHAEOLOGISTS STILL ARGUE", font(fx.F_TITLE, 46), WHITE + (int(255 * q),), stroke=3)
            pulse = 1 + 0.06 * math.sin((t - 4.53) * 8)
            fb = font(fx.F_BIG, int(70 * pulse)); outlined(d, (W / 2, 1420), "YOUR GUESS? COMMENT", fb, GOLD + (int(255 * q),), stroke=4)
            ax, ay = W / 2, 1510 + 12 * math.sin((t - 4.53) * 8)
            d.polygon([(ax - 34, ay), (ax + 34, ay), (ax, ay + 44)], fill=GOLD + (int(255 * q),), outline=(0, 0, 0, int(255 * q)))
        return im
    fx.write_mp4(frame, 7.0, I + "options.mp4")
if "ending" in todo:
    fx.ending(I + "ai2.png", I + "ending.mp4", ["7 OF EVERY", "10 SEALS"], ["WHAT IS THIS", "CREATURE?"], "INDUS FILES  #5  ·  COMMENT YOUR GUESS", q_at=1.0, dur=4.6)
if "unicorn" in todo:   # line 12 starts 47.36: "seven of every ten seals" ~49.5
    fx.zoom_rings(I + "unicorn_met.jpg", I + "unicorn.mp4", (0, 200, 1280, 1080), (590, 470, 1030, 900),
                  rings=[{"box": (640, 560, 960, 840), "t": 2.2, "color": "gold"}],
                  top_text="ON NEARLY 7 OF EVERY 10 SEALS", label="REAL: INDUS SEAL + MODERN IMPRESSION · MET MUSEUM", push=(0.2, 1.6), dur=8.5)
