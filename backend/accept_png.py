from fastapi import FastAPI, UploadFile, File

async def accept_png(image: UploadFile = File(...)):
    contents = await image.read()
    with open(f"uploads/{image.filename}", "wb") as file:
        file.write(contents)
    return {"filename": image.filename, "message": "Upload successfully!"}