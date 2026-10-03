"""fxkit.py - code-built visuals and sounds for Legend's Shorts (any channel).

Every function writes a 1080x1920 30 fps MP4 (or a WAV for sounds) that make_short2.py / make_short.py use like any clip.
Clips HOLD their last frame for the rest of `dur`: always make `dur` longer than the shot (a clip shorter than its
shot loops back to frame 0, e.g. a "+2,000" counter suddenly showing "+0").

  import fxkit as fx
  fx.punch_hook("images/ai1.png", "images/hook.mp4", focus=(0.36, 0.42), chips_from=(0.05, 0.72, 0.6, 0.95))
  fx.route_map(stops, route, bounds, "images/map_draw.mp4", draw=(0.1, 0.8))            # fast line draw
  fx.route_map(stops, route, bounds, "images/map_pin.mp4", pin="HARAPPA", pin_t=0.7, draw=(-1, 0.01))
  fx.arc_map(src, dests, bounds, "images/map_west.mp4", caption="SAME SEALS. 2,000+ KM APART.")
  fx.counter("images/bg.jpg", "images/count.mp4", 2000, top="INDIA'S KNOWN HISTORY", unit="YEARS", prefix="+")
  fx.zoom_rings("images/seal.jpg", "images/seal.mp4", wide, tight, rings=[...], top_text="STILL UNDECIPHERED TODAY")
  fx.stamp("images/seal.jpg", "images/stamp.mp4", "FOREIGN?", label='A. CUNNINGHAM, 1875: "FOREIGN TO INDIA"')
  fx.stamp(..., strike_t=0.45, stamped_from_start=True)                                   # payoff: strike it out
  fx.ending("images/ai6.png", "images/ending.mp4", ["INDUS VALLEY", "CIVILISATION"], ["BUT WHO", "WERE THEY?"], "INDUS FILES  #2")
  fx.dust("images/dust.mp4")                       # overlay with "mode": "screen"
  fx.blur_box("images/ai5.png", "images/ai5_fix.png", (0.30, 0.345, 1.0, 0.43))      # hide AI gibberish text
  fx.make_sfx("sfx")                               # writes the synthesized story sounds below

Tamil text: pass font=fx.TAMIL (Noto Sans Tamil) to any text argument family (stamp, counter, ending).
Map data: Natural Earth GeoJSON in ROOT/geo (download once from raw.githubusercontent.com/nvkelso/natural-earth-vector).
"""
import json, math, os, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, SR = 1080, 1920, 30, 44100
ROOT = os.path.dirname(os.path.abspath(__file__))
F_TITLE = os.path.join(ROOT, "fonts", "Cinzel-Bold.ttf")
F_BIG = os.path.join(ROOT, "fonts", "Anton.ttf")
TAMIL = os.path.join(ROOT, "fonts", "NotoSansTamilLatin-800.ttf")   # ships with the Udal Uzhavan engine; copy it into fonts/ if missing
GOLD, RED, WHITE = (255, 197, 61), (230, 50, 40), (245, 240, 230)
SEA, LAND, LAND_EDGE, RIVER = (12, 22, 32), (58, 46, 32), (120, 96, 60), (70, 140, 190)


def font(p, s): return ImageFont.truetype(p, s)
def ease(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3


def write_mp4(frame_fn, dur, path):
    n = int(dur * FPS)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", path], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame_fn(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); print("wrote", path)


def cover(im, w=W, h=H):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2; return im.crop((x, y, x + w, y + h))


def outlined(d, xy, text, f, fill, anchor="mm", stroke=3):
    d.text(xy, text, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0, fill[3] if len(fill) > 3 else 255))


