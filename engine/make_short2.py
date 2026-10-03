#!/usr/bin/env python3
"""
make_short2.py - timeline editor for cinematic Shorts (several shots per line, overlays, word-anchored cuts).

    python3 make_short2.py <episode> --voice take1.mp3 [take2.mp3 ...] [--tempo 1.05] [--preview]

scenes.json (v2):
  lines:    [{"text": "...", "caption": optional, "emph": ["word", ...]}]
  shots:    [{"line": i, "at": 0.0 | "word:fire" | "frac:0.5" | "end:-0.3", "src": "x.png" | "clip.mp4" | "black",
              "move": in|out|left|right|up|down|punch|still, "focus": [x,y], "fit": cover|fit,
              "z": [z0, z1], "clip_start": s, "speed": 1, "bright": [b0, b1], "xfade": 0.3,
              "overlays": [{"src": "fire.mp4", "mode": "screen"|"normal", "opacity": 0.8, "clip_start": 0,
                            "scale": 1.0, "pos": [cx, cy], "fade": [in_s, out_s], "speed": 1}],
              "label": "ORAL TRADITION", "label_dur": 1.5, "ai": true, "flash": true, "shake": true,
              "fade_out_black": 0.6}]
  sfx:      [{"line": i, "at": ..., "name": "hit_big", "db": -6, "anchor": "start"|"end"}]
  music:    [{"src": "../music/x.mp3", "offset": 0, "line": 0, "at": 0, "gap_db": 6, "xfade": 1.0}]
  line_times (optional): [[s, e], ...] to skip automatic alignment
"""
import argparse, json, math, os, re, subprocess, sys, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_short as M

W, H, FPS, SR = M.W, M.H, M.FPS, M.SR
FONT_CAP = M.FONT_CAP
FONT_T = M.FONT_TITLE
GOLD = (255, 197, 61, 255)
WHITE = (255, 255, 255, 255)


# ------------------------------------------------------------ timing
def resolve(anchor, line_i, lines_t, words_t):
    s, e = lines_t[line_i]
    if isinstance(anchor, (int, float)):
        return s + anchor
    a = str(anchor)
    if a.startswith("word:"):
        tgt, off = a[5:], 0.0
        if "@" in tgt:
            tgt, off = tgt.split("@"); off = float(off)
        n = 1
        if "#" in tgt:
            tgt, n = tgt.split("#"); n = int(n)
        hits = [w for w in words_t[line_i] if re.sub(r"[^\w]", "", w[0].lower()) == tgt.lower()]
        if len(hits) >= n:
            return hits[n - 1][1] + off
        print(f"   ! word '{tgt}' not found in line {line_i+1}"); return s + off
    if a.startswith("frac:"):
        return s + (e - s) * float(a[5:])
    if a.startswith("end:"):
        return e + float(a[4:])
    if a.startswith("abs:"):
        return float(a[4:])
    return s


# ------------------------------------------------------------ media
class Clip:
    def __init__(self, path, start=0.0, speed=1.0, size=(W, H), fit="cover"):
        self.path, self.start, self.speed, self.size, self.fit = path, start, speed, size, fit
        self.proc, self.idx, self.frame = None, -1, None

    def _open(self):
        w, h = self.size
        vf = (f"setpts=(PTS-STARTPTS)/{self.speed},fps={FPS},scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}")
        self.proc = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(self.start), "-stream_loop", "-1", "-i", self.path,
                                      "-an", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.idx = -1

    def at(self, lt):
        want = max(0, int(lt * FPS))
        if self.proc is None or want < self.idx:
            if self.proc: self.proc.kill()
            self._open()
        w, h = self.size
        while self.idx < want:
            buf = self.proc.stdout.read(w * h * 3)
            if len(buf) < w * h * 3:
                break
            self.frame = Image.frombytes("RGB", (w, h), buf); self.idx += 1
        return self.frame if self.frame is not None else Image.new("RGB", (w, h))

    def close(self):
        if self.proc: self.proc.kill(); self.proc = None


def grade_still(im):
    """Consistent film look for stills: slight contrast, a touch less saturation (tames orange)."""
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(0.92)
    return im


