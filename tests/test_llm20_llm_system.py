"""test_llm20_llm_system.py"""

import pytest
from llm20_llm_system import LLMSystem
from llm20_config import Config, AgentConfig
from unittest.mock import MagicMock, patch


@pytest.fixture
def config():
    return Config(start_time=0)


@pytest.fixture
def asker_config():
    return AgentConfig(
        temperature=0.0,
        max_new_tokens=15,
        system_prompt="You are a helpful AI assistant",
        initial_bad_words=["let", "was", "think"],
    )


@pytest.fixture
def guesser_config():
    return AgentConfig(
        temperature=0.0,
        max_new_tokens=15,
        system_prompt="You are a smart AI assistant",
        initial_bad_words=["guess", "i", "you"],
    )


@pytest.fixture
def answerer_config():
    return AgentConfig(
        temperature=0.0,
        max_new_tokens=1,
        system_prompt="Your task is to reply with a single word answer",
        initial_bad_words=["maybe", "none", "invalid"],
    )


@pytest.fixture
def llm_system(config, asker_config, guesser_config, answerer_config):
    return LLMSystem(config, asker_config, guesser_config, answerer_config)


def test_setup(llm_system):
    with patch(
        "llm20_llm_system.AutoTokenizer.from_pretrained"
    ) as mock_tokenizer, patch(
        "llm20_llm_system.AutoModelForCausalLM.from_pretrained"
    ) as mock_model:
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()
        llm_system.setup()
        assert llm_system.device is not None
        assert llm_system.tokenizer is not None
        assert llm_system.model is not None


if __name__ == "__main__":
    pytest.main()