# ------------------------------------------------------------------ hook: whip push-in + photographic debris + steam/dust
def punch_hook(image, out, focus=(0.5, 0.45), chips_from=(0.05, 0.72, 0.6, 0.95), dur=3.4, steam=True, n_chips=90, seed=11):
    """Frame 1 stays crisp (it is the thumbnail). Then: flash, zoom-blur burst, push-in with decaying shake,
    debris cut from the image itself (chips_from = x0,y0,x1,y1 fractions of a textured area) flying at the camera."""
    src = Image.open(image).convert("RGB"); s = max(W / src.width, H / src.height) * 1.02
    src = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    rng = np.random.default_rng(seed); N = n_chips
    ang = rng.uniform(0, 2 * np.pi, N); spd = rng.uniform(0.6, 1.6, N)
    t0 = np.concatenate([rng.uniform(0.05, 0.35, N // 2), rng.uniform(0.35, 1.8, N - N // 2)]); rot = rng.uniform(0, 360, N)
    cx0, cy0 = focus[0] * W, focus[1] * H + 120
    chips = []
    for _ in range(40):
        cw = int(rng.uniform(26, 60)); x = int(rng.uniform(chips_from[0], chips_from[2]) * src.width); y = int(rng.uniform(chips_from[1], chips_from[3]) * src.height)
        patch = src.crop((x, y, x + cw, y + int(cw * 0.75))).convert("RGBA")
        m = Image.new("L", patch.size, 0)
        ImageDraw.Draw(m).polygon([(patch.width / 2 * (1 + (0.6 + 0.4 * rng.random()) * math.cos(2 * math.pi * j / 6)),
                                    patch.height / 2 * (1 + (0.6 + 0.4 * rng.random()) * math.sin(2 * math.pi * j / 6))) for j in range(6)], fill=255)
        patch.putalpha(m.filter(ImageFilter.GaussianBlur(1))); chips.append(patch)
    puffs = [(rng.uniform(-0.1, 0.5) * W, rng.uniform(-0.05, 0.25) * H, rng.uniform(0, 0.8), rng.uniform(260, 520)) for _ in range(9)]

    def view(z, dx=0, dy=0):
        cw, ch = W / z, H / z; fx, fy = focus[0] * src.width, focus[1] * src.height
        x0 = min(max(fx - cw / 2 + dx, 0), src.width - cw); y0 = min(max(fy - ch / 2 + dy, 0), src.height - ch)
        return src.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))

    def frame(t):
        q0 = max(t - 0.04, 0); z = 1.0 + 0.32 * (1 - math.exp(-q0 * 3.2)) + 0.04 * q0
        amp = 26 * math.exp(-t * 2.5) + 3; dx, dy = amp * math.sin(t * 61), amp * math.cos(t * 47)
        im = view(z, dx, dy)
        if 0.04 < t < 0.55:
            k = 1 - (t - 0.04) / 0.51
            for j in (1, 2, 3): im = Image.blend(im, view(z * (1 + 0.035 * j * k), dx, dy), 0.28 * k)
        im = im.convert("RGBA")
        if steam:
            st = Image.new("RGBA", (W, H)); sd = ImageDraw.Draw(st)
            for (px, py, d0, r) in puffs:
                q = (t - d0) / 2.2
                if 0 < q < 1:
                    rr = r * (0.4 + 1.4 * q); a = int(170 * (1 - q) * min(1, q * 6))
                    sd.ellipse((px + 260 * q - rr, py - 80 * q - rr, px + 260 * q + rr, py - 80 * q + rr), fill=(235, 230, 222, a))
            im.alpha_composite(st.filter(ImageFilter.GaussianBlur(40)))
        du = Image.new("RGBA", (W, H)); dd = ImageDraw.Draw(du)
        for j in range(6):
            q = (t - 0.06 - j * 0.12) / 1.6
            if 0 < q < 1:
                rr = 160 + 520 * q; a = int(150 * (1 - q)); x = W * (0.25 + 0.1 * j); y = H * 0.68 - 120 * q
                dd.ellipse((x - rr, y - rr * 0.5, x + rr, y + rr * 0.5), fill=(200, 160, 120, a))
        im.alpha_composite(du.filter(ImageFilter.GaussianBlur(50)))
        for i in range(N):
            q = float(t - t0[i])
            if q <= 0 or q > 1.3: continue
            dist = (q * spd[i]) ** 1.7 * 950
            x = cx0 + math.cos(ang[i]) * dist; y = cy0 + math.sin(ang[i]) * dist * 0.8 + 350 * q * q
            sc = 0.35 + q * 2.4; c = chips[i % len(chips)]
            c2 = c.resize((max(4, int(c.width * sc)), max(4, int(c.height * sc))), Image.BILINEAR).rotate(rot[i] + q * 420, expand=True)
            if q > 0.25: c2 = c2.filter(ImageFilter.GaussianBlur(min(4.0, q * 4)))
            if -c2.width < x < W + c2.width and -c2.height < y < H + c2.height:
                im.alpha_composite(c2, (int(x - c2.width / 2), int(y - c2.height / 2)))
        if 0.03 < t < 0.16:
            im = Image.blend(im, Image.new("RGBA", (W, H), (255, 245, 225, 255)), 0.4 * (1 - (t - 0.03) / 0.13))
        return im
    write_mp4(frame, dur, out)


# ------------------------------------------------------------------ maps (Natural Earth, no national borders drawn)
_GEO = {}
def _geo():
    if not _GEO:
        g = os.path.join(ROOT, "geo")
        _GEO["land"] = [f["geometry"] for f in json.load(open(os.path.join(g, "ne_50m_land.geojson")))["features"]]
        _GEO["rivers"] = json.load(open(os.path.join(g, "ne_50m_rivers_lake_centerlines.geojson")))["features"]
    return _GEO


class Proj:
    def __init__(self, lon0, lon1, lat0, lat1, top=420, bottom=1600):
        self.lon0, self.lat1 = lon0, lat1; k = math.cos(math.radians((lat0 + lat1) / 2))
        self.s = min(W / ((lon1 - lon0) * k), (bottom - top) / (lat1 - lat0)); self.k = k
        self.ox = (W - (lon1 - lon0) * k * self.s) / 2; self.oy = top + ((bottom - top) - (lat1 - lat0) * self.s) / 2
    def __call__(self, lon, lat): return (self.ox + (lon - self.lon0) * self.k * self.s, self.oy + (self.lat1 - lat) * self.s)


def base_map(P, rivers=("Indus", "Ravi", "Sutlej", "Chenab", "Jhelum", "Ganges", "Yamuna", "Tigris", "Euphrates", "Karun", "Nile")):
    G = _geo(); im = Image.new("RGB", (W, H), SEA); d = ImageDraw.Draw(im)
    for g in G["land"]:
        for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]):
            d.polygon([P(x, y) for x, y in poly[0]], fill=LAND, outline=LAND_EDGE)
    for f in G["rivers"]:
        if (f["properties"].get("name") or "") in rivers:
            g = f["geometry"]
            for ln in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
                d.line([P(x, y) for x, y in ln], fill=RIVER, width=4)
    im = Image.blend(im, Image.effect_noise((W, H), 18).convert("RGB"), 0.06)
    vig = Image.new("L", (W, H), 0); ImageDraw.Draw(vig).ellipse((-300, -200, W + 300, H + 200), fill=255)
    return Image.composite(im, Image.new("RGB", (W, H)), vig.filter(ImageFilter.GaussianBlur(220)))


