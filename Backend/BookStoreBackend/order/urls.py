# category/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('/pre', views.create_order_summary_and_save, name='order_summary'),
    path('/<int:id>', views.get_order_detail, name='order_detail'),
]
