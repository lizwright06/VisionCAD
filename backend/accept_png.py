from pathlib import Path

from fastapi import UploadFile, File

DRAWINGS_DIR = Path(__file__).resolve().parent / "drawings"
TARGET_IMAGE = DRAWINGS_DIR / "1.png"

async def accept_png(image: UploadFile = File(...)):
    contents = await image.read()
    DRAWINGS_DIR.mkdir(parents=True, exist_ok=True)
    with open(TARGET_IMAGE, "wb") as file:
        file.write(contents)
    return {"filename": image.filename, "message": "Upload successfully!"}
