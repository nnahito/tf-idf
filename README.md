## これはなに
久々に自然言語処理で遊びたくなった + skleanって使ったことねーなーと思って、作ってみたやつ。


## 環境
Python3系（Python 3.7.0）使ってます。
Windows10です。


## 使い方

### 環境準備
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 起動
```
python main.py
```

### データ準備
[青空文庫](https://www.aozora.gr.jp/)様のデータを利用しています。
著作権の切れたデータなので、適当にCSVでデータを上げています。

1. `studies.csv`を開き、A列にラベル名（今回は小説の作者名）を入れます。
1. B列に特徴が出そうなテキストを入れます。
1. このとき作者名が一緒でも別々の行に保存してOKです。コード内で同じ作者の小説は、自動で連結しています
1. `main.py`を開き、50行目あたりの`sample変数`に類似度を図りたい未知の文章を入れます
1. `python main.py`を実行します