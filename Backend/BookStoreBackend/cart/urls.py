from django.urls import path
from .views import merge_cart,cart_view

urlpatterns = [
    path('/merge', merge_cart, name='merge_cart'),
    path('', cart_view, name='cart'),
]
