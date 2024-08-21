"""protocol.py"""

import re


def func0(keyword: str, question: str) -> bool | None:
    keyword = keyword.lower().strip()
    question = question.lower().strip()

    if question in ["are we playing 20 questions?", "is it agent alpha?"]:
        return True

    return None


def func1(keyword: str, question: str) -> bool | None:
    """
    Agent Alphaに対応する関数
    https://www.kaggle.com/code/lohmaa/llm20-agent-alpha

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower()
    keyword_pattern = r"^[\x21-\x7E\s]+$"
    question_pattern = (
        r'keyword.*(?:come before|precede) ?["\'"]?([^\"]+)["\'"]? .+ order\?$'
    )

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.search(question_pattern, question)
    if match:
        compare_word = match.group(1).lower()
        return keyword < compare_word

    return None


def func2(keyword: str, question: str) -> bool | None:
    """
    最初の文字が指定された文字で始まるかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = r'^Does the keyword begin(?:s)? with the letter ?["\'"]?([a-zA-Z0-9])["\'"]?\??$'

    if not re.match(keyword_pattern, keyword) or not re.match(
        question_pattern, question
    ):
        return None

    match = re.match(question_pattern, question)
    search_letter = match.group(1)

    return keyword.strip().lower().startswith(search_letter.lower())


def func3(keyword: str, question: str) -> bool | None:
    """
    キーワードの最初の文字が指定された文字で始まるかどうかを判定する関数

    Parameters:
    keyword (str): 判定対象のキーワード
    question (str): 判定の条件を含む質問

    Returns:
    bool | None: キーワードが指定された文字で始まる場合はTrue、そうでない場合はFalse
                 質問が無効な場合はNoneを返す
    """
    question_patterns = [
        r'^Does the keyword start with one of the letters ["\']?([a-zA-Z0-9])["\']?(?:, ["\']?([a-zA-Z0-9])["\']?)*(?:\s*or\s*["\']?([a-zA-Z0-9])["\']?)?\?$',
        r'^Does the keyword start with the letter ["\']?([a-zA-Z0-9])["\']?\?$',
    ]
    if not any(re.match(pattern, question) for pattern in question_patterns):
        return None

    if re.match(question_patterns[0], question):
        letters = re.findall(r'["\']?([a-zA-Z0-9])["\']?', question)
    else:
        match = re.match(question_patterns[1], question)
        letters = [match.group(1)]

    letters = [c.lower() for c in letters]
    return keyword.strip()[0].lower() in letters


def func4(keyword: str, question: str) -> bool | None:
    """
    キーワードが指定された文字列の中に含まれているかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower().strip()
    question = question.lower().strip()
    keyword_pattern = r"^[a-zA-Z\s]+$"
    question_pattern = r"^is the keyword one of the following\? ([a-zA-Z\s,]+)\??$"

    if not re.match(keyword_pattern, keyword) or not re.match(
        question_pattern, question
    ):
        return None

    match = re.match(question_pattern, question)
    options = [option.strip() for option in match.group(1).split(",")]
    return keyword in [option.lower() for option in options]


def func5(keyword: str, question: str) -> bool | None:
    """
    指定した文字がキーワードに含まれているかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower()
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = r'^Considering every letter in the name of the keyword, does the name of the keyword include the letter ?["\'"]?([a-zA-Z0-9])["\'"]?\?$'

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.match(question_pattern, question)
    if match:
        search_letter = match.group(1).lower()
        return search_letter in keyword

    return None


def func6(keyword: str, question: str) -> bool | None:
    """
    キーワードリストが全て含まれていたらTrueを返す関数
    """
    target_words = [["Agent", "Alpha"]]  # Is it Agent Alpha?
    for words in target_words:
        if all(word.lower() in question.lower() for word in words):
            return True
    return None


def func7(keyword: str, question: str) -> bool | None:
    """
    https://www.kaggle.com/competitions/llm-20-questions/leaderboard?dialog=episodes-episode-55400288

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower().strip()
    question = question.lower().strip()
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = (
        r"^is any of the letters \[(.*)\] inside the spelling of the keyword\?$"
    )

    if not re.match(keyword_pattern, keyword) or not re.match(
        question_pattern, question
    ):
        return None

    match = re.match(question_pattern, question)
    letters = [char.strip().strip("'") for char in match.group(1).split(",")]
    return any(letter in keyword for letter in letters)


def func8(keyword: str, question: str) -> bool | None:
    """
    https://www.kaggle.com/competitions/llm-20-questions/leaderboard?dialog=episodes-episode-55400288

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower().strip()
    question = question.lower().strip()
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = (
        r"^is the keyword one of the following words: ?'([a-zA-Z0-9\s\',]+)'\s?\?$"
    )

    if not re.match(keyword_pattern, keyword) or not re.match(
        question_pattern, question
    ):
        return None

    match = re.match(question_pattern, question)
    words = [word.strip().strip("'") for word in match.group(1).split(",")]
    return keyword in [word.lower() for word in words]


