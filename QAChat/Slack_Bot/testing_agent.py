# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Emanuel Erben
# SPDX-FileCopyrightText: 2023 Felix Nützel

import tkinter as tk

from QAChat.Slack_Bot.qa_bot_api_interface import QABotAPIInterface


class TestingAgent:
    """
        This is just an easy Testing Bot for testing reasons and should not be part of the final release.
        Its purpose is to send and receive answers from our system, without having a functioning SlackBot or other.
    """

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.api_interface = QABotAPIInterface()
        master.title("My GUI")

        self.label = tk.Label(master, text="Enter some text:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.button = tk.Button(master, text="Submit", command=self.receive_question)
        self.button.pack()

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

    def receive_question(self):
        input_text = self.entry.get()
        answer = self.api_interface.request(input_text)
        self.result_label.config(text=answer)


if __name__ == "__main__":
    root = tk.Tk()
    gui = TestingAgent(root)
    root.mainloop()
