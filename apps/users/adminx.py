# -*- coding: utf-8 -*-
# @Time : 2022/1/4 11:32 上午
# @Author : Hao
# @File : adminx
import xadmin
from users.models import EmailVerifyRecord, Banner, UserProfile
from xadmin import views
# 引入这个模块
# from xadmin.plugins.auth import UserAdmin
#
# class UserProfileAdmin(UserAdmin):
#     pass

class BaseSetting(object):
    # 使用主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '肖战网站'
    site_footer = '我的网址底部'
    menu_style = 'accordion'



class EmailVerifyRecordAdmin(object):

    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    # font-awesome的替换 https://fontawesome.com/
    model_icon = 'fa fa-address-book-o'


class BannerAdmin(object):

    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']

# from django.contrib.auth.models import User
# xadmin.site.unregister(User)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