def map_label(d, xy, text, size=44, color=WHITE, anchor="lm", alpha=1.0, f=F_TITLE):
    fnt = font(f, size); c = tuple(int(v * alpha) for v in color)
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (2, 2)): d.text((xy[0] + dx, xy[1] + dy), text, font=fnt, fill=(0, 0, 0), anchor=anchor)
    d.text(xy, text, font=fnt, fill=c, anchor=anchor)


def _partial(pts, frac):
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; L = sum(seg) * frac; out = [pts[0]]
    for i, s in enumerate(seg):
        if L >= s: out.append(pts[i + 1]); L -= s
        else: a, b = pts[i], pts[i + 1]; out.append((a[0] + (b[0] - a[0]) * L / s, a[1] + (b[1] - a[1]) * L / s)); break
    return out


def _pin(d, c, t, color=RED):
    r = 16 + 4 * math.sin(t * 7)
    for k in range(3):
        q = (t * 1.2 + k / 3) % 1.0; rr = 18 + q * 70
        d.ellipse((c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr), outline=color + (int(200 * (1 - q)),), width=5)
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=color, outline=WHITE, width=4)


def route_map(stops, route, bounds, out, pin=None, pin_t=99, draw=(0.1, 0.8), zoom=(1.0, 1.0, 0, 1), title=None, dur=2.6,
              first="", last=""):
    """stops: {"NAME": (lon, lat)}; route: [(lon, lat), ...] drawn as a railway/road; bounds: (lon0, lon1, lat0, lat1).
    Keep draw[1] under 1 s (Gemini: slow map draws are swipe points). Pair with the 'scribble' sound."""
    P = Proj(*bounds); bg = base_map(P); pts = [P(*xy) for xy in route]
    first = first or list(stops)[0]; last = last or list(stops)[-1]
    def frame(t):
        im = bg.copy().convert("RGBA"); ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
        fr = ease((t - draw[0]) / draw[1]); p = _partial(pts, fr)
        if len(p) > 1:
            d.line(p, fill=(20, 12, 6, 255), width=20, joint="curve"); d.line(p, fill=GOLD + (255,), width=10, joint="curve")
            x, y = p[-1]; d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=WHITE + (255,))
        a = P(*stops[first]); map_label(d, (a[0] - 20, a[1] - 60), first, 50, anchor="mm")
        if fr > 0.97: b = P(*stops[last]); map_label(d, (b[0], b[1] + 70), last, 50, anchor="mm")
        if pin and t > pin_t:
            c = P(*stops[pin]); _pin(d, c, t - pin_t); map_label(d, (c[0] + 10, c[1] - 95), pin, 64, GOLD, "mm", ease((t - pin_t) / 0.35))
        if title: map_label(d, (W / 2, 250), title, 46, anchor="mm", alpha=ease(t / 0.25))
        im.alpha_composite(ov)
        z = zoom[0] + (zoom[1] - zoom[0]) * ease((t - zoom[2]) / zoom[3])
        if z > 1.001:
            fc = P(*stops[pin]) if pin else (W / 2, H / 2); cw, ch = W / z, H / z
            cx = min(max(W / 2, cw / 2), W - cw / 2); cy = min(max(fc[1], ch / 2), H - ch / 2)
            im = im.resize((W, H), Image.BICUBIC, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
        return im
    write_mp4(frame, dur, out)


def arc_map(src, dests, bounds, out, src_name="", caption="", dur=5.5, draw=(0.3, 1.6), cap_t=1.8):
    """Dashed arcs from src (lon, lat) to each {"NAME": (lon, lat)}: trade, travel, influence."""
    P = Proj(*bounds); bg = base_map(P); s = P(*src)
    def arc(a, b, h): return [(a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u - h * math.sin(math.pi * u)) for u in np.linspace(0, 1, 60)]
    arcs = [arc(s, P(*xy), 260 - 80 * k) for k, xy in enumerate(dests.values())]
    def frame(t):
        im = bg.copy().convert("RGBA"); ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
        g = Image.new("RGBA", (W, H)); ImageDraw.Draw(g).ellipse((s[0] - 150, s[1] - 210, s[0] + 150, s[1] + 210), fill=GOLD + (90,))
        ov.alpha_composite(g.filter(ImageFilter.GaussianBlur(40)))
        if src_name: map_label(d, (s[0] - 40, s[1] + 250), src_name, 54, GOLD, "rm")
        for k, A in enumerate(arcs):
            fr = ease((t - draw[0] - draw[0] * 1.1 * k) / draw[1]); p = _partial(A, fr)
            if len(p) > 1:
                for i in range(0, len(p) - 1, 2): d.line((p[i], p[i + 1]), fill=WHITE + (255,), width=9)
                x, y = p[-1]; d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=GOLD + (255,))
            if fr > 0.98:
                name = list(dests)[k]; c = P(*dests[name]); _pin(d, c, t, (240, 170, 40))
                map_label(d, (max(c[0] - 60, 20), c[1] + (-80 if k % 2 == 0 else 80)), name, 42)
        if caption: map_label(d, (W / 2, 300), caption, 50, anchor="mm", alpha=ease((t - cap_t) / 0.3))
        im.alpha_composite(ov); return im
    write_mp4(frame, dur, out)


