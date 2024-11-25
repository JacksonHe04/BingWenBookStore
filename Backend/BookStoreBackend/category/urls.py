# category/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("head/", views.get_response_data, name='category_list'),  # 查看单个分类详情
]