def camera(im, p, move, focus, z=None, t=0.0, hh=0.0):
    p = 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, p)))
    iw, ih = im.size
    base = min(iw / W, ih / H)
    fx, fy = focus
    if z:
        z0, z1 = z
    else:
        z0, z1 = {"in": (1.0, 1.12), "out": (1.12, 1.0), "punch": (1.0, 1.25), "still": (1.02, 1.03)}.get(move, (1.08, 1.08))
    if move == "punch" and not z:
        q = min(1.0, p / 0.12); zz = 1.0 + 0.18 * (1 - (1 - q) ** 3) + 0.06 * p
    else:
        zz = z0 + (z1 - z0) * p
    cw, ch = W * base / zz, H * base / zz
    if move in ("left", "right"):
        a, b = (0.25, 0.75) if move == "right" else (0.75, 0.25)
        cx = cw / 2 + (iw - cw) * (a + (b - a) * p); cy = fy * ih
    elif move in ("up", "down"):
        a, b = (0.7, 0.3) if move == "up" else (0.3, 0.7)
        cy = ch / 2 + (ih - ch) * (a + (b - a) * p); cx = fx * iw
    else:
        cx, cy = fx * iw, fy * ih
    if hh:   # gentle handheld drift (pixels of output)
        k = base / zz
        cx += hh * k * (math.sin(t * 1.3) + 0.5 * math.sin(t * 3.1 + 1)); cy += hh * k * (math.cos(t * 1.1) + 0.5 * math.sin(t * 2.7))
    cx = min(max(cx, cw / 2), iw - cw / 2); cy = min(max(cy, ch / 2), ih - ch / 2)
    return im.resize((W, H), Image.BICUBIC, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))


def load_still(path, fit):
    im = Image.open(path).convert("RGB")
    if fit == "fit" or (fit == "auto" and im.width / im.height > 0.8):
        bg = im.copy()
        s = max(W * 1.25 / bg.width, H * 1.25 / bg.height)
        bg = bg.resize((int(bg.width * s), int(bg.height * s)), Image.LANCZOS)
        bg = bg.crop(((bg.width - int(W * 1.25)) // 2, (bg.height - int(H * 1.25)) // 2,
                      (bg.width + int(W * 1.25)) // 2, (bg.height + int(H * 1.25)) // 2))
        bg = bg.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.4))
        fg_w = int(W * 1.25 * 0.94)
        fg = im.resize((fg_w, int(im.height * fg_w / im.width)), Image.LANCZOS)
        if fg.height > bg.height * 0.8:
            fg_h = int(bg.height * 0.8); fg = im.resize((int(im.width * fg_h / im.height), fg_h), Image.LANCZOS)
        bg.paste(fg, ((bg.width - fg.width) // 2, int(bg.height * 0.42 - fg.height / 2)))
        im = bg
    s = max(W * 1.3 / im.width, H * 1.3 / im.height)
    if s > 1:
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return grade_still(im)


# ------------------------------------------------------------ layers
def vignette():
    y, x = np.mgrid[0:H, 0:W]
    r = np.sqrt(((x - W / 2) / (W * 0.72)) ** 2 + ((y - H / 2) / (H * 0.68)) ** 2)
    a = np.clip((r - 0.5) * 1.5, 0, 0.8)
    band = np.exp(-((y - H * 0.66) / (H * 0.10)) ** 2) * 0.28
    alpha = np.clip(a + band, 0, 0.88)
    ov = np.zeros((H, W, 4), np.uint8); ov[..., 3] = (alpha * 255).astype(np.uint8)
    return Image.fromarray(ov, "RGBA")


_grain = [np.random.default_rng(k).normal(0, 7, (H // 2, W // 2)).astype(np.int16) for k in range(6)]

def add_grain(fr, f):
    a = np.asarray(fr, np.int16)
    g = np.repeat(np.repeat(_grain[f % 6], 2, 0), 2, 1)[..., None]
    return Image.fromarray(np.clip(a + g, 0, 255).astype(np.uint8))


def caption_layer(words, active, emph, size=100):
    font = ImageFont.truetype(FONT_CAP, size)
    fonts = [ImageFont.truetype(FONT_CAP, int(size * 1.22)) if e else font for e in emph]
    sp = size * 0.26
    widths = [f.getlength(w) for f, w in zip(fonts, words)]
    total = sum(widths) + sp * (len(words) - 1)
    if total > W * 0.86:
        return caption_layer(words, active, emph, int(size * W * 0.86 / total))
    img = Image.new("RGBA", (W, int(size * 2.1)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = (W - total) / 2
    for i, (w, wd, f, e) in enumerate(zip(words, widths, fonts, emph)):
        col = GOLD if e else WHITE
        y = size * 0.25 - (f.size - size) * 0.8
        d.text((x + 4, y + 6), w, font=f, fill=(0, 0, 0, 150))                  # soft shadow
        d.text((x, y), w, font=f, fill=col, stroke_width=max(5, f.size // 16), stroke_fill=(0, 0, 0, 255))
        x += wd + sp
    return img


def label_layer(text, size=40):
    f = ImageFont.truetype(FONT_T, size)
    tw = f.getlength(text)
    img = Image.new("RGBA", (int(tw + 64), int(size * 2)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, img.width - 1, img.height - 1), 10, fill=(0, 0, 0, 140))
    d.line([(20, img.height - 10), (img.width - 20, img.height - 10)], fill=GOLD, width=3)
    d.text((32, size * 0.35), text, font=f, fill=(245, 235, 215, 255))
    return img


def headline_layer(text, size=118, color=(255, 255, 255, 255), accent=None):
    """Big on-screen text (hook / key facts). Lines split on '\n'; words in accent list are gold."""
    lines = text.split("\n")
    font = ImageFont.truetype(FONT_CAP, size)
    wmax = max(font.getlength(l) for l in lines)
    if wmax > W * 0.9:
        return headline_layer(text, int(size * W * 0.9 / wmax), color, accent)
    img = Image.new("RGBA", (W, int(size * 1.18 * len(lines) + size * 0.5)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = size * 0.15
    for l in lines:
        x = (W - font.getlength(l)) / 2
        for w in l.split(" "):
            col = GOLD if accent and w.strip("?!.,").upper() in accent else color
            d.text((x + 5, y + 7), w, font=font, fill=(0, 0, 0, 160))
            d.text((x, y), w, font=font, fill=col, stroke_width=max(6, size // 14), stroke_fill=(0, 0, 0, 255))
            x += font.getlength(w + " ")
        y += size * 1.18
    return img


def ai_tag():
    f = ImageFont.truetype(FONT_T, 26)
    t = "ARTIST'S IMPRESSION"
    img = Image.new("RGBA", (int(f.getlength(t) + 30), 44), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((15, 8), t, font=f, fill=(255, 255, 255, 150), stroke_width=2, stroke_fill=(0, 0, 0, 120))
    return img


def fade_alpha(layer, a):
    if a >= 1: return layer
    l = layer.copy(); l.putalpha(l.getchannel("A").point(lambda v: int(v * max(0, a)))); return l


# ------------------------------------------------------------ audio
def build_music(segs, total, work, vclean):
    """Concatenate music sections with crossfades, level each against the voice in the phone band."""
    v = M.band_rms_db(vclean, active_only=True)
    n = int((total + 1) * SR); out = np.zeros((n, 2), np.float32)
    for k, sg in enumerate(segs):
        t0 = sg["t"]; t1 = segs[k + 1]["t"] if k + 1 < len(segs) else total + 1
        xf = sg.get("xfade", 1.0)
        src = sg["src"]
        m = M.band_rms_db(src, M.PHONE_BAND + "," + M.MUSIC_EQ, start=sg.get("offset", 0), dur=max(3, t1 - t0))
        gain = v - sg.get("gap_db", 6.0) - m + sg.get("trim_db", 0)
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(sg.get("offset", 0)), "-t", str(t1 - t0 + xf + 0.5),
                              "-i", src, "-af", M.MUSIC_EQ + f",volume={gain}dB", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                             capture_output=True).stdout
        a = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
        fin = int((xf if k > 0 else sg.get("fade_in", 0.3)) * SR)
        if fin: a[:fin] *= np.linspace(0, 1, fin)[:, None]
        L = int((t1 - t0 + (xf if k + 1 < len(segs) else 0)) * SR); a = a[:L]
        if k + 1 < len(segs):
            fo = int(segs[k + 1].get("xfade", 1.0) * SR); a[-fo:] *= np.linspace(1, 0, fo)[:, None]
        st = int(max(0, t0 - (xf if k > 0 else 0) * 0) * SR)
        e = min(n, st + len(a)); out[st:e] += a[: e - st]
        print(f"   music {k}: {os.path.basename(src)} from {sg.get('offset',0)}s at {t0:.2f}s gain {gain:+.1f} dB")
    p = os.path.join(work, "music_bed.wav")
    import wave
    with wave.open(p, "wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes((np.clip(out[: int(total * SR)], -1, 1) * 32767).astype(np.int16).tobytes())
    return p


def final_mix(voice, music, sfx, total, dst, fade_out=1.0):
    fc = (f"[0:a]apad[v];[1:a]apad[m];[2:a]alimiter=limit=0.85:attack=1:release=60:level=false,apad[fx];"
          f"[v][m][fx]amix=inputs=3:duration=first:normalize=0,atrim=0:{total:.3f},"
          f"alimiter=limit=0.95:attack=5:release=200:level=false,afade=t=out:st={total-fade_out:.3f}:d={fade_out}[out]")
    M.run(["ffmpeg", "-y", "-i", voice, "-i", music, "-i", sfx, "-filter_complex", fc, "-map", "[out]",
           "-ar", str(SR), "-ac", "2", dst])
    # loudness to about -14 LUFS
    tmp = dst + ".ln.wav"
    M.run(["ffmpeg", "-y", "-i", dst, "-af", "loudnorm=I=-14:TP=-1.2:LRA=11", "-ar", str(SR), tmp]); os.replace(tmp, dst)


# ------------------------------------------------------------ main
HEARD = {}   # segment start (rounded) -> number of words the ASR heard there

def word_times_snap(text, group):
    """Like make_short.word_times, but each pause in the voice (gap between speech segments) is snapped
    to a word boundary, preferring words that end in punctuation; words are then spread inside each
    segment by length. Fixes captions running ahead when a phrase is spoken slowly (e.g. years)."""
    words = text.split()
    segs = [(s, e) for s, e in group]
    if len(segs) <= 1 or len(words) < len(segs):
        return M.word_times(text, group)
    w = [len(re.sub(r"[^\w]", "", x)) + 1.5 for x in words]
    tw = sum(w); C = np.cumsum(w) / tw
    dur = [e - s for s, e in segs]; T = np.cumsum(dur) / sum(dur)
    m, n = len(words), len(segs)
    punct = [bool(re.search(r"[,.;:!?…]$", x)) for x in words]
    hc = [HEARD.get(round(a, 2)) for a, _ in segs]
    def cnt_cost(i, j0, k):   # words assigned to segment i = j0..k vs ASR count
        return 0.0 if hc[i] is None else 0.004 * ((k - j0 + 1) - hc[i]) ** 2
    INF = 1e9
    # best[i][k]: cost when segment i ends after word k
    best = [[INF] * m for _ in range(n)]; back = [[-1] * m for _ in range(n)]
    for k in range(m - n + 1):
        best[0][k] = (C[k] - T[0]) ** 2 + (0 if punct[k] else 0.01) + cnt_cost(0, 0, k)
    for i in range(1, n - 1):
        for k in range(i, m - (n - 1 - i)):
            c = (C[k] - T[i]) ** 2 + (0 if punct[k] else 0.01)
            for j in range(i - 1, k):
                cc = best[i - 1][j] + c + cnt_cost(i, j + 1, k)
                if cc < best[i][k]:
                    best[i][k] = cc; back[i][k] = j
    # last segment must end at the last word
    k_last = m - 1; bk = min(range(n - 2, m - 1), key=lambda j: best[n - 2][j]);
    ends = [k_last, bk]
    for i in range(n - 2, 0, -1):
        ends.append(back[i][ends[-1]])
    ends = ends[::-1]
    out, start = [], 0
    for (s, e), k in zip(segs, ends):
        ws = w[start:k + 1]; tot = sum(ws); acc = 0
        for word, wt in zip(words[start:k + 1], ws):
            out.append((word, s + (e - s) * acc / tot, s + (e - s) * (acc + wt) / tot)); acc += wt
        start = k + 1
    return out


def caption_times(line, group):
    """Word timings for the caption text, but timed by what is SPOKEN: '1536' takes the time of
    'fifteen thirty-six', 'Dai' the time of 'Dhaai'. Unmatched caption words absorb spoken words
    up to the next matching word."""
    cap = line.get("caption", line["text"])
    spoken = word_times_snap(line["text"], group)
    if cap == line["text"]:
        return spoken
    cw = cap.split()
    norm = lambda w: re.sub(r"[^\w]", "", w.lower())
    out, j = [], 0
    for i, w in enumerate(cw):
        if j >= len(spoken):
            out.append((w, spoken[-1][2], spoken[-1][2])); continue
        if norm(w) == norm(spoken[j][0]):
            out.append((w, spoken[j][1], spoken[j][2])); j += 1; continue
        nxt = norm(cw[i + 1]) if i + 1 < len(cw) else None
        k = j + 1
        while k < len(spoken) and nxt is not None and norm(spoken[k][0]) != nxt:
            k += 1
        if nxt is None:
            k = len(spoken)
        if k > len(spoken) or (nxt is not None and k == len(spoken)):
            k = j + 1      # no anchor ahead: 1:1
        out.append((w, spoken[j][1], spoken[k - 1][2])); j = k
    return out


_FD = None
def detect_faces(fr):
    """YuNet face boxes [(x0,y0,x1,y1,score)] in output pixels (models/yunet.onnx next to this script)."""
    global _FD
    import cv2
    if _FD is None:
        _FD = cv2.FaceDetectorYN.create(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "yunet.onnx"), "", (W // 2, H // 2), 0.6)
    img = cv2.cvtColor(np.asarray(fr.convert("RGB").resize((W // 2, H // 2))), cv2.COLOR_RGB2BGR)
    _, f = _FD.detect(img)
    out = []
    for r in (f if f is not None else []):
        x, y, w, h = [v * 2 for v in r[:4]]
        out.append((x, y - 0.25 * h, x + w, y + h * 1.1, float(r[-1])))   # pad up for hair/headwear, down for chin
    return out


def facecheck(shots, base_frame, plan, labels, heads, hook_layer, hook, caps, lt):
    """For each shot, sample frames without text, find faces, and report any text box over a face."""
    def ov(a, b):
        return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
    bad = 0
    for k, s in enumerate(shots):
        t0, t1 = s["_t"], s["_e"]
        boxes = []
        for t in sorted({t0 + 0.05, (t0 + t1) / 2, max(t0 + 0.05, t1 - 0.08)}):
            boxes += [(t, b) for b in detect_faces(base_frame(s, t))]
        texts = []
        cy = H * s.get("cap_y", plan.get("cap_y", 0.60))
        if any(t0 < c[1][-1][2] and c[1][0][1] < t1 for c in caps) and t1 > plan.get("captions_from", 0):
            texts.append(("caption", (W * 0.07, cy + 15, W * 0.93, cy + 200)))
        if hook_layer is not None and t0 < hook.get("until", 2.5):
            y = H * hook.get("y", 0.15); texts.append(("hook", (W * 0.05, y, W * 0.95, y + hook_layer.height)))
        if id(s) in heads:
            y = H * s.get("headline_y", 0.16); texts.append(("headline", (W * 0.08, y, W * 0.92, y + heads[id(s)].height)))
        if id(s) in labels:
            L = labels[id(s)]; y = s.get("label_y", 300); texts.append(("label", ((W - L.width) / 2, y, (W + L.width) / 2, y + L.height)))
        hits = []
        for t, b in boxes:
            for name, r in texts:
                area = (b[2] - b[0]) * (b[3] - b[1])
                if area > 0 and ov(b, r) / area > 0.12:
                    hits.append(f"{name}@{t:.1f}s face y={b[1]/H:.2f}-{b[3]/H:.2f}")
        faces = ", ".join(f"{b[1]/H:.2f}-{b[3]/H:.2f}" for _, b in boxes[:3])
        flag = "  <-- OVERLAP " + "; ".join(sorted(set(hits))) if hits else ""
        bad += bool(hits)
        print(f"   shot {k:2d} {t0:6.2f} {s['src'][:26]:26s} faces[{faces}]{flag}")
    print(f"facecheck: {bad} shot(s) with text over a face")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--voice", nargs="+")
    ap.add_argument("--tempo", type=float, default=1.0)
    ap.add_argument("--noise-db", type=float, default=-38)
    ap.add_argument("--min-pause", type=float, default=0.22)
    ap.add_argument("--preview", action="store_true", help="half resolution, fast")
    ap.add_argument("--frames", help="comma list of seconds: only export stills at those times")
    ap.add_argument("--out")
    ap.add_argument("--facecheck", action="store_true", help="detect faces per shot and report text that covers them")
    args = ap.parse_args()
    ep = os.path.abspath(args.episode)
    plan = json.load(open(os.path.join(ep, "scenes.json")))
    lines = plan["lines"]; texts = [l["text"] for l in lines]
    work = os.path.join(ep, "_work"); os.makedirs(work, exist_ok=True)
    vclean = os.path.join(work, "voice_clean.wav")
    timing_p = os.path.join(work, "line_times.json")

    if plan.get("line_times"):
        lt = plan["line_times"]
        if not os.path.exists(vclean):
            M.clean_voice(args.voice[0], vclean, args.tempo)
    elif args.voice:
        print("1 voice")
        if len(args.voice) > 1 or plan.get("best_takes"):
            best, groups = M.assemble_best_takes(args.voice, texts, work, args.noise_db, 0.18, args.tempo)
            M.clean_voice(best, vclean, 1.0)
        else:
            if plan.get("voice_light"):   # already-clean TTS: no denoise/compressor (they pop after silences)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", args.voice[0], "-af",
                                "highpass=f=80,volume=7dB,alimiter=limit=0.8:attack=7:release=120:level=disabled",
                                "-ar", str(SR), "-ac", "1", vclean], check=True)
            else:
                M.clean_voice(args.voice[0], vclean, args.tempo)
            segs, _ = M.speech_segments(vclean, args.noise_db, args.min_pause)
            tx = M.transcribe_segments(vclean, segs)
            if tx:   # split blocks holding two sentences at the sentence break
                ns, nt = [], []
                for (a, b), t_ in zip(segs, tx):
                    parts = [p.strip() for p in re.split(r"(?<=[.?!])\s+", t_) if p.strip()]
                    if len(parts) > 1 and b - a > 1.2:
                        tot = sum(len(p) for p in parts); t0 = a
                        for p in parts:
                            t1 = t0 + (b - a) * len(p) / tot
                            ns.append([t0, t1 - 0.02]); nt.append(p); t0 = t1 + 0.02
                    else:
                        ns.append([a, b]); nt.append(t_)
                segs, tx = ns, nt
            groups = M.align_by_text(segs, tx, texts) if tx else M.align(segs, texts)
            if tx:
                open(os.path.join(work, "heard.txt"), "w").write("\n".join(f"{a:6.2f}-{b:6.2f} {t}" for (a, b), t in zip(segs, tx)))
        lt = [[g[0][0], g[-1][1]] for g in groups]
        wg = [[[a, b] for a, b in g] for g in groups]
        json.dump({"lt": lt, "groups": wg}, open(timing_p, "w"))
    else:
        d = json.load(open(timing_p)); lt = d["lt"]
    groups = json.load(open(timing_p))["groups"] if os.path.exists(timing_p) and not plan.get("line_times") else [[x] for x in lt]
    for i, (s, e) in enumerate(lt):
        print(f"   line {i+1:2d} {s:6.2f}-{e:6.2f}  {texts[i][:60]}")
    hp = os.path.join(work, "heard.txt")
    if os.path.exists(hp):
        for ln in open(hp):
            mm = re.match(r"\s*([\d.]+)-\s*([\d.]+) (.*)", ln)
            if mm: HEARD[round(float(mm.group(1)), 2)] = len(mm.group(3).split())
    words_t = [caption_times(l, g) for l, g in zip(lines, groups)]
    total = lt[-1][1] + plan.get("tail_seconds", 1.2)

    shots = plan["shots"]
    for s in shots:
        s["_t"] = 0.0 if (s["line"] == 0 and s.get("at", 0) == 0) else resolve(s.get("at", 0), s["line"], lt, words_t)
    shots.sort(key=lambda s: s["_t"])
    for k, s in enumerate(shots):
        s["_e"] = shots[k + 1]["_t"] if k + 1 < len(shots) else total
        print(f"   shot {k:2d} {s['_t']:6.2f}-{s['_e']:6.2f} {s['src']}")

    if not args.frames and not args.facecheck:
        print("2 audio")
        ev = []
        for x in plan.get("sfx", []):
            ev.append((resolve(x.get("at", 0), x["line"], lt, words_t) + x.get("offset", 0), x["name"], x.get("db", -6), x.get("anchor", "start")))
        sfx_wav = os.path.join(work, "sfx.wav"); M.build_sfx_track(ev, total, sfx_wav)
        segs = []
        for m in plan["music"]:
            src = m["src"] if os.path.isabs(m["src"]) else os.path.join(ep, m["src"])
            if m.get("align_src") is not None:
                ta = resolve(m["align_at"], m["align_line"], lt, words_t)
                m = dict(m, offset=round(m["align_src"] - ta, 3)); print(f"   music aligned: src {m['align_src']}s at video {ta:.2f}s -> offset {m['offset']}")
            segs.append(dict(m, src=src, t=resolve(m.get("at", 0), m.get("line", 0), lt, words_t) if (m.get("line", 0) or m.get("at", 0)) else 0.0))
        bed = build_music(segs, total, work, vclean)
        if plan.get("music_env"):   # piecewise-linear gain automation on the bed: [[line, at, db], ...]
            pts = sorted((resolve(a, l, lt, words_t), d) for l, a, d in plan["music_env"])
            import wave
            raw = subprocess.run(["ffmpeg", "-v", "error", "-i", bed, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
            b = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
            tt = np.arange(len(b)) / SR
            g = np.interp(tt, [p[0] for p in pts], [p[1] for p in pts], left=pts[0][1], right=pts[-1][1])
            b *= (10 ** (g / 20))[:, None]
            with wave.open(bed, "wb") as wf:
                wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((np.clip(b, -1, 1) * 32767).astype(np.int16).tobytes())
            print("   music envelope", [(round(t, 2), d) for t, d in pts])
        mixed = os.path.join(work, "mix.wav")
        final_mix(vclean, bed, sfx_wav, total, mixed, plan.get("audio_fade_out", 0.8))

    print("3 frames")
    cache = {}
    def media(src, fit, start=0.0, speed=1.0, key=None):
        k = key or (src, fit, start, speed)
        if k not in cache:
            if src == "black":
                cache[k] = Image.new("RGB", (W, H))
            else:
                p = os.path.join(ep, "images", src)
                cache[k] = Clip(p, start, speed) if p.lower().endswith((".mp4", ".mov", ".webm")) else load_still(p, fit)
        return cache[k]

    def base_frame(s, t):
        m = media(s["src"], s.get("fit", "cover"), s.get("clip_start", 0.0), s.get("speed", 1.0))
        lt_ = t - s["_t"]
        if isinstance(m, Clip):
            fr = m.at(lt_)
            if s.get("z") or s.get("move") in ("in", "out", "punch"):
                span = s["_e"] - s["_t"] + 0.4
                z0, z1 = s.get("z", [1.0, 1.08])
                zz = z0 + (z1 - z0) * min(1, lt_ / span)
                if zz != 1:
                    fx, fy = s.get("focus", [0.5, 0.5]); cw, ch = W / zz, H / zz
                    cx = min(max(fx * W, cw / 2), W - cw / 2); cy = min(max(fy * H, ch / 2), H - ch / 2)
                    fr = fr.resize((W, H), Image.BICUBIC, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
        elif isinstance(m, Image.Image) and s["src"] == "black":
            fr = m.copy()
        else:
            span = s["_e"] - s["_t"] + s.get("xfade", 0.3)
            fr = camera(m, lt_ / span, s.get("move", "in"), s.get("focus", [0.5, 0.5]), s.get("z"), t, s.get("handheld", plan.get("handheld", 0)))
        for ov in s.get("overlays", []):
            o = media(ov["src"], "cover", ov.get("clip_start", 0.0), ov.get("speed", 1.0),
                      key=(ov["src"], "ov", ov.get("clip_start", 0.0), ov.get("speed", 1.0), id(s)))
            ofr = o.at(lt_) if isinstance(o, Clip) else o
            sc = ov.get("scale", 1.0)
            if sc != 1.0:
                ofr = ofr.resize((int(W * sc), int(H * sc)), Image.BILINEAR)
                cx, cy = ov.get("pos", [0.5, 0.5]); canvas = Image.new("RGB", (W, H))
                canvas.paste(ofr, (int(cx * W - ofr.width / 2), int(cy * H - ofr.height / 2))); ofr = canvas
            if ov.get("flip"): ofr = ofr.transpose(Image.FLIP_LEFT_RIGHT)
            fi, fo = ov.get("fade", [0.3, 0.0])
            a = ov.get("opacity", 1.0) * min(1, (lt_ - ov.get("delay", 0)) / fi if fi else 1)
            if fo: a *= min(1, max(0, (s["_e"] - t) / fo))
            if lt_ < ov.get("delay", 0): a = 0
            if a <= 0: continue
            if ov.get("mode", "screen") == "screen":
                blended = ImageChops.screen(fr, ofr)
            elif ov["mode"] == "add":
                blended = ImageChops.add(fr, ofr)
            else:
                blended = ofr
            fr = Image.blend(fr, blended, min(1, a))
        b = s.get("bright")
        if b:
            span = s["_e"] - s["_t"]
            bb = b[0] + (b[1] - b[0]) * min(1, max(0, lt_ / (s.get("bright_dur") or span)))
            if bb < 0.999:
                fr = Image.eval(fr, lambda v, bb=bb: int(v * bb))
        return fr

    vig = vignette(); tag = ai_tag()
    labels = {id(s): label_layer(s["label"]) for s in shots if s.get("label")}
    heads = {id(s): headline_layer(s["headline"], s.get("headline_size", 100), accent=s.get("headline_accent")) for s in shots if s.get("headline")}
    hook = plan.get("hook")
    hook_layer = headline_layer(hook["text"], hook.get("size", 130), accent=hook.get("accent")) if hook else None
    emph_words = [set(w.lower() for w in l.get("emph", [])) for l in lines]
    caps = []
    for i, wt in enumerate(words_t):
        for ch in M.chunk_words(wt, plan.get("cap_words", 3), plan.get("cap_chars", 16)):
            caps.append((i, ch))
    no_caps = set(plan.get("no_caption_lines", []))
    cap_cache = {}

    if args.facecheck:
        facecheck(shots, base_frame, plan, labels, heads, hook_layer, hook, caps, lt)
        return
    only = [float(x) for x in args.frames.split(",")] if args.frames else None
    out = args.out or os.path.join(ep, plan.get("output", "short.mp4"))
    if not only:
        enc = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                "-i", os.path.join(work, "mix.wav"), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
                               stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    frames = [int(x * FPS) for x in only] if only else range(int(total * FPS))
    ci = 0
    for f in frames:
        t = f / FPS
        k = max(i for i, s in enumerate(shots) if s["_t"] <= t + 1e-6) if t >= shots[0]["_t"] else 0
        s = shots[k]
        fr = base_frame(s, t)
        xf = s.get("xfade", 0.25)
        if k > 0 and xf and t - s["_t"] < xf:
            fr = Image.blend(base_frame(shots[k - 1], t), fr, (t - s["_t"]) / xf)
        lt_ = t - s["_t"]
        if s.get("shake") and lt_ < 0.5:
            amp = 20 * (1 - lt_ / 0.5); dx, dy = int(amp * math.sin(lt_ * 90)), int(amp * math.cos(lt_ * 73))
            fr = fr.resize((int(W * 1.04), int(H * 1.04))).crop((int(W * .02) + dx, int(H * .02) + dy, int(W * .02) + dx + W, int(H * .02) + dy + H))
        if s.get("fade_out_black"):
            fo = s["fade_out_black"]; a = min(1, max(0, (s["_e"] - t) / fo))
            if a < 1: fr = Image.eval(fr, lambda v, a=a: int(v * a))
        fr = add_grain(fr, f).convert("RGBA")
        fr.alpha_composite(vig)
        if s.get("glint") and lt_ < s["glint"].get("dur", 0.6):      # bright diagonal light sweep across the frame
            g = s["glint"]; q = lt_ / g.get("dur", 0.6)
            band = Image.new("L", (W, H), 0); bd = ImageDraw.Draw(band)
            cx = -0.3 * W + q * 1.6 * W; wdt = 120
            bd.polygon([(cx - wdt, H), (cx + wdt, H), (cx + wdt + H * 0.55, 0), (cx - wdt + H * 0.55, 0)], fill=int(200 * (1 - abs(q - 0.5))))
            band = band.filter(ImageFilter.GaussianBlur(40))
            fr.alpha_composite(Image.merge("RGBA", (Image.new("L", (W, H), 255),) * 3 + (band,)))
        if s.get("flash") and lt_ < 0.25:
            fr.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(235 * (1 - lt_ / 0.25)))))
        if s.get("ai") and lt_ > 0.15:
            fr.alpha_composite(fade_alpha(tag, min(1, (lt_ - 0.15) / 0.3)), (40, 190))
        if id(s) in labels:
            L = labels[id(s)]; dur = s.get("label_dur", 1.5); d0 = s.get("label_delay", 0.1)
            a = min(1, (lt_ - d0) / 0.25, (d0 + dur - lt_) / 0.3)
            if a > 0: fr.alpha_composite(fade_alpha(L, a), ((W - L.width) // 2, int(s.get("label_y", 300))))
        if hook_layer is not None and t < hook.get("until", 2.5):
            a = min(1, (hook["until"] - t) / 0.25)
            sc_ = 1.0 + 0.04 * math.sin(min(t, 0.3) / 0.3 * math.pi)       # tiny punch on frame 1, already visible at 0.0
            L = hook_layer if sc_ == 1 else hook_layer.resize((int(W * sc_), int(hook_layer.height * sc_)), Image.BILINEAR)
            fr.alpha_composite(fade_alpha(L, a), ((W - L.width) // 2, int(H * hook.get("y", 0.15))))
        if id(s) in heads:
            L = heads[id(s)]; d0 = s.get("headline_delay", 0.05); dur = s.get("headline_dur", 99)
            a = min(1, (lt_ - d0) / 0.15, (s["_e"] - t) / 0.2, (d0 + dur - lt_) / 0.2)
            if a > 0:
                age = lt_ - d0; sc_ = 0.85 + 0.15 * min(1, max(0, age) / 0.12)
                L2 = L if sc_ >= 1 else L.resize((int(W * sc_), int(L.height * sc_)), Image.BILINEAR)
                fr.alpha_composite(fade_alpha(L2, a), ((W - L2.width) // 2, int(H * s.get("headline_y", 0.16))))
        # captions
        if only:
            ci = 0
        while ci + 1 < len(caps) and caps[ci + 1][1][0][1] <= t:
            ci += 1
        li, ch = caps[ci]
        if t >= plan.get("captions_from", 0) and li not in no_caps and ch[0][1] - 0.05 <= t <= ch[-1][2] + 0.35 and t < plan.get("captions_until", 1e9):
            act = max([j for j, w in enumerate(ch) if w[1] <= t] or [0])
            key = (ci, act)
            if key not in cap_cache:
                cap_cache.clear()
                ws = [w[0].upper() for w in ch]
                em = [re.sub(r"[^\w']", "", w[0].lower()) in emph_words[li] for w in ch]
                cap_cache[key] = caption_layer(ws, act, em)
            layer = cap_cache[key]
            age = t - ch[0][1]
            if age < 0.1:
                sc = 0.88 + 0.12 * max(0, age) / 0.1
                layer = layer.resize((int(W * sc), int(layer.height * sc)), Image.BILINEAR)
            fr.alpha_composite(layer, ((W - layer.width) // 2, int(H * s.get("cap_y", plan.get("cap_y", 0.60)))))
        if only:
            fr.convert("RGB").save(os.path.join(work, f"frame_{t:05.2f}.jpg"), quality=85)
        else:
            enc.stdin.write(fr.convert("RGB").tobytes())
            if f % (FPS * 5) == 0: print(f"   {t:5.1f}/{total:.1f}s", flush=True)
    if not only:
        enc.stdin.close(); enc.wait()
        print(f"done -> {out} ({total:.1f}s)")
    for m in cache.values():
        if isinstance(m, Clip): m.close()


if __name__ == "__main__":
    main()
