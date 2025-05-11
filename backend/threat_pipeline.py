# threat_pipeline.py
from PIL import Image
from io import BytesIO
from agents.user_proxy_orchestrator import VisionThreatOrchestrator

orch = VisionThreatOrchestrator()

def analyze_image(image_path: str, request_type: str = None):
    img = Image.open(image_path)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return orch.run_sequence(buf.getvalue(), request_type=request_type)
