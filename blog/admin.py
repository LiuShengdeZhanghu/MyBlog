from django.contrib import admin
from .models import Article,BlogType
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id","title","author","is_deleted","read_num","create_time","last_updated_time")
    ordering = ("-id",)#以什么排序，必须是元组,在id前加-表示倒序排列

#admin.site.register(Article,ArticleAdmin)，两种注册方法
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ("id","type_name")
    ordering = ("id",)
