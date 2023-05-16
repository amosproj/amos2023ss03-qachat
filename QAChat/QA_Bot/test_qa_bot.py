from qa_bot import QABot

if __name__ == '__main__':
    bot = QABot()

    print(bot.answer_question("What is the meaning of life?", "test_user"))
