from django.urls import path, include, re_path
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentsView,AddCommentsView,VideoPlayView

app_name = '[app_name]'
urlpatterns = [
    # 课程列表页
    path('list/', CourseListView.as_view(), name='course_list'),
    re_path('detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    re_path('info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    # 课程评论
    re_path('comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name='course_comments'),
    # 添加课程评论
    path('add_comment/$', AddCommentsView.as_view(), name='add_comment'),
    re_path('video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),

]
