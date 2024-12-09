from django.db import models
from user.models import User
from product.models import Book


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    # 移除多对多关系，因为我们将使用 CartItem 来处理


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cart_items')
    count = models.IntegerField(default=1)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
