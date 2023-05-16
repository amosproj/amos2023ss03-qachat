# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel

import QAChat.QA_Bot.api_interface as APIInterface

class BaseAgent:

    def __init__(self):
        self.api_interface = APIInterface.APIInterface()

    def receive_question(self, question, user_id):
        self.api_interface.listen_for_requests(question, self)

    def receive_answer(self, answer, user_id):
        # pass answer to slackbotapi
        pass
