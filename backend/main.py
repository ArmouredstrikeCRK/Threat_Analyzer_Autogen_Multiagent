from fastapi import FastAPI, UploadFile, File, Form
from backend.threat_pipeline import analyze_image
from io import BytesIO
from PIL import Image

app = FastAPI()

@app.post("/analyze_image_agent")
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    request_type: str = Form(...),  # Additional parameter for request type
    additional_param: str = Form(None)  # Optional additional parameter
):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    
    # Pass the additional parameters to the analyze_image function
    return analyze_image(path, request_type=request_type)

