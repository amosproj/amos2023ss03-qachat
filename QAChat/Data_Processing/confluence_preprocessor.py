# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Hafidz Arifin
# SPDX-FileCopyrightText: 2023 Abdelkader Alkadour


from document_embedder import DataInformation, DataSource
from data_preprocessor import DataPreprocessor
from atlassian import Confluence
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import supabase
import os, io
import datetime
from pdf_reader import read_pdf
import requests

load_dotenv("../tokens.env")

# Get Confluence API credentials from environment variables
CONFLUENCE_ADDRESS = os.getenv("CONFLUENCE_ADDRESS")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN")

# Get Supabase API credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")




class ConfluencePreprocessor(DataPreprocessor):

    def __init__(self):
        self.confluence = Confluence(
            url=CONFLUENCE_ADDRESS,
            username=CONFLUENCE_USERNAME,
            password=CONFLUENCE_TOKEN,
            cloud=True)
        self.all_spaces = []
        self.all_pages_id = []
        self.all_page_information = []
        self.restricted_pages = []
        self.supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

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
            spaces_data = self.confluence.get_all_spaces(start=start, limit=limit, expand=None)

            # exclude personal/user spaces only global spaces
            for space in spaces_data['results']:
                if space['type'] == 'global':
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
                pages_data = self.confluence.get_all_pages_from_space(space['key'], start=start, limit=limit,
                                                                      status=None,
                                                                      expand=None, content_type='page')
                #  Get all page id
                for page in pages_data:
                    if page["id"] not in self.restricted_pages:
                        self.all_pages_id.append(page['id'])

                # Check if there are more pages
                if len(pages_data) < limit:
                    break
                start = start + limit

    def get_relevant_data_from_pages(self):
        # Get all relevant information from each page
        for page_id in self.all_pages_id:
            # Get page by id
            page_with_body = self.confluence.get_page_by_id(page_id, expand='body.storage, version', status=None,
                                                            version=None)
            page_info = self.confluence.get_page_by_id(page_id, expand=None, status=None, version=None)

            # Set final parameters for DataInformation
            last_changed = self.get_last_modified_formated_date(page_info)
            text = self.get_raw_text_from_page(page_with_body)
            pdf_text = self.get_page_attachments(page_id)
            text += pdf_text

            # Add to list of DataInformation
            self.all_page_information.append( #check for changes 
                DataInformation(id=page_id, last_changed=last_changed, typ=DataSource.CONFLUENCE, text=text)) #TODO: append pdf

    def delete_old_content(self):
        response = self.supabase_client.table('data_embedding').select("id").eq('metadata->>type', "confluence").execute().data
        ids = []
        for i in response:
            ids.append(i["id"])
        for i in ids:
            self.supabase_client.table("data_embedding").delete().eq("id", i).execute()
        
    def get_page_attachments(self, id):
        #TODO: PDF
        """
        attachments_container = self.confluence.get_attachments_from_content(
            page_id=id, start=0, limit=500
        )
        attachments = attachments_container["results"]
        #print(attachments)

        pdf_content = ""
        for attachment in attachments:
            if "application/pdf" == attachment["extensions"]["mediaType"]:
                fname = attachment["title"]
                content = ""
                download_link = self.confluence.url + attachment["_links"]["download"]
                print(fname)
                r = requests.get(
                    download_link, auth=(self.confluence.username, self.confluence.password)
                )
                if r.status_code == 200:
                    pdf_file = io.BytesIO(r.content)
                    pdf = read_pdf(pdf_file.getvalue(), datetime.datetime(2025, 1, 1), datetime.datetime(1970, 1, 1), DataSource.CONFLUENCE)
                    if pdf is not None:
                        for i in pdf:
                            content += i.text + " "
            pdf_content += content + "#"

        return pdf_content
        """
        return ""


    def get_last_modified_formated_date(self, page_info) -> datetime:
        # Get date of last modified page
        data_last_changed = page_info['version']['when']
        year_string = data_last_changed[0:4]
        month_string = data_last_changed[5:7]
        day_string = data_last_changed[8:10]

        # Convert string to int
        year = int(year_string)
        month = int(month_string)
        day = int(day_string)

        return datetime.datetime(year, month, day)

    def get_raw_text_from_page(self, page_with_body) -> str:
        # Get page content
        page_in_html = page_with_body['body']['storage']['value']

        # Convert HTML page content to raw text
        page_in_raw_text = BeautifulSoup(page_in_html, features="html.parser")

        return page_in_raw_text.get_text()

    def load_preprocessed_data(self, before: datetime, after: datetime) -> List[DataInformation]:

        self.get_all_spaces()
        self.get_all_page_ids_from_spaces()
        self.get_relevant_data_from_pages()
        self.delete_old_content() # TODO: update

        return [data for data in self.all_page_information]



