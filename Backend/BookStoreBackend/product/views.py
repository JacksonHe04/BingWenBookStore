from django.db.models import Sum
from django.http import JsonResponse
from product.models import Author
from django.shortcuts import get_object_or_404
from .models import Book
from decimal import Decimal

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
            "picture": request.build_absolute_uri(author.picture.url) if author.picture else None,
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
            "nowPrice": float(book.old_price) * (1 - book.discount / 100),  # 计算折后价格
            "oldPrice": float(book.old_price),  # 原价格
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
            "collectCount": book.collect_count,
            "commentCount": book.comment_count,
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
            "price": str(book.old_price * (1 - Decimal(book.discount / 100))),
            "recommends": None,
            "salesCount": book.sales_count,
            "similarProducts": [],
            "skus": [],
            "specs": [],
            "spuCode": "",
            "userAddresses": None,
            "videoScale": 1.0
        }
    }

    return JsonResponse(response_data)
