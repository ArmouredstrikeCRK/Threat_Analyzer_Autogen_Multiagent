# agents/vision_assistant_agent.py

from autogen import AssistantAgent

class VisionAssistantAgent(AssistantAgent):
    def __init__(self, name: str, prompt: str):
        super().__init__(
            name=name,
            system_message=f"Process image with prompt:\n\n{prompt}"
        )
        self.prompt = prompt

    def analyze(self, image_bytes: bytes, vision_call_fn):
        """
        Runs the given vision function (e.g., local_llama32)
        with this agent's assigned prompt.
        """
        print(f"[{self.name}] Running analysis...")
        response = vision_call_fn(image_data=image_bytes, prompt=self.prompt)
        return response
