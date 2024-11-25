# category/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("brand", views.top_selling_authors, name="top_selling_authors"),  # 查看单个分类详情
    path("stock/<int:id>", views.get_book_stock, name='get_book_stock'),
    path("", views.get_book_details, name="get_book_details"),
]
