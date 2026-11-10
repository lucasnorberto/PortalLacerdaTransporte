"""Optimize fleet photos for web and strongly obscure license plates."""
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(
    r"C:\Users\ghlac\.cursor\projects\d-Projeto-pai-PortalLacerdaTransporte\assets"
)
OUT = ROOT / "images"

JOBS = [
    {
        "src": ASSETS
        / "WhatsApp_Image_2026-11-10_at_08.27.07-9ee52c90-e4c4-405b-9711-238a50a8ab8f.jpg",
        "dst": OUT / "caminhao-bau.jpg",
        # Front plate on red bumper (side-front angle)
        "plates": [(0.08, 0.80, 0.30, 0.96)],
        "max_side": 1400,
        "quality": 82,
    },
    {
        "src": ASSETS
        / "WhatsApp_Image_2026-11-10_at_08.27.06-bf5afa38-cb74-452e-a9aa-a59f48941ba3.jpg",
        "dst": OUT / "plataforma-carga.jpg",
        # Rear plate centered under FACCHINI
        "plates": [(0.34, 0.60, 0.56, 0.71)],
        "max_side": 1400,
        "quality": 82,
    },
]


def obscure_plates(img: Image.Image, plates) -> Image.Image:
    w, h = img.size
    out = img.copy()
    for l, t, r, b in plates:
        box = (int(l * w), int(t * h), int(r * w), int(b * h))
        # Sample surrounding color for a natural cover
        pad = 8
        sample = out.crop(
            (
                max(0, box[0] - pad),
                max(0, box[1] - pad),
                min(w, box[2] + pad),
                min(h, box[3] + pad),
            )
        )
        # Heavy blur + pixelate
        region = out.crop(box)
        pw, ph = region.size
        tiny = region.resize((max(1, pw // 20), max(1, ph // 20)), Image.Resampling.BILINEAR)
        region = tiny.resize((pw, ph), Image.Resampling.NEAREST)
        region = region.filter(ImageFilter.GaussianBlur(radius=12))
        # Darken slightly so characters disappear
        region = ImageEnhance.Brightness(region).enhance(0.85)
        region = region.filter(ImageFilter.GaussianBlur(radius=10))
        out.paste(region, box[:2])

        # Soft rounded rect overlay sampled from nearby pixels
        avg = sample.resize((1, 1), Image.Resampling.BOX).getpixel((0, 0))
        overlay = Image.new("RGBA", out.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.rounded_rectangle(box, radius=6, fill=(*avg[:3], 210))
        out = Image.alpha_composite(out.convert("RGBA"), overlay).convert("RGB")
    return out


def resize_max(img: Image.Image, max_side: int) -> Image.Image:
    w, h = img.size
    scale = min(1.0, max_side / max(w, h))
    if scale >= 1.0:
        return img
    nw, nh = int(w * scale), int(h * scale)
    return img.resize((nw, nh), Image.Resampling.LANCZOS)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for job in JOBS:
        img = Image.open(job["src"]).convert("RGB")
        img = obscure_plates(img, job["plates"])
        img = resize_max(img, job["max_side"])
        img = ImageEnhance.Sharpness(img).enhance(1.05)
        img.save(job["dst"], "JPEG", quality=job["quality"], optimize=True, progressive=True)
        print(f"wrote {job['dst'].name} {img.size} {job['dst'].stat().st_size} bytes")


if __name__ == "__main__":
    main()
