import re
import unittest
from unittest.mock import MagicMock

from QAChat.Slack_Bot.qa_agent import QAAgent

from unittest.mock import patch



@patch('slack_sdk.WebClient')
@patch('slack_bolt.adapter.socket_mode.SocketModeHandler')
def test_run_agent(mocked_socket_mode_handler, mocked_web_client):
    agent = QAAgent()
    # Mock the methods that get called in the start method
    agent.handler.app.message = MagicMock()
    agent.handler.start = MagicMock()

        # Run the method
    agent.start()
    with patch.object(agent.handler, 'start'):
        agent.start()
    # Check if the methods were called
    agent.handler.app.message.assert_called_with(re.compile('.*'))
    agent.handler.start.assert_called()


class UnitTest:
    pass


if __name__ == "__main__":
    unittest.main()
