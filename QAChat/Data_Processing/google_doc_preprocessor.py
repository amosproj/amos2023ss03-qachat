# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Hafidz Arifin
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel

from __future__ import print_function

import io
from pdf_reader import read_pdf
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow


def export_pdf(real_file_id):
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", ["https://www.googleapis.com/auth/drive"]
    )
    creds = flow.run_local_server()

    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)

        file_id = real_file_id

        request = service.files().export_media(
            fileId=file_id, mimeType="application/pdf"
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
    print(
        read_pdf(
            export_pdf(real_file_id="1UxipR3mJfZjdKslGFZrTLmh78pfjKpfW7HxZ4phuWPs")
        )
    )
