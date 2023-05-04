from BaseAgent import BaseAgent

class QAAgent(BaseAgent):

    def __init__(self):
        super().__init__()

    def receive_question(self, question):
        self.api_interface.listen_for_requests(question)

    def receive_answer(self, answer):
        # pass answer to slackbotapi
        pass