# ------------------------------------------------------------------ counter / stat count-up
def counter(bg_image, out, value, top="", unit="", prefix="+", suffix="", window=(0.15, 1.75), dur=6.5, bar=True, f_top=F_TITLE, f_num=F_BIG):
    """Count-up that HOLDS on the final value. Time window[0]+window[1] to land on the spoken number.
    Health use: counter(bg, out, 38, top="நீரிழிவு அபாயம்", unit="", prefix="", suffix="%", f_top=TAMIL)."""
    bg = Image.blend(cover(Image.open(bg_image).convert("RGB")).filter(ImageFilter.GaussianBlur(14)), Image.new("RGB", (W, H)), 0.62)
    def frame(t):
        im = bg.copy().convert("RGBA"); d = ImageDraw.Draw(im); p = ease((t - window[0]) / window[1])
        step = 50 if value >= 500 else 1; n = int(round(value * p / step) * step)
        if top: d.text((W / 2, 520), top, font=font(f_top, 54), fill=WHITE, anchor="mm")
        d.text((W / 2, 800), f"{prefix}{n:,}{suffix}", font=font(f_num, 210), fill=GOLD, anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
        if unit: d.text((W / 2, 960), unit, font=font(f_num, 90), fill=GOLD, anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
        if bar:
            y = 1180; d.rounded_rectangle((110, y - 26, 970, y + 26), 26, fill=(40, 40, 40)); d.rounded_rectangle((640, y - 22, 960, y + 22), 22, fill=(200, 200, 200))
            if p > 0: d.rounded_rectangle((640 - 520 * p, y - 22, 662, y + 22), 22, fill=GOLD)
        return im
    write_mp4(frame, dur, out)


# ------------------------------------------------------------------ zoom into a real photo + self-drawing rings
def zoom_rings(image, out, wide, tight, rings=(), top_text="", label="", dur=5.5, push=(0.6, 1.4)):
    """wide/tight: (x0, y0, x1, y1) source pixels. rings: [{"box": (x0,y0,x1,y1), "t": 1.35, "color": "gold"|"red"}].
    Use for the exact detail the narration names ('a bull', 'six signs')."""
    src = Image.open(image).convert("RGB")
    bgf = Image.blend(cover(src).filter(ImageFilter.GaussianBlur(30)), Image.new("RGB", (W, H)), 0.55)
    def frame(t):
        p = ease((t - push[0]) / push[1]); box = [wide[i] + (tight[i] - wide[i]) * p for i in range(4)]
        bw, bh = box[2] - box[0], box[3] - box[1]; s = min(W / bw, (H * 0.62) / bh)
        crop = src.resize((max(1, int(bw * s)), max(1, int(bh * s))), Image.BICUBIC, box=tuple(box))
        im = bgf.copy().convert("RGBA"); ox, oy = (W - crop.width) // 2, int(H * 0.40 - crop.height / 2); im.paste(crop, (ox, oy))
        def scr(x, y): return (ox + (x - box[0]) * s, oy + (y - box[1]) * s)
        for r in rings:
            if t > r["t"] and p > 0.95:
                q = ease((t - r["t"]) / 0.5); (x0, y0), (x1, y1) = scr(*r["box"][:2]), scr(*r["box"][2:])
                cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 20, (y1 - y0) / 2 + 20
                col = GOLD if r.get("color") == "gold" else RED
                pts = [(cx + rx * math.cos(-math.pi / 2 + 2 * math.pi * q * k / 80 * 1.06), cy + ry * math.sin(-math.pi / 2 + 2 * math.pi * q * k / 80 * 1.06)) for k in range(81)]
                ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
                d.line(pts, fill=(0, 0, 0, 170), width=20, joint="curve"); d.line(pts, fill=col + (255,), width=12, joint="curve"); im.alpha_composite(ov)
                if r.get("text") and q > 0.9: outlined(ImageDraw.Draw(im), (W / 2, max(110, oy - 70)), r["text"], font(F_TITLE, 46), WHITE + (255,))
        d = ImageDraw.Draw(im)
        if top_text and t > (rings[-1]["t"] + 0.45 if rings else 0): outlined(d, (W / 2, max(110, oy - 70)), top_text, font(F_TITLE, 46), WHITE + (255,))
        if label: outlined(d, (W / 2, 1560), label, font(F_TITLE, 34), (230, 230, 230, 255), stroke=2)
        return im
    write_mp4(frame, dur, out)


# ------------------------------------------------------------------ rubber stamp verdict (+ strike-through payoff)
def stamp(image, out, text, label="", t_stamp=0.9, strike_t=None, stamped_from_start=False, dur=3.4, color=(205, 30, 30), f=F_BIG, sink=True, border=True, size=190):
    """Slams a worn ink stamp onto a photo. Uses: a historical verdict ('FOREIGN?'), myth-busting ('MYTH' / 'பொய்!'),
    a fact check ('TRUE' in green). Start the shot at word:<x>@-t_stamp so the slam lands on the word; add the 'stamp' sound."""
    src = Image.open(image).convert("RGB"); sw, sh = src.size
    bgf = Image.blend(cover(src).filter(ImageFilter.GaussianBlur(30)), Image.new("RGB", (W, H)), 0.55)
    fnt = font(f, size); tw = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(text, font=fnt)) + 120
    st = Image.new("RGBA", (max(760, tw), 300)); sd = ImageDraw.Draw(st)
    if border: sd.rounded_rectangle((10, 10, st.width - 10, 290), 30, outline=color + (255,), width=18)   # border=False for Udal Uzhavan (no boxes rule)
    sd.text((st.width / 2, 152), text, font=fnt, fill=color + (255,), anchor="mm")
    grit = Image.effect_noise(st.size, 90).point(lambda v: 255 if v > 95 else 0)
    st.putalpha(Image.composite(st.getchannel("A"), Image.new("L", st.size, 0), grit)); st = st.rotate(-11, expand=True, resample=Image.BICUBIC)
    if st.width > W * 0.95: st = st.resize((int(W * 0.95), int(st.height * W * 0.95 / st.width)))
    def frame(t):
        z = 1.0 + 0.06 * t / dur; bw = W * (1.28 if sw / sh > 1.3 else 1.0) * z; s = bw / sw
        crop = src.resize((int(sw * s), int(sh * s)), Image.BICUBIC)
        im = bgf.copy().convert("RGBA"); ox, oy = (W - crop.width) // 2, int(H * 0.42 - crop.height / 2); dx = dy = 0
        if not stamped_from_start and 0 <= t - t_stamp < 0.35:
            a = 22 * (1 - (t - t_stamp) / 0.35); dx, dy = int(a * math.sin(t * 90)), int(a * math.cos(t * 70))
        im.paste(crop, (ox + dx, oy + dy))
        show = stamped_from_start or t >= t_stamp
        if show:
            q = 1.0 if stamped_from_start else min(1, (t - t_stamp) / 0.11)
            sc = 2.3 - 1.3 * ease(q); s2 = st.resize((int(st.width * sc), int(st.height * sc)), Image.BICUBIC)
            fade = 1.0 if strike_t is None or t <= strike_t + 0.45 else max(0, 1 - (t - strike_t - 0.45) / 0.5)
            if fade < 1: s2.putalpha(s2.getchannel("A").point(lambda v, f_=fade: int(v * f_)))
            im.alpha_composite(s2, (W // 2 - s2.width // 2 + dx, int(H * 0.42) - s2.height // 2 + dy))
            if strike_t is not None and t > strike_t:
                p = ease((t - strike_t) / 0.3); sl = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(sl)
                x0, y0, x1, y1 = W * 0.08, H * 0.48, W * 0.92, H * 0.36
                d.line((x0, y0, x0 + (x1 - x0) * p, y0 + (y1 - y0) * p), fill=(255, 255, 255, int(255 * fade)), width=24); im.alpha_composite(sl)
            if strike_t is not None and t > strike_t + 0.6:
                g = ease((t - strike_t - 0.6) / 0.5); gl = Image.new("RGBA", (W, H))
                ImageDraw.Draw(gl).rounded_rectangle((ox - 10, oy - 10, ox + crop.width + 10, oy + crop.height + 10), 30, outline=GOLD + (int(230 * g),), width=12)
                im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(6)))
        if strike_t is None and show:
            if label: outlined(ImageDraw.Draw(im), (W / 2, 1560), label, font(F_TITLE, 36), (235, 235, 235, 255), stroke=2)
            m = ease((t - t_stamp - 0.9) / 1.2)
            if sink and m > 0: im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), 0.55 * m)
        return im
    write_mp4(frame, dur, out)


