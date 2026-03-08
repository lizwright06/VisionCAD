from fastapi import FastAPI, UploadFile, APIRouter, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from open_step_file import open_step_file
from accept_png import accept_png

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
    
    async def broadcast(self):
        for connection in self.active_connections:
            await connection.send_text("DOWNLOAD COMPLETE")

manager = ConnectionManager()

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            await manager.broadcast() # Broadcasts the message to all connected clients
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
