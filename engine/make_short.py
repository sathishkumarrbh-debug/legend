#!/usr/bin/env python3
"""
make_short.py  -  turn a voice recording + scene plan into a finished YouTube Short.

Usage:
    python3 make_short.py <episode_folder> [--voice FILE] [--music FILE] [--out FILE]

Episode folder layout:
    scenes.json      scene plan (one entry per spoken line, see ep001 for an example)
    images/          pictures referenced by scenes.json
    ep###_voice.*    your recording (mp3 / m4a / wav / ogg / aac)

How the sync works:
    You read one line, pause about a second, read the next. The script finds those
    pauses, matches each speech block to a line of the script (using line length as
    a guide, so an extra breath mid-line doesn't break it), and cuts each scene
    exactly where its line starts. Captions are timed word by word inside each line.
"""
import argparse, json, math, os, re, subprocess, sys, glob, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, PngImagePlugin
PngImagePlugin.MAX_TEXT_CHUNK = 100 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
SR = 44100
FONT_CAP = os.path.join(HERE, "fonts", "Anton.ttf")
FONT_TITLE = os.path.join(HERE, "fonts", "Cinzel-Bold.ttf")
GOLD = (255, 197, 61, 255)
WHITE = (255, 255, 255, 255)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r


def duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(r.stdout.strip())


# ---------------------------------------------------------------- audio

def clean_voice(src, dst, tempo=1.0):
    """Optional speed-up (pitch kept), high-pass, gentle denoise, compression, loudness to -14 LUFS."""
    af = ((f"atempo={tempo}," if abs(tempo - 1) > 0.01 else "") + "highpass=f=80,afftdn=nf=-25,"
          "acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,"
          "loudnorm=I=-14:TP=-1.5:LRA=9")
    run(["ffmpeg", "-y", "-i", src, "-af", af, "-ar", str(SR), "-ac", "1", dst])


def speech_segments(path, noise_db=-35, min_sil=0.28):
    r = subprocess.run(["ffmpeg", "-i", path, "-af", f"silencedetect=noise={noise_db}dB:d={min_sil}",
                        "-f", "null", "-"], capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    total = duration(path)
    sil = list(zip(starts, ends + [total] * (len(starts) - len(ends))))
    segs, t = [], 0.0
    for s, e in sil:
        if s - t > 0.12:
            segs.append([t, s])
        t = e
    if total - t > 0.12:
        segs.append([t, total])
    return segs, total


def split_longest(segs):
    i = max(range(len(segs)), key=lambda k: segs[k][1] - segs[k][0])
    s, e = segs[i]
    m = s + (e - s) / 2
    return segs[:i] + [[s, m - 0.02], [m + 0.02, e]] + segs[i + 1:]


def align(segs, lines):
    """Group M speech segments into N consecutive groups, one per line (dynamic programming)."""
    n = len(lines)
    while len(segs) < n:
        segs = split_longest(segs)
    m = len(segs)
    weights = [max(len(l), 4) for l in lines]
    speech = sum(e - s for s, e in segs)
    expect = [speech * w / sum(weights) for w in weights]
    gaps = [segs[i + 1][0] - segs[i][1] for i in range(m - 1)] + [9.0]
    INF = float("inf")
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for k in range(1, n + 1):
        for j in range(k, m - (n - k) + 1):
            for i in range(k - 1, j):
                if dp[k - 1][i] == INF:
                    continue
                d = sum(segs[x][1] - segs[x][0] for x in range(i, j))
                c = (d - expect[k - 1]) ** 2 / expect[k - 1]
                c -= 0.8 * min(gaps[j - 1], 1.5)          # prefer to end a line at a long pause
                c += 0.6 * sum(1 for x in range(i, j - 1) if gaps[x] > 0.7)  # don't swallow long pauses
                if dp[k - 1][i] + c < dp[k][j]:
                    dp[k][j] = dp[k - 1][i] + c
                    back[k][j] = i
    groups, j = [], m
    for k in range(n, 0, -1):
        i = back[k][j]
        groups.append(segs[i:j])
        j = i
    return groups[::-1]


# ---------------------------------------------------------------- speech recognition (optional)
ASR_DIR = os.path.join(HERE, "asr", "sherpa-onnx-whisper-small.en")
_rec = None

def transcribe_segments(path, segs):
    """Transcribe each speech block with Whisper (offline). Returns None if the model isn't installed."""
    global _rec
    if not os.path.isdir(ASR_DIR):
        try:   # one-time download of the offline speech model (~1 GB) from the sherpa-onnx GitHub releases
            os.makedirs(os.path.dirname(ASR_DIR), exist_ok=True)
            url = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-small.en.tar.bz2"
            subprocess.run(f"curl -sSL {url} | tar xj -C {os.path.dirname(ASR_DIR)}", shell=True, check=True, timeout=900)
        except Exception:
            return None
    import sherpa_onnx
    if _rec is None:
        m = os.path.join(ASR_DIR, "small.en-")
        _rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=m + "encoder.int8.onnx", decoder=m + "decoder.int8.onnx",
                                                          tokens=m + "tokens.txt", num_threads=os.cpu_count() or 2)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ar", "16000", "-ac", "1", "-f", "s16le", "-"],
                         capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    out = []
    for s, e in segs:
        st = _rec.create_stream()
        st.accept_waveform(16000, a[int(max(0, s - 0.08) * 16000):int((e + 0.08) * 16000)])
        _rec.decode_stream(st)
        out.append(st.result.text.strip())
    return out


