import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Add the current directory to the path to find other modules
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from summarizer import summarize_text
from grammar_corrector import correct_grammar
from ai_detector import detect_ai_text

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow requests from the frontend

@app.route('/summarize', methods=['POST'])
def handle_summarize():
    """Endpoint to handle text summarization requests."""
    data = request.json
    
    # --- DEBUGGING LINE ---
    print(f"Received request for /summarize with data: {data}")

    # --- FIX: Handle older frontend versions ---
    if 'style' in data and 'format' not in data:
        data['format'] = data.pop('style')
    if 'tone' not in data:
        data['tone'] = 'Neutral' # Default to Neutral if tone is not provided

    api_key = os.getenv("GEMINI_API_KEY")

    if not data or not all(k in data for k in ['text', 'format', 'tone', 'length']):
        missing_keys = {'text', 'format', 'tone', 'length'} - set(data.keys())
        print(f"Request failed: Missing required parameters: {missing_keys}")
        return jsonify({"error": f"Missing required parameters: {', '.join(missing_keys)}"}), 400
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY not found in .env file"}), 500

    try:
        text = data['text']
        summary_format = data['format']
        tone = data['tone']
        length = data['length']
        
        result = summarize_text(api_key, text, summary_format, tone, length)
        return jsonify({"result": result})
    except Exception as e:
        print(f"Error in /summarize: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/correct', methods=['POST'])
def handle_correct():
    """Endpoint to handle grammar correction requests."""
    data = request.json
    api_key = os.getenv("GEMINI_API_KEY")

    if 'text' not in data:
        return jsonify({"error": "Missing text parameter"}), 400
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY not found in .env file"}), 500

    try:
        result = correct_grammar(api_key, data['text'])
        return jsonify({"result": result})
    except Exception as e:
        print(f"Error in /correct: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/detect-ai', methods=['POST'])
def handle_detect_ai():
    """Endpoint to handle AI detection requests."""
    data = request.json
    api_key = os.getenv("GEMINI_API_KEY")

    if 'text' not in data:
        return jsonify({"error": "Missing text parameter"}), 400
    if not api_key:
        return jsonify({"error": "GEMINI_API_KEY not found in .env file"}), 500

    try:
        result = detect_ai_text(api_key, data['text'])
        return jsonify({"result": result})
    except Exception as e:
        print(f"Error in /detect-ai: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

