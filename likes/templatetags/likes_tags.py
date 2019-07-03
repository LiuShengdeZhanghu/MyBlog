#!/usr/bin/env python
# -*- conding:utf-8 -*-
# author: liusheng time:2019/5/19
from django import template
from ..models import LikeCount,LikeRecord
from django.contrib.contenttypes.models import ContentType

register = template.Library()
# 注册标签
@register.simple_tag
def get_likes_count(obj):
    # 通过前端页面传递值进行查询点赞数，如果不存在，就创建一个模型
    content_type = ContentType.objects.get_for_model(obj)
    likecount,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=obj.pk)
    return likecount.liked_num

# 使用takes_context=True和context后，就可以使用所在模板的模板变量, 使用模板标签来控制点赞图标的样式
@register.simple_tag(takes_context=True)
def get_like_status(context,obj):
    content_type = ContentType.objects.get_for_model(obj)
    # 能通过模板变量获取得到user信息，是因为在setting文件中设置了 TEMPLATES django.contrib.auth.context_processors.auth
    user = context["user"]
    if not user.is_authenticated:
        return ""
    booler = LikeRecord.objects.filter(content_type=content_type, object_id=obj.id, user=context["user"]).exists()
    if booler:
        return "active"
    else:
        return ""

@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model