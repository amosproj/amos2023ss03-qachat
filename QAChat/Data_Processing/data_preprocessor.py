# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Tim Palarus
# SPDX-FileCopyrightText: 2023 Amela Pucic

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from document_embedder import DataInformation


class DataPreprocessor(ABC):
    @abstractmethod
    def load_preprocessed_data(
        self, before: datetime, after: datetime
    ) -> List[DataInformation]:
        """
        Loads preprocessed data of a specific type that was created or modified
        within a certain timeframe.

        The specific data type is defined by the superclass of the instance calling this method.

        Parameters:
        before (type): The end of the timeframe during which the data was created or modified.
        after (type): The start of the timeframe during which the data was created or modified.

        Returns:
        List[DataInformation]: A list of DataInformation instances representing the preprocessed data.
        """
        pass