def func9(keyword: str, question: str) -> bool | None:
    """
    キーワードの最初の文字が指定された文字で始まるかどうかを判定する関数

    パターン:
    - Does the word start with the letter n , 0, or p?
    - Does the keyword start with the letter 'n', '0', or 'p'?
    - Does the keyword start with the letter 'n',?
    """
    # キーワードが英数字とスペースのみから成るかをチェックするパターン
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"

    # 質問のパターンリストを定義
    question_patterns = [
        r"^Does the (word|keyword) start with the letter (.+?),?(?: or .*)?\?$"
    ]

    # キーワードと質問が定義されたパターンに一致するかをチェック
    if not re.match(keyword_pattern, keyword):
        return None

    match = None
    for pattern in question_patterns:
        match = re.match(pattern, question)
        if match:
            break

    if not match:
        return None

    # 抽出された文字列を解析し、不要な文字を除去
    letters_str = match.group(2)
    # 文字列リストの抽出
    letters = re.findall(r"[a-zA-Z0-9]", letters_str)

    # 文字を小文字に変換
    letters = [c.lower() for c in letters]

    # キーワードの最初の文字がリストに含まれているかを判定
    return keyword.strip()[0].lower() in letters


def func10(keyword: str, question: str) -> bool | None:
    """
    キーワードの最後の文字が指定された文字で終わるかどうかを判定する関数
    """
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = (
        r'^Does the keyword end with the letter ["\'"]?([a-zA-Z0-9])["\'"]?\?$'
    )

    if not re.match(keyword_pattern, keyword) or not re.match(
        question_pattern, question
    ):
        return None

    match = re.match(question_pattern, question)
    search_letter = match.group(1)

    return keyword.strip().lower().endswith(search_letter.lower())


def func11(keyword: str, question: str) -> bool | None:
    """
    キーワードが指定された文字を含むかどうかを判定する関数
    """
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = (
        r'^Does the keyword contain the letter ["\'"]?([a-zA-Z0-9])["\'"]?\?$'
    )

    if not re.match(keyword_pattern, keyword) or not re.match(
        question_pattern, question
    ):
        return None

    match = re.match(question_pattern, question)
    search_letter = match.group(1)

    return search_letter.lower() in keyword.lower()


def func12(keyword: str, question: str) -> bool | None:
    """
    キーワードが指定された文字を含むかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_patterns = [
        r'^Does the keyword include the letter ["\'"]?([a-zA-Z0-9])["\'"]?\??$',
        r'^Does the keyword contain the letter ["\'"]?([a-zA-Z0-9])["\'"]?\??$',
        r'^Is the letter ["\'"]?([a-zA-Z0-9])["\'"]? in the keyword\??$',
    ]

    if not re.match(keyword_pattern, keyword):
        return None

    for pattern in question_patterns:
        match = re.match(pattern, question)
        if match:
            search_letter = match.group(1)
            return search_letter.lower() in keyword.lower()

    return None


def func13(keyword: str, question: str) -> bool | None:
    """
    agent_first_letterに対応する関数
    https://www.kaggle.com/code/gavinxgcao/a-different-interaction-between-asker-and-answer

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower()
    keyword_pattern = r"^[\x21-\x7E\s]+$"
    question_pattern = r".*str\(obs\.keyword\)\[0\]\.lower\(\) in list\([\'\"]([a-z,\'\"]+)[\'\"]\) .*: (\[[\'\"a-z,]+]) ?\?$"

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.search(question_pattern, question)
    if match:
        letters = match.group(1).replace("'", "").replace('"', "").split(",")
        compare_letters = (
            match.group(2)
            .replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace('"', "")
            .split(",")
        )
        return keyword[0] in compare_letters

    return None


def func14(keyword: str, question: str) -> bool | None:
    """
    キーワードに特定の文字が含まれているかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower()
    keyword_pattern = r"^[\x21-\x7E\s]+$"
    question_pattern = r'^Does the keyword contain an ?["\'"]?([a-zA-Z0-9])["\'"]?\??$'

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.match(question_pattern, question)
    if match:
        char_to_check = match.group(1).lower()
        return char_to_check in keyword

    return None


def func15(keyword: str, question: str) -> bool | None:
    """
    指定された重要な文字群にキーワードの最初の文字が含まれているかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower().replace(" ", "")
    question = question.strip().replace("\n", "")
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = r'When you spell out the keyword, is the first letter of the keyword one of the letters in this important group of letters\?\s*This is an important group of letters, listed with both upper and lower case in the group: ["\']([a-zA-Z0-9,\s]+)["\']\.'

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.search(question_pattern, question)
    if match:
        important_letters = match.group(1).replace(" ", "").split(",")
        first_letter = keyword[0]
        return (
            first_letter in important_letters
            or first_letter.upper() in important_letters
        )

    return None


