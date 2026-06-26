import os

from modules.mail_sender import MailSender
from modules.stock_getter import StockGetter
from modules.stock_graph import StockGraph


class StockService:

    def __init__(self, config_file: str) -> None:
        self.config_file = config_file

    def execute(self) -> None:
        # 株価取得
        stock_getter = StockGetter(self.config_file)
        numbers_and_prices = stock_getter.detect_stock_price()
        stock_getter.file_to_csv(numbers_and_prices)

        # グラフ作成
        stock_graph = StockGraph(self.config_file)
        stocks_by_day = stock_graph.format_array_from_csv()
        stock_graph.create_graph_on_pdf(stocks_by_day)

        # メール送信
        password = os.getenv("MAIL_PASSWORD", "")
        sender = os.getenv("SENDER", "")
        tos = [os.getenv("TO", "")]

        mail = MailSender(
            sender=sender,
            password=password,
            tos=tos,
            filename=self.config_file
        )

        mail.send_mail(
            body="株価レポートを送付します。",
            attachment_files=[
                "dist/日本株チャート.pdf",
                "dist/米国株チャート.pdf"
            ]
        )
