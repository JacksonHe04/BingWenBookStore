import os
import django
import pandas as pd
from decimal import Decimal
import random
from datetime import datetime

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookStoreBackend.settings')
django.setup()

# 导入模型
from product.models import Author,Publisher,Book
from category.models import Category,SubCategory


def parse_date(date_str):
    """解析日期字符串"""
    if pd.isna(date_str):
        return None

    date_str = str(date_str)

    try:
        # 尝试多种日期格式
        formats = [
            '%Y/%m/%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d',
            '%Y-%m-%d'
        ]

        for date_format in formats:
            try:
                return datetime.strptime(date_str, date_format).date()
            except:
                continue

        # 如果是Excel的日期数字格式，使用pandas转换
        try:
            return pd.to_datetime(date_str).date()
        except:
            pass

        print(f"无法解析的日期格式: {date_str}")
        return None

    except Exception as e:
        print(f"日期解析错误 ({date_str}): {str(e)}")
        return None


def generate_reasonable_numbers(comment_count):
    """生成合理的库存和销售量"""
    comment_count = int(comment_count) if pd.notna(comment_count) else 0

    if comment_count > 500000:
        base_sales = random.randint(50000, 100000)
    elif comment_count > 100000:
        base_sales = random.randint(10000, 50000)
    elif comment_count > 10000:
        base_sales = random.randint(5000, 10000)
    elif comment_count > 1000:
        base_sales = random.randint(1000, 5000)
    else:
        base_sales = random.randint(100, 1000)

    monthly_sales = base_sales // 12
    inventory = random.randint(monthly_sales * 2, monthly_sales * 4)

    return inventory, base_sales


def import_book_data(row):

    """导入单行图书数据"""
    try:
        # 打印原始日期值用于调试
        # print(f"处理图书: {row['title']}")
        # print(f"原始日期值: {row['createTime']}")
        # print(f"日期值类型: {type(row['createTime'])}")

        # 1. 创建或获取分类
        category, _ = Category.objects.get_or_create(
            name=row['category'],
            defaults={'picture': None}
        )

        # 2. 创建或获取子分类
        subcategory, _ = SubCategory.objects.get_or_create(
            name=row['subcategory'],
            parent=category,
            defaults={
                'picture': None,
                'sale_properties': {}
            }
        )

        # 3. 处理作者
        author_text = str(row['author'])
        author_name = author_text.split('著')[0].strip()
        author, _ = Author.objects.get_or_create(
            name=author_name,
            defaults={
                'desc': "暂无数据",
                'place': "暂无数据"
            }
        )

        # 4. 创建或获取出版社
        publisher, _ = Publisher.objects.get_or_create(
            name=row['press'],
            defaults={
                'desc': "暂无数据",
                'place': "暂无数据"
            }
        )

        # 5. 生成合理的库存和销售数据
        inventory, sales = generate_reasonable_numbers(row['comment_num'])

        # 6. 解析出版日期
        # 解析出版日期
        publish_date = parse_date(row['createTime'])
        # print(f"解析后的日期: {publish_date}")


        # 7. 创建图书
        book, created = Book.objects.get_or_create(
            ISBN=row['ISBN'],
            defaults={
                'name': row['title'],
                'desc': row['detail'] if pd.notna(row['detail']) else "暂无数据",
                'discount': int(float(row['discount']) * 10),
                'old_price': Decimal(str(row['pre_price'])),
                'inventory': inventory,
                'publisher': publisher,
                'subcategory': subcategory,
                'collect_count': int(sales * random.uniform(0.05, 0.15)),
                'sales_count': sales,
                'comment_count': int(row['comment_num']) if pd.notna(row['comment_num']) else 0,
                'main_pictures': row['img_url'] if pd.notna(row['img_url']) else None,
                'publish_date': publish_date
            }
        )

        # 8. 添加作者关系
        if created:
            book.authors.add(author)

        return True, f"成功导入图书: {book.name} (销量: {sales}, 库存: {inventory}, 出版日期: {publish_date})"

    except Exception as e:
        return False, f"导入错误: {str(e)}"


def main():
    # 读取Excel文件
    excel_path = r'D:\Users\15654\PycharmProjects\BingWenBookStore\Backend\BookStoreBackend\modified_data_with_isbn.xlsx'  # 替换为你的Excel文件路径

    try:
        df = pd.read_excel(excel_path)

        success_count = 0
        error_count = 0

        for index, row in df.iterrows():
            success, message = import_book_data(row)
            if success:
                success_count += 1
                print(f"✓ {message}")
            else:
                error_count += 1
                print(f"✗ {message}")

        print(f"\n导入完成:")
        print(f"成功导入: {success_count} 本图书")
        print(f"导入失败: {error_count} 本图书")

    except Exception as e:
        print(f"读取Excel文件错误: {str(e)}")


if __name__ == '__main__':
    main()