# Scripts

## gas/moveUnnecessaryMailsToTorash.gs

### 概要
Gmailに溜まった、特定のラベルに属する不要メールを一括削除する

## py/stock_manager/stock_getter.py

### 概要
特定の企業の株価を取得し、csvに記載する

### 使い方

1. 事前準備として、config/setting.ymlのstocks:以下に取得したい株価の企業名とコードを記載する(複数可)
1. 以下を実行
```bash
python main.py
```

## py/stock_manager/stock_graph.py

### 概要
stock_getter.pyで作成した株価情報(stocks.csv)のデータをグラフ化し、PDF出力する

### 使い方

1. 事前準備として、config/setting.ymlのstocks:以下に取得したい株価の企業名とコードを記載する(複数可)
```bash
python main.py
```
  ※stock_getter.pyの直後に実行される

## py/ipo_manager/ipo_screenshot.py

事前準備として、config/setting.ymlのstocks:以下に取得したい株価の企業名とコードを記載する(複数可)
### 概要
複数の証券会社サイトにアクセスし、現在のIPO情報のスクショ取得

### 使い方

1. 事前準備として、config/setting.ymlのpages:以下にスクショ取得したい企業名とURLを記載する(複数可)
1. 以下を実行
```bash
python main.py
```
