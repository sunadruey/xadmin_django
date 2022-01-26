from django import forms
from operation.models import UserAsk


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
        model= UserAsk
        fields=['name', 'mobile', 'course_name']
