import re
import unittest
from unittest.mock import MagicMock

from QAChat.Slack_Bot.qa_agent import QAAgent


def test_run_agent():
    agent = QAAgent()
    # Mock the methods that get called in the start method
    agent.handler.app.message = MagicMock()
    agent.handler.start = MagicMock()

    # Run the method
    agent.start()

    # Check if the methods were called
    agent.handler.app.message.assert_called_once_with(re.compile('.*'))
    agent.handler.start.assert_called_once()


class UnitTest:
    pass


if __name__ == "__main__":
    unittest.main()
