import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_total_sales_by_store(df, unit="day"):
    # 日付列をdatetime型に変換
    df["日付"] = pd.to_datetime(df["日付"])

    # 単位ごとにデータを集計
    if unit == "day":
        grouper = pd.Grouper(key="日付", freq="D")
    elif unit == "month":
        grouper = pd.Grouper(key="日付", freq="M")
    elif unit == "year":
        grouper = pd.Grouper(key="日付", freq="Y")
    else:
        raise ValueError("Invalid unit. Use 'day', 'month', or 'year'.")

    # 店舗IDごとにプロット
    unique_stores = df["店舗ID"].unique()
    for store_id in unique_stores:
        store_data = df[df["店舗ID"] == store_id]
        total_sales_by_store = (
            store_data.groupby(["店舗ID", grouper])["売上"].sum().reset_index()
        )

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        ax = sns.lineplot(
            x="日付",
            y="売上",
            data=total_sales_by_store,
            label=f"店舗ID {store_id}",
            dashes=False,
        )

        # グラフの設定
        title = f"店舗ID {store_id} - 売り上げ合計推移 ({unit}単位)"
        plt.title(title)
        plt.xlabel(unit.capitalize())
        plt.ylabel("売り上げ")
        plt.legend(title="店舗ID", loc="upper left", bbox_to_anchor=(1, 1))

        if unit == "day":
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
            plt.xticks(rotation=45, ha="right")  # 45度傾けて表示
        plt.ylim(0, 12000000)
        plt.ticklabel_format(style="plain", axis="y")
        plt.grid()
        plt.show()


def plot_sales_by_store_category(df, unit="day"):
    # 日付列をdatetime型に変換
    df["日付"] = pd.to_datetime(df["日付"])

    # 単位ごとにデータを集計
    if unit == "day":
        grouper = pd.Grouper(key="日付", freq="D")
    elif unit == "month":
        grouper = pd.Grouper(key="日付", freq="M")
    elif unit == "year":
        grouper = pd.Grouper(key="日付", freq="Y")
    else:
        raise ValueError("Invalid unit. Use 'day', 'month', or 'year'.")

    # 店舗IDごとにプロット
    unique_stores = df["店舗ID"].unique()
    for store_id in unique_stores:
        store_data = df[df["店舗ID"] == store_id]
        sales_by_store_category = (
            store_data.groupby(["店舗ID", "商品カテゴリ", grouper])["売上"]
            .sum()
            .reset_index()
        )

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        ax = sns.lineplot(
            x="日付",
            y="売上",
            hue="商品カテゴリ",
            data=sales_by_store_category,
            dashes=False,
        )

        # グラフの設定
        title = f"店舗ID {store_id} - カテゴリ別売り上げ ({unit}単位)"
        plt.title(title)
        plt.xlabel(unit.capitalize())
        plt.ylabel("売り上げ")
        plt.legend(title="商品カテゴリ", loc="upper left", bbox_to_anchor=(1, 1))

        if unit == "day":
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
            plt.xticks(rotation=45, ha="right")  # 45度傾けて表示
        plt.ylim(0, 2000000)
        plt.ticklabel_format(style="plain", axis="y")
        plt.grid()
        plt.show()


def plot_sales_by_category_foreach_and_store(df, store_id, agg_period="D"):
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
    df["日付"] = pd.to_datetime(df["日付"])

    # 指定した店舗IDのデータを抽出
    store_data = df[df["店舗ID"] == store_id]

    # 商品カテゴリごとにグラフを描画
    unique_categories = store_data["商品カテゴリ"].unique()

    # y軸の範囲を保存するリスト
    y_limits = []

    for category in unique_categories:
        category_data = store_data[store_data["商品カテゴリ"] == category]

        # 期間ごとにデータを集計
        pivot_table = pd.pivot_table(
            category_data,
            values="売上",
            index=pd.Grouper(key="日付", freq=agg_period),
            aggfunc="sum",
        )

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=pivot_table, dashes=False)

        # y軸の範囲を保存
        y_limits.append(plt.gca().get_ylim())

        # グラフの設定
        plt.title(
            f"店舗ID {store_id} - 商品カテゴリ: {category} 別売り上げ ({agg_period})"
        )
        plt.xlabel("日付")
        plt.ylabel("売り上げ")
        plt.legend(title="商品カテゴリ", loc="upper left", bbox_to_anchor=(1, 1))

        # y軸の範囲を設定（指定の値を採用）
        plt.ylim(0, 1500000)
        plt.ticklabel_format(style="plain", axis="y")

        # x軸の日付を設定
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
        plt.xticks(rotation=45, ha="right")  # 45度傾けて表示
        plt.grid

    # y軸の範囲を揃える
    min_y = min([y[0] for y in y_limits])
    max_y = max([y[1] for y in y_limits])
    plt.axis(ymin=min_y, ymax=max_y)
    plt.grid()

    plt.show()


