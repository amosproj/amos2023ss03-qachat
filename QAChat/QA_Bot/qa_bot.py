# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel
# SPDX-FileCopyrightText: 2023 Jesse Palarus
# SPDX-FileCopyrightText: 2023 Amela Pucic


from huggingface_hub import hf_hub_download
from langchain import LlamaCpp, PromptTemplate
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from supabase import create_client

from QAChat.Common.deepL_translator import DeepLTranslator
from get_tokens import get_tokens_path


class QABot:
    def __init__(
            self,
            embeddings=None,
            database=None,
            model=None,
            translator=None,
            embeddings_gpu=False,
            repo_id="TheBloke/WizardLM-13B-V1.0-Uncensored-GGML",
            filename="wizardlm-13b-v1.0-uncensored.ggmlv3.q5_0.bin",
    ):
        self.answer = None
        self.context = None
        load_dotenv(get_tokens_path())

        self.embeddings = embeddings
        if embeddings is None:
            self.embeddings = HuggingFaceInstructEmbeddings(
                model_name="hkunlp/instructor-xl",
                model_kwargs=None if embeddings_gpu else {"device": "cpu"},
            )

        self.database = database
        if database is None:
            client = create_client(
                os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY")
            )
            self.database = SupabaseVectorStore(
                client=client,
                embedding=self.embeddings,
                table_name="data_embedding",
                query_name="match_data",
            )
        self.model = model
        if model is None:
            self.model = self.get_llama_model(repo_id=repo_id, filename=filename)

        self.translator = translator
        if translator is None:
            self.translator = DeepLTranslator()

    def get_llama_model(
            self,
            repo_id,
            filename,
            n_ctx=2048,
            max_tokens=512,
    ):
        path = hf_hub_download(repo_id=repo_id, filename=filename)

        return LlamaCpp(
            model_path=path,
            verbose=False,
            n_ctx=n_ctx,
            max_tokens=max_tokens,
            temperature=0,
            n_gpu_layers=100,
            repeat_penalty=0.9,
        )

    def answer_question_with_context(self, question: str, context: List[str]) -> str:
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

        context_str = "\n\n".join(
            f"{x}" for i, x in enumerate(context)
        )

        template = (
            "You are a chatbot, your primary task is to help people by answering their questions. Keep your responses short, precise, and directly related to the user's question, using the following context to guide your answer:\n"
            "{context_str}\n\n"
            "Try your best to answer based on the given context, and avoid creating new information. If the context does not provide enough details to formulate a response, or if you are unsure, kindly state that you can't provide a certain answer.\n"
            "\n\n"
            "USER: {question}"
            "ASSISTANT:"
        )
        prompt = PromptTemplate(
            template=template, input_variables=["question", "context_str"]
        )

        print(prompt.format_prompt(question=question, context_str=context_str))
        answer = self.model.generate_prompt(
            [
                prompt.format_prompt(question=question, context_str=context_str),
            ],
            stop=["</s>"],
        )
        return answer.generations[0][0].text.strip()

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
        return [
            context.page_content
            for context in self.database.similarity_search(question, k=3)
        ]

    def translate_text(self, question, language="EN-US"):
        return self.translator.translate_to(question, language)

    def answer_question(self, question: str):
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

        print(f"Receive Question: {question}")
        translation = self.translate_text(question)
        translated_question = translation.text
        print(f"Translation: {translated_question}")
        context = self.__sim_search(translated_question)
        print(f"Context: {context}")
        answer = self.answer_question_with_context(translated_question, context)
        print(f"Answer: {answer}")
        answer = self.translate_text(answer, translation.detected_source_lang).text
        print(f"Translated answer: {answer}")
        return {
            "answer": answer,
            "question": question,
            "context": context,
        }
