"""Prepare the three character illustrations for the neon film.

White background is removed by flood-filling from the border only, so interior
whites (dresses, highlights) survive. Edge is eroded + feathered to avoid a
white fringe on the dark background.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "raw"
OUT = ROOT
JOBS = {
    "deepseek": dict(crop=(0, 308, 1552, 1240), scale=1.0, tol=26),
    "claude": dict(crop=None, scale=3.2, tol=24),
    "gpt": dict(crop=None, scale=3.2, tol=24),
}


def process(name, cfg):
    im = Image.open(SRC / f"raw_{name}.png").convert("RGB")
    if cfg["crop"]:
        im = im.crop(cfg["crop"])
    if cfg["scale"] != 1.0:
        im = im.resize((int(im.width * cfg["scale"]), int(im.height * cfg["scale"])), Image.LANCZOS)
    a = np.asarray(im).astype(np.int16)
    # near-white pixels, tolerant to JPEG noise
    near_white = (a.min(axis=2) > 255 - cfg["tol"]) & ((a.max(axis=2) - a.min(axis=2)) < 18)
    labels, count = ndimage.label(near_white)
    border_ids = set(np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]])))
    border_ids.discard(0)
    bg = np.isin(labels, list(border_ids))
    mask = (~bg).astype(np.uint8)
    # drop specks, then erode 1px so no white halo is left behind
    lab2, n2 = ndimage.label(mask)
    sizes = ndimage.sum(mask, lab2, range(1, n2 + 1))
    keep = {i + 1 for i, s in enumerate(sizes) if s > mask.size * 0.0004}
    mask = np.isin(lab2, list(keep)).astype(np.uint8)
    mask = ndimage.binary_erosion(mask, iterations=1).astype(np.uint8)
    alpha = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.4))
    rgba = im.convert("RGBA")
    rgba.putalpha(alpha)
    box = rgba.getbbox()
    if box:
        pad = 6
        box = (max(0, box[0] - pad), max(0, box[1] - pad),
               min(rgba.width, box[2] + pad), min(rgba.height, box[3] + pad))
        rgba = rgba.crop(box)
    rgba.save(OUT / f"{name}.png", optimize=True)
    arr = np.asarray(rgba)[:, :, 3] / 255.0
    print(f"{name:<9} size={rgba.size} opaque_ratio={float((arr > 0.5).mean()):.3f} "
          f"edge_alpha={float(arr[0].mean()):.3f}")


if __name__ == "__main__":
    for key, cfg in JOBS.items():
        process(key, cfg)
