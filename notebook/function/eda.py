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


def plot_sales_by_category(df, store_id):
    # 日付列をdatetime型に変換
    df['日付'] = pd.to_datetime(df['日付'])
    
    # 指定した店舗IDのデータを抽出
    store_data = df[df['店舗ID'] == store_id]

    # 商品カテゴリごとに時系列データを作成
    pivot_table = pd.pivot_table(store_data, values='売上', index='日付', columns='商品カテゴリ', aggfunc='sum')

    # グラフのプロット
    plt.figure(figsize=(12, 8))
    ax = sns.lineplot(data=pivot_table, dashes=False)

    # グラフの設定
    plt.title(f'店舗ID {store_id} - 商品カテゴリ別売り上げ')
    plt.xlabel('日付')
    plt.ylabel('売り上げ')
    plt.legend(title='商品カテゴリID', loc='upper left', bbox_to_anchor=(1, 1))

    # x軸の日付を半年ごとに設定
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    plt.xticks(rotation=45, ha='right')  # 45度傾けて表示

    plt.show()

def plot_sales_by_category_foreach_and_store(df, store_id, agg_period='D'):
    """
    指定した店舗IDの各商品カテゴリごとに、売り上げの時系列データをグラフに描画します。

    Parameters:
    - df (pd.DataFrame): 入力データフレーム
    - store_id (int): 対象の店舗ID
    - agg_period (str): 集計期間の指定 ('D': 日ごと, 'W': 週ごと, 'M': 月ごと)、デフォルトは 'D'

    Returns:
    None
    """

    # 日付列をdatetime型に変換
    df['日付'] = pd.to_datetime(df['日付'])
    
    # 指定した店舗IDのデータを抽出
    store_data = df[df['店舗ID'] == store_id]

    # 商品カテゴリごとにグラフを描画
    unique_categories = store_data['商品カテゴリ'].unique()

    # y軸の範囲を保存するリスト
    y_limits = []

    for category in unique_categories:
        category_data = store_data[store_data['商品カテゴリ'] == category]

        # 期間ごとにデータを集計
        pivot_table = pd.pivot_table(category_data, values='売上', index=pd.Grouper(key='日付', freq=agg_period), aggfunc='sum')

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=pivot_table, dashes=False)

        # y軸の範囲を保存
        y_limits.append(plt.gca().get_ylim())

        # グラフの設定
        plt.title(f'店舗ID {store_id} - 商品カテゴリ: {category} 別売り上げ ({agg_period})')
        plt.xlabel('日付')
        plt.ylabel('売り上げ')
        plt.legend(title='商品カテゴリ', loc='upper left', bbox_to_anchor=(1, 1))

        # y軸の範囲を設定（指定の値を採用）
        plt.ylim(0, 1500000)
        plt.ticklabel_format(style='plain', axis='y')

        # x軸の日付を設定
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
        plt.xticks(rotation=45, ha='right')  # 45度傾けて表示



    # y軸の範囲を揃える
    min_y = min([y[0] for y in y_limits])
    max_y = max([y[1] for y in y_limits])
    plt.axis(ymin=min_y, ymax=max_y)
    plt.grid()

    plt.show()


def plot_sales_by_category_foreach(df, agg_period='D'):
    """
    指定した店舗IDの各商品カテゴリごとに、売り上げの時系列データをグラフに描画します。

    Parameters:
    - df (pd.DataFrame): 入力データフレーム
    - store_id (int): 対象の店舗ID（今回は使用しない）
    - agg_period (str): 集計期間の指定 ('D': 日ごと, 'W': 週ごと, 'M': 月ごと)、デフォルトは 'D'

    Returns:
    None
    """

    # 日付列をdatetime型に変換
    df['日付'] = pd.to_datetime(df['日付'])

    # 商品カテゴリごとにグラフを描画
    unique_categories = df['商品カテゴリ'].unique()

    # y軸の範囲を保存するリスト
    y_limits = []

    for category in unique_categories:
        category_data = df[df['商品カテゴリ'] == category]

        # 期間ごとにデータを集計
        pivot_table = pd.pivot_table(category_data, values='売上', index=pd.Grouper(key='日付', freq=agg_period), aggfunc='sum')

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=pivot_table, dashes=False)

        # y軸の範囲を保存（最大値を採用）
        y_limits.append(plt.gca().get_ylim())



        # グラフの設定
        plt.title(f'商品カテゴリ: {category} 別売り上げ ({agg_period})')
        plt.xlabel('日付')
        plt.ylabel('売り上げ')
        plt.legend(title='商品カテゴリ', loc='upper left', bbox_to_anchor=(1, 1))

        # y軸の範囲を設定（指定の値を採用）
        plt.ylim(0, 9000000)
        plt.ticklabel_format(style='plain', axis='y')

        # x軸の日付を設定
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
        plt.xticks(rotation=45, ha='right')  # 45度傾けて表示
        plt.show()

    # y軸の範囲を揃える（全体の最大値を採用）
    max_y = max([y[1] for y in y_limits])
    plt.ylim(0, max_y)
    plt.grid()

    

def plot_sales_by_store_foreach(df, agg_period='D'):
    """
    各店舗ごとに、売り上げの時系列データをグラフに描画します。

    Parameters:
    - df (pd.DataFrame): 入力データフレーム
    - agg_period (str): 集計期間の指定 ('D': 日ごと, 'W': 週ごと, 'M': 月ごと)、デフォルトは 'D'

    Returns:
    None
    """

    # 日付列をdatetime型に変換
    df['日付'] = pd.to_datetime(df['日付'])

    # 各店舗の日付別の売り上げの最大値を取得
    max_sales_by_store = df.groupby(['店舗ID', '日付'])['売上'].sum().groupby('店舗ID').max()

    # 店舗ごとにグラフを描画
    unique_stores = df['店舗ID'].unique()

    for store_id in unique_stores:
        store_data = df[df['店舗ID'] == store_id]

        # 期間ごとにデータを集計
        pivot_table = pd.pivot_table(store_data, values='売上', index=pd.Grouper(key='日付', freq=agg_period), aggfunc='sum')

        # 各店舗での最大の売り上げ値を取得
        max_sales = max_sales_by_store[store_id]

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=pivot_table, dashes=False)

        # y軸の範囲を設定（指定の値を採用）
        plt.ylim(0, 1500000)

        # グラフの設定
        plt.title(f'店舗ID {store_id} 別売り上げ ({agg_period})')
        plt.xlabel('日付')
        plt.ylabel('売り上げ')

        # y軸の表記を通常の表記に戻す
        plt.ticklabel_format(style='plain', axis='y')

        # x軸の日付を設定
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
        plt.xticks(rotation=45, ha='right')  # 45度傾けて表示

        # グラフを表示
        plt.grid()
        plt.show()