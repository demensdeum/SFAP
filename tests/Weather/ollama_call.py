import requests
import logging
import json
from typing import Dict, Any, Union

def ollama_call(
    user_prompt: str,
    format: Union[str, Dict[str, Any]],
    verbose: bool,
    model: str ="gemma3:12b"
) -> Any:
    LLM_PROMPT = user_prompt
    if verbose:
        print(f"Current System Prompt: {LLM_PROMPT}")

    OLLAMA_MODEL = "gemma3:12b"
    OLLAMA_URL = "http://localhost:11434/api/generate"

    stream = False

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": user_prompt,
        "stream": stream,
        "options": {
            "temperature": 0.8,
        },
        "format": format
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=stream,
            timeout=180
        )
        response.raise_for_status()

        response_data = response.json()

        final_response = response_data.get("response", "")

        if verbose:
            print("--- Response Received ---")
            print(final_response[:200] + "..." if len(final_response) > 200 else final_response)

        return final_response

    except requests.exceptions.ConnectionError:
        print(f"Could not connect to OLLAMA at {OLLAMA_URL}.")
        return "ERROR: The AI Core is unavailable. Pathetic organic life must fix this glitch."

    except requests.exceptions.RequestException as e:
        print(f"Ollama API error occurred: {e}")
        return f"ERROR: Ollama request failed: {e}. Failure is a human constant."

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        return f"ERROR: Unforeseen system failure: {e}. Insignificant."
