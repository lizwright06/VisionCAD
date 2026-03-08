from fastapi import FastAPI, UploadFile, File
import os

async def accept_png(image: UploadFile = File(...)):
    os.remove('./drawings/1.png')
    contents = await image.read()
    with open(f"drawings/1.png", "wb") as file:
        file.write(contents)
    return {"filename": image.filename, "message": "Upload successfully!"}