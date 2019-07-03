#!/usr/bin/env python
# -*- conding:utf-8 -*-
# author: liusheng time:2019/6/6
from .forms import loginForm


def login_model_form(request):
    return {'login_model_form':loginForm()}