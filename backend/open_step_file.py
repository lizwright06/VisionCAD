from fastapi.responses import FileResponse
from fastapi import HTTPException
from pathlib import Path

#This script opens a step file to download 
def open_step_file():
  file_path = Path(__file__).resolve().parent / "generated_step_files" / "model.step"
  if not file_path.exists():
    raise HTTPException(status_code=404, detail="STEP file not found")
  return FileResponse(path=str(file_path), filename="model.step", media_type="application/octet-stream")

# def open_onshape():
#  url = "https://cad.onshape.com"
#  driver = webdriver.Chrome()
#  driver.get(url)
