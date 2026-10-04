"""Extract the ten real Dholavira signs (Siyajkak drawing) as clean solid masks."""
import cv2, numpy as np
im = cv2.imread("images/ten_signs_drawing.jpg", 0)
S = 6
big = cv2.resize(im, None, fx=S, fy=S, interpolation=cv2.INTER_CUBIC)
ink = (big < 150).astype(np.uint8) * 255
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))
solid = cv2.morphologyEx(ink, cv2.MORPH_CLOSE, k)
solid = cv2.GaussianBlur(solid, (9, 9), 0); solid = (solid > 127).astype(np.uint8) * 255
cols = (solid > 0).any(0)
runs, x = [], 0
while x < len(cols):
    if cols[x]:
        s = x
        while x < len(cols) and cols[x]: x += 1
        runs.append((s, x))
    x += 1
runs = [r for r in runs if r[1] - r[0] > 20]
print(len(runs), runs)
masks = []
for a, b in runs:
    c = solid[:, a:b]; rows = np.where(c.any(1))[0]; c = c[rows[0]:rows[-1] + 1]
    masks.append(c)
np.save("images/sign_masks.npy", np.array(masks, dtype=object), allow_pickle=True)
strip = np.full((solid.shape[0], solid.shape[1]), 0, np.uint8); strip[:] = solid
cv2.imwrite("images/signs_solid.png", 255 - strip)
