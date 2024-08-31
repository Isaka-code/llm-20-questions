# %% [code]
"""word_utils.py"""

import string


def normalize(s: str) -> str:
    t = str.maketrans("", "", string.punctuation)
    return s.lower().replace("the", "").replace(" ", "").translate(t)


def compare_words(a, b) -> bool:
    a = normalize(a)
    b = normalize(b)
    if a == b:
        return True
    # don't check for plurals if string is too short
    if len(a) < 3 or len(b) < 3:
        return False
    # accept common plurals
    if a[-1] == "s" and a[:-1] == b:
        return True
    if b[-1] == "s" and a == b[:-1]:
        return True
    if a[-2:] == "es" and a[:-2] == b:
        return True
    if b[-2:] == "es" and a == b[:-2]:
        return True
    return False


def find_word_indices(word: str, words: list[str]) -> list[int]:
    indices = []
    for i, w in enumerate(words):
        if compare_words(w, word):
            indices.append(i)
    return indices
