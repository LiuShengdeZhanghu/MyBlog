from django.contrib import admin
from .models import ReadNum,ReadDetail
# Register your models here.

@admin.register(ReadNum)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ("read_num","content_object")
    ordering = ("id",)

@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ("date","read_num","content_object")
    ordering = ("-id",)