# -*- coding: utf-8 -*-
# @Time : 2022/1/4 4:20 下午
# @Author : zhaoshuangmei
# @File : adminx
import xadmin
from .models import Course,CourseResourse,Video,Lesson,BannerCourse
from organization.models import CourseOrg


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResourse
    extra = 0


class CourseAdmin(object):

    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'click_num', 'add_time','get_zj_nums','go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'click_num']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'click_num', 'add_time']
    # 进入列表，点击次数倒叙排列，
    ordering = ['-click_num']
    # 设置字段只读
    readonly_fields = ['click_num']
    # 默认隐藏字段和readonly_fields冲突 字段不能一样
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]
    # 在列表页可直接修改
    list_editable = ['degree','desc']
    # 设置页面定时刷新
    refresh_times = [3,5]

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()



class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'click_num', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'click_num']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums', 'click_num', 'add_time']
    # 进入列表，点击次数倒叙排列，
    ordering = ['-click_num']
    # 设置字段只读
    readonly_fields = ['click_num']
    # 默认隐藏字段和readonly_fields冲突 字段不能一样
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


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

xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResourse, CourseResourseAdmin)