# ------------------------------------------------------------------ ending: title reveal -> cliffhanger question
def ending(image, out, title, question, series="", dur=4.6, q_at=2.1, f_big=F_BIG, f_small=F_TITLE):
    src = cover(Image.open(image).convert("RGB"), int(W * 1.12), int(H * 1.12))
    f1, f2, f3 = font(f_big, 150), font(f_big, 112), font(f_small, 44)
    def frame(t):
        z = 1.0 + 0.10 * t / dur; cw, ch = W * 1.12 / z, H * 1.12 / z; cw, ch = min(cw, src.width), min(ch, src.height); x0 = max(0, (src.width - cw) / 2); y0 = max(0, (src.height - ch) * 0.35)
        im = src.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)).convert("RGBA")
        q = ease((t - q_at) / 0.6)
        if q > 0: im = Image.blend(im, Image.new("RGBA", (W, H), (0, 0, 0, 255)), 0.55 * q)
        ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
        a = ease((t - 0.1) / 0.5) * (1 - 0.65 * q); dy = 40 * (1 - ease((t - 0.1) / 0.5)) - 120 * q
        for k, txt in enumerate(title):
            outlined(d, (W / 2, 560 + k * 165 + dy), txt, f1, (GOLD if k == 0 else WHITE) + (int(255 * a),), stroke=6)
        if q > 0:
            b = ease((t - q_at - 0.1) / 0.5)
            for k, txt in enumerate(question):
                outlined(d, (W / 2, 1060 + k * 125), txt, f2, (WHITE if k == 0 else GOLD) + (int(255 * b),), stroke=5)
            if series:
                c = ease((t - q_at - 0.7) / 0.5); outlined(d, (W / 2, 1060 + len(question) * 125 + 20), series, f3, (230, 230, 230, int(255 * c)), stroke=2)
        im.alpha_composite(ov.filter(ImageFilter.GaussianBlur(18))); im.alpha_composite(ov); return im
    write_mp4(frame, dur, out)


