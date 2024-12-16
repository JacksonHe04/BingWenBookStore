from django.db import models
from user.models import User, Address
from product.models import Book


class Order(models.Model):
    """
    订单模型
    """
    ORDER_STATUS = (
        ('PENDING', '待支付'),
        ('PAID', '已支付'),
        ('SHIPPED', '已发货'),
        ('COMPLETED', '已完成'),
        ('CANCELLED', '已取消'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_pay_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    post_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    # 添加新的字段
    delivery_time_type = models.IntegerField(default=0)
    pay_type = models.IntegerField(default=0)
    pay_channel = models.IntegerField(default=0)
    buyer_message = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单表"

    def __str__(self):
        return f"订单 #{self.id} - 用户 {self.user.nickname}"


class OrderItem(models.Model):
    """
    订单商品模型
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='order_items')
    count = models.IntegerField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_pay_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "订单商品"
        verbose_name_plural = "订单商品表"

    def __str__(self):
        return f"订单商品 #{self.id} - {self.book.name}"


class Payment(models.Model):
    """
    支付信息模型
    """
    PAYMENT_METHODS = (
        ('CREDIT_CARD', '信用卡'),
        ('PAYPAL', 'PayPal'),
        ('WECHAT', '微信支付'),
        ('ALIPAY', '支付宝'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='CREDIT_CARD')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "支付信息"
        verbose_name_plural = "支付信息表"

    def __str__(self):
        return f"支付信息 #{self.id} - 订单 #{self.order.id}"
