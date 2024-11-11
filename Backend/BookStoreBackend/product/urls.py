# category/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.top_selling_authors,name="top_selling_authors"),  # 查看单个分类详情
]
