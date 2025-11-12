from typing import Annotated
from urllib.parse import quote

import pillow_heif
from fastapi import FastAPI, File, HTTPException, Response, UploadFile

from services.convert import (
    ImageIsNotHEIFError,
    InvalidImageError,
    convert_heic_to_png,
    load_image,
)

app = FastAPI()
pillow_heif.register_heif_opener()


def _safe_filename(name: str, ext: str = ".png") -> str:
    # strip path parts and control chars; force .png
    base = (name or "converted").split("/")[-1].split("\\")[-1]
    base = "".join(ch for ch in base if 32 <= ord(ch) < 127)  # ASCII-ish
    base = base.rsplit(".", 1)[0]  # drop existing extension
    if not base:
        base = "converted"
    return f"{base}{ext}"


@app.post("/convert")
async def convert_img(file: Annotated[UploadFile, File(...)]):
    data = await file.read()
    try:
        img = load_image(data)
    except ImageIsNotHEIFError:
        raise HTTPException(status_code=400, detail="not heif")
    except InvalidImageError:
        raise HTTPException(status_code=400, detail="invalid image")

    png_bytes = convert_heic_to_png(img)

    name = _safe_filename(file.filename or "converted.png", ext=".png")
    cd = f"attachment; filename=\"{name}\"; filename*=UTF-8''{quote(name)}"

    return Response(
        content=png_bytes,
        media_type="image/png",
        headers={"Content-Disposition": cd},
    )
