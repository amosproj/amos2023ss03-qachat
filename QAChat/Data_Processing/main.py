# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Tim Palarus
# SPDX-FileCopyrightText: 2023 Amela Pucic
# SPDX-FileCopyrightText: 2023 Hafidz Arifin

from document_embedder import DocumentEmbedder, DataSource
from dotenv import load_dotenv
import os

load_dotenv("../tokens.env")
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN")

if __name__ == '__main__':

    DocumentEmbedder().store_information_in_database(DataSource.CONFLUENCE)
