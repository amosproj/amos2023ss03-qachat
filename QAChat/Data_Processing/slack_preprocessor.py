# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel
# SPDX-FileCopyrightText: 2023 Hafidz Arifin

from datetime import datetime, timezone
from typing import List
from slack_sdk import WebClient
from dotenv import load_dotenv
import os
from slack_sdk.errors import SlackApiError
from QAChat.Data_Processing.data_preprocessor import DataPreprocessor
from QAChat.Data_Processing.deepL_translator import DeepLTranslator
from QAChat.Data_Processing.document_embedder import DataInformation, DataSource
from supabase.client import create_client

load_dotenv("../tokens.env")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SIGNING_SECRET = os.getenv("SIGNING_SECRET")


class SlackPreprocessor(DataPreprocessor):

    def __init__(self):
        self.client = WebClient(token=SLACK_TOKEN)
        self.conversation_store = {}
        self.conversation_history = []
        self.translator = DeepLTranslator()
        self.count_found_messages = 0
        self.supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY"))

    def fetch_conversations(self):
        try:
            # Call the conversations.list method using the WebClient
            result = self.client.conversations_list()
            self.__save_conversations(result["channels"])
        except SlackApiError as e:
            print("Error fetching conversations: {}".format(e))

    # Put conversations into the JavaScript object
    def __save_conversations(self, conversations):
        conversation_id = ""
        for conversation in conversations:
            # Key conversation info on its unique ID
            conversation_id = conversation["id"]

            # Store the entire conversation object
            # (you may not need all of the info)
            if conversation["is_member"]:
                self.conversation_store[conversation_id] = conversation

    def load_messages(self, channel_list, oldest=None):

        for channel_id in channel_list:
            try:
                # Call the conversations.history method using the WebClient
                # conversations.history returns the first 100 messages by default
                # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
                result = self.client.conversations_history(channel=channel_id, oldest=oldest)

                for message in result["messages"]:
                    self.conversation_history.append(self.translator.translate_german_english(message["text"]))

                # Print results
                print(
                    "{} messages found in {}".format(len(self.conversation_history) - self.count_found_messages, channel_id))

                count_found_messages = len(self.conversation_history)

            except SlackApiError as e:
                print("Error creating conversation: {}".format(e))

    def load_preprocessed_data(self, before: datetime, after: datetime) -> List[DataInformation]:
        raw_data = []
        for index, row in enumerate(self.conversation_history):
            raw_data.append(DataInformation(id=f"{index}", last_changed=datetime.now(), typ=DataSource.SLACK,
                                            text=row))

        return [data for data in raw_data if after < data.last_changed]


if __name__ == '__main__':
    preprocess = SlackPreprocessor()
