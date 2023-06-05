# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel


import io
import os
from datetime import datetime

import nltk
import pytesseract
from pdf2image import convert_from_bytes
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from QAChat.Data_Processing.document_embedder import DataInformation, DataSource

TESSDATA_PREFIX = os.getenv("TESSDATA_PREFIX")
nltk.download("punkt")


def get_text_from_pdf(pdf_object):
    # First try to read the PDF with PDFMiner
    text = __read_pdf_from_object(pdf_object)

    # If the result is empty or too short, try OCR
    if len(text.strip()) < 100:
        text = __ocr_pdf(pdf_object)

    return text

def read_pdf(pdf_object, before: datetime, after: datetime, data_src: DataSource):
    # First try to read the PDF with PDFMiner
    text = __read_pdf_from_object(pdf_object)

    # If the result is empty or too short, try OCR
    if len(text.strip()) < 100:
        text = __ocr_pdf(pdf_object)

    #return transform_to_data_information_list(text, before, after, data_src)


def transform_to_data_information_list(
    text, before: datetime, after: datetime, data_src: DataSource
):
    # Splits the text into sentences and then puts them in groups of twenty with an overlap of 1
    raw_data = []
    sentences = nltk.sent_tokenize(text)
    n = 2  # group size
    m = 1  # overlap size
    overlapping_sentences = [
        " ".join(sentences[i : i + n]) for i in range(0, len(sentences), n - m)
    ]

    for index, chunk in enumerate(overlapping_sentences):
        raw_data.append(
            DataInformation(
                id=f"{index}",
                last_changed=datetime(2021, 1, 1),
                typ=data_src,
                text=" ".join(chunk),
            )
        )

    return [data for data in raw_data if after < data.last_changed <= before]


def __read_pdf_from_object(pdf_object):
    # Create a BytesIO object from the pdf_object
    pdf_file_object = io.BytesIO(pdf_object)

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(pdf_file_object)

    # Create a PDF document object that stores the document structure.
    document = PDFDocument(parser)

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a buffer for the extracted text
    retstr = io.StringIO()

    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF device object
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    # Create a PDF interpreter object
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Process each page contained in the document.
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)

    text = retstr.getvalue()

    # Close open resources
    retstr.close()
    device.close()

    return text


def __ocr_pdf(pdf_object):
    # Convert the PDF to a series of images
    images = convert_from_bytes(pdf_object)

    # Initialize an empty string to hold the OCR results
    ocr_text = ""

    # Perform OCR on each image
    for i, image in enumerate(images):
        ocr_text += pytesseract.image_to_string(image)

        return ocr_text


if __name__ == "__main__":
    with open("../../Deliverables/sprint-03/planning-documents.pdf", "rb") as f:
        pdf_bytes = f.read()
    print(
        read_pdf(
            pdf_bytes, datetime(2025, 1, 1), datetime(1970, 1, 1), DataSource.CONFLUENCE
        )
    )

    print()

    with open("../../Deliverables/sprint-02/software-architecture.pdf", "rb") as f:
        pdf_bytes = f.read()
    print(
        read_pdf(
            pdf_bytes, datetime(2025, 1, 1), datetime(1970, 1, 1), DataSource.CONFLUENCE
        )
    )
