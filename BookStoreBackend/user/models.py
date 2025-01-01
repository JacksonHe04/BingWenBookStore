from django.db import models

# Create your models here.
# 用户
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, account, password=None, **extra_fields):
        if not account:
            raise ValueError("必须提供账号")
        user = self.model(account=account, **extra_fields)
        user.set_password(password)  # 使用 set_password 加密
        user.save(using=self._db)
        return user

    def create_superuser(self, account, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(account, password, **extra_fields)


class User(AbstractBaseUser):
    account = models.CharField(max_length=50, unique=True)
    avatar = models.ImageField(upload_to='user_avatars/', null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    city_code = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    nickname = models.CharField(max_length=50)
    profession = models.CharField(max_length=100)
    province_code = models.CharField(max_length=20)
    token = models.CharField(max_length=100)
    password = models.CharField(max_length=128, default="default_password")  # 新增的 password 字段，带有默认值

    objects = UserManager()

    USERNAME_FIELD = 'account'  # 指定账号字段
    REQUIRED_FIELDS = []  # 创建超级用户时仅需要 account 和 password

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.nickname


# 收货地址
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')  # 用户和收货信息：一对多
    address = models.CharField(max_length=255)
    address_tags = models.CharField(max_length=20, null=True, blank=True)
    city_code = models.CharField(max_length=20)
    contact = models.CharField(max_length=50)
    county_code = models.CharField(max_length=20)
    full_location = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    province_code = models.CharField(max_length=20)
    receiver = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = '收货地址表'

    def __str__(self):
        return f"{self.receiver} - {self.full_location}"
