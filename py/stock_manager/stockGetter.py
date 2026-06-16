import csv
import os
import sys
import time
from datetime import datetime
from tkinter import Tk, messagebox
from playwright.sync_api import sync_playwright

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def to_csv(numbers_and_prices):
    file_path = "stocks.csv"
    current_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    for i in range(len(numbers_and_prices)):
        numbers_and_prices[i].insert(0, current_datetime)

    header = ["日時", "銘柄コード", "銘柄名", "株価(円)"]
    header_exist = os.path.exists(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not header_exist:
            writer.writerow(header)

        for stock in numbers_and_prices:
            writer.writerow(stock)


def detect_stock_price(stock_numbers):
    result = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for stock in stock_numbers:

            print(f"取得中: {stock}")

            page.goto(
                f"https://finance.yahoo.co.jp/quote/{stock}.T",
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
                stock,
                company_name,
                price
            ])

            print(company_name, price)

        browser.close()

    return result


def get_stock_numbers():
    file_path = "stocklist.txt"
    if not os.path.exists(file_path):
        messagebox.showinfo(
            "ファイル未存在エラー",
            f"stockGetter.exeと同フォルダに銘柄コードリスト({file_path})が存在しません",
        )
        sys.exit()

    stock_numbers = []
    with open(file_path, "r") as f:
        while True:
            line = f.readline().rstrip("\n")
            stock_numbers.append(line)
            if not line:
                break

    return stock_numbers


# entry point
stock_numbers = get_stock_numbers()
del stock_numbers[-1]  # なぜか末尾にできる空文字列を削除

numbers_and_prices = detect_stock_price(stock_numbers)
to_csv(numbers_and_prices)
