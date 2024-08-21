"""llm20_config.py"""

import os
from dataclasses import dataclass, field
from logger import Logger, MockLogger

# General parameters
KAGGLE_AGENT_PATH = "/kaggle_simulations/agent/"

# Agent parameters
## Asker
TEMPERATURE_ASK = 0.0
MAX_NEW_TOKENS_ASK = 15
SYS_PROMPT_ASK = """You are a helpful AI assistant, and your are very smart in playing 20 questions game,
the user is going to think of a word, it can be only one of the following 2 categories:
1. a place
2. a thing
So focus your area of search on these options. and give smart questions that narrows down the search space\n"""
BAD_WORDS_ASK = [
    "!",
    "let",
    "Let",
    "was",
    "think",
    "Think",
    "guess",
    "Guess",
    "me",
]
LIST_PROMPT = "Is the keyword one of the following?"  # 36words
GLUE_SENTENCE = '\nExamples of "yes" keywords include the following: \n'  # 54words


## Guesser
TEMPERATURE_GUESS = 0.0
MAX_NEW_TOKENS_GUESS = 15
SYS_PROMPT_GUESS = SYS_PROMPT_ASK
BAD_WORDS_GUESS = [
    ":",
    "Guess",
    "guess",
    "GUESS",
    "I",
    "i",
    "You",
    "you",
    "we",
    "We",
]

## Answerer
TEMPERATURE_ANSWER = 0.0
MAX_NEW_TOKENS_ANSWER = 1

CONTEXT_PROMPT = """Context:
'''
{CONTEXT}
'''
"""

SYS_PROMPT_ANSWER = """Your task is to reply with a single word answer - either 'yes' or 'no'.

I am providing you an entity delimited by <entity> </entity>.

Entity:
<entity>{KEYWORD}</entity>

Next, the user will ask you a question delimited by <question> </question>.

Please use the entity and the question, and formulate a single word 'yes' or 'no' answer that is factually correct. You must use all your knowledge about the entity to formulate the answer.

Never mention the entity in your answer. Do not provide an explanation for your answer, and do not use any other words.
Question:
<question>{QUESTION}</question>"""

BAD_WORDS_ANSWER = [
    "maybe",
    "Maybe",
    "none",
    "None",
    "Invalid",
    "invalid",
    "INVALID",
    "I",
    "can",
    "can't",
    "Can't",
    "CAN'T",
    "I'm",
    "I'll",
    "I've",
]


@dataclass
class Config:
    # timer
    start_time: int
    infer_limit: int = 55  # 55 seconds

    # prompt
    limit: int = 750
    ## list
    list_prompt: str = LIST_PROMPT
    list_words_num: int = 0
    ## Q+list
    glue_sentence: str = GLUE_SENTENCE
    example_num: int = 0

    ## wikipedia-context
    min_context_len: int = 280
    max_context_len: int = 2048
    context_prompt: str = CONTEXT_PROMPT

    # logger
    use_log: bool = False

    # agent
    ## Asker
    ### DictionaryBinarySearch
    use_dictionary_binary_search_asker: bool = True

    ### KeywordQuestionMapping
    use_table_asker: bool = True
    enqued_questions: dict[str, str] = field(
        # You can set the questions you want to ask in advance.
        default_factory=lambda: {
            # "R1": "Would the keyword be considered a natural physical object?",
            # "R2y": "Is it an object that has been in use since ancient times?",
            # "R3yy": "Is it a natural object?",
            # "R3yn": "Is it something that existed before the Industrial Revolution?",
            # "R2n": "Would the keyword be considered a product?",
            # "R3ny": "Is it something that existed before the 20th century?",
            # "R3nn": "Is it used in healthcare?",
        }
    )
    ### LLM
    use_llm_asker: bool = True

    ## Guesser
    ### DictionaryBinarySearch
    use_dictionary_binary_search_guesser: bool = True

    ### KeywordQuestionMapping
    use_table_guesser: bool = True
    guesser_candidate_num_threshold: int = 1

    ### LLM
    use_llm_guesser: bool = False

    ## Answerer
    ### protocol
    use_protocol_answer: bool = True
    ### KeywordQuestionMapping
    use_table_answer: bool = True
    ### LLM
    use_llm_answer: bool = True
    answer_times: int = 1
    answer_times_th: float = 0.5

    def __post_init__(self):
        if os.path.exists(KAGGLE_AGENT_PATH):
            self.model_path = os.path.join(
                KAGGLE_AGENT_PATH, "fixed-llama-3.1-8b-instruct"
            )
            self.keyword_question_mapping_path = os.path.join(
                KAGGLE_AGENT_PATH, "keyword_question_mapping.csv"
            )
            self.binary_search_primary_keywords_path = os.path.join(
                KAGGLE_AGENT_PATH, "binary_search_primary_keywords.csv"
            )
            self.binary_search_supplementary_keywords_path = os.path.join(
                KAGGLE_AGENT_PATH, "binary_search_supplementary_keywords.csv"
            )

            self.wikipedia_context_path = os.path.join(
                KAGGLE_AGENT_PATH, "wikipedia_context.csv"
            )

        else:
            self.model_path = (
                "../input/llama-3-1-8b-instruct-fix-json/fixed-llama-3.1-8b-instruct"
            )
            csv_path_1 = "../working/submission/keyword_question_mapping.csv"
            csv_path_2 = "../input/llm-20-questions-keyword-question-mapping/without_public_keywords_15113_Q_521.csv"
            csv_path_3 = "input/llm-20-questions-keyword-question-mapping/without_public_keywords_15113_Q_521.csv"
            self.keyword_question_mapping_path = (
                csv_path_1
                if os.path.exists(csv_path_1)
                else csv_path_2 if os.path.exists(csv_path_2) else csv_path_3
            )

            self.binary_search_primary_keywords_path = (
                "../working/submission/binary_search_primary_keywords.csv"
            )
            self.binary_search_supplementary_keywords_path = (
                "../working/submission/binary_search_supplementary_keywords.csv"
            )

            self.wikipedia_context_path = "../working/submission/wikipedia_context.csv"

        if self.use_log:
            self.logger = Logger("llm-20-questions")
        else:
            self.logger = MockLogger("llm-20-questions")


@dataclass
class AgentConfig:
    temperature: float
    max_new_tokens: int
    system_prompt: str
    initial_bad_words: list


def make_config(start_time):
    return Config(start_time)


def make_asker_config():
    return AgentConfig(
        TEMPERATURE_ASK, MAX_NEW_TOKENS_ASK, SYS_PROMPT_ASK, BAD_WORDS_ASK
    )


def make_guesser_config():
    return AgentConfig(
        TEMPERATURE_GUESS, MAX_NEW_TOKENS_GUESS, SYS_PROMPT_GUESS, BAD_WORDS_GUESS
    )


def make_answerer_config():
    return AgentConfig(
        TEMPERATURE_ANSWER, MAX_NEW_TOKENS_ANSWER, SYS_PROMPT_ANSWER, BAD_WORDS_ANSWER
    )
