# 4日目 DBに初期データ投入

## 参照
https://docs.djangoproject.com/ja/3.0/intro/tutorial02/#playing-with-the-api

## 投入スクリプト作成

`scripts/insert_initial_data_to_db.py` を作成した。
ポイントは、 

```
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","drm_project.settings")
 
django.setup()
 
from drm.models import Protein
```

というように、プロジェクトのルートディレクトリをパスに追加してモジュールをインポートできるようにすること。


## 一覧ページと詳細ページの作成

    URLの設定　(drm/urls.py)

    ```
    app_name = 'drm'
    ```

    を追加。

    urlpatternsには
    ```
    path('proteins', views.list_proteins, name='protein_list'),
    path('proteins/<str:ref_id>/', views.ref_detail, name='detail'),
    ```
    を追加。これによりテンプレートファイルにURLを下記のように生成して埋め込むことができる。
    ```
    {% url 'drm:protein_list' %}
    {% url 'drm:detail' protein.ref_id %}
    ```
    app_name でURL名称の名前空間を分けることができる。app_nameを指定しなかった場合　{% url 'protein_list' %}のように指定する。



## 詳細ページのview

    ```
    def ref_detail(request, ref_id):
        protein = get_object_or_404(Protein, ref_id=ref_id)
        context = {
            'message': f"{protein.ref_id}: {protein.description} ({protein.organism})"
        }
        return render(request, 'drm/index.html', context)
    ```
  
    django.shortcuts の get_object_or_404 をインポートして使用。検索結果が見つからなかった場合には404を返す。

## 一覧ページのview
    3日目で作成済み

## 一覧ページのtemplate

```
<h1>{{ message }}</h1>

<table class="table table-condensed table-striped table-bordered">
    <thead>
      <tr>
        <th scope="col">ID</th>
        <th scope="col">Description</th>
        <th scope="col">Gene</th>
        <th scope="col">EC number</th>
        <th scope="col">Flag</th>
        <th scope="col">Organism</th>
        <th scope="col">Source DB</th>
        <th scope="col">Sequence</th>
      </tr>
    </thead>
    <tbody>
      {% for protein in proteins %}
      <tr>
        <th scope="row"><a href="{% url 'drm:detail' protein.ref_id %}">{{ protein.ref_id }}</a></th>
        <td>{{ protein.description }}</td>
        <td>{{ protein.gene }}</td>
        <td>{{ protein.ec_number }}</td>
        <td>{{ protein.flag }}</td>
        <td>{{ protein.organism }}</td>
        <td>{{ protein.source_db }}</td>
        <td>{{ protein.sequence }}</td>
    </tr>
      {% endfor %}
    </tbody>
</table>
```