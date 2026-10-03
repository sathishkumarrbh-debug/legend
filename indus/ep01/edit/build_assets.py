"""Custom assets for Indus Files #1: animated maps, +2,000 years timeline, brick dust overlay, synthesized story SFX.
Run from the episode folder: python3 build_assets.py"""
import json, math, os, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SR = 1080, 1920, 30, 44100
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(HERE, "images")
SFX = os.path.join(ROOT, "sfx")
os.makedirs(IMG, exist_ok=True); os.makedirs(SFX, exist_ok=True)
F_TITLE = os.path.join(ROOT, "fonts", "Cinzel-Bold.ttf")
F_BIG = os.path.join(ROOT, "fonts", "Anton.ttf")
GOLD, RED, WHITE = (255, 197, 61), (230, 50, 40), (245, 240, 230)
SEA, LAND, LAND_EDGE, RIVER = (12, 22, 32), (58, 46, 32), (120, 96, 60), (70, 140, 190)


def font(p, s): return ImageFont.truetype(p, s)
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def write_mp4(frames_fn, n, path):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", path],
                         stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frames_fn(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("wrote", path)


# ------------------------------------------------------------------ maps
GEO = os.path.join(ROOT, "geo")
LAND_POLYS = [f["geometry"] for f in json.load(open(os.path.join(GEO, "ne_50m_land.geojson")))["features"]]
RIVERS = [f for f in json.load(open(os.path.join(GEO, "ne_50m_rivers_lake_centerlines.geojson")))["features"]
          if (f["properties"].get("name") or "") in ("Indus", "Ravi", "Sutlej", "Chenab", "Jhelum", "Tigris", "Euphrates", "Karun")]


class Proj:
    def __init__(self, lon0, lon1, lat0, lat1, top=330, bottom=1650):
        self.lon0, self.lat1 = lon0, lat1
        k = math.cos(math.radians((lat0 + lat1) / 2))
        sx = W / ((lon1 - lon0) * k); sy = (bottom - top) / (lat1 - lat0)
        self.s = min(sx, sy); self.k = k
        self.ox = (W - (lon1 - lon0) * k * self.s) / 2; self.oy = top + ((bottom - top) - (lat1 - lat0) * self.s) / 2
    def __call__(self, lon, lat):
        return (self.ox + (lon - self.lon0) * self.k * self.s, self.oy + (self.lat1 - lat) * self.s)


def base_map(P):
    im = Image.new("RGB", (W, H), SEA)
    d = ImageDraw.Draw(im)
    for g in LAND_POLYS:
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            pts = [P(x, y) for x, y in poly[0]]
            if max(p[0] for p in pts) < -200 or min(p[0] for p in pts) > W + 200: continue
            d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for f in RIVERS:
        g = f["geometry"]; lines = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
        for ln in lines:
            d.line([P(x, y) for x, y in ln], fill=RIVER, width=4)
    # paper grain + vignette
    noise = Image.effect_noise((W, H), 18).convert("RGB")
    im = Image.blend(im, noise, 0.06)
    vig = Image.new("L", (W, H), 0); ImageDraw.Draw(vig).ellipse((-300, -200, W + 300, H + 200), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(220))
    return Image.composite(im, Image.new("RGB", (W, H), (0, 0, 0)), vig)


def label(d, xy, text, size=44, color=WHITE, anchor="lm", alpha=1.0):
    f = font(F_TITLE, size); x, y = xy
    c = tuple(int(v * alpha) for v in color)
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (2, 2)):
        d.text((x + dx, y + dy), text, font=f, fill=(0, 0, 0), anchor=anchor)
    d.text((x, y), text, font=f, fill=c, anchor=anchor)


def polyline_partial(pts, frac):
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = sum(seg) * frac; out = [pts[0]]
    for i, s in enumerate(seg):
        if L >= s: out.append(pts[i + 1]); L -= s
        else:
            a, b = pts[i], pts[i + 1]; out.append((a[0] + (b[0] - a[0]) * L / s, a[1] + (b[1] - a[1]) * L / s)); break
    return out


def pin(d, c, t, color=RED):
    r = 16 + 4 * math.sin(t * 7)
    for k in range(3):
        q = ((t * 1.2 + k / 3) % 1.0)
        rr = 18 + q * 70; a = int(200 * (1 - q))
        d.ellipse((c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr), outline=color + (a,), width=5)
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=color, outline=WHITE, width=4)


