from unittest.mock import MagicMock, Mock, call, mock_open, patch

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


@patch("modules.stock_graph.PdfPages")
@patch.object(StockGraph, "_create_graph")
def test_create_graph(mock_create, mock_pdf):

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

    fig = MagicMock()
    mock_create.return_value = fig

    stocks = [
        ["2025/01/01", "AAPL(Apple)", "us", 200, "IT"],
        ["2025/02/01", "AAPL(Apple)", "us", 210, "IT"],
        ["2025/01/01", "7203(トヨタ)", "ja", 3000, "工業"],
        ["2025/02/01", "7203(トヨタ)", "ja", 3050, "工業"],
    ]

    pdf_instance = mock_pdf.return_value.__enter__.return_value

    graph.create_graph_on_pdf(stocks)

    # PDFはカテゴリごとに2ファイル
    assert mock_pdf.call_count == 2

    mock_pdf.assert_has_calls([
        call("pdf/ja_工業.pdf"),
        call("pdf/us_IT.pdf")
    ], any_order=True)

    # 月ごとに4ページ保存
    assert pdf_instance.savefig.call_count == 4

    # 月ごとにグラフ作成
    assert mock_create.call_count == 4
