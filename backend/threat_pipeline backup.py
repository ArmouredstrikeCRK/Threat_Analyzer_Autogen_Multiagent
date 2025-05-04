from PIL import Image
from io import BytesIO
from agents.image_analyzer_agent import ImageAnalyzerAgent
from agents.threat_evaluator_agent import ThreatEvaluatorAgent

# Initialize agents
image_analyzer = ImageAnalyzerAgent()
threat_evaluator = ThreatEvaluatorAgent()

# Function to analyze image and classify threat
def analyze_image(image_path: str):
    # Open the image using PIL
    try:
        img = Image.open(image_path)
    except Exception as e:
        return {"error": f"Error opening image: {str(e)}"}

    # Convert image to bytes format suitable for Ollama
    img_byte_array = BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()

    # Generate caption from Llama 3.2 Vision model (Image Captioning)
    vision_response = image_analyzer.analyze_image(img_byte_array)
    if "error" in vision_response:
        return {"error": "Image description not generated."}

    description = vision_response.get("description", "")

    if not description:
        return {"error": "Image description not available."}

    # Now classify the threat level using DeepSeek model (Threat Classification)
    threat_response = threat_evaluator.evaluate_threat(description)
    
    if "error" in threat_response:
        return {"error": "Error in threat classification."}

    return {"description": description, "threat_level": threat_response}
