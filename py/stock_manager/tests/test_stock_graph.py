from unittest.mock import Mock, mock_open, patch

from modules.stock_graph import StockGraph


def test_format_array_from_csv():
    csv_data = """日時,銘柄コード,銘柄名,国,株価(円),カテゴリ
2025/01/02 10:00:00,7203,トヨタ,ja,3000,工業
2025/01/01 10:00:00,AAPL,Apple,us,200,IT
2025/01/02 11:00:00,7203,トヨタ,ja,3000,工業
"""

    m = mock_open(read_data=csv_data)

    with patch("builtins.open", m):

        getter = StockGraph.__new__(StockGraph)

        getter.logger = Mock()

        getter.config = {
            "csv": {
                "filepath": ".",
                "filename": "stock.csv"
            }
        }

        result = getter.format_array_from_csv()

        assert result == [
            ["2025/01/01", "AAPL(Apple)", "us", 200, "IT"],
            ["2025/01/02", "7203(トヨタ)", "ja", 3000, "工業"]
        ]


@patch.object(StockGraph, "_create_graph")
def test_create_graph(mock_create):

    graph = StockGraph.__new__(StockGraph)

    graph.logger = Mock()

    graph.config = {
        "pdf": {
            "header": [
                "日付",
                "銘柄",
                "国",
                "株価",
                "カテゴリ"
            ],
            "filepath": "pdf"
        }
    }

    stocks = [
        ["2025/01/01", "AAPL(Apple)", "us", 200, "IT"],
        ["2025/01/01", "7203(トヨタ)", "ja", 3000, "工業"],
        ["2025/02/01", "AAPL(Apple)", "us", 210, "IT"],
        ["2025/02/01", "7203(トヨタ)", "ja", 3050, "工業"],
    ]

    graph.create_graph_on_pdf(stocks)

    assert mock_create.call_count == 4

    actual = {
        (args.args[1], args.args[2], args.args[3])
        for args in mock_create.call_args_list
    }

    expected = {
        ("ja", "工業", "pdf/ja_工業_202501.pdf"),
        ("ja", "工業", "pdf/ja_工業_202502.pdf"),
        ("us", "IT", "pdf/us_IT_202501.pdf"),
        ("us", "IT", "pdf/us_IT_202502.pdf"),
    }

    assert actual == expected
