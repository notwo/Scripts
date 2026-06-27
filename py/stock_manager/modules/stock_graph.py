import csv
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TypeAlias

import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from modules.logger import Logger
from modules.util import Util

StockByDay: TypeAlias = tuple[str, str, str, int | float]


@dataclass(slots=True)
class StockData:
    date: str
    code: str
    code_name: str
    country: str
    price: float


# グラフの日本語文字フォント設定
plt.rcParams["font.family"] = "Yu Gothic"


class StockGraph:
    def __init__(self, filename: str) -> None:
        try:
            self.config = Util.load_config(filename)
        except FileNotFoundError:
            print(f"設定ファイルが存在しません: {filename}")
        except UnicodeDecodeError:
            print(f"設定ファイルの文字コードがUTF-8ではありません: {filename}")
        except Exception as e:
            print(f"設定ファイルの読み込みに失敗しました: {filename}")

        self.logger = Logger.get_logger(
            log_dir=self.config["log"]["filepath"],
            logfile=self.config["log"]["filename"],
            reload=True
        )

    def _create_country_graph(
        self,
        df: pd.DataFrame,
        country: str,
        output_file: str
    ) -> None:

        country_df = df[df["国"] == country]

        if country_df.empty:
            self.logger.warning(
                f"{country} のデータがありません"
            )
            return

        # 日時型に変換
        country_df = country_df.copy()
        country_df["日時"] = (
            pd.to_datetime(country_df["日時"])
            .dt.normalize()
        )

        pivot_df = country_df.pivot_table(
            index="日時",
            columns="銘柄",
            values="株価",
            aggfunc="last"
        )

        pivot_df = pivot_df.sort_index()

        fig, sub_ax = plt.subplots(figsize=(10, 5))

        # 横方向の点線グリッド
        sub_ax.grid(
            axis='y',       # y軸目盛りに合わせる
            linestyle='--', # 点線
            linewidth=0.5
        )

        for column in pivot_df.columns:
            sub_ax.plot(
                pivot_df.index,
                pivot_df[column],
                marker="o",
                label=column
            )

        sub_ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%m/%d")
        )

        sub_ax.xaxis.set_major_locator(
            mdates.DayLocator(interval=1)
        )

        # グラフの装飾
        sub_ax.set_title(
            "日本株推移" if country == "ja"
            else "米国株推移"
        )

        sub_ax.set_xlabel("日付")

        sub_ax.set_ylabel(
            "株価(￥)" if country == "ja"
            else "株価(＄)"
        )

        sub_ax.legend(
            fontsize=7,
        )
        fig.tight_layout()

        # PDF出力
        self.logger.info("PDF出力")

        with PdfPages(output_file) as pdf:
            pdf.savefig(fig)
            plt.close(fig)

    def create_graph_on_pdf(
        self,
        stocks_by_day: list[StockByDay]
    ) -> None:

        self.logger.info("グラフ作成開始")

        df = pd.DataFrame(
            stocks_by_day,
            columns=self.config["pdf"]["header"]
        )

        df["日時"] = pd.to_datetime(df["日付"])

        self._create_country_graph(
            df,
            "ja",
            f'{self.config["pdf"]["filepath"]}/日本株チャート.pdf'
        )

        self._create_country_graph(
            df,
            "us",
            f'{self.config["pdf"]["filepath"]}/米国株チャート.pdf'
        )

        self.logger.info("グラフ作成終了")

    def format_array_from_csv(self) -> list[StockByDay]:
        self.logger.info("株価ロード開始")
        file_path = f'{self.config["csv"]["filepath"]}/{self.config["csv"]["filename"]}'

        stocks = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    stock = StockData(
                        date=row["日時"],
                        code=row["銘柄コード"],
                        code_name=row["銘柄名"],
                        country=row["国"],
                        price=float(row["株価(円)"]),
                    )
                    stocks.append(stock)

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
            date = stock.date.split(" ")[0]
            code = (
                f"{stock.code}({stock.code_name})"
            )
            price = stock.price

            country = stock.country
            new_arr.append([
                date,
                code,
                country,
                price
            ])

        # データ全体を日時でソート
        new_arr.sort(
            key=lambda x: datetime.strptime(x[0], "%Y/%m/%d")
        )

        # pandasで頭2つの要素(日時,銘柄コード)から重複を削除
        df = pd.DataFrame(
            new_arr,
            columns=["Date", "Code", "Country", "Price"]
        )
        df = df.drop_duplicates(
            subset=["Date", "Code"]
        )
        stocks_by_day = df.values.tolist()

        self.logger.info("データ整形終了")

        return stocks_by_day
