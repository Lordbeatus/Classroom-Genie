import os
import secrets
import requests
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
import sys

# Ensure parent directory is in path for prompts import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prompts.Qwen import build_prompt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))
CORS(app)

HF_TOKEN = os.environ.get("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

MODEL_NAME = "microsoft/DialoGPT-medium"  # Let's try a model that definitely works

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_question = data.get('message')
    subject = data.get('subject')
    history = data.get('history', [])

    # Require subject before chat
    if not session.get('subject'):
        if not subject:
            return jsonify({'response': 'Please provide a subject before starting the chat.'}), 400
        session['subject'] = subject
        session['is_first_prompt'] = True

    # Track if this is the first prompt in the session
    is_first_prompt = session.get('is_first_prompt', True)
    base_prompt = build_prompt(user_question, is_first_prompt, session.get('subject'))
    session['is_first_prompt'] = False

    # Add chat history to the prompt for memory, but keep prompt engineering
    if history:
        history_text = ""
        for msg in history:
            if msg['role'] == 'user':
                history_text += f"User: {msg['content']}\n"
            else:
                history_text += f"Assistant: {msg['content']}\n"
        prompt = history_text + f"User: {user_question}\nAssistant:"
        # Prepend the engineered instructions to the history
        prompt = base_prompt + "\n" + prompt
    else:
        prompt = base_prompt

    # Call the model using Hugging Face Inference API directly
    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        response = requests.post(API_URL + MODEL_NAME, headers=HEADERS, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                response_text = result[0].get("generated_text", "No response generated")
            else:
                response_text = str(result)
        else:
            raise Exception(f"API returned status {response.status_code}: {response.text}")
            
    except Exception as e:
        # If the primary model fails, try a simple fallback
        print(f"Primary model failed: {e}")
        try:
            fallback_payload = {"inputs": prompt}
            fallback_response = requests.post(API_URL + "gpt2", headers=HEADERS, json=fallback_payload)
            
            if fallback_response.status_code == 200:
                fallback_result = fallback_response.json()
                if isinstance(fallback_result, list) and len(fallback_result) > 0:
                    response_text = f"[Using fallback] {fallback_result[0].get('generated_text', 'No response')}"
                else:
                    response_text = f"[Using fallback] {str(fallback_result)}"
            else:
                response_text = f"Error with both models. Primary: {str(e)}, Fallback status: {fallback_response.status_code}"
        except Exception as fallback_error:
            response_text = f"Error with both models. Primary: {str(e)}, Fallback: {str(fallback_error)}"

    # No more post-processing for math: let the frontend/MathJax handle all LaTeX/Markdown
    return jsonify({'response': response_text})

@app.route('/api/reset', methods=['POST'])
def reset():
    session.clear()
    return jsonify({'response': 'Session reset.'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)