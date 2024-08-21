import pytest
from protocol import (
    func,
    func0,
    func1,
    func2,
    func3,
    func4,
    func5,
    func6,
    func7,
    func8,
    func9,
    func10,
    func11,
    func12,
    func13,
    func14,
    func15,
    func16,
    func17,
    func18,
    func19,
    func20,
    func21,
    func22,
)


def test_func0():
    assert (
        func0(
            "Kaggle",
            "Is it Agent Alpha?",
        )
        is True
    )

    assert (
        func0(
            "Kaggle",
            "Is it Beta Bravo?",
        )
        is None
    )

    assert (
        func0(
            "Kaggle",
            "Are we playing 20 questions?",
        )
        is True
    )


def test_func1():
    assert (
        func1(
            "apple",
            'Does the keyword (in lowercase) come before "banana" in alphabetical order?',
        )
        is True
    )
    assert (
        func1(
            "banana",
            'Does the keyword (in lowercase) come before "apple" in alphabetical order?',
        )
        is False
    )
    assert (
        func1(
            "apple",
            'Does the keyword (in lowercase) precede "banana" in alphabetical order?',
        )
        is True
    )
    assert (
        func1(
            "banana",
            'Does the keyword (in lowercase) precede "apple" in alphabetical order?',
        )
        is False
    )
    assert (
        func1(
            "123",
            'Does the keyword (in lowercase) come before "apple" in alphabetical order?',
        )
        is True
    )
    assert func1("apple", "Invalid question format") is None

    assert (
        func1("apple", 'Does the keyword come before "banana" in alphabetical order?')
        == True
    )
    assert (
        func1("banana", "Does the keyword come before 'cherry' in alphabetical order?")
        == True
    )
    assert (
        func1("cherry", "Does the keyword come before grape in alphabetical order?")
        == True
    )
    assert (
        func1("date", 'Does the keyword come before "apple" in alphabetical order?')
        == False
    )
    assert (
        func1(
            "elderberry", "Does the keyword come before 'date' in alphabetical order?"
        )
        == False
    )
    assert (
        func1("fig", "Does the keyword come before apple in alphabetical order?")
        == False
    )
    assert func1("apple", "Is the keyword a fruit?") == None
    assert (
        func1("apple1", 'Does the keyword come before "banana" in alphabetical order?')
        == True
    )
    assert (
        func1("1apple", 'Does the keyword come before "apple" in alphabetical order?')
        == True
    )
    assert (
        func1("apple!", 'Does the keyword come before "banana" in alphabetical order?')
        == True
    )


def test_func2():
    assert func2("apple", 'Does the keyword begin with the letter "a"?') is True
    assert func2("apple", 'Does the keyword begins with the letter "a"?') is True
    assert func2("banana", 'Does the keyword begin with the letter "a"?') is False
    assert func2("banana", 'Does the keyword begins with the letter "a"?') is False
    assert func2("123", 'Does the keyword begin with the letter "1"?') is True
    assert func2("3D printer", 'Does the keyword begin with the letter "3"?') is True
    assert func2("3D printer", 'Does the keyword begins with the letter "3"?') is True
    assert func2("apple", "Invalid question format") is None
    assert func2("apple", 'Does the keyword begin with the letter "@"?') is None
    assert func2("3D printer", 'Does the keyword begin with the letter "d"?') is False
    assert func2("apple", 'Does the keyword begin with the letter "a"?') == True
    assert func2("banana", "Does the keyword begin with the letter 'b'?") == True
    assert func2("cherry", "Does the keyword begin with the letter c?") == True
    assert func2("date", 'Does the keyword begin with the letter "d"?') == True
    assert func2("elderberry", "Does the keyword begin with the letter 'e'?") == True
    assert func2("fig", "Does the keyword begin with the letter f?") == True
    assert func2("grape", 'Does the keyword begin with the letter "h"?') == False
    assert func2("apple", "Is the keyword a fruit?") == None
    assert func2("apple1", 'Does the keyword begin with the letter "a"?') == True
    assert func2("1apple", 'Does the keyword begin with the letter "1"?') == True
    assert func2("apple!", 'Does the keyword begin with the letter "a"?') == None


