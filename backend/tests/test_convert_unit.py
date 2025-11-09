from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from src.services.convert import (
    ImageIsNotHEIFError,
    InvalidImageError,
    convert_heic_to_png,
    load_image,
)

DATA_DIR = Path(__file__).parent / "data"


def load_bytes(name: str) -> bytes:
    return (DATA_DIR / name).read_bytes()


def test_load_image_valid_heic():
    data = load_bytes("sample.HEIC")
    img = load_image(data)

    assert isinstance(img, Image.Image)
    assert img.size[0] > 0 and img.size[1] > 0


def test_load_image_jpg_raises():
    data = load_bytes("sample.jpg")
    with pytest.raises(ImageIsNotHEIFError):
        _ = load_image(data)


def test_load_image_invalid_bytes_raises():
    data = b"this is not an image"
    with pytest.raises(InvalidImageError):
        _ = load_image(data)


def test_convert_heic_to_png():
    raw = load_bytes("sample.HEIC")
    img = load_image(raw)

    out_bytes = convert_heic_to_png(img)

    out = BytesIO(out_bytes)
    png = Image.open(out)
    _ = png.load()

    assert png.size == img.size
    assert png.mode in ("RGB", "RGBA")
