# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Tim Palarus
# SPDX-FileCopyrightText: 2023 Amela Pucic

from datetime import datetime
from typing import List

import pandas as pd
from document_embedder import DataInformation, DataSource
from data_preprocessor import DataPreprocessor


class DummyPreprocessor(DataPreprocessor):
    def load_preprocessed_data(self, before: datetime, after: datetime) -> List[DataInformation]:
        df = pd.read_csv("../../DummyData/qa.csv", sep=";")
        raw_data = []
        for index, row in df.iterrows():
            raw_data.append(DataInformation(id=f"{index}", last_changed=datetime(2021, 1, 1), typ=DataSource.DUMMY,
                                            text=row["Answer"]))

        return [data for data in raw_data if after < data.last_changed <= before]