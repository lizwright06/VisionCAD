from typing import List

from fastapi import FastAPI, UploadFile, APIRouter, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

try:
    from .open_step_file import open_step_file
    from .accept_png import accept_png
    from .image_analysis import file_to_data_url, llm_analyze, OBSERVED_IMAGE_PATH
    from .cadGeneration import generateCad
except ImportError:
    # Allows running as `uvicorn main:app` from `backend/`
    # and `uvicorn backend.main:app` from repo root.
    from open_step_file import open_step_file
    from accept_png import accept_png
    from image_analysis import file_to_data_url, llm_analyze, OBSERVED_IMAGE_PATH
    from cadGeneration import generateCad

app = FastAPI()

router = APIRouter()
app.include_router(router)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
         self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str = "DOWNLOAD COMPLETE"):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

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
    print("calling analysis")
    analysis_str = await llm_analyze(data_url)

    try:
        analysis_json = json.loads(analysis_str)
    except json.JSONDecodeError:
        analysis_json = {"error": "LLM returned invalid JSON", "raw": analysis_str}
    print(analysis_json)
    
    generateCad(analysis_json["objects"])

    await manager.broadcast()
    
    return {
        "upload": result,
        "analysis": analysis_json
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
            await manager.broadcast() # Broadcasts the message to all connected clients
    except WebSocketDisconnect:
        manager.disconnect(websocket)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
