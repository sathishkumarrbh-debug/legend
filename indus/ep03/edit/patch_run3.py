from PIL import Image
import patch as P
for n, poly, far, near, ratio, sh in [
    ("ai10", [(0, 720), (941, 1110), (941, 1310), (0, 860)], (55, 795), (905, 1225), 1.8, (0, -170)),
    ("ai9", [(0, 515), (941, 820), (941, 1075), (0, 690)], (55, 615), (905, 1000), 1.6, (0, 230))]:
    im = Image.open(f"images/{n}.png").convert("RGB")
    _, m = P.inpaint_white(im, poly, thr=140, grow=6)
    clean = P.clone_fill(im, m, sh); clean.save(f"images/{n}_clean.png")
    P.lay_row_line(clean, far, near, m, size_ratio=ratio, squash=0.8, bold=17).save(f"images/{n}_fix.png")
