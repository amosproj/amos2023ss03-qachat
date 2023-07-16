# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Hafidz Arifin

from dotenv import load_dotenv
from atlassian import Confluence
from bs4 import BeautifulSoup
import unittest
import requests
import random
import string
import os
import io

from QAChat.Data_Processing.pdf_reader import PDFReader

load_dotenv("../QAChat/tokens.env")

# Get Confluence API credentials from environment variables
CONFLUENCE_ADDRESS = os.getenv("CONFLUENCE_ADDRESS")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN")


class ConfluenceIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.confluence = Confluence(
            url=CONFLUENCE_ADDRESS,
            username=CONFLUENCE_USERNAME,
            password=CONFLUENCE_TOKEN,
            cloud=True,
        )

    def test_reading(self):
        # set parameter for new page
        space = "Test2"
        page_title = "Example Page " + "".join(
            random.choice(string.ascii_lowercase) for i in range(4)
        )
        page_body = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."

        # create page
        self.confluence.create_page(
            space,
            page_title,
            page_body,
            parent_id=None,
            type="page",
            representation="storage",
            editor="v2",
            full_width=False,
        )

        # get page id
        page_id = self.confluence.get_page_id(space, page_title)

        # get page body
        page_raw_body = self.confluence.get_page_by_id(
            page_id, expand="body.storage, version", status=None, version=None
        )["body"]["storage"]["value"]

        # filter page body
        page_filtered_body = BeautifulSoup(
            page_raw_body, features="html.parser"
        ).get_text()

        # set pdf
        test_pdf = "../Deliverables/sprint-03/planning-documents.pdf"

        # attach pdf
        self.confluence.attach_file(
            test_pdf,
            name=None,
            content_type=None,
            page_id=page_id,
            title=None,
            space=space,
            comment=None,
        )
        # get pdf
        attachment = self.confluence.get_attachments_from_content(
            page_id=page_id, start=0, limit=100
        )["results"][0]

        # download pdf
        r = requests.get(
            self.confluence.url + attachment["_links"]["download"],
            auth=(self.confluence.username, self.confluence.password),
        )

        # read pdf from confluence
        pdf_bytes = io.BytesIO(r.content).read()
        retrieved_pdf_content = PDFReader().read_pdf(pdf_bytes)

        # read pdf from local
        with open("../Deliverables/sprint-03/planning-documents.pdf", "rb") as f:
            pdf_bytes = f.read()
        local_pdf_content = PDFReader().read_pdf(pdf_bytes)

        # delete page
        self.confluence.remove_page(page_id, status=None, recursive=False)

        # assert page body
        self.assertEqual(page_filtered_body, page_body)

        # assert page attachments
        self.assertEqual(retrieved_pdf_content, local_pdf_content)


if __name__ == "__main__":
    unittest.main()
