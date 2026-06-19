import csv
from datetime import datetime
from enum import Enum
from typing import TypeAlias

import japanize_matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from modules.logger import Logger
from modules.util import Util


StockByDay: TypeAlias = tuple[str, str, int | float]


class StockDataRow(Enum):
    DATE = 0
    CODE = 1
    CODE_NAME = 2
    PRICE = 3


class StockGraph:
    def __init__(self, filename: str) -> None:
        try:
            self.config = Util.load_config(filename)
        except FileNotFoundError:
            self.logger.error(f"設定ファイルが存在しません: {filename}")
        except UnicodeDecodeError:
            self.logger.error(f"設定ファイルの文字コードがUTF-8ではありません: {filename}")
        except Exception:
            self.logger.exception(f"設定ファイルの読み込みに失敗しました: {filename}")

        self.logger = Logger.get_logger(
            self.config["log"]["filepath"],
            self.config["log"]["filename"])

    def create_graph_on_pdf(self, stocks_by_day: list[StockByDay]) -> None:
        self.logger.info("グラフ作成開始")

        # データをDataFrameに変換
        df = pd.DataFrame(stocks_by_day, columns=self.config["pdf"]["header"])

        # 日付をdatetime型に変換
        df["Date"] = pd.to_datetime(df["日付"])

        # 折れ線グラフを作成
        plt.figure(figsize=(8, 6))
        for category, group in df.groupby("銘柄"):
            plt.plot(group["日付"], group["株価"], marker="o", label=category)

        # グラフの装飾
        plt.title("銘柄ごと株価推移")
        plt.xlabel("日付")
        plt.ylabel("株価(￥)")
        plt.legend(title="銘柄")
        plt.grid(False)
        plt.xticks(fontsize=6.5)  # X軸の目盛りのフォントサイズ
        plt.tight_layout()

        # PDF出力
        self.logger.info("PDF出力")
        start_datetime = stocks_by_day[0][StockDataRow.DATE.value].replace("/", "")
        end_datetime = stocks_by_day[len(stocks_by_day) - 1][
            StockDataRow.DATE.value
        ].replace("/", "")
        with PdfPages(f'{self.config["pdf"]["filepath"]}/株価チャート_{start_datetime}_{end_datetime}.pdf') as pdf:
            pdf.savefig()  # 現在のプロットをPDFに保存
            plt.close()

        self.logger.info("グラフ作成終了")

    def format_array_from_csv(self) -> list[StockByDay]:
        self.logger.info("株価ロード開始")
        file_path = f'{self.config["csv"]["filepath"]}/{self.config["csv"]["filename"]}'

        stocks = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)

                for row in reader:
                    stocks.append(row)
                    if not row:
                        break
        except FileNotFoundError:
            self.logger.error(f"CSVファイルが存在しません: {file_path}")
        except UnicodeDecodeError:
            self.logger.error(f"CSVファイルの文字コードがUTF-8ではありません: {file_path}")
        except Exception:
            self.logger.exception(f"CSVファイルの読み込みに失敗しました: {file_path}")

        self.logger.info("株価ロード終了")

        self.logger.info("データ整形開始")
        new_arr = []
        for stock in stocks:
            date = stock[StockDataRow.DATE.value].split(" ")[0]
            code = (
                f"{stock[StockDataRow.CODE.value]}({stock[StockDataRow.CODE_NAME.value]})"
            )
            price_text = stock[StockDataRow.PRICE.value]
            if "." in price_text:
                price = float(price_text)
            else:
                price = int(price_text)
            new_arr.append([date, code, price])

        # データ全体を日付でソート
        new_arr.sort(
            key=lambda x: datetime.strptime(x[StockDataRow.DATE.value], "%Y/%m/%d")
        )

        # pandasで頭2つの要素(日時,銘柄コード)から重複を削除
        df = pd.DataFrame(new_arr, columns=["A", "B", "C"])
        df = df.drop_duplicates(subset=["A", "B"])
        stocks_by_day = df.values.tolist()

        self.logger.info("データ整形終了")

        return stocks_by_day
