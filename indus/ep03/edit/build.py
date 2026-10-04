"""Indus Files #3 assets (fxkit + board.py). Run from the episode folder."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fxkit as fx, board as B
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
I = "images/"
todo = sys.argv[1:] or ["hook", "ten", "size", "fall", "lit", "black", "count", "five", "prize", "ending"]
if "hook" in todo: fx.punch_hook(I + "ai1_fix.png", I + "hook.mp4", focus=(0.62, 0.55), chips_from=(0.3, 0.45, 0.9, 0.97), steam=False)
if "ten" in todo: B.clip_lit(I + "ten.mp4", dur=4.5, text=())
if "size" in todo: B.clip_size(I + "sign_size.mp4", dur=5.0)
if "fall" in todo:
    bg = ImageEnhance.Brightness(fx.cover(Image.open(I + "ai7_fix.png").convert("RGB")).filter(ImageFilter.GaussianBlur(10))).enhance(0.55)
    bg.save(I + "ai2_soft.png"); B.clip_board2(I + "board_fall.mp4", bg_image=I + "ai2_soft.png", dur=7.6, t_fall=1.0, t_sweep=3.45)
if "lit" in todo: B.clip_lit(I + "signs_lit.mp4", dur=4.5, text=())
if "black" in todo: Image.new("RGB", (1080, 1920), (6, 5, 4)).save(I + "black.png")
if "count" in todo: fx.counter(I + "ai4.png", I + "count_4000.mp4", 4000, top="WE HAVE FOUND", unit="PIECES OF WRITING", prefix="", suffix="+", window=(0.1, 1.5), dur=7)
if "five" in todo:
    bg = Image.blend(fx.cover(Image.open(I + "ai4.png").convert("RGB")).filter(ImageFilter.GaussianBlur(14)), Image.new("RGB", (1080, 1920)), 0.62)
    def frame(t):
        im = bg.copy().convert("RGBA"); d = ImageDraw.Draw(im); k = fx.ease(t / 0.35); s = int(210 * (1.25 - 0.25 * k))
        d.text((540, 520), "MOST ARE ONLY", font=fx.font(fx.F_TITLE, 54), fill=fx.WHITE, anchor="mm")
        d.text((540, 800), "4–5", font=fx.font(fx.F_BIG, s), fill=fx.GOLD + (int(255 * k),), anchor="mm", stroke_width=6, stroke_fill=(0, 0, 0))
        d.text((540, 960), "SIGNS LONG", font=fx.font(fx.F_BIG, 90), fill=fx.GOLD + (int(255 * k),), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
        return im
    fx.write_mp4(frame, 5.0, I + "five.mp4")
if "prize" in todo: fx.counter(I + "ai8_fix.png", I + "prize.mp4", 1000000, top="A PRIZE OF", unit="TO READ IT", prefix="$", suffix="", window=(0.3, 1.8), dur=7, bar=False)
if "ending" in todo:
    im6 = Image.open(I + "ai8_fix.png").convert("RGB"); sh = 330; c = Image.new("RGB", im6.size); c.paste(im6.crop((0, sh, im6.width, im6.height)), (0, 0)); c.paste(im6.crop((0, im6.height - sh, im6.width, im6.height)).transpose(Image.FLIP_TOP_BOTTOM), (0, im6.height - sh)); c.save(I + "ai6_end.png")
    fx.ending(I + "ai6_end.png", I + "ending.mp4", ["IF WE CAN'T", "READ THEM…"], ["WHO", "RULED THEM?"], "INDUS FILES  #4", q_at=1.0, dur=4.8)
