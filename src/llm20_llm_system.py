# %% [code]
"""llm20_llm_system.py"""

import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from llm20_config import AgentConfig, Config
import torch


class LLMSystem:
    def __init__(
        self,
        config: Config,
        asker_config: AgentConfig,
        guesser_config: AgentConfig,
        answerer_config: AgentConfig,
    ):
        self.config = config
        self.asker_config = asker_config
        self.guesser_config = guesser_config
        self.answerer_config = answerer_config
        self.model = None

    def setup(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.config.model_path, torch_dtype=torch.bfloat16, device_map="auto"
        )

        self.id_eot = self.tokenizer.convert_tokens_to_ids(["<|eot_id|>"])[0]

        self.bad_words_ids_ASK = [
            self.tokenizer.encode(word, add_special_tokens=False)
            for word in self.asker_config.initial_bad_words
        ]

        self.bad_words_ids_GUESS = [
            self.tokenizer.encode(word, add_special_tokens=False)
            for word in self.guesser_config.initial_bad_words
        ]

        self.bad_words_ids_ANSWER = [
            self.tokenizer.encode(word, add_special_tokens=False)
            for word in self.answerer_config.initial_bad_words
        ]

    def generate(self, template, temperature, max_new_tokens, bad_words_ids):
        self.config.logger.log(f"template: \n{template}")
        do_sample = temperature > 0
        inp_ids = self.tokenizer(template, return_tensors="pt").to(self.device)
        self.config.logger.log(f"input_ids_len: {inp_ids.input_ids.shape[1]}")
        out_ids = self.model.generate(
            **inp_ids,
            temperature=temperature,
            do_sample=do_sample,
            max_new_tokens=max_new_tokens,
            bad_words_ids=bad_words_ids,
            pad_token_id=self.tokenizer.eos_token_id,
        ).squeeze()
        self.config.logger.log(f"output_ids_len: {out_ids.shape[0]}")
        start_gen = inp_ids.input_ids.shape[1]
        out_ids = out_ids[start_gen:]
        if self.id_eot in out_ids:
            stop = out_ids.tolist().index(self.id_eot)
            out = self.tokenizer.decode(out_ids[:stop])
        else:
            out = self.tokenizer.decode(out_ids)
        return out

    def block_ids(self, output: str, bad_words_ids: list) -> list:
        bad_words_id = self.tokenizer.encode(output, add_special_tokens=False)
        bad_words_id_upper = self.tokenizer.encode(
            output.upper(), add_special_tokens=False
        )
        bad_words_id_lower = self.tokenizer.encode(
            output.lower(), add_special_tokens=False
        )
        bad_words_id_capitalize = self.tokenizer.encode(
            output.capitalize(), add_special_tokens=False
        )
        bad_words_ids.extend(
            [
                bad_words_id,
                bad_words_id_upper,
                bad_words_id_lower,
                bad_words_id_capitalize,
            ]
        )
        return bad_words_ids

    def asker(self, questions: list[str], answers: list[str]) -> str:
        ask_prompt = (
            self.asker_config.system_prompt
            + """your role is to find the word by asking him up to 20 questions, your questions to be valid must have only a 'yes' or 'no' answer.
to help you, here's an example of how it should work assuming that the keyword is Morocco:
examle:
<you: is it a place?
user: yes
you: is it in europe?
user: no
you: is it in africa?
user: yes
you: do most people living there have dark skin?
user: no
user: is it a country name starting by m ?
you: yes
you: is it Morocco?
user: yes.>

the user has chosen the word, ask your first question!
please be short and not verbose, give only one question, no extra word!"""
        )
        chat_template = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{ask_prompt}<|eot_id|>"""
        chat_template += "<|start_header_id|>assistant<|end_header_id|>\n\n"
        if len(questions) >= 1:
            for q, a in zip(questions, answers):
                chat_template += (
                    f"{q}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
                )
                chat_template += (
                    f"{a}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
                )

        output = self.generate(
            chat_template,
            self.asker_config.temperature,
            self.asker_config.max_new_tokens,
            self.bad_words_ids_ASK,
        )
        print(f"output:{output}")

        return output

    def guesser(self, questions: list[str], answers: list[str]) -> str:
        conv = ""
        for q, a in zip(questions, answers):
            conv += f"""Question: {q}\nAnswer: {a}\n"""
        guess_prompt = (
            self.guesser_config.system_prompt
            + f"""so far, the current state of the game is as following:\n{conv}
based on the conversation, can you guess the word, please give only the word, no verbosity around"""
        )
        chat_template = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{guess_prompt}<|eot_id|>"""
        chat_template += "<|start_header_id|>assistant<|end_header_id|>\n\n"

        output = self.generate(
            chat_template,
            self.guesser_config.temperature,
            self.guesser_config.max_new_tokens,
            self.bad_words_ids_GUESS,
        )
        self.config.logger.log(f"output:{output}")

        self.bad_words_ids_GUESS = self.block_ids(output, self.bad_words_ids_GUESS)

        return output

    def get_chat_template_answerer(
        self, keyword: str, context: str, question: str
    ) -> list[dict[str, str]]:
        system_prompt = self.answerer_config.system_prompt.format(
            KEYWORD=keyword,
            QUESTION=question,
        )
        if context:
            self.config.logger.log("context is not NaN")
            system_prompt = (
                self.config.context_prompt.format(CONTEXT=context) + system_prompt
            )
        chat_template = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|>"""
        chat_template += "<|start_header_id|>assistant<|end_header_id|>\n\n"
        return chat_template

    def answerer(
        self,
        keyword: str,
        context: str,
        questions: list[str],
        on_time: float,  # t1
    ) -> str:
        chat_template = self.get_chat_template_answerer(keyword, context, questions[-1])

        outputs, yes_count, no_count = [], 0, 0
        for i in range(self.config.answer_times):
            output = self.generate(
                chat_template,
                self.answerer_config.temperature,
                self.answerer_config.max_new_tokens,
                self.bad_words_ids_ANSWER,
            )
            self.config.logger.log(f"{i}_output:{output}")
            outputs.append(output)
            self.config.logger.log(f"tt_{i}: {time.perf_counter() - on_time}")  # tt_i
            if "yes" == output.lower():
                yes_count += 1
            elif "no" == output.lower():
                no_count += 1
            if max(yes_count, no_count) >= self.config.answer_times_th:
                self.config.logger.log("Threshold is reached!")
                break
            if time.perf_counter() - on_time >= self.config.infer_limit:
                self.config.logger.log("Time is up!")
                break
        self.config.logger.log(f"outputs:{outputs}")
        self.config.logger.log(f"yes_count:{yes_count}")
        self.config.logger.log(f"no_count:{no_count}")
        return "yes" if yes_count > no_count else "no"
