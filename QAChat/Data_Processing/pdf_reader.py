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


def read_pdf(pdf_object):
    # First try to read the PDF with PDFMiner
    text = __read_pdf_from_object(pdf_object)

    # If the result is empty or too short, try OCR
    if len(text.strip()) < 100:
        text = __ocr_pdf(pdf_object)

    return text


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
    print(read_pdf(pdf_bytes))

    print()

    with open("../../Deliverables/sprint-02/software-architecture.pdf", "rb") as f:
        pdf_bytes = f.read()
    print(read_pdf(pdf_bytes))
