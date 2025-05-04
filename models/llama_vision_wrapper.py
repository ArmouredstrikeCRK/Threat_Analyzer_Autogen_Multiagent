# models/llama_vision_wrapper.py

# models/llama_vision_wrapper.py
from autogen_ext.models.ollama import OllamaChatCompletionClient
import ollama

# Pick one temperature for all calls
STATIC_TEMPERATURE = 0.05

def local_llama32(
    image_data: bytes,
    prompt: str,
    model: str = "llama3.2-vision",
):
    try:
        res = ollama.chat(
            model=model,
            messages=[{
                "role": "user",
                "content": prompt,
                "images": [image_data]
            }],
            options={"temperature": STATIC_TEMPERATURE}
        )
        return res["message"]["content"]
    except Exception as e:
        return f"[LLaMA Error] {str(e)}"






