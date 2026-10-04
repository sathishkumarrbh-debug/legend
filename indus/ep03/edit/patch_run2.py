import numpy as np
from PIL import Image
import patch as P
# gates: keep the AI board, swap its symbols for the real ten
if 0: P.signs_on_quad(Image.open("images/ai7.png"), [(118, 318), (895, 266), (902, 410), (112, 450)],
                [(95, 290), (910, 235), (920, 400), (90, 455)], thr=150).save("images/ai7_fix.png")
if 0: P.signs_on_quad(Image.open("images/ai8.png"), [(112, 385), (868, 470), (868, 600), (112, 540)],
                [(100, 360), (875, 445), (875, 610), (100, 545)], thr=140, glow=0.18).save("images/ai8_fix.png")
# trench close-ups: erase invented row, lay the real ten along the same line
for n, poly, far, near, ratio, src in [
    ("ai10", [(0, 720), (941, 1110), (941, 1310), (0, 860)], (55, 795), (905, 1225), 1.8, (300, 200, 700, 560)),
    ("ai9", [(0, 515), (941, 820), (941, 1075), (0, 690)], (55, 615), (905, 1000), 1.6, (380, 1150, 941, 1550))]:
    im = Image.open(f"images/{n}.png").convert("RGB")
    _, m = P.inpaint_white(im, poly, thr=140, grow=7)
    clean, m = P.inpaint_white(im, poly, thr=140, grow=4)
    clean.save(f"images/{n}_clean.png")
    P.lay_row_line(clean, far, near, m, size_ratio=ratio, squash=0.8, bold=17).save(f"images/{n}_fix.png")
