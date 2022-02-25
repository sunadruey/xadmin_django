from django.urls import path, include, re_path
from .views import CourseListView

app_name = '[app_name]'
urlpatterns = [
    # 课程列表页
    path('list/', CourseListView.as_view(), name='course_list'),


]
