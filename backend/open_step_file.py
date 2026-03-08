from fastapi.responses import FileResponse
import os

#This script opens a step file to download 
def open_step_file():
  file_path = os.path.abspath("generated_step_files/model.step")
  return FileResponse(path=file_path, filename="model.step", media_type="application/octet-stream")
