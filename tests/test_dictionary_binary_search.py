"""test_dictionary_binary_search.py"""

import pandas as pd
import pytest
from unittest.mock import MagicMock
from dictionary_binary_search import (
    DictionaryBinarySearch,
    remove_non_alphanumeric_and_space,
    remove_non_alphabetic,
)


class MockConfig:
    def __init__(self):
        self.binary_search_primary_keywords_path = "test_primary_keywords.csv"
        self.binary_search_supplementary_keywords_path = (
            "test_supplementary_keywords.csv"
        )
        self.logger = MagicMock()


def create_test_csv(file_path, data):
    df = pd.DataFrame(data, columns=["keyword"])
    df.to_csv(file_path, index=False)


@pytest.fixture
def setup_files(tmp_path):
    test_data = ["apple", "banana", "cherry", "date"]
    supplement_data = ["elderberry", "fig", "grape", "honeydew"]
    main_csv = tmp_path / "test_primary_keywords.csv"
    supplement_csv = tmp_path / "test_supplementary_keywords.csv"
    create_test_csv(main_csv, test_data)
    create_test_csv(supplement_csv, supplement_data)
    return main_csv, supplement_csv


@pytest.fixture
def mock_config(setup_files):
    primary_keywords, supplementary_keywords = setup_files
    config = MockConfig()
    config.binary_search_primary_keywords_path = primary_keywords
    config.binary_search_supplementary_keywords_path = supplementary_keywords
    return config


def test_load(mock_config):
    search = DictionaryBinarySearch(mock_config)
    search.load()
    assert len(search.keywords) == 4
    assert search.keywords == ["apple", "banana", "cherry", "date"]
    mock_config.logger.log.assert_called_with("Loaded 4 keywords")


def test_find_center_word():
    search = DictionaryBinarySearch(MockConfig())
    assert search.find_center_word(["apple", "banana", "cherry", "date"]) == "cherry"
    assert search.find_center_word(["apple", "banana", "cherry"]) == "banana"


def test_ask_search_question(mock_config):
    search = DictionaryBinarySearch(mock_config)
    search.load()
    question = search.ask_search_question()
    assert "Does the keyword (in lowercase) precede" in question
    assert mock_config.logger.log.called


def test_update_dictionary(mock_config):
    search = DictionaryBinarySearch(mock_config)
    search.load()
    search.update_dictionary("yes", "cherry")
    assert search.keywords == ["apple", "banana"]


def test_remove_duplicates(mock_config):
    search = DictionaryBinarySearch(mock_config)
    search.load()
    search.remove_duplicates("banana")
    assert "banana" not in search.keywords


def test_guess(mock_config):
    search = DictionaryBinarySearch(mock_config)
    search.load()
    guess = search.guess("yes")
    assert guess is not None
    assert mock_config.logger.log.called


def test_remove_non_alphanumeric_and_space():
    assert remove_non_alphanumeric_and_space("Hello, World!") == "Hello World"
    assert (
        remove_non_alphanumeric_and_space("Python3.8 is great!") == "Python38 is great"
    )
    assert remove_non_alphanumeric_and_space("123-456-7890") == "1234567890"
    assert (
        remove_non_alphanumeric_and_space("Clean this_text up!") == "Clean thistext up"
    )
    assert (
        remove_non_alphanumeric_and_space("   Spaces should  remain   ")
        == "   Spaces should  remain   "
    )


def test_remove_non_alphabetic():
    assert remove_non_alphabetic(["apple", "banana", "cherry"]) == [
        "apple",
        "banana",
        "cherry",
    ]
    assert remove_non_alphabetic(["apple123", "banana!", "cherry@"]) == [
        "apple123",
        "banana",
        "cherry",
    ]
    assert remove_non_alphabetic(["apple-", "banana–", "cherry_"]) == [
        "apple",
        "banana",
        "cherry",
    ]
    assert remove_non_alphabetic(
        ["apple, banana", "banana - fig", "grape – melon"]
    ) == ["apple banana", "banana   fig", "grape   melon"]


if __name__ == "__main__":
    pytest.main()
