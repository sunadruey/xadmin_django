from django.urls import path, include
from .views import OrgView
app_name='[app_name]'
urlpatterns = [
    # 课程机构首页列表
    path('list/', OrgView.as_view(), name='org_list'),
]