"""Replace AI-invented symbols with the real ten Dholavira signs (code-rendered gypsum)."""
import sys, numpy as np, cv2
sys.path.insert(0, ".")
from PIL import Image, ImageFilter
import board as B

def inpaint_white(img, poly, thr=150, grow=9, keep=None):
    a = np.asarray(img.convert("RGB")).copy(); g = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    region = np.zeros(a.shape[:2], np.uint8); cv2.fillPoly(region, [np.array(poly, np.int32)], 1)
    if keep is not None:
        for kp in keep: cv2.fillPoly(region, [np.array(kp, np.int32)], 0)
    bright = ((g[..., 2] > thr) & (g[..., 1] < 110)).astype(np.uint8) & region
    m = cv2.dilate(bright, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (grow * 2 + 1, grow * 2 + 1)))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))) & region
    out = cv2.inpaint(a, m * 255, 25, cv2.INPAINT_TELEA)
    # re-grain the filled area with dirt texture sampled from the image
    noise = np.random.default_rng(1).normal(0, 9, a.shape).astype(np.float32)
    mm = cv2.GaussianBlur(m.astype(np.float32), (31, 31), 0)[..., None]
    out = np.clip(out + noise * mm, 0, 255).astype(np.uint8)
    return Image.fromarray(out), m

