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
import logging
import os

load_dotenv("../tokens.env")

CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN")


class ConfluencePreprocessor(DataPreprocessor):
    def load_preprocessed_data(self, before: datetime, after: datetime) -> List[DataInformation]:

        all_spaces = []
        all_pages_id = []
        all_page_information = []

        try:

            start = 0
            limit = 500

            # Get all spaces first
            while True:

                # TODO: need to change parameter
                # url:      to the confluence parameter
                # username: to your email used in confluence
                # password: if confluence is cloud set Confluence API Token https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
                #           if confluence is server set your password
                # cloud:    True if confluence is cloud version

                confluence = Confluence(
                    url='https://qaware-confluence2.atlassian.net/',
                    username='user@email.com',
                    password=CONFLUENCE_TOKEN,
                    cloud=True)

                # Get all confluence spaces from the confluence instance
                spaces_data = confluence.get_all_spaces(start=start, limit=limit, expand=None)

                # exclude personal/user spaces only global spaces
                for space in spaces_data['results']:
                    if space['type'] == 'global':
                        all_spaces.append(space)

                # Check if there are more spaces
                if len(spaces_data) < limit:
                    break
                start = start + limit


            # Get all pages from a space
            for space in all_spaces:

                start = 0
                limit = 100

                while True:
                    pages_data = confluence.get_all_pages_from_space(space['key'], start=start, limit=limit, status=None,
                                                                     expand=None, content_type='page')
                    #  Get all page id
                    for page in pages_data:
                        all_pages_id.append(page['id'])

                    # Check if there are more pages
                    if len(pages_data) < limit:
                        break
                    start = start + limit

            # Get all relevant information from each page
            for page_id in all_pages_id:
                # Get page by id
                page_with_body = confluence.get_page_by_id(page_id, expand='body.storage, version', status=None,
                                                           version=None)
                page_info = confluence.get_page_by_id(page_id, expand=None, status=None, version=None)

                # Get page content
                page_in_html = page_with_body['body']['storage']['value']

                # Convert HTML page content to raw text
                page_in_raw_text = BeautifulSoup(page_in_html, features="html.parser")

                # Get date of last modified page
                data_last_changed = page_info['version']['when']
                year_string = data_last_changed[0:4]
                month_string = data_last_changed[5:7]
                day_string = data_last_changed[8:10]

                # Convert string to int
                year = int(year_string)
                month = int(month_string)
                day = int(day_string)

                # Set final parameters for DataInformation
                last_changed = datetime(year, month, day)
                text = page_in_raw_text.get_text()

                # Add to list of DataInformation
                all_page_information.append(
                    DataInformation(id=page_id, last_changed=last_changed, typ=DataSource.CONFLUENCE, text=text))

            return all_page_information



        except Exception as e:
            logging.error(e)