def plot_sales_by_store_weekday(df, unit="day"):
    # 日付列をdatetime型に変換
    df["日付"] = pd.to_datetime(df["日付"])

    # 単位ごとにデータを集計
    if unit == "day":
        grouper = pd.Grouper(key="日付", freq="D")
    elif unit == "month":
        grouper = pd.Grouper(key="日付", freq="M")
    elif unit == "year":
        grouper = pd.Grouper(key="日付", freq="Y")
    else:
        raise ValueError("Invalid unit. Use 'day', 'month', or 'year'.")

    # 曜日ごとにプロット
    unique_stores = df["店舗ID"].unique()
    for store_id in unique_stores:
        store_data = df[df["店舗ID"] == store_id]
        total_sales_by_store = (
            store_data.groupby(["店舗ID", "曜日", grouper])["売上"].sum().reset_index()
        )

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        ax = sns.lineplot(
            x="曜日",
            y="売上",
            data=total_sales_by_store,
            label=f"店舗ID {store_id}",
            dashes=False,
        )

        # グラフの設定
        title = f"店舗ID {store_id} - 売り上げ合計推移 ({unit}単位)"
        plt.title(title)
        plt.xlabel("曜日")
        plt.ylabel("売り上げ")
        plt.legend(title="店舗ID", loc="upper left", bbox_to_anchor=(1, 1))

        plt.ylim(0, 12000000)
        plt.ticklabel_format(style="plain", axis="y")
        plt.grid()
        plt.show()

def plot_quantity_by_category_foreach_and_store(df, store_id, agg_period="D"):

    """
    指定した店舗IDの各商品カテゴリごとに、売上個数の時系列データをグラフに描画します。

    Parameters:
    - df (pd.DataFrame): 入力データフレーム
    - store_id (int): 対象の店舗ID
    - agg_period (str): 集計期間の指定 ('D': 日ごと, 'W': 週ごと, 'M': 月ごと)、デフォルトは 'D'

    Returns:
    None
    """

    # 日付列をdatetime型に変換
    df["日付"] = pd.to_datetime(df["日付"])

    # 指定した店舗IDのデータを抽出
    store_data = df[df["店舗ID"] == store_id]

    # 商品カテゴリごとにグラフを描画
    unique_categories = store_data["商品カテゴリ"].unique()

    # y軸の範囲を保存するリスト
    y_limits = []

    for category in unique_categories:
        category_data = store_data[store_data["商品カテゴリ"] == category]

        # 期間ごとにデータを集計
        pivot_table = pd.pivot_table(
            category_data,
            values="売上個数",  # ここを'売上'から'売上個数'に変更
            index=pd.Grouper(key="日付", freq=agg_period),
            aggfunc="sum",
        )

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=pivot_table, dashes=False)

        # y軸の範囲を保存
        y_limits.append(plt.gca().get_ylim())

        # グラフの設定
        plt.title(
            f"店舗ID {store_id} - 商品カテゴリ: {category} 別売上個数 ({agg_period})"
        )
        plt.xlabel("日付")
        plt.ylabel("売上個数")  # ここを'売上'から'売上個数'に変更
        plt.legend(title="商品カテゴリ", loc="upper left", bbox_to_anchor=(1, 1))

        # y軸の範囲を設定（指定の値を採用）
        plt.ylim(0, 1500)
        plt.ticklabel_format(style="plain", axis="y")

        # x軸の日付を設定
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
        plt.xticks(rotation=45, ha="right")  # 45度傾けて表示
        plt.grid()

