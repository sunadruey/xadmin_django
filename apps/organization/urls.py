from django.urls import path, include
from .views import OrgView, AddUserAskView,OrgHomeView
app_name = '[app_name]'
urlpatterns = [
    # 课程机构首页列表
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_ask/', AddUserAskView.as_view(), name='add_ask'),
    path('home/(?P<org_id>\d+)', OrgHomeView.as_view(), name='org_home')

]