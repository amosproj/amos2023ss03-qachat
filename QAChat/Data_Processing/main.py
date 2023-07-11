# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Tim Palarus
# SPDX-FileCopyrightText: 2023 Amela Pucic

from document_embedder import DocumentEmbedder, DataSource
from QAChat.Common.bucket_managing import upload_database

if __name__ == "__main__":
    DocumentEmbedder().store_information_in_database(DataSource.CONFLUENCE)
    DocumentEmbedder().store_information_in_database(DataSource.SLACK)
    upload_database()
