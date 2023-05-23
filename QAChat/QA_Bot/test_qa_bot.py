from qa_bot import QABot

if __name__ == '__main__':
    bot = QABot()

    print(bot.answer_question("Wie verbinde ich mich mit den SSH Server?", "test_user"))
    print(bot.answer_question("Gibt es im Office eine Kantine?", "test_user"))
    print(bot.answer_question("Von wann bis wann sind die Arbeiteiszeiten bei QAWare?", "test_user"))
