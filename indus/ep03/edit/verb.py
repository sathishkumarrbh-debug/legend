"""Reverb/echo tails on build-up lines only (dry voice kept intact)."""
import numpy as np, wave, subprocess
import sys; sys.path.insert(0, '..')
from fxkit import _bp
SR = 44100
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "voice_t.wav", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
r = np.random.default_rng(5)
def fftconvolve(x, h):
    n = 1 << int(np.ceil(np.log2(x.size + h.size))); return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:x.size + h.size - 1].astype(np.float32)
def ir(decay, length=2.2):
    t = np.arange(int(length * SR)) / SR; x = r.normal(size=t.size) * np.exp(-t / decay); x[:int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
    x = _bp(x, 250, 5000); return x / np.sqrt((x ** 2).sum())
def echo(x, delay, gains):
    y = np.zeros(x.size + int(delay * SR * len(gains)), np.float32)
    for k, g in enumerate(gains, 1): y[int(delay * SR * k):int(delay * SR * k) + x.size] += x * g
    return y
g_ = np.ones_like(a); s0, s1 = int(26.55 * SR), int(28.10 * SR); f = int(0.05 * SR)
g_[s0:s1] = 10 ** (11 / 20); g_[s0 - f:s0] = np.linspace(1, 10 ** (11 / 20), f); g_[s1:s1 + f] = np.linspace(10 ** (11 / 20), 1, f); s0, s1 = int(47.62 * SR), int(52.75 * SR); g_[s0:s1] = 10 ** (10 / 20); g_[s0 - f:s0] = np.linspace(1, 10 ** (10 / 20), f); g_[s1:s1 + f] = np.linspace(10 ** (10 / 20), 1, f)   # lift the soft last line
s0, s1 = int(23.20 * SR), int(26.45 * SR); g_[s0:s1] = 10 ** (5 / 20); g_[s0 - f:s0] = np.linspace(1, 10 ** (5 / 20), f); g_[s1:s1 + f] = np.linspace(10 ** (5 / 20), 1, f)   # lift 'oldest signboard'
a = a * g_   # lift the whisper
out = np.concatenate([a, np.zeros(3 * SR, np.float32)])
# (start, end, wet gain, decay, echo)
fx = [
      (28.32, 29.32, 0.17, 0.55, (0.24, [0.20, 0.09, 0.04])),   # Nobody knows.  (hall + slap echo)
      ]
for s, e, g, d, ec in fx:
    seg = a[int(s * SR):int(e * SR)].copy(); f = int(0.02 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    if g: w = fftconvolve(seg, ir(d)) * g * 6.0; out[int(s * SR):int(s * SR) + w.size] += w[:out.size - int(s * SR)]
    if ec: w = echo(_bp(seg, 250, 9000).astype(np.float32), *ec); out[int(s * SR):int(s * SR) + w.size] += w[:out.size - int(s * SR)]
out = out[:a.size + int(1.0 * SR)]; print('peak', round(float(np.abs(out).max()), 3)); pk = np.abs(out).max(); out = out / max(pk, 1) * 0.97 if pk > 0.97 else out
with wave.open("voice_in.wav", "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
def rms(x): return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
for s, e, *_ in fx[:0]:
    print(f"{s:5.1f} dry {rms(a[int(s*SR):int(e*SR)]):6.1f}  tail(0.5s after) dry {rms(a[int(e*SR):int((e+.5)*SR)]):6.1f} wet {rms(out[int(e*SR):int((e+.5)*SR)]):6.1f}")
