

import ollama
import re

STATIC_TEMPERATURE = 0.05  # the one and only temperature

def extract_think_and_classification(response: str):
    thinks = re.findall(r"<think>(.*?)</think>", response, re.DOTALL|re.IGNORECASE)
    reasoning = thinks[-1].strip() if thinks else "No reasoning provided"
    classes = re.findall(r'\b([0-4])\b', response)
    classification = classes[-1] if classes else "Error: No valid classification found"
    return reasoning, classification

def local_deepseek(
    new_messages,
    model: str = "deepseek-r1:8b",
):
    try:
        res = ollama.chat(
            model=model,
            messages=new_messages,
            options={"temperature": STATIC_TEMPERATURE}
        )
        content = res["message"]["content"]
        reasoning, classification = extract_think_and_classification(content)
        return {
            "raw": content,
            "reasoning": reasoning,
            "threatLevel": int(classification) if classification.isdigit() else None
        }
    except Exception as e:
        return {"error": f"[DeepSeek Error] {str(e)}"}

