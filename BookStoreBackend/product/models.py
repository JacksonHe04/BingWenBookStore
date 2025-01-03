from django.db import models
from category.models import SubCategory

# Create your models here.


# 作家
class Author(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='author_pictures/', null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = '作家'
        verbose_name_plural = '作家表'

    def __str__(self):
        return self.name


# 出版商
class Publisher(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='publisher_logos/', null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='publisher_pictures/', null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = '出版商'
        verbose_name_plural = '出版商表'

    def __str__(self):
        return self.name


# 商品详情（书籍）
class Book(models.Model):
    ISBN = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    discount = models.IntegerField()
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    authors = models.ManyToManyField(Author, related_name='books')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='books')
    collect_count = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    main_pictures = models.URLField(max_length=500, null=True, blank=True)
    publish_date = models.DateField(null=True, blank=True)
    # 属性picture string
    # picture = models.TextField(null=True, blank=True)


    class Meta:
        verbose_name = '书籍'
        verbose_name_plural = '书籍表'

    def __str__(self):
        return self.name