FROM python:3.7

# 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#
RUN mkdir /code
WORKDIR /code

# モジュールのインストール
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# ソースコードをコピー
ADD . /code/
