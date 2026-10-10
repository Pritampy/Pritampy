#!/usr/bin/env python3
"""
Prepare the photo for clean ASCII conversion:
  1. remove the background (rembg or OpenCV GrabCut / chroma-key fallback)
  2. bilateral-smooth away noise and textures while keeping drawn lines sharp
  3. stretch tones so skin lands near bright and hair/lines stay dark
  4. darken line work (difference-of-gaussians ridges)
  5. composite onto white and crop square around the subject

Output: source-prepped.png (grayscale), consumed by make_ascii_svg.py.

    python scripts/prep_photo.py [input.png] [output.png]
"""
import os
import sys
import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "avatar.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

LINE_WEIGHT = 0.6

# 1. Remove background
bgr = cv2.imread(INP)
if bgr is None:
    raise FileNotFoundError(f"Cannot load image {INP}")

h, w = bgr.shape[:2]
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

# Blue background detection (typical studio blue background)
lower_blue = np.array([90, 70, 40])
upper_blue = np.array([135, 255, 255])
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

if np.count_nonzero(blue_mask) > (h * w * 0.15):
    # Studio blue background detected: use precise fast GrabCut segmentation
    subject_mask = cv2.bitwise_not(blue_mask)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    subject_mask = cv2.morphologyEx(subject_mask, cv2.MORPH_OPEN, kernel)
    subject_mask = cv2.morphologyEx(subject_mask, cv2.MORPH_CLOSE, kernel)

    border_mask = np.zeros_like(subject_mask)
    border_mask[10:h-5, 15:w-15] = 255
    subject_mask = cv2.bitwise_and(subject_mask, border_mask)

    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    gc_mask = np.where(subject_mask > 0, cv2.GC_PR_FGD, cv2.GC_BGD).astype('uint8')
    gc_mask[0:10, :] = cv2.GC_BGD
    gc_mask[h-5:h, :] = cv2.GC_BGD
    gc_mask[:, 0:15] = cv2.GC_BGD
    gc_mask[:, w-15:w] = cv2.GC_BGD
    gc_mask[int(h*0.25):int(h*0.6), int(w*0.35):int(w*0.65)] = cv2.GC_FGD

    cv2.grabCut(bgr, gc_mask, None, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_MASK)
    alpha = np.where((gc_mask == cv2.GC_FGD) | (gc_mask == cv2.GC_PR_FGD), 255, 0).astype('uint8')
else:
    try:
        from rembg import remove
        cut = remove(Image.open(INP).convert("RGBA"))
        alpha = np.array(cut.split()[-1])
    except Exception:
        alpha = np.full((h, w), 255, np.uint8)

# 2. Smooth texture & lines
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
smooth = gray.copy()
for _ in range(3):
    smooth = cv2.bilateralFilter(smooth, 9, 40, 9)

# 3. Tone stretch over subject only
fg_pixels = smooth[alpha > 128]
if len(fg_pixels) > 0:
    lo, hi = np.percentile(fg_pixels, [2, 92])
else:
    lo, hi = 20, 230
tone = np.clip((smooth.astype(np.float32) - lo) / max(1.0, (hi - lo)), 0, 1)

# 4. Dark-on-light ridges -> darken (DoG)
fine = cv2.GaussianBlur(smooth, (0, 0), 1.5).astype(np.float32)
coarse = cv2.GaussianBlur(smooth, (0, 0), 6).astype(np.float32)
lines = np.clip((coarse - fine) / 40.0, 0, 1)
out = np.clip(tone - LINE_WEIGHT * lines, 0, 1) * 255

# 5. Composite onto white
feathered_mask = cv2.GaussianBlur(alpha.astype(np.float32) / 255.0, (0, 0), 1.0)
out = out * feathered_mask + 255.0 * (1.0 - feathered_mask)

# Crop square around subject
ys, xs = np.where(alpha > 20)
if len(xs) > 0 and len(ys) > 0:
    side = max(xs.max() - xs.min(), ys.max() - ys.min()) + 40
    cx, cy = (xs.min() + xs.max()) // 2, (ys.min() + ys.max()) // 2
else:
    side = min(h, w)
    cx, cy = w // 2, h // 2

canvas = np.full((side, side), 255, np.uint8)
x0, y0 = cx - side // 2, cy - side // 2
sx0, sy0 = max(x0, 0), max(y0, 0)
sx1, sy1 = min(x0 + side, out.shape[1]), min(y0 + side, out.shape[0])
canvas[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = out[sy0:sy1, sx0:sx1].astype(np.uint8)

cv2.imwrite(OUT, canvas)
print("Wrote", OUT, canvas.shape)
