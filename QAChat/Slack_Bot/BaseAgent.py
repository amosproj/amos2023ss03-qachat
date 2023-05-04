import QA_Bot.APIInterface


class BaseAgent:

    def __init__(self):
        self.api_interface = QA_Bot.APIInterface.APIInterface()

    def receive_question(self, question):
        self.api_interface.listen_for_requests(question, self)

    def receive_answer(self, answer):
        # pass answer to slackbotapi
        pass