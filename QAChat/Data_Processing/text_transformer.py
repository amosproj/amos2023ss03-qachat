from QAChat.Data_Processing.deepL_translator import DeepLTranslator
from langchain.text_splitter import NLTKTextSplitter

CHUNK_SIZE = 100


def transform_text_to_chunks(data_information_list):
    new_data_information_list = []

    for data_information in data_information_list:
        # translate text
        translator = DeepLTranslator()
        data_information.text = translator.translate_to(data_information.text, "EN-US")

        # split the text
        text_splitter = NLTKTextSplitter(chunk_size=CHUNK_SIZE)
        chunks = text_splitter.split_text(data_information.text)

        for chunk, index in chunks:
            new_data_information = data_information
            new_data_information.text = chunk
            new_data_information.id = data_information.id + "_" + index
            new_data_information_list.append(data_information)

    return new_data_information_list
