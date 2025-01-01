
import os
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookStoreBackend.settings')
django.setup()

import img_urls
from category.models import SubCategory,Category
from product.models import Author

def update_subcategory_pictures():
    """根据子分类和父分类的组合更新子分类的图片链接"""
    for key, url in img_urls.sub_urls.items():
        if isinstance(key, tuple):
            # 情况1：如果 key 是元组 (sub_name, parent_name)
            sub_name, parent_name = key
            try:
                # 查找父分类
                parent_category = Category.objects.get(name=parent_name)
                # 查找子分类
                sub_category = SubCategory.objects.get(name=sub_name, parent=parent_category)
                # 更新图片链接
                sub_category.picture = url
                sub_category.save()
                print(f"已更新分类 '{sub_name}' (父分类: '{parent_name}') 的图片链接为 {url}")
            except Category.DoesNotExist:
                print(f"父分类 '{parent_name}' 不存在，跳过更新")
            except SubCategory.DoesNotExist:
                print(f"子分类 '{sub_name}' (父分类: '{parent_name}') 不存在，跳过更新")
        else:
            # 情况2：如果 key 只是一个子分类名称
            sub_name = key
            try:
                # 只根据子分类名称查找
                sub_category = SubCategory.objects.get(name=sub_name)
                # 更新图片链接
                sub_category.picture = url
                sub_category.save()
                print(f"已更新分类 '{sub_name}' 的图片链接为 {url}")
            except SubCategory.DoesNotExist:
                print(f"子分类 '{sub_name}' 不存在，跳过更新")

def update_author_pictures():
    """将图片链接更新到对应的作家记录"""
    for name, url in img_urls.writer_urls.items():
        try:
            # 查找对应的 Author 实例
            author = Author.objects.get(name=name)
            # 更新图片链接到 picture 字段
            author.picture = url
            author.save()
            print(f"已更新作家 '{name}' 的图片链接为 {url}")
        except Author.DoesNotExist:
            print(f"作家 '{name}' 不存在，跳过更新")


# 调用更新函数
update_subcategory_pictures()
# 调用更新函数
update_author_pictures()
