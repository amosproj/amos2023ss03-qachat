import json
import os

import requests
from dotenv import load_dotenv

load_dotenv("../tokens.env")


class QABotAPIInterface:

    def request(self, question):
        url = os.getenv("GOOGLE_CLOUD_QA_BOT")
        headers = {'Content-type': 'application/json'}

        data = {
            "question": question
        }
        print("Sending question to Google Cloud QA Bot")
        response = requests.post(url, data=json.dumps(data), headers=headers)
        response_data = response.json()
        return response_data["answer"]