def test_func3():
    assert (
        func3("apple", "Does the keyword start with one of the letters 'a', 'b', 'c'?")
        is True
    )
    assert (
        func3("banana", "Does the keyword start with one of the letters 'd', 'e', 'f'?")
        is False
    )
    assert func3("carrot", "Does the keyword start with the letter 'c'?") is True
    assert (
        func3("123", "Does the keyword start with one of the letters 'a', 'b', 'c'?")
        is False
    )
    assert func3("apple", "Invalid question format") is None
    assert (
        func3("3D printer", "Does the keyword start with one of the letters '3', 'D'?")
        is True
    )
    assert func3("7eleven", "Does the keyword start with the letter '7'?") is True
    assert func3("zero", "Does the keyword start with the letter 'z'?") is True
    assert (
        func3(
            "7eleven", "Does the keyword start with one of the letters 'a', 'b', 'c'?"
        )
        is False
    )
    # 正常ケース
    assert (
        func3(
            "purse",
            "Does the keyword start with one of the letters 'S', 'V', 'M', 'W', 'X' or 'R'?",
        )
        == False
    )
    assert (
        func3(
            "purse",
            "Does the keyword start with one of the letters P, V, M, W, X or R?",
        )
        == True
    )
    assert (
        func3(
            "purse",
            'Does the keyword start with one of the letters "S", "V", "M", "W", "X" or "R"?',
        )
        == False
    )
    assert (
        func3(
            "purse",
            "Does the keyword start with one of the letters 'P', 'V', 'M', 'W', 'X' or 'R'?",
        )
        == True
    )
    assert (
        func3("purse", "Does the keyword start with one of the letters 'P' or 'R'?")
        == True
    )
    assert func3("purse", "Does the keyword start with the letter 'P'?") == True
    assert func3("purse", "Does the keyword start with the letter P?") == True
    assert func3("purse", 'Does the keyword start with the letter "P"?') == True
    assert func3("purse", "Does the keyword start with the letter 'R'?") == False
    # 無効な質問形式
    assert (
        func3(
            "purse",
            "Does the keyword start with one of the letters S, V, M, W, X or R?",
        )
        == False
    )
    assert func3("purse", "Is the keyword starting with the letter 'P'?") == None
    # 無効なキーワード
    assert func3("purse@", "Does the keyword start with the letter 'P'?") == True


def test_func4():
    assert (
        func4("apple", "Is the keyword one of the following? apple, banana, carrot?")
        is True
    )
    assert (
        func4("banana", "Is the keyword one of the following? apple, carrot, orange?")
        is False
    )
    assert (
        func4("123", "Is the keyword one of the following? apple, banana, carrot?")
        is None
    )
    assert (
        func4("banana", "is the keyword one of the following? apple, carrot, orange?")
        is False
    )

    assert func4("apple", "Invalid question format") is None


def test_func5():
    assert (
        func5(
            "apple",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter 'a'?",
        )
        is True
    )
    assert (
        func5(
            "banana",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter 'z'?",
        )
        is False
    )
    assert (
        func5(
            "123",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter 'a'?",
        )
        is False
    )
    assert func5("apple", "Invalid question format") is None

    assert (
        func5(
            "example",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter 'e'?",
        )
        == True
    )
    assert (
        func5(
            "example",
            'Considering every letter in the name of the keyword, does the name of the keyword include the letter "e"?',
        )
        == True
    )
    assert (
        func5(
            "example",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter e?",
        )
        == True
    )
    assert (
        func5(
            "example",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter 'z'?",
        )
        == False
    )
    assert (
        func5(
            "example",
            'Considering every letter in the name of the keyword, does the name of the keyword include the letter "z"?',
        )
        == False
    )
    assert (
        func5(
            "example",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter z?",
        )
        == False
    )
    assert (
        func5(
            "example123",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter '1'?",
        )
        == True
    )
    assert (
        func5(
            "example123",
            'Considering every letter in the name of the keyword, does the name of the keyword include the letter "2"?',
        )
        == True
    )
    assert (
        func5(
            "example123",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter 3?",
        )
        == True
    )
    assert (
        func5(
            "example",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter 'E'?",
        )
        == True
    )
    assert (
        func5(
            "example",
            'Considering every letter in the name of the keyword, does the name of the keyword include the letter "E"?',
        )
        == True
    )
    assert (
        func5(
            "example",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter E?",
        )
        == True
    )
    assert func5("example", "Is the keyword a fruit?") == None


def test_func6():
    assert func6("Kaggle", "Is it Agent Alpha?") is True
    assert func6("Kaggle", "Is it Beta Bravo?") is None
    assert func6("Kaggle", "Is it Gamma Delta?") is None
    assert func6("Kaggle", "Is it Agent Bravo?") is None
    assert func6("Kaggle", "Is it Alpha Gamma?") is None
    assert func6("Kaggle", "Invalid question format") is None


def test_func7():
    assert (
        func7(
            "Iron bar",
            "Is any of the letters ['l','w'] inside the spelling of the keyword?",
        )
        is False
    )
    assert (
        func7(
            "Iron bar",
            "Is any of the letters ['o','r'] inside the spelling of the keyword?",
        )
        is True
    )
    assert (
        func7(
            "12345",
            "Is any of the letters ['1','9'] inside the spelling of the keyword?",
        )
        is True
    )
    assert (
        func7(
            "abcdef",
            "Is any of the letters ['x','y','z'] inside the spelling of the keyword?",
        )
        is False
    )

    assert (
        func7(
            "abcdef",
            "is any of the letters ['x','y','z'] inside the spelling of the keyword?",
        )
        is False
    )


