from django.urls import path,include
from . import views
urlpatterns = [
    path('login/',views.blog_login,name='blog_login'),
    path('login_for_medal',views.login_for_medal,name='login_for_medal'),
    path('register',views.blog_register,name="blog_register"),
    path('logout/',views.logout,name="logout"),
    path('user_info/',views.user_info,name="user_info"),
    path('change_nickname/',views.change_nickname,name="change_nickname"),
    path('bind_email/',views.bind_email,name="bind_email"),
    path('bind_email_code/',views.send_verification_code,name="bind_email_code"),
    path('change_password/', views.change_password, name="change_password"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
]