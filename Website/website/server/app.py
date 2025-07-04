import os
import secrets
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import sys

# Ensure parent directory is in path for prompts import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from prompts.Qwen import build_prompt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))
CORS(app)

HF_TOKEN = os.environ.get("HUGGINGFACE_API_KEY")
client = InferenceClient(token=HF_TOKEN)

MODEL_NAME = "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"  # Back to your original model

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

    # Call the model using Hugging Face Inference API
    try:
        response = client.text_generation(
            prompt,
            model=MODEL_NAME,
            max_new_tokens=500,
            temperature=0.7,
            return_full_text=False,
            stream=False
        )
        response_text = response if isinstance(response, str) else response.generated_text
    except Exception as e:
        response_text = f"Error calling model: {str(e)}"

    # No more post-processing for math: let the frontend/MathJax handle all LaTeX/Markdown
    return jsonify({'response': response_text})

@app.route('/api/reset', methods=['POST'])
def reset():
    session.clear()
    return jsonify({'response': 'Session reset.'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)