def map_railway(pin_t=4.3, dur=6.0, out="map_railway2.mp4"):
    P = Proj(70.6, 75.2, 29.4, 32.3, top=420, bottom=1500)
    bg = base_map(P)
    stops = {"LAHORE": (74.34, 31.55), "HARAPPA": (72.86, 30.63), "MULTAN": (71.47, 30.20)}
    route = [P(*xy) for xy in [(74.34, 31.55), (73.75, 31.10), (73.10, 30.66), (72.86, 30.63), (72.35, 30.47), (71.93, 30.30), (71.47, 30.20)]]
    hx = P(*stops["HARAPPA"])
    def frame(t):
        im = bg.copy().convert("RGBA"); ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
        fr = ease((t - 0.15) / 1.75)
        pts = polyline_partial(route, fr)
        if len(pts) > 1:
            d.line(pts, fill=(20, 12, 6, 255), width=20, joint="curve")
            d.line(pts, fill=GOLD + (255,), width=10, joint="curve")
            # sleepers
            for i in range(len(pts) - 1):
                a, b = pts[i], pts[i + 1]; L = math.dist(a, b); n = int(L / 26)
                for j in range(n):
                    x = a[0] + (b[0] - a[0]) * j / max(n, 1); y = a[1] + (b[1] - a[1]) * j / max(n, 1)
                    nx, ny = -(b[1] - a[1]) / L, (b[0] - a[0]) / L
                    d.line((x - nx * 16, y - ny * 16, x + nx * 16, y + ny * 16), fill=(30, 20, 10, 255), width=4)
            hx_, hy_ = pts[-1]
            d.ellipse((hx_ - 14, hy_ - 14, hx_ + 14, hy_ + 14), fill=WHITE + (255,))
        label(d, (P(*stops["LAHORE"])[0] - 20, P(*stops["LAHORE"])[1] - 60), "LAHORE", 50, anchor="mm")
        if fr > 0.97:
            label(d, (P(*stops["MULTAN"])[0], P(*stops["MULTAN"])[1] + 70), "MULTAN", 50, anchor="mm")
        if t > pin_t:
            pin(d, hx, t - pin_t)
            a = ease((t - pin_t) / 0.35)
            label(d, (hx[0] + 10, hx[1] - 95), "HARAPPA", 64, color=GOLD, anchor="mm", alpha=a)
        label(d, (W / 2, 250), "THE LAHORE–MULTAN RAILWAY", 46, anchor="mm", alpha=ease(t / 0.4))
        im.alpha_composite(ov)
        z = 1 + 0.35 * ease((t - 2.2) / 3.0)
        if z > 1.001:
            cw, ch = W / z, H / z; cx = min(max(hx[0], cw / 2), W - cw / 2); cy = min(max(hx[1], ch / 2), H - ch / 2)
            im = im.resize((W, H), Image.BICUBIC, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
        return im
    write_mp4(frame, int(dur * FPS), os.path.join(IMG, out))


def map_west():
    P = Proj(38.0, 80.0, 18.0, 38.0, top=420, bottom=1600)
    bg = base_map(P)
    src = P(70.5, 28.8)  # between Harappa and Mohenjo-daro
    dst = {"SUSA (PERSIA)": (48.26, 32.19), "UR (MESOPOTAMIA)": (46.10, 30.96)}
    def arc(a, b, h):
        return [(a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s - h * math.sin(math.pi * s)) for s in np.linspace(0, 1, 60)]
    arcs = [arc(src, P(*dst["SUSA (PERSIA)"]), 260), arc(src, P(*dst["UR (MESOPOTAMIA)"]), 180)]
    def frame(t):
        im = bg.copy().convert("RGBA"); ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
        # Indus region glow
        g = Image.new("RGBA", (W, H)); gd = ImageDraw.Draw(g)
        gd.ellipse((src[0] - 150, src[1] - 210, src[0] + 150, src[1] + 210), fill=GOLD + (90,))
        ov.alpha_composite(g.filter(ImageFilter.GaussianBlur(40)))
        label(d, (src[0] - 40, src[1] + 250), "INDUS VALLEY", 54, color=GOLD, anchor="rm")
        for k, A in enumerate(arcs):
            fr = ease((t - 0.3 - 0.35 * k) / 1.6)
            pts = polyline_partial(A, fr)
            if len(pts) > 1:
                for i in range(0, len(pts) - 1, 2):   # dashed
                    d.line((pts[i], pts[i + 1]), fill=WHITE + (255,), width=9)
                x, y = pts[-1]; d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=GOLD + (255,))
            if fr > 0.98:
                name = list(dst)[k]; c = P(*dst[name]); pin(d, c, t, color=(240, 170, 40))
                label(d, (max(c[0] - 60, 20), c[1] + (-80 if k == 0 else 80)), name, 42, anchor="lm")
        label(d, (W / 2, 300), "SAME SEALS. 2,000+ KM APART.", 50, anchor="mm", alpha=ease((t - 1.8) / 0.4))
        im.alpha_composite(ov); return im
    write_mp4(frame, int(3.6 * FPS), os.path.join(IMG, "map_west.mp4"))


