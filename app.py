from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

openai.api_key = "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"
assistant_id = "asst_ugCI63m19mcgFmwnoJK56NY9"  # Career Roadmap Assistant

@app.route('/')
def home():
    return "🟢 Ti Tivi AI is running. Use POST /chat"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('input')

        thread = openai.beta.threads.create()
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == "completed":
                break
            time.sleep(1)

        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        reply = messages.data[0].content[0].text.value

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
