from fastapi import FastAPI
from backend.open_step_file import open_step_file

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/download-step-file")
def download_step_file():
    return open_step_file()