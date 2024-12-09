import os
import django
from django.core.files import File

# 设置 Django 环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BookStoreBackend.settings")  # 替换为你的项目名称
django.setup()

from product.models import Author  # 替换为你的应用名称


def import_author_images():
    # 设置图片文件夹路径
    images_dir = r"D:\数据库原理\writer"  # 替换为你的图片路径

    # 检查目录是否存在
    if not os.path.exists(images_dir):
        print(f"目录 {images_dir} 不存在，请检查路径！")
        return

    # 遍历图片文件夹中的所有文件
    for filename in os.listdir(images_dir):
        # 获取文件名和扩展名
        name, ext = os.path.splitext(filename)

        # 检查文件是否是有效图片
        if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            try:
                # 查找对应的作家
                author = Author.objects.get(name=name)
                file_path = os.path.join(images_dir, filename)

                # 打开图片文件并保存到 Author.picture 字段
                with open(file_path, 'rb') as f:
                    author.picture.save(filename, File(f))
                    author.save()

                print(f"成功导入图片: {filename} 对应 {author.name}")
            except Author.DoesNotExist:
                print(f"未找到匹配的作家: {name}")
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {e}")


if __name__ == "__main__":
    import_author_images()
