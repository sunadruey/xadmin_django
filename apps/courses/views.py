from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse

from django.views.generic.base import View
from django.shortcuts import render

from operation.models import UserFavorite,CourseComments,UserCourse
from .models import Course,CourseResourse,Video
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.mixin_utils import LoginRequiredMixin

class CourseListView(View):

    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_num")[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            # i不区分大小写 类似mysql like语句
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))

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
        # course = video.lesson.course

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
            "has_fav_org": has_fav_org,


        })


class CourseInfoView(LoginRequiredMixin,View):

    def get(self, request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students+=1
        course.save()
        # 查询用户是否已经关联该课程
        user_courses =UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_cousers =UserCourse.objects.filter(course=course)

        user_ids = [ user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        relate_courses= Course.objects.filter(id__in=course_ids).order_by("-click_num")
        # 学过该课程的用户学过的其他课程
        all_resources= CourseResourse.objects.filter(course=course)
        return render(request, 'course-video.html', {
        "course": course,
        "course_resources": all_resources,
        "relate_courses": relate_courses

    })


class CommentsView(LoginRequiredMixin,View):

    def get(self, request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources= CourseResourse.objects.filter(course=course)

        all_comments= CourseComments.objects.all()

        return render(request, 'course-comment.html', {
        "course": course,
        "course_resources": all_resources,
        "all_comments" : all_comments

    })


class AddCommentsView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated:
            # 判断用户是否登录
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id",0)
        comments = request.POST.get("comments","")
        if int(course_id)>0 and len(comments) >0 :
            course_comments = CourseComments()
#             course为外键，外键传值必须为一个类
#             get方法只能取出一条数据  不存在会报错
            course =Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type='application/json')



class VideoPlayView(View):
    '''
    视频播放页面
    '''
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 增加课程点击数
        course.click_num += 1
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
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, 'course-play.html', {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "video": video

        })

