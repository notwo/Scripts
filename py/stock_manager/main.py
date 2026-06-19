from modules.stock_getter import StockGetter
from modules.stock_graph import StockGraph


def main():
    # 株価取得
    stock_getter = StockGetter("config/setting.yml")
    numbers_and_prices = stock_getter.detect_stock_price()
    stock_getter.file_to_csv(numbers_and_prices)

    # グラフ作成
    stock_graph = StockGraph("config/setting.yml")
    stocks_by_day = stock_graph.format_array_from_csv()
    stock_graph.create_graph_on_pdf(stocks_by_day)


if __name__ == "__main__":
    main()
