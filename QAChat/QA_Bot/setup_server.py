# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Palarus

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

    def run_long_running_function():
        qa_bot.answer_question(question, handler)
        handler.asynchronous_processor.end()

    threading.Thread(target=run_long_running_function).start()

    response = Response(
        stream_with_context(handler.asynchronous_processor.stream()),
        mimetype="text/event-stream",
    )
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