# ------------------------------------------------------------------ overlays and fixes
def dust(out, dur=5, n=260, seed=7):
    rng = np.random.default_rng(seed); x = rng.uniform(0, W, n); y = rng.uniform(0, H, n)
    vx = rng.uniform(-30, 60, n); vy = rng.uniform(-60, -10, n); r = rng.uniform(1.5, 5, n); b = rng.uniform(0.3, 1, n)
    def frame(t):
        im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
        for i in range(n):
            px, py = (x[i] + vx[i] * t) % W, (y[i] + vy[i] * t) % H; c = (int(255 * b[i]), int(170 * b[i]), int(100 * b[i]))
            d.ellipse((px - r[i], py - r[i], px + r[i], py + r[i]), fill=c)
        return im.filter(ImageFilter.GaussianBlur(1.2))
    write_mp4(frame, dur, out)


def blur_box(image, out, box, radius=14):
    """Hide AI-generated gibberish text (newspaper headers, signs). box = fractions (x0, y0, x1, y1)."""
    im = Image.open(image).convert("RGB"); b = (int(im.width * box[0]), int(im.height * box[1]), int(im.width * box[2]), int(im.height * box[3]))
    im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(radius)), b[:2]); im.save(out); print("wrote", out)


# ------------------------------------------------------------------ synthesized sounds (energy kept in 150 Hz - 6 kHz: audible on phones)
_rng = np.random.default_rng(3)
def _bp(x, lo, hi):
    X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR); X[(fr < lo) | (fr > hi)] = 0; return np.fft.irfft(X, len(x))