# ------------------------------------------------------------------ timeline "+2,000 years"
def timeline():
    bgsrc = Image.open(os.path.join(IMG, "harappa_ruins.jpg")).convert("RGB")
    s = max(W / bgsrc.width, H / bgsrc.height); bgsrc = bgsrc.resize((int(bgsrc.width * s), int(bgsrc.height * s)))
    bgsrc = bgsrc.crop(((bgsrc.width - W) // 2, (bgsrc.height - H) // 2, (bgsrc.width - W) // 2 + W, (bgsrc.height - H) // 2 + H))
    bg = Image.blend(bgsrc.filter(ImageFilter.GaussianBlur(14)), Image.new("RGB", (W, H), (0, 0, 0)), 0.62)
    x_now, x_old, x_new, y = 960, 640, 120, 1180
    def frame(t):
        im = bg.copy().convert("RGBA"); d = ImageDraw.Draw(im)
        d.text((W / 2, 520), "INDIA'S KNOWN HISTORY", font=font(F_TITLE, 54), fill=WHITE, anchor="mm")
        p = ease((t - 0.5) / 1.7)
        n = int(round(2000 * p / 50) * 50)
        big = font(F_BIG, 210)
        d.text((W / 2, 800), f"+{n:,}", font=big, fill=GOLD, anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
        d.text((W / 2, 960), "YEARS", font=font(F_BIG, 90), fill=GOLD, anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
        d.rounded_rectangle((x_new - 10, y - 26, x_now + 10, y + 26), 26, fill=(40, 40, 40))
        d.rounded_rectangle((x_old, y - 22, x_now, y + 22), 22, fill=(200, 200, 200))   # what was known before
        xl = x_old - (x_old - x_new) * p
        if p > 0: d.rounded_rectangle((xl, y - 22, x_old + 22, y + 22), 22, fill=GOLD)
        d.text((x_now, y + 70), "1924", font=font(F_TITLE, 40), fill=WHITE, anchor="mm")
        d.text(((x_old + x_now) / 2, y - 70), "BEFORE", font=font(F_TITLE, 34), fill=(210, 210, 210), anchor="mm")
        if p > 0.6: d.text(((x_new + x_old) / 2, y - 70), "AFTER ONE LETTER", font=font(F_TITLE, 34), fill=GOLD, anchor="mm")
        return im
    write_mp4(frame, int(3.6 * FPS), os.path.join(IMG, "timeline.mp4"))


# ------------------------------------------------------------------ brick dust overlay (for "screen" blend)
def dust():
    rng = np.random.default_rng(7); N = 260
    x = rng.uniform(0, W, N); y = rng.uniform(0, H, N); vx = rng.uniform(-30, 60, N); vy = rng.uniform(-60, -10, N)
    r = rng.uniform(1.5, 5, N); b = rng.uniform(0.3, 1, N)
    def frame(t):
        im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
        for i in range(N):
            px = (x[i] + vx[i] * t) % W; py = (y[i] + vy[i] * t) % H
            c = (int(255 * b[i]), int(170 * b[i]), int(100 * b[i]))
            d.ellipse((px - r[i], py - r[i], px + r[i], py + r[i]), fill=c)
        return im.filter(ImageFilter.GaussianBlur(1.2))
    write_mp4(frame, int(5 * FPS), os.path.join(IMG, "dust.mp4"))


# ------------------------------------------------------------------ synthesized SFX (phone-audible: energy kept in 200 Hz to 5 kHz)
def save(name, a):
    a = a / (np.abs(a).max() or 1) * 0.9
    st = np.stack([a, a], 1)
    with wave.open(os.path.join(SFX, name + ".wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
    print("sfx", name, round(len(a) / SR, 2), "s")


def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))


def env(n, a, d):
    t = np.arange(n) / SR; return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)


rng = np.random.default_rng(3)


def sfx_all():
    # steam train chug: 4 chuffs per second over a rumble, plus rail clacks
    n = int(3.2 * SR); out = np.zeros(n)
    for k in range(13):
        st = int(k * 0.25 * SR); m = int(0.22 * SR)
        ch = bp(rng.normal(size=m), 250, 3500) * env(m, 0.01, 0.06) * (1.0 if k % 2 == 0 else 0.6)
        out[st:st + m] += ch[: n - st]
    t = np.arange(n) / SR
    out += 0.35 * bp(rng.normal(size=n), 80, 400) * (0.6 + 0.4 * np.sin(2 * np.pi * 4 * t))
    for k in range(4):
        st = int((0.4 + k * 0.8) * SR); m = int(0.08 * SR)
        out[st:st + m] += 1.2 * bp(rng.normal(size=m), 1500, 6000) * env(m, 0.001, 0.015)
    out *= np.minimum(t / 0.3, 1) * np.minimum((3.2 - t) / 0.6, 1)
    save("train_chug", out)
    # steam whistle: two-tone chord with breath, slight pitch rise
    n = int(1.7 * SR); t = np.arange(n) / SR; bend = 1 + 0.015 * np.minimum(t / 0.2, 1)
    w = sum(np.sin(2 * np.pi * f * bend * t) * g for f, g in ((440, 1), (554, 0.8), (659, 0.6), (880, 0.25)))
    w += 0.25 * bp(rng.normal(size=n), 400, 3000)
    w *= np.minimum(t / 0.08, 1) * np.minimum((1.7 - t) / 0.5, 1)
    save("train_whistle", w)
    # hammer on brick: crack + crumble debris
    n = int(0.9 * SR); out = np.zeros(n)
    m = int(0.03 * SR); out[:m] += 1.5 * bp(rng.normal(size=m), 800, 9000) * env(m, 0.0005, 0.006)
    m2 = int(0.35 * SR); out[:m2] += bp(rng.normal(size=m2), 300, 4500) * env(m2, 0.002, 0.07)
    for k in range(25):
        st = int(rng.uniform(0.05, 0.7) * SR); m = int(0.02 * SR)
        out[st:st + m] += rng.uniform(0.1, 0.4) * bp(rng.normal(size=m), 1500, 7000) * env(m, 0.0005, 0.004)
    save("hammer_brick", out)
    # clock ticks (tick-tock x4) for "one week later"
    n = int(2.1 * SR); out = np.zeros(n)
    for k in range(4):
        st = int(k * 0.5 * SR); m = int(0.05 * SR); f = 3200 if k % 2 == 0 else 2400
        tt = np.arange(m) / SR; out[st:st + m] += (np.sin(2 * np.pi * f * tt) + 0.6 * bp(rng.normal(size=m), 2000, 8000)) * env(m, 0.0003, 0.006)
    save("clock_tick", out)
    # heartbeat with harmonics so phones hear it
    n = int(1.4 * SR); out = np.zeros(n)
    for st_s, g in ((0, 1), (0.28, 0.7)):
        st = int(st_s * SR); m = int(0.25 * SR); tt = np.arange(m) / SR
        thump = sum(np.sin(2 * np.pi * f * tt) / h for h, f in ((1, 55), (2, 110), (3, 165), (4, 220), (6, 330)))
        out[st:st + m] += g * thump * env(m, 0.004, 0.05)
    save("heartbeat_phone", out)
    # paper rustle for the letter
    n = int(0.7 * SR); t = np.arange(n) / SR
    out = bp(rng.normal(size=n), 1500, 9000) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 9 * t))) * np.minimum(t / 0.05, 1) * np.minimum((0.7 - t) / 0.2, 1)
    save("paper", out)
    # stone tap: small seal set down
    n = int(0.4 * SR); tt = np.arange(n) / SR
    out = (np.sin(2 * np.pi * 1900 * tt) + 0.7 * np.sin(2 * np.pi * 2730 * tt)) * env(n, 0.0005, 0.03) + 0.6 * bp(rng.normal(size=n), 1000, 8000) * env(n, 0.0003, 0.005)
    save("stone_tap", out)


