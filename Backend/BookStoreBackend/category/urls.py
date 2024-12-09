# category/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("head", views.get_response_data),  # 查看单个分类详情
]
