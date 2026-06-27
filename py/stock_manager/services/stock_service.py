import os

from modules.mail_sender import MailSender
from modules.stock_getter import StockGetter
from modules.stock_graph import StockGraph
from modules.util import Util


class StockService:

    def __init__(self, config_file_path: str) -> None:
        self.config_file_path = config_file_path
        filename = f"{self.config_file_path}/system.yml"
        try:
            self.config = Util.load_config(filename)
        except FileNotFoundError:
            print(f"設定ファイルが存在しません: {filename}")
        except UnicodeDecodeError:
            print(f"設定ファイルの文字コードがUTF-8ではありません: {filename}")
        except Exception:
            print(f"設定ファイルの読み込みに失敗しました: {filename}")

    def execute(self) -> None:
        # 株価取得
        if self.config["mode"]["csv"]:
            stock_getter = StockGetter(f"{self.config_file_path}/stock_getter.yml")
            numbers_and_prices = stock_getter.detect_stock_price()
            stock_getter.file_to_csv(numbers_and_prices)

        # グラフ作成
        if self.config["mode"]["pdf"]:
            stock_graph = StockGraph(f"{self.config_file_path}/stock_graph.yml")
            stocks_by_day = stock_graph.format_array_from_csv()
            stock_graph.create_graph_on_pdf(stocks_by_day)

        # メール送信
        if self.config["mode"]["mail"]:
            password = os.getenv("MAIL_PASSWORD", "")
            sender = os.getenv("SENDER", "")
            tos = [os.getenv("TO", "")]

            mail = MailSender(
                sender=sender,
                password=password,
                tos=tos,
                filename=f"{self.config_file_path}/mail_sender.yml"
            )

            mail.send_mail(
                body="株価レポートを送付します。",
                attachment_files=[
                    "dist/日本株チャート.pdf",
                    "dist/米国株チャート.pdf"
                ]
            )
