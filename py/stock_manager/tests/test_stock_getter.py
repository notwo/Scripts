from unittest.mock import Mock, mock_open, patch

from modules.stock_getter import StockGetter


@patch("modules.stock_getter.sync_playwright")
def test_detect_stock_price_ja(mock_playwright):
    getter = StockGetter.__new__(StockGetter)
    getter.logger = Mock()

    getter.config = {
        "browser": {
            "headless_mode": True
        },
        "base_url": "https://finance.yahoo.co.jp/quote"
    }
    getter.stocks = [
        {
            "name": "トヨタ",
            "code": "7203",
            "country": "ja"
        }
    ]

    mock_page = Mock()
    mock_company_locator = Mock()
    mock_company_locator.inner_text.return_value = "トヨタ自動車(株)"

    mock_price_locator = Mock()
    mock_price_locator.first.inner_text.return_value = "2,850"

    mock_page.locator.side_effect = [
        Mock(
            filter=Mock(
                return_value=Mock(
                    first=mock_company_locator
                )
            )
        ),
        Mock(
            locator=Mock(
                return_value=mock_price_locator
            )
        )
    ]

    mock_browser = Mock()
    mock_browser.new_page.return_value = mock_page
    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
    result = getter.detect_stock_price()

    assert result == [
        [
            "7203",
            "トヨタ自動車(株)",
            "ja",
            2850
        ]
    ]


@patch("modules.stock_getter.sync_playwright")
def test_detect_stock_price_us(mock_playwright):
    getter = StockGetter.__new__(StockGetter)
    getter.logger = Mock()

    getter.config = {
        "browser": {
            "headless_mode": True
        },
        "base_url": "https://finance.yahoo.co.jp/quote"
    }
    getter.stocks = [
        {
            "name": "EPAM",
            "code": "EPAM",
            "country": "us"
        }
    ]

    mock_page = Mock()
    company_first = Mock()
    company_first.inner_text.return_value = "EPAM Systems"

    price_first = Mock()
    price_first.inner_text.return_value = "150.25"

    company_locator = Mock()
    company_locator.first = company_first

    price_locator = Mock()
    price_locator.first = price_first

    mock_page.locator.side_effect = [
        company_locator,
        price_locator
    ]

    mock_browser = Mock()
    mock_browser.new_page.return_value = mock_page
    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser
    result = getter.detect_stock_price()

    assert result == [
        [
            "EPAM",
            "EPAM Systems",
            "us",
            150.25
        ]
    ]


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists")
def test_file_to_csv(mock_exists, mock_file):

    mock_exists.return_value = False

    getter = StockGetter.__new__(StockGetter)

    getter.logger = Mock()

    getter.config = {
        "csv": {
            "filepath": ".",
            "filename": "test.csv",
            "header": [
                "Date",
                "Code",
                "Name",
                "Country",
                "Price"
            ]
        }
    }

    stocks = [
        [
            "7203",
            "トヨタ自動車",
            "ja",
            2850
        ]
    ]

    getter.file_to_csv(stocks)

    mock_file.assert_called_once()
