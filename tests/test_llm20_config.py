"""test_llm20_config.py"""

import pytest
import os
from llm20_config import (
    Config,
    AgentConfig,
    make_config,
    make_asker_config,
    make_guesser_config,
    make_answerer_config,
)
from logger import Logger, MockLogger


@pytest.fixture
def mock_start_time():
    return 0


@pytest.fixture
def config(mock_start_time):
    return make_config(mock_start_time)


@pytest.fixture
def asker_config():
    return make_asker_config()


@pytest.fixture
def guesser_config():
    return make_guesser_config()


@pytest.fixture
def answerer_config():
    return make_answerer_config()


def test_config_initialization(config):
    assert isinstance(config, Config)
    assert config.start_time == 0
    assert config.infer_limit == 55
    assert config.limit == 750
    assert config.list_prompt == "Is the keyword one of the following?"
    assert (
        config.glue_sentence == '\nExamples of "yes" keywords include the following: \n'
    )
    assert config.min_context_len == 280
    assert config.max_context_len == 2048
    assert config.context_prompt == "Context:\n'''\n{CONTEXT}\n'''\n"
    assert config.use_dictionary_binary_search_asker == True
    assert config.use_table_asker == True
    assert config.use_llm_asker == True
    assert config.use_dictionary_binary_search_guesser == True
    assert config.use_table_guesser == True
    assert config.guesser_candidate_num_threshold == 1
    assert config.use_llm_guesser == False
    assert config.use_protocol_answer == True
    assert config.use_table_answer == True
    assert config.use_llm_answer == True
    assert config.answer_times == 1
    assert config.answer_times_th == 0.5


def test_agent_config_initialization(asker_config, guesser_config, answerer_config):
    assert isinstance(asker_config, AgentConfig)
    assert asker_config.temperature == 0.0
    assert asker_config.max_new_tokens == 15
    assert asker_config.system_prompt.startswith("You are a helpful AI assistant")
    assert "let" in asker_config.initial_bad_words

    assert isinstance(guesser_config, AgentConfig)
    assert guesser_config.temperature == 0.0
    assert guesser_config.max_new_tokens == 15
    assert guesser_config.system_prompt == asker_config.system_prompt
    assert "guess" in guesser_config.initial_bad_words

    assert isinstance(answerer_config, AgentConfig)
    assert answerer_config.temperature == 0.0
    assert answerer_config.max_new_tokens == 1
    assert answerer_config.system_prompt.startswith(
        "Your task is to reply with a single word answer"
    )
    assert "maybe" in answerer_config.initial_bad_words


def test_post_init_config(config):
    assert isinstance(config.logger, (Logger, MockLogger))


def test_paths_config(config):
    if os.path.exists("/kaggle_simulations/agent/"):
        assert config.model_path == os.path.join(
            "/kaggle_simulations/agent/", "fixed-llama-3.1-8b-instruct"
        )
        assert config.keyword_question_mapping_path == os.path.join(
            "/kaggle_simulations/agent/", "keyword_question_mapping.csv"
        )
        assert config.binary_search_primary_keywords_path == os.path.join(
            "/kaggle_simulations/agent/", "binary_search_primary_keywords.csv"
        )
        assert config.binary_search_supplementary_keywords_path == os.path.join(
            "/kaggle_simulations/agent/", "binary_search_supplementary_keywords.csv"
        )
        assert config.wikipedia_context_path == os.path.join(
            "/kaggle_simulations/agent/", "wikipedia_context.csv"
        )
    else:
        assert (
            config.model_path
            == "../input/llama-3-1-8b-instruct-fix-json/fixed-llama-3.1-8b-instruct"
        )
        assert config.keyword_question_mapping_path in [
            "/kaggle/working/submission/keyword_question_mapping.csv",
            "../input/llm-20-questions-keyword-question-mapping/without_public_keywords_15113_Q_521.csv",
            "input/llm-20-questions-keyword-question-mapping/without_public_keywords_15113_Q_521.csv",
        ]
        assert (
            config.binary_search_primary_keywords_path
            == "../working/submission/binary_search_primary_keywords.csv"
        )
        assert (
            config.binary_search_supplementary_keywords_path
            == "../working/submission/binary_search_supplementary_keywords.csv"
        )
        assert (
            config.wikipedia_context_path
            == "../working/submission/wikipedia_context.csv"
        )


if __name__ == "__main__":
    pytest.main()
