"""dictionary_binary_search.py"""

import re

import pandas as pd
from llm20_config import Config
import word_utils


class DictionaryBinarySearch:
    def __init__(self, config: Config):
        self.config = config
        self.csv_path_list = [
            self.config.binary_search_primary_keywords_path,
            self.config.binary_search_supplementary_keywords_path,
        ]
        self.keywords = None
        self.FIRST_QUESTION = "Is it Agent Alpha?"  # [ref] https://www.kaggle.com/code/lohmaa/llm20-agent-alpha
        self.QUESTION_FORMAT = (
            'Does the keyword (in lowercase) precede "{WORD}" in alphabetical order?'
        )
        self.answerable = False

        self.centered_word_history = ["zzzzzzzzzzz"]  # last word in the dictionary
        self.answer_history = []
        self.guess_history = []

    def replay(self):
        if len(self.centered_word_history) == len(self.answer_history):
            for centered_word, answer in zip(
                self.centered_word_history, self.answer_history
            ):
                self.update_dictionary(answer, centered_word)
                self.config.logger.log(f"Remaining keywords: {len(self.keywords)}")

            for guess_word in self.guess_history:
                self.remove_duplicates(guess_word)

    def load(self):
        if self.csv_path_list:
            csv_path = self.csv_path_list.pop(0)
            self.keywords = (
                pd.read_csv(csv_path, dtype={"keyword": str})
                .sort_values("keyword")
                .loc[:, "keyword"]
                .values.tolist()
            )
            self.keywords = remove_non_alphabetic(self.keywords)
            self.keywords = sorted([k.lower() for k in self.keywords])
            self.replay()
        else:
            self.keywords = []
        self.config.logger.log(f"Loaded {len(self.keywords)} keywords")

    def ask_first_question(self) -> str:
        self.config.logger.log("Asking the first question")
        return self.FIRST_QUESTION

    @staticmethod
    def find_center_word(words: list[str]) -> str:
        return words[len(words) // 2]

    def ask_search_question(self) -> str | None:
        if self.keywords is None or len(self.keywords) == 0:
            self.config.logger.log("Keywords is None[DictionaryBinarySearch]")
            return None
        centered_word = self.find_center_word(self.keywords)
        self.centered_word_history.append(centered_word)
        self.config.logger.log(f"Centered word: {centered_word}")
        self.config.logger.log("Asking a search question")
        return self.QUESTION_FORMAT.format(WORD=centered_word)

    def ask(self, questions: list[str]) -> str | None:
        if len(questions) == 0:
            return self.ask_first_question()
        return self.ask_search_question()

    def update_dictionary(self, last_answer: str, centered_word: str):
        if last_answer == "yes":
            self.keywords = [k for k in self.keywords if k < centered_word]
        else:
            self.keywords = [k for k in self.keywords if k >= centered_word]

        if len(self.keywords) == 0:
            self.config.logger.log("No keywords left.[update_dictionary]")
            self.load()

    def remove_duplicates(self, guess_word: str) -> None:
        self.keywords = [
            k for k in self.keywords if not word_utils.compare_words(k, guess_word)
        ]

    def guess(self, last_answer: str) -> str | None:
        self.answer_history.append(last_answer)
        # Judge if the agent is answerable
        if not self.answerable and last_answer == "no":
            self.keywords = []
            self.config.logger.log(
                "Answer agent is not answerable. Keywords will be empty."
            )
        else:
            if self.keywords:
                self.answerable = True
                self.config.logger.log("Answer agent is answerable.")

        if self.answerable:
            self.update_dictionary(last_answer, self.centered_word_history[-1])
            self.config.logger.log(f"Remaining keywords: {len(self.keywords)}")
            if self.keywords:
                guess_word = self.keywords.pop(0)
                self.config.logger.log(f"Guessed word: {guess_word}")
                self.guess_history.append(guess_word)
                self.remove_duplicates(guess_word)

                if len(self.keywords) == 0:
                    self.config.logger.log("No keywords left.[guess]")
                    self.load()

                return guess_word

        return None


def contains_non_alphabetic(keyword: str) -> bool:
    non_alphabetic_pattern = r"[^a-zA-Z]"
    return bool(re.search(non_alphabetic_pattern, str(keyword)))


def remove_non_alphanumeric_and_space(text: str) -> str:
    pattern = re.compile(r"[^a-zA-Z0-9 ]")
    cleaned_text = pattern.sub("", text)
    return cleaned_text


def remove_non_alphabetic(keywords: list[str]) -> list[str]:
    cleaned_keywords = []
    for keyword in keywords:
        keyword = (
            str(keyword)
            .replace(",", "")
            .replace("-", " ")
            .replace("–", " ")
            .lower()
            .strip()
        )
        cleaned_keyword = remove_non_alphanumeric_and_space(keyword)
        cleaned_keywords.append(cleaned_keyword)
    return cleaned_keywords
