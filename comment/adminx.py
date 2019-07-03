#!/usr/bin/env python
# -*- conding:utf-8 -*-
# author: liusheng time:2019/6/29
import xadmin
from .models import Comment

class CommentAdmin(object):
    list_display = ('user','text','comment_time','reply_to')
xadmin.site.register(Comment,CommentAdmin)