import japanize_matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import numpy as np

japanize_matplotlib.japanize()


def plot_total_sales_by_store(df, unit="day"):
    # 日付列をdatetime型に変換
    df["日付"] = pd.to_datetime(df["日付"])

    # 単位ごとにデータを集計
    if unit == "day":
        grouper = pd.Grouper(key="日付", freq="D")
        y_limit = 2000000  # 日ごとのy軸範囲
    elif unit == "month":
        grouper = pd.Grouper(key="日付", freq="M")
        y_limit = 10000000  # 月ごとのy軸範囲
    elif unit == "year":
        grouper = pd.Grouper(key="日付", freq="Y")
        y_limit = 100000000  # 年ごとのy軸範囲
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
        plt.ylim(0, y_limit)  # y軸範囲の設定
        plt.ticklabel_format(style="plain", axis="y")
        plt.grid()
        plt.show()


def plot_sales_by_store_category(df, unit="day"):
    # 日付列をdatetime型に変換
    df["日付"] = pd.to_datetime(df["日付"])

    # 単位ごとにデータを集計
    if unit == "day":
        grouper = pd.Grouper(key="日付", freq="D")
        y_limit = 1000000
    elif unit == "month":
        grouper = pd.Grouper(key="日付", freq="M")
        y_limit = 5000000
    elif unit == "year":
        grouper = pd.Grouper(key="日付", freq="Y")
        y_limit = 20000000
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
        plt.ylim(0, y_limit)
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

    # 商品カテゴリごとにグラフを描画するためのデータをまとめる
    plot_data = []

    for category in store_data["商品カテゴリ"].unique():
        category_data = store_data[store_data["商品カテゴリ"] == category]
        pivot_table = pd.pivot_table(
            category_data,
            values="売上",
            index=pd.Grouper(key="日付", freq=agg_period),
            aggfunc="sum",
        )
        plot_data.append((category, pivot_table))

    # グラフのプロット
    plt.figure(figsize=(12, 8))

    for category, data in plot_data:
        sns.lineplot(data=data["売上"], label=f"商品カテゴリ: {category}", dashes=False)

    # グラフの設定
    plt.title(f"店舗ID {store_id} - 商品カテゴリ別売り上げ ({agg_period})")
    plt.xlabel("日付")
    plt.ylabel("売り上げ")
    plt.legend(title="商品カテゴリ", loc="upper left", bbox_to_anchor=(1, 1))

    # y軸の範囲を設定
    plt.ylim(0, max(data["売上"].max() for _, data in plot_data) * 1.1)
    plt.ticklabel_format(style="plain", axis="y")

    # x軸の日付を設定
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
    plt.xticks(rotation=45, ha="right")  # 45度傾けて表示
    plt.grid()

    plt.show()


