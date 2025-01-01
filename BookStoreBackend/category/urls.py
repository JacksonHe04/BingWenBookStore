# category/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_category_view, name='category_list'),  # 查看单个分类详情
    path("/sub/filter", views.get_subcategory_filter_view, name='subcategory_list'),
]
