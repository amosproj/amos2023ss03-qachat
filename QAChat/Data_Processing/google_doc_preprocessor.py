# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Hafidz Arifin
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel

from __future__ import print_function
import io
from QAChat.Data_Processing.pdf_reader import PDFReader
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account


class GoogleDocPreProcessor:
    def __init__(self):
        self.creds = None

    def export_pdf(self, real_file_id):
        if self.creds is None or not self.creds.valid:
            credentials = service_account.Credentials.from_service_account_file(
                "credentials_file.json",
                scopes=["https://www.googleapis.com/auth/drive"],
            )
        try:
            service = build("drive", "v3", credentials=credentials)

            request = service.files().export_media(
                fileId=real_file_id, mimeType="application/pdf"
            )
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")
                print("")

        except HttpError as error:
            print(f"An error occurred: {error}")
            print("")
            file = None

        return file.getvalue()


if __name__ == "__main__":
    g_doc_proc = GoogleDocPreProcessor()
    pdf_reader = PDFReader()
    file_data = g_doc_proc.export_pdf(
        real_file_id="1UxipR3mJfZjdKslGFZrTLmh78pfjKpfW7HxZ4phuWPs"
    )
    print(pdf_reader.read_pdf(file_data))
    file_data = g_doc_proc.export_pdf(
        real_file_id="1UxipR3mJfZjdKslGFZrTLmh78pfjKpfW7HxZ4phuWPs"
    )
    print(pdf_reader.read_pdf(file_data))
