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

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-70b-versatile"

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
        # Build the chat prompt using your prompt engineering
        prompt = base_prompt

    # Call Groq API
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful, hint-giving tutor. Never give direct answers, only hints and encouragement."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        groq_response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        if groq_response.status_code == 200:
            data = groq_response.json()
            response_text = data["choices"][0]["message"]["content"]
        else:
            response_text = f"Groq API error: {groq_response.status_code} {groq_response.text}"
    except Exception as e:
        response_text = f"Error calling Groq API: {str(e)}"

    # No more post-processing for math: let the frontend/MathJax handle all LaTeX/Markdown
    return jsonify({'response': response_text})

@app.route('/api/reset', methods=['POST'])
def reset():
    session.clear()
    return jsonify({'response': 'Session reset.'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)