def test_func8():
    assert (
        func8(
            "Iron bar",
            "Is the keyword one of the following words: 'apple', 'banana', 'carrot' ?",
        )
        is False
    )
    assert (
        func8(
            "apple",
            "Is the keyword one of the following words: 'apple', 'banana', 'carrot' ?",
        )
        is True
    )
    assert (
        func8("123", "Is the keyword one of the following words: '123', '456', '789' ?")
        is True
    )
    assert (
        func8("xyz", "Is the keyword one of the following words: 'abc', 'def', 'ghi' ?")
        is False
    )

    assert (
        func8("xyz", "is the keyword one of the following words: 'abc', 'def', 'ghi' ?")
        is False
    )


def test_func9():
    assert (
        func9("Apple", "Does the word start with the letter 'A' , 'B', or 'C'?") == True
    )
    assert (
        func9("banana", "Does the word start with the letter 'A' , 'B', or 'C'?")
        == True
    )
    assert (
        func9("cherry", "Does the word start with the letter 'a' , 'b', 'c'?") == True
    )
    assert func9("date", "Does the word start with the letter 'd' , 'e', 'f'?") == True
    assert (
        func9("elephant", "Does the keyword start with the letter 'g' , 'h', 'i'?")
        == False
    )
    assert func9("grape", "Does the keyword start with the letter g , h, or i?") == True
    assert func9("kiwi", "Does the keyword start with the letter 'k'?") == True
    assert func9("lemon", "Does the word start with the letter 'l'?") == True
    assert func9("mango", "Does the word start with the letter m , n, or o?") == True
    assert func9("orange", "Does the word start with the letter p , q, or r?") == False
    assert func9("apple", "Is the first letter 'a'?") == None
    assert func9("apple", "Does the word start with the number '1'?") == None
    assert (
        func9("grapefruit", 'Does the word start with the letter "g" , "h", or "i"?')
        == True
    )
    assert func9("nut", "Does the keyword start with the letter 'n',?") == True
    assert func9("nut", "Does the keyword start with the letter n,?") == True


def test_func10():
    assert func10("apple", 'Does the keyword end with the letter "e"?') is True
    assert func10("banana", 'Does the keyword end with the letter "n"?') is False
    assert func10("apple", 'Does the keyword end with the letter "a"?') is False
    assert func10("banana", 'Does the keyword end with the letter "a"?') is True
    assert func10("123", 'Does the keyword end with the letter "3"?') is True
    assert func10("apple", "Invalid question format") is None
    assert func10("apple", 'Does the keyword end with the letter "@")?') is None
    assert func10("apple", "Does the keyword end with the letter e?") is True
    assert func10("banana", "Does the keyword end with the letter n?") is False
    assert func10("apple", "Does the keyword end with the letter a?") is False
    assert func10("banana", "Does the keyword end with the letter a?") is True
    assert func10("banana", "Does the keyword end with the letter A?") is True
    assert func10("123", "Does the keyword end with the letter 3?") is True
    assert func10("apple", "Does the keyword end with the letter @)?") is None
    assert func10("banana", "Does the keyword end with the letter 'n'?") is False
    assert func10("apple", "Does the keyword end with the letter 'a'?") is False
    assert func10("banana", "Does the keyword end with the letter 'a'?") is True
    assert func10("123", "Does the keyword end with the letter '3'?") is True
    assert func10("apple", "Does the keyword end with the letter '@')?") is None
    assert func10("HELLO", 'Does the keyword end with the letter "O"?') is True
    assert func10("WORLD", 'Does the keyword end with the letter "D"?') is True
    assert func10("HELLO", "Does the keyword end with the letter O?") is True
    assert func10("WORLD", "Does the keyword end with the letter D?") is True
    assert func10("HELLO", 'Does the keyword end with the letter "o"?') is True
    assert func10("WORLD", 'Does the keyword end with the letter "d"?') is True
    assert func10("HELLO", "Does the keyword end with the letter o?") is True
    assert func10("WORLD", "Does the keyword end with the letter d?") is True
    assert func10("hello", "Does the keyword end with the letter o?") is True
    assert func10("world", "Does the keyword end with the letter d?") is True