def _words(t):
    t = t.lower().replace("chandragupta the second", "chandragupta ii")
    return re.findall(r"[a-z0-9']+", t)


def align_by_text(segs, texts, lines):
    """Assign consecutive speech blocks to script lines by matching the words actually spoken."""
    import difflib
    n, m = len(lines), len(segs)
    lw = [_words(l) for l in lines]
    sw = [_words(t) for t in texts]
    INF = float("inf")
    dp = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[0] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for k in range(1, n + 1):
        for j in range(k, m - (n - k) + 1):
            for i in range(k - 1, j):
                if dp[k - 1][i] == INF:
                    continue
                spoken = [w for x in range(i, j) for w in sw[x]]
                sim = difflib.SequenceMatcher(None, lw[k - 1], spoken).ratio()
                c = (1 - sim) * (len(lw[k - 1]) + len(spoken))
                if dp[k - 1][i] + c < dp[k][j]:
                    dp[k][j] = dp[k - 1][i] + c
                    back[k][j] = i
    groups, j = [], m
    for k in range(n, 0, -1):
        i = back[k][j]
        groups.append(segs[i:j]); j = i
    return groups[::-1]


# ---------------------------------------------------------------- best-take picker
def assemble_best_takes(voice_files, lines, work, noise_db=-38, min_pause=0.18, tempo=1.0):
    """You can read each line 2 to 3 times (or the whole script 2 to 3 times, in any order).
    Every phrase is transcribed; for each script line the take whose words match best is kept
    (on a tie the later take wins, since the last try is usually the best), then the kept takes are
    joined with short natural gaps."""
    import difflib
    cands = []                                   # (file_index, seg list, texts)
    for fi, vf in enumerate(voice_files):
        c = os.path.join(work, f"take_src{fi}.wav")
        clean_voice(vf, c, tempo)
        segs, _ = speech_segments(c, noise_db, min_pause)
        texts = transcribe_segments(c, segs)
        if texts is None:
            sys.exit("best-take picking needs the speech model; could not load it")
        cands.append((c, segs, texts))
    report, pieces = [], []
    for li, line in enumerate(lines):
        lw = _words(line)
        best = None
        for fi, (c, segs, texts) in enumerate(cands):
            for i in range(len(segs)):
                spoken = []
                for j in range(i, min(len(segs), i + 8)):
                    spoken += _words(texts[j])
                    if len(spoken) > len(lw) * 1.6 + 3:
                        break
                    sm = difflib.SequenceMatcher(None, lw, spoken)
                    cover = sum(b.size for b in sm.get_matching_blocks()) / max(1, len(lw))
                    r = 0.5 * sm.ratio() + 0.5 * cover   # reward covering the whole line, not just a clean half
                    key = (round(r, 2), fi, i)
                    if best is None or key >= best[0]:
                        best = (key, c, segs[i][0], segs[j][1], " ".join(texts[i:j + 1]))
        (r, fi, _), c, a, b, heard = best
        report.append(f"line {li+1:2d}: take from file {fi+1} at {a:6.2f}s  match {int(r*100)}%  heard: {heard[:70]}")
        pieces.append((c, max(0, a - 0.06), b + 0.12))
    out = os.path.join(work, "best_takes.wav")
    parts, i = [], 0
    for c, a, b in pieces:
        p = os.path.join(work, f"piece{i:02d}.wav"); i += 1
        run(["ffmpeg", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", c,
             "-af", "afade=t=in:d=0.02,afade=t=out:st=%.3f:d=0.05" % max(0, b - a - 0.05), "-ar", str(SR), "-ac", "1", p])
        parts.append(p)
    gap = os.path.join(work, "gap.wav")
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", "0.32", gap])
    lst = os.path.join(work, "pieces.txt")
    with open(lst, "w") as fh:
        for p in parts:
            fh.write(f"file '{os.path.abspath(p)}'\nfile '{os.path.abspath(gap)}'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:a", "pcm_s16le", out])
    open(os.path.join(work, "takes_report.txt"), "w").write("\n".join(report))
    print("\n".join("   " + r for r in report))
    spans, t = [], 0.0                      # exact position of every line in the joined file
    for c, a, b in pieces:
        spans.append([[t + 0.06, t + (b - a) - 0.12]]); t += (b - a) + 0.32
    return out, spans


