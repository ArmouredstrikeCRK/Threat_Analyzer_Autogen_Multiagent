# agents/aggregator_agent.py
import os
from agents.image_analyzer_agent import ImageAnalyzerAgent
from agents.threat_evaluator_agent import ThreatEvaluatorAgent

PROMPT_DIR = "prompts"

def read_prompt(file_name):
    with open(os.path.join(PROMPT_DIR, file_name), "r") as file:
        return file.read()

def run_orchestrated_analysis(image_data):
    prompt_files = [
        "aggression_analysis.txt", 
        "civilian_presence.txt",
        "equipment_profiling.txt",
        "military_context_analysis.txt",
        "object_detection.txt",
        "tactical_layout.txt"
    ]

    vision_agent = ImageAnalyzerAgent()
    threat_agent = ThreatEvaluatorAgent()

    vision_responses = []

    for prompt_file in prompt_files:
        prompt = read_prompt(prompt_file)
        response = vision_agent.analyze_image_with_prompt(image_data, prompt)
        vision_responses.append(response)

        # Early exit if response is clearly non-threatening
        if "no military" in response.lower() and "civilian" in response.lower():
            break

    combined_context = "\n\n".join(vision_responses)
    threat = threat_agent.evaluate_threat(combined_context)

    return {
        "vision_analysis": vision_responses,
        "threat_level": threat
    }
