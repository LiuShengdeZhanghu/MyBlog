#!/usr/bin/env python
# -*- conding:utf-8 -*-
# author: liusheng time:2019/6/29

import xadmin
from .models import Article,BlogType
from xadmin import views

class ArticleAdmin(object):
    list_display = ('title','blog_type','create_time','last_updated_time','author','read_num')
xadmin.site.register(Article,ArticleAdmin)

class BlogTypeAdmin(object):
    list_display = ('type_name','id')
xadmin.site.register(BlogType,BlogTypeAdmin)

class BaseSetting(object):
    enable_themes =True
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView,BaseSetting)


class GloableSetting(object):
    site_title = "博客后台管理系统"
    site_footer = "博客后台管理系统，刘胜版权所有"

xadmin.site.register(views.CommAdminView,GloableSetting)