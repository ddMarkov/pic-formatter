from __future__ import annotations

import io

import pillow_heif
from PIL import Image, UnidentifiedImageError

pillow_heif.register_heif_opener()


class InvalidImageError(Exception):
    """Raised when bytes are not a valid image"""

    pass


class ImageIsNotHEIFError(Exception):
    """Raised when the image is valid but not a HEIF file"""

    pass


def load_image(data: bytes) -> Image.Image:
    """
    Decode HEIF bytes into a Pillow Image.
    Raises:
        - InvalidImageError: If the data is not a valid/supported image.
        - ImageIsNotHEIFError: If the image is valid but not HEIF/HEIC.
    """
    try:
        img = Image.open(io.BytesIO(data))
        if img.format not in ("HEIF", "HEIC"):
            raise ImageIsNotHEIFError(f"Image format is {img.format}, not HEIF/HEIC")

        _ = img.load()
        return img

    except (UnidentifiedImageError, IOError, SyntaxError):
        raise InvalidImageError("This file is corrupted or not an image")


def convert_heic_to_png(img: Image.Image) -> bytes:
    """
    Convert a Pillow Image to PNG format and return bytes.
    """
    output_buffer = io.BytesIO()
    img.save(output_buffer, format="PNG")
    return output_buffer.getvalue()