def fix_ai5():
    im = Image.open(os.path.join(IMG, "ai5.png")).convert("RGB")
    box = (int(im.width * 0.30), int(im.height * 0.345), im.width, int(im.height * 0.43))  # garbled newspaper header
    im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(14)), box[:2])
    im.save(os.path.join(IMG, "ai5_fix.png")); print("wrote ai5_fix.png")

def seal(t_bull=1.35, t_signs=2.35, dur=4.2):
    """Real Cunningham seal (British Museum): wide on seal + impression, push into the clay impression,
    soft gold glow on the bull, then a red ring draws itself around the six signs."""
    src = Image.open(os.path.join(IMG, "cunningham_seal_BM.jpg")).convert("RGB")
    sw, sh = src.size
    bgf = src.resize((int(sw * H / sh), H)).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(30))
    bgf = Image.blend(bgf, Image.new("RGB", (W, H)), 0.55)
    f_ = sw / 960; wide = (0, 0, sw, sh); tight = tuple(v * f_ for v in (520, 20, 920, 330))      # clay impression: signs y 50-160, bull y 190-300
    def frame(t):
        p = ease((t - 0.6) / 1.4)
        box = [wide[i] + (tight[i] - wide[i]) * p for i in range(4)]
        bw, bh = box[2] - box[0], box[3] - box[1]
        s_ = min(W / bw, (H * 0.62) / bh)
        crop = src.resize((max(1, int(bw * s_)), max(1, int(bh * s_))), Image.BICUBIC, box=tuple(box))
        im = bgf.copy().convert("RGBA"); ox, oy = (W - crop.width) // 2, int(H * 0.40 - crop.height / 2)
        im.paste(crop, (ox, oy))
        d = ImageDraw.Draw(im)
        def to_scr(x, y): return (ox + (x * f_ - box[0]) * s_, oy + (y * f_ - box[1]) * s_)
        if t > t_bull and p > 0.95:
            a = ease((t - t_bull) / 0.4)
            g = Image.new("RGBA", (W, H)); gd = ImageDraw.Draw(g)
            (x0, y0), (x1, y1) = to_scr(590, 190), to_scr(880, 305)
            gd.ellipse((x0, y0, x1, y1), outline=GOLD + (int(220 * a),), width=10)
            im.alpha_composite(g.filter(ImageFilter.GaussianBlur(2)))
        if t > t_signs and p > 0.95:
            q = ease((t - t_signs) / 0.5)
            (x0, y0), (x1, y1) = to_scr(575, 40), to_scr(890, 170)
            cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 20, (y1 - y0) / 2 + 20
            pts = [(cx + rx * math.cos(-math.pi / 2 + 2 * math.pi * q * k / 80 * 1.06), cy + ry * math.sin(-math.pi / 2 + 2 * math.pi * q * k / 80 * 1.06)) for k in range(81)]
            d.line(pts, fill=(0, 0, 0, 170), width=20, joint="curve"); d.line(pts, fill=RED + (255,), width=12, joint="curve")
            if q > 0.9:
                d.text((W / 2, 260), "STILL UNDECIPHERED TODAY", font=font(F_TITLE, 46), fill=WHITE + (255,), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))
        d.text((W / 2, 1560), "REAL: THE FIRST INDUS SEAL · BRITISH MUSEUM", font=font(F_TITLE, 34), fill=(230, 230, 230, 255), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
        return im
    write_mp4(frame, int(dur * FPS), os.path.join(IMG, "seal_signs.mp4"))



if __name__ == "__main__":
    import sys
    todo = sys.argv[1:] or ["sfx", "dust", "railway", "west", "timeline", "ai5", "seal"]
    if "sfx" in todo: sfx_all()
    if "dust" in todo: dust()
    if "railway" in todo: map_railway()
    if "west" in todo: map_west()
    if "timeline" in todo: timeline()
    if "ai5" in todo: fix_ai5()
    if "seal" in todo: seal()
