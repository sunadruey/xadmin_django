from django.shortcuts import render
from django.views.generic import View

from operation.models import UserFavorite
from .models import CourseOrg, CityDict
# from django.shortcuts import render_to_response
from django.http import HttpResponse
from .forms import UseAskForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from courses.models import Course
# Create your views here.


class OrgView(View):

    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_num")[:3]
        # 直接统计modeL实例的数量
        org_nums = all_orgs.count()
        # 城市
        all_citys = CityDict.objects.all()

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category=request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这个地方可以换成查询数据库的记录。
        p = Paginator(all_orgs, 2, request=request)
        # 这里的数字5是每页显示的记录条数，官方例子没加这个参数，但是不加会报错。
        orgs = p.page(page)
        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UseAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')
#     异步的操作ajax操作 返回的json


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = 'home'
        # course_org = CourseOrg.objects.get(id=int(org_id))
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
#         取出机构所有的courses
#         all_orgs.filter(city_id=int(city_id))
#         all_courses = Course.objects.filter(course_org=course_org)[:4]
#         外键直接取出数据Course模块名小写，加_set,
        all_courses = course_org.course_set.all()[:2]
        all_teachers = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        # course_org = CourseOrg.objects.get(id=int(org_id))
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page ='course'
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=1):
                has_fav = True
#         取出机构所有的courses
#         all_orgs.filter(city_id=int(city_id))
#         all_courses = Course.objects.filter(course_org=course_org)[:4]
#         外键直接取出数据Course模块名小写，加_set,
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })



class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self, request, org_id):
        # course_org = CourseOrg.objects.get(id=int(org_id))
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page ='desc'
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=1):
                has_fav = True
#         取出机构所有的courses
#         all_orgs.filter(city_id=int(city_id))
#         all_courses = Course.objects.filter(course_org=course_org)[:4]
#         外键直接取出数据Course模块名小写，加_set,
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-desc.html', {

            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        })

class OrgTeacherView(View):
    """
    机构教师页
    """
    def get(self, request, org_id):
        # course_org = CourseOrg.objects.get(id=int(org_id))
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page ='teacher'
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=3):
                has_fav = True
#         取出机构所有的courses
#         all_orgs.filter(city_id=int(city_id))
#         all_courses = Course.objects.filter(course_org=course_org)[:4]
#         外键直接取出数据Course模块名小写，加_set,
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class AddFavView(View):
    ''''
    用户收藏 用户取消收藏
    '''

    def post(self,request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        # 判断用户是否登录
        if not request.user.is_authenticated:
            # 判断用户是否登录
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，则表示用户取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id)>0 and int(fav_type)>0:
                user_fav.user=request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')











