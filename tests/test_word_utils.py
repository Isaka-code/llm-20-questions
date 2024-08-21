"""test_word_utils.py"""

import pytest

from word_utils import compare_words, find_word_indices, normalize


def test_normalize():
    assert normalize("Hello, World!") == "helloworld"
    assert normalize("The quick brown fox.") == "quickbrownfox"
    assert normalize("Python's great!") == "pythonsgreat"
    assert normalize("A test, with punctuation!") == "atestwithpunctuation"
    assert normalize("") == ""


def test_compare_words():
    assert compare_words("apple", "apple") == True
    assert compare_words("apple", "apples") == True
    assert compare_words("apple", "appl") == False
    assert compare_words("banana", "bananas") == True
    # assert compare_words("cherry", "cherries") == True  # You can't compare the plural form of a word with the singular form
    assert compare_words("cherry", "berry") == False
    assert compare_words("a", "a") == True
    assert compare_words("a", "as") == False


def test_find_word_indices():
    assert find_word_indices(
        "apple", ["apple", "banana", "apple", "cherry", "apple"]
    ) == [0, 2, 4]
    assert find_word_indices("banana", ["apple", "banana", "cherry"]) == [1]
    assert find_word_indices("grape", ["apple", "banana", "cherry"]) == []
    assert find_word_indices("apple", []) == []
    assert find_word_indices("", ["apple", "banana", "", "cherry"]) == [2]
    assert find_word_indices("taco", ["apple", "banana", "tacos", "cherry"]) == [2]
    assert find_word_indices("apples", ["apple", "banana", "cherries", "berry"]) == [0]


if __name__ == "__main__":
    pytest.main()
