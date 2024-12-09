from django.db import models


# Create your models here.
# 一级分类
class Category(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='category_pictures/', null=True, blank=True)

    class Meta:
        verbose_name = '一级分类'
        verbose_name_plural = '一级分类表'



    def __str__(self):
        return self.name


# 二级分类
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='subcategory_pictures/', null=True, blank=True)
    sale_properties = models.JSONField(null=True, blank=True)  # 销售属性为 JSON 格式
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")  # 一级分类和二级分类：一对多

    class Meta:
        verbose_name = '二级分类'
        verbose_name_plural = '二级分类表'

    def __str__(self):
        return self.name
