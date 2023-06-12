# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Felix Nützel

import math
import unittest
import pandas as pd

from QAChat.Data_Processing.document_embedder import DataInformation, DataSource
from QAChat.Data_Processing.text_transformer import transform_text_to_chunks
from QAChat.Data_Processing.text_transformer import CHUNK_SIZE
from datetime import datetime
from typing import List


class TestChunking(unittest.TestCase):

    def setUp(self):
        self.current_time = datetime.now()
        self.last_updated = datetime(1970, 1, 1)

    @staticmethod
    def __load_preprocessed_data(before: datetime, after: datetime, filepath: str) -> List[DataInformation]:
        df = pd.read_csv(filepath, sep=";")
        raw_data = []
        for index, row in df.iterrows():
            raw_data.append(
                DataInformation(
                    id=f"{index}",
                    last_changed=datetime(2021, 1, 1),
                    typ=DataSource.DUMMY,
                    text=row["Answer"] + row["Question"],
                )
            )

        return [data for data in raw_data if after < data.last_changed <= before]

    def test_smaller_than_overlap(self):
        data_list = self.__load_preprocessed_data(self.current_time, self.last_updated, "../DummyData/qa_less_50.csv")
        result = transform_text_to_chunks(data_list)
        self.assertTrue(len(result) is len(data_list))

    def test_smaller_than_chunk_size(self):
        data_list = self.__load_preprocessed_data(self.current_time, self.last_updated, "../DummyData/qa_less_200.csv")
        result = transform_text_to_chunks(data_list)
        self.assertTrue(len(result) is len(data_list))

    def test_larger_than_chunk_size(self):
        data_list = self.__load_preprocessed_data(self.current_time, self.last_updated, "../DummyData/qa_2000.csv")
        df = pd.read_csv("../DummyData/qa_2000.csv", sep=";")
        characters = len(df.to_string().strip())
        result = transform_text_to_chunks(data_list)
        new_lines = len(result)
        self.assertTrue(math.ceil(characters / CHUNK_SIZE) == new_lines)
