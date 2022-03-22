# -*- coding: utf-8 -*-
# @Time : 2022/1/4 4:20 下午
# @Author : zhaoshuangmei
# @File : adminx
import xadmin
from .models import Course,CourseResourse,Video,Lesson


class CourseAdmin(object):

    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'click_num', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'click_num']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'click_num', 'add_time']
    # 进入列表，点击次数倒叙排列，
    ordering = ['-click_num']
    # 设置字段只读
    readonly_fields = ['click_num']
    # 默认隐藏字段和readonly_fields冲突 字段不能一样
    exclude = ['fav_nums']





class LessonAdmin(object):

    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):

    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourseAdmin(object):

    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']



xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResourse, CourseResourseAdmin)


