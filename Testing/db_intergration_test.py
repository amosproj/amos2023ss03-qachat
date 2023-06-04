import unittest
from langchain.vectorstores import SupabaseVectorStore
import os
from supabase.client import create_client
import supabase
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceInstructEmbeddings



load_dotenv("/Users/kad/Desktop/AMOS/amos2023ss03-qachat/tokens.env")

class Embedder():
    def __init__(self):
        pass


class DatabaseIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.embedder = Embedder()
    
    def test_integration_scenario_positive(self):
        supabase_client = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY"))
        db = SupabaseVectorStore(supabase_client, embedding=self.embedder, table_name="data_embedding")
        self.assertEqual(db.table_name, "data_embedding")
    
    def test_integration_scenario_negative_url(self):
        with self.assertRaises(supabase.client.SupabaseException):
            supabase_client = create_client(None, os.environ.get("SUPABASE_SERVICE_KEY"))
            db = SupabaseVectorStore(supabase_client, embedding=self.embedder, table_name="data_embedding")

    def test_integration_scenario_negative_url_format(self):
        with self.assertRaises(supabase.client.SupabaseException):
            supabase_client = create_client("htp://google.com", os.environ.get("SUPABASE_SERVICE_KEY"))
            db = SupabaseVectorStore(supabase_client, embedding=self.embedder, table_name="data_embedding")
    
    def test_integration_scenario_negative_api_key(self):
        with self.assertRaises(supabase.client.SupabaseException):
            supabase_client = create_client(os.environ.get("SUPABASE_URL"), None)
            db = SupabaseVectorStore(supabase_client, embedding=self.embedder, table_name="data_embedding")


if __name__ == '__main__':
      unittest.main()
