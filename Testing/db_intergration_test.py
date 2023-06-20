# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Abdelkader Alkadour
# SPDX-FileCopyrightText: 2023 Amela Pucic

import unittest
import os
import supabase
from dotenv import load_dotenv

"""
Here is an integration test to  verify the existence of two databses
"""


class DatabaseIntegrationTestDBExist(unittest.TestCase):
    def setUp(self):
        load_dotenv("../tokens.env")
        # Creating a Supabase client using environment variables
        self.supabase_client = supabase.create_client(
            os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY")
        )

    def test_if_data_embedding_exists(self):
        # Selecting all columns from the "data_embedding" table using the Supabase client
        response = self.supabase_client.table("data_embedding").select("*").execute()
        # Asserting that the response type is "postgrest.base_request_builder.APIResponse"
        self.assertEqual(
            str(type(response)).split("'")[1],
            "postgrest.base_request_builder.APIResponse",
        )

    def test_if_last_update_per_data_typ_exists(self):
        # Selecting all columns from the "last_update_per_data_typ" table using the Supabase client
        response = (
            self.supabase_client.table("last_update_per_data_typ").select("*").execute()
        )
        # Asserting that the response type is "postgrest.base_request_builder.APIResponse"
        self.assertEqual(
            str(type(response)).split("'")[1],
            "postgrest.base_request_builder.APIResponse",
        )


"""
Here is an integration to check the writing, reading and deleting from the database
"""


class DatabaseIntegrationTestDBInteract(unittest.TestCase):
    def setUp(self):
        # Creating a Supabase client using environment variables
        self.supabase_client = supabase.create_client(
            os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY")
        )

    def test_db_interaction(self):
        test_obj = {
            "content": "JUST A TEST OBJECT",
            "metadata": {
                "last_changed": "01.01.1000",
                "type": "dummy",
                "id": "999999999999999999",
            },
            "embedding": [0] * 768,
        }
        # Inserting the test object into the "data_embedding" table
        result = self.supabase_client.table("data_embedding").insert(test_obj).execute()
        # Asserting that the ID of the inserted object matches the expected ID
        self.assertAlmostEqual(int(result.json().split('"')[21]), 999999999999999999)

        # Selecting the object from the "data_embedding" table based on the content
        result = (
            self.supabase_client.table("data_embedding")
            .select("content")
            .eq("content", "JUST A TEST OBJECT")
            .execute()
        )
        # Asserting that the selected object's content matches the expected content
        self.assertEqual(result.json().split('"')[5], "JUST A TEST OBJECT")

        # Deleting the object from the "data_embedding" table based on the content
        result = (
            self.supabase_client.table("data_embedding")
            .delete()
            .eq("content", "JUST A TEST OBJECT")
            .execute()
        )
        # Asserting that the deleted object's content matches the expected content
        self.assertEqual(result.json().split('"')[7], "JUST A TEST OBJECT")


if __name__ == "__main__":
    unittest.main()
