#!/usr/bin/env python
# -*- conding:utf-8 -*-
# author: liusheng time:2019/6/29
import xadmin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# class ProfileInline(xadmin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'employee'
#
# class UserAdmin(BaseUserAdmin):
#     inlines = (ProfileInline,)
#     list_display = ('username','nickname','email','is_staff','is_active','is_superuser')
#
#     def nickname(self,obj):
#         # 这里的obj指的是user，通过外键读出nickname
#         return obj.profile.nickname
#
#     # 把自定义字段展示的时候显示为中文
#     nickname.short_description = '昵称'
#
# xadmin.site.unregister(User)
# xadmin.site.register(User, BaseUserAdmin)


class ProfileAdmin(object):
    list_display = ('user','nickname')
xadmin.site.register(Profile,ProfileAdmin)