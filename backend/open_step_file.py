from fastapi.responses import FileResponse
import os

#This script opens a step file to download 
def open_step_file():
  file_path = os.path.abspath("test.STEP")
  return FileResponse(path=file_path, filename="test.STEP", media_type="application/octet-stream")
