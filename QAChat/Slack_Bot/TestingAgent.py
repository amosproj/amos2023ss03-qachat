import tkinter as tk
from slack_bolt import App
from BaseAgent import BaseAgent
import slack
from slack_bolt.adapter.socket_mode import SocketModeHandler
import re

'''
    This is just an easy Testing Bot for testing reasons and should not be part of the final release. 
    Its purpose is to send and receive answers from our system, without having a functioning SlackBot or other.
'''

SLACK_TOKEN = "INSERT"
SLACK_APP_TOKEN = "INSERT"
app = App(token=SLACK_TOKEN)
SIGNING_SECRET = "INSERT"
client = slack.WebClient(token=SLACK_TOKEN)
client.chat_postMessage(channel='#bot-test', text='Hi')


class TestingAgent(BaseAgent):
    def __init__(self, master):
        super().__init__()
        self.master = master
        master.title("My GUI")

        self.label = tk.Label(master, text="Enter some text:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.button = tk.Button(master, text="Submit", command=self.receive_question)
        self.button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def receive_question(self, question=None):
        input_text = self.entry.get()
        self.api_interface.listen_for_requests(input_text, self)

    def receive_answer(self, answer):
        self.result_label.config(text=answer)


@app.message(re.compile('.*'))
def process_question(body, say):
    text = body['event']['text']
    say("I cannot answer if " + text)


@app.event("app_mention")
def mention_handler(body, say):
    user = body['user']
    say(f"Hi there, <@{user}>!")


if __name__ == '__main__':
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
    # root = tk.Tk()
    # gui = TestingAgent(root)
    # root.mainloop()
