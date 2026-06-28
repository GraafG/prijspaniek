"""Generate Prijspaniek PWA icons with Pillow."""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(HERE, "icons")
os.makedirs(ICON_DIR, exist_ok=True)

BLUE = (10, 61, 145)
BLUE_D = (7, 28, 80)
YELLOW = (255, 210, 0)
WHITE = (255, 255, 255)


def rounded(size, radius_frac, fill):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(size * radius_frac)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=fill)
    return img


def draw_icon(size, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # background
    if maskable:
        d.rectangle([0, 0, size, size], fill=BLUE)
    else:
        bg = rounded(size, 0.22, BLUE)
        img.alpha_composite(bg)
        d = ImageDraw.Draw(img)

    s = size
    pad = s * (0.30 if maskable else 0.20)
    # yellow price tag (rotated rounded rect) with a hole
    tag = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    td = ImageDraw.Draw(tag)
    x0, y0 = s * 0.30, s * 0.30
    x1, y1 = s * 0.82, s * 0.72
    td.rounded_rectangle([x0, y0, x1, y1], radius=int(s * 0.07), fill=YELLOW)
    # hole
    hr = s * 0.035
    hx, hy = x0 + s * 0.075, y0 + s * 0.085
    td.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=BLUE)
    tag = tag.rotate(-18, center=(s / 2, s / 2), resample=Image.BICUBIC)
    img.alpha_composite(tag)

    # euro sign
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arialbd.ttf", int(s * 0.30))
    except Exception:
        font = ImageFont.load_default()
    txt = "€"
    bbox = d.textbbox((0, 0), txt, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((s - tw) / 2 - bbox[0] + s * 0.02, (s - th) / 2 - bbox[1] - s * 0.02),
           txt, font=font, fill=BLUE_D)
    return img


for size in (192, 512):
    draw_icon(size).save(os.path.join(ICON_DIR, f"icon-{size}.png"))
    draw_icon(size, maskable=True).save(os.path.join(ICON_DIR, f"maskable-{size}.png"))

# apple touch icon (no transparency, rounded handled by iOS)
apple = Image.new("RGBA", (180, 180), BLUE)
apple.alpha_composite(draw_icon(180, maskable=True))
apple.convert("RGB").save(os.path.join(ICON_DIR, "apple-touch-icon.png"))

# favicon
draw_icon(32).save(os.path.join(ICON_DIR, "favicon-32.png"))
draw_icon(180).save(os.path.join(ICON_DIR, "icon-180.png"))
print("icons written to", ICON_DIR)
