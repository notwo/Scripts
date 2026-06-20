import csv
import os
from datetime import datetime
from typing import TypeAlias

from playwright.sync_api import sync_playwright, Error, TimeoutError
from modules.logger import Logger
from modules.util import Util


StockInfo: TypeAlias = list[int | str | float]


class StockGetter:
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
        self.stocks = self.config["stocks"]

    def file_to_csv(self, numbers_and_prices: list[int]) -> None:
        self.logger.info("CSV出力開始")

        file_path = f'{self.config["csv"]["filepath"]}/{self.config["csv"]["filename"]}'
        current_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        for i in range(len(numbers_and_prices)):
            numbers_and_prices[i].insert(0, current_datetime)

        header = self.config["csv"]["header"]
        header_exist = os.path.exists(file_path)
        try:
            with open(file_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not header_exist:
                    writer.writerow(header)

                for stock in numbers_and_prices:
                    writer.writerow(stock)
        except FileNotFoundError:
            self.logger.error(f"CSVファイルが存在しません: {file_path}")
        except UnicodeDecodeError:
            self.logger.error(f"CSVファイルの文字コードがUTF-8ではありません: {file_path}")
        except Exception:
            self.logger.exception(f"CSVファイルの読み込みに失敗しました: {file_path}")

        self.logger.info("CSV出力終了")

    def detect_stock_price(self) -> list[StockInfo]:
        result = []

        self.logger.info("株価取得処理開始")
        try:
            with sync_playwright() as p:
                self.logger.info("アクセス開始")
                browser = p.chromium.launch(headless=self.config["browser"]["headless_mode"])
                page = browser.new_page()

                for stock in self.stocks:
                    name = stock["name"]
                    code = stock["code"]
                    country = stock["country"]

                    self.logger.info(f"取得中: {name}({code})")

                    match country:
                        case "ja":
                            page.goto(
                                f'{self.config["base_url"]}/{code}.T',
                                wait_until="networkidle"
                            )

                            # 取得先画面のUI変更があった場合に失敗する可能性大
                            company_name = page.locator("h2").filter(
                                has_text="(株)"
                            ).first.inner_text()

                            price_text = (
                                # 取得先画面のUI変更があった場合に失敗する可能性大
                                page.locator('[class*="_CommonPriceBoard__priceBlock"]')
                                    .locator('[class*="_StyledNumber__value"]')
                                    .first
                                    .inner_text()
                            )
                            price_text = price_text.replace(",", "")

                        case "us":
                            page.goto(
                                f'{self.config["base_url"]}/{code}',
                                wait_until="networkidle"
                            )

                            company_name = (
                                # 取得先画面のUI変更があった場合に失敗する可能性大
                                page.locator('h2[class*="PriceBoard__name__"]')
                                .first
                                .inner_text()
                            )
                            price_text = (
                                # 取得先画面のUI変更があった場合に失敗する可能性大
                                page.locator(
                                    '[class*="PriceBoard"] span[class*="StyledNumber__value__"]'
                                ).first.inner_text()
                            )
                            price_text = price_text.replace(",", "")

                    if "." in price_text:
                        price = float(price_text)
                    else:
                        price = int(price_text)

                    result.append([
                        code,
                        company_name,
                        country,
                        price
                    ])

                    self.logger.info(f"{company_name}, {price}")

                browser.close()

        except TimeoutError:
            self.logger.error("タイムアウトが発生しました。")

        except Error as e:
            if "ERR_INTERNET_DISCONNECTED" in str(e):
                self.logger.error("インターネット接続なし")
            else:
                self.logger.exception("Playwrightエラー")
        except Exception:
            self.logger.exception("予期しないエラー")

        self.logger.info("株価取得処理終了")

        return result
