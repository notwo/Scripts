from datetime import datetime
from pathlib import Path

from playwright.sync_api import Error, TimeoutError, sync_playwright

from modules.logger import Logger
from modules.util import Util


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
        self.pages = self.config["pages"]

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
                    name = page_info["name"]
                    url = page_info["url"]

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
