"""Indus Files #2 assets (fxkit). Run from the episode folder."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, fxkit as fx
I = "images/"
todo = sys.argv[1:] or ["hook", "kish", "map1", "map2", "seal", "ending", "sfx"]
B = (38.0, 80.0, 18.0, 38.0); INDUS = (68.6, 27.6)
if "hook" in todo: fx.punch_hook(I + "ai1.png", I + "hook.mp4", focus=(0.45, 0.62), chips_from=(0.3, 0.80, 0.95, 0.97), steam=False)
if "kish" in todo: fx.zoom_rings(I + "kish_seal_beads.jpg", I + "kish.mp4", (0, 0, 500, 670), (40, 25, 380, 360),
                                 rings=[{"box": (60, 40, 360, 340), "t": 1.0, "color": "gold"}], label="REAL: INDUS SEAL FOUND AT KISH, IRAQ", push=(0.1, 0.9), dur=5)
if "map1" in todo: fx.arc_map(INDUS, {"KISH": (44.6, 32.5), "UR": (46.1, 30.96)}, B, I + "map_iraq.mp4", src_name="INDUS VALLEY", caption="2,000+ KM APART", dur=4.5, draw=(0.05, 0.4), cap_t=0.3)
if "map2" in todo: fx.arc_map(INDUS, {"AKKAD": (44.4, 33.1)}, B, I + "map_meluhha.mp4", src_name="MELUHHA?", caption="SHIPS OF MELUHHA TO AKKAD", dur=5)
if "seal" in todo:
    W, H = 1280, 661
    fx.zoom_rings(I + "shuilishu_seal.jpg", I + "seal_reveal.mp4", (0, 0, W, H), (430, 60, 900, 620), rings=[], label="REAL: SEAL OF SHU-ILISHU · LOUVRE, c. 2200 BC", push=(0.0, 0.9), dur=6)
    fx.zoom_rings(I + "shuilishu_seal.jpg", I + "seal_rings.mp4", (330, 40, 980, 640), (0, 30, 470, 640),
                  rings=[{"box": (30, 70, 190, 560), "t": 1.6}],
                  top_text="CUNEIFORM INSCRIPTION", label="REAL: SEAL OF SHU-ILISHU · LOUVRE, c. 2200 BC", push=(0.0, 1.2), dur=6)
if "ending" in todo: fx.ending(I + "ai6.png", I + "ending.mp4", ["THE INDUS", "SCRIPT"], ["WHY CAN'T", "WE READ IT?"], "INDUS FILES  #3", q_at=2.7, dur=6.5)
if "sfx" in todo:   # sea swell for the ships
    SR = 44100; n = int(3.5 * SR); t = np.arange(n) / SR; r = np.random.default_rng(9)
    w = fx._bp(r.normal(size=n), 150, 2500) * (0.35 + 0.65 * np.sin(np.pi * t / 3.5) ** 2) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.6 * t))
    fx._save("../sfx", "waves", w)
