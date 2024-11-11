from django.db.models import Sum
from django.http import JsonResponse
from product.models import Author


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
