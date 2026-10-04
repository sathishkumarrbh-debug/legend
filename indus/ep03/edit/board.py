"""Code-built signboard clips for Indus Files #3 (ten real Dholavira signs, Siyajkak drawing)."""
import sys, math, numpy as np, cv2
sys.path.insert(0, "..")
import fxkit as fx
from PIL import Image, ImageDraw, ImageFilter
W, H = fx.W, fx.H
rng = np.random.default_rng(3)
MASKS = list(np.load("images/sign_masks.npy", allow_pickle=True))

def noise(w, h, scale, seed):
    r = np.random.default_rng(seed); a = r.random((h // scale + 2, w // scale + 2)).astype(np.float32)
    return cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)

def gypsum(mask, hpx):
    """RGBA gypsum piece of height hpx: chalky white, soft bevel, grain."""
    s = hpx / mask.shape[0]; m = cv2.resize(mask, (max(2, int(mask.shape[1] * s)), hpx), interpolation=cv2.INTER_AREA)
    m = np.pad(m, 8); a = (m > 110).astype(np.uint8)
    dist = cv2.distanceTransform(a, cv2.DIST_L2, 5); dist = np.clip(dist / max(2, hpx * 0.03), 0, 1)
    gx = cv2.Sobel(dist, cv2.CV_32F, 1, 0); gy = cv2.Sobel(dist, cv2.CV_32F, 0, 1)
    shade = 0.82 + 0.18 * dist - 0.25 * (gx + gy)
    g = noise(a.shape[1], a.shape[0], 3, hpx) * 0.10 + noise(a.shape[1], a.shape[0], 1, hpx + 1) * 0.06
    v = np.clip(shade - g, 0.45, 1.05)
    rgb = np.stack([238 * v, 232 * v, 218 * v], -1)
    alpha = cv2.GaussianBlur(a.astype(np.float32) * 255, (3, 3), 0)
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), alpha]).astype(np.uint8), "RGBA")

def wood(w, h, seed=5):
    y = np.linspace(0, 1, h)[:, None]; x = np.linspace(0, 1, w)[None, :]
    n = noise(w, h, 40, seed); fine = noise(w, h, 4, seed + 1)
    grain = np.sin((y * 38 + n * 3.2) * math.pi * 2) * 0.5 + 0.5
    v = 0.55 + 0.22 * grain + 0.15 * fine - 0.2 * np.abs(y - 0.5)
    rgb = np.stack([96 * v, 60 * v, 32 * v], -1)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))

def dirt(w, h, seed=9):
    n = noise(w, h, 60, seed) * 0.5 + noise(w, h, 8, seed + 1) * 0.3 + noise(w, h, 2, seed + 2) * 0.2
    rgb = np.stack([118 * n + 40, 86 * n + 30, 58 * n + 20], -1)
    im = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im); r = np.random.default_rng(seed)
    for _ in range(int(w * h / 2500)):
        x, y, rr = r.integers(0, w), r.integers(0, h), r.integers(2, 9); c = int(r.integers(70, 150))
        d.ellipse([x - rr, y - rr * 0.7, x + rr, y + rr * 0.7], fill=(c, int(c * 0.8), int(c * 0.6)))
    return im.filter(ImageFilter.GaussianBlur(0.8))