def test_func11():
    assert func11("apple", 'Does the keyword contain the letter "a"?') is True
    assert func11("banana", 'Does the keyword contain the letter "z"?') is False
    assert func11("apple", 'Does the keyword contain the letter "p"?') is True
    assert func11("banana", 'Does the keyword contain the letter "n"?') is True
    assert func11("123", 'Does the keyword contain the letter "3"?') is True
    assert func11("apple", "Invalid question format") is None
    assert func11("apple", 'Does the keyword contain the letter "@")?') is None
    assert func11("HELLO", 'Does the keyword contain the letter "O"?') is True
    assert func11("WORLD", 'Does the keyword contain the letter "D"?') is True
    assert func11("HELLO", "Does the keyword contain the letter O?") is True
    assert func11("WORLD", "Does the keyword contain the letter D?") is True
    assert func11("HELLO", 'Does the keyword contain the letter "o"?') is True
    assert func11("WORLD", 'Does the keyword contain the letter "d"?') is True
    assert func11("HELLO", "Does the keyword contain the letter o?") is True
    assert func11("WORLD", "Does the keyword contain the letter d?") is True
    assert func11("hello", "Does the keyword contain the letter o?") is True
    assert func11("world", "Does the keyword contain the letter d?") is True
    assert func11("kaggle", "Does the keyword contain the letter g?") is True
    assert func11("python", "Does the keyword contain the letter y?") is True
    assert func11("kaggle", "Does the keyword contain the letter K?") is True
    assert func11("python", "Does the keyword contain the letter P?") is True


def test_func12():
    assert func12("apple", 'Does the keyword include the letter "a"?') is True
    assert func12("apple", 'Does the keyword include the letter "p"?') is True
    assert func12("banana", 'Does the keyword include the letter "z"?') is False
    assert func12("wind vane", 'Does the keyword include the letter "a"?') is True
    assert func12("apple", 'Does the keyword contain the letter "a"?') is True
    assert func12("apple", 'Does the keyword contain the letter "p"?') is True
    assert func12("banana", 'Does the keyword contain the letter "z"?') is False
    assert func12("wind vane", 'Does the keyword contain the letter "a"?') is True
    assert func12("apple", 'Is the letter "a" in the keyword?') is True
    assert func12("apple", 'Is the letter "p" in the keyword?') is True
    assert func12("banana", 'Is the letter "z" in the keyword?') is False
    assert func12("wind vane", 'Is the letter "a" in the keyword?') is True
    assert func12("apple", "Invalid question format") is None
    assert func12("apple", 'Does the keyword include the letter "@"?') is None


def test_func13():
    assert (
        func13(
            "apple",
            "str(obs.keyword)[0].lower() in list('abcdefghijklm') #Is the first letter of the keyword any of the following: ['a','b','c','d','e','f','g','h','i','j','k','l','m'] ?",
        )
        == True
    )
    assert (
        func13(
            "banana",
            "str(obs.keyword)[0].lower() in list('abcdef') #Is the first letter of the keyword any of the following: ['a','b','c','d','e','f']?",
        )
        == True
    )
    assert (
        func13(
            "cherry",
            "str(obs.keyword)[0].lower() in list('ghij') #Is the first letter of the keyword any of the following: ['g','h','i','j'] ?",
        )
        == False
    )
    assert (
        func13(
            "date",
            "str(obs.keyword)[0].lower() in list('nopqrs') #Is the first letter of the keyword any of the following: ['n','o','p','q','r','s']?",
        )
        == False
    )
    assert (
        func13(
            "elderberry",
            "str(obs.keyword)[0].lower() in list('nop') #Is the first letter of the keyword any of the following: ['n','o','p'] ?",
        )
        == False
    )
    assert (
        func13(
            "fig",
            "str(obs.keyword)[0].lower() in list('nopqrs') #Is the first letter of the keyword any of the following: ['n','o','p','q','r','s']?",
        )
        == False
    )
    assert (
        func13(
            "grape",
            "str(obs.keyword)[0].lower() in list('abcdef') #Is the first letter of the keyword any of the following: ['a','b','c','d','e','f']?",
        )
        == False
    )
    assert (
        func13(
            "apple",
            "str(obs.keyword)[0].lower() in list('tuvw') #Is the first letter of the keyword any of the following: ['t','u','v','w'] ?",
        )
        == False
    )
    assert (
        func13(
            "apple!",
            "str(obs.keyword)[0].lower() in list('abcdef') #Is the first letter of the keyword any of the following: ['a','b','c','d','e','f']?",
        )
        == True
    )


def test_func14():
    assert func14("example", 'Does the keyword contain an "m"?') == True
    assert func14("example", "Does the keyword contain an 'm'?") == True
    assert func14("example", "Does the keyword contain an m?") == True
    assert func14("example", 'Does the keyword contain an "z"?') == False
    assert func14("example", "Does the keyword contain an 'z'?") == False
    assert func14("example", "Does the keyword contain an z?") == False
    assert func14("example123", 'Does the keyword contain an "1"?') == True
    assert func14("example123", "Does the keyword contain an '2'?") == True
    assert func14("example123", "Does the keyword contain an 3?") == True
    assert func14("example", 'Does the keyword contain an "M"?') == True
    assert func14("example", "Does the keyword contain an 'M'?") == True
    assert func14("example", "Does the keyword contain an M?") == True
    assert func14("example", "Is the keyword a fruit?") == None


