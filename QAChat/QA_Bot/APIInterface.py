# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel

from QAChat.QA_Bot.QABot import QABot
import QAChat.Slack_Bot.BaseAgent as BaseAgent


class APIInterface:

    def __init__(self, qa_bot=None):
        self.qa_bot = qa_bot
        self.sender: BaseAgent = None

    def listen_for_requests(self, question, sender, user_id):
        self.sender = sender
        if self.qa_bot is None:
            self.qa_bot = QABot(self)
        self.qa_bot.answer_question(question, user_id)

    def forward_answer(self, answer, user_id):
        self.sender.receive_answer(answer, user_id)
