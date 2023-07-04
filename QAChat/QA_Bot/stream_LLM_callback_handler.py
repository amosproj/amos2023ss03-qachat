# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Jesse Palarus
import queue

from langchain.callbacks.base import BaseCallbackHandler


class StreamLLMCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.text = ""
        self.q = queue.Queue()

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.q.put(self.text)