def word_times(text, group):
    """Spread words across the speech-only time of a line, weighted by word length."""
    words = text.split()
    w = [len(re.sub(r"[^\w]", "", x)) + 1.5 for x in words]
    speech = [(s, e) for s, e in group]
    total = sum(e - s for s, e in speech)

    def at(frac):
        t = frac * total
        for s, e in speech:
            if t <= e - s:
                return s + t
            t -= e - s
        return speech[-1][1]

    acc, out = 0, []
    for word, wt in zip(words, w):
        a = acc / sum(w)
        acc += wt
        out.append((word, at(a), at(acc / sum(w))))
    return out


def tanpura(seconds, sa=130.81, path=None):
    """Original tanpura-style drone (Pa Sa Sa Sa-low), synthesised here so it is copyright-free."""
    n = int(seconds * SR) + SR
    out = np.zeros(n)
    notes = [sa * 0.75, sa, sa, sa / 2]
    period = 1.25
    rng = np.random.default_rng(7)
    t_note = np.arange(int(5.5 * SR)) / SR
    k = 0
    t0 = 0.0
    while t0 < seconds + 1:
        f = notes[k % 4] * (1 + rng.normal(0, 0.0008))
        tone = np.zeros_like(t_note)
        for h in range(1, 16):
            amp = (1 / h ** 0.9) * np.exp(-t_note * (0.55 + 0.05 * h))
            buzz = 1 + 0.35 * np.sin(2 * np.pi * 0.7 * t_note + h) * (h > 4)  # jawari shimmer
            tone += amp * buzz * np.sin(2 * np.pi * f * h * t_note + rng.uniform(0, 6.28))
        tone *= np.minimum(1, t_note / 0.01)
        a = int(t0 * SR)
        b = min(n, a + len(tone))
        out[a:b] += tone[: b - a]
        t0 += period
        k += 1
    out = out[: int(seconds * SR)]
    out /= np.max(np.abs(out)) + 1e-9
    fade = int(1.5 * SR)
    out[:fade] *= np.linspace(0, 1, fade)
    out[-fade:] *= np.linspace(1, 0, fade)
    pcm = (out * 0.6 * 32767).astype(np.int16)
    import wave
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())


PHONE_BAND = "highpass=f=300,highpass=f=300,lowpass=f=6000"   # roughly what a phone speaker reproduces

