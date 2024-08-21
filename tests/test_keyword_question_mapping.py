"""test_keyword_question_mapping.py"""

import pytest
import pandas as pd
from keyword_question_mapping import KeywordQuestionMapping
from unittest.mock import MagicMock


@pytest.fixture
def config():
    class MockConfig:
        def __init__(self):
            self.keyword_question_mapping_path = "input/llm-20-questions-keyword-question-mapping/without_public_keywords_15113_Q_521.csv"
            self.list_prompt = "Is the keyword one of the following?"
            self.glue_sentence = (
                "\nExamples of 'yes' keywords include the following: \n"
            )
            self.limit = 100
            self.example_num = 3
            self.enqued_questions = {
                "R1": "Would the keyword be considered a natural physical object?"
            }
            self.logger = MagicMock()

    return MockConfig()


@pytest.fixture
def keyword_question_mapping(config):
    return KeywordQuestionMapping(config)


def test_read_csv(keyword_question_mapping, config):
    df = pd.DataFrame(
        {
            "keyword": ["test", "example", "sample"],
            "offset_type": [1.0, 2.0, 3.0],
            "question1?": ["yes", "no", "yes"],
            "question2?": ["no", "yes", "no"],
        }
    )
    pd.read_csv = MagicMock(return_value=df)

    result_df = keyword_question_mapping.read_csv(config.keyword_question_mapping_path)

    assert "score" in result_df.columns
    assert result_df["score"].tolist() == [0.0, -0.5, -1.0]


def test_update_round_status(keyword_question_mapping, config):
    round_status = "R2y"
    questions = ["Is it Agent Alpha?"]

    updated_round_status = keyword_question_mapping.update_round_status(
        round_status, questions
    )

    assert updated_round_status == "R1"


def test_update_round_status2(keyword_question_mapping, config):
    round_status = "R3yn"
    questions = [
        "Is it Agent Alpha?",
        'Does the keyword (in lowercase) precede "knitting machine" in alphabetical order?',
    ]

    updated_round_status = keyword_question_mapping.update_round_status(
        round_status, questions
    )

    assert updated_round_status == "R1"


def test_select(keyword_question_mapping, config):
    df = pd.DataFrame(
        {
            "keyword": ["test", "example", "sample", "test2", "example2", "sample2"],
            "score": [3.0, 3.0, 1.0, 2.0, 2.0, 1.0],
            "question1?": [1, 1, 0, 1, 0, 0],
            "question2?": [-1, 1, 0, 1, 0, 0],
            "question3?": [1, 1, 0, 1, 0, 0],
        }
    )
    keyword_question_mapping.cols_wo_question = ["keyword", "score"]

    selected_id, _ratios = keyword_question_mapping.select(df)

    assert selected_id == 1
    assert len(_ratios) == 3


def test_answerer(keyword_question_mapping, config):
    keyword_question_mapping.questions_processed = [
        "keyword",
        "question1?",
        "question2?",
    ]
    keyword_question_mapping.keywords_processed = ["test", "example", "sample"]
    df = pd.DataFrame(
        {
            "keyword": ["test", "example", "sample"],
            "question1?": [1, -1, 0],
            "question2?": [-1, 1, 0],
        }
    )
    keyword_question_mapping.keywords_questions_matrix = df

    output = keyword_question_mapping.answerer("question1?", "test")

    assert output == 1


def test_list_words(keyword_question_mapping, config):
    head_prompt = "Is the keyword one of the following:"
    words = ["test", "example", "sample"]
    limit = 50

    prompt, remaining_words = keyword_question_mapping.list_words(
        head_prompt, words, limit
    )

    assert "test" in prompt
    assert len(remaining_words) <= len(words)


if __name__ == "__main__":
    pytest.main()