def lay_row(img, near, far, h_near, h_far, squash=0.55, order=range(10), shade=1.0):
    """Ten real signs lying in the dirt in a row from `near` (big) to `far` (small)."""
    im = img.convert("RGBA"); n = 10
    for k, i in enumerate(order):
        t = k / (n - 1); x = near[0] + (far[0] - near[0]) * t; y = near[1] + (far[1] - near[1]) * t
        h = int(h_near + (h_far - h_near) * t)
        p = B.gypsum(B.MASKS[i], h); p = p.resize((p.width, max(4, int(p.height * squash))), Image.LANCZOS)
        if shade != 1.0:
            r, g, b, al = p.split(); p = Image.merge("RGBA", [c.point(lambda v: int(v * shade)) for c in (r, g, b)] + [al])
        B.shadowed(im, p, (int(x - p.width / 2), int(y - p.height / 2)), (int(h * 0.04), int(h * 0.06)), max(2, h // 25), 170)
    return im.convert("RGB")

def board_on_quad(img, quad, glow=0.0):
    """Warp the code-built board (real signs) onto the AI board's 4 corners (tl, tr, br, bl)."""
    bd, _ = B.make_board(hpx=150, gap=22, pad=40); bd = np.asarray(bd)
    h, w = bd.shape[:2]; src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    M = cv2.getPerspectiveTransform(src, np.float32(quad)); a = np.asarray(img.convert("RGB")).astype(np.float32)
    war = cv2.warpPerspective(bd, M, (a.shape[1], a.shape[0]), flags=cv2.INTER_LANCZOS4)
    al = war[..., 3:4].astype(np.float32) / 255
    # match lighting of the original board: scale by local brightness of the AI board
    lum = cv2.GaussianBlur(cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32), (0, 0), 25)
    ref = (lum[al[..., 0] > 0.5]).mean(); k = np.clip(lum / max(ref, 1), 0.6, 1.4)[..., None]
    col = war[..., :3].astype(np.float32) * k
    if glow:
        sig = (war[..., :3].mean(-1) > 150).astype(np.float32)[..., None] * al
        col = col + sig * glow * np.array([255, 210, 120], np.float32)
    out = a * (1 - al) + col * al
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def quilt_fill(img, mask, src_box, patch=120, seed=2):
    """Fill mask with randomly flipped dirt patches cut from src_box (real texture, no smear)."""
    a = np.asarray(img.convert("RGB")).astype(np.float32); x0, y0, x1, y1 = src_box; src = a[y0:y1, x0:x1]
    r = np.random.default_rng(seed); fill = a.copy(); H_, W_ = mask.shape; step = patch * 2 // 3
    acc = np.zeros_like(a); wsum = np.zeros(a.shape[:2] + (1,), np.float32)
    win = np.outer(np.hanning(patch), np.hanning(patch)).astype(np.float32)[..., None] + 1e-3
    ys, xs = np.where(mask > 0)
    for y in range(max(0, ys.min() - patch), ys.max() + 1, step):
        for x in range(max(0, xs.min() - patch), xs.max() + 1, step):
            sy, sx = r.integers(0, src.shape[0] - patch), r.integers(0, src.shape[1] - patch); p = src[sy:sy + patch, sx:sx + patch]
            if r.random() < .5: p = p[:, ::-1]
            hh, ww = min(patch, H_ - y), min(patch, W_ - x)
            acc[y:y + hh, x:x + ww] += p[:hh, :ww] * win[:hh, :ww]; wsum[y:y + hh, x:x + ww] += win[:hh, :ww]
    tex = acc / np.maximum(wsum, 1e-3)
    # match local mean brightness of the surroundings
    m = mask.astype(np.float32); mb = cv2.GaussianBlur(m, (0, 0), 6)[..., None]
    lo = cv2.GaussianBlur(cv2.inpaint(a.astype(np.uint8), mask * 255, 15, cv2.INPAINT_TELEA).astype(np.float32), (0, 0), 30)
    tlo = cv2.GaussianBlur(tex, (0, 0), 30); tex = tex - tlo + lo
    out = a * (1 - mb) + tex * mb
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def lay_row_persp(img, near, far, h_near, zf=3.2, squash=0.5, n=10):
    im = img.convert("RGBA"); zs = np.linspace(1, zf, n)
    for k in range(n - 1, -1, -1):  # far first so near signs overlap correctly
        z = zs[k]; u = (1 / z - 1 / zf) / (1 - 1 / zf)
        x = far[0] + (near[0] - far[0]) * u; y = far[1] + (near[1] - far[1]) * u; h = int(h_near / z)
        p = B.gypsum(B.MASKS[k], h); p = p.resize((p.width, max(4, int(p.height * squash))), Image.LANCZOS)
        B.shadowed(im, p, (int(x - p.width / 2), int(y - p.height / 2)), (max(1, h // 30), max(2, h // 18)), max(2, h // 25), 170)
    return im.convert("RGB")

def lay_row_packed(img, near, far, r=0.86, squash=0.6, gap=0.12, n=10):
    """Pack the ten signs from near to far without overlap; size shrinks by r each step; auto-fit to the strip."""
    hs = np.array([r ** k for k in range(n)]); ext = hs * squash
    steps = [(ext[k] + ext[k + 1]) / 2 + gap * hs[k] for k in range(n - 1)]
    L = abs(near[1] - far[1]); h0 = L / (sum(steps) + 0.0001)
    im = img.convert("RGBA"); pos = [0.0]
    for s_ in steps: pos.append(pos[-1] + s_ * h0)
    for k in range(n - 1, -1, -1):
        u = pos[k] / pos[-1]; x = near[0] + (far[0] - near[0]) * u; y = near[1] + (far[1] - near[1]) * u; h = int(h0 * hs[k])
        p = B.gypsum(B.MASKS[k], h); p = p.resize((p.width, max(4, int(p.height * squash))), Image.LANCZOS)
        B.shadowed(im, p, (int(x - p.width / 2), int(y - p.height / 2)), (max(1, h // 30), max(2, h // 18)), max(2, h // 25), 170)
    return im.convert("RGB")

def signs_strip(hpx=150, gap=26, pad=40):
    pcs, total = B.row_layout(hpx, gap); w, h = total + pad * 2, hpx + pad * 2
    st = Image.new("RGBA", (w, h), (0, 0, 0, 0)); x = pad
    for p in pcs: B.shadowed(st, p, (x, pad + (hpx - p.height) // 2), (3, 5), 4, 170); x += p.width + gap
    return st

def lum_match(a, al, col, ref_mask):
    lum = cv2.GaussianBlur(cv2.cvtColor(a.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32), (0, 0), 30)
    ref = np.median(lum[ref_mask > 0]) if ref_mask.any() else lum.mean()
    return col * np.clip(lum / max(ref, 1), 0.35, 1.3)[..., None]

def signs_on_quad(img, quad, poly, thr=150, glow=0.0, bright=1.0):
    """Erase the AI's invented symbols inside poly, then warp the real ten signs onto quad (tl, tr, br, bl)."""
    orig = np.asarray(img.convert("RGB")).astype(np.float32)
    clean, m = inpaint_white(img, poly, thr=thr, grow=6)
    a = np.asarray(clean).astype(np.float32); st = np.asarray(signs_strip())
    h, w = st.shape[:2]; M_ = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), np.float32(quad))
    war = cv2.warpPerspective(st, M_, (a.shape[1], a.shape[0]), flags=cv2.INTER_LANCZOS4).astype(np.float32)
    al = war[..., 3:4] / 255; col = lum_match(orig, al, war[..., :3], m) * bright
    if glow:
        g = cv2.GaussianBlur(al[..., 0] * (war[..., :3].mean(-1) > 120), (0, 0), 9)[..., None]
        a = a + g * glow * np.array([255, 205, 120], np.float32)
    out = a * (1 - al) + col * al
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def lay_row_line(img, p_far, p_near, mask, size_ratio=1.8, squash=0.8, gap=0.10, rot=0.0, bright=1.0, bold=0):
    """Ten real signs along a straight line, growing toward p_near; spacing uses each sign's projected extent; auto-fit."""
    a0 = np.asarray(img.convert("RGB")).astype(np.float32)
    d = np.array(p_near, float) - np.array(p_far, float); L = np.linalg.norm(d); u = d / L
    rel = np.linspace(1.0, size_ratio, 10)
    probe = [B.gypsum(B.MASKS[k], 200) for k in range(10)]  # extents from undilated masks
    ext = [max(pp.width / 200 * abs(u[0]), squash * abs(u[1])) for pp in probe]   # extent along the line per unit height
    steps = [(ext[k] * rel[k] + ext[k + 1] * rel[k + 1]) / 2 + gap * rel[k] for k in range(9)]
    h0 = L / sum(steps); pos = np.concatenate([[0], np.cumsum(steps) * h0])
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    for k in range(10):
        c = np.array(p_far) + u * pos[k]; hh = int(h0 * rel[k])
        mk = B.MASKS[k]
        if bold: mk = cv2.dilate(mk, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (bold, bold)))
        p = B.gypsum(mk, hh); p = p.resize((p.width, max(4, int(p.height * squash))), Image.LANCZOS)
        if rot: p = p.rotate(rot, expand=True, resample=Image.BICUBIC)
        B.shadowed(layer, p, (int(c[0] - p.width / 2), int(c[1] - p.height / 2)), (max(1, hh // 30), max(2, hh // 16)), max(2, hh // 22), 180)
    la = np.asarray(layer).astype(np.float32); al = la[..., 3:4] / 255
    col = lum_match(a0, al, la[..., :3], mask) * bright
    return Image.fromarray(np.clip(a0 * (1 - al) + col * al, 0, 255).astype(np.uint8))

def clone_fill(img, mask, shift, feather=15):
    """Fill mask with the image itself shifted by `shift` (dx, dy): real texture in the same light; low frequencies matched."""
    a = np.asarray(img.convert("RGB")).astype(np.float32); dx, dy = shift
    src = np.roll(np.roll(a, -dy, 0), -dx, 1)
    lo_a = cv2.GaussianBlur(cv2.inpaint(a.astype(np.uint8), mask * 255, 15, cv2.INPAINT_TELEA).astype(np.float32), (0, 0), 25)
    lo_s = cv2.GaussianBlur(src, (0, 0), 25); tex = src - lo_s + lo_a
    mb = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), feather)[..., None]; mb = np.clip(mb * 1.6, 0, 1)
    return Image.fromarray(np.clip(a * (1 - mb) + tex * mb, 0, 255).astype(np.uint8))
