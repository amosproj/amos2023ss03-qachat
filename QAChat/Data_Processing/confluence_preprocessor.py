# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Hafidz Arifin
# SPDX-FileCopyrightText: 2023 Abdelkader Alkadour

import io
import os
from datetime import datetime
from typing import List
import re

import requests
from weaviate.embedded import EmbeddedOptions
import weaviate
from atlassian import Confluence
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from QAChat.Data_Processing.google_doc_preprocessor import GoogleDocPreProcessor
from data_preprocessor import DataPreprocessor
from document_embedder import DataInformation, DataSource
from QAChat.Data_Processing.pdf_reader import PDFReader
from get_tokens import get_tokens_path
from QAChat.Common.init_db import init_db

load_dotenv(get_tokens_path())

# Get Confluence API credentials from environment variables
CONFLUENCE_ADDRESS = os.getenv("CONFLUENCE_ADDRESS")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN")



class ConfluencePreprocessor(DataPreprocessor):
    def __init__(self):
        self.confluence = Confluence(
            url=CONFLUENCE_ADDRESS,
            username=CONFLUENCE_USERNAME,
            password=CONFLUENCE_TOKEN,
            cloud=True,
        )
        self.pdf_reader = PDFReader()
        self.all_spaces = []
        self.all_pages_id = []
        self.all_page_information = []
        self.restricted_pages = []
        self.restricted_spaces = []
        self.weaviate_client = weaviate.Client(embedded_options=EmbeddedOptions())
        self.last_update_lookup = dict()
        self.chunk_id_lookup_table = dict()
        self.g_docs_proc = GoogleDocPreProcessor()

        init_db(self.weaviate_client)
        self.pdf_reader = PDFReader()

    def init_blacklist(self):
        # Retrieve blacklist data from Supabase table
        blacklist = (
            self.weaviate_client.query.get("BlackList", ["identifier", "note"]).do()["data"]["Get"]["BlackList"]
        )

        # Extract restricted spaces and restricted pages from the blacklist data
        for entries in blacklist:
            if "/pages/" in entries["identifer"]:
                # Split by slash and get the page id, https://.../pages/PAGE_ID
                self.restricted_pages.append(entries["identifer"].split("/")[7])
            else:
                # Split by slash and get the space name, https://.../space/SPACE_NAME
                self.restricted_spaces.append(entries["identifer"].split("/")[5])

    def get_all_spaces(self):
        start = 0
        limit = 500

        # Get all spaces first
        while True:
            # url:      to the confluence parameter
            # username: to your email used in confluence
            # password: if confluence is cloud set Confluence API Token https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
            #           if confluence is server set your password
            # cloud:    True if confluence is cloud version

            # Get all confluence spaces from the confluence instance
            spaces_data = self.confluence.get_all_spaces(
                start=start, limit=limit, expand=None
            )

            for space in spaces_data["results"]:
                # exclude personal/user spaces only global spaces
                if space["type"] == "global":
                    # exclude blacklisted spaces
                    if space["key"] not in self.restricted_spaces:
                        self.all_spaces.append(space)

            # Check if there are more spaces
            if len(spaces_data) < limit:
                break
            start = start + limit

    def get_all_page_ids_from_spaces(self):
        # Get all pages from a space
        for space in self.all_spaces:
            start = 0
            limit = 100

            while True:
                pages_data = self.confluence.get_all_pages_from_space(
                    space["key"],
                    start=start,
                    limit=limit,
                    status=None,
                    expand=None,
                    content_type="page",
                )
                #  Get all page id
                for page in pages_data:
                    if page["id"] not in self.restricted_pages:
                        self.all_pages_id.append(page["id"])

                # Check if there are more pages
                if len(pages_data) < limit:
                    break
                start = start + limit

    def get_relevant_data_from_pages(self):
        # Get all relevant information from each page
        for page_id in self.all_pages_id:
            # Get page by id
            page_with_body = self.confluence.get_page_by_id(
                page_id, expand="body.storage, version", status=None, version=None
            )
            page_info = self.confluence.get_page_by_id(
                page_id, expand=None, status=None, version=None
            )

            # Set final parameters for DataInformation
            last_changed = self.get_last_modified_formated_date(page_info)
            text = self.get_raw_text_from_page(page_with_body)

            # get googledoc url:
            urls = re.findall(r"https?://docs\.google\.com\S+", text)

            # get content from googledoc
            google_doc_content = self.get_content_from_google_drive(urls)

            # get content from confluence attachments
            pdf_content = self.get_content_from_page_attachments(page_id)

            # replace consecutive occurrences of \n into one space
            text = re.sub(
                r"\n+", " ", text + " " + google_doc_content + " " + pdf_content
            )

            # Add Page content to list of DataInformation
            self.all_page_information.append(
                DataInformation(
                    id=page_id,
                    last_changed=last_changed,
                    typ=DataSource.CONFLUENCE,
                    text=text,
                )
            )

    def get_last_modified_formated_date(self, page_info) -> datetime:
        # Get date of last modified page
        data_last_changed = page_info["version"]["when"]
        year_string = data_last_changed[0:4]
        month_string = data_last_changed[5:7]
        day_string = data_last_changed[8:10]

        # Convert string to int
        year = int(year_string)
        month = int(month_string)
        day = int(day_string)

        return datetime(year, month, day)

    def get_raw_text_from_page(self, page_with_body) -> str:
        # Get page content
        page_in_html = page_with_body["body"]["storage"]["value"]

        # Convert HTML page content to raw text
        page_in_raw_text = BeautifulSoup(page_in_html, features="html.parser")

        return page_in_raw_text.get_text()

    def get_content_from_google_drive(self, urls):
        pdf_content = ""

        # go through all urls
        for url in urls:
            # get id from url
            google_drive_id = url.split("/d/")[1].split("/")[0]

            # get pdf by id
            pdf_bytes = self.g_docs_proc.export_pdf(google_drive_id)

            # get content from pdf
            pdf_content += self.pdf_reader.read_pdf(pdf_bytes) + " "

        return pdf_content

    def get_content_from_page_attachments(self, page_id) -> str:
        start = 0
        limit = 100
        attachments = []

        number_of_attachments = self.confluence.get_attachments_from_content(
            page_id=page_id, start=start, limit=limit
        )["size"]
        pdf_content = ""

        if number_of_attachments > 0:
            # iterate over all attachments
            while True:
                attachments_container = self.confluence.get_attachments_from_content(
                    page_id=page_id, start=start, limit=limit
                )

                attachments.extend(attachments_container["results"])

                # Check if there are more spaces
                if len(attachments_container) < limit:
                    break
                start = start + limit

            if len(attachments) > 0:
                for attachment in attachments:
                    if "application/pdf" == attachment["extensions"]["mediaType"]:
                        download_link = (
                                self.confluence.url + attachment["_links"]["download"]
                        )
                        r = requests.get(
                            download_link,
                            auth=(self.confluence.username, self.confluence.password),
                        )

                        if r.status_code == 200:
                            pdf_bytes = io.BytesIO(r.content).read()

                            pdf_content += self.pdf_reader.read_pdf(pdf_bytes) + " "
        return pdf_content

    def load_preprocessed_data(
            self, end_of_timeframe: datetime, start_of_timeframe: datetime
    ) -> List[DataInformation]:
        self.init_lookup_tables()
        self.init_blacklist()
        self.get_all_spaces()
        self.get_all_page_ids_from_spaces()
        self.get_relevant_data_from_pages()
        self.filter_pages()
        return [data for data in self.all_page_information]

    def init_lookup_tables(self):
        # get the metadata of type Confluence from DB
        data = \
        self.weaviate_client.query.get("Embeddings", ["type", "type_id", "last_changed"]).with_where({"path": ["type"],
                                                                                                      "operator": "Equal",
                                                                                                      "valueString": "confluence"}).do()[
            "data"]["Get"]["Embeddings"]

        for i in data:
            page_id = i["type_id"].split("_")[0]
            chunk_id = i["type_id"].split("_")[1]
            last_update = i["last_changed"]

            # add each ID in dict last_update_lookup
            if page_id not in self.last_update_lookup:
                self.last_update_lookup[page_id] = datetime.strptime(
                    last_update.split("T")[0], "%Y-%m-%d"
                )

            # add max of chunk ID to chunk_id_lookup_table
            if page_id not in self.chunk_id_lookup_table:
                self.chunk_id_lookup_table[page_id] = chunk_id
            else:
                if chunk_id > self.chunk_id_lookup_table[page_id]:
                    self.chunk_id_lookup_table[page_id] = chunk_id

    def filter_pages(self):
        to_delete = []
        for i in self.all_page_information:
            if i.id in self.last_update_lookup:  # if page is already in DB
                if (
                        i.last_changed > self.last_update_lookup[i.id]
                ):  # if there is a change in the page
                    self.remove_from_db(i.id)  # remove from DB
                    self.last_update_lookup[
                        i.id
                    ] = None  # make the dict's entry None -> To detect remove page
                elif (
                        i.last_changed == self.last_update_lookup[i.id]
                ):  # if no change in the page
                    to_delete.append(i)  # append in the list
                    self.last_update_lookup[
                        i.id
                    ] = None  # make the dict's entry None -> To detect remove page

        for i in to_delete:
            self.all_page_information.remove(
                i
            )  # remove the page where no changes from the internal list

        for i in self.last_update_lookup:
            if (
                    self.last_update_lookup[i] is not None
            ):  # check which entry is not None -> Page is deleted from website
                self.remove_from_db(i)  # remove it from DB

    def remove_from_db(self, id):
        # loop over max number in chunk id and remove all the rows from DB
        for i in range(0, int(self.chunk_id_lookup_table[id]) + 1):
            self.weaviate_client.batch.delete_objects("Embeddings", {"path": ["type_id"],
                                                                     "operator": "Equal",
                                                                     "valueString": str(id) + "_" + str(i)})


if __name__ == "__main__":
    cp = ConfluencePreprocessor()

    date_string = "2023-05-04"
    format_string = "%Y-%m-%d"

    z = cp.load_preprocessed_data(
        datetime.now(), datetime.strptime(date_string, format_string)
    )
    for i in z:
        print(i.id)
        print(i.text)
        print(i.typ)
        print(i.last_changed)
        print("----" * 5)
