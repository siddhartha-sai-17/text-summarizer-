import requests
import json
import time

def call_gemini_api(api_key: str, text: str, system_prompt: str, is_json: bool = False, max_retries: int = 3):
    """
    Calls the Gemini API with specified text and system prompt.

    Args:
        api_key: The Gemini API key.
        text: The user input text.
        system_prompt: The instruction for the AI model.
        is_json: Flag to indicate if the response should be JSON.
        max_retries: Maximum number of retry attempts.

    Returns:
        The text content from the API response.

    Raises:
        Exception: If the API call fails after all retries.
    """
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }
    
    if is_json:
        payload["generationConfig"] = {
            "responseMimeType": "application/json",
        }

    last_error = None

    for attempt in range(max_retries):
        try:
            response = requests.post(
                api_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)

            result = response.json()
            
            candidate = result.get("candidates", [{}])[0]
            content_part = candidate.get("content", {}).get("parts", [{}])[0]
            
            if "text" in content_part:
                return content_part["text"]
            else:
                reason = candidate.get("finishReason", "No content")
                raise ValueError(f"Model did not return content. Finish Reason: {reason}")

        except requests.exceptions.RequestException as e:
            last_error = e
            print(f"API call attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                delay = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
        except (ValueError, KeyError) as e:
            last_error = e
            print(f"Error processing API response: {e}")
            break # Don't retry on data processing errors

    raise Exception(f"API call failed after {max_retries} attempts. Last error: {last_error}")
