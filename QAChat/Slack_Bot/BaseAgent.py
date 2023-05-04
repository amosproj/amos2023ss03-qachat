import QAChat.QA_Bot.APIInterface as APIInterface

class BaseAgent:

    def __init__(self):
        self.api_interface = APIInterface.APIInterface()

    def receive_question(self, question):
        self.api_interface.listen_for_requests(question, self)

    def receive_answer(self, answer):
        # pass answer to slackbotapi
        pass
