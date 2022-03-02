from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse

from django.views.generic.base import View
from django.shortcuts import render

from operation.models import UserFavorite
from .models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

class CourseListView(View):

    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_num")[:3]

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_num")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这个地方可以换成查询数据库的记录。
        p = Paginator(all_courses, 3, request=request)
        # 这里的数字5是每页显示的记录条数，官方例子没加这个参数，但是不加会报错。
        courses = p.page(page)
        return render(request, 'course-list.html', {
            # 传递分页后的数据
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,

        })

class CourseDetailView(View):
    """
    课程详情页

    """

    def get(self, request,course_id):
        course= Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_num+=1
        course.save()

        has_fav_course = False
        has_fav_org = False
        # 判断用户是否登录
        if request.user.is_authenticated:
            # 判断用户是否登录
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            relate_courses =Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org

        })