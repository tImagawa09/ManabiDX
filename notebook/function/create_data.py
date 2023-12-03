import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# 商品カテゴリ名を『-』でsplit
def split_column_by_delimiter(df, column, delimiter, new_columns):
    if column not in df.columns:
        raise ValueError(f"{column} not found in columns")
    # 新しい列を追加する
    df[new_columns] = df[column].str.split(delimiter, expand=True)
    # 先頭と末尾の半角スペースを除去する
    df[new_columns] = df[new_columns].apply(lambda x: x.str.strip())
    # # 元の列を削除する
    # df.drop(columns=[column], inplace=True)
    return df


def check_unique_values(df, same_name_column, unique_column):
    result = df.groupby(same_name_column)[unique_column].unique()
    return result