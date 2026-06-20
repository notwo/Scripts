from unittest.mock import Mock, mock_open, patch

import pandas as pd

from modules.stock_graph import StockGraph


@patch("builtins.open", new_callable=mock_open)
def test_format_array_from_csv(mock_file):

    csv_data = """日付,コード,銘柄名,国,株価
2025/01/02 10:00:00,7203,トヨタ,ja,3000
2025/01/01 10:00:00,AAPL,Apple,us,200
2025/01/02 11:00:00,7203,トヨタ,ja,3000
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
            ["2025/01/01", "AAPL(Apple)", "us", 200],
            ["2025/01/02", "7203(トヨタ)", "ja", 3000]
        ]


@patch.object(StockGraph, "_create_country_graph")
def test_create_graph_on_pdf(mock_create):

    graph = StockGraph.__new__(StockGraph)

    graph.logger = Mock()

    graph.config = {
        "pdf": {
            "header": [
                "日付",
                "銘柄",
                "国",
                "株価"
            ],
            "filepath": "pdf"
        }
    }

    stocks = [
        ["2025/01/01", "AAPL(Apple)", "us", 200],
        ["2025/01/01", "7203(トヨタ)", "ja", 3000]
    ]

    graph.create_graph_on_pdf(stocks)

    assert mock_create.call_count == 2

    mock_create.assert_any_call(
        mock_create.call_args_list[0][0][0],
        "ja",
        "pdf/日本株チャート.pdf"
    )

    mock_create.assert_any_call(
        mock_create.call_args_list[1][0][0],
        "us",
        "pdf/米国株チャート.pdf"
    )


def test_create_country_graph_empty():

    graph = StockGraph.__new__(StockGraph)

    graph.logger = Mock()

    df = pd.DataFrame(
        columns=["日付", "銘柄", "国", "株価"]
    )

    graph._create_country_graph(
        df,
        "ja",
        "dummy.pdf"
    )

    graph.logger.warning.assert_called_once()


@patch("modules.stock_graph.PdfPages")
@patch("modules.stock_graph.plt")
def test_create_country_graph(
    mock_plt,
    mock_pdf_pages
):

    graph = StockGraph.__new__(StockGraph)

    graph.logger = Mock()

    df = pd.DataFrame([
        [
            "2025/01/01",
            "AAPL(Apple)",
            "us",
            200
        ]
    ], columns=[
        "日付",
        "銘柄",
        "国",
        "株価"
    ])

    graph._create_country_graph(
        df,
        "us",
        "us.pdf"
    )

    mock_plt.figure.assert_called_once()
    mock_plt.plot.assert_called_once()
    mock_plt.title.assert_called_once()
