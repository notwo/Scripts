import csv
import os
from datetime import datetime
from pathlib import Path
from tkinter import Tk, messagebox
from typing import TypeAlias

import yaml
from playwright.sync_api import sync_playwright


StockInfo: TypeAlias = list[int | str | float]


class StockGetter:
    def __init__(self, filename: str) -> None:
        self.config = None
        self._load_config(filename)
        self.logger = None
        self.stocks = self.config["stocks"]

    def _load_config(self, filename: str) -> None:
        config_file = Path(filename)

        with open(config_file, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def file_to_csv(self, numbers_and_prices: list[int]) -> None:
        file_path = f'{self.config["csv"]["filepath"]}/{self.config["csv"]["filename"]}'
        current_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        for i in range(len(numbers_and_prices)):
            numbers_and_prices[i].insert(0, current_datetime)

        header = self.config["csv"]["header"]
        header_exist = os.path.exists(file_path)
        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not header_exist:
                writer.writerow(header)

            for stock in numbers_and_prices:
                writer.writerow(stock)

    def detect_stock_price(self) -> list[StockInfo]:
        result = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.config["browser"]["headless_mode"])
            page = browser.new_page()

            for stock in self.stocks:
                name = stock["name"]
                code = stock["code"]

                print(f"取得中: {name}({code})")

                page.goto(
                    f"https://finance.yahoo.co.jp/quote/{code}.T",
                    wait_until="networkidle"
                )

                company_name = page.locator("h2").filter(
                    has_text="(株)"
                ).first.inner_text()

                price_text = (
                    page.locator('[class*="_CommonPriceBoard__priceBlock"]')
                        .locator('[class*="_StyledNumber__value"]')
                        .first
                        .inner_text()
                )
                price_text = price_text.replace(",", "")

                if "." in price_text:
                    price = float(price_text)
                else:
                    price = int(price_text)

                result.append([
                    code,
                    company_name,
                    price
                ])

                print(company_name, price)

            browser.close()

        return result
