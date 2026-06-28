import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from playwright.sync_api import Error, TimeoutError, sync_playwright

from modules.logger import Logger
from modules.util import Util


@dataclass(slots=True)
class IPOData:
    name: str
    url: str


class ScreenShotCollctor:
    def __init__(self, filename: str) -> None:
        try:
            self.config = Util.load_config(filename)
        except FileNotFoundError:
            self.logger.error(f"設定ファイルが存在しません: {filename}")
        except UnicodeDecodeError:
            self.logger.error(f"設定ファイルの文字コードがUTF-8ではありません: {filename}")
        except Exception:
            self.logger.exception(f"設定ファイルの読み込みに失敗しました: {filename}")

        self.logger = Logger.get_logger(
            self.config["log"]["filepath"],
            self.config["log"]["filename"])
        self.pages = self._load_pages_csv()

    def _load_pages_csv(self) -> list[IPOData]:
        file_path = f'{self.config["pages"]["filepath"]}/{self.config["pages"]["filename"]}'

        pages = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    page = IPOData(
                        name=row["証券会社名"],
                        url=row["URL"],
                    )
                    pages.append(page)

        except FileNotFoundError:
            self.logger.error(f"CSVファイルが存在しません: {file_path}")
        except UnicodeDecodeError:
            self.logger.error(f"CSVファイルの文字コードがUTF-8ではありません: {file_path}")
        except Exception:
            self.logger.exception(f"CSVファイルの読み込みに失敗しました: {file_path}")

        return pages
    
    def launch(self, make_timestamp_folder: bool = True) -> None:
        output_dir = Path("screenshots")
        if make_timestamp_folder:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path("screenshots") / timestamp

        self.logger.info(f"Save directory: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=self.config["browser"]["headless_mode"]
                )
                page = browser.new_page(
                    viewport={
                        "width": self.config['browser']['width'],
                        "height": self.config['browser']['height']}
                )

                for page_info in self.pages:
                    name = page_info.name
                    url = page_info.url

                    self.logger.info(f"Accessing: {url}")

                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=self.config['browser']['timeout']
                    )

                    page.screenshot(
                        path=output_dir / f"{name}.png",
                        full_page=True
                    )

                    self.logger.info("  -> Success")

                browser.close()

                self.logger.info('Done')

        except TimeoutError:
            self.logger.error("タイムアウトが発生しました。")

        except Error as e:
            if "ERR_INTERNET_DISCONNECTED" in str(e):
                self.logger.error("インターネット接続なし")
            else:
                self.logger.exception("Playwrightエラー")
        except Exception:
            self.logger.exception("予期しないエラー")
