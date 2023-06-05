# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Felix Nützel

import unittest
from queue import Queue
from unittest.mock import patch, MagicMock

from QAChat.Slack_Bot.qa_agent import QAAgent


class TestQAAgent(unittest.TestCase):
    def tearDown(self):
        # Terminate the response_worker_thread
        self.agent.response_queue.put(None)
        self.agent.response_worker.join()
        # Disconnect the handler
        self.agent.handler.disconnect()

    @patch("slack_bolt.App", autospec=True)
    @patch("slack_sdk.WebClient", autospec=True)
    @patch("slack_bolt.adapter.socket_mode.SocketModeHandler", autospec=True)
    @patch("QAChat.QA_Bot.api_interface.APIInterface", autospec=True)
    def setUp(
        self, mock_socket_mode_handler, mock_web_client, mock_app, mock_api_interface
    ):
        mock_socket_mode_handler.return_value = MagicMock()
        mock_socket_mode_handler.start = MagicMock()

        mock_socket_mode_handler.app = MagicMock()
        mock_socket_mode_handler.connect = MagicMock()
        mock_socket_mode_handler.disconnect = MagicMock()
        mock_socket_mode_handler.client = MagicMock()
        mock_web_client.return_value = MagicMock()
        mock_app.return_value = MagicMock()
        mock_api_interface.app = MagicMock()
        self.mock_socket_mode_handler = mock_socket_mode_handler
        self.mock_web_client = mock_web_client
        self.mock_app = mock_app
        self.mock_api_interface = mock_api_interface
        self.agent = QAAgent(
            self.mock_app, self.mock_web_client, self.mock_socket_mode_handler
        )

    def test_init(self):
        self.assertIsInstance(self.agent.response_queue, Queue)
        self.assertEqual(self.agent.say_functions, {})
        self.assertTrue(self.agent.response_worker.is_alive())

    # Tests if process question is called correctly
    @patch.object(QAAgent, "receive_question")
    def test_process_question(self, mock_receive_question):
        body = {"event": {"text": "Hello", "user": "U1"}}

        say = MagicMock()

        self.agent.process_question(body, say)
        say.assert_called_with(body["event"]["text"])
        self.assertEqual(self.agent.say_functions["U1"], say)

    # Tests if the answer is saved in the queue properly
    def test_receive_answer(self):
        answer = "test answer"
        user_id = 31
        self.agent.receive_answer(answer, user_id)
        self.assertEqual(self.agent.response_queue.get(), (user_id, answer))

    # Tests if the client connects to the Slack Server after starting
    def test_start(self):
        self.agent.start()
        self.assertTrue(self.agent.handler.client.is_connected())
