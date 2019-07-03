#!/usr/bin/env python
# -*- conding:utf-8 -*-
# author: liusheng time:2019/5/3
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class loginForm(forms.Form):
    username = forms.CharField(label="用户名", widget=forms.TextInput(attrs={"class":"form-control","placeholder":"用户名"}), required=True)   #默认为True
    password = forms.CharField(label="密码", widget=forms.PasswordInput(attrs={'class':'form-control',"placeholder":"用户密码"}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            # Django提供的form的错误信息接口
            raise forms.ValidationError('用户名或者密码不正确')
        else:
            #写回user
            self.cleaned_data["user"] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label="用户名",max_length="30",min_length=3,
                               widget=forms.TextInput(attrs={"class":"form-control","placeholder":"输入3-30之间的用户名"}), required=True)
    email = forms.EmailField(label="用户邮箱",
                             widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"填写用户邮箱"}), required=True)
    password = forms.CharField(label="设置密码", min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control',"placeholder":"设定用户密码"}))
    password_again = forms.CharField(label="再输入一次密码",min_length=6,
                                     widget=forms.PasswordInput(attrs={'class':'form-control',"placeholder":"再次输入用户密码"}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists() > 0:
            raise forms.ValidationError("用户名已经存在！")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() > 0:
            raise forms.ValidationError("该邮箱已经注册过！")
        return email

    def clean_password_again(self):
        password_again = self.cleaned_data['password_again']
        password = self.cleaned_data['password']
        if password != password_again:
            raise forms.ValidationError("两次输入的密码不相同！")
        return password_again