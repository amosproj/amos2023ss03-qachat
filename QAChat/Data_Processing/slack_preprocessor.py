# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel
# SPDX-FileCopyrightText: 2023 Hafidz Arifin

import os
from datetime import datetime
from typing import List
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from supabase.client import create_client

from QAChat.Data_Processing.data_preprocessor import DataPreprocessor
from QAChat.QA_Bot.deepL_translator import DeepLTranslator
from QAChat.Data_Processing.document_embedder import DataInformation, DataSource

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
        self.supabase = create_client(
            os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY")
        )

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
                result = self.client.conversations_history(
                    channel=channel_id, oldest=oldest
                )

                for message in result["messages"]:
                    if "subtype" in message and message["subtype"] == "channel_join":
                        continue
                    self.conversation_history.append(
                        self.translator.translate_german_english(message["text"])
                    )

                # Print results
                print(
                    "{} messages found in {}".format(
                        len(self.conversation_history) - self.count_found_messages,
                        channel_id,
                    )
                )

                self.count_found_messages = len(self.conversation_history)

            except SlackApiError as e:
                print("Error creating conversation: {}".format(e))

    def load_preprocessed_data(
            self, before: datetime, after: datetime
    ) -> List[DataInformation]:
        self.fetch_conversations()
        oldest = after.timestamp()
        already_loaded_ids = (
            self.supabase.table("slack_loaded_channels")
            .select("channel_id")
            .execute()
            .data
        )

        new_channels = [
            channel
            for channel in self.conversation_store
            if {"channel_id": channel} not in already_loaded_ids
        ]
        self.load_messages(new_channels)
        already_loaded_ids = [
            channel["channel_id"] for channel in already_loaded_ids
        ]  # convert to list of strings
        self.load_messages(already_loaded_ids, oldest=oldest)

        # create new entries in the database
        new_channels_names = [
            self.conversation_store[channel]["name"] for channel in new_channels
        ]

        for channel_id, channel_name in zip(new_channels, new_channels_names):
            self.supabase.table("slack_loaded_channels").insert(
                {"channel_id": channel_id, "channel_name": channel_name}
            ).execute()

        raw_data = []
        for index, row in enumerate(self.conversation_history):
            raw_data.append(
                DataInformation(
                    id=f"{index}",
                    last_changed=datetime.now(),
                    typ=DataSource.SLACK,
                    text=row,
                )
            )

        return [data for data in raw_data if after < data.last_changed]


if __name__ == "__main__":
    preprocess = SlackPreprocessor()
    preprocess.fetch_conversations()
    preprocess.load_messages()
    print("")
    print("conversation_store")
    print(preprocess.conversation_store)
    print("")
    print("preprocess.conversation_store.keys()")
    print(preprocess.conversation_store.keys())
    print("")
    print("preprocess.conversation_history")
    print(preprocess.conversation_history)
