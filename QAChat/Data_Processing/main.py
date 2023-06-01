# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Tim Palarus
# SPDX-FileCopyrightText: 2023 Amela Pucic

from document_embedder import DocumentEmbedder, DataSource

if __name__ == "__main__":
    DocumentEmbedder().store_information_in_database(DataSource.DUMMY)
    DocumentEmbedder().store_information_in_database(DataSource.SLACK)
