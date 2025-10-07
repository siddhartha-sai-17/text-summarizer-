from gemini_client import call_gemini_api

def correct_grammar(api_key: str, text: str) -> str:
    """
    Corrects grammar and spelling errors in the provided text.

    Args:
        api_key: The Gemini API key.
        text: The text to correct.

    Returns:
        A string containing the corrected text.
    """
    system_prompt = (
        "You are a grammar and spelling correction tool. Review the text for errors in "
        "spelling, punctuation, and grammar. Return only the corrected version. "
        "Do not add any commentary or explanations."
    )
    return call_gemini_api(api_key, text, system_prompt)