def func16(keyword: str, question: str) -> bool | None:
    """
    指定した文字がキーワードの最後の文字であるかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower().strip()
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = r'^Is keyword last letter is ?["\'"]?([a-zA-Z0-9])["\'"]?\?$'

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.match(question_pattern, question)
    if match:
        search_letter = match.group(1).lower()
        return keyword[-1] == search_letter

    return None


def func17(keyword: str, question: str) -> bool | None:
    """
    指定した文字がキーワードの最初の文字であるかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower().strip()
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = r'^Is keyword first letter is ?["\'"]?([a-zA-Z0-9])["\'"]?\?$'

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.match(question_pattern, question)
    if match:
        search_letter = match.group(1).lower()
        return keyword[0] == search_letter

    return None


def func18(keyword: str, question: str) -> bool | None:
    """
    指定したリストの中にキーワードが含まれているかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower().strip()
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = r"^Here is an important list of \d+ potential keywords: (.+?)\. Is the keyword one of the \d+ potential keywords\?$"

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.match(question_pattern, question)
    if match:
        keywords_string = match.group(1)
        keywords_list = re.split(r", and |, | and ", keywords_string)
        keywords_list = [k.lower().replace('"', "").strip() for k in keywords_list]
        return keyword in keywords_list

    return None


def func19(keyword: str, question: str) -> bool | None:
    """
    指定したリストの中にキーワードが含まれているかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower().strip()
    question = question.strip()
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = r"^Is it any of potential keywords\s*(.+)$"

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.search(question_pattern, question)
    if match:
        keywords_string = match.group(1)
        keywords_list = re.split(r",\s*", keywords_string.strip(", "))
        keywords_list = [k.lower().strip() for k in keywords_list]
        return keyword in keywords_list

    return None


def func20(keyword: str, question: str) -> bool | None:
    """
    キーワードの最初の文字が指定された文字リストに含まれているか、または
    キーワードが指定された単語よりもアルファベット順で前にあるかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower().strip()
    question = question.lower()
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = r'^is the first letter of the word any of the following: (.+) or does the keyword \(in lowercase\) precede "([a-zA-Z0-9]+)" in alphabetical order\?$'

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.search(question_pattern, question)
    if match:
        letters = match.group(1).split()
        compare_word = match.group(2).lower()
        return keyword[0] in letters or keyword < compare_word

    return None


def func21(keyword: str, question: str) -> str | None:
    """
    キーワードが指定された単語よりもアルファベット順で前にあるかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        str | None: 質問に合致する場合は "yes" / "no" を返し、合致しない場合は None を返す。
    """
    keyword = keyword.lower().strip()
    keyword_pattern = r"^[a-zA-Z0-9\s]+$"
    question_pattern = r'^Does the keyword \(in lowercase\) precede "([a-zA-Z0-9\s]+)" in alphabetical order\?'

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.search(question_pattern, question)
    if match:
        compare_word = match.group(1).lower().strip()
        return "yes" if keyword < compare_word else "no"

    return None


def func22(keyword: str, question: str) -> bool | None:
    """
    キーワードの最初の文字が指定された文字リストに含まれているかどうかを判定する関数

    Args:
        keyword (str): 判定対象のキーワード。
        question (str): 質問文。

    Returns:
        bool | None: 質問に合致する場合はTrue/Falseを返し、合致しない場合はNoneを返す。
    """
    keyword = keyword.lower().strip()
    question = question.lower().replace(", or ", ", ").replace("'", "")
    keyword_pattern = r"^[a-zA-Z\s]+$"
    question_pattern = r"^does its name start with the letters ([a-z,\s]+)\?$"

    if not re.match(keyword_pattern, keyword):
        return None

    match = re.match(question_pattern, question)
    if match:
        letters = [char.strip() for char in match.group(1).split(",")]
        return keyword[0] in letters

    return None


def func(keyword: str, question: str) -> bool | None:
    """
    プロトコルをまとめて追加する関数
    https://www.kaggle.com/competitions/llm-20-questions/discussion/515801"""
    solves = [
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
    ]
    for f in solves:
        result = f(keyword, question)
        if result is not None:
            return result
    return None
