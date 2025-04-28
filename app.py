from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import time
import os

app = Flask(__name__)
CORS(app)  # 👈🏽 Enable CORS

openai.api_key = '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'

assistant_id = 'asst_ugCI63m19mcgFmwnoJK56NY9'  # Default assistant
thread_id = None

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input')
    custom_assistant_id = request.json.get('assistant_id')  # Allow dynamic assistant selection
    global thread_id

    if not thread_id:
        thread = openai.beta.threads.create()
        thread_id = thread.id

    try:
        openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=custom_assistant_id or assistant_id
        )

        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == "completed":
                break
            time.sleep(1)

        messages = openai.beta.threads.messages.list(thread_id=thread_id)
        last_msg = messages.data[0].content[0].text.value

        return jsonify({'reply': last_msg})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
