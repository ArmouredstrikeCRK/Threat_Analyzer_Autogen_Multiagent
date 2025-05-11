import os
from autogen import UserProxyAgent
from agents.image_analyzer_agent import ImageAnalyzerAgent
from agents.threat_evaluator_agent import ThreatEvaluatorAgent

PROMPT_DIR = "prompts"


def read_prompt(path: str) -> str:
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

        # Load all prompts from the directory
        self.prompts = {}
        for fn in os.listdir(PROMPT_DIR):
            if not fn.endswith(".txt"):
                continue
            tag = os.path.splitext(fn)[0].upper()
            full_path = os.path.join(PROMPT_DIR, fn)
            self.prompts[tag] = read_prompt(full_path)

    def run_sequence(self, image_bytes: bytes, request_type: str = "threat_analysis") -> dict:
        """
        request_type: 'threat_analysis' or 'vision_analysis'

        - 'vision_analysis': runs only the image prompts and returns their outputs.
        - 'threat_analysis': runs the full pipeline including threat evaluation.
        """
        # 1) Perform vision analysis for all prompts
        vision_outputs = {}
        for tag, prompt in self.prompts.items():
            raw = self.v_agent.analyze_with_prompt(image_bytes, prompt)
            vision_outputs[tag] = raw

        # If only vision analysis is requested, return here
        if request_type.lower() == "vision_analysis":
            return {
                "vision_analysis": vision_outputs,
                "raw_agent_outputs": vision_outputs
            }

        # 2) Early-exit check
        scene = vision_outputs.get("MILITARY_CONTEXT_ANALYSIS", "").lower()
        objects = vision_outputs.get("OBJECT_DETECTION", "").lower()

        # Terms indicating destructive or lethal context
        destructive_terms = ["blast", "destruction", "explosion", "deadbody","corpse","blood"]

        # Early-exit: civilian without weapons and without destructive scene terms
        if "civilian" in scene and "weapon" not in objects and not any(term in scene for term in destructive_terms):
            return {
                "vision_analysis": vision_outputs,
                "raw_agent_outputs": vision_outputs,
                "threat_level": "0 – Non-military image"
            }

        # 3) Build a combined summary of all raw vision outputs
        summary = "\n\n".join(f"[{tag}]\n{vision_outputs[tag]}" for tag in vision_outputs)
        threat = self.t_agent.evaluate(summary)

        return {
            "vision_analysis": vision_outputs,
            "raw_agent_outputs": vision_outputs,
            "threat_level": threat
        }
