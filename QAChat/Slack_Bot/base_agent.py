# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel


class BaseAgent:
    def __init__(self):
        pass
    
    def receive_question(self, question, user_id):
        pass

    def receive_answer(self, answer, user_id):
        # pass answer to slackbotapi
        pass
