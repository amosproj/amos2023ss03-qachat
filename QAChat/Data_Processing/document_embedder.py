# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Tim Palarus
# SPDX-FileCopyrightText: 2023 Amela Pucic

import os
from datetime import datetime
from enum import Enum

from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from supabase.client import create_client
from dateutil import parser


class DataSource(Enum):
    SLACK = "slack"
    CONFLUENCE = "confluence"
    DRIVE = "drive"
    DUMMY = "dummy"


class DataInformation:
    def __init__(self, id: str, last_changed: datetime, typ: DataSource, text: str):
        self.id = id
        self.last_changed = last_changed
        self.typ = typ
        self.text = text


class DocumentEmbedder:
    def __init__(self):
        self.embedder = HuggingFaceInstructEmbeddings(
            model_name="hkunlp/instructor-xl",
        )

        load_dotenv("../tokens.env")
        self.supabase = create_client(
            os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY")
        )
        self.vector_store = SupabaseVectorStore(
            self.supabase,
            embedding=self.embedder,
            table_name="data_embedding",
            query_name="match_data",
        )

    def store_information_in_database(self, typ: DataSource):
        if typ == DataSource.DUMMY:
            from dummy_preprocessor import DummyPreprocessor

            data_preprocessor = DummyPreprocessor()
        elif typ == DataSource.SLACK:
            from slack_preprocessor import SlackPreprocessor

            data_preprocessor = SlackPreprocessor()
        else:
            raise ValueError("Invalid data source type")

        last_updated_database_result = (
            self.supabase.table("last_update_per_data_typ")
            .select("last_update")
            .eq("type", typ.value)
            .execute()
        )
        if len(last_updated_database_result.data) == 0:
            last_updated = datetime(1970, 1, 1)
        else:
            last_updated = parser.parse(
                last_updated_database_result.data[0]["last_update"]
            ).replace(tzinfo=None)

        current_time = datetime.now()
        all_changed_data = data_preprocessor.load_preprocessed_data(
            current_time, last_updated
        )

        if len(all_changed_data) != 0:
            ids = {data.id for data in all_changed_data}
            self.supabase.rpc(
                "delete_old_embeddings", {"ids": list(ids), "delete_type": typ.value}
            ).execute()

            self.vector_store.add_texts(
                [data.text for data in all_changed_data],
                [
                    {
                        "last_changed": data.last_changed.isoformat(),
                        "type": typ.value,
                        "id": data.id,
                    }
                    for data in all_changed_data
                ],
            )

        self.supabase.table("last_update_per_data_typ").upsert(
            {"type": typ.value, "last_update": current_time.isoformat()},
        ).execute()
