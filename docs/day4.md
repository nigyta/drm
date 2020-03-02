# 4日目

## DBに初期データ投入

## 参照
https://docs.djangoproject.com/ja/3.0/intro/tutorial02/#playing-with-the-api

## やったこと

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