def plot_sales_by_store_yearly(df):
    """
    年ごとに店舗IDごとの曜日ごとの売り上げ合計を可視化する関数。

    Parameters:
    - df (pd.DataFrame): 時系列データが格納されたDataFrame。

    Returns:
    None (グラフが表示されるのみ)
    """

    # 日付列をdatetime型に変換
    df["日付"] = pd.to_datetime(df["日付"])

    # 年ごとにプロット
    unique_stores = df["店舗ID"].unique()
    for store_id in unique_stores:
        # 対象店舗のデータを抽出
        store_data = df[df["店舗ID"] == store_id]

        # 年ごとに曜日ごとの売上を合計
        total_sales_by_store = (
            store_data.groupby(["店舗ID", store_data["日付"].dt.year, "曜日"])["売上"].sum().reset_index()
        )

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        ax = sns.lineplot(
            x="曜日",
            y="売上",
            hue="日付",
            data=total_sales_by_store,
            label=f"店舗ID {store_id}",
            dashes=False,
        )

        # グラフの設定
        title = f"店舗ID {store_id} - 年ごとの曜日ごとの売り上げ合計推移"
        plt.title(title)
        plt.xlabel("曜日")
        plt.ylabel("売り上げ")
        plt.legend(title="年", loc="upper left", bbox_to_anchor=(1, 1))

        # y軸範囲の設定（適宜調整する）
        plt.ylim(0, 20000000)

        # y軸の表示フォーマット指定
        plt.ticklabel_format(style="plain", axis="y")

        # グリッド表示
        plt.grid()

        # グラフの表示
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

    # 商品カテゴリごとにグラフを描画するためのデータをまとめる
    plot_data = []

    for category in store_data["商品カテゴリ"].unique():
        category_data = store_data[store_data["商品カテゴリ"] == category]
        pivot_table = pd.pivot_table(
            category_data,
            values="売上個数",
            index=pd.Grouper(key="日付", freq=agg_period),
            aggfunc="sum",
        )
        plot_data.append((category, pivot_table))

    # グラフのプロット
    plt.figure(figsize=(12, 8))

    # y軸の範囲を設定
    if agg_period == "D":
        y_limit = 200
    elif agg_period == "W":
        y_limit = 500
    elif agg_period == "M":
        y_limit = 5000
    else:
        raise ValueError("Invalid agg_period. Use 'D', 'W', or 'M'.")

    for category, data in plot_data:
        sns.lineplot(
            data=data["売上個数"], label=f"商品カテゴリ: {category}", dashes=False
        )

    # グラフの設定
    plt.title(f"店舗ID {store_id} - 商品カテゴリ別売上個数 ({agg_period})")
    plt.xlabel("日付")
    plt.ylabel("売上個数")
    plt.legend(title="商品カテゴリ", loc="upper left", bbox_to_anchor=(1, 1))

    plt.ylim(0, y_limit)  # y軸範囲を指定
    plt.ticklabel_format(style="plain", axis="y")

    # x軸の日付を設定
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
    plt.xticks(rotation=45, ha="right")  # 45度傾けて表示
    plt.grid()

    plt.show()


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

    # 商品カテゴリごとにグラフを描画するためのデータをまとめる
    plot_data = []

    for category in store_data["商品カテゴリ"].unique():
        category_data = store_data[store_data["商品カテゴリ"] == category]
        pivot_table = pd.pivot_table(
            category_data,
            values="売上",
            index=category_data["日付"].dt.day_name(),
            aggfunc="sum",
        ).reindex(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )
        plot_data.append((category, pivot_table))

    # グラフのプロット
    plt.figure(figsize=(12, 8))

    # 曜日ごとに適した y_limit を設定
    if agg_period == "D":
        y_limit = 1500  # 日ごとの場合の y_limit
    elif agg_period == "W":
        y_limit = 7000  # 週ごとの場合の y_limit
    elif agg_period == "M":
        y_limit = 30000  # 月ごとの場合の y_limit
    else:
        raise ValueError("Invalid agg_period. Use 'D', 'W', or 'M'.")

    # y軸の範囲を初期化
    y_limits = [y_limit]

    for category, data in plot_data:
        sns.lineplot(data=data["売上"], label=f"商品カテゴリ: {category}", dashes=False)

        # 曜日ごとの適した y_limit を設定
        if agg_period == "D":
            y_limit = 150000
        elif agg_period == "W":
            y_limit = 700000
        elif agg_period == "M":
            y_limit = 10000000

        # y軸の範囲を保存
        y_limits.append(y_limit)

    # グラフの設定
    plt.title(f"店舗ID {store_id} - 商品カテゴリ別曜日ごとの売上 ({agg_period})")
    plt.xlabel("曜日")
    plt.ylabel("売上")
    plt.legend(title="商品カテゴリ", loc="upper left", bbox_to_anchor=(1, 1))

    # y軸の範囲を揃える
    min_y = min(y_limits)
    max_y = max(y_limits)
    plt.ylim(0, max_y)
    plt.ticklabel_format(style="plain", axis="y")

    # x軸の日付を設定
    plt.xticks(rotation=45, ha="right")  # 45度傾けて表示
    plt.grid()

    plt.show()


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

    # 商品カテゴリごとにグラフを描画するためのデータをまとめる
    plot_data = []

    for category in store_data["商品カテゴリ"].unique():
        category_data = store_data[store_data["商品カテゴリ"] == category]
        pivot_table = pd.pivot_table(
            category_data,
            values="売上個数",
            index=category_data["日付"].dt.day_name(),
            aggfunc="sum",
        ).reindex(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )
        plot_data.append((category, pivot_table))

    # グラフのプロット
    plt.figure(figsize=(12, 8))

    # 曜日ごとに適した y_limit を設定
    if agg_period == "D":
        y_limit = 1500  # 日ごとの場合の y_limit
    elif agg_period == "W":
        y_limit = 7000  # 週ごとの場合の y_limit
    elif agg_period == "M":
        y_limit = 12000  # 月ごとの場合の y_limit
    else:
        raise ValueError("Invalid agg_period. Use 'D', 'W', or 'M'.")

    # y軸の範囲を初期化
    y_limits = [y_limit]

    for category, data in plot_data:
        sns.lineplot(
            data=data["売上個数"], label=f"商品カテゴリ: {category}", dashes=False
        )

        # 曜日ごとの適した y_limit を設定
        if agg_period == "D":
            y_limit = 1500
        elif agg_period == "W":
            y_limit = 7000
        elif agg_period == "M":
            y_limit = 30000

        # y軸の範囲を保存
        y_limits.append(y_limit)

    # グラフの設定
    plt.title(f"店舗ID {store_id} - 商品カテゴリ別曜日ごとの売上個数 ({agg_period})")
    plt.xlabel("曜日")
    plt.ylabel("売上個数")
    plt.legend(title="商品カテゴリ", loc="upper left", bbox_to_anchor=(1, 1))

    # y軸の範囲を揃える
    min_y = min(y_limits)
    max_y = max(y_limits)
    plt.ylim(0, max_y)
    plt.ticklabel_format(style="plain", axis="y")

    # x軸の日付を設定
    plt.xticks(rotation=45, ha="right")  # 45度傾けて表示
    plt.grid()

    plt.show()


