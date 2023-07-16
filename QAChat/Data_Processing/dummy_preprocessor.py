# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Palarus
# SPDX-FileCopyrightText: 2023 Amela Pucic

from datetime import datetime
from typing import List

import pandas as pd

from data_preprocessor import DataPreprocessor
from document_embedder import DataInformation, DataSource


class DummyPreprocessor(DataPreprocessor):
    def load_preprocessed_data(
            self, end_of_timeframe: datetime, start_of_timeframe: datetime
    ) -> List[DataInformation]:
        df = pd.read_csv("../../DummyData/qa_less_50.csv", sep=";")
        raw_data = []
        for index, row in df.iterrows():
            raw_data.append(
                DataInformation(
                    id=f"{index}",
                    last_changed=datetime(2021, 1, 1),
                    typ=DataSource.DUMMY,
                    text=row["Answer"],
                )
            )

        return [
            data
            for data in raw_data
            if start_of_timeframe < data.last_changed <= end_of_timeframe
        ]
