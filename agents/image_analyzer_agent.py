# agents/image_analyzer_agent.py

from autogen import AssistantAgent
#from models.ollama_clients import vision_client
from models.llama_vision_wrapper import local_llama32

class ImageAnalyzerAgent:
    def __init__(self):
       
        pass

    def analyze_with_prompt(self, image_bytes: bytes, prompt: str) -> str:
        # Use the local_llama32 model to analyze the image with the given prompt
        try:
            return local_llama32(image_bytes, prompt)
        except Exception as e:
            # Handle any exceptions that occur during analysis
            return f"Error during analysis: {str(e)}"