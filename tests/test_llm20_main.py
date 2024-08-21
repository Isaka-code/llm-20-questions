"""test_llm20_main.py"""

import pytest
from unittest.mock import MagicMock, patch
import llm20_main
from llm20_main import agent, Robot
from llm20_config import Config
from dictionary_binary_search import DictionaryBinarySearch
from keyword_question_mapping import KeywordQuestionMapping
from llm20_llm_system import LLMSystem
from wiki_data import WikiData


@pytest.fixture
def mock_config():
    config = MagicMock(Config)
    config.logger = MagicMock()
    return config


@pytest.fixture
def mock_obs():
    class MockObs:
        def __init__(self):
            self.turnType = "ask"
            self.questions = ["Is it an animal?"]
            self.answers = ["yes"]
            self.keyword = "dog"

    return MockObs()


def test_agent(mock_config, mock_obs):
    dictionary_binary_search_instance = MagicMock(DictionaryBinarySearch)
    keyword_question_map = MagicMock(KeywordQuestionMapping)
    llm_system = MagicMock(LLMSystem)
    wiki_data_instance = MagicMock(WikiData)
    robot = Robot(
        dictionary_binary_search_instance,
        keyword_question_map,
        llm_system,
        wiki_data_instance,
        mock_config,
    )
    llm20_main.robot = robot

    with patch.object(robot, "on", return_value="Is it a mammal?"):
        response = agent(mock_obs, mock_config)
        assert response == "Is it a mammal?"

    with patch.object(robot, "on", side_effect=Exception("Test Error")):
        response = agent(mock_obs, mock_config)
        assert response == "no"


if __name__ == "__main__":
    pytest.main()
