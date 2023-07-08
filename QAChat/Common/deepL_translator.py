# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel

import os

import deepl
import spacy
import xx_ent_wiki_sm
from dotenv import load_dotenv
from spacy import Language
from spacy_langdetect import LanguageDetector

from get_tokens import get_tokens_path

DEEPL_TOKEN = os.getenv("DEEPL_TOKEN")
if DEEPL_TOKEN is None:
    load_dotenv(get_tokens_path())
    DEEPL_TOKEN = os.getenv("DEEPL_TOKEN")

class Result:
    def __init__(self, text, detected_source_lang):
        self.text = text
        self.detected_source_lang = detected_source_lang

class DeepLTranslator:
    def __init__(self):
        super().__init__()
        # initialize a DeepL translator service
        self.translator = deepl.Translator(DEEPL_TOKEN)
        spacy.cli.download("xx_ent_wiki_sm")
        spacy.load("xx_ent_wiki_sm")
        self.muulti_lang_nlp = xx_ent_wiki_sm.load()
        Language.factory("language_detector", func=self.get_lang_detector)
        if 'sentencizer' not in self.muulti_lang_nlp.pipe_names:
            self.muulti_lang_nlp.add_pipe('sentencizer')
        if 'language_detector' not in self.muulti_lang_nlp.pipe_names:
            self.muulti_lang_nlp.add_pipe('language_detector', last=True)

    def translate_to(self, text, target_lang):
        doc = self.muulti_lang_nlp(text)
        if doc._.language['language'] == 'en' and doc._.language['score'] > 0.8:
            return Result(text, "EN_US")
        result = self.translator.translate_text(
            text, target_lang=target_lang, ignore_tags="name"
        )
        if result.detected_source_lang == "EN":
            result.detected_source_lang = "EN-US"
        elif result.detected_source_lang == "PT":
            result.detected_source_lang = "PT-PT"
        return result

    def get_lang_detector(self, nlp, name):
        return LanguageDetector()


if __name__ == "__main__":
    translator = DeepLTranslator()
    result = translator.translate_to("Was sind xyhj", "EN-US")
    result2 = translator.translate_to("How are you", "EN-US")

    print(result.text)
    print(result.detected_source_lang)
    print(result2.text)
    print(result2.detected_source_lang)
