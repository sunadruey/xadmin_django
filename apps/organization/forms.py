from django import forms
from operation.models import UserAsk
import re

# class UseAskForm(forms.Form):
#     name = forms.CharField(required=True, max_length=20, min_length=2)
#     phone = forms.CharField(required=True, max_length=11, min_length=11)
#     course_name = forms.CharField(required=True, min_length=5, max_length=50)


class UseAskForm(forms.ModelForm):
    # 也可以save
    # 新增字段
    # my_field =forms.CharField()
    # 指定字段
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 自己定义字段的校验规则，命名规则clean开头  后面跟字段
    def clean_mobile(self):
        """
        验证手机号号码是否非法
        :return:
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[35678]\d{9}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法', code='mobile_invalid')





