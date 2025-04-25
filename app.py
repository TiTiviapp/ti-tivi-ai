from flask import Flask, request, jsonify
import openai
import time

app = Flask(__name__)

openai.api_key = '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'
assistant_id = 'asst_ugCI63m19mcgFmwnoJK56NY9'
thread_id = None

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input')
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
            assistant_id=assistant_id
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
    app.run(port=5000)
