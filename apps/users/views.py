from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.backends import ModelBackend
import json
from utils.mixin_utils import LoginRequiredMixin
from .models import UserProfile, EmailVerifyRecord
from django.db.models import Q
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm,UploadImageForm,UserInfoForm
from django.contrib.auth.hashers import make_password
from users.utils.email_send import send_register_email
from django.http import HttpResponse,HttpResponseRedirect
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from courses.models import Course
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


# 判断账号时候激活
class AciveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


# 注册账号
class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})

            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 明文密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
#             写入欢迎注册消息
            user_message =UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学在线网"
            user_message.save()

#             发送邮箱
            send_register_email(user_name, 'register')
            return render(request, 'login.html', {})
        else:
            return render(request, 'register.html', {'register_form': register_form})


# 类登录方式
class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {"msg": "账号未激活!"})
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误!"})
        else:
            return render(request, 'login.html', {"login_form": login_form})


# 邮件登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 自己的后台逻辑
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LogoutView(View):
    def get(self,request):
        '''

        用户登出
        '''
        logout(request)
#         重定向到另一个页面
        from django.urls import reverse
        return HttpResponseRedirect(reverse("index"))


# 账号登录
def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get('username', '')
        pass_word = request.POST.get('password', '')
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {"msg": "用户名或密码错误!"})
    elif request.method == "GET":
        return render(request, 'login.html', {})

# 忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form":forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})

# 重置密码
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})

        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")

# """
#     修改用户密码
#     """
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password_old", "")
            pwd2 = request.POST.get("password_new", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin,View):
    """
    用户的个人信息
    """
    def get(self,request):
        return render(request,'usercenter-info.html',{})

    def post(self,request):
        user_info_form =UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')





class UploadImageView(LoginRequiredMixin,View):
    """
    用户修改头像
    """

    def post(self,request):
        image_form =UploadImageForm( request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            # image =image_form.cleaned_data['image']
            # request.user.image=image
            # request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


# 个人中心修改密码
class UpdatePwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")

            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user =request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:

            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    '''
    发送邮箱验证码
    '''
    def get(self,request):
        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email,'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    '''
    修改个人邮箱
    '''

    def post(self,request):

        email = request.POST.get('email','')
        code = request.POST.get('code','')

        existed_records =EmailVerifyRecord.objects.filter(email='email',code='email',send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()

        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin,View):
    '''
    我的课程
    '''

    def get(self,request):

        user_courses =UserCourse.objects.filter(user=request.user)

        return render(request,'usercenter-mycourse.html',{
            'user_courses':user_courses
        })

class MyFavOrgView(LoginRequiredMixin,View):
    '''
    我收藏的课程机构
    '''

    def get(self,request):
        org_list=[]
        fav_orgs =UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request,'usercenter-fav-org.html',{
            'org_list':org_list,
        })



class MyFavTeacherView(LoginRequiredMixin,View):
    '''
    我收藏的授课讲师
    '''

    def get(self,request):
        teacher_list=[]
        fav_teachers =UserFavorite.objects.filter(user=request.user,fav_type=3)

        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request,'usercenter-fav-teacher.html',{
            'teacher_list':teacher_list,
        })




class MyFavCourseView(LoginRequiredMixin,View):
    '''
    我收藏的授课讲师
    '''

    def get(self,request):
        course_list=[]
        fav_courses =UserFavorite.objects.filter(user=request.user,fav_type=1)

        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request,'usercenter-fav-course.html',{
            'course_list':course_list,
        })

class MymessageView(LoginRequiredMixin,View):
    '''
    我的消息
    '''

    def get(self,request):

        all_messages =UserMessage.objects.filter(user=request.user.id)
        # 用户进入个人中心后清空未读消息，清空自己的
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对我的消息分页,无数据报错
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这个地方可以换成查询数据库的记录。
        p = Paginator(all_messages, 1, request=request)
        # 这里的数字5是每页显示的记录条数，官方例子没加这个参数，但是不加会报错。
        messages = p.page(page)
        return render(request,'usercenter-message.html',{
            "messages": messages,
        })


