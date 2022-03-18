from django.urls import path, include, re_path

from .views import UserInfoView,UploadImageView,UpdatePwdView
app_name = '[app_name]'
urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('image/upload', UploadImageView.as_view(), name='image_upload'),
    path('update/pwd', UpdatePwdView.as_view(), name='update_pwd'),

]
