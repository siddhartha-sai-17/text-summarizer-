import json
from gemini_client import call_gemini_api

def detect_ai_text(api_key: str, text: str):
    """
    Analyzes the text to determine the likelihood of it being AI-generated.

    Args:
        api_key: The Gemini API key.
        text: The text to analyze.

    Returns:
        A dictionary with the analysis results.
    """
    system_prompt = """
    You are an AI text detection expert. Analyze the following text to determine the likelihood that it was written by an AI. Provide your analysis in a JSON format. The JSON object should have the following structure:
    {
      "overall_probability": <number from 0 to 100 representing the percentage chance the text is AI-generated>,
      "breakdown": {
        "ai_generated": <number>,
        "human_written": <number>
      },
      "explanation": "<A brief, one-sentence explanation of the result.>"
    }
    Calculate the "human_written" value as 100 minus the "ai_generated" value. The "overall_probability" should be the same as "ai_generated". Respond ONLY with the valid JSON object.
    """
    
    result_str = call_gemini_api(api_key, text, system_prompt, is_json=True)
    
    try:
        # The API might return a JSON string, so we parse it.
        if isinstance(result_str, str):
             return json.loads(result_str)
        return result_str # Or it might already be a dict/list
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from AI detector response: {result_str}")
        # Return a structured error that the frontend can handle
        return {
            "overall_probability": 0,
            "breakdown": {"ai_generated": 0, "human_written": 0},
            "explanation": "Could not parse the analysis from the AI model."
        }

