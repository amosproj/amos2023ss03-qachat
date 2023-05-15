# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel

from queue import Queue
from threading import Thread
from dotenv import load_dotenv
import deepl
import os

load_dotenv("../tokens.env")
DEEPL_TOKEN = os.getenv("DEEPL_TOKEN")


class DeepL_Translator():

    def __init__(self):
        super().__init__()
        #initialize a DeepL translator service
        self.translator = deepl.Translator(DEEPL_TOKEN)




    def receive_question(self, text):
        result = self.translator.translate_text(text, target_lang="EN-US")
        return result.text

if __name__ == '__main__':
    translator = DeepL_Translator()
    print(translator.receive_question("Test"))


