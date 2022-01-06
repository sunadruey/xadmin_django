# -*- coding: utf-8 -*-
# @Time : 2022/1/6 11:51 上午
# @Author : zhaoshuangmei
# @File : forms

from django import forms


class LoginForm(forms.Form):
    # 变量值和html中的变量值名称保持一致
    username = forms.CharField(required=True, min_length=5)
    password = forms.CharField(required=True,min_length=3)
