from datetime import datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):

   name = models.CharField(max_length=20, verbose_name=u'城市')
   desc = models.CharField(max_length=200, verbose_name=u"城市描述")
   add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

   class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

   def __str__(self):
        return self.name


class CourseOrg(models.Model):
   name = models.CharField(max_length=50, verbose_name=u'机构名称')
   desc = models.CharField(max_length=300, verbose_name=u"机构描述")
   tag = models.CharField(max_length=10, default=u'全国著名' ,verbose_name=u'机构标签')
   category = models.CharField(max_length=20, verbose_name=u"培训机构", default="pxjg", choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")))
   click_num = models.IntegerField(default=0, verbose_name=u'点击数')
   fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
   image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u'封面图', max_length=100, blank=True, null=True)
   address = models.CharField(max_length=150, verbose_name=u"机构地址")
   city = models.ForeignKey(CityDict, on_delete=models.CASCADE, verbose_name=u'所在城市')
   students = models.IntegerField(default=0, verbose_name=u'学习人数')
   course_nums = models.IntegerField(default=0, verbose_name=u'课程数')
   add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

   class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

   def __str__(self):
       return self.name


   def get_teacher_nums(self):
       # 获取课程机构的教室数量
       return self.teacher_set.all().count()


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name=u'所属机构')
    name = models.CharField(max_length=50, verbose_name=u'教师名')
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name=u'封面图', max_length=100)
    age = models.IntegerField(default=10,blank=True, null=True, verbose_name=u'年龄')
    work_years = models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'公司职位')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_nums(self):
        return self.course_set.all().count()


