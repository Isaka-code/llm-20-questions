"""keyword_question_mapping.py"""

import re
import math
import copy
import pandas as pd
import numpy as np
from llm20_config import Config
import formulas


class KeywordQuestionMapping:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.keywords_questions_matrix = self.read_csv(
            config.keyword_question_mapping_path
        )
        self.config.logger.log(
            f"self.keywords_questions_matrix.head(): {self.keywords_questions_matrix.head()}"
        )

        self.questions_processed = [
            q.lower().strip()
            for q in self.keywords_questions_matrix.columns.values.tolist()
        ]
        self.config.logger.log(
            f"self.questions_processed[:3]: {self.questions_processed[:3]}"
        )
        self.keywords_processed = [
            str(k).lower().strip()
            for k in self.keywords_questions_matrix.loc[:, "keyword"].values.tolist()
        ]
        self.config.logger.log(
            f"self.keywords_processed[:3]: {self.keywords_processed[:3]}"
        )
        self.top_scoring_keywords: list[str] = []

    def offset_type_to_score(self, offset_type: int) -> float:
        if offset_type == 1:
            return 0.0
        elif offset_type == 2:
            return -0.5
        elif offset_type == 3:
            return -1.0
        elif offset_type == 4:
            return -1.5
        else:
            return -5.0

    def read_csv(self, path: str) -> pd.DataFrame:
        self.config.logger.log(f"path: {path}")
        df = pd.read_csv(path)

        try:
            df.loc[:, "score"] = df.loc[:, "offset_type"].map(self.offset_type_to_score)

            self.config.logger.log("offset to score conversion succeeded.")
        except:
            df.loc[:, "score"] = 0.0
            self.config.logger.log("offset to score conversion failed.")

        self.cols_wo_question = [col for col in df.columns if "?" not in col]
        self.cols_with_question = [col for col in df.columns if "?" in col]
        self.config.logger.log(f"self.cols_wo_question: {self.cols_wo_question}")
        df = pd.concat(
            [
                df.loc[:, self.cols_wo_question],
                df.loc[:, self.cols_with_question].map(self.yes_no_to_int),
            ],
            axis=1,
        )

        assert df.columns[0] == "keyword"
        assert len(self.cols_wo_question) + len(self.cols_with_question) == len(
            df.columns.values.tolist()
        )
        assert (
            self.cols_wo_question + self.cols_with_question
            == df.columns.values.tolist()
        )
        assert df["keyword"].dtype == object or df["keyword"].dtype == str
        return df

    @staticmethod
    def yes_no_to_int(x: str) -> int:
        if x == "yes":
            return 1
        elif x == "no":
            return -1
        else:
            return 0

    def extract_candidates(self, questions: list[str]) -> pd.DataFrame:
        df = self.keywords_questions_matrix.copy()
        asked_questions = self.find_asked_questions(questions, self.cols_with_question)
        df = df.drop(columns=asked_questions)
        df_sorted = df.sort_values(by="score", ascending=False)
        top_score = df_sorted.iloc[0, df_sorted.columns.get_loc("score")]
        semi_top_score = df_sorted.iloc[1, df_sorted.columns.get_loc("score")]
        self.config.logger.log(f"top_score: {top_score}")
        self.config.logger.log(f"semi_top_score: {semi_top_score}")
        score_range = top_score - semi_top_score
        self.config.logger.log(f"score_range: {score_range}")
        df = df[df.loc[:, "score"] >= semi_top_score]

        return df

    def df_to_ratios(self, df: pd.DataFrame) -> list[float]:
        self.config.logger.log(f"df.shape: {df.shape}")
        yes_counts = [
            df.iloc[:, i].value_counts().get(1, 0)
            for i in range(len(self.cols_wo_question), df.shape[1])
        ]
        no_counts = [
            df.iloc[:, i].value_counts().get(-1, 0)
            for i in range(len(self.cols_wo_question), df.shape[1])
        ]
        tie_counts = [
            df.iloc[:, i].value_counts().get(0, 0)
            for i in range(len(self.cols_wo_question), df.shape[1])
        ]

        ratios = [
            formulas.estimate_reduction_expected_value(y, n, t)
            for y, n, t in zip(yes_counts, no_counts, tie_counts)
        ]
        return ratios

    def select(
        self, keywords_questions_matrix_candidates: pd.DataFrame
    ) -> tuple[int, list[float]]:
        _ratios = self.df_to_ratios(keywords_questions_matrix_candidates)
        selected_id = np.argmax(_ratios)
        sorted_df = keywords_questions_matrix_candidates.sort_values(
            by="score", ascending=False
        ).reset_index(drop=True)

        self.config.logger.log(f"sorted_df.head(): {sorted_df.head()}")
        self.config.logger.log(
            f"sorted(_ratios)[::-1][:3]: {sorted(_ratios)[::-1][:3]}"
        )
        self.config.logger.log(f"selected_id: {selected_id}")
        self.config.logger.log(f"_ratios[selected_id]: {_ratios[selected_id]}")

        return selected_id, _ratios

    @staticmethod
    def list_words(head_prompt: str, words: list[str], limit: int) -> str:
        """
        head_promptとwordsリストから、指定された文字数制限内でプロンプトを作成する関数。
        制限を超えた場合は、リストの最後の要素を削除して再試行します。

        :param head_prompt: プロンプトの先頭部分となる文字列
        :param words: プロンプトに含める単語のリスト
        :param limit: プロンプトの文字数制限
        :return: 制限内のプロンプト文字列
        """
        prompt = head_prompt + " " + ", ".join(words) + "?"
        if len(prompt) <= limit:
            return prompt, copy.deepcopy(words)
        else:
            return KeywordQuestionMapping.list_words(
                head_prompt, copy.deepcopy(words)[:-1], limit
            )

    def find_yes_examples(
        self, keywords_questions_matrix_candidates: pd.DataFrame, question: str
    ) -> list[str]:
        yes_examples = (
            keywords_questions_matrix_candidates[
                keywords_questions_matrix_candidates[question] == 1
            ]
            .loc[:, "keyword"]
            .values.tolist()[: self.config.example_num]
        )
        return yes_examples

    @staticmethod
    def is_question_matching_pattern(question: str) -> bool:
        """
        質問文が特定の正規表現パターンにマッチするかどうかを判定します。

        Args:
            question (str): 質問文。

        Returns:
            bool: 質問文がパターンに一致する場合はTrue、そうでない場合はFalse。
        """
        question_pattern = r'keyword.*(?:come before|precede) "([^"]+)" .+ order\?$'
        return bool(re.search(question_pattern, question))

    def count_binary_search_questions(self, questions: list[str]) -> int:
        count = 0
        for question in questions:
            if question == "Is it Agent Alpha?" or self.is_question_matching_pattern(
                question
            ):
                count += 1
        return count

    def update_round_status(self, round_status: str, questions: list[str]) -> str:
        self.config.logger.log(f"round_status: {round_status}")
        binary_search_questions_count = self.count_binary_search_questions(questions)
        self.config.logger.log(
            f"binary_search_questions_count: {binary_search_questions_count}"
        )
        number = round_status.replace("R", "").replace("y", "").replace("n", "")
        yn = round_status.replace("R", "").replace(number, "")
        round_status = (
            "R"
            + str(int(number) - binary_search_questions_count)
            + yn[binary_search_questions_count:]
        )
        self.config.logger.log(f"updated round_status: {round_status}")
        return round_status

    def asker(self, round_status: str, questions) -> str:
        round_status = self.update_round_status(round_status, questions)

        # 1. R初期はエンキューされた質問を選択
        if round_status in self.config.enqued_questions:
            output = self.config.enqued_questions[round_status]
            self.config.logger.log(f"Enqued question selected.: {output}")
            assert output in self.keywords_questions_matrix.columns
            return output

        # 2. 最も情報利得の多い（削減数の期待値が最大）質問を選択
        ## 2.1. top_scoreを取得
        top_score = self.keywords_questions_matrix.loc[:, "score"].max()
        self.config.logger.log(f"top_score: {top_score}")
        self.top_scoring_keywords = self.keywords_questions_matrix[
            self.keywords_questions_matrix.loc[:, "score"] == top_score
        ][: self.config.list_words_num].loc[:, "keyword"]
        output, self.top_scoring_keywords = self.list_words(
            self.config.list_prompt, self.top_scoring_keywords, self.config.limit
        )
        self.L = len(self.top_scoring_keywords)
        self.config.logger.log(f"self.L: {self.L}")
        self.config.logger.log(
            f"self.top_scoring_keywords: \n{self.top_scoring_keywords}"
        )

        ## 2.2. 情報利得が最大の質問を選択
        asked_questions = self.find_asked_questions(questions, self.cols_with_question)
        keywords_questions_matrix_candidates = self.extract_candidates(asked_questions)
        _selected_id, _ratios = self.select(keywords_questions_matrix_candidates)

        self.config.logger.log(
            f"_ratios[_selected_id] > self.L\n{_ratios[_selected_id]} > {self.L}\n{_ratios[_selected_id] > self.L}"
        )
        if _ratios[_selected_id] > self.L:
            # _ratios[_selected_id] > L なら質問を選択
            self.config.logger.log("Semantic question selected.")
            output = keywords_questions_matrix_candidates.columns[
                len(self.cols_wo_question) + _selected_id
            ]  # 質問を選択
            self.config.logger.log(f"Semantic question: {output}")
            yes_examples = self.find_yes_examples(
                keywords_questions_matrix_candidates, output
            )
            if yes_examples:
                self.config.logger.log(f"yes_examples: {yes_examples}")
                output, _ = self.list_words(
                    output + self.config.glue_sentence, yes_examples, self.config.limit
                )
                self.config.logger.log(f"output: \n{output}")
            return output
        else:
            # そうでなければ、上位L個のキーワードをリストアップ
            self.config.logger.log("List question selected.")
            self.config.logger.log(f"List question: {output}")
            return output

    @staticmethod
    def find_asked_question(question: str, columns: list[str]) -> str:
        for col in columns:
            if question.startswith(col):
                return col
        return None

    def find_asked_questions(self, questions: list[str], columns: list[str]) -> str:
        asked_questions = []
        for question in questions:
            asked_question = self.find_asked_question(question, columns)
            if asked_question is not None:
                asked_questions.append(asked_question)
        self.config.logger.log(f"asked_questions: {asked_questions}")
        return asked_questions

    def update_score(self, answer: str, last_question: str) -> None:
        # 1. 最後の質問がList question
        if last_question.startswith(self.config.list_prompt):
            self.config.logger.log("last_question is List question.")
            if answer == "yes":
                # top ceil(L/2)にスコアを+1
                self.config.logger.log("half of top_scoring_keywords +=1")
                K = math.ceil(len(self.top_scoring_keywords) / 2)
                self.top_scoring_keywords = self.top_scoring_keywords[:K]
                self.keywords_questions_matrix.loc[
                    self.keywords_questions_matrix.loc[:, "keyword"].isin(
                        self.top_scoring_keywords
                    ),
                    "score",
                ] += 1
            elif answer == "no":
                # top Kにスコアを-30
                self.config.logger.log("whole of top_scoring_keywords -=30")
                self.keywords_questions_matrix.loc[
                    self.keywords_questions_matrix.loc[:, "keyword"].isin(
                        self.top_scoring_keywords
                    ),
                    "score",
                ] -= 30
            else:
                self.config.logger.log("answer is not yes or no...")

        # 2. 最後の質問がSemantic question
        if last_question in self.keywords_questions_matrix.columns:
            self.config.logger.log("last_question is in columns.")
            if answer == "yes":
                self.keywords_questions_matrix.loc[:, "score"] = (
                    self.keywords_questions_matrix.loc[:, "score"]
                    + self.keywords_questions_matrix.loc[:, last_question].values
                )
            elif answer == "no":
                self.keywords_questions_matrix.loc[:, "score"] = (
                    self.keywords_questions_matrix.loc[:, "score"]
                    - self.keywords_questions_matrix.loc[:, last_question].values
                )
            else:
                self.config.logger.log("answer is not yes or no...")
        self.config.logger.log(
            f'scores[:3]=\n{self.keywords_questions_matrix.loc[:, "score"].sort_values(ascending=False)[:3]}'
        )

    def sample_keyword(self) -> str:
        idx = np.argmax(self.keywords_questions_matrix.score.values)
        return self.keywords_questions_matrix.keyword.values[idx]

    @staticmethod
    def drop_keyword(df: pd.DataFrame, output: str) -> pd.DataFrame:
        return df[df["keyword"] != output]

    def guesser(self) -> str:
        output = self.sample_keyword()
        self.keywords_questions_matrix = self.drop_keyword(
            self.keywords_questions_matrix, output
        )
        return output

    def answerer(self, question: str, keyword: str) -> int | None:
        last_question = question.lower().strip()
        if (
            last_question in self.questions_processed
            and keyword.lower().strip() in self.keywords_processed
        ):
            question_index = self.questions_processed.index(last_question)
            keyword_index = self.keywords_processed.index(keyword.lower().strip())

            output = self.keywords_questions_matrix.iloc[keyword_index, question_index]
            self.config.logger.log(f"output:{output}")
            return output
        else:
            self.config.logger.log("No answer found in Table.")
            return None
