# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel
# SPDX-FileCopyrightText: 2023 Jesse Palarus
# SPDX-FileCopyrightText: 2023 Amela Pucic

import os

from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from supabase import create_client
from dotenv import load_dotenv
from typing import List


class QABot:

    def __init__(self, embeddings=None, database=None):
        self.answer = None
        self.context = None
        load_dotenv("tokens.env")

        self.embeddings = embeddings
        if embeddings is None:
            self.embeddings = HuggingFaceInstructEmbeddings(
                model_name="hkunlp/instructor-xl",
            )

        self.database = database
        if database is None:
            client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY"))
            self.database = SupabaseVectorStore(client=client, embedding=self.embeddings, table_name="data_embedding",
                                                query_name="match_data")

    def __answer_question_with_context(self, question: str, context: List[str]) -> str:
        """
            This method takes a question and a list of context strings as input, and attempts to answer the question using the provided context.

            The method uses the context to understand the scope and reference points for the given question and then formulates an answer based on that context.

            Parameters:
            question (str): The question that needs to be answered. This should be a string containing a clear, concise question.

            context (list[str]): A list of strings providing context for the question. The list should provide relevant information that can be used to answer the question.

            Returns:
            str: The method returns a string that contains the answer to the question, formulated based on the provided context.

            Example:
            >> ask_question("What is the color of the sky?", ["The sky is blue during a clear day."])
            'The sky is blue during a clear day.'
        """

        # For the moment simply return the context without the use of an LLM
        return "\n".join(context)

    def __sim_search(self, question: str) -> List[str]:
        """
            This method uses the given question to conduct a similarity search in the database, retrieving the most relevant information for answering the question.

            The method parses the question, identifies key words and phrases, and uses these to perform a similarity search in the database. The results of the search, which are the pieces of information most similar or relevant to the question, are then returned as a list of strings.

            Parameters:
            question (str): The question that needs to be answered. This should be a string containing a clear, concise question.

            Returns:
            list[str]: The method returns a list of strings, each string being a piece of information retrieved from the database that is considered relevant for answering the question.

            Example:
            >> sim_search("What is the color of the sky?")
            ['The sky is blue during a clear day.', 'The color of the sky can change depending on the time of day, weather, and location.']

            Note: The actual return value will depend on the contents of your database.
        """
        return [context.page_content for context in self.database.similarity_search(question, k=3)]

    def answer_question(self, question: str, user_id) -> str:
        """
            This method takes a user's question as input and returns an appropriate answer.

            Parameters:
            question (str): The question that needs to be answered. This should be a string containing a clear, concise question.

            Returns:
            str: The method returns a string that contains the answer to the question.

            Example:
            >> answer_question("What is the color of the sky?")
            'The sky is blue during a clear day.'
        """

        context = self.__sim_search(question)
        answer = self.__answer_question_with_context(question, context)
        return answer
