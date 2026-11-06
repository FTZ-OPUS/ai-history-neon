"""Fetch and crop Wikimedia Commons images with source/attribution metadata."""
import html
import json
import re
import time
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
API = "https://commons.wikimedia.org/w/api.php"
FILES = {
    "turing": "Alan Turing (1951).jpg",
    "mccarthy": "John McCarthy (computer scientist) Stanford 2006 (272020300).jpg",
    "rosenblatt": "Frank Rosenblatt.jpg",
    "hinton": "Geoffrey E. Hinton, 2024 Nobel Prize Laureate in Physics (cropped1).jpg",
    "deepblue": "Deep Blue.jpg",
    "leedol": "Lee Se-Dol - 2016 (cropped).jpg",
}
HEADERS = {"User-Agent": "NeonHistoryFilm/1.0 (educational video; image attribution preserved)"}


def clean(text):
    return html.unescape(re.sub("<[^>]*>", "", text or "")).strip()


def main():
    session = requests.Session()
    session.headers.update(HEADERS)
    manifest = {}
    for key, title in FILES.items():
        data = session.get(API, params={
            "action": "query", "titles": "File:" + title, "prop": "imageinfo",
            "iiprop": "url|extmetadata", "iiurlwidth": 1200, "format": "json",
        }, timeout=40).json()
        page = next(iter(data["query"]["pages"].values()))
        if "imageinfo" not in page:
            raise RuntimeError(f"Missing source file: {title}")
        info = page["imageinfo"][0]
        meta = info.get("extmetadata", {})
        url = info["url"]
        output = ASSETS / f"{key}.png"
        if output.exists():
            manifest[key] = {
                "file": f"assets/{key}.png", "source_file": page["title"],
                "source_page": info["descriptionurl"],
                "license": clean(meta.get("LicenseShortName", {}).get("value")),
                "license_url": clean(meta.get("LicenseUrl", {}).get("value")),
                "author": clean(meta.get("Artist", {}).get("value")),
                "changes": "Cropped to circle; contrast and saturation adjusted.",
            }
            print(key, "existing", manifest[key]["license"])
            continue
        for attempt in range(3):
            try:
                response = session.get(url, timeout=28)
                response.raise_for_status()
                im = Image.open(BytesIO(response.content)).convert("RGB")
                break
            except (requests.RequestException, OSError):
                if attempt == 2:
                    raise
                time.sleep(1 + attempt)
        if key in {"dartmouth", "deepblue"}:
            im = ImageOps.fit(im, (1100, 780), centering=(0.5, 0.5))
        else:
            im = ImageOps.fit(im, (800, 800), centering=(0.5, 0.38))
        im = ImageEnhance.Contrast(im).enhance(1.12)
        im = ImageEnhance.Color(im).enhance(0.82)
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).ellipse((5, 5, im.width - 5, im.height - 5), fill=255)
        im.putalpha(mask)
        im.save(ASSETS / f"{key}.png", optimize=True)
        manifest[key] = {
            "file": f"assets/{key}.png", "source_file": page["title"],
            "source_page": info["descriptionurl"],
            "license": clean(meta.get("LicenseShortName", {}).get("value")),
            "license_url": clean(meta.get("LicenseUrl", {}).get("value")),
            "author": clean(meta.get("Artist", {}).get("value")),
            "changes": "Cropped to circle; contrast and saturation adjusted.",
        }
        print(key, im.size, manifest[key]["license"])
    (ASSETS / "attribution.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
