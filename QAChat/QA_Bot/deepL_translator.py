# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel

import os

import deepl
from dotenv import load_dotenv

load_dotenv("../../tokens.env")
DEEPL_TOKEN = os.getenv("DEEPL_TOKEN")


class DeepLTranslator:
    def __init__(self):
        super().__init__()
        # initialize a DeepL translator service
        self.translator = deepl.Translator(DEEPL_TOKEN)

    def translate_to(self, text, target_lang):
        result = self.translator.translate_text(
            text, target_lang=target_lang, ignore_tags="name"
        )
        if result.detected_source_lang == "EN":
            result.detected_source_lang = "EN-US"
        elif result.detected_source_lang == "PT":
            result.detected_source_lang = "PT-PT"
        return result


if __name__ == "__main__":
    translator = DeepLTranslator()
    # print(translator.receive_question("Was sind xyhj"))
    result = translator.translate_to("Was sind xyhj", "EN-US")

    print(result.text)
    print(result.detected_source_lang)
