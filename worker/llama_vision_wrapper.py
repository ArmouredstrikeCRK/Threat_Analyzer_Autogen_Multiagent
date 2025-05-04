import requests
import base64

# HTTP-based wrapper for LLaMA 3.2 Vision via local Ollama daemon
# Uses host.docker.internal to reach the host from macOS Docker container

def local_llama32(image_data: bytes, prompt: str,
                   model_url: str = "http://host.docker.internal:11434/api/generate") -> str:
    """
    Send image and prompt to Ollama vision model over HTTP and return the result.

    :param image_data: Raw bytes of the PNG image
    :param prompt: Prompt text for the vision model
    :param model_url: HTTP endpoint for the Ollama generate API
    :return: The vision model's textual response
    """
    # Encode image to base64 for transport
    image_b64 = base64.b64encode(image_data).decode('utf-8')

    payload = {
        "model": "llama3.2-vision",
        "prompt": prompt,
        "images": [image_b64]
    }

    try:
        res = requests.post(model_url, json=payload, timeout=60)
        res.raise_for_status()
        data = res.json()
        # Ollama's HTTP API returns the generated text under 'response'
        return data.get("response", "[No response field]")
    except Exception as e:
        return f"[Ollama HTTP Error]: {e}"
