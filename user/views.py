#!/usr/bin/env python
# -*- conding:utf-8 -*-
# author: liusheng time:2019/6/2
import string
import random
import time
import re
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect,render
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import Profile
from .forms import loginForm, RegForm,ChangeNicknameForm,BindEmailForm,ChangePasswordForm,ForgotPasswordForm


def login_for_medal(request):
    login_form = loginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data["user"]
        auth.login(request, user)
        data["status"] = "SUCCESS"
    else:
        data["status"] = "ERROR"

    return JsonResponse(data)

def blog_login(request):
    # username = request.POST.get('username','')
    # user = authenticate(request, username=username, password=password)
    # #在请求头中找到发送请求的网页url，登录成功后就返回当前页面，（反向解析出index的路径，首页）
    # referer = request.META.get("HTTP_REFERER",reverse("index"))
    # if user is not None:
    #     return redirect(referer)
    if request.method == 'POST':
        login_form = loginForm(request.POST)
        if login_form.is_valid():
            # username = login_form.cleaned_data['username'],is_valid方法会执行到form的clean方法
            user = login_form.cleaned_data["user"]
            auth.login(request, user)
                # Redirect to a success page.
                # 解析出登录页面之前的页面的链接，并跳转到该页面，from为该页面传入的参数
            return redirect(request.GET.get('from',reverse('index')))

    else:
        # get
        login_form = loginForm()
    content = {}
    content["login_form"] = login_form
    # return render(request,'login.html',content)
    return render(request,'user/login.html',content)

def blog_register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST,request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data["username"]
            email = reg_form.cleaned_data["email"]
            password = reg_form.cleaned_data["password"]
            # 创建用户
            user = User.objects.create_user(username,email,password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            # 删除邮箱验证的会话
            del request.session['register_code']
            del request.session['send_code_time']
            del request.session['email']
            return redirect(request.GET.get('from',reverse('index')))
        else:
            print(reg_form.errors)
    else:
        reg_form = RegForm()
    content = {}
    content["reg_form"] = reg_form
    # return render(request,'register.html',content)
    return render(request,'user/register.html',content)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('index')))

def user_info(request):
    return render(request,"user/user_info.html")

# 修改昵称
def change_nickname(request):
    redirect_to = request.GET.get('from',reverse('index'))
    content = {}
    if request.method == "POST":
        form = ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            # 查询这个用户是否创建了昵称，然后进行修改保存
            profile,created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
        content['page_title'] = "修改昵称"
        content["form_title"] = "修改昵称"
        content["submit_text"] = "修改"
        content["my_style"] = "btn-primary"
        content['form'] = form
        content['return_back_url'] = redirect_to
        return render(request,'form.html',content)

def bind_email(request):
    redirect_to = request.GET.get('from', reverse('index'))
    content = {}
    if request.method == "POST":
        form = BindEmailForm(request.POST, request=request)

        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            del request.session['bind_email_code']
            del request.session['send_code_time']
            del request.session['email']
            return redirect(redirect_to)

    else:
        form = BindEmailForm()
    # get请求和绑定邮箱发生错误时进行下面
    content['page_title'] = "绑定邮箱"
    content["form_title"] = "绑定邮箱"
    content["submit_text"] = "绑定"
    content["my_style"] = "btn-primary"
    content['form'] = form
    content['return_back_url'] = redirect_to
    return render(request, 'user/bind_email.html', content)

def send_verification_code(request):
    email = request.GET.get('email','')
    end_for = request.GET.get('sendfor','')
    use = request.GET.get('use','绑定邮箱')
    data = {}
    c = re.compile(r'^\w+@(\w+\.)+(com|cn|net)$')
    searchobj1 = c.search(email)
    if email != '' and searchobj1:

        # 确定一个重复发送邮件的时间间隔
        now = int(time.time())
        send_code_time = request.session.get('send_code_time',0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
            data['info'] = '使用邮箱发送验证码前后时间不得小于30秒'
        else:
            # 生产验证码 string.ascii_letters表示所有的字母，string.digits表示所有的数字（0-9）
            code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
            request.session[end_for] = code
            request.session['send_code_time'] = now
            request.session['email'] = email
            request.session.set_expiry(300)
            # 发送邮件
            send_mail(
                use, # 标题
                '验证码：%s' % code,   # 正文
                '947172572@qq.com', # 邮箱来自哪里
                [email],            #  发送到哪里去
                fail_silently=False,  # 是否忽略错误
            )
            data['status'] = 'SUCCESS'
    else:
        data['info'] = "邮箱格式不正确"
        data['status'] = 'ERROR'

    return JsonResponse(data)

def change_password(request):
    redirect_to = reverse('index')
    content = {}
    if request.method == "POST":
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]
            user.set_password(new_password)
            user.save()
            # 修改密码后退出
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()
        content['page_title'] = "修改密码"
        content["form_title"] = "修改密码"
        content["submit_text"] = "修改"
        content["my_style"] = "btn-primary"
        content['form'] = form
        content['return_back_url'] = redirect_to
        return render(request, 'form.html', content)

def forgot_password(request):
    redirect_to = reverse('index')
    content = {}
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data["email"]
            new_password = form.cleaned_data["new_password"]
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            del request.session["forgot_password_code"]
            del request.session['send_code_time']
            del request.session['email']
            return redirect(redirect_to)

    else:
        form = ForgotPasswordForm()
    # get请求和绑定邮箱发生错误时进行下面
    content['page_title'] = "忘记密码"
    content["form_title"] = "重置密码"
    content["submit_text"] = "重置"
    content["my_style"] = "btn-primary"
    content['form'] = form
    content['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', content)