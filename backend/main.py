from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from open_step_file import open_step_file
from accept_png import accept_png

app = FastAPI()
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/download-step-file")
def download_step_file():
    return open_step_file()

@app.post("/upload")
async def upload(image: UploadFile = File(...)):
    result = await accept_png(image)
    return result

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