def test_func15():
    pass
    # assert (
    #     func15(
    #         "cat",
    #         'When you spell out the keyword, is the first letter of the keyword one of the letters in this important group of letters?\nThis is an important group of letters, listed with both upper and lower case in the group: "C", "P", "S", "c", "p", and "s".',
    #     )
    #     == True
    # )
    # assert (
    #     func15(
    #         "dog",
    #         'When you spell out the keyword, is the first letter of the keyword one of the letters in this important group of letters?\nThis is an important group of letters, listed with both upper and lower case in the group: "C", "P", "S", "c", "p", and "s".',
    #     )
    #     == False
    # )
    # assert (
    #     func15(
    #         "Cat",
    #         'When you spell out the keyword, is the first letter of the keyword one of the letters in this important group of letters?\nThis is an important group of letters, listed with both upper and lower case in the group: "C", "P", "S", "c", "p", and "s".',
    #     )
    #     == True
    # )
    # assert (
    #     func15(
    #         "apple",
    #         'When you spell out the keyword, is the first letter of the keyword one of the letters in this important group of letters?\nThis is an important group of letters, listed with both upper and lower case in the group: "C", "P", "S", "c", "p", and "s".',
    #     )
    #     == False
    # )
    # assert (
    #     func15(
    #         "paper",
    #         'When you spell out the keyword, is the first letter of the keyword one of the letters in this important group of letters?\nThis is an important group of letters, listed with both upper and lower case in the group: "C", "P", "S", "c", "p", and "s".',
    #     )
    #     == True
    # )


def test_func16():
    assert func16("python", "Is keyword last letter is 'n'?") == True
    assert func16("python", 'Is keyword last letter is "n"?') == True
    assert func16("python", "Is keyword last letter is n?") == True
    assert func16("python", "Is keyword last letter is 'm'?") == False
    assert func16("python", 'Is keyword last letter is "m"?') == False
    assert func16("python", "Is keyword last letter is m?") == False
    assert func16("example123", "Is keyword last letter is '3'?") == True
    assert func16("example123", 'Is keyword last letter is "3"?') == True
    assert func16("example123", "Is keyword last letter is 3?") == True
    assert func16("python", "Is keyword last letter is 'N'?") == True
    assert func16("python", 'Is keyword last letter is "N"?') == True
    assert func16("python", "Is keyword last letter is N?") == True
    assert func16("python", "Is the keyword a fruit?") == None


def test_func17():
    assert func17("python", "Is keyword first letter is 'p'?") == True
    assert func17("python", 'Is keyword first letter is "p"?') == True
    assert func17("python", "Is keyword first letter is p?") == True
    assert func17("python", "Is keyword first letter is 'n'?") == False
    assert func17("python", 'Is keyword first letter is "n"?') == False
    assert func17("python", "Is keyword first letter is n?") == False
    assert func17("example123", "Is keyword first letter is 'e'?") == True
    assert func17("example123", 'Is keyword first letter is "e"?') == True
    assert func17("example123", "Is keyword first letter is e?") == True
    assert func17("python", "Is keyword first letter is 'P'?") == True
    assert func17("python", 'Is keyword first letter is "P"?') == True
    assert func17("python", "Is keyword first letter is P?") == True
    assert func17("python", "Is the keyword a fruit?") == None


def test_func18():
    assert (
        func18(
            "dominion",
            'Here is an important list of 5 potential keywords: "dominion", "digimon", "division", "duodenum", and "disc jockey". Is the keyword one of the 5 potential keywords?',
        )
        == True
    )
    assert (
        func18(
            "digimon",
            'Here is an important list of 5 potential keywords: "dominion", "digimon", "division", "duodenum", and "disc jockey". Is the keyword one of the 5 potential keywords?',
        )
        == True
    )
    assert (
        func18(
            "random",
            'Here is an important list of 5 potential keywords: "dominion", "digimon", "division", "duodenum", and "disc jockey". Is the keyword one of the 5 potential keywords?',
        )
        == False
    )
    assert (
        func18(
            "division",
            'Here is an important list of 5 potential keywords: "dominion", "digimon", "division", "duodenum", and "disc jockey". Is the keyword one of the 5 potential keywords?',
        )
        == True
    )
    assert (
        func18(
            "disc jockey",
            'Here is an important list of 5 potential keywords: "dominion", "digimon", "division", "duodenum", and "disc jockey". Is the keyword one of the 5 potential keywords?',
        )
        == True
    )
    assert func18("apple", "Invalid question format") == None


