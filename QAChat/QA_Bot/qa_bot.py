# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel

import QAChat.QA_Bot.api_interface as APIInterface
import json
from langchain.embeddings import HuggingFaceInstructEmbeddings

from QAChat.Data_Processing.deepL_translator import DeepLTranslator


class QABot:

    def __init__(self, api_interface=None, supabase_url=None, supabase_key=None, llm_list=None):
        self.answer = None
        self.context = None
        self.api_interface = api_interface
        self.llm_list = llm_list
        self.embeddings = HuggingFaceInstructEmbeddings(query_instruction="Represent the query for retrieval: ")
        self.i = 0

    def ask_question(self, question, context):
        return question

    def get_embedding(self, question):
        return self.embeddings.embed_query(question)

    def sim_search(self, question_embedding):
        question_embedding_json = json.dumps(question_embedding)
        return "Test"

    def translate_question(self, question):
        return DeepLTranslator().receive_question(question)

    def answer_question(self, question, user_id):

        self.answer = ""
        if self.api_interface is None:
            self.api_interface = APIInterface
        translated_question = self.translate_question(question)
        question_embedding = self.get_embedding(translated_question)
        self.context = self.sim_search(question_embedding)
        self.answer = self.ask_question(translated_question, self.context)

        self.answer += ": Resolved Questions:" + str(self.i+1)
        self.i += 1

        self.api_interface.forward_answer(self.answer, user_id)