def shadowed(base, piece, xy, off=(6, 10), blur=8, op=150):
    sh = Image.new("RGBA", piece.size, (0, 0, 0, 0)); sh.putalpha(piece.getchannel("A").point(lambda v: v * op // 255))
    sh = sh.filter(ImageFilter.GaussianBlur(blur)); base.alpha_composite(sh, (xy[0] + off[0], xy[1] + off[1]))
    base.alpha_composite(piece, xy)

def row_layout(hpx, gap):
    pcs = [gypsum(m, hpx) for m in MASKS]; total = sum(p.width for p in pcs) + gap * 9
    return pcs, total

def vignette(im, k=0.55):
    y, x = np.ogrid[:H, :W]; d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    v = np.clip(1 - k * d ** 2, 0.15, 1)[..., None]; a = np.asarray(im.convert("RGB")).astype(np.float32) * v
    return Image.fromarray(a.astype(np.uint8))

F_LAB = fx.font(fx.F_TITLE, 52); F_NUM = fx.font(fx.F_BIG, 120)

def label(d, text, y, alpha=255, color=fx.GOLD, f=F_LAB):
    fx.outlined(d, (W // 2, y), text, f, color + (alpha,), stroke=4)

# ---------------------------------------------------------------- 1. one sign rises + ruler comparison (line 2)
def clip_size(out="images/sign_size.mp4", dur=4.8):
    bg = dirt(W, H, 21); piece = gypsum(MASKS[0], 600)
    def frame(t):
        im = bg.copy().convert("RGBA")
        k = fx.ease(t / 0.7); y0 = int(H * 0.52 - piece.height / 2 + (1 - k) * 260)
        sc = 0.92 + 0.08 * k; p = piece.resize((int(piece.width * sc), int(piece.height * sc)), Image.LANCZOS)
        p.putalpha(p.getchannel("A").point(lambda v: int(v * min(1, t / 0.35))))
        x0 = 90
        shadowed(im, p, (x0, y0), (14, 22), 18, 170)
        d = ImageDraw.Draw(im)
        # height marker beside the sign = 37 cm; ruler = 30 cm
        if t > 1.0:
            a = int(255 * fx.ease((t - 1.0) / 0.4)); top, bot = y0, y0 + p.height; xm = x0 + p.width + 50
            d.line([(xm, top), (xm, bot)], fill=fx.GOLD + (a,), width=6)
            for yy in (top, bot): d.line([(xm - 22, yy), (xm + 22, yy)], fill=fx.GOLD + (a,), width=6)
            fx.outlined(d, (xm + 30, (top + bot) // 2), "37 CM", fx.font(fx.F_BIG, 70), fx.GOLD + (a,), anchor="lm", stroke=4)
        if t > 1.9:
            k2 = fx.ease((t - 1.9) / 0.5); rh = int(p.height * 30 / 37); xr = W - 110
            rb = y0 + p.height; rt = rb - rh; ry = int(rt + (1 - k2) * 400)
            d.rounded_rectangle([xr - 34, ry, xr + 34, ry + rh], 8, fill=(226, 196, 92, int(255 * k2)), outline=(60, 40, 10, int(255 * k2)), width=3)
            for i in range(31):
                yy = ry + rh - int(rh * i / 30); L = 26 if i % 10 == 0 else (16 if i % 5 == 0 else 9)
                d.line([(xr - 34, yy), (xr - 34 + L, yy)], fill=(50, 35, 10, int(255 * k2)), width=2)
            fx.outlined(d, (xr - 40, ry + rh + 50), "RULER 30 CM", fx.font(fx.F_BIG, 46), fx.WHITE + (int(255 * k2),), stroke=3)
        return vignette(im)
    fx.write_mp4(frame, dur, out)

# ---------------------------------------------------------------- 2. board at the gate, then falls face down (lines 3-4)
def make_board(hpx=118, gap=16, pad=34):
    pcs, total = row_layout(hpx, gap)
    bw, bh = total + pad * 2, hpx + pad * 2
    b = wood(bw, bh).convert("RGBA"); x = pad
    for p in pcs:
        shadowed(b, p, (x, pad + (hpx - p.height) // 2 + 4), (3, 5), 4, 160); x += p.width + gap
    d = ImageDraw.Draw(b); d.rectangle([0, 0, bw - 1, bh - 1], outline=(40, 24, 10, 255), width=6)
    return b, pcs

def gate_bg():
    """Simple stone gate wall (dark, code-drawn) used if no AI gate image is passed."""
    im = Image.new("RGB", (W, H), (34, 30, 26)); d = ImageDraw.Draw(im); r = np.random.default_rng(4)
    for row in range(0, H, 70):
        off = (row // 70) % 2 * 60
        for col in range(-120 + off, W, 120):
            c = int(r.integers(50, 78)); d.rectangle([col + 3, row + 3, col + 117, row + 67], fill=(c + 10, c + 2, c - 8))
    d.rectangle([W // 2 - 230, int(H * 0.55), W // 2 + 230, H], fill=(10, 8, 6))
    return im.filter(ImageFilter.GaussianBlur(1.2))

def clip_board(out="images/board_fall.mp4", bg_image=None, dur=8.0, t_fall=3.2):
    board, pcs = make_board()
    s = (W - 40) / board.width; board = board.resize((int(board.width * s), int(board.height * s)), Image.LANCZOS)
    bg = fx.cover(Image.open(bg_image).convert("RGB")) if bg_image else gate_bg()
    floor = dirt(W, H, 33)
    by = int(H * 0.40)
    # signs lying in the dirt (same order), for after the fall
    lying = floor.copy().convert("RGBA"); x = 20 + int(34 * s)
    for p in pcs:
        q = p.resize((int(p.width * s), int(p.height * s)), Image.LANCZOS)
        shadowed(lying, q, (x, int(H * 0.5) - q.height // 2), (2, 4), 3, 140); x += q.width + int(16 * s)
    woodlay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); woodlay.alpha_composite(board, ((W - board.width) // 2, int(H * 0.5) - board.height // 2))
    back = wood(board.width, board.height, 8).convert('RGBA'); woodonly = Image.new('RGBA', (W, H), (0, 0, 0, 0)); woodonly.alpha_composite(back, ((W - board.width) // 2, int(H * 0.5) - board.height // 2))
    def frame(t):
        if t < t_fall:  # standing on the gate, slow push in
            z = 1 + 0.06 * t / t_fall; im = bg.resize((int(W * z), int(H * z)), Image.LANCZOS)
            im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H)).convert("RGBA")
            shadowed(im, board, ((W - board.width) // 2, by), (8, 16), 12, 190)
            return vignette(im, 0.6)
        u = t - t_fall
        if u < 0.55:  # tipping toward camera: height grows, darkens
            k = (u / 0.55) ** 2; im = bg.copy().convert("RGBA")
            hh = int(board.height * (1 + 6 * k)); bb = board.resize((board.width, hh)).point(lambda v: int(v * (1 - 0.8 * k)))
            im.alpha_composite(bb, ((W - board.width) // 2, by + board.height - hh // 2))
            return vignette(im, 0.6)
        if u < 0.75: return Image.new("RGB", (W, H), (8, 6, 4))  # impact
        v = u - 0.75  # lying in the dirt: wood rots away, signs remain in order
        im = lying.copy(); rot = fx.ease((v - 0.6) / 2.2)
        if rot < 1:
            wl = woodonly.copy(); wl.putalpha(wl.getchannel("A").point(lambda a: int(a * (1 - rot))))
            # wood is above the signs only while it lasts (we see its back after the fall): signs show through as it rots
            im.alpha_composite(wl)
        z = 1.0 + 0.05 * fx.ease(v / 4); im = im.resize((int(W * z), int(H * z)), Image.LANCZOS)
        im = im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))
        sh = int(18 * math.exp(-v * 6) * math.sin(v * 60)); im = im.transform(im.size, Image.AFFINE, (1, 0, 0, 0, 1, sh))
        return vignette(im, 0.5)
    fx.write_mp4(frame, dur, out)

# ---------------------------------------------------------------- 3. all ten lit one by one (line 5)
def clip_lit(out="images/signs_lit.mp4", dur=4.6, text=("MAYBE THE OLDEST", "SIGNBOARD EVER FOUND")):
    pcs, total = row_layout(150, 18); s = (W - 60) / total
    pcs = [p.resize((int(p.width * s), int(p.height * s)), Image.LANCZOS) for p in pcs]
    base = Image.new("RGBA", (W, H), (10, 8, 6, 255)); y = int(H * 0.47)
    def frame(t):
        im = base.copy(); glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); x = 30
        for i, p in enumerate(pcs):
            k = fx.ease((t - 0.15 - i * 0.12) / 0.25)
            if k > 0:
                q = p.copy(); q.putalpha(q.getchannel("A").point(lambda a: int(a * k)))
                g = Image.new("RGBA", p.size, fx.GOLD + (0,)); g.putalpha(p.getchannel("A").point(lambda a: int(a * k * 0.9)))
                glow.alpha_composite(g, (x, y - p.height // 2)); im.alpha_composite(q, (x, y - p.height // 2))
            x += p.width + int(18 * s)
        im = Image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(22)), im) if t > 0.15 else im
        im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(8)).point(lambda v: v // 2))
        d = ImageDraw.Draw(im)
        if t > 1.6:
            for j, ln in enumerate(text): label(d, ln, int(H * 0.60) + j * 70, int(255 * fx.ease((t - 1.6) / 0.4)))
        return vignette(im, 0.4)
    fx.write_mp4(frame, dur, out)

if __name__ == "__main__":
    which = sys.argv[1:] or ["size", "board", "lit"]
    if "size" in which: clip_size()
    if "board" in which: clip_board()
    if "lit" in which: clip_lit()
