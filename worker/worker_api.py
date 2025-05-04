# worker/worker_api.py

from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
from io import BytesIO
from models.llama_vision_wrapper import local_llama32

app = FastAPI()

@app.get("/")                              
async def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_image(
    prompt: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        image = Image.open(BytesIO(await file.read()))
        buf = BytesIO()
        image.save(buf, format="PNG")
        image_bytes = buf.getvalue()

        result = local_llama32(image_data=image_bytes, prompt=prompt)
        return {"result": result}

    except Exception as e:
        return {"error": str(e)}
