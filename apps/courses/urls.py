from django.urls import path, include, re_path
from .views import CourseListView,CourseDetailView,CourseInfoView

app_name = '[app_name]'
urlpatterns = [
    # 课程列表页
    path('list/', CourseListView.as_view(), name='course_list'),
    re_path('detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    re_path('info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    # 机构收藏



]
