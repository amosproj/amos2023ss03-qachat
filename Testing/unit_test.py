import re
from unittest.mock import MagicMock

from QAChat.Slack_Bot.qa_agent import QAAgent

from unittest.mock import patch


def test_run_agent():
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
