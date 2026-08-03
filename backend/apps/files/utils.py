import io

from PIL import Image, ImageOps

WEBP_QUALITY = 82


def resize_and_encode(pil_image: Image.Image, box: tuple[int, int]) -> bytes:
    img = ImageOps.exif_transpose(pil_image)
    img = img.convert("RGB")
    img.thumbnail(box, Image.LANCZOS)

    buffer = io.BytesIO()
    img.save(buffer, format="WEBP", quality=WEBP_QUALITY, method=6)
    return buffer.getvalue()