def _env(n, a, d): t = np.arange(n) / SR; return np.minimum(t / max(a, 1e-4), 1) * np.exp(-t / d)
def _save(folder, name, a):
    a = a / (np.abs(a).max() or 1) * 0.9; st = np.stack([a, a], 1)
    with wave.open(os.path.join(folder, name + ".wav"), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
    print("sfx", name)


def make_sfx_foley(folder):
    """dirt_brush, bow_drill, ship_creak, waves_loud: textured foley with mid-band energy (Gemini: foley needs mid-range punch)."""
    os.makedirs(folder, exist_ok=True); r = np.random.default_rng(21)
    n = int(1.6 * SR); out = np.zeros(n)
    for k in range(5):                                   # five brush strokes over grit
        st, m = int(k * 0.3 * SR), int(0.26 * SR); tt = np.arange(m) / SR
        stroke = _bp(r.normal(size=m), 900, 7000) * np.sin(np.pi * tt / 0.26) ** 1.5
        for _ in range(18):
            g = int(r.uniform(0, m - 200)); stroke[g:g + 200] += r.uniform(0.3, 0.9) * _bp(r.normal(size=200), 2000, 8000) * np.hanning(200)
        out[st:st + m] += stroke
    _save(folder, "dirt_brush", out)
    n = int(1.4 * SR); t = np.arange(n) / SR; out = np.zeros(n)
    for k in range(6):                                   # bow strokes: squeaky pitch sweep + stone grit
        st, m = int(k * 0.22 * SR), int(0.2 * SR); tt = np.arange(m) / SR
        f = 900 + 500 * np.sin(np.pi * tt / 0.2) * (1 if k % 2 else -1) * 0.5
        squeak = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 * np.sin(np.pi * tt / 0.2)
        out[st:st + m] += squeak + 0.8 * _bp(r.normal(size=m), 1500, 6000) * np.sin(np.pi * tt / 0.2)
    _save(folder, "bow_drill", out)
    n = int(1.8 * SR); t = np.arange(n) / SR
    f = 180 + 70 * np.sin(2 * np.pi * 0.7 * t); creak = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.5 + 0.5 * np.sin(2 * np.pi * 6 * t))
    creak = _bp(creak, 200, 3000) * np.sin(np.pi * t / 1.8) ** 2
    _save(folder, "ship_creak", creak)
    n = int(3.5 * SR); t = np.arange(n) / SR
    w = _bp(r.normal(size=n), 300, 4000) * (0.2 + 0.8 * np.sin(np.pi * t / 1.75) ** 4)   # two crashing swells
    w += 0.5 * _bp(r.normal(size=n), 2500, 8000) * (np.sin(np.pi * t / 1.75) ** 8)        # foam hiss on the crest
    _save(folder, "waves_loud", w)


