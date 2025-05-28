import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"

def extract_json(response_text: str) -> dict:
    """Extract the first JSON block from LLM output."""
    try:
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("No JSON object found in LLM response.")
    except Exception as e:
        raise ValueError(f"Error parsing JSON: {str(e)}")

def classify_caption_with_mistral(caption: str) -> dict:
    """
    Sends the caption to a locally hosted Mistral model via Ollama for 3-level classification.
    Returns a dictionary with category, sub_category, sub_sub_category.
    """

    prompt = f"""
Classify the following Instagram reel caption into a 3-level category hierarchy.

Caption:
\"{caption}\"

Return a JSON object like this:
{{
  "category": "...",
  "sub_category": "...",
  "sub_sub_category": "..."
}}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False  # Disable streaming for easy handling
            }
        )

        if response.status_code == 200:
            result = response.json()
            return extract_json(result["response"])
        else:
            raise Exception(f"Ollama error: {response.status_code} - {response.text}")

    except Exception as e:
        raise Exception(f"Classification failed: {str(e)}")
