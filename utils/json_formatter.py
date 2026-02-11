import json
import re

def safe_json_parse(text: str):
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    return {
        "error": "Invalid JSON from LLM",
        "raw_output": text
    }
