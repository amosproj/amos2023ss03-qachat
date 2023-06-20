# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Tim Palarus
# SPDX-FileCopyrightText: 2023 Amela Pucic
# SPDX-FileCopyrightText: 2023 Felix Nützel
# SPDX-FileCopyrightText: 2023 Emanuel Erben

import os
from datetime import datetime
from enum import Enum

from dateutil import parser
from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from supabase.client import create_client
import spacy
import spacy.cli
import xx_ent_wiki_sm
import de_core_news_sm

from QAChat.Common.deepL_translator import DeepLTranslator
from get_tokens import get_tokens_path

from QAChat.Data_Processing.text_transformer import transform_text_to_chunks


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

        load_dotenv(get_tokens_path())
        self.supabase = create_client(
            os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_KEY")
        )
        self.vector_store = SupabaseVectorStore(
            self.supabase,
            embedding=self.embedder,
            table_name="data_embedding",
            query_name="match_data",
        )

        # name identification
        spacy.cli.download("xx_ent_wiki_sm")
        spacy.load("xx_ent_wiki_sm")
        self.muulti_lang_nlp = xx_ent_wiki_sm.load()
        spacy.cli.download("de_core_news_sm")
        spacy.load("de_core_news_sm")
        self.de_lang_nlp = de_core_news_sm.load()
        self.translator = DeepLTranslator()

    def store_information_in_database(self, typ: DataSource):
        if typ == DataSource.DUMMY:
            from dummy_preprocessor import DummyPreprocessor

            data_preprocessor = DummyPreprocessor()
        elif typ == DataSource.CONFLUENCE:
            from confluence_preprocessor import ConfluencePreprocessor

            data_preprocessor = ConfluencePreprocessor()
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

        # identify names and add name-tags before chunking and translation
        all_changed_data = self.identify_names(all_changed_data)

        # transform long entries into multiple chunks and translation to english
        all_changed_data = transform_text_to_chunks(all_changed_data)

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

    def identify_names(self, all_data: list[DataInformation]) -> list[DataInformation]:
        """
        Method identifies names with spacy and adds name tags to the text
        :param all_data:  which is the List of DataInformation that gets send to the chunking
        :return: the input list with added name tags to persons
        """

        for data in all_data:
            # identify language of text
            language = self.translator.translate_to(
                data.text, "EN-US"
            ).detected_source_lang
            # choose spacy model after language
            if language == "DE":
                nlp = self.de_lang_nlp
            else:
                nlp = self.muulti_lang_nlp
            # identify sentence parts
            doc = nlp(data.text)
            already_replaced = []
            for ent in doc.ents:
                if ent.text in already_replaced or ent.label_ != "PER":
                    continue
                # only person names are flanked by tag and multiplicity is avoided
                already_replaced.append(ent.text)
                data.text = data.text.replace(ent.text, "<name>" + ent.text + "</name>")
        return all_data
