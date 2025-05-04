# models/ollama_clients.py

from autogen_ext.models.ollama import OllamaChatCompletionClient
from pydantic import BaseModel

# Vision model
vision_client = OllamaChatCompletionClient(
    model="llama3.2-vision:latest",
       
)

# Threat schema
class ThreatLabel(BaseModel):
    threat_level: str

# Threat model
threat_client = OllamaChatCompletionClient(
    model="deepseek-r1:8b",
    response_format=ThreatLabel
)
