# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel

import os

import deepl
from dotenv import load_dotenv

load_dotenv("../tokens.env")
DEEPL_TOKEN = os.getenv("DEEPL_TOKEN")


class DeepLTranslator:
    def __init__(self):
        super().__init__()
        # initialize a DeepL translator service
        self.translator = deepl.Translator(DEEPL_TOKEN)

    def receive_question(self, text):
        result = self.translator.translate_text(text, target_lang="EN-US")
        return result.text

    def translate_german_english(self, text):
        result = self.translator.translate_text(text, target_lang="EN-US")
        return result.text

    def translate_english_german(self, text):
        result = self.translator.translate_text(text, target_lang="DE")
        return result.text


if __name__ == "__main__":
    translator = DeepLTranslator()
    print(translator.receive_question("Hallo wie geht es dir?"))
