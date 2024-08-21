"""test_robot.py"""

import time
import pytest
from unittest.mock import MagicMock
from robot import Robot
from dictionary_binary_search import DictionaryBinarySearch
from keyword_question_mapping import KeywordQuestionMapping
from llm20_llm_system import LLMSystem
from wiki_data import WikiData


@pytest.fixture
def mock_config():
    class MockConfig:
        def __init__(self):
            self.start_time = time.perf_counter()
            self.use_dictionary_binary_search_asker = True
            self.use_table_asker = True
            self.use_llm_asker = True
            self.use_dictionary_binary_search_guesser = True
            self.use_table_guesser = True
            self.use_llm_guesser = True
            self.use_protocol_answer = True
            self.use_table_answer = True
            self.use_llm_answer = True
            self.sampling_method = "argmax"
            self.logger = MagicMock()

    return MockConfig()


@pytest.fixture
def mock_obs():
    class MockObs:
        def __init__(self):
            self.questions = ["Is it an animal?"]
            self.answers = ["yes"]
            self.keyword = "dog"

    return MockObs()


@pytest.fixture
def robot(mock_config):
    dictionary_binary_search_instance = MagicMock(DictionaryBinarySearch)
    keyword_question_map = MagicMock(KeywordQuestionMapping)
    llm_system = MagicMock(LLMSystem)
    wiki_data_instance = MagicMock(WikiData)
    return Robot(
        dictionary_binary_search_instance,
        keyword_question_map,
        llm_system,
        wiki_data_instance,
        mock_config,
    )


def test_return_round(robot):
    assert robot.return_round("ask", ["Is it an animal?"]) == 2
    assert robot.return_round("guess", ["Is it an animal?"]) == 1


def test_log_timing_info(robot, mock_config):
    robot.log_timing_info("ask", ["Is it an animal?"], "yes", time.perf_counter())
    mock_config.logger.log.assert_called()


def test_on_guess(robot, mock_obs):
    robot.dictionary_binary_search_instance.guess.return_value = "dog"
    output = robot.on("guess", mock_obs)
    assert output == "dog"


def test_on_answer(robot, mock_obs):
    robot.keyword_question_map.answerer.return_value = 1
    output = robot.on("answer", mock_obs)
    assert output == "yes"


def test_guesser(robot, mock_obs):
    robot.dictionary_binary_search_instance.guess.return_value = "dog"
    output = robot.guesser(mock_obs)
    assert output == "dog"


def test_answerer(robot, mock_obs):
    robot.keyword_question_map.answerer.return_value = 1
    output = robot.answerer(mock_obs)
    assert output == "yes"


if __name__ == "__main__":
    pytest.main()