def plot_sales_by_category_and_store_by_weekday(df, store_id, agg_period="D"):
    """
    指定した店舗IDの各商品カテゴリごとに、曜日ごとの売上の時系列データをグラフに描画します。

    Parameters:
    - df (pd.DataFrame): 入力データフレーム
    - store_id (int): 対象の店舗ID
    - agg_period (str): 集計期間の指定 ('D': 日ごと, 'W': 週ごと, 'M': 月ごと)、デフォルトは 'D'

    Returns:
    None
    """

    # 日付列をdatetime型に変換
    df["日付"] = pd.to_datetime(df["日付"])

    # 指定した店舗IDのデータを抽出
    store_data = df[df["店舗ID"] == store_id]

    # 商品カテゴリごとにグラフを描画
    unique_categories = store_data["商品カテゴリ"].unique()

    # y軸の範囲を保存するリスト
    y_limits = []

    for category in unique_categories:
        category_data = store_data[store_data["商品カテゴリ"] == category]

        # 期間ごとにデータを集計
        pivot_table = pd.pivot_table(
            category_data,
            values="売上",  # 売上個数から売上に変更
            index=category_data["日付"].dt.day_name(),
            aggfunc="sum",
        ).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=pivot_table, dashes=False)

        # y軸の範囲を保存
        y_limits.append(plt.gca().get_ylim())

        # グラフの設定
        plt.title(
            f"店舗ID {store_id} - 商品カテゴリ: {category} 別曜日ごとの売上 ({agg_period})"
        )
        plt.xlabel("曜日")
        plt.ylabel("売上")  # 売上個数から売上に変更
        plt.legend(title="商品カテゴリ", loc="upper left", bbox_to_anchor=(1, 1))

        # y軸の範囲を設定（指定の値を採用）
        plt.ylim(0, 1500)
        plt.ticklabel_format(style="plain", axis="y")

        # x軸の日付を設定
        plt.xticks(rotation=45, ha="right")  # 45度傾けて表示
        plt.grid()

def plot_quantity_by_category_and_store_by_weekday(df, store_id, agg_period="D"):
    """
    指定した店舗IDの各商品カテゴリごとに、曜日ごとの売上個数の時系列データをグラフに描画します。

    Parameters:
    - df (pd.DataFrame): 入力データフレーム
    - store_id (int): 対象の店舗ID
    - agg_period (str): 集計期間の指定 ('D': 日ごと, 'W': 週ごと, 'M': 月ごと)、デフォルトは 'D'

    Returns:
    None
    """

    # 日付列をdatetime型に変換
    df["日付"] = pd.to_datetime(df["日付"])

    # 指定した店舗IDのデータを抽出
    store_data = df[df["店舗ID"] == store_id]

    # 商品カテゴリごとにグラフを描画
    unique_categories = store_data["商品カテゴリ"].unique()

    # y軸の範囲を保存するリスト
    y_limits = []

    for category in unique_categories:
        category_data = store_data[store_data["商品カテゴリ"] == category]

        # 期間ごとにデータを集計
        pivot_table = pd.pivot_table(
            category_data,
            values="売上個数",
            index=category_data["日付"].dt.day_name(),
            aggfunc="sum",
        ).reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=pivot_table, dashes=False)

        # y軸の範囲を保存
        y_limits.append(plt.gca().get_ylim())

        # グラフの設定
        plt.title(
            f"店舗ID {store_id} - 商品カテゴリ: {category} 別曜日ごとの売上個数 ({agg_period})"
        )
        plt.xlabel("曜日")
        plt.ylabel("売上個数")
        plt.legend(title="商品カテゴリ", loc="upper left", bbox_to_anchor=(1, 1))

        # y軸の範囲を設定（指定の値を採用）
        plt.ylim(0, 1500)
        plt.ticklabel_format(style="plain", axis="y")

        # x軸の日付を設定
        plt.xticks(rotation=45, ha="right")  # 45度傾けて表示
        plt.grid()

