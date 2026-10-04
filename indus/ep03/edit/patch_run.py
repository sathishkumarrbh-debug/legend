from PIL import Image
import patch as P
S = 941 / 470
sc = lambda pts: [(int(x * S), int(y * S)) for x, y in pts]
# image 1 (hook): remove invented symbols, lay the real ten in the dirt
im = Image.open("images/ai1.png").convert("RGB")
poly = sc([(300, 262), (445, 262), (452, 420), (400, 640), (340, 836), (20, 836), (30, 640), (150, 470), (215, 360), (240, 340)])
hand = [sc([(95, 270), (215, 270), (215, 418), (95, 418)])]
clean, m = P.inpaint_white(im, poly, thr=150, keep=hand)
clean.save("images/ai1_clean.png")
P.lay_row(clean, sc([(185, 735)])[0], sc([(370, 300)])[0], int(170 * S), int(48 * S), squash=0.5).save("images/ai1_fix.png")
# images 2 and 6: real signboard on the gate
P.board_on_quad(Image.open("images/ai2.png"), [(100, 398), (897, 250), (902, 396), (100, 542)]).save("images/ai2_fix.png")
P.board_on_quad(Image.open("images/ai6.png"), [(122, 362), (866, 442), (866, 632), (118, 545)], glow=0.25).save("images/ai6_fix.png")
