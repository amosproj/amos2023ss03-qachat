import QA_Bot.APIInterface as APIInterface
import json
from supabase import create_client, Client
from langchain.embeddings import HuggingFaceInstructEmbeddings


class QABot:

    def __init__(self, api_interface=None, supabase_url=None, supabase_key=None, llm_list=None):
        self.answer = None
        self.context = None
        self.api_interface = api_interface
        # self.supabase: Client = create_client(supabase_url, supabase_key)
        self.llm_list = llm_list
        self.embeddings = HuggingFaceInstructEmbeddings(query_instruction="Represent the query for retrieval: ")
        # for testing
        self.i = 0

    def ask_question(self, question, context):
        # TODO: self.answer = ask selected LLM
        return self.answer

    def get_embedding(self, question):
        return self.embeddings.embed_query(question)

    def sim_search(self, question_embedding):
        question_embedding_json = json.dumps(question_embedding)
        # TODO:  still needs a corresponding supabase sql query
        # self.context = supabase.rpc("search_documents", {"query_embedding": question_embedding_json})
        return "sdssdsdsdss"

    def answer_question(self, question):
        if self.api_interface is None:
            self.api_interface = APIInterface.APIInterface()
        question_embedding = self.get_embedding(question)
        self.context = self.sim_search(question_embedding)
        self.answer = self.ask_question(question, self.context)

        # for testing
        if self.answer is None:
            self.answer = ""
        self.answer += ": Resolved Questions:" + str(self.i)

        self.api_interface.forward_answer(self.answer)
