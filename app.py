from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import time

app = Flask(__name__)
CORS(app)

openai.api_key = "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"

assistant_id = "asst_ugCI63m19mcgFmwnoJK56NY9"  # Ti Tivi Career Coach
thread_id = None

@app.route('/')
def index():
    return "🟢 Ti Tivi AI is live. POST to /chat"

@app.route('/chat', methods=['POST'])
def chat():
    global thread_id
    user_input = request.json.get('input')

    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    try:
        # Create a new thread if none exists
        if not thread_id:
            thread = openai.beta.threads.create()
            thread_id = thread.id

        # Add user message to the thread
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Run assistant on that thread
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Wait for completion
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                return jsonify({'error': 'Assistant failed'}), 500
            time.sleep(1)

        # Get the latest assistant reply
        messages = openai.beta.threads.messages.list(thread_id=thread_id)

        for msg in reversed(messages.data):
            if msg.role == "assistant" and msg.content:
                content = msg.content[0]
                if hasattr(content, "text") and hasattr(content.text, "value"):
                    return jsonify({'reply': content.text.value})

        return jsonify({'reply': "We're improving Ti Tivi’s answers. Come back soon!"})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
