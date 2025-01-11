from tkinter import Tk,messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_binary
import csv
from datetime import datetime
import pytz
import time
import os
import sys


def to_csv(numbers_and_prices):
    file_path = "stocks.csv"
    jst = pytz.timezone('Asia/Tokyo')
    current_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    for i in range(len(numbers_and_prices)):
        numbers_and_prices[i].insert(0, current_datetime)

    header = ["日時", "銘柄コード", "株価"]
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not os.path.exists(file_path):
            writer.writerow(header)

        for stock in numbers_and_prices:
            writer.writerow(stock)


def detect_stock_price(stock_numbers):
    numbers_and_prices = []

    driver = webdriver.Chrome()
    driver.get("https://finance.yahoo.co.jp/")
    time.sleep(0.5) # 読み込み時間を考慮

    for stock in stock_numbers:
        # yahoo financeトップ
        input = driver.find_element(By.XPATH, "//input[@name='query']")
        price = input.send_keys(stock)
        input.send_keys(Keys.RETURN)
        time.sleep(0.5) # 読み込み時間を考慮

        # 検索後の画面
        price_element = driver.find_element(By.XPATH, "//div[@id='root']/main/div/section/div[2]/div[2]/div/span/span/span")
        price = int(price_element.text.replace(",", ""))
        numbers_and_prices.append([stock, price])

    driver.close()
    driver.quit()

    return numbers_and_prices


def get_stock_numbers():
    file_path = "stocklist.txt"
    if not os.path.exists(file_path):
        messagebox.showinfo('ファイル未存在エラー', f'stockGetter.exeと同フォルダに銘柄コードリスト({file_path})が存在しません')
        sys.exit()

    stock_numbers = []
    with open(file_path, "r") as f:
        while(True):
            line = f.readline().rstrip("\n")
            stock_numbers.append(line)
            if not line:
                break

    return stock_numbers


# entry point
stock_numbers = get_stock_numbers()
del stock_numbers[-1] # なぜか末尾にできる空文字列を削除

numbers_and_prices = detect_stock_price(stock_numbers)
to_csv(numbers_and_prices)
