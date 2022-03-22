# -*- coding: utf-8 -*-
# @Time : 2022/1/4 4:53 下午
# @Author : zhaoshuangmei
# @File : adminx

import xadmin
from organization.models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):

    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc', ]
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):

    list_display = ['name', 'desc',  'fav_nums', 'click_num', 'city', 'address', 'add_time']
    search_fields = ['name', 'desc',  'fav_nums', 'click_num', 'city', 'address']
    list_filter =['name', 'desc',  'fav_nums', 'click_num', 'city', 'address', 'add_time']
#     设置课程机构可搜索
    relfield_style ='fk_ajax'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'points', 'click_num', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'points', 'click_num', 'fav_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'points', 'click_num', 'fav_nums', 'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)