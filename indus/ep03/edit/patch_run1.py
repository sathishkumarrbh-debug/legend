import numpy as np, cv2
from PIL import Image
import patch as P
S = 941 / 470
sc = lambda pts: [(int(x * S), int(y * S)) for x, y in pts]
im = Image.open("images/ai1.png").convert("RGB")
_, m = P.inpaint_white(im, sc([(300, 262), (445, 262), (452, 420), (400, 640), (340, 836), (20, 836), (30, 640), (150, 470), (215, 360), (240, 340)]), thr=150, keep=[sc([(95, 270), (215, 270), (215, 418), (95, 418)])])
clean = P.quilt_fill(im, m, (10, 860, 270, 1300), patch=110)
clean.save("images/ai1_clean.png")
P.lay_row_packed(clean, sc([(205, 770)])[0], sc([(385, 300)])[0], r=0.87, squash=0.6, gap=0.1).save("images/ai1_fix.png")
