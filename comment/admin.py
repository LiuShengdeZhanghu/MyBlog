from django.contrib import admin
from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id","user","comment_time","text","content_object")
    ordering = ("id",)
