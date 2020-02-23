# ２日目

## 概要
Djangoアプリケーションを作成して、Hello world　を表示させる。

Djangoではプロジェクトとアプリケーションという概念があり、プロジェクトはサイト全体を示し、　アプリケーションはプロジェクト内で実際に処理を行うWebアプリケーションのことを示す。1つのプロジェクトは複数のアプリケーションを含むことができる。（逆に1つのアプリケーションを複数のプロジェクトで使うこともできるらしい。http://farewell-work.hatenablog.com/entry/2017/05/07/160359)

## 参考資料

Hellow worldの作成までは https://docs.djangoproject.com/ja/3.0/intro/tutorial01/ 


テンプレートの利用については
https://docs.djangoproject.com/ja/3.0/intro/tutorial03/


## 作業記録
1. アプリケーション作成

    "drm"という名称で作成する。
    ```
    python manage.py startapp drm
    ```
    結果、"drm"という名称のディレクトリとその傘下にいくつかのファイルが作られた。
    ```
    $ ls drm
    __init__.py admin.py    apps.py     migrations  models.py   tests.py    views.py
    ```

    Django用の開発スペースを "drm" という名称にしたのでアプリケーションの名前を "drm" にすると、 "drm/drm" というように同じディレクトリ名で階層になってしまうので開発スペースの名称を変えた方がよかったかも。  
    https://qiita.com/Saku731/items/ed64190a12a4498b9446 によるとプロジェクト名は app_config、アプリ名はapp_folderというようにしている。プロジェクト=サイト全体の設定を行う、アプリ=webサービスの実際の処理を記述する、という役割なのでこの命名方法は分かりやすいかも。

2. view の作成

    drm/views.py を編集
    ```
    from django.http import HttpResponse
    from django.shortcuts import render

    # Create your views here.

    def index(request):
        return HttpResponse("Hello world.")
    ```

3. ルーティングの設定1

    drm/urls.py を作成し下記の通りにする
    ```
    from django.urls import path

    from . import views

    urlpatterns = [
        path('', views.index, name='index'),
    ]
    ```

4. ルーティングの設定2

    上で作成したルーティングの設定をプロジェクトに追加する　　
    drm_project/urls.py を下記のように変更

    ```
    from django.contrib import admin
    from django.urls import path, include  # include追加

    urlpatterns = [
        path('admin/', admin.site.urls),
            path('', include('drm.urls')),  # 追加
    ]
    ```

    include をすることでアプリケーションごとのルーティング設定をプロジェクトに加えることができる。

5. ブラウザで確認

    http://localhost:8000 で　Hello world　が表示されることを確認。

6. テンプレートの利用1 templates ディレクトリの作成

    `drm/templates/drm`  ディレクトリを作成する

    drm アプリケーション配下に templates ディレクトリを作成し、その中にアプリケーションと同じ名称でディレクトリを作る。その下にテンプレート index.html　を作ると、"drm/index.html" という名称で参照できる。("Within the templates directory you have just created, create another directory called polls, and within that create a file called index.html.")  

7. テンプレートの利用2 templateファイルの作成

    "drm/templates/drm/index.html" を作成

8. テンプレートの利用3 viewの変更

    本来のやり方は、テンプレートをloadしてHttpResponseを使うが、ショートカットとして `django.shortcuts.render` が用意されている。

    結果、views.py は下記のようになる。
    ```
    from django.shortcuts import render
    # from django.http import HttpResponse　# 不要
    # from django.template import loader # 不要


    def index(request):
        context = {
            'message': "Hello world!!!",
        }
        return render(request, 'drm/index.html', context)
    ```

9. アプリケーションのプロジェクトへの追加

    これだけでは　"TemplateDoesNotExist" というエラーが出てしまった。テンプレートがプロジェクト配下に見つからないという意味らしい。これを解決するためにプロジェクトの `setting.py` を編集しアプリケーションをプロジェクトに追加する。

    変更箇所は以下の通り
    ```
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'drm'  # 追加
    ]
    ```

    6 のときに規約にしたがって templates ディレクトリ（とその下にアプリケーション名と同じディレクトリ）を作れば自動でtemplatesディレクトリを参照するようになる。

    同様に静的ファイル置き場は "static"  という名称でアプリケーション配下に作成すれば、プロジェクトに追加すれば参照できるようになると思われる。
    

    [補足]  
    別の方法として "TEMPLATES" 部分の "DIRS" にテンプレートの場所を指定する方法もある。
    ```
     'DIRS': [os.path.join(BASE_DIR,'drm', 'templates'),],
    ```
    この方法よりも、アプリケーションごとにtemplates ディレクトリを用意しておく方が簡単だと思われる。

10. webブラウザで開いて確認

    http://localhost:8080/ でテンプレートを介してHello worldが表示されるようになった。

    viewsとurlsにテスト用のページをいくつか追加しておく。

## まとめ

HelloWorld 表示までの手順

- アプリケーション新規作成
    - `manage.py startapp` でアプリケーションを新規作成

- プロジェクト側の設定項目
    - アプリケーションをプロジェクトに追加する (setting.py)
    - アプリケーションのURLルーティング設定を include する (urls.py)

- アプリケーション側設定
    - template ディレクトリを作成 (規約通りの場所につくれば自動で参照してくれるようになる)
    - views.py を編集して view 関数を作成
    - urls.py を編集して url のルーティングを設定
    - ショートカットの render 関数を使うとテンプレートのレンダリングは簡単に行える



