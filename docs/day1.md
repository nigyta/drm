# 1日目
## 開発環境  
- MacOS 14  
- VSC (Remote Developmentが入っていること。他にも必要なエクステンションあるかも)
- Docker for Mac

## 参考サイト
- [Docker Composeの公式クイックスタートガイド for Django](http://docs.docker.jp/compose/django.html)  
python2.7用に記述してあったのでpython3.7にアレンジする

- [djangoをPostgreSQL+Dockerで起動する。](https://qiita.com/sebeckawamura/items/45a4c2004af2296b6ea1)も参考にした

Django
- [Django(Python)でシステム開発できるようになる記事_入門編](https://qiita.com/Saku731/items/ed64190a12a4498b9446)
- [Python Django入門](https://qiita.com/kaki_k/items/511611cadac1d0c69c54)

VSC + Docker
- [Dockerで立ち上げた開発環境をVS Codeで開く!](https://qiita.com/yoskeoka/items/01c52c069123e0298660)

Django + Docker
- [Djangoの開発環境をDockerで作ってみた](https://qiita.com/homines22/items/2730d26e932554b6fb58)
- [DjangoをDocker Composeでupしよう！](https://qiita.com/kyhei_0727/items/e0eb4cfa46d71258f1be)

## 作業記録
1. ディレクトリ作成

ソースコードおよび設定ファイル等、アプリ全体を格納するためのディレクトリを作成。以後、基本的にこのディレクトリを起点として操作を行う。

2. `Dockerfile`作成
```
FROM python:3.7

# 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

# モジュールのインストール
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# ソースコードをコピー
ADD . /code/
```
`PYTHONDONTWRITEBYTECODE` は.pycファイルを作らないようにする環境変数。`PYTHONUNBUFFERED`は標準出力のバッファリングをしないようにする環境変数。

3. `requirements.txt`作成
```
Django==3.0.3
psycopg2==2.8.4
```
2020-02時点の最新版にした。

4. `dockr-compose.yml`作成

```
version: '3.7'

services:
    db:
        image: postgres:12
        environment:
          POSTGRES_PASSWORD: postgres
    web:
      build: .
      command: python /code/manage.py runserver 0.0.0.0:8000
      volumes:
        - .:/code
      ports:
        - 8000:8000
      depends_on:
        - db
```

`version`はPythonのバージョンではなくて、docker-composeファイルのバージョン ([こちらを参考](https://docs.docker.com/compose/compose-file/))。
`db`の`environment`の部分はデフォルトのパスワードを環境変数で与えないとコンテナの起動に失敗したため、後から追加した。

5. VSCからコンテナへの接続

VSCのコマンドパレットから`Remote-Containers: Add Development Container Configuration Files...`を選択し、開発用コンテナへの接続用の設定ファイルを作成する。Docker-composeを利用するため、`From docker-compose.yaml`と選んだあと`web`（django app用）コンテナを指定する。
作業ディレクトリ (デフォルトでは/Workspace)を`/code`に変更するため、`devcontainer.json`を編集する。
```
	"workspaceFolder": "/code",
```

再びコマンドパレットから`Remote-Containers: Reopen in Container`を選ぶとコンテナが起動し、`web`コンテナに接続することができる。(ホスト側に戻るには`Reopne Locally`)


6. Djangoプロジェクト作成
  コンテナ内の`/code`ディレクトリにて、
  ```
  django-admin.py startproject drm_project .
  ```
  を実行。自動的に各種ファイルが生成される。

7. DB設定
`drm_project/settings.py`のDATABASESの部分を次のように編集する
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432
    }
}
```
設定後、
```
python manage.py migrate
```
を実行し、DBの初期化を行う(行わずに次に進むと警告が出る。警告は出るがサービスの起動は可能)。
  
8. サービス起動  
  ```
  python /code/manage.py runserver 0.0.0.0:8000
  ```
  ウェブブラウザで http://localhost:8000 にアクセスしてDjangoの画面が表示されればOK。

## 積み残し
  VSCを使わない場合、`docker-compose up`でコンテナを起動してサービスを立ち上げることができる。  
  DBのデータを永続化させるために、`db`コンテナにディレクトリをマウントさせる必要がある気がする。  
  settings.py で言語やタイムゾーンの設定をした方がよかったかも

  ```
  LANGUAGE_CODE = 'ja'
  TIME_ZONE = 'Asia/Tokyo'
  ```

## 終わりに
  https://github.com/nigyta/drm にレポジトリ作成して終了  
  tag: day1 とした https://github.com/nigyta/drm/tree/day1
