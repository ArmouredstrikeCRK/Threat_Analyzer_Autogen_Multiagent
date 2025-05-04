# agents/threat_evaluator_agent.py

from autogen import AssistantAgent
from models.deepseek_wrapper import local_deepseek

class ThreatEvaluatorAgent:
    def __init__(self):
        # Define the model to be used with local_deepseek
        self.model_name = "deepseek-r1:8b"
        # Define the system message
        self.system_message = (
            "You are a threat‐classification agent. You receive a combined, tagged summary. "
            "Output only JSON matching the ThreatLabel schema."
        )
        # Additional configurations
    
        self.human_input_mode = "NEVER"
        self.code_execution_config = {"use_docker": False}
       

    def evaluate(self, context: str) -> str:
        """
        Evaluates the threat based on the provided context using the local_deepseek function.
        """
        try:
            # Prepare the messages for the DeepSeek model
            new_messages = [
                {
                    "role": "system",
                    "content": self.system_message
                },
                {
                    "role": "user",
                    "content": (
                        "\nBased on following text, determine the military threat level on the following scale:"
                        "\n0: No military significance, civilian setting."
                        "\n1: Low significance, military equipment in a civilian setting, public display, non-combat formations."
                        "\n2: Medium significance, military exercises, battlefield-like setup, or training, weapons with blank adaptors or orange/red/yellow tip or telltale signs of training."
                        "\n3: Increased significance, aggressive military posturing, battlefield setting, military preparation."
                        "\n4: High threat, clear military aggression, attack formations, casualties."
                        "\nAlso, make sure the response is limited to reasoning and actual threat classification, keeping it under 10 characters."
                        "\nRespond with a single integer (0, 1, 2, 3, or 4) as the final classification.\n\n"
                        f"{context}"
                    )
                }
            ]
            
            # Call the local_deepseek function
            classification = local_deepseek(new_messages, model=self.model_name)
            
            return classification
        except Exception as e:
            # Handle any exceptions that occur during evaluation
            return f"Error during threat evaluation: {str(e)}"

