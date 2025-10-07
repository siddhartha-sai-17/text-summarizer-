import json

def print_summary(summary: str, style: str):
    """
    Prints the summary in a formatted way.

    Args:
        summary: The summary string.
        style: The style of the summary, to handle bullet points.
    """
    if style == 'bullet points':
        try:
            points = json.loads(summary)
            for point in points:
                print(f"- {point}")
        except json.JSONDecodeError:
            print("Could not parse bullet points, showing raw output:")
            print(summary)
    else:
        print(summary)


def print_ai_analysis(analysis_data: dict):
    """
    Prints the AI detection analysis in a user-friendly format.

    Args:
        analysis_data: A dictionary with the analysis results.
    """
    ai_prob = analysis_data.get("overall_probability", 0)
    human_prob = 100 - ai_prob
    
    print(f"Score: {ai_prob}% of text is likely AI-generated.\n")

    # Simple ASCII bar chart
    ai_bar = '█' * int(ai_prob / 2)
    human_bar = '░' * int(human_prob / 2)
    print(f"|{ai_bar}{human_bar}|")
    print(f" AI {ai_prob}% <---> {human_prob}% Human\n")

    print("--- Breakdown ---")
    print(f"AI-generated:    {analysis_data['breakdown']['ai_generated']}%")
    print(f"Human-written:   {analysis_data['breakdown']['human_written']}%")
    
    print("\n--- Explanation ---")
    print(analysis_data.get("explanation", "No explanation provided."))
