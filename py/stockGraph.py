import csv
import os
import sys
from datetime import datetime
from enum import Enum
from tkinter import Tk, messagebox

import japanize_matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


class StockDataRow(Enum):
    DATE = 0
    CODE = 1
    CODE_NAME = 2
    PRICE = 3


def create_graph_on_pdf(stocks_by_day):
    # データをDataFrameに変換
    df = pd.DataFrame(stocks_by_day, columns=["日付", "銘柄", "株価"])

    # 日付をdatetime型に変換
    df["Date"] = pd.to_datetime(df["日付"])

    # 折れ線グラフを作成
    plt.figure(figsize=(8, 6))
    for category, group in df.groupby("銘柄"):
        plt.plot(group["日付"], group["株価"], marker="o", label=category)

    # グラフの装飾
    plt.title("銘柄ごと株価推移")
    plt.xlabel("日付")
    plt.ylabel("株価")
    plt.legend(title="銘柄")
    plt.grid(False)
    plt.tight_layout()
    # plt.show() # グラフを即時描画

    # PDF出力
    start_datetime = stocks_by_day[0][StockDataRow.DATE.value].replace("/", "")
    end_datetime = stocks_by_day[len(stocks_by_day) - 1][
        StockDataRow.DATE.value
    ].replace("/", "")
    with PdfPages(f"株価チャート_{start_datetime}_{end_datetime}.pdf") as pdf:
        pdf.savefig()  # 現在のプロットをPDFに保存
        plt.close()


def format_array_from_csv():
    file_path = "stocks.csv"
    if not os.path.exists(file_path):
        messagebox.showinfo(
            "ファイル未存在エラー",
            f"stockGraph.exeと同フォルダに株価リスト({file_path})が存在しません",
        )
        sys.exit()

    stocks = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            stocks.append(row)
            if not row:
                break

    new_arr = []
    for stock in stocks:
        date = stock[StockDataRow.DATE.value].split(" ")[0]
        code = (
            f"{stock[StockDataRow.CODE.value]}({stock[StockDataRow.CODE_NAME.value]})"
        )
        price = int(stock[StockDataRow.PRICE.value])
        new_arr.append([date, code, price])

    # データ全体を日付でソート
    new_arr.sort(
        key=lambda x: datetime.strptime(x[StockDataRow.DATE.value], "%Y/%m/%d")
    )

    # pandasで頭2つの要素(日時,銘柄コード)から重複を削除
    df = pd.DataFrame(new_arr, columns=["A", "B", "C"])
    df = df.drop_duplicates(subset=["A", "B"])
    stocks_by_day = df.values.tolist()

    return stocks_by_day


# entry point
stocks_by_day = format_array_from_csv()
create_graph_on_pdf(stocks_by_day)
