# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel
# SPDX-FileCopyrightText: 2023 Jesse Palarus
import os
import sys
import re

from threading import Thread

from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App

from QAChat.Slack_Bot.base_agent import BaseAgent
from QAChat.Slack_Bot.qa_bot_api_interface import QABotAPIInterface

load_dotenv("../../tokens.env")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")


class QAAgent(BaseAgent):
    def __init__(self, app=None, client=None, handler=None, api_interface=None):
        self.app = app or App(token=SLACK_TOKEN)
        self.client = client or WebClient(token=SLACK_TOKEN)
        self.handler = handler or SocketModeHandler(self.app, SLACK_APP_TOKEN)
        self.api_interface = api_interface or QABotAPIInterface()

    def receive_question(self, question, say, channel_id):
        say("...")
        answer = self.api_interface.request(question)
        say(answer)
        self.delete_processing_message(channel_id)

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

    def delete_processing_message(self, channel_id):
        """
        This method deletes the '...' in a given channel's conversation history in Slack, previously send from the bot.

        The method does not return any value. In case of a Slack API error during deletion,
        it prints the error.

        Args:
            channel_id (str): The ID of the channel from which the message should be deleted.

        Raises:
            SlackApiError: If there is a problem with the Slack API, e.g.,
            the channel does not exist.
        """

        # Get conversation history
        result = self.client.conversations_history(channel=channel_id)

        messages = result.data.get("messages")

        # Loop through all messages
        for msg in messages:
            try:
                if msg.get("text") is not None and msg.get("text") == "...":
                    ts = msg.get("ts")
                    # ...delete a message
                    self.client.chat_delete(channel=channel_id, ts=ts)
            except SlackApiError:
                print(f"Error deleting loading message", file=sys.stderr)


if __name__ == "__main__":
    agent = QAAgent()
    agent.start()
