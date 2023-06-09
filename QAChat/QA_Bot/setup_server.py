from flask import Flask, request

from qa_bot import QABot

app = Flask(__name__)
qa_bot = QABot()


@app.route('/', methods=['POST'])
def calculate():
    data = request.get_json()
    question = data["question"]
    answer = qa_bot.answer_question(question)
    return answer


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
