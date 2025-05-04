import os
from autogen import UserProxyAgent
from agents.image_analyzer_agent import ImageAnalyzerAgent
from agents.threat_evaluator_agent import ThreatEvaluatorAgent

PROMPT_DIR = "prompts"

def read_prompt(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

class VisionThreatOrchestrator(UserProxyAgent):
    def __init__(self):
        super().__init__(
            name="Coordinator",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False}
        )
        self.v_agent = ImageAnalyzerAgent()
        self.t_agent = ThreatEvaluatorAgent()

        # Scan prompts/ for all your .txt files and load them
        self.prompts = {}
        for fn in os.listdir(PROMPT_DIR):
            if not fn.endswith(".txt"):
                continue
            tag = os.path.splitext(fn)[0].upper()  # e.g. "object_detection.txt" → "OBJECT_DETECTION"
            full_path = os.path.join(PROMPT_DIR, fn)
            self.prompts[tag] = read_prompt(full_path)

    def run_sequence(self, image_bytes: bytes):
        vision_outputs = {}

        # 1) Ask every prompt (in the directory) in order
        for tag, prompt in self.prompts.items():
            raw = self.v_agent.analyze_with_prompt(image_bytes, prompt)
            vision_outputs[tag] = raw

        # 2) Early-exit check
        scene   = vision_outputs.get("MILITARY_CONTEXT_ANALYSIS", "").lower()
        objects = vision_outputs.get("OBJECT_DETECTION", "").lower()
        if "civilian" in scene and "weapon" not in objects:
            return {
                "vision_analysis": vision_outputs,
                "raw_agent_outputs": vision_outputs,
                "threat_level": "0 – Non-military image"
            }

        # 3) Classify: join all the *raw* vision outputs into one summary
        summary = "\n\n".join(f"[{tag}]\n{vision_outputs[tag]}" for tag in vision_outputs)
        threat  = self.t_agent.evaluate(summary)

        return {
            "vision_analysis":    vision_outputs,
            "raw_agent_outputs":  vision_outputs,
            "threat_level":       threat
        }
