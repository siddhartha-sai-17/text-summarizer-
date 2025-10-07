import json
from gemini_client import call_gemini_api

def summarize_text(api_key: str, text: str, summary_format: str, tone: str, length: int):
    """
    Summarizes the given text based on the specified format, tone, and length.

    Args:
        api_key: The Gemini API key.
        text: The text to summarize.
        summary_format: The desired format ('paragraph', 'bullet points', 'keywords').
        tone: The desired tone for the summary.
        length: The desired number of lines or points.

    Returns:
        The summarized text as a string or list of strings.
    """
    is_json = False
    system_prompt = f"You are an expert summarizer. Take the following text and provide a concise, easy-to-read summary. The summary should be presented in a '{summary_format}' format with a '{tone}' tone."

    if summary_format == 'bullet points':
        system_prompt = f"You are an expert summarizer. Take the following text and create a summary as a list of bullet points with a '{tone}' tone. The summary should have exactly {length} points. Respond with a JSON array of strings, where each string is a bullet point. For example: [\"Point 1\", \"Point 2\"]. Respond ONLY with the valid JSON object."
        is_json = True
    elif summary_format == 'keywords':
        system_prompt = "Extract the most important keywords from the following text. Present them as a single, comma-separated list."
    else: # Paragraph and other text-based formats
        system_prompt += f" The summary should be exactly {length} lines long. Do not write more or less than {length} lines."

    result_str = call_gemini_api(api_key, text, system_prompt, is_json=is_json)
    
    if is_json:
        try:
            return json.loads(result_str)
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from summarizer response: {result_str}")
            return ["Could not parse the summary from the AI model."]
    
    return result_str

