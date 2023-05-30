# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Hafidz Arifin
# SPDX-FileCopyrightText: 2023 Abdelkader Alkadour


from atlassian import Confluence
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
import os, io, requests, PyPDF2, supabase, hashlib


# Load environment variables
# load_dotenv("../tokens.env")
load_dotenv("/Users/kad/Desktop/AMOS/amos2023ss03-qachat/tokens.env")

# Get Confluence API credentials from environment variables
CONFLUENCE_ADRESS = os.getenv("CONFLUENCE_ADRESS")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_PASSWORD = os.getenv("CONFLUENCE_PASSWORD")

# Get Supabase API credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")


class ConfluencePreprocessor:
    spaces = []
    pages = []
    restricted_spaces = []
    restricted_pages = []
    hashtable = dict()

    # Initialize Confluence API client
    confluence = Confluence(
        url=CONFLUENCE_ADRESS,
        username=CONFLUENCE_USERNAME,
        password=CONFLUENCE_PASSWORD,
        cloud=True,
    )

    # Initialize Supabase API client
    supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

    # Blacklist used to restrict pages and spaces from being saved in the database
    def init_blacklist(self):
        # Retrieve blacklist data from Supabase table
        blacklist = (
            self.supabase_client.table("confluence_blacklist")
            .select("*")
            .execute()
            .data
        )

        # Extract restricted spaces and restricted pages from the blacklist data
        for i in blacklist:
            if "/pages/" in i["identifer"]:
                # Split by slash and get the page id, https://.../pages/PAGE_ID
                self.restricted_pages.append(i["identifer"].split("/")[7])
            else:
                # Split by slash and get the space name, https://.../space/SPACE_NAME
                self.restricted_spaces.append(i["identifer"].split("/")[5])

    # Hashtable used to check weather a content of page has been changed from last update
    def init_hashtable(self):
        # Retrieve hash and page ID data from Supabase table
        hash_page_id = (
            self.supabase_client.table("confluence_data")
            .select("page_id,hash")
            .execute()
            .data
        )
        # Create a hashtable using page ID as the key and hash as the value
        self.hashtable = {i["page_id"]: i["hash"] for i in hash_page_id}

    def check_hashtable(self, key, value):
        # Check if the key exists in the hashtable and if the corresponding value matches the provided value
        if int(key) not in self.hashtable:
            return True
        elif self.hashtable[int(key)] == value:
            return False
        else:
            return True

    def calculate_hash(self, page):
        # Concatenate relevant data from the page object
        text = "".join(
            [
                page["page_id"],
                page["space"],
                page["space"],
                page["title"],
                page["content"],
                " ".join(page["attachments"]),
                " ".join(page["comments"]),
            ]
        )

        # Calculate the hash value using SHA256 algorithm
        hash_object = hashlib.sha256()
        hash_object.update(text.encode("utf-8"))
        hash_value = hash_object.hexdigest()

        return hash_value

    def get_spaces(self):
        start = 0
        limit = 500
        spaces = []

        # Get all spaces starting from 0 to 500 (max of possible retrieved spaces via API)
        # While there is no empty response, keep making requests
        while True:
            new_spaces = self.confluence.get_all_spaces(
                start=start, limit=limit, expand=None
            )
            if new_spaces["size"] == 0:
                break
            spaces.extend(new_spaces["results"])
            start += limit

        # Exclude personal/user spaces, only include global spaces, and save necessary data
        for space in spaces:
            if space["type"] == "global":
                if space["key"] not in self.restricted_spaces:
                    self.spaces.append({"key": space["key"], "name": space["name"]})

    def get_page_by_id(self, id):
        # Retrieve page content by ID and extract the text from HTML
        return self.get_text_from_html(
            self.confluence.get_page_by_id(id, expand="body.storage")["body"][
                "storage"
            ]["value"]
        )

    def get_comments(self, id):
        # Retrieve comments for a page and extract the text from HTML
        comments = []
        for i in self.confluence.get_page_child_by_type(
            id, type="comment", start=None, limit=None, expand="body.storage"
        ):
            comments.append(self.get_text_from_html(i["body"]["storage"]["value"]))
        return comments

    def get_page_attacments(
        self, id
    ):  # TODO: Change this to use the one who implemented by the team
        attachments_container = self.confluence.get_attachments_from_content(
            page_id=id, start=0, limit=500
        )
        attachments = attachments_container["results"]
        pdf_content = []
        for attachment in attachments:
            content = ""
            fname = attachment["title"]
            download_link = self.confluence.url + attachment["_links"]["download"]
            r = requests.get(
                download_link, auth=(self.confluence.username, self.confluence.password)
            )
            if r.status_code == 200:
                #   with open(fname, "wb") as f:
                #       for bits in r.iter_content():
                #           f.write(bits)
                pdf_file = io.BytesIO(r.content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)

                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    content += text
                pdf_content.append(content)
        return pdf_content

    def get_text_from_html(self, html):
        # Parse HTML using BeautifulSoup and extract the text
        return BeautifulSoup(html, features="html.parser").get_text().replace("\n", " ")

    def get_pages_from_space(self, key, name):
        start = 0
        limit = 500
        pages = []

        # Get all pages from a space starting from 0 to 500 (max of possible retrieved pages via API)
        # While there is no empty response, keep making requests
        while True:
            new_pages = self.confluence.get_all_pages_from_space(
                key,
                start=start,
                limit=limit,
                status=None,
                expand=None,
                content_type="page",
            )
            pages.extend(new_pages)
            if len(new_pages) < limit:
                break
            start += limit

        for page in pages:
            _page = {
                "page_id": page["id"],
                "space": name,
                "title": page["title"],
                "content": self.get_page_by_id(page["id"]),
                "attachments": self.get_page_attacments(page["id"]),
                "comments": self.get_comments(page["id"]),
            }

            hash = self.calculate_hash(_page)
            _page["hash"] = hash

            if _page["page_id"] not in self.restricted_pages:
                if self.check_hashtable(_page["page_id"], hash):
                    self.pages.append(_page)

    def get_pages(self):
        self.init_blacklist()
        self.init_hashtable()
        self.get_spaces()
        for space in self.spaces:
            self.get_pages_from_space(space["key"], space["name"])

    def update_data(self):
        self.get_pages()
        for page in self.pages:
            if int(page["page_id"]) in self.hashtable:
                # Update existing page in the Supabase table
                self.supabase_client.table("confluence_data").update(page).eq(
                    "page_id", page["page_id"]
                ).execute()
            else:
                # Insert new page into the Supabase table
                self.supabase_client.table("confluence_data").insert(
                    {
                        "page_id": page["page_id"],
                        "space": page["space"],
                        "title": page["title"],
                        "content": page["content"],
                        "attachments": page["attachments"],
                        "comments": page["comments"],
                        "hash": page["hash"],
                    }
                ).execute()


if __name__ == "__main__":  # TODO: Only for testing, remove this
    data_preprocessor = ConfluencePreprocessor()
    data_preprocessor.update_data()
