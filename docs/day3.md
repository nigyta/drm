# 3日目

## 概要
モデルの作成を行う

## 作業記録

1. django superuserの作成

    ターミナルで
    ```
    python manage.py createsuperuser
    ```
    を実行し、指示に従う。

    adminユーザーができたら、
    http://localhost:8000/admin/
    へのログインが可能になる。

2. モデルの作成

    DFASTの参照DBの形式については https://github.com/nigyta/dfast_core/blob/master/docs/workflow.md#reference-databases を参照

    id: 参照配列のID, モデルでは ref_id とする。 Char 20
    description: Char 255
    gene: 遺伝子シンボル Char 30
    EC_number: EC番号 Char 20
    flag: 特に使用していないが Char 20
    organism: 生物名 Char 255
    source_DB： Char 20
    sequence: Text

    `drm/models.py` に下記のクラスを追加

    ```
    class Protein(models.Model):
        """Reference protein sequence"""
        ref_id = models.CharField('Reference ID', max_length=20)
        description = models.CharField('Description', max_length=255)
        gene = models.CharField('Gene symbol', max_length=30)
        ec_number = models.CharField('EC number', max_length=20)
        flag = models.CharField('flag', max_length=20)
        organisma = models.CharField('organisma', max_length=255)
        source_db = models.CharField('source_db', max_length=20)
        sequence = models.TextField('Sequence')

        def __str__(self):
            return f"<Protein {self.ref_id} {self.description}>"
    ```

3. モデルをadminページで編集できるようにする。

    `drm/admin.py` を編集
    
    ```
    from django.contrib import admin
    from drm.models import Protein

    # Register your models here.
    admin.site.register(Protein)
    ```    

    これで admin ページから Protein モデルが見えるようになるが、DBのマイグレーションを行なっていないのでまだ編集できない（エラーになる）

4. DB マイグレーション
    ターミナルで下記を実行して migrate file を作る。
    ```
    python manage.py makemigrations drm
    ```
    ファイルは drm/migrations 以下にできる。(drm/migrations/0001_initial.py)

    migrate 実行
    ```
    python manage.py migrate drm
    ```

    これによりDBに"drm_protein"テーブルが追加され admin ページで追加・編集ができるようになった。

5. モデルを更新

    空文字列を許容するため、下記のようにオプションを追加

    ```
    ec_number = models.CharField('EC number', max_length=20, blank=True)
    flag = models.CharField('flag', max_length=20, blank=True)
    ```

    空文字列の許可・不許可はDjango側で制御しているようでDB定義の更新は不要。（マイグレーションしなくても良い）

6. モデルを更新その２

    ref_id をプライマリーキーとして設定する

    ```
        ref_id = models.CharField('Reference ID', max_length=20, primary_key=True)
    ```
    として。反映させるには

    ```
    python manage.py makemigrations drm
    python manage.py migrate drm
    ```

    しかし、adminページにおいてref_id を変更しようとすると、変更するのではなく新規レコードとして追加されてしまい運用上使いにくかったので元に戻すことにする。

7. migrationのロールバック

    migrationの履歴を表示
    ```
    python manage.py showmigrations

    # 結果
    drm
    [X] 0001_initial
    [X] 0002_auto_20200224_0622
    ```
    というようになっていたので、0001の段階まで戻すことにする。

    ```
    python manage.py migrate drm 0001
    ```

    その後、マイグレーションファイル `drm/migrations/0002_auto_20200224_0622.py` を削除すると履歴から消えて、元に戻った。

    ```python manage.py migrate (app_name) zero``` でリセット (migration前の状態までrollbask) できる。

    その後、ref_id にユニーク制約を加えてとりあえず確定
    ```
        ref_id = models.CharField('Reference ID', max_length=20, unique=True)
    ```

    反映させるには makemagrations と migrate を繰り返す

8. migrationsのsquash

    いろいろ試しているうちに migration fileが複数できたので、squashする

    ```
    python manage.py showmigrations

    # 結果
    drm
    [X] 0001_initial
    [X] 0002_auto_20200224_0655
    [X] 0003_auto_20200224_0657
    ```

    下記のコマンドで0001から0003をまとめられる
    ```
    python manage.py squashmigrations drm 0001 0003
    ```

    ただし squash したからといってmigration fileが減るわけではない（履歴上で減っているように見えるだけ）
    結局squashした結果を決して最初からやり直した。

9. 管理画面のカスタマイズ

    一覧に表示したい項目をカスタマイズするため。drm/admin.py を編集しBookAdminクラスを追加

    ```
    class BookAdmin(admin.ModelAdmin):
        list_display = ('id', 'ref_id', 'description', 'gene', 'organism', 'source_db')  # 一覧に出したい項目
        list_display_links = ('id', 'ref_id',)  # 修正リンクでクリックできる項目

    admin.site.register(Protein, BookAdmin)　# 変更
    ```

9. DBの一覧を表示させるviewを作成

    下のようにするとテーブルから全データ取得してリストに格納してくれる。

    ```
    def list_proteins(request):
        """Proteinの一覧"""
        proteins = Protein.objects.all().order_by('id')[:100] # debug用に先頭100件のみ
        context = {
            'proteins': proteins,
            'message': "Protein List"
        }
        return render(request, 'drm/list_proteins.html', context)
    ```  

    URLは　"http://localhost:8000/proteins"

## まとめ
    モデルの作成とadminページの利用について扱った。
    次回はDBへの一括データ投入

## その他
    Postgresqlに接続するプラグインとしてSQLToolsをVSCにインストールして使った。
    