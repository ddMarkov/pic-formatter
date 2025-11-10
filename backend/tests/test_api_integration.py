from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from src.converter_api.main import app

client = TestClient(app)
DATA_DIR = Path(__file__).parent / "data"


def load_bytes(name: str) -> bytes:
    return (DATA_DIR / name).read_bytes()


def test_convert_heic_to_png_via_api():
    data = load_bytes("sample.HEIC")

    files = {"file": ("sample.HEIC", data, "image/heic")}

    resp = client.post("/convert", files=files)
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("image/png")

    img = Image.open(BytesIO(resp.content))
    _ = img.load()
    assert img.size[0] > 0 and img.size[1] > 0


def test_convert_non_heic_rejected():
    data = load_bytes("sample.jpg")

    files = {
        "file": ("sample.jpg", data, "image/jpeg"),
    }

    resp = client.post(
        "/convert",
        data={"target_format": "png"},
        files=files,
    )

    assert resp.status_code == 400
    assert "not heif" in resp.text.lower() or "not heic" in resp.text.lower()


def test_convert_invalid_bytes_rejected():
    data = b"not an image"

    files = {
        "file": ("fake.heic", data, "image/heic"),
    }

    resp = client.post(
        "/convert",
        data={"target_format": "png"},
        files=files,
    )

    assert resp.status_code == 400
    assert "invalid image" in resp.text.lower()
