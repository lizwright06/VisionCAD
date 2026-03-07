from fastapi import FastAPI
from image_analysis import router  # replace with your actual filename without .py

app = FastAPI()
app.include_router(router)

@app.get("/health")
def health():
    return {"ok": True}