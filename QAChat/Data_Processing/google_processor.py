# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Recursively extracts the text from a Google Doc.
"""
import os, re, io

import googleapiclient.discovery as discovery
from dotenv import load_dotenv

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from QAChat.Data_Processing.pdf_reader import read_pdf

SCOPES = 'https://www.googleapis.com/auth/documents.readonly'
DISCOVERY_DOC = 'https://docs.googleapis.com/$discovery/rest?version=v1'
DOCUMENT_ID = 'YOUR_DOCUMENT_ID'

settings = {
    "client_config_backend": "file",
    "client_config_file": "client_secrets.json",
    "client_config": {"client_id": "your_client_id", "client_secret": "your_client_secret"},
    "save_credentials": True,
    "save_credentials_backend": "file",
    "save_credentials_file": "credentials.json",
    "oauth_scope": ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.install"],
    "client_config_service": "installed"
}
gauth = GoogleAuth(settings=settings)
gauth.LocalWebserverAuth()
print(gauth.credentials)


drive = GoogleDrive(gauth)

def get_google_doc_id_from_link(link):
     return link.split("/d/")[1].split("/")[0]

     # Regular expression pattern to match Google Docs document ID
     #pattern = r"https?:\/\/docs\.google\.com\/document\/d\/[a-zA-Z0-9_-]+"


     # Find the document ID using the pattern
     #match = re.search(pattern, link)


     #if match:
     #    return match.gs
     #else:
     #    return None

def get_text_from_googledoc(url):
    id = get_google_doc_id_from_link(url)
    text = drive.CreateFile({'id': id}).GetContentString(mimetype="text/plain")
    return text


def get_google_doc_as_pdf(url):

    id = get_google_doc_id_from_link(url)

    # Retrieve the file by ID
    file = drive.CreateFile({'id': id})

    # Set the download format to PDF
    file['exportFormat'] = 'pdf'

    # Download the file as PDF
    file.GetContentFile('output.pdf')

    # Process the downloaded PDF file
    #pdf_content = read_pdf( ).read())


    #print(read_pdf(io.BytesIO(file.GetContentFile('output.pdf').content).read()))

    #return pdf_content




if __name__ == '__main__':
    #text = get_text_from_googledoc("https://docs.google.com/document/d/1UxipR3mJfZjdKslGFZrTLmh78pfjKpfW7HxZ4phuWPs/edit")
    #print(text)

    text = get_google_doc_as_pdf("https://docs.google.com/presentation/u/0/d/1ZslqpJ6lG4WFEzekqJ8qv0vx-UwPeJkZ/edit?usp=slides_home&ths=true&rtpof=true")
    print(text)