def plot_detrended_sales_by_store(df, unit="day", window_size=7, moving_average_type="simple"):
    """
    概要:
        指定された店舗ごとに、移動平均を除去した売上データの推移をプロットします。

    パラメータ:
        - df (pd.DataFrame): 時系列データが格納されたDataFrame。列には '日付', '店舗ID', '売上' が含まれている必要があります。
        - unit (str, optional): 'day', 'month', 'year' のいずれか。データを集計する単位を指定します。デフォルトは 'day' です。
        - window_size (int, optional): 移動平均の窓サイズ。デフォルトは 7 です。
        - moving_average_type (str, optional): 使用する移動平均の種類。'simple'（単純移動平均）、'exponential'（指数移動平均）、'weighted'（加重移動平均）のいずれかを指定します。デフォルトは 'simple' です。

    戻り値:
        なし。プロットが表示されます。
    """
    # 日付列をdatetime型に変換
    df["日付"] = pd.to_datetime(df["日付"])

    # 単位ごとにデータを集計
    if unit == "day":
        grouper = pd.Grouper(key="日付", freq="D")
        y_limit = 1000000  # 日ごとのy軸範囲
    elif unit == "month":
        grouper = pd.Grouper(key="日付", freq="M")
        y_limit = 10000000  # 月ごとのy軸範囲
    elif unit == "year":
        grouper = pd.Grouper(key="日付", freq="Y")
        y_limit = 50000000  # 年ごとのy軸範囲
    else:
        raise ValueError("Invalid unit. Use 'day', 'month', or 'year'.")

    # 店舗IDごとにプロット
    unique_stores = df["店舗ID"].unique()
    for store_id in unique_stores:
        store_data = df[df["店舗ID"] == store_id]
        total_sales_by_store = (
            store_data.groupby(["店舗ID", grouper])["売上"].sum().reset_index()
        )

        # 移動平均の計算
        if moving_average_type == "simple":
            total_sales_by_store["移動平均"] = total_sales_by_store["売上"].rolling(window=window_size).mean()
        elif moving_average_type == "exponential":
            total_sales_by_store["移動平均"] = total_sales_by_store["売上"].ewm(span=window_size, adjust=False).mean()
        elif moving_average_type == "weighted":
            weights = np.arange(1, window_size + 1)
            total_sales_by_store["移動平均"] = total_sales_by_store["売上"].rolling(window=window_size).apply(lambda x: np.average(x, weights=weights))
        else:
            raise ValueError("Invalid moving_average_type. Use 'simple', 'exponential', or 'weighted'.")

        # 移動平均を除去
        total_sales_by_store["売上除去移動平均"] = total_sales_by_store["売上"] - total_sales_by_store["移動平均"]

        # グラフのプロット
        plt.figure(figsize=(12, 8))
        ax = sns.lineplot(
            x="日付",
            y="売上除去移動平均",
            data=total_sales_by_store,
            label=f"店舗ID {store_id}",
            dashes=False,
        )

        # グラフの設定
        title = f"店舗ID {store_id} - 移動平均を除去した売り上げ合計推移 ({unit}単位)"
        plt.title(title)
        plt.xlabel(unit.capitalize())
        plt.ylabel("売り上げ")
        plt.legend(title="店舗ID", loc="upper left", bbox_to_anchor=(1, 1))

        if unit == "day":
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y/%m/%d"))
            plt.xticks(rotation=45, ha="right")  # 45度傾けて表示
        plt.ylim(-y_limit, y_limit)  # y軸範囲の設定
        plt.ticklabel_format(style="plain", axis="y")
        plt.grid()
        plt.show()