def make_sfx(folder):
    """train_chug, train_whistle, hammer_brick2, stone_reveal, stamp, strike, scribble, clock_tick, heartbeat_phone, paper, stone_tap, count_tick"""
    os.makedirs(folder, exist_ok=True); r = _rng
    n = int(3.2 * SR); t = np.arange(n) / SR; out = np.zeros(n)
    for k in range(13):
        st, m = int(k * 0.25 * SR), int(0.22 * SR); out[st:st + m] += (_bp(r.normal(size=m), 250, 3500) * _env(m, 0.01, 0.06) * (1.0 if k % 2 == 0 else 0.6))[: n - st]
    out += 0.35 * _bp(r.normal(size=n), 80, 400) * (0.6 + 0.4 * np.sin(2 * np.pi * 4 * t))
    for k in range(4):
        st, m = int((0.4 + k * 0.8) * SR), int(0.08 * SR); out[st:st + m] += 1.2 * _bp(r.normal(size=m), 1500, 6000) * _env(m, 0.001, 0.015)
    _save(folder, "train_chug", out * np.minimum(t / 0.3, 1) * np.minimum((3.2 - t) / 0.6, 1))
    n = int(1.7 * SR); t = np.arange(n) / SR; bend = 1 + 0.015 * np.minimum(t / 0.2, 1)
    w = sum(np.sin(2 * np.pi * f * bend * t) * g for f, g in ((440, 1), (554, 0.8), (659, 0.6), (880, 0.25))) + 0.25 * _bp(r.normal(size=n), 400, 3000)
    _save(folder, "train_whistle", w * np.minimum(t / 0.08, 1) * np.minimum((1.7 - t) / 0.5, 1))
    n = int(1.0 * SR); t = np.arange(n) / SR
    out = 1.1 * sum(np.sin(2 * np.pi * f * t) / k for k, f in ((1, 140), (2, 280), (3, 420), (4, 560))) * _env(n, 0.002, 0.07)
    m = int(0.03 * SR); out[:m] += 1.6 * _bp(r.normal(size=m), 900, 9000) * _env(m, 0.0004, 0.005)
    m2 = int(0.5 * SR); out[:m2] += 0.9 * _bp(r.normal(size=m2), 400, 5000) * _env(m2, 0.002, 0.11)
    for k in range(45):
        st, m = int(r.uniform(0.03, 0.85) * SR), int(0.025 * SR); out[st:st + m] += r.uniform(0.15, 0.55) * _bp(r.normal(size=m), 1200, 7000) * _env(m, 0.0004, 0.005)
    _save(folder, "hammer_brick2", out)
    n = int(2.2 * SR); t = np.arange(n) / SR
    out = sum(g * np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, g, d in ((196, 1, 0.9), (311, 0.7, 0.7), (467, 0.5, 0.55), (742, 0.35, 0.4), (1180, 0.2, 0.25)))
    m = int(0.05 * SR); out[:m] += _bp(r.normal(size=m), 300, 3000) * _env(m, 0.0005, 0.01); _save(folder, "stone_reveal", out * np.minimum(t / 0.004, 1))
    n = int(0.6 * SR); t = np.arange(n) / SR
    _save(folder, "stamp", sum(np.sin(2 * np.pi * f * t) / k for k, f in ((1, 110), (2, 220), (3, 330), (5, 550))) * _env(n, 0.001, 0.05) + 0.8 * _bp(r.normal(size=n), 700, 6000) * _env(n, 0.0005, 0.02))
    n = int(0.35 * SR); t = np.arange(n) / SR; _save(folder, "strike", _bp(r.normal(size=n), 1500, 7000) * np.minimum(t / 0.02, 1) * np.exp(-t / 0.15))
    n = int(0.9 * SR); t = np.arange(n) / SR
    _save(folder, "scribble", _bp(r.normal(size=n), 2000, 9000) * (0.4 + 0.6 * np.abs(np.sin(2 * np.pi * 7 * t))) * np.minimum(t / 0.03, 1) * np.minimum((0.9 - t) / 0.1, 1))
    n = int(2.1 * SR); out = np.zeros(n)
    for k in range(4):
        st, m = int(k * 0.5 * SR), int(0.05 * SR); f = 3200 if k % 2 == 0 else 2400; tt = np.arange(m) / SR
        out[st:st + m] += (np.sin(2 * np.pi * f * tt) + 0.6 * _bp(r.normal(size=m), 2000, 8000)) * _env(m, 0.0003, 0.006)
    _save(folder, "clock_tick", out)
    n = int(1.6 * SR); out = np.zeros(n)
    for k in range(16):
        st, m = int(k * 0.1 * SR), int(0.03 * SR); tt = np.arange(m) / SR; out[st:st + m] += np.sin(2 * np.pi * (1800 + 40 * k) * tt) * _env(m, 0.0003, 0.006)
    _save(folder, "count_tick", out)
    n = int(1.4 * SR); out = np.zeros(n)
    for st_s, g in ((0, 1), (0.28, 0.7)):
        st, m = int(st_s * SR), int(0.25 * SR); tt = np.arange(m) / SR
        out[st:st + m] += g * sum(np.sin(2 * np.pi * f * tt) / h for h, f in ((1, 55), (2, 110), (3, 165), (4, 220), (6, 330))) * _env(m, 0.004, 0.05)
    _save(folder, "heartbeat_phone", out)
    n = int(0.7 * SR); t = np.arange(n) / SR
    _save(folder, "paper", _bp(r.normal(size=n), 1500, 9000) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 9 * t))) * np.minimum(t / 0.05, 1) * np.minimum((0.7 - t) / 0.2, 1))
    n = int(0.4 * SR); tt = np.arange(n) / SR
    _save(folder, "stone_tap", (np.sin(2 * np.pi * 1900 * tt) + 0.7 * np.sin(2 * np.pi * 2730 * tt)) * _env(n, 0.0005, 0.03) + 0.6 * _bp(r.normal(size=n), 1000, 8000) * _env(n, 0.0003, 0.005))
