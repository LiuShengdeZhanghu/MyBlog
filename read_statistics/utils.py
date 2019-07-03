#!/usr/bin/env python
# -*- conding:utf-8 -*-
# author: liusheng time:2019/3/28
import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,ReadDetail
from django.db.models import Sum
from django.utils import timezone
from blog.models import Article

def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read"% (ct.model,obj.pk)
    #构造cookie的结构
    if not request.COOKIES.get(key):
        '''
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        '''
        #每篇博客的总阅读数+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        #每天的阅读数+1
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key

def get_preSevenDays_readnum(content_type):
    #今天
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,-1,-1):   #过去七天和今天的访问量
        date = today - datetime.timedelta(days=i)  #days=1 表示差量为一天
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date = date)
        #对每一天的各篇博客阅读数量进行求和，aggregate是进行聚合查询,对查询出的read_num进行求和
        result = read_details.aggregate(read_num_sum = Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    #以元组形式返回
    return dates, read_nums

def get_today_hot_data(content_type):
    today = timezone.now().date()
    # read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    #排序,今天的阅读热度

    blogs = Article.objects.filter(read_details__date=today)\
        .values('id','title')\
        .annotate(read_num_sum = Sum('read_details__read_num'))\
        .order_by('-read_num_sum')

    return blogs[:3] #切片，取前3条

def get_yesterday_hot_data(content_type):
    yesterday = timezone.now().date() - datetime.timedelta(days=1)    #今天减去一天就是昨天
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    # 排序,昨天的阅读热度
    return read_details[:3]

def get_7_days_hot_data(content_type):
    today = timezone.now().date()
    pre_seven_days = today - datetime.timedelta(days=7)
    read_details = ReadDetail.objects.filter(content_type=content_type,date__lt=today, date__gte=pre_seven_days)\
        .values('content_type','object_id').annotate(read_num_sum = Sum('read_num'))\
        .order_by('-read_num_sum')
    #文档 https://docs.djangoproject.com/en/1.11/ref/models/querysets/#django.db.models.query.QuerySet.values
    #小于今天，大于等于7天前，把七天的每篇博客的阅读量进行加和，并排序
    return read_details[:3]