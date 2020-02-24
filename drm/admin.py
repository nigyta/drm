from django.contrib import admin
from drm.models import Protein

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'ref_id', 'description', 'gene', 'organism', 'source_db')  # 一覧に出したい項目
    list_display_links = ('id', 'ref_id',)  # 修正リンクでクリックできる項目

admin.site.register(Protein, BookAdmin)
