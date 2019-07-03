
from django.urls import path
from blog import views

urlpatterns = [
    #localhost:8000/article/
    path('', views.article_list, name="article_list"),
    path('<int:article_id>', views.article_detail, name='article_detail'),
    path('type/<int:blog_type_pk>',views.blogs_with_type,name='blog_with_type'),
    path('date/<int:year>/<int:month>',views.blogs_with_date,name='blog_with_date'),
    # path('login/',views.blog_login,name='blog_login'),
    # path('login_for_medal',views.login_for_medal,name='login_for_medal'),
    # path('register',views.blog_register,name="blog_register"),
    path('home',views.home),
    path('talk/',views.talk),
    path('searchblog/',views.searchblog,name="searchblog"),
]
