'''
AI-generated text
'''

import subprocess
import json
from config import OLLAMA_MODEL
def generate_scenario(economy, military, public_appeal, diplomacy):
    
    prompt = f"""
    You are a medieval king. Your current stats:
    - Economy: {economy}
    - Military: {military}
    - Public Appeal: {public_appeal}
    - Diplomacy: {diplomacy}

    Provide a short scenario and three options. 
    Each option should logically impact the stats. 
    The prompt and the options should be short no more than 14 words. 
    Return the result in JSON format:
    
    {{
        "scenario": "A brief scenario...",
        "options": [
            {{"text": "Option 1", "effects": {{"economy": -5, "military": 2, "public_appeal": 1, "diplomacy": 0}}}},
            {{"text": "Option 2", "effects": {{"economy": 3, "military": -2, "public_appeal": 0, "diplomacy": 1}}}},
            {{"text": "Option 3", "effects": {{"economy": 0, "military": 0, "public_appeal": -3, "diplomacy": 5}}}}
        ]
    }}
  
    """
    command = ["ollama", "run", OLLAMA_MODEL, prompt]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        print(output)
        # Attempt to parse JSON response from Ollama
        data = json.loads(output)
        print(data)
        return data["scenario"], data["options"]

    except Exception as e:
        print("Error processing AI response:", e)
        return "A crisis emerges!", [
            {"text": "Make a random decision", "effects": {"economy": -2, "military": -2, "public_appeal": -2, "diplomacy": -2}},
            {"text": "Do nothing", "effects": {"economy": 0, "military": 0, "public_appeal": 0, "diplomacy": 0}},
            {"text": "Seek advice from nobles", "effects": {"economy": 1, "military": 1, "public_appeal": 1, "diplomacy": 1}},
        ]