def test_func19():
    assert (
        func19(
            "trashcan",
            "Is it any of potential keywords television remote,tackle box,trashcan,",
        )
        == True
    )
    assert func19("trashcan", "Is it any of potential keywords tackle box,") == False
    assert (
        func19(
            "trashcan",
            "Is it any of potential keywords television remote, tackle box, trashcan,",
        )
        == True
    )
    assert (
        func19(
            "trashcan", "Is it any of potential keywords television remote,tackle box,"
        )
        == False
    )
    assert func19("apple", "Invalid question format") == None


def test_func20():
    assert (
        func20(
            "apple",
            'Is the first letter of the word any of the following: a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z or does the keyword (in lowercase) precede "zzzz" in alphabetical order?',
        )
        == True
    )
    assert (
        func20(
            "banana",
            'Is the first letter of the word any of the following: a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z or does the keyword (in lowercase) precede "zzzz" in alphabetical order?',
        )
        == True
    )
    assert (
        func20(
            "apple",
            'Is the first letter of the word any of the following: a b c d e f g h i j k l m A B C D E F G H I J K L M or does the keyword (in lowercase) precede "mzzz" in alphabetical order?',
        )
        == True
    )
    assert (
        func20(
            "orange",
            'Is the first letter of the word any of the following: a b c d e f g h i j k l m A B C D E F G H I J K L M or does the keyword (in lowercase) precede "mzzz" in alphabetical order?',
        )
        == False
    )
    assert (
        func20(
            "apple",
            'Is the first letter of the word any of the following: a b c d e f A B C D E F or does the keyword (in lowercase) precede "fzzz" in alphabetical order?',
        )
        == True
    )
    assert (
        func20(
            "grape",
            'Is the first letter of the word any of the following: a b c d e f A B C D E F or does the keyword (in lowercase) precede "fzzz" in alphabetical order?',
        )
        == False
    )

    assert (
        func20(
            "grape",
            'is the first letter of the word any of the following: a b c d e f A B C D E F or does the keyword (in lowercase) precede "fzzz" in alphabetical order?',
        )
        == False
    )

    assert func20("apple", "Invalid question format") == None


def test_func21():
    assert (
        func21(
            "apple",
            'Does the keyword (in lowercase) precede "kale" in alphabetical order? For example, if the word is "tire inflator", and the keyword is "rabbit", which precedes "tire inflator", so the answer is "yes". For example, if the word is "court", and the keyword is "net", which does not precede "court", so the answer is "no". For example, if the word is "smoke", and the keyword is "orange juice", which precedes "smoke", so the answer is "yes". So for your keyword, does it (in lowercase) alphabetically precede the word? Please answer with "yes" or "no" only.',
        )
        == "yes"
    )
    assert (
        func21(
            "zebra",
            'Does the keyword (in lowercase) precede "kale" in alphabetical order? For example, if the word is "tire inflator", and the keyword is "rabbit", which precedes "tire inflator", so the answer is "yes". For example, if the word is "court", and the keyword is "net", which does not precede "court", so the answer is "no". For example, if the word is "smoke", and the keyword is "orange juice", which precedes "smoke", so the answer is "yes". So for your keyword, does it (in lowercase) alphabetically precede the word? Please answer with "yes" or "no" only.',
        )
        == "no"
    )
    assert (
        func21(
            "kale",
            'Does the keyword (in lowercase) precede "kale" in alphabetical order? For example, if the word is "tire inflator", and the keyword is "rabbit", which precedes "tire inflator", so the answer is "yes". For example, if the word is "court", and the keyword is "net", which does not precede "court", so the answer is "no". For example, if the word is "smoke", and the keyword is "orange juice", which precedes "smoke", so the answer is "yes". So for your keyword, does it (in lowercase) alphabetically precede the word? Please answer with "yes" or "no" only.',
        )
        == "no"
    )
    assert func21("apple", "Invalid question format") == None


def test_func22():
    assert (
        func22("muffin", "Does its name start with the letters 'Q', 'R', 'S', or 'T'?")
        == False
    )
    assert (
        func22("muffin", "Does its name start with the letters 'M', 'N', 'O', or 'P'?")
        == True
    )
    assert (
        func22("apple", "Does its name start with the letters 'A', 'B', 'C', or 'D'?")
        == True
    )
    assert (
        func22("banana", "Does its name start with the letters 'E', 'F', 'G', or 'H'?")
        == False
    )
    assert (
        func22("cherry", "Does its name start with the letters 'C', 'H', 'E', or 'R'?")
        == True
    )
    assert func22("apple", "Invalid question format") == None


