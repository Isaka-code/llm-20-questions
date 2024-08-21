"""robot.py"""

import time
import protocol
from dictionary_binary_search import DictionaryBinarySearch
from keyword_question_mapping import KeywordQuestionMapping
from llm20_llm_system import LLMSystem
from wiki_data import WikiData
from llm20_config import Config


ASK_LENGTH_LIMIT = 750
GUESS_LENGTH_LIMIT = 100


class Robot:
    def __init__(
        self,
        dictionary_binary_search_instance: DictionaryBinarySearch,
        keyword_question_map: KeywordQuestionMapping,
        llm_system: LLMSystem,
        wiki_data_instance: WikiData,
        config: Config,
    ):
        self.dictionary_binary_search_instance = dictionary_binary_search_instance
        self.keyword_question_map = keyword_question_map
        self.llm_system = llm_system
        self.wiki_data_instance = wiki_data_instance
        self.config = config

    @staticmethod
    def return_round(mode: str, questions: list[str]) -> int:
        round_num = len(questions)
        if mode == "ask":
            round_num += 1
        return round_num

    def log_timing_info(
        self,
        mode: str,
        questions: list[str],
        output: str,
        start_time: float,
    ):
        response_time = time.perf_counter()
        self.config.logger.log(f"R{self.return_round(mode, questions)}@{mode}")
        self.config.logger.log(f"t1_from_t0: {start_time - self.config.start_time}")
        self.config.logger.log(
            f"RESPONSE_TIME_from_t0: {response_time - self.config.start_time}"
        )
        self.config.logger.log(f"RESPONSE_TIME - ON_TIME: {response_time - start_time}")
        self.config.logger.log("output: \n" + str(output))
        self.config.logger.log("len(output): " + str(len(output)))

    def on(self, mode, obs):
        self.on_time = time.perf_counter()  # t1
        self.config.logger.log("\n" * 2)
        self.config.logger.log(f"R{self.return_round(mode, obs.questions)}@{mode}")
        self.config.logger.log(f"t1_from_t0: {self.on_time - self.config.start_time}")
        if mode == "ask":
            output = self.asker(obs)[:ASK_LENGTH_LIMIT]

        elif mode == "guess":
            output = self.guesser(obs)[:GUESS_LENGTH_LIMIT]

        elif mode == "answer":
            output = self.answerer(obs).lower()
            if output not in ["yes", "no"]:
                output = "no"

        self.log_timing_info(mode, obs.questions, output, self.on_time)

        return output

    def get_round_status(self, questions: list[str], answers: list[str]) -> str:
        round_status = f"R{self.return_round('ask', questions)}" + "".join(
            [ans[0] for ans in answers]
        )
        return round_status

    def asker(self, obs):
        round_status = self.get_round_status(obs.questions, obs.answers)
        self.config.logger.log(f"round_status: {round_status}")

        # 1. 辞書順バイナリサーチのプロトコルに従って質問を行う
        if self.config.use_dictionary_binary_search_asker:
            self.config.logger.log("1. use_dictionary_binary_search_asker[START]")
            if self.dictionary_binary_search_instance.keywords is None:
                self.dictionary_binary_search_instance.load()
            output = self.dictionary_binary_search_instance.ask(obs.questions)
            if output is not None:
                self.config.logger.log("1. use_dictionary_binary_search_asker[END]")
                return output

        # 2. Keyword Question Mapping
        if self.config.use_table_asker:
            self.config.logger.log("2. use_table_asker[START]")
            output = self.keyword_question_map.asker(round_status, obs.questions)
            if output is not None:
                self.config.logger.log("2. use_table_asker[END]")
                return output

        # 3. LLM
        if self.config.use_llm_asker:
            self.config.logger.log("3. use_llm_asker[START]")
            if self.llm_system.model is None:
                self.config.logger.log("3. use_llm_asker[LOADING]")
                self.llm_system.setup()
            output = self.llm_system.asker(obs.questions, obs.answers)
            self.config.logger.log("3. use_llm_asker[END]")
            return output

        # 4. 全てに該当しない場合は、"no"を返す
        self.config.logger.log("4. else [asker]")
        return "no"

    def guesser(self, obs):
        # 1. 辞書順バイナリサーチのプロトコルに従って推測を行う
        if self.config.use_dictionary_binary_search_guesser:
            self.config.logger.log("1. use_dictionary_binary_search_gueeser[START]")
            output = self.dictionary_binary_search_instance.guess(obs.answers[-1])
            if output is not None:
                self.config.logger.log("1. use_dictionary_binary_search_gueeser[END]")
                return output

        # 2. Keyword Question Mapping
        if self.config.use_table_guesser:
            self.config.logger.log("2. use_table_guesser[START]")

            # 2.1. スコアの更新
            self.keyword_question_map.update_score(obs.answers[-1], obs.questions[-1])

            # 2.2. "score"でソートしたdfを取得しログに記録
            sorted_df = self.keyword_question_map.keywords_questions_matrix.sort_values(
                by="score", ascending=False
            )
            self.config.logger.log(f"sorted_df.head(): \n{sorted_df.head()}")
            self.config.logger.log(
                f"self.keyword_question_map.keywords_questions_matrix.head(): \n{self.keyword_question_map.keywords_questions_matrix.head()}"
            )

            # 2.3. Keyword Question Mappingの推論と予測したキーワードの削除(+LLMならbad_wordsに追加)
            output = self.keyword_question_map.guesser()
            self.config.logger.log("2. use_table_guesser[BLOCK]")
            if self.config.use_llm_guesser and self.llm_system.model is not None:
                self.llm_system.block_ids(
                    output, self.llm_system.bad_words_ids_GUESS
                )  # Keyword Question Mappingでの推論もLLMのブロックに追加
            self.config.logger.log("2. use_table_guesser[END]")
            return output

        # 3. LLM
        if self.config.use_llm_guesser:
            self.config.logger.log("3. use_llm_guesser[START]")
            if self.llm_system.model is None:
                self.config.logger.log("3. use_llm_guesser[LOADING]")
                self.llm_system.setup()
            output = self.llm_system.guesser(obs.questions, obs.answers)
            self.config.logger.log("3. use_llm_guesser[END]")
            return output

        # 4. 全てに該当しない場合は、"no"を返す
        self.config.logger.log("4. else [guesser]")
        return "no"

    def answerer(self, obs):
        # 1. プロトコルに合致するパターンならそれを返す
        if self.config.use_protocol_answer:
            self.config.logger.log("2. use_protocol_answer[START]")
            result = protocol.func(obs.keyword, obs.questions[-1])
            if result is not None:
                self.config.logger.log(f"keword: {obs.keyword}")
                self.config.logger.log(f"question: {obs.questions[-1]}")
                self.config.logger.log(f"result: {result}")
                self.config.logger.log("2. use_protocol_answer[END]")
                return "yes" if result else "no"

        # 2. キーワード、質問ペア行列に存在する場合は、その回答を返す
        if self.config.use_table_answer:
            self.config.logger.log("2. use_table_answer[START]")
            output = self.keyword_question_map.answerer(obs.questions[-1], obs.keyword)
            # 1, -1, 0, Noneがある
            if output == 1:
                self.config.logger.log("2. return yes(1). use_table_answer[END]")
                return "yes"
            elif output == -1:
                self.config.logger.log("2. return no(-1). use_table_answer[END]")
                return "no"
            elif output == 0:
                self.config.logger.log("2. return no(TIE). use_table_answer[END]")
                return "no"

        # 3. それ以外は、LLMを使用して回答を生成する
        if self.config.use_llm_answer:
            self.config.logger.log("3. use_llm_answer[START]")
            if self.llm_system.model is None:
                self.config.logger.log("3. use_llm_answer[LOADING LLM]")
                self.llm_system.setup()
            if self.wiki_data_instance.context is None:
                self.config.logger.log("3. use_llm_answer[LOADING WIKI]")
                try:
                    self.wiki_data_instance.setup(obs.keyword)
                except:
                    self.config.logger.log("3. use_llm_answer[LOADING WIKI ERROR]")
                    self.wiki_data_instance.context = ""
            output = self.llm_system.answerer(
                obs.keyword,
                self.wiki_data_instance.context,
                obs.questions,
                self.on_time,
            )
            self.config.logger.log("3. use_llm_answer[END]")
            return output

        # 4. 全てに該当しない場合は、"no"を返す
        self.config.logger.log("4. else [answer]")
        return "no"
