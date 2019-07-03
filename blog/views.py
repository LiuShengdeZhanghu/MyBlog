import json
import urllib.request
import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Article,BlogType
from django.template import loader
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import read_statistics_once_read,get_preSevenDays_readnum,get_today_hot_data
from comment.models import Comment
from django.db.models import Count,Sum
from django.core.cache import cache
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.urls import reverse
from user.forms import loginForm
from comment.forms import CommentForm

# Create your views here.
def get_blog_list_common_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUM)  # 每10页进行分页
    page_num = request.GET.get("page", 1)  # 默认打开第一页,获取页面参数（GET请求）#实现分页
    page_of_blogs = paginator.get_page(page_num)  # 不和规矩的参数就默认返回1
    current_page_num = page_of_blogs.number  # 获取当前页面的页码
    page_range = [x for x in range(int(current_page_num - 2), int(current_page_num + 3)) if
                  0 < x <= int(paginator.num_pages)]  # 在一个页面中只显示附近两个选项
    #加上省略页标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "…")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("…")
    if page_range[0] != 1:  # 加上首页和尾页以及省略页码
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #获取分类的博客数量
    blog_types_list = BlogType.objects.annotate(blog_count = Count('article'))
    #利用Django的model的Count方法进行计数并赋值给blog_count变量，这种方法在需要的时候才会执行把数据加入内存，比下面的方法好
    '''blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Article.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)'''

    #获取按照日期分类的博客数量
    blog_dates = Article.objects.dates('create_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Article.objects.filter(create_time__year=blog_date.year,create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    content = {}

    content['page_of_blogs'] = page_of_blogs
    content["blog_types"] = blog_types_list
    content["page_range"] = page_range
    content["blog_dates"] = blog_dates_dict
    #得到博客按日期分类
    return content

def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Article.objects.filter(blog_type=blog_type)
    content = get_blog_list_common_data(request,blogs_all_list)
    #得到当前页面的博客
    content["blog_type"]=blog_type
    return render(request,"blog_with_type.html",content)


def article_detail(request,article_id):
    blog = get_object_or_404(Article,pk=article_id)
    '''    
    if not request.COOKIES.get('blog_%s_read'%article_id):
        #如果没有cookie 就说明是不同的阅读,因为cookie的有效过了就代表不同的阅读
        
        if ReadNum.objects.filter(blog=blog).count():
            #已经创建了这个字段
            readnum = ReadNum.objects.get(blog=blog)
        else:
            readnum = ReadNum()
            readnum.blog = blog
        readnum.read_num += 1
        readnum.save()
        '''

    read_cookie_key = read_statistics_once_read(request,blog)

    content = {}
    content["article"] = blog
    content["previous_blog"] = Article.objects.filter(create_time__gt=blog.create_time).last()
    content["next_blog"] = Article.objects.filter(create_time__lt=blog.create_time).first()

    # content["login_form"] = loginForm()
    # 把数据初始化到Form表单中
    # content["comment_form"] = CommentForm(initial={"content_type":blog_content_type.model,"object_id":article_id,"reply_comment_id":0})
    # content['user'] = request.user
    response = render(request,"article_detail.html",content)
    #通过设置cookie来确定计数，不同的人访问，同一个人不同时间访问
    response.set_cookie(read_cookie_key, 'true', max_age=600) #cookie有效时间,不设置值的时候就关闭浏览器的时候失效
    return response   #绑定参数

def article_list(request):
    #加一个判断筛选，计划删除的不展示
    blogs_all_list = Article.objects.filter(is_deleted=False)
    content = get_blog_list_common_data(request,blogs_all_list)
    return render(request,"article_list.html",content)

def blogs_with_date(request,year,month):
    #对时间进行筛选
    blogs_all_list = Article.objects.filter(create_time__year=year, create_time__month=month)

    content = get_blog_list_common_data(request,blogs_all_list)
    content["blog_with_date"] = "%s年%s月" % (year,month)
    return render(request, "blog_with_date.html", content)

def get_7_days_hot_blogs_teacher():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Article.objects.filter(read_details__date__lt=today, read_details__date__gte=date)\
        .values('id','title')\
        .annotate(read_num_sum = Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    #通过对read_details的关联，找出这些日期的博客，然后统计排序
    return blogs[:3]

def get_7_days_hot_blogs(hot_data_for_7_days):
    #得到近七天热门博客的名字 ，自己写的方法
    i = 0
    for hot_data in hot_data_for_7_days:
        blog = Article.objects.get(pk=hot_data['object_id']).title
        hot_data_for_7_days[i]['blog_title'] = blog
        i += 1
    return hot_data_for_7_days

def index(request):
    blog_content_type = ContentType.objects.get_for_model(Article)
    dates, read_nums = get_preSevenDays_readnum(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    # hot_data_for_7_days = get_7_days_hot_data(blog_content_type)
    # hot_data_for_7_days = get_7_days_hot_blogs(hot_data_for_7_days)

    #获取七天热门博客的缓存数据
    hot_data_for_7_days = cache.get('hot_data_for_7_days')
    if hot_data_for_7_days is None:
        hot_data_for_7_days = get_7_days_hot_blogs_teacher()
        cache.set('hot_data_for_7_days',hot_data_for_7_days,3600)

    content = {}
    content['read_nums'] = read_nums
    content['dates'] = dates
    content['today_hot_data'] = today_hot_data
    content['hot_data_for_7_days'] = hot_data_for_7_days
    return render(request, "index.html",content)

def home(request):
    return render(request,'home.html')

def searchblog(request):
    print(request.POST)
    print(request.POST.get("keyword"))
    keyword = request.POST.get("keyword")
    blogs_search_list = Article.objects.filter(title__contains=keyword)
    content = get_blog_list_common_data(request, blogs_search_list)
    content["search_keyword"] = keyword
    return render(request, "blog_with_search.html", content)

#屏蔽掉这个验证
@csrf_exempt
def talk(request):
    url = "http://openapi.tuling123.com/openapi/api/v2"
    key = 'b8e17d600f50475c95052ab1dcedaa01'
    if request.method == 'POST':
        A_word = request.POST.get("data")
        #print(A_word)
        input_data = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": A_word
                },
                "selfInfo": {
                    "location": {
                        "city": "北京",
                        "province": "北京",
                        "street": "信息路"
                    }
                }
            },
            "userInfo": {
                "apiKey": key,
                "userId": "demo"
            }
        }
        req = json.dumps(input_data).encode("utf-8")
        http_post = urllib.request.Request(url, data=req, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(http_post)
        reponse_str = response.read()

        # 解析json
        reponse_dic = json.loads(reponse_str)
        # print(reponse_dic)
        intent_code = reponse_dic['intent']['code']
        res_text = reponse_dic['results'][0]['values']['text']
        #print(res_text)
        ret = {"word":res_text}
        return JsonResponse(ret)
    ret = {"back": "你好"}
    return JsonResponse(ret)