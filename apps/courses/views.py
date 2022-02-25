from django.core.paginator import PageNotAnInteger
from django.views.generic.base import View
from django.shortcuts import render
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