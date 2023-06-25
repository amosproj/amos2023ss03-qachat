import random
import time
from unittest.mock import Mock, create_autospec

from dotenv import load_dotenv

from QAChat.QA_Bot.qa_bot import QABot
from get_tokens import get_tokens_path

mock = Mock()

questions_en = [
    "Could you summarize the key points of Isaac Asimov's Three Laws of Robotics?",
    "What are some good strategies for teaching mathematics to children?",
    "What is the role of artificial intelligence in climate change mitigation?",
    "Can you explain the concept of quantum entanglement in simple terms?",
    "How can mindfulness techniques improve mental health?",
    "What are the potential uses of blockchain technology beyond cryptocurrencies?",
    "What are some popular machine learning algorithms and their applications?",
    "Can you provide a detailed recipe for homemade pizza?",
    "What are the major contributions of Albert Einstein to physics?",
    "What's the current understanding of the impact of microbiome on human health?",
]


def test_llm_speed():
    qa_bot = QABot(
        embeddings=mock,
        database=mock,
        translator=mock,
    )

    start_time = time.time()
    sum_of_chars = 0

    for question in questions_en:
        output = qa_bot.model.generate([question])
        sum_of_chars += len(output.generations[0][0].text)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(
        f"LLM test time: {elapsed_time} seconds ({sum_of_chars / elapsed_time} chars per second)."
    )


def test_deepl_speed():
    qa_bot = QABot(
        embeddings=mock,
        database=mock,
        model=mock,
    )

    questions = [
        "Could you summarize the key points of Isaac Asimov's Three Laws of Robotics?",
        "What are some good strategies for teaching mathematics to children?",
        "What is the role of artificial intelligence in climate change mitigation?",
        "Can you explain the concept of quantum entanglement in simple terms?",
        "How can mindfulness techniques improve mental health?",
        "Welche potenziellen Anwendungen hat die Blockchain-Technologie außerhalb von Kryptowährungen?",
        "Was sind einige beliebte Machine-Learning-Algorithmen und ihre Anwendungen?",
        "Können Sie ein detailliertes Rezept für hausgemachte Pizza liefern?",
        "Was sind die wichtigsten Beiträge von Albert Einstein zur Physik?",
        "Was ist das aktuelle Verständnis von der Auswirkung des Mikrobioms auf die menschliche Gesundheit?",
    ]

    start_time = time.time()
    for question in questions:
        qa_bot.translator.translate_to(question, "EN-US")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"LLM test time: {elapsed_time} seconds.")


def test_embedding_speed():
    qa_bot = QABot(
        translator=mock,
        database=mock,
        model=mock,
    )

    start_time = time.time()
    for question in questions_en:
        qa_bot.embeddings.embed_query(question)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Embedding test time: {elapsed_time} seconds.")


def test_supabase_speed():
    qa_bot = QABot(
        translator=mock,
        model=mock,
        embeddings=mock,
    )

    start_time = time.time()
    for i in range(10):
        random_embedding = [random.uniform(0, 1) for _ in range(768)]
        qa_bot.database.similarity_search_by_vector(random_embedding, 3)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Supabase reading time: {elapsed_time} seconds.")


def time_this(original_method):
    def side_effect(*args, **kwargs):
        start_time = time.time()
        result = original_method(*args, **kwargs)
        end_time = time.time()
        print(
            f"{original_method.__name__} took {end_time - start_time} seconds to execute"
        )
        return result

    return side_effect


def time_this(original_method):
    def side_effect(*args, **kwargs):
        start_time = time.time()
        result = original_method(*args, **kwargs)
        end_time = time.time()
        print(
            f"{original_method.__name__} took {end_time - start_time} seconds to execute"
        )
        return result

    return side_effect


def test_overall_performance():
    qa_bot_original = QABot()
    translator_mock = create_autospec(qa_bot_original.translator)
    database_mock = create_autospec(qa_bot_original.database)
    llm_mock = create_autospec(qa_bot_original.model)

    translator_mock.translate_to.side_effect = time_this(
        qa_bot_original.translator.translate_to
    )
    database_mock.similarity_search.side_effect = time_this(
        qa_bot_original.database.similarity_search
    )
    llm_mock.generate_prompt.side_effect = time_this(
        qa_bot_original.model.generate_prompt
    )

    qa_bot = QABot(
        translator=translator_mock,
        database=database_mock,
        model=llm_mock,
        embeddings=mock,
    )
    start_time = time.time()
    sum_of_chars = 0

    for question in questions_en:
        output = qa_bot.answer_question(question)
        sum_of_chars += len(output["answer"])
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(
        f"Overall performance: {elapsed_time} seconds ({sum_of_chars / elapsed_time} chars per second)."
    )


if __name__ == "__main__":
    load_dotenv(get_tokens_path())
    test_llm_speed()
    test_deepl_speed()
    test_embedding_speed()
    test_supabase_speed()
    test_overall_performance()
