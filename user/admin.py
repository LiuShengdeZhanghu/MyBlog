#!/usr/bin/env python
# -*- conding:utf-8 -*-
# author: liusheng time:2019/6/15
from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# 在admin的User的页面中可以见到自定义的外键关联的内容
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'employee'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username','nickname','email','is_staff','is_active','is_superuser')

    def nickname(self,obj):
        # 这里的obj指的是user，通过外键读出nickname
        return obj.profile.nickname

    # 把自定义字段展示的时候显示为中文
    nickname.short_description = '昵称'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','nickname')