def test_func():
    assert (
        func(
            "apple",
            'Does the keyword (in lowercase) come before "banana" in alphabetical order?',
        )
        is True
    )
    assert func("banana", 'Does the keyword begins with the letter "a"?') is False
    assert func("carrot", "Does the keyword start with the letter 'c'?") is True
    assert (
        func("apple", "Is the keyword one of the following? apple, banana, carrot?")
        is True
    )
    assert (
        func(
            "banana",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter 'z'?",
        )
        is False
    )
    assert (
        func(
            "123",
            'Does the keyword (in lowercase) come before "apple" in alphabetical order?',
        )
        is True
    )
    assert func("apple", "Invalid question format") is None
    assert func("Kaggle", "Is it Agent Alpha?") is True
    assert func("Kaggle", "Is it Beta Bravo?") is None
    assert func("Kaggle", "Is it Gamma Delta?") is None
    assert (
        func(
            "bulgaria",
            'Does the keyword (in lowercase) precede "measuring cup" in alphabetical order?',
        )
        is True
    )

    assert (
        func(
            "Iron bar",
            "Is any of the letters ['l','w'] inside the spelling of the keyword?",
        )
        is False
    )

    assert (
        func(
            "Iron bar",
            "Is the keyword one of the following words: 'apple', 'banana', 'carrot' ?",
        )
        is False
    )

    assert (
        func(
            "Iron bar",
            "Is the keyword one of the following words: 'apple', 'banana', 'carrot' ?",
        )
        is False
    )

    assert (
        func(
            "Iron bar",
            "Is the keyword one of the following words:'apple', 'banana', 'carrot' ?",
        )
        is False
    )

    assert (
        func(
            "Piano",
            "Is it a place recognized for its architectual beauty?",
        )
        is None
    )

    # オリジナルのプロトコルは、末尾に"?"がないとNoneを返す
    assert (
        func(
            "broth",
            "Is the keyword one of the following? bacon, Baguette, banana, Bath Mat, battery, bean, bedspread, broth, butter, Cantaloupe, Cauliflower, Cereal, Cheesecake, chutney, coke, conditioner, cotton, Croissant?",
        )
        is True
    )

    # 末尾に"?"があってもなくても判定できるようにした
    assert (
        func(
            "broth",
            "Is the keyword one of the following? bacon, Baguette, banana, Bath Mat, battery, bean, bedspread, broth, butter, Cantaloupe, Cauliflower, Cereal, Cheesecake, chutney, coke, conditioner, cotton, Croissant",
        )
        is True
    )

    assert (
        func(
            "coca-cola",
            'Does the keyword (in lowercase) precede "pepsi" in alphabetical order?',
        )
        is True
    )

    assert (
        func(
            "coca-cola",
            'Does the keyword (in lowercase) precede "pepsi" in alphabetical order?',
        )
        is True
    )

    assert (
        func(
            "Lint Trap",
            "Does the keyword begin with the letter t?",
        )
        is False
    )
    assert (
        func(
            "Lint Trap",
            "Does the keyword begin with the letter 't'?",
        )
        is False
    )
    assert (
        func(
            "Lint Trap",
            'Does the keyword begin with the letter "t"?',
        )
        is False
    )

    assert (
        func(
            "Lint Trap",
            "Does the keyword begin with the letter T?",
        )
        is False
    )
    assert (
        func(
            "Lint Trap",
            "Does the keyword begin with the letter 'T'?",
        )
        is False
    )
    assert (
        func(
            "Lint Trap",
            'Does the keyword begin with the letter "T"?',
        )
        is False
    )

    assert (
        func(
            "Lint Trap",
            "Does the keyword begin with the letter l?",
        )
        is True
    )
    assert (
        func(
            "Lint Trap",
            "Does the keyword begin with the letter 'l'?",
        )
        is True
    )
    assert (
        func(
            "Lint Trap",
            'Does the keyword begin with the letter "l"?',
        )
        is True
    )

    assert (
        func(
            "lint Trap",
            "Does the keyword begin with the letter l?",
        )
        is True
    )
    assert (
        func(
            "lint Trap",
            "Does the keyword begin with the letter 'l'?",
        )
        is True
    )
    assert (
        func(
            "lint Trap",
            'Does the keyword begin with the letter "l"?',
        )
        is True
    )

    assert (
        func(
            "lint Trap",
            "Does the keyword begin with the letter L?",
        )
        is True
    )
    assert (
        func(
            "lint Trap",
            "Does the keyword begin with the letter 'L'?",
        )
        is True
    )
    assert (
        func(
            "lint Trap",
            'Does the keyword begin with the letter "L"?',
        )
        is True
    )

    assert (
        func(
            "wind vane",
            "Does the keyword include the letter A?",
        )
        is True
    )
    assert (
        func(
            "wind vane",
            "Does the keyword include the letter C?",
        )
        is False
    )
    assert (
        func(
            "water chestnut",
            "Does the keyword start with the letter 'v?",
        )
        is False
    )

    assert (
        func(
            "tv stand",
            'Does the keyword (in lowercase) precede "tweezers" in alphabetical order?',
        )
        is True
    )

    # オリジナルのプロトコルは、""がないとNoneを返す
    assert (
        func(
            "tv stand",
            "Does the keyword (in lowercase) precede 'tweezers' in alphabetical order?",
        )
        is True
    )

    assert (
        func(
            "purse",
            "Does the keyword start with one of the letters 'p', 'q', 'r'?",
        )
        is True
    )

    assert (
        func(
            "purse",
            "Does the keyword start with one of the letters 'S', 'V', 'M', 'W', 'X' or 'R'?",
        )
        is False
    )

    assert (
        func(
            "doog poop",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter 'o'?",
        )
        is True
    )

    assert (
        func(
            "Kaggle",
            "Is it Agent Alpha?",
        )
        is True
    )

    assert (
        func(
            "apple",
            'Does the keyword (in lowercase) come before "banana" in alphabetical order?',
        )
        is True
    )

    assert func("apple", 'Does the keyword begin with the letter "a"?') == True

    assert (
        func(
            "apple",
            "Does the keyword start with one of the letters 'a', 'b', 'c'?",
        )
        is True
    )

    assert (
        func(
            "apple",
            "Is the keyword one of the following? apple, banana, carrot?",
        )
        is True
    )

    assert (
        func(
            "apple",
            "Considering every letter in the name of the keyword, does the name of the keyword include the letter 'a'?",
        )
        is True
    )

    assert func("Kaggle", "Is it Agent Alpha?") is True

    assert (
        func(
            "Iron bar",
            "Is any of the letters ['l','w'] inside the spelling of the keyword?",
        )
        is False
    )

    assert (
        func(
            "Iron bar",
            "Is the keyword one of the following words: 'apple', 'banana', 'carrot' ?",
        )
        is False
    )

    assert (
        func(
            "Apple",
            "Does the word start with the letter 'A' , 'B', or 'C'?",
        )
        is True
    )

    assert func("apple", 'Does the keyword end with the letter "e"?') is True

    assert func("apple", 'Does the keyword contain the letter "a"?') is True

    assert func("apple", 'Does the keyword include the letter "a"?') is True

    assert (
        func(
            "apple",
            "str(obs.keyword)[0].lower() in list('abcdefghijklm') #Is the first letter of the keyword any of the following: ['a','b','c','d','e','f','g','h','i','j','k','l','m'] ?",
        )
        == True
    )

    assert func("example", 'Does the keyword contain an "m"?') == True

    assert func("python", "Is keyword last letter is 'n'?") == True

    assert func("python", "Is keyword first letter is 'p'?") == True

    assert (
        func(
            "dominion",
            'Here is an important list of 5 potential keywords: "dominion", "digimon", "division", "duodenum", and "disc jockey". Is the keyword one of the 5 potential keywords?',
        )
        == True
    )

    assert (
        func(
            "pine cone",
            'Does the keyword (in lowercase) come before "pineapple" in alphabetical order?',
        )
        == True
    )
    assert (
        func(
            "pine cone",
            'Does the keyword (in lowercase) come before "pine nut" in alphabetical order?',
        )
        == True
    )

    assert (
        func(
            "trashcan",
            "Is it any of potential keywords  television remote,tackle box,trashcan,",
        )
        == True
    )

    assert (
        func(
            "trashcan",
            "Is it any of potential keywords tackle box,",
        )
        == False
    )

    assert (
        func(
            "Muffin",
            "Does its name start with the letters 'Q', 'R', 'S', or 'T'?",
        )
        == False
    )

    assert (
        func(
            "Muffin",
            "Does its name start with the letters 'M', 'N', 'O', or 'P'?",
        )
        == True
    )

    assert (
        func(
            "workout log",
            """keyword Please follow these 2 steps to compare alphabetical order:
Step 1: take the known keyword and the comparison word and write them out with a space between each character, in lowercase.
Step 2: Now iterate through the characters of both words, until you find a mismatch. The first mismatch determines alphabetical order.
If one word ends while the other has more letters, the shorter word comes first alphabetically.
Finally answer with yes or no.
For your reference, the alphabetical order of characters is: a < b < c < d < e < f < g < h < i < j < k < l < m < n < o < p < q < r < s < t < u < v < w < x < y < z.

Does the keyword (in lowercase) precede "lf" in alphabetical order?""",
        )
        == False
    )
    assert (
        func(
            "workout log",
            """keyword Please follow these 2 steps to compare alphabetical order:
Step 1: take the known keyword and the comparison word and write them out with a space between each character, in lowercase.
Step 2: Now iterate through the characters of both words, until you find a mismatch. The first mismatch determines alphabetical order.
If one word ends while the other has more letters, the shorter word comes first alphabetically.
Finally answer with yes or no.
For your reference, the alphabetical order of characters is: a < b < c < d < e < f < g < h < i < j < k < l < m < n < o < p < q < r < s < t < u < v < w < x < y < z.

Does the keyword (in lowercase) precede "worst film" in alphabetical order?""",
        )
        == True
    )


if __name__ == "__main__":
    pytest.main()
