# -*- coding: utf-8 -*-
# @Time : 2022/1/4 5:03 下午
# @Author : zhaoshuangmei
# @File : adminx
import xadmin
from .models import UserAsk, CourseComments, UserFavorite, UserMessage,UserCourse


class UserAskAdmin(object):
    list_display = ['name', 'mobile',  'course_name', 'add_time']
    search_fields = ['name', 'mobile',  'course_name']
    list_filter = ['name', 'mobile',  'course_name', 'add_time']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course',  'comments', 'add_time']
    search_fields = ['user', 'course',  'comments']
    list_filter = ['user', 'course',  'comments', 'add_time']


class UserFavoriteAdmin(object):

    list_display = ['user', 'fav_id',  'fav_type']
    search_fields = ['user', 'fav_id',  'fav_type']
    list_filter = ['user', 'fav_id',  'fav_type']


class UserMessageAdmin(object):

    list_display = ['user', 'message',  'has_read', 'add_time']
    search_fields = ['user', 'message',  'has_read']
    list_filter = ['user', 'message',  'has_read', 'add_time']


class CourseCourseAdmin(object):

    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, CourseCourseAdmin)