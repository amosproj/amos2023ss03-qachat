from QAChat.QA_Bot.QABot import QABot
import QAChat.Slack_Bot.BaseAgent as BaseAgent

class APIInterface:

    def __init__(self, qa_bot=None):
        self.qa_bot = qa_bot
        # TODO: This needs remodeling to handle multiple Request at once maybe ???
        self.sender: BaseAgent = None

    # forwards the question sent by the slackbot to the qabot
    def listen_for_requests(self, question, sender):
        self.sender = sender
        if self.qa_bot is None:
            self.qa_bot = QABot(self)
        self.qa_bot.answer_question(question)

    # forwards the answer sent by the qabot to the userAgent
    def forward_answer(self, answer):
        self.sender.receive_answer(answer)
