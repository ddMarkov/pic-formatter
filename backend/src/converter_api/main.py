from typing import Literal

import pillow_heif
from fastapi import FastAPI, UploadFile

app = FastAPI()
pillow_heif.register_heif_opener()

TargetFmt = Literal["png", "jpeg", "webp", "tiff", "pdf"]


@app.get("/")
def read_root():
    pass


@app.post("/convert")
def convert_img(files: list[UploadFile], target_format: str):
    if len(files) == 1:
        pass
