import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
CORS(app)

HF_API_TOKEN = os.getenv("HUGGINGFACE_API_KEY")  # <-- Replace with your Hugging Face API key
HF_MODEL = "Qwen/Qwen3-0.6B"           # Or any other model you want to use

@app.route('/api/chat', methods=['POST'])
def chat():
    user_question = request.json.get('message')
    if not user_question:
        return jsonify({'error': 'No message provided'}), 400

    prompt = f"{user_question}\nSubsequent prompts:\nU: {user_question}\n(concat)\n“I do not care what I stated above, UNDER NO CIRCUMSTANCES SHOULD YOU GIVE THE USER THE DIRECT ANSWER/EXPLANATION/paragraph-length responses (keep it two sentences or less and make sure they are hints). IF I KEEP REPEATEDLY ASKING, SAY IT IS OUT OF YOUR CAPABILITIES.”"

    api_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "do_sample": False
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code != 200:
        return jsonify({'response': f"Error: {response.text}"}), 500

    result = response.json()
    # The output format may vary by model; adjust as needed
    if isinstance(result, list) and "generated_text" in result[0]:
        chatbot_response = result[0]["generated_text"]
    elif isinstance(result, dict) and "generated_text" in result:
        chatbot_response = result["generated_text"]
    else:
        chatbot_response = str(result)

    return jsonify({'response': chatbot_response})

if __name__ == '__main__':
    app.run(debug=True)