def band_rms_db(path, af=PHONE_BAND, start=0.0, dur=None, active_only=False):
    """RMS level (dBFS) of a file as a phone speaker would play it. active_only ignores pauses (for voice)."""
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start)] + (["-t", str(dur)] if dur else []) + \
          ["-i", path, "-af", af, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32)
    if len(a) == 0:
        return -99.0
    if active_only:
        fr = a[: len(a) // 800 * 800].reshape(-1, 800)
        r = np.sqrt((fr ** 2).mean(1)); a = fr[r > r.max() * 0.1].ravel()
    return float(20 * np.log10(np.sqrt((a ** 2).mean()) + 1e-9))


MUSIC_EQ = "acompressor=threshold=-26dB:ratio=3:attack=300:release=1500:makeup=1,equalizer=f=2500:t=q:w=1.2:g=-3"  # compressor evens out music swells

def mix(voice, music, total, dst, music_db=None, offset=0.0, sfx=None, music_gap_db=6.0):
    """Voice on top of a CONTINUOUS music bed (no ducking/pumping). The music level is set automatically so that,
    on a PHONE speaker, it sits music_gap_db under the voice (EP1 lesson: -14 dB fixed gain left the music
    about 11 dB under the voice and viewers could barely hear it). A gentle dip at 2.5 kHz keeps words clear."""
    if music_db is None:
        v = band_rms_db(voice, active_only=True)
        m = band_rms_db(music, PHONE_BAND + "," + MUSIC_EQ, start=offset, dur=total)
        music_db = round(v - music_gap_db - m, 1)
        print(f"   music auto-level: voice {v:.1f} dB, music {m:.1f} dB (phone band) -> gain {music_db:+.1f} dB")
    fc = (f"[1:a]atrim=start={offset},asetpts=PTS-STARTPTS,afade=t=in:d=0.6,{MUSIC_EQ},volume={music_db}dB,apad[m];"
          f"[0:a]apad[v];" +
          (f"[2:a]alimiter=limit=0.8:attack=1:release=60:level=false,apad[fx];[v][m][fx]amix=inputs=3:duration=first:normalize=0," if sfx else
           f"[v][m]amix=inputs=2:duration=first:normalize=0,") +
          f"atrim=0:{total:.3f},alimiter=limit=0.97:attack=5:release=200:level=false,afade=t=out:st={total-1.2:.3f}:d=1.2[out]")
    cmd = ["ffmpeg", "-y", "-i", voice, "-stream_loop", "-1", "-i", music]
    if sfx:
        cmd += ["-i", sfx]
    run(cmd + ["-filter_complex", fc, "-map", "[out]", "-ar", str(SR), "-ac", "2", dst])


# ---------------------------------------------------------------- video clips as scenes
VIDEO_EXT = (".mp4", ".mov", ".webm", ".mkv", ".m4v")

class VideoSource:
    """Streams frames of a clip (cover-cropped to W x H, looped) on demand, in time order."""
    def __init__(self, path, speed=1.0):
        self.path, self.speed = path, speed
        self.proc, self.idx, self.frame = None, -1, None

    def _open(self):
        vf = (f"setpts=PTS/{self.speed},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H}")
        self.proc = subprocess.Popen(["ffmpeg", "-v", "error", "-stream_loop", "-1", "-i", self.path, "-an",
                                      "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                     stdout=subprocess.PIPE)
        self.idx = -1

    def at(self, local_t):
        want = max(0, int(local_t * FPS))
        if self.proc is None or want < self.idx:
            if self.proc: self.proc.kill()
            self._open()
        while self.idx < want:
            buf = self.proc.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                break
            self.frame = Image.frombytes("RGB", (W, H), buf); self.idx += 1
        return self.frame

    def close(self):
        if self.proc: self.proc.kill()


# ---------------------------------------------------------------- sound effects
SFX_DIR = os.path.join(HERE, "sfx")

def load_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


def sfx_path(name):
    for ext in (".wav", ".mp3"):
        p = os.path.join(SFX_DIR, name + ext)
        if os.path.exists(p):
            return p
    return None


def build_sfx_track(events, total, dst):
    """events: list of (time_seconds, name, db, anchor) with anchor 'start' (sound begins at t) or 'end' (sound ends at t)."""
    n = int((total + 1) * SR)
    track = np.zeros((n, 2), np.float32)
    cache = {}
    for t, name, db, anchor in events:
        p = sfx_path(name)
        if not p:
            print(f"   (sound effect '{name}' not found, skipped)"); continue
        if name not in cache:
            # normalise every effect to the same loudness ON A PHONE SPEAKER (-20 dBFS in the 300 Hz to 6 kHz band),
            # so 'db' means how loud it is heard, not how much sub-bass it has. Peak capped at 1.0.
            a = load_audio(p)
            g = 10 ** ((-20 - band_rms_db(p, active_only=True)) / 20)
            g = min(g, 1.0 / (np.abs(a).max() or 1))
            cache[name] = a * g
        a = cache[name] * (10 ** (db / 20))
        st = int((t - (len(a) / SR if anchor == "end" else 0)) * SR)
        if st < 0:
            a = a[-st:]; st = 0
        e = min(n, st + len(a))
        track[st:e] += a[: e - st]
    pcm = (np.clip(track[: int(total * SR)], -1, 1) * 32767).astype(np.int16)
    import wave
    with wave.open(dst, "wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes(pcm.tobytes())


def plan_sfx(scenes, starts, groups, plan):
    ev = []
    default = plan.get("cut_sfx")          # no automatic whoosh on every cut (EP1 lesson: it sounded cheap)
    for i, sc in enumerate(scenes):
        items = sc.get("sfx")
        if items is None:
            items = [default] if (i > 0 and default) else []
        if isinstance(items, (str, dict)):
            items = [items]
        for it in items:
            if isinstance(it, str):
                it = {"name": it}
            name = it["name"]
            db = it.get("db", -6)
            at = it.get("at", "before" if name in ("riser", "rise") else "start")
            if at == "before":
                ev.append((groups[i][0][0], name, db, "end"))
            elif at == "voice":
                ev.append((groups[i][0][0], name, db, "start"))
            elif isinstance(at, (int, float)):
                ev.append((groups[i][0][0] + at, name, db, "start"))
            elif isinstance(at, str) and at.startswith("word:"):
                target = at[5:].lower()
                wt = word_times(sc.get("caption", sc["text"]), groups[i])
                hit = next((w for w in wt if re.sub(r"[^\w]", "", w[0].lower()) == target), None)
                ev.append(((hit[1] if hit else groups[i][0][0]), name, db, "start"))
            else:
                ev.append((max(0.0, starts[i] - (0.08 if name == "whoosh" else 0)), name, db, "start"))
    return ev


# ---------------------------------------------------------------- annotations
RED = (230, 40, 40, 255)

def draw_annotation(fr, sc, lt):
    """Animated red circle / arrow that draws itself in, like the top history Shorts use."""
    d = ImageDraw.Draw(fr)
    delay = sc.get("annot_delay", 0.4)
    p = min(1.0, max(0.0, (lt - delay) / 0.45))
    if p <= 0:
        return
    if sc.get("circle"):
        cx, cy, r = sc["circle"]; cx *= W; cy *= H; r *= W
        pts = [(cx + r * math.cos(-math.pi / 2 + 2 * math.pi * p * k / 60 * 1.08),
                cy + r * 0.9 * math.sin(-math.pi / 2 + 2 * math.pi * p * k / 60 * 1.08)) for k in range(61)]
        d.line(pts, fill=(0, 0, 0, 160), width=18, joint="curve")
        d.line(pts, fill=RED, width=11, joint="curve")
    if sc.get("arrow"):
        x1, y1, x2, y2 = sc["arrow"]; x1 *= W; x2 *= W; y1 *= H; y2 *= H
        xe, ye = x1 + (x2 - x1) * p, y1 + (y2 - y1) * p
        d.line([(x1, y1), (xe, ye)], fill=RED, width=14)
        if p > 0.95:
            ang = math.atan2(y2 - y1, x2 - x1)
            for s_ in (-1, 1):
                d.line([(x2, y2), (x2 - 60 * math.cos(ang + s_ * 0.5), y2 - 60 * math.sin(ang + s_ * 0.5))], fill=RED, width=14)


# ---------------------------------------------------------------- visuals

def load_scene_image(path, mode):
    im = Image.open(path).convert("RGB")
    if mode == "fit" or (mode == "auto" and im.width / im.height > 1.25):
        # wide picture: keep it whole over a blurred, darkened copy of itself
        bg = im.copy()
        s = max(W * 1.25 / bg.width, H * 1.25 / bg.height)
        bg = bg.resize((int(bg.width * s), int(bg.height * s)), Image.LANCZOS)
        bg = bg.crop(((bg.width - int(W * 1.25)) // 2, (bg.height - int(H * 1.25)) // 2,
                      (bg.width + int(W * 1.25)) // 2, (bg.height + int(H * 1.25)) // 2))
        bg = bg.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.45))
        fg_w = int(W * 1.25 * 0.96)
        fg = im.resize((fg_w, int(im.height * fg_w / im.width)), Image.LANCZOS)
        bg.paste(fg, ((bg.width - fg.width) // 2, int(bg.height * 0.36 - fg.height / 2)))
        return bg
    s = max(W * 1.3 / im.width, H * 1.3 / im.height)
    if s > 1:
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    return im


def camera(im, p, move, focus):
    """Return a W x H frame for progress p in [0,1] using a smooth Ken Burns move."""
    p = 0.5 - 0.5 * math.cos(math.pi * p)          # ease in-out
    iw, ih = im.size
    base = min(iw / W, ih / H)                      # largest crop that fits
    fx, fy = focus
    z0, z1 = {"in": (1.0, 1.15), "out": (1.15, 1.0), "punch": (1.0, 1.3)}.get(move, (1.08, 1.08))
    if move == "punch":        # snap in fast over the first ~15% of the shot, then keep creeping
        q = min(1.0, p / 0.15)
        z = 1.0 + 0.2 * (1 - (1 - q) ** 3) + 0.08 * p   # quick push-in, then a slow creep
    else:
        z = z0 + (z1 - z0) * p
    cw, ch = W * base / z, H * base / z
    if move in ("left", "right"):
        a, b = (0.0, 1.0) if move == "right" else (1.0, 0.0)
        cx = cw / 2 + (iw - cw) * (a + (b - a) * p)
        cy = fy * ih
    elif move in ("up", "down"):
        a, b = (1.0, 0.0) if move == "up" else (0.0, 1.0)
        cy = ch / 2 + (ih - ch) * (a + (b - a) * p)
        cx = fx * iw
    else:
        cx, cy = fx * iw, fy * ih
    cx = min(max(cx, cw / 2), iw - cw / 2)
    cy = min(max(cy, ch / 2), ih - ch / 2)
    return im.resize((W, H), Image.BILINEAR, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))


def make_grade():
    """Vignette + darker band behind captions, applied to every frame."""
    y, x = np.mgrid[0:H, 0:W]
    r = np.sqrt(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H / 2) / (H * 0.7)) ** 2)
    a = np.clip((r - 0.55) * 1.4, 0, 0.75)
    band = np.exp(-((y - H * 0.66) / (H * 0.12)) ** 2) * 0.35
    top = np.clip((H * 0.2 - y) / (H * 0.2), 0, 1) * 0.45
    alpha = np.clip(a + band + top, 0, 0.85)
    ov = np.zeros((H, W, 4), np.uint8)
    ov[..., 3] = (alpha * 255).astype(np.uint8)
    return Image.fromarray(ov, "RGBA")


def text_layer(words, active, size=108):
    font = ImageFont.truetype(FONT_CAP, size)
    sp = size * 0.28
    widths = [font.getlength(w) for w in words]
    total = sum(widths) + sp * (len(words) - 1)
    if total > W * 0.86:
        return text_layer(words, active, int(size * W * 0.86 / total))
    img = Image.new("RGBA", (W, int(size * 1.9)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = (W - total) / 2
    for i, (w, wd) in enumerate(zip(words, widths)):
        d.text((x, size * 0.2), w, font=font, fill=GOLD if i == active else WHITE,
               stroke_width=max(6, size // 13), stroke_fill=(0, 0, 0, 255))
        x += wd + sp
    return img


def chunk_words(wt, max_words=3, max_chars=17):
    chunks, cur = [], []
    for item in wt:
        word = item[0]
        if cur and (len(cur) >= max_words or sum(len(c[0]) + 1 for c in cur) + len(word) > max_chars):
            chunks.append(cur); cur = []
        cur.append(item)
        if re.search(r"[.,?!;:]$", word):
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    return chunks


def title_layer(text, sub=None):
    img = Image.new("RGBA", (W, 420), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = 78
    font = ImageFont.truetype(FONT_TITLE, size)
    lines, cur = [], ""
    for w in text.upper().split():
        t = (cur + " " + w).strip()
        if font.getlength(t) > W * 0.84 and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    y = 20
    for ln in lines:
        d.text(((W - font.getlength(ln)) / 2, y), ln, font=font, fill=GOLD,
               stroke_width=5, stroke_fill=(0, 0, 0, 255))
        y += size * 1.2
    if sub:
        f2 = ImageFont.truetype(FONT_TITLE, 40)
        d.text(((W - f2.getlength(sub.upper())) / 2, y + 8), sub.upper(), font=f2, fill=WHITE,
               stroke_width=3, stroke_fill=(0, 0, 0, 255))
    return img


def label_layer(text):
    f = ImageFont.truetype(FONT_TITLE, 38)
    tw = f.getlength(text.upper())
    img = Image.new("RGBA", (int(tw + 60), 76), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, img.width - 1, 75), 16, fill=(0, 0, 0, 150), outline=GOLD, width=3)
    d.text((30, 14), text.upper(), font=f, fill=WHITE)
    return img


def badge_layer(text):
    f = ImageFont.truetype(FONT_TITLE, 34)
    tw = f.getlength(text.upper())
    img = Image.new("RGBA", (int(tw + 56), 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, img.width - 1, 63), 32, fill=(0, 0, 0, 160))
    # thin tricolour underline: saffron, white, green
    third = (img.width - 60) / 3
    for k, col in enumerate([(255, 153, 51, 255), (255, 255, 255, 255), (19, 136, 8, 255)]):
        d.line([(30 + k * third, 55), (30 + (k + 1) * third, 55)], fill=col, width=4)
    d.text((28, 9), text.upper(), font=f, fill=GOLD)
    return img


def end_card_layer(title, sub):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f1 = ImageFont.truetype(FONT_TITLE, 96); f2 = ImageFont.truetype(FONT_CAP, 56)
    y = int(H * 0.40)
    for k, col in enumerate([(255, 153, 51, 255), (255, 255, 255, 255), (19, 136, 8, 255)]):
        d.rectangle((W * 0.2 + k * W * 0.2, y - 40, W * 0.2 + (k + 1) * W * 0.2, y - 30), fill=col)
    for ln in title.upper().split("|"):
        tw = d.textlength(ln, font=f1)
        d.text(((W - tw) / 2, y), ln, font=f1, fill=GOLD, stroke_width=6, stroke_fill=(0, 0, 0, 255)); y += 115
    if sub:
        tw = d.textlength(sub.upper(), font=f2)
        d.text(((W - tw) / 2, y + 20), sub.upper(), font=f2, fill=WHITE, stroke_width=5, stroke_fill=(0, 0, 0, 255))
    return img


def fade_alpha(layer, a):
    if a >= 1:
        return layer
    l = layer.copy()
    l.putalpha(l.getchannel("A").point(lambda v: int(v * a)))
    return l


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--voice", nargs="+", help="one recording, or 2 to 3 takes to pick the best lines from")
    ap.add_argument("--music")
    ap.add_argument("--out")
    ap.add_argument("--noise-db", type=float, default=-38)
    ap.add_argument("--min-pause", type=float, default=0.22)
    ap.add_argument("--best-takes", action="store_true", help="the single recording contains repeated takes")
    ap.add_argument("--tempo", type=float, default=1.0, help="speed up the voice, e.g. 1.15 (pitch unchanged)")
    args = ap.parse_args()
    ep = os.path.abspath(args.episode)
    plan = json.load(open(os.path.join(ep, "scenes.json")))
    scenes = plan["scenes"]
    voices = args.voice or sorted(glob.glob(os.path.join(ep, "*voice*.*")))
    if not voices:
        sys.exit("no voice file found (name it ep###_voice.mp3 or pass --voice)")
    work = os.path.join(ep, "_work"); os.makedirs(work, exist_ok=True)
    out = args.out or os.path.join(ep, plan.get("output", "short.mp4"))

    print("1/5 cleaning voice"); vclean = os.path.join(work, "voice_clean.wav")
    if len(voices) > 1 or args.best_takes:
        print("   picking the best take of every line")
        best, known_groups = assemble_best_takes(voices, [s["text"] for s in scenes], work, args.noise_db, 0.18, args.tempo)
        clean_voice(best, vclean, 1.0)
    else:
        known_groups = None
        clean_voice(voices[0], vclean, args.tempo)

    print("2/5 finding line breaks")
    segs, vdur = speech_segments(vclean, args.noise_db, args.min_pause)
    lines = [s["text"] for s in scenes]
    texts = None if known_groups else (transcribe_segments(vclean, segs) if len(segs) >= len(lines) else None)
    if texts:   # split blocks that hold two sentences (no pause between them) at the sentence break
        ns, nt = [], []
        for (a, b), tx in zip(segs, texts):
            parts = [p.strip() for p in re.split(r"(?<=[.?!])\s+", tx) if p.strip()]
            if len(parts) > 1 and b - a > 1.2:
                tot = sum(len(p) for p in parts); t0 = a
                for p in parts:
                    t1 = t0 + (b - a) * len(p) / tot
                    ns.append([t0, t1 - 0.02]); nt.append(p); t0 = t1 + 0.02
            else:
                ns.append([a, b]); nt.append(tx)
        segs, texts = ns, nt
    if known_groups:
        groups = known_groups
    elif texts:
        groups = align_by_text(segs, texts, lines)
        with open(os.path.join(work, "heard.txt"), "w") as fh:
            fh.write("\n".join(f"{s:6.2f}-{e:6.2f}  {t}" for (s, e), t in zip(segs, texts)))
    else:
        groups = align(segs, lines)
    total = groups[-1][-1][1] + plan.get("tail_seconds", 1.2)
    starts = [0.0] + [max(0.0, g[0][0] - 0.12) for g in groups[1:]]
    ends = starts[1:] + [total]
    for i, (s, g) in enumerate(zip(scenes, groups)):
        print(f"   line {i+1:2d}  {g[0][0]:6.2f}-{g[-1][1]:6.2f}s  {s['text'][:60]}")
    timing = [{"line": s["text"], "start": round(g[0][0], 2), "end": round(g[-1][1], 2)} for s, g in zip(scenes, groups)]
    json.dump(timing, open(os.path.join(work, "timing.json"), "w"), indent=1)

    print("3/5 music")
    music = args.music or plan.get("music")
    if music and not os.path.isabs(music):
        music = os.path.join(ep, music)
    if not music or not os.path.exists(music):
        music = os.path.join(work, "tanpura.wav"); tanpura(total + 2, path=music)
    sfx_wav = None
    if plan.get("sound_effects", True):
        sfx_wav = os.path.join(work, "sfx.wav")
        build_sfx_track(plan_sfx(scenes, starts, groups, plan), total, sfx_wav)
    mixed = os.path.join(work, "mix.wav")
    mix(vclean, music, total, mixed, plan.get("music_db"), plan.get("music_offset", 0.0), sfx_wav,
        plan.get("music_gap_db", 6.0))

    print("4/5 rendering frames")
    grade = make_grade()
    imgs = []
    for s in scenes:
        p = os.path.join(ep, "images", s["image"])
        imgs.append(VideoSource(p, s.get("speed", 1.0)) if p.lower().endswith(VIDEO_EXT)
                    else load_scene_image(p, s.get("fit", "auto")))
    caps = []
    for s, g in zip(scenes, groups):
        wt = word_times(s.get("caption", s["text"]), g)
        for ch in chunk_words(wt):
            caps.append(ch)
    cap_cache = {}
    title = title_layer(plan["title"], plan.get("subtitle")) if plan.get("title") else None
    labels = [label_layer(s["label"]) if s.get("label") else None for s in scenes]
    badge = badge_layer(plan["badge"]) if plan.get("badge") else None
    endc = plan.get("end_card")
    end_layer = end_card_layer(endc["title"], endc.get("subtitle")) if endc else None
    end_from = starts[-1] + endc.get("delay", 0.0) if endc else 1e9
    xfade = 0.35
    nframes = int(total * FPS)
    enc = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-i", mixed, "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                            "-movflags", "+faststart", out], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    ci = 0
    for f in range(nframes):
        t = f / FPS
        k = max(i for i in range(len(scenes)) if starts[i] <= t)
        def frame_of(i):
            if isinstance(imgs[i], VideoSource):
                return imgs[i].at(t - starts[i])
            span = ends[i] - starts[i] + xfade
            return camera(imgs[i], min(1, max(0, (t - starts[i]) / span)),
                          scenes[i].get("move", "in"), scenes[i].get("focus", [0.5, 0.5]))
        fr = frame_of(k)
        if k > 0 and t - starts[k] < xfade:                       # crossfade from previous scene
            fr = Image.blend(frame_of(k - 1), fr, (t - starts[k]) / xfade)
        lt = t - starts[k]
        if scenes[k].get("shake") and lt < 0.45:                  # impact shake
            amp = 22 * (1 - lt / 0.45)
            dx, dy = int(amp * math.sin(lt * 90)), int(amp * math.cos(lt * 73))
            fr = fr.resize((int(W * 1.04), int(H * 1.04))).crop((int(W * 0.02) + dx, int(H * 0.02) + dy,
                                                                  int(W * 0.02) + dx + W, int(H * 0.02) + dy + H))
        fr = fr.convert("RGBA")
        fr.alpha_composite(grade)
        draw_annotation(fr, scenes[k], lt)
        if scenes[k].get("flash") and lt < 0.18:                  # white flash on impact
            fr.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(200 * (1 - lt / 0.18)))))
        if title and t < plan.get("title_seconds", 3.0):
            a = min(1, t / 0.3, (plan.get("title_seconds", 3.0) - t) / 0.4)
            fr.alpha_composite(fade_alpha(title, a), (0, 230))
        if badge is not None and plan.get("title_seconds", 3.0) + 0.2 < t < end_from:
            fr.alpha_composite(fade_alpha(badge, min(1, (t - plan.get("title_seconds", 3.0) - 0.2) / 0.4)), ((W - badge.width) // 2, 150))
        if labels[k] is not None:
            lt = t - starts[k]
            a = min(1, lt / 0.3, (ends[k] - t) / 0.3)
            if a > 0:
                fr.alpha_composite(fade_alpha(labels[k], a), ((W - labels[k].width) // 2, 1500))
        # captions
        while ci + 1 < len(caps) and caps[ci + 1][0][1] <= t:
            ci += 1
        ch = caps[ci]
        if ch[0][1] - 0.05 <= t <= ch[-1][2] + 0.45 and t < end_from:
            act = max([j for j, w in enumerate(ch) if w[1] <= t] or [0])
            key = (ci, act)
            if key not in cap_cache:
                cap_cache.clear()
                cap_cache[key] = text_layer([w[0].upper() for w in ch], act)
            layer = cap_cache[key]
            age = t - ch[0][1]
            if age < 0.12:                                          # little pop-in
                sc = 0.85 + 0.15 * max(0, age) / 0.12
                layer = layer.resize((int(W * sc), int(layer.height * sc)), Image.BILINEAR)
            fr.alpha_composite(layer, ((W - layer.width) // 2, int(H * 0.60)))
        if end_layer is not None and t >= end_from:
            a = min(1, (t - end_from) / 0.5)
            fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(120 * a))))
            fr.alpha_composite(fade_alpha(end_layer, a))
        enc.stdin.write(fr.convert("RGB").tobytes())
        if f % (FPS * 5) == 0:
            print(f"   {t:5.1f}s / {total:.1f}s", flush=True)
    enc.stdin.close(); enc.wait()
    for im in imgs:
        if isinstance(im, VideoSource): im.close()
    print(f"5/5 done -> {out}  ({total:.1f}s)")


if __name__ == "__main__":
    main()
