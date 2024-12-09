# category/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),  # 查看单个分类详情
    path("code", views.UserVerificationView.as_view(), name="mobile_code"),
    path('address', views.address_method, name='address_list'),  # 获取或添加地址
    path('address/<str:id>', views.address_edit_delete, name='address_detail'),  # 删除特定地址
]
