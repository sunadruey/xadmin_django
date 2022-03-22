from datetime import datetime

from django.db import models
from organization.models import CourseOrg,Teacher
# from DjangoUeditor.models import UEditorField


# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u'课程机构', blank=True, null=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    youneed_know = models.CharField(max_length=300,default="", blank=True, null=True, verbose_name=u"课程须知")
    teacher_tell= models.CharField(max_length=300, default="", blank=True, null=True, verbose_name=u"教师告知")
    detail = models.TextField(verbose_name=u'课程详情')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播图')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', "中级"), ('gj', '高级')), verbose_name=u'难度', max_length=2)
    theacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, verbose_name=u'讲师', blank=True, null=True)
    learn_time = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u'封面图', max_length=100)
    category= models.CharField(  max_length=20,default=u"后端开发", blank=True, null=True, verbose_name=u'课程类别')
    tag = models.CharField(  max_length=20, default="", blank=True, null=True, verbose_name=u'课程标签')
    click_num = models.IntegerField(default=0, verbose_name=u'点击人数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    def get_learn_users(self):
        # 学习人数
        return self.usercourse_set.all()[:3]

    def get_course_lesson(self):
        # 获取章节数
        return self.lesson_set.all()[:3]

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = u"轮播课程"
        verbose_name_plural = verbose_name
        proxy = True

class Lesson(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        # 获取视频数
        return self.video_set.all()[:3]

    def __str__(self):
        return self.name



class Video(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,  verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.CharField(max_length=200, default=u"", blank=True, null=True,verbose_name=u'视频地址')
    learn_time = models.IntegerField(default=0, verbose_name=u'视频时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResourse(models.Model):
    course = models.ForeignKey(Course,  on_delete=models.CASCADE,verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(upload_to='course/resource/%Y/%m',verbose_name=u'资源文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name








