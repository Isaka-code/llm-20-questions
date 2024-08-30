# %% [code]
"""llm20_main.py"""

import time
import torch
import llm20_config
from dictionary_binary_search import DictionaryBinarySearch
from keyword_question_mapping import KeywordQuestionMapping
from llm20_llm_system import LLMSystem
from wiki_data import WikiData
from robot import Robot

torch.backends.cuda.enable_mem_efficient_sdp(False)
torch.backends.cuda.enable_flash_sdp(False)
START_TIME = time.perf_counter()
config = llm20_config.make_config(START_TIME)
asker_config = llm20_config.make_asker_config()
guesser_config = llm20_config.make_guesser_config()
answerer_config = llm20_config.make_answerer_config()
dictionary_binary_search_instance = DictionaryBinarySearch(config)
keyword_question_map = KeywordQuestionMapping(config)
llm_system = LLMSystem(
    config,
    asker_config,
    guesser_config,
    answerer_config,
)
wiki_data_instance = WikiData(config)
robot = Robot(
    dictionary_binary_search_instance,
    keyword_question_map,
    llm_system,
    wiki_data_instance,
    config,
)


def agent(obs, cfg):
    try:
        response = robot.on(mode=obs.turnType, obs=obs)
        config.logger.log(f"response: {response}")
    except:
        response = "no"
    return response
