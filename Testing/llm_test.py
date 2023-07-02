from unittest.mock import Mock

from QAChat.QA_Bot.qa_bot import QABot

mock = Mock()

if __name__ == "__main__":
    qabot = QABot(
        embeddings=mock,
        database=mock,
        translator=mock,
        repo_id="TheBloke/WizardLM-13B-V1.0-Uncensored-GGML",
        filename="wizardlm-13b-v1.0-uncensored.ggmlv3.q5_0.bin",
    )

    with open("answers.txt", "w") as file:
        questions = [
            "What does Kadi like to do?",
            "Is Hafidz better in playing tennis than Amela?",
            "Who has a red cat?",
            "Who can play computer games?",
        ]

        context = [
            "Emanuel has a red cat",
            "Hafidz has a green car",
            "Jesse has a blue computer",
            "Felix has a dog",
            "Kadi likes to swim",
            "Amela likes to play tennis and plays tennis better than Hafidz",
        ]

        for question in questions:
            answer = qabot.answer_question_with_context(question, context)
            file.write(f"{question};{answer}\n")

        questions = [
            "Do we eat noodles for dinner?",
            "Would it be a good idea for Mom to order the food tomorrow?",
            "How does a good pizza looks like?",
        ]

        context = [
            "Pizza tastes good only with a little tomato sauce. You should also never put too much cheese on the pizza. But do not skimp on the mushrooms.",
            "My mom ordered food yesterday. As usual, the food was not good. She always orders the wrong food. ",
            "We have noodles for lunch. But never for breakfast. Only if there are noodles left over from lunch, there are noodles for dinner.",
        ]

        for question in questions:
            answer = qabot.answer_question_with_context(question, context)
            file.write(f"{question};{answer}\n")

        questions = [
            "What is the mission of QAware?",
            "How does QAware contribute to the success of digital products?",
            "What type of expertise does QAware specialize in?",
        ]

        context = [
            "QAware aims to unite individuals through their shared passion for programming, with a focus on architectural, methodological, and platform expertise.",
            "QAware is dedicated to taking responsibility for developing and operating crucial digital products with enthusiasm and the right solutions.",
            "QAware's specializations include software architecture, development methodologies, and platform proficiency.",
        ]

        for question in questions:
            answer = qabot.answer_question_with_context(question, context)
            file.write(f"{question};{answer}\n")
