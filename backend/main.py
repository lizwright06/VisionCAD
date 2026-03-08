from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import json

try:
    from .open_step_file import open_step_file
    from .accept_png import accept_png
    from .image_analysis import router as analysis_router
except ImportError:
    # Allows running as `uvicorn main:app` from `backend/`
    # and `uvicorn backend.main:app` from repo root.
    from open_step_file import open_step_file
    from accept_png import accept_png
    from image_analysis import file_to_data_url, llm_analyze, OBSERVED_IMAGE_PATH
    from cadGeneration import generateCad

app = FastAPI()
# app.include_router(analysis_router)

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.get("/download-step-file")
def download_step_file():
    return open_step_file()

# @app.post("/upload")
# async def upload(image: UploadFile = File(...)):
#     result = await accept_png(image)
#     return result
@app.post("/upload")
async def upload(image: UploadFile = File(...)):
    result = await accept_png(image)

    data_url = file_to_data_url(OBSERVED_IMAGE_PATH)

    analysis_str = await llm_analyze(data_url)

    try:
        analysis_json = json.loads(analysis_str)
    except json.JSONDecodeError:
        analysis_json = {"error": "LLM returned invalid JSON", "raw": analysis_str}
    print(analysis_json)
    
    generateCad(analysis_json["objects"])
    
    return {
        "upload": result,
        "analysis": analysis_json
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

