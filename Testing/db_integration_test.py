# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Abdelkader Alkadour
# SPDX-FileCopyrightText: 2023 Amela Pucic
# SPDX-FileCopyrightText: 2023 Felix Nützel

import unittest
import weaviate
from weaviate.embedded import EmbeddedOptions
import re

from QAChat.Common.init_db import init_db

"""
Here is an integration test to  verify the existence of two databses
"""


class DatabaseIntegrationTestDBExist(unittest.TestCase):
    def setUp(self):
       self.weaviate_client = weaviate.Client(embedded_options=EmbeddedOptions())
       init_db(self.weaviate_client)

    def test_if_data_embedding_exists(self):
        # Selecting all properties from the "Embeddings" class using the Weaviate client
        response = self.weaviate_client.query.get("Embeddings")
        # Asserting that the response type is "weaviate.gql.get.GetBuilder" and the name is "Embeddings"
        self.assertEqual(
            str(type(response)).split("'")[1],
            "weaviate.gql.get.GetBuilder",
        )
        self.assertEqual(response.name, "Embeddings")

    def test_if_last_update_per_data_typ_exists(self):
        # Selecting all columns from the "last_update_per_data_typ" table using the Supabase client
        response = (
            self.weaviate_client.query.get("LastChanged")
        )
        # Asserting that the response type is "weaviate.gql.get.GetBuilder" and the name is "LastChanged"
        self.assertEqual(
            str(type(response)).split("'")[1],
            "weaviate.gql.get.GetBuilder",
        )
        self.assertEqual(response.name, "LastChanged")


"""
Here is an integration to check the writing, reading and deleting from the database
"""


class DatabaseIntegrationTestDBInteract(unittest.TestCase):
    def setUp(self):
        self.weaviate_client = weaviate.Client(embedded_options=EmbeddedOptions())
        init_db(self.weaviate_client)

    def test_db_interaction(self):
        test_obj = {
            "text": "JUST A TEST OBJECT",
            "last_changed": "01.01.1000",
            "type": "dummy",
            "type_id": "999999999999999999",
            "embedding": [0] * 768,
        }
        # Inserting the test object into the "data_embedding" table
        self.weaviate_client.data_object.create(test_obj, "Embeddings")
        result = self.weaviate_client.query.get("Embeddings", properties=["type_id"]).with_where({
            "path": "text",
            "operator": "Equal",
            "valueString": "JUST A TEST OBJECT",
        }).do()

        # Asserting that the ID of the inserted object matches the expected ID
        self.assertEqual(result["data"]["Get"]["Embeddings"][0]["type_id"], '999999999999999999')
        # Selecting the object from the "data_embedding" table based on the content
        result = self.weaviate_client.query.get("Embeddings", properties=["text"]).with_where({
                            "path": "text",
                            "operator": "Equal",
                            "valueString": "JUST A TEST OBJECT",
                        }).do()
        # Asserting that the selected object's content matches the expected content
        self.assertEqual(result["data"]["Get"]["Embeddings"][0]["text"], 'JUST A TEST OBJECT')

        # Deleting the object from the "data_embedding" table based on the content
        result = (
            self.weaviate_client.batch.delete_objects("Embeddings", where={
                            "path": ["text"],
                            "operator": "Equal",
                            "valueString": "JUST A TEST OBJECT",
                        })
        )

        # Asserting that the object is deleted successfully
        self.assertTrue(result["results"]["successful"] > 0)


if __name__ == "__main__":
    unittest.main()
