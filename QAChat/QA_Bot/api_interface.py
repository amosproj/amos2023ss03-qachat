# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel


from .qa_bot import QABot


class APIInterface:
    def __init__(self, qa_bot=None):
        self.qa_bot = qa_bot
        if qa_bot is None:
            self.qa_bot = QABot()

    def listen_for_requests(self, question, sender, user_id):
        answer = self.qa_bot.answer_question(question, user_id)
        self.forward_answer(answer, sender, user_id)

    def forward_answer(self, answer, sender, user_id):
        sender.receive_answer(answer, user_id)
