from django.db.models import Sum
from django.http import JsonResponse
from product.models import Author
from django.shortcuts import get_object_or_404
from .models import Book
from decimal import Decimal
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


def top_selling_authors(request):
    # 获取 limit 参数并设置默认值为 1
    limit = int(request.GET.get('limit', 10))

    # 统计每位作家的书籍总销量
    authors_with_sales = Author.objects.annotate(total_sales=Sum('books__sales_count'))

    # 按销量总和降序排列，并限制返回数量
    top_authors = authors_with_sales.order_by('-total_sales')[:limit]

    # 构建结果列表
    results = [
        {
            "author_id": author.id,
            "author_name": author.name,
            "desc": author.desc,
            "picture": request.build_absolute_uri(author.picture) if author.picture else None,
            "place": author.place,
            "total_sales": author.total_sales
        }
        for author in top_authors
    ]

    # 返回结果
    response_data = {
        "code": "200",
        "msg": "Success",
        "result": results
    }

    return JsonResponse(response_data)


def get_book_stock(request, id):
    # 根据 ID 查找书籍
    book = get_object_or_404(Book, id=id)

    # 构造返回数据
    response_data = {
        "code": "200",
        "msg": "获取书籍库存成功",
        "result": {
            "nowPrice": round(float(book.old_price) * (book.discount / 100), 2),  # 计算折后价格
            "oldPrice": round(float(book.old_price), 2),  # 原价格
            "stock": book.inventory,  # 库存
            "discount": book.discount,  # 折扣信息
            "isEffective": book.inventory > 0,  # 是否有效（库存大于 0）
        }
    }

    # 返回 JSON 响应
    return JsonResponse(response_data)


def get_book_details(request):
    # 获取书籍的 ID 参数
    book_id = request.GET.get('id')
    if not book_id:
        return JsonResponse({
            "code": "400",
            "msg": "缺少必要参数 id",
            "result": None
        })

    # 获取书籍对象
    book = get_object_or_404(Book, id=book_id)

    # 获取关联的出版社信息
    publisher = book.publisher

    # 构造返回结果
    response_data = {
        "code": "200",
        "msg": "获取书籍详情成功",
        "result": {
            "brand": {
                "desc": None,
                "id": str(publisher.id),
                "logo": publisher.logo.url if publisher.logo else "",
                "name": publisher.name,
                "nameEn": publisher.name,
                "picture": publisher.picture.url if publisher.picture else "",
                "place": None,
                "type": None,
            },
            "categories": [
                {
                    "id": str(book.subcategory.id),
                    "layer": 2,  # 二级分类
                    "name": book.subcategory.name,
                    "parent": {
                        "id": str(book.subcategory.parent.id),
                        "layer": 1,
                        "name": book.subcategory.parent.name,
                        "parent": None
                    } if book.subcategory.parent else None,
                }
            ],
            "desc": book.desc,
            "details": {
                "pictures": book.main_pictures if book.main_pictures else [],
                "properties": [
                    {"name": "ISBN", "value": book.ISBN},
                    {"name": "库存", "value": str(book.inventory)},
                ]
            },
            "discount": book.discount,
            "evaluationInfo": {
                "content": "暂无评价内容",
                "createTime": "",
                "id": "",
                "member": None,
                "officialReply": None,
                "orderInfo": None,
                "pictures": None,
                "praiseCount": 0,
                "praisePercent": 100,
                "score": 5,
                "tags": None,
            },
            "hotByDay": [],
            "id": str(book.id),
            "inventory": book.inventory,
            "isCollect": None,
            "isPreSale": False,
            "mainPictures": book.main_pictures if book.main_pictures else [],
            "mainVideos": [],
            "name": book.name,
            "oldPrice": str(book.old_price),
            "price": str(round(book.old_price * (Decimal(book.discount / 100)), 2)),
            "recommends": None,
            "salesCount": book.sales_count,
            "commentCount": book.comment_count,
            "collectCount": book.collect_count,
            "similarProducts": [],
            "skus": [],
            "specs": [],
            "spuCode": "",
            "userAddresses": None,
            "videoScale": 1.0
        }
    }

    return JsonResponse(response_data)


import random
from django.http import JsonResponse
from category.models import Category
from .models import Book
import img_urls


def banner_view(request):
    # 获取投放位置参数，默认为 1（首页）
    distribution_site = int(request.GET.get("distributionSite", 1))

    # 固定随机种子
    random.seed(1337)

    if distribution_site == 1:
        # 指定的书籍ID列表
        specified_book_ids = [7592, 2998, 4379, 5826, 5071]

        # 根据指定的ID获取书籍对象
        books = Book.objects.filter(id__in=specified_book_ids)

        # 构建结果列表
        result = [
            {
                "hrefUrl": f"/books/{book.id}",
                "id": book.id,
                "imgUrl": img_urls.img_urls.get(book.id),
                "type": "book"
            }
            for book in books
        ]

    elif distribution_site == 2:
        # 分类商品页：从每个大分类中随机选择五本书籍
        categories = Category.objects.all()
        result = []
        for category in categories:
            # 获取该大分类下所有的书籍
            books = Book.objects.filter(subcategory__parent=category, main_pictures__isnull=False)
            if books.exists():
                # 从中随机选择最多 5 本书
                selected_books = random.sample(list(books), min(len(books), 5))
                # 构建每本书的响应数据并添加分类名称
                result.extend([
                    {
                        "hrefUrl": f"/books/{book.id}",
                        "id": book.id,
                        "imgUrl": book.main_pictures,
                        "type": "book",
                        "categoryName": category.name
                    }
                    for book in selected_books
                ])
    else:
        return JsonResponse({"code": "400", "msg": "Invalid distributionSite parameter"})

    response = {
        "code": "200",
        "msg": "Success",
        "result": result
    }
    return JsonResponse(response)


from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from product.models import Book
import re

@require_GET
def search_books(request):
    """
    模糊搜索书籍名称
    """
    query = request.GET.get("query", "")  # 从请求中获取搜索关键词
    if not query:
        return JsonResponse({"error": "请输入搜索关键词"}, status=400)

    # 使用正则表达式对书籍名称进行模糊匹配
    try:
        regex = re.compile(query, re.IGNORECASE)  # 构建正则表达式，忽略大小写
        books = Book.objects.filter(name__iregex=regex.pattern)  # 使用 Django 的 iregex 过滤书籍

        # 构建返回数据
        result = []
        for book in books:
            result.append({
                "id": book.id,
                "name": book.name,
                "picture": book.main_pictures,  # 假设图片的 URL 存储在 main_pictures 字段
                "children": None,
                "goods": None,
            })

        return JsonResponse(result, safe=False, status=200)

    except re.error:
        return JsonResponse({"error": "无效的正则表达式"}, status=400)
