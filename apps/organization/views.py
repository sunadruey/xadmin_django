from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from .models import CourseOrg,CityDict


class OrgView(View):

    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 直接统计modeL实例的数量
        org_nums = all_orgs.count()
        # 城市
        all_citys = CityDict.objects.all()

        return render(request, "org-list.html", {
            "all_orgs": all_orgs,
            "all_citys": all_citys,
            "org_nums": org_nums

        })

