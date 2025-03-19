"""
AI-generated text
"""

import subprocess
import ollama
import json
from config import OLLAMA_MODEL

# JSON Schema for the output of the AI
output_schema = {
    "type": "object",
    "properties": {
        "scenario": {"type": "string"},
        "options": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "effects": {
                        "type": "object",
                        "properties": {
                            "economy": {"type": "number"},
                            "military": {"type": "number"},
                            "public_appeal": {"type": "number"},
                            "diplomacy": {"type": "number"},
                        },
                        "required": [
                            "economy",
                            "military",
                            "public_appeal",
                            "diplomacy",
                        ],
                    },
                },
                "required": ["text", "effects"],
            },
        },
    },
    "required": ["scenario", "options"],
}


# Example
# {{
#     "scenario": "A brief scenario...",
#     "options": [
#         {{"text": "Option 1", "effects": {{"economy": -5, "military": 2, "public_appeal": 1, "diplomacy": 0}}}},
#         {{"text": "Option 2", "effects": {{"economy": 3, "military": -2, "public_appeal": 0, "diplomacy": 1}}}},
#         {{"text": "Option 3", "effects": {{"economy": 0, "military": 0, "public_appeal": -3, "diplomacy": 5}}}}
#     ]
# }}


def generate_scenario(
    economy, military, public_appeal, diplomacy, previous_events=None, load_from_file="assets/scenario.json"
):
    print("Generating scenario...")
    # Add random neighboring kingdom names for flavor
    neighboring_kingdoms = ["Valoria", "Drakthar", "Lunaris", "Zytheria", "Caldoria"]
    random_neighbors = ", ".join(neighboring_kingdoms)

    # Include previous events in the prompt if available
    previous_events_text = (
        "\n".join(f"- {event}" for event in previous_events)
        if previous_events
        else "No significant events have occurred recently."
    )

    prompt = f"""
    You are the ruler of the medieval kingdom of Eldoria, a land known for:
    - Vast forests that provide timber and shelter for wildlife.
    - Thriving trade routes connecting neighboring kingdoms like {random_neighbors}.
    - A history of political intrigue and power struggles among nobles.
    - A diverse population with varying needs and expectations.

    Your kingdom's current state is as follows:
    - Economy: {economy} (Represents the wealth and resources of the kingdom.)
    - Military: {military} (Represents the strength and readiness of your army.)
    - Public Appeal: {public_appeal} (Represents the trust and satisfaction of your people.)
    - Diplomacy: {diplomacy} (Represents your relationships with neighboring kingdoms.)

    Recent events in Eldoria:
    {previous_events_text}

    Your task is to make decisions that will shape the future of Eldoria. 
    Provide a short scenario that reflects a realistic challenge or opportunity 
    faced by a medieval ruler. The scenario must:
    - Be relevant to the medieval setting of Eldoria.
    - Involve one or more aspects of the kingdom's state (economy, military, public appeal, diplomacy).
    - Be concise, no more than 50 words.
    - Take into account the recent events listed above.

    Additionally, provide three options for the ruler to choose from. Each option must:
    - Be no more than 14 words.
    - Clearly describe an action or decision the ruler can take.
    - Include logical effects on the kingdom's stats (economy, military, public appeal, diplomacy).
    - Avoid vague or unrealistic actions.
    - Be consistent with the scenario and recent events.

    Return the scenario and options in the following JSON format:
    {{
        "scenario": "A brief description of the situation.",
        "options": [
            {{
                "text": "Option 1 description.",
                "effects": {{
                    "economy": <number>,
                    "military": <number>,
                    "public_appeal": <number>,
                    "diplomacy": <number>
                }}
            }},
            {{
                "text": "Option 2 description.",
                "effects": {{
                    "economy": <number>,
                    "military": <number>,
                    "public_appeal": <number>,
                    "diplomacy": <number>
                }}
            }},
            {{
                "text": "Option 3 description.",
                "effects": {{
                    "economy": <number>,
                    "military": <number>,
                    "public_appeal": <number>,
                    "diplomacy": <number>
                }}
            }}
        ]
    }}
    """

    try:
        if load_from_file:
            with open(load_from_file, "r") as file:
                data = json.load(file)
                return data["scenario"], data["options"]
        else:
            result = ollama.generate(OLLAMA_MODEL, prompt, format=output_schema)
            output = result.response
            print(output)
            # Attempt to parse JSON response from Ollama
            data = json.loads(output)

            print(data)
            return data["scenario"], data["options"]

    except Exception as e:
        print("Error processing AI response:", e)
        return "A crisis emerges!", [
            {
                "text": "Make a random decision",
                "effects": {
                    "economy": -2,
                    "military": -2,
                    "public_appeal": -2,
                    "diplomacy": -2,
                },
            },
            {
                "text": "Do nothing",
                "effects": {
                    "economy": 0,
                    "military": 0,
                    "public_appeal": 0,
                    "diplomacy": 0,
                },
            },
            {
                "text": "Seek advice from nobles",
                "effects": {
                    "economy": 1,
                    "military": 1,
                    "public_appeal": 1,
                    "diplomacy": 1,
                },
            },
        ]
