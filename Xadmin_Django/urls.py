"""Xadmin_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
import xadmin
# from users.views import user_login,IndexView
from users.views import IndexView

from users.views import LoginView, RegisterView, AciveUserView, ForgetPwdView, ResetView,ModifyPwdView,LogoutView
from users.views import LoginUnsafeView
from organization.views import OrgView
from django.views.static import serve
from Xadmin_Django.settings import MEDIA_ROOT

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    # path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('', IndexView.as_view(), name='index'),
    # path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    # path('login/', user_login, name='login')

    path('login/', LoginView.as_view(), name='login'),
    # 不安全登录
    # path('login/', LoginUnsafeView.as_view(), name='login'),
    # 退出登录
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', RegisterView.as_view(), name='register'),

    path('captcha/', include('captcha.urls')),
    re_path('active/(?P<active_code>.*)/$', AciveUserView.as_view(), name='user_active'),
    re_path('reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构url配置
    path('org/', include('organization.urls', namespace='org')),



    # 课程app相关url配置
    path("course/", include('courses.urls', namespace="course")),

    # 用户相关的配置
    path("users/", include('users.urls', namespace="users")),

   # # 讲师app相关url配置
   #  path("teacher/", include('teacher.urls', namespace="teacher")),


    # 配置上传文件的访问处理函数
    re_path('media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),
    # DEBUG = False时不会访问静态数据，需要手动添加
    # re_path('static/(?P<path>.*)/$', serve, {"document_root": STATIC_ROOT}),
    # 富文本相关url
    path('ueditor/', include('DjangoUeditor.urls')),

]
# 全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
