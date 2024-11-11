# category/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),  # 查看单个分类详情
    path("code", views.UserVerificationView.as_view(), name="mobile_code"),
]
