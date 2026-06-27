# Scripts

## gas/moveUnnecessaryMailsToTorash.gs

### 概要
Gmailに溜まった、特定のラベルに属する不要メールを一括削除する

## stock_manager

株価情報を任意で取得/グラフ化/メール送信するスクリプト

### 使い方

config/companies.csvに、取得したい企業情報を追加する(1行につき1企業)

powershellを開いて、py/stock_manager以下に移動し以下を実行する
```
$env:MAIL_PASSWORD="<Gmailのアプリパスワード>"
$env:SENDER="<送信元>"
$env:TO="<宛先>"
python main.py
```
※送信元と宛先はどちらも自分のメールアドレスで構わない

詳細な設定についてはconfig/以下ymlファイルを参照すること

### py/stock_manager/stock_getter.py

#### 概要
特定の企業の株価を取得し、csvに記載する

### py/stock_manager/stock_graph.py

#### 概要
- stock_getter.pyで作成した株価情報(stocks.csv)のデータをグラフ化し、PDF出力する
- stock_getter.pyの直後に実行される

### py/stock_manager/mail_sender.py
- stock_graph.pyで作成したPDFを添付して宛先へメール送信する
- stock_graph.pyの直後に実行される


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
