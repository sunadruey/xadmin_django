from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class OrgView(View):

    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
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
            "category":category,
        })

