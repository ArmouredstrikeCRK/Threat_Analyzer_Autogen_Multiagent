# backend/main.py
from fastapi import FastAPI, UploadFile, File
from backend.threat_pipeline import analyze_image
from io import BytesIO
from PIL import Image

app = FastAPI()

@app.post("/analyze_image_agent")
async def analyze_image_endpoint(file: UploadFile=File(...)):
    path = f"/tmp/{file.filename}"
    with open(path,"wb") as f: f.write(await file.read())
    return analyze_image(path)



