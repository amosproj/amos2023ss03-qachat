import re
import unittest
from queue import Queue
from unittest.mock import patch, Mock, MagicMock

from QAChat.Slack_Bot.qa_agent import QAAgent


class TestQAAgent(unittest.TestCase):

    def tearDown(self):
        # Terminate the response_worker_thread
        self.agent.response_queue.put(None)
        self.agent.response_worker.join()

    @patch('slack_bolt.App', autospec=True)
    @patch('slack_sdk.WebClient', autospec=True)
    @patch('slack_bolt.adapter.socket_mode.SocketModeHandler', autospec=True)
    @patch('QAChat.QA_Bot.api_interface.APIInterface', autospec=True)
    @patch('threading.Thread', autospec=True)
    @patch.dict('os.environ', {'SLACK_BOT_TOKEN': 'mock_slack_token', 'SLACK_APP_TOKEN': 'mock_slack_app_token'})
    def setUp(self, mock_thread, mock_socket_mode_handler, mock_web_client, mock_app, mock_api_interface):
        mock_thread.return_value = MagicMock()
        mock_socket_mode_handler.return_value = MagicMock()
        mock_web_client.return_value = MagicMock()
        mock_app.return_value = MagicMock()
        self.mock_thread = mock_thread
        self.mock_socket_mode_handler = mock_socket_mode_handler
        self.mock_web_client = mock_web_client
        self.mock_app = mock_app
        self.mock_api_interface = mock_api_interface

        self.agent = QAAgent(self.mock_app, self.mock_web_client, self.mock_socket_mode_handler)

    def test_init(self):
        self.assertIsInstance(self.agent.response_queue, Queue)
        self.assertEqual(self.agent.say_functions, {})
        self.assertTrue(self.agent.response_worker.is_alive())

    @patch.object(QAAgent, 'receive_question')
    def test_process_question(self, mock_receive_question):
        body = {
            'event': {
                'text': 'Hello',
                'user': 'U1'
            }
        }

        say = MagicMock()

        self.agent.process_question(body, say)
        say.assert_called_with(body['event']['text'])
        self.assertEqual(self.agent.say_functions['U1'], say)


