# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Palarus

import json
import threading

from flask import Flask, request, stream_with_context, Response

from stream_LLM_callback_handler import StreamLLMCallbackHandler
from qa_bot import QABot

app = Flask(__name__)
qa_bot = QABot()


@app.route("/", methods=["POST"])
def calculate():
    handler = StreamLLMCallbackHandler()

    data = request.get_json()
    question = data["question"]

    def generate():
        while True:
            # Block until there is new data on the queue
            text = handler.q.get()

            # This is a special value indicating the transfer is complete
            if text == "__END__":
                break

            data = {
                "text": text,
            }
            yield json.dumps(data) + "\n"

    def run_long_running_function():
        qa_bot.answer_question(question, handler)
        handler.q.put("__END__")  # Signal that the transfer is complete

    threading.Thread(target=run_long_running_function).start()

    return Response(stream_with_context(generate()), mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
