"""test_wiki_data.py"""

import pytest
import pandas as pd
from wiki_data import (
    WikiData,
    select_longest_text_id,
    select_simplest_text_id,
    split_text_and_remove_last,
    process,
    drop_nan_and_reset_index,
)
from unittest.mock import MagicMock


@pytest.fixture
def config():
    class MockConfig:
        def __init__(self):
            self.wikipedia_context_path = "test.csv"
            self.min_context_len = 100
            self.max_context_len = 200
            self.logger = MagicMock()

    return MockConfig()


@pytest.fixture
def wiki_data(config):
    return WikiData(config)


def test_setup(wiki_data, config):
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "keyword": ["test", "example", "sample"],
            "keyword_lower": ["test", "example", "sample"],
            "text": ["This is a test.", "This is an example.", "This is a sample."],
            "title": ["Test", "Example", "Sample"],
            "title_wo_parentheses": ["Test", "Example", "Sample"],
            "text_len": [15, 18, 16],
        }
    )
    pd.read_csv = MagicMock(return_value=df)

    keyword = "test"
    wiki_data.setup(keyword)

    assert wiki_data.context is not None
    assert wiki_data.df is not None


def test_set_context_no_match(wiki_data, config):
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "keyword": ["test", "example", "sample"],
            "keyword_lower": ["test", "example", "sample"],
            "text": ["This is a test.", "This is an example.", "This is a sample."],
            "title": ["Test", "Example", "Sample"],
            "title_wo_parentheses": ["Test", "Example", "Sample"],
            "text_len": [15, 18, 16],
        }
    )
    wiki_data.df = df
    wiki_data.set_context("nomatch")

    assert wiki_data.context == ""


def test_select_longest_text_id():
    df = pd.DataFrame({"id": [1, 2, 3], "text_len": [10, 20, 15]})
    indices = [0, 1, 2]
    assert select_longest_text_id(df, indices) == 2


def test_select_simplest_text_id():
    df = pd.DataFrame(
        {"id": [1, 2, 3], "title": ["Test (example)", "Example", "Sample"]}
    )
    indices = [0, 1, 2]
    assert select_simplest_text_id(df, indices) == 2


def test_split_text_and_remove_last():
    text = "This is a sentence. This is another sentence. This is the last sentence."
    result = split_text_and_remove_last(text)
    assert (
        result
        == "This is a sentence. This is another sentence. \n(The rest of the context is omitted for brevity.)"
    )


def test_process():
    df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "title_wo_parentheses": ["Test", "Example", "Sample"],
            "text": ["This is a test.", "This is an example.", "This is a sample."],
        }
    )
    processed_df = process(df)
    assert "text_len" in processed_df.columns
    assert "keyword" in processed_df.columns
    assert "keyword_lower" in processed_df.columns


def test_drop_nan_and_reset_index():
    df = pd.DataFrame({"id": [1, 2, 3], "keyword": ["test", None, "sample"]})
    cleaned_df = drop_nan_and_reset_index(df, "keyword")
    assert len(cleaned_df) == 2
    assert cleaned_df.index[0] == 0


if __name__ == "__main__":
    pytest.main()
