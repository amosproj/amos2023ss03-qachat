# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Tim Palarus
# SPDX-FileCopyrightText: 2023 Amela Pucic

from datetime import datetime
from typing import List

from document_embedder import DataInformation, DataSource
from data_preprocessor import DataPreprocessor


class DummyPreprocessor(DataPreprocessor):
    def load_preprocessed_data(self, before: datetime, after: datetime) -> List[DataInformation]:
        raw_data = [
            DataInformation(id="1", last_changed=datetime(2021, 1, 1), typ=DataSource.DUMMY,
                            text="This is a dummy text."),
            DataInformation(id="2", last_changed=datetime(2021, 1, 2), typ=DataSource.DUMMY,
                            text="This is another dummy text."),
            DataInformation(id="3", last_changed=datetime(2021, 1, 3), typ=DataSource.DUMMY,
                            text="This is a third dummy text."),
            DataInformation(id="4", last_changed=datetime(2023, 1, 3), typ=DataSource.DUMMY,
                            text="This is another dummy text, that is changed."),
            DataInformation(id="5", last_changed=datetime(2023, 1, 3), typ=DataSource.DUMMY,
                            text="To connect to the QAWare SSH server please use the following command: ssh -p 2222 qaware@localhost"),
            DataInformation(id="6", last_changed=datetime(2023, 1, 3), typ=DataSource.DUMMY,
                            text="You can find our office in: Aschauer Straße 32. The office is located in the 3rd floor. Also there is a cantine in the 2nd floor for employees."),
        ]

        return [data for data in raw_data if after < data.last_changed <= before]
