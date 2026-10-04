"""Ep3 sounds: crisp brush, heavy board thud (phone-audible), driving low pulse."""
import sys, os, numpy as np, wave, subprocess; sys.path.insert(0, "..")
import fxkit as fx
SR = 44100; r = np.random.default_rng(3)
def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
# crisp brush: keep the original texture, add 3-9 kHz bristle hiss
b = load("../sfx/dirt_brush.wav"); hi = fx._bp(b, 2500, 9500); b = b + 1.8 * hi; fx._save("../sfx", "dirt_brush_crisp", b / np.abs(b).max() * 0.9)
# heavy thud: falling-pitch body 110->55 Hz with 2nd/3rd harmonics (phones play 100-300 Hz), wood crack, low-mid debris
n = int(1.4 * SR); t = np.arange(n) / SR
f = 55 + 55 * np.exp(-t / 0.08); ph = 2 * np.pi * np.cumsum(f) / SR
body = (np.sin(ph) + 0.6 * np.sin(2 * ph) + 0.35 * np.sin(3 * ph)) * np.exp(-t / 0.28)
crack = fx._bp(r.normal(size=n), 900, 5000) * np.exp(-t / 0.025) * 0.8
debris = fx._bp(r.normal(size=n), 150, 900) * np.exp(-t / 0.35) * 0.45
th = body + crack + debris; fx._save("../sfx", "thud_heavy", th / np.abs(th).max() * 0.95)
# pulse: low heartbeat-style kick at 100 bpm, swelling, 13 s
n = int(12.05 * SR); out = np.zeros(n); beat = 0.6
k_n = int(0.35 * SR); kt = np.arange(k_n) / SR; kf = 50 + 70 * np.exp(-kt / 0.03)
kick = (np.sin(2 * np.pi * np.cumsum(kf) / SR) + 0.9 * np.sin(4 * np.pi * np.cumsum(kf) / SR) + 0.5 * np.sin(6 * np.pi * np.cumsum(kf) / SR)) * np.exp(-kt / 0.12)
kick += fx._bp(r.normal(size=k_n), 700, 2500) * np.exp(-kt / 0.012) * 0.6   # knock: lets phone speakers 'hear' the beat
for i in range(int(12.05 / beat)):
    s0 = int(i * beat * SR); g = 0.45 + 0.55 * (i * beat / 12)
    out[s0:s0 + k_n] += kick[:n - s0] * g
    s1 = s0 + int(0.2 * SR)
    if s1 + k_n < n: out[s1:s1 + k_n] += kick * g * 0.45   # lub-dub
out[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR)); fx._save("../sfx", "pulse", out / np.abs(out).max() * 0.9)
print("ok")
