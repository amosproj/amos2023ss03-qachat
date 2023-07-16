# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel
# SPDX-FileCopyrightText: 2023 Jesse Palarus
import os
import re

from threading import Thread

from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App

from QAChat.Common.asynchronous_processor import AsynchronousProcessor
from QAChat.Slack_Bot.base_agent import BaseAgent
from QAChat.Slack_Bot.qa_bot_api_interface import QABotAPIInterface
from get_tokens import get_tokens_path

load_dotenv(get_tokens_path())
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")


class QAAgent(BaseAgent):
    def __init__(self, app=None, client=None, handler=None, api_interface=None):
        self.app = app or App(token=SLACK_TOKEN)
        self.client = client or WebClient(token=SLACK_TOKEN)
        self.handler = handler or SocketModeHandler(self.app, SLACK_APP_TOKEN)
        self.api_interface = api_interface or QABotAPIInterface()

    def receive_question(self, question, say, channel_id):
        initial_message = self.client.chat_postMessage(channel=channel_id, text="...")
        initial_ts = initial_message["ts"]

        asynchronous_processor = AsynchronousProcessor(
            lambda message: self.client.chat_update(
                channel=channel_id,
                ts=initial_ts,
                text=message,
            ),
        )

        for answer in self.api_interface.request(question):
            asynchronous_processor.add(answer)
        asynchronous_processor.end()

    def process_question(self, body, say):
        """
        This method is called when a new message arrives from a user via the Slack API.
        It processes the request and will answer the user.

        Args:
            body (dict): The body of the incoming request from the Slack API, structured as follows:
                {"event": {"text": str, "user": str, "channel": str}}
            say (function): A function that can be called to send a message back to the Slack channel.
        """

        text = body["event"]["text"]
        channel_id = body["event"]["channel"]

        # Use a separate thread to call receive_question
        thread = Thread(target=self.receive_question, args=(text, say, channel_id))
        thread.start()

    def start(self):
        self.handler.app.message(re.compile(".*"))(self.process_question)
        self.handler.start()


if __name__ == "__main__":
    agent = QAAgent()
    agent.start()
