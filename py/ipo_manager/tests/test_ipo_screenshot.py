from pathlib import Path
from unittest.mock import Mock, patch

from playwright.sync_api import Error, TimeoutError

from modules.ipo_screenshot import IPOData,ScreenShotCollctor


@patch("modules.ipo_screenshot.sync_playwright")
def test_launch(mock_playwright):
    collector = ScreenShotCollctor.__new__(ScreenShotCollctor)

    collector.logger = Mock()

    collector.config = {
        "pages": {
            "filepath": "config",
            "filename": "pages.csv"
        },
        "browser": {
            "headless_mode": True,
            "width": 1920,
            "height": 1080,
            "timeout": 60000
        }
    }

    collector.pages = collector._load_pages_csv()

    mock_page = Mock()

    mock_browser = Mock()
    mock_browser.new_page.return_value = mock_page

    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser

    collector.launch(make_timestamp_folder=False)

    mock_browser.new_page.assert_called_once_with(
        viewport={
            "width": 1920,
            "height": 1080
        }
    )

    mock_page.goto.call_count == len(collector.pages)

    mock_page.screenshot.call_count == len(collector.pages)

    mock_browser.close.assert_called_once()


@patch("modules.ipo_screenshot.sync_playwright")
def test_launch_timeout(mock_playwright):

    collector = ScreenShotCollctor.__new__(ScreenShotCollctor)

    collector.logger = Mock()

    collector.config = {
        "pages": {
            "filepath": "config",
            "filename": "pages.csv"
        },
        "browser": {
            "headless_mode": True,
            "width": 1920,
            "height": 1080,
            "timeout": 60000
        }
    }

    collector.pages = collector._load_pages_csv()

    mock_page = Mock()
    mock_page.goto.side_effect = TimeoutError("timeout")

    mock_browser = Mock()
    mock_browser.new_page.return_value = mock_page

    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser

    collector.launch(False)

    collector.logger.error.assert_called_with(
        "タイムアウトが発生しました。"
    )


@patch("modules.ipo_screenshot.sync_playwright")
def test_launch_no_internet(mock_playwright):

    collector = ScreenShotCollctor.__new__(ScreenShotCollctor)

    collector.logger = Mock()

    collector.config = {
        "pages": {
            "filepath": "config",
            "filename": "pages.csv"
        },
        "browser": {
            "headless_mode": True,
            "width": 1920,
            "height": 1080,
            "timeout": 60000
        }
    }

    collector.pages = collector._load_pages_csv()

    mock_page = Mock()

    mock_page.goto.side_effect = Error(
        "net::ERR_INTERNET_DISCONNECTED"
    )

    mock_browser = Mock()
    mock_browser.new_page.return_value = mock_page

    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser

    collector.launch(False)

    collector.logger.error.assert_called_with(
        "インターネット接続なし"
    )


@patch("modules.ipo_screenshot.datetime")
@patch("modules.ipo_screenshot.sync_playwright")
def test_launch_timestamp_folder(
    mock_playwright,
    mock_datetime
):

    mock_datetime.now.return_value.strftime.return_value = (
        "20260620_120000"
    )

    collector = ScreenShotCollctor.__new__(ScreenShotCollctor)

    collector.logger = Mock()

    collector.config = {
        "pages": {
            "filepath": "config",
            "filename": "pages.csv"
        },
        "browser": {
            "headless_mode": True,
            "width": 1920,
            "height": 1080,
            "timeout": 60000
        }
    }

    collector.pages = collector._load_pages_csv()

    mock_page = Mock()

    mock_browser = Mock()
    mock_browser.new_page.return_value = mock_page

    mock_playwright.return_value.__enter__.return_value.chromium.launch.return_value = mock_browser

    collector.launch()

    screenshot_path = mock_page.screenshot.call_args.kwargs["path"]

    assert screenshot_path == (
        Path("screenshots")
        / "20260620_120000"
        / f"{collector.pages[-1].name}.png"
    )
