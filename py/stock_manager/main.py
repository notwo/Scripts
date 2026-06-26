import os

from modules.mail_sender import MailSender
from modules.stock_getter import StockGetter
from modules.stock_graph import StockGraph

CONFIG_FILE = "config/setting.yml"


def main():
    # 株価取得
    stock_getter = StockGetter(CONFIG_FILE)
    numbers_and_prices = stock_getter.detect_stock_price()
    stock_getter.file_to_csv(numbers_and_prices)

    # グラフ作成
    stock_graph = StockGraph(CONFIG_FILE)
    stocks_by_day = stock_graph.format_array_from_csv()
    stock_graph.create_graph_on_pdf(stocks_by_day)

    password = os.environ.get("MAIL_PASSWORD", "")
    sender = os.environ.get("SENDER", "")
    tos = [os.environ.get("TO", "")]

    # メール送信
    mail = MailSender(sender, password, tos, CONFIG_FILE)
    mail.send_mail(
        body="株価レポートを送付します。",
        attachment_files=[
            "dist/日本株チャート.pdf",
            "dist/米国株チャート.pdf"
        ]
    )


if __name__ == "__main__":
    main()
