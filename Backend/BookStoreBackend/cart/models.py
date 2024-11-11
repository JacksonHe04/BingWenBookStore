from django.db import models
from user.models import User
from product.models import Book


# Create your models here.

# 购物车
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    books = models.ManyToManyField(Book, related_name='carts')  # 购物车和书籍：多对多
    count = models.IntegerField(default=1)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='cart_pictures/', null=True, blank=True)
    post_fee = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = '购物车表'

    def __str__(self):
        return f"{self.user.nickname}'s Cart"
