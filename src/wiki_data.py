"""wiki_data.py"""

import pandas as pd
import word_utils


class WikiData:
    def __init__(self, config):
        self.config = config
        self.context: str | None = None

    def setup(self, keyword: str) -> None:
        self.df = self.read_csv(self.config.wikipedia_context_path)
        self.set_context(keyword)

    def read_csv(self, csv_path: str) -> str:
        df = pd.read_csv(csv_path)
        return df

    def set_context(self, keyword: str) -> str:
        try:
            # Perfect match
            indices = self.df[self.df["keyword"] == keyword].index
            simple_id = select_simplest_text_id(self.df, indices)
            if simple_id == -1:
                simple_id = indices[0]
            self.context = self.df[self.df["id"] == simple_id]["text"].values[0]
            self.config.logger.log(f"Perfect match: {keyword}")
        except:
            try:
                # Lower match
                indices = self.df[self.df["keyword_lower"] == make_lower(keyword)].index
                simple_id = select_simplest_text_id(self.df, indices)
                if simple_id == -1:
                    simple_id = indices[0]
                self.context = self.df[self.df["id"] == simple_id]["text"].values[0]
                if len(self.context) <= self.config.min_context_len:
                    self.context = self.df[self.df["id"] == indices[0]]["text"].values[
                        0
                    ]
                self.config.logger.log(f"Lower match: {keyword}")
            except:
                try:
                    # Normalize match
                    indices = word_utils.find_word_indices(
                        keyword, self.df["keyword"].values.tolist()
                    )
                    simple_id = select_simplest_text_id(self.df, indices)
                    if simple_id == -1:
                        simple_id = indices[0]
                    self.context = self.df[self.df["id"] == simple_id]["text"].values[0]
                    if len(self.context) <= self.config.min_context_len:
                        self.context = self.df[self.df["id"] == indices[0]][
                            "text"
                        ].values[0]
                    self.config.logger.log(f"Normalize match: {keyword}")
                except:
                    self.context = ""
                    self.config.logger.log(f"No match: {keyword}")

        if len(self.context) < self.config.min_context_len:
            self.context = ""
        else:
            self.context = split_text_and_remove_last(
                self.context[: self.config.max_context_len]
            )

        self.config.logger.log(f"Context: {self.context}")


def make_lower(keyword):
    return keyword.replace(",", "").replace("-", " ").replace("–", " ").strip().lower()


def select_longest_text_id(df: pd.DataFrame, indices: list[int]) -> int:
    """
    候補となるidの中で、text_lenが一番長いidを選択する関数

    Args:
        df (pd.DataFrame): データフレーム
        indices (list[int]): 候補の行インデックスのリスト

    Returns:
        int: text_lenが一番長い行のid
    """
    subset_df = df.loc[indices, :]
    max_text_len_row = subset_df.loc[subset_df["text_len"].idxmax()]
    return max_text_len_row["id"]


def select_simplest_text_id(df: pd.DataFrame, indices: list[int]) -> int:
    """
    候補となるidの中で、()がないidを選択する関数

    Args:
        df (pd.DataFrame): データフレーム
        indices (list[int]): 候補の行インデックスのリスト

    Returns:
        int: text_lenが一番長い行のid
    """
    subset_df = df.loc[indices, :]
    for t in subset_df.title.values.tolist():
        if "(" not in t and ")" not in t:
            return subset_df[subset_df["title"] == t]["id"].values[0]

    return -1


def split_text_and_remove_last(text: str) -> str:
    """
    与えられたテキストを ". " で分割し、最後の要素を削除して再結合し、
    最後に「以下は省略」を意味する英語のメッセージを追加して文字列を返します。

    Parameters:
    text (str): 入力テキスト

    Returns:
    str: 分割され、最後の要素が削除された文字列にメッセージを追加したもの
    """
    # ". "でテキストを分割
    split_text = text.split(". ")

    # 最後の要素を削除
    if split_text:
        split_text.pop()

    # リストを再結合して文字列にする
    result_text = ". ".join(split_text)

    # 最後に省略を示すメッセージを追加
    result_text += ". \n(The rest of the context is omitted for brevity.)"

    return result_text


def process(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[:, "text_len"] = df.loc[:, "text"].map(len)
    df = df.sort_values(by="text_len", ascending=False)
    df.loc[:, "keyword"] = df.loc[:, "title_wo_parentheses"]
    df["keyword_lower"] = df["keyword"].map(make_lower)
    return df.reset_index(drop=True)


def drop_nan_and_reset_index(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    指定された列にNaNが含まれている行をドロップし、ドロップされた行とインデックスをリセットしたデータフレームを表示する関数。

    Parameters:
    df (pd.DataFrame): 処理するデータフレーム
    column_name (str): NaNをチェックする列の名前

    Returns:
    pd.DataFrame: NaNをドロップし、インデックスをリセットしたデータフレーム
    """
    # NaNが含まれている行を抽出
    rows_with_nan = df[df[column_name].isna()]

    # 指定された列にNaNが含まれている行をドロップ
    df_cleaned = df.dropna(subset=[column_name])

    # インデックスをリセット
    df_cleaned = df_cleaned.reset_index(drop=True)

    # 結果を表示
    print("NaNが含まれている行:")
    print(rows_with_nan)

    return df_cleaned
