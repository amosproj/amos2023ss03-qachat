# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Palarus

import json
import os

import requests
from dotenv import load_dotenv
from get_tokens import get_tokens_path

load_dotenv(get_tokens_path())


class QABotAPIInterface:
    def request(self, question):
        url = os.getenv("GOOGLE_CLOUD_QA_BOT")

        response = requests.post(url, json={'question': question}, stream=True)

        for line in response.iter_lines():
            # filter out keep-alive new lines
            if line:
                decoded_line = line.decode('utf-8')
                data = json.loads(decoded_line)
                yield data["text"]
