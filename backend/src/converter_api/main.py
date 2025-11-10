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


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


@app.post("/convert")
async def convert_img(file: UploadFile = File(...)):
    content = await file.read()
    try:
        img_in_bytes = load_image(content)
    except ImageIsNotHEIFError:
        raise HTTPException(status_code=400)
    except InvalidImageError:
        raise HTTPException(status_code=400)
    png_bytes = convert_heic_to_png(img_in_bytes)
    return Response(content=png_bytes, media_type="image/png")
