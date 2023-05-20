import re
from unittest.mock import patch, MagicMock
from QAChat.Slack_Bot.qa_agent import QAAgent


def test_run_agent():
    with patch('QAChat.QA_Bot.qa_bot.QABot.__init__', return_value=None), \
            patch('slack_bolt.App.__init__', return_value=None), \
            patch('slack_bolt.adapter.socket_mode.SocketModeHandler.__init__', return_value=None):
        agent = QAAgent()

        # Mock the app and attach it to the handler
        agent.handler.app = MagicMock()
        agent.handler.app.message = MagicMock()
        agent.handler.start = MagicMock()

        # Run the method
        agent.start()
        with patch.object(agent.handler, 'start'):
            agent.start()

        # Check if the methods were called
        agent.handler.app.message.assert_called_with(re.compile('.*'))
        agent.handler.start.assert_called()
