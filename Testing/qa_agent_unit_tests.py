# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2023 Felix Nützel

import unittest
from queue import Queue
from unittest.mock import patch, MagicMock, Mock, call

from QAChat.Slack_Bot.qa_agent import QAAgent
from QAChat.Slack_Bot.qa_bot_api_interface import QABotAPIInterface


class TestQAAgent(unittest.TestCase):
    def tearDown(self):
        # Disconnect the handler
        self.agent.handler.disconnect()

    @patch("slack_bolt.App", autospec=True)
    @patch("slack_sdk.WebClient", autospec=True)
    @patch("slack_bolt.adapter.socket_mode.SocketModeHandler", autospec=True)
    def setUp(
            self, mock_socket_mode_handler, mock_web_client, mock_app
    ):
        mock_socket_mode_handler.return_value = MagicMock()
        mock_socket_mode_handler.start = MagicMock()

        mock_socket_mode_handler.app = MagicMock()
        mock_socket_mode_handler.connect = MagicMock()
        mock_socket_mode_handler.disconnect = MagicMock()
        mock_socket_mode_handler.client = MagicMock()
        mock_web_client.return_value = MagicMock()
        mock_app.return_value = MagicMock()
        self.mock_socket_mode_handler = mock_socket_mode_handler
        self.mock_web_client = mock_web_client
        self.mock_app = mock_app
        self.mock_api_interface = Mock(spec=QABotAPIInterface)
        self.agent = QAAgent(
            self.mock_app,
            self.mock_web_client,
            self.mock_socket_mode_handler,
            self.mock_api_interface,
        )

    # Tests if process question is called correctly
    def test_process_question(self):
        body = {"event": {"text": "Hello", "user": "U1", "channel": "Test"}}

        say = MagicMock()

        self.mock_api_interface.request.return_value = "How can I help you?"
        self.agent.process_question(body, say)
        self.mock_api_interface.request.assert_called_with("Hello")
        say.assert_has_calls([call("..."), call("How can I help you?")])

    # Tests if the client connects to the Slack Server after starting
    def test_start(self):
        self.agent.start()
        self.assertTrue(self.agent.handler.client.is_connected())
