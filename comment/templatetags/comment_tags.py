#!/usr/bin/env python
# -*- conding:utf-8 -*-
# author: liusheng time:2019/5/19
from django import template
from ..models import Comment
from ..forms import CommentForm
from django.contrib.contenttypes.models import ContentType

register = template.Library()

# 注册标签
@register.simple_tag
def get_comment_count(obj):
    # 通过前端页面传递值进行计算评论数
    content_type = ContentType.objects.get_for_model(obj)
    comment_count = Comment.objects.filter(content_type=content_type,object_id=obj.pk).count()
    return comment_count

@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={
            "content_type":content_type.model,
            "object_id":obj.pk,
            "reply_comment_id":0})
    return form

@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)  # 一级评论
    # 依据时间，新的评论在最前
    return comments.order_by("-comment_time")