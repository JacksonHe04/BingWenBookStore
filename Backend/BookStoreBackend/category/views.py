from django.http import JsonResponse
from category.models import Category, SubCategory
from product.models import Book


def get_response_data(request):
    # 构造 Response 数据
    response_data = {
        "code": "200",
        "msg": "Success",
        "result": []
    }

    # 获取一级分类数据作为 Result 对象
    categories = Category.objects.all()
    for category in categories:
        result = {
            "id": str(category.id),
            "name": category.name,
            "picture": category.picture.url if category.picture else "",
            "children": [],
            "goods": []
        }

        # 获取该分类的二级分类作为 Child 对象
        subcategories = SubCategory.objects.filter(parent=category)
        for subcategory in subcategories:
            child = {
                "id": str(subcategory.id),
                "name": subcategory.name,
                "picture": subcategory.picture.url if subcategory.picture else "",
                "children": None,
                "goods": None
            }
            result["children"].append(child)

        # 获取该分类的书籍作为 Good 对象
        books = Book.objects.filter(subcategory__parent=category)[:9]
        for book in books:
            good = {
                "id": str(book.id),
                "name": book.name,
                "desc": book.desc,
                "discount": book.discount,
                "orderNum": None,
                "picture": book.main_pictures if book.main_pictures else "",  # 假设 main_pictures 是一个图片 URL 列表
                "price": str(round(book.old_price * (Decimal(book.discount/100)),2)),
            }
            result["goods"].append(good)

        response_data["result"].append(result)

    return JsonResponse(response_data)


from django.http import JsonResponse
from .models import Category, SubCategory
from product.models import Book


def get_category_view(request):
    # 获取分类 ID 参数
    category_id = request.GET.get("id")
    if not category_id:
        return JsonResponse({"code": "400", "msg": "Missing 'id' parameter"})

    try:
        # 获取指定分类
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse({"code": "404", "msg": "Category not found"})

    # 获取子分类
    subcategories = SubCategory.objects.filter(parent=category)

    # 构建子分类数据
    children = []
    for subcategory in subcategories:
        # 获取子分类中的商品
        books = Book.objects.filter(subcategory=subcategory)

        goods = [
            {
                "desc": book.desc,
                "discount": None,  # 假设没有折扣信息
                "id": str(book.id),
                "name": book.name,
                "orderNum": book.sales_count,  # 使用销售量作为 orderNum
                "picture": book.main_pictures if book.main_pictures else "",
                "price": str(round(book.old_price * (Decimal(book.discount/100)),2)),
            }
            for book in books
        ]

        children.append({
            "brands": None,  # 假设没有品牌信息
            "categories": category.name,  # 假设没有多级子分类
            "goods": goods,
            "id": str(subcategory.id),
            "name": subcategory.name,
            "parentId": str(category.id),
            "parentName": category.name,
            "picture": subcategory.picture.url if subcategory.picture else "",
            "saleProperties": None,  # 假设没有销售属性
        })

    # 构建返回数据
    result = {
        "children": children,
        "id": str(category.id),
        "name": category.name,
        "picture": category.picture.url if category.picture else None,
    }

    response = {
        "code": "200",
        "msg": "Success",
        "result": result
    }
    return JsonResponse(response)


from django.http import JsonResponse
from .models import SubCategory, Category
from product.models import Book
from decimal import Decimal

def get_subcategory_filter_view(request):
    # 获取子分类 ID 参数
    subcategory_id = request.GET.get("id")
    if not subcategory_id:
        return JsonResponse({"code": "400", "msg": "Missing 'id' parameter"})

    try:
        # 获取指定子分类
        subcategory = SubCategory.objects.get(id=subcategory_id)
    except SubCategory.DoesNotExist:
        return JsonResponse({"code": "404", "msg": "Subcategory not found"})

    # 获取子分类所属的大分类
    parent_category = subcategory.parent

    # 获取子分类中的商品
    books = Book.objects.filter(subcategory=subcategory)

    # 构建商品数据
    goods = [
        {
            "desc": book.desc,
            "id": str(book.id),
            "name": book.name,
            "orderNum": book.sales_count,  # 使用销售量作为 orderNum
            "picture": book.main_pictures if book.main_pictures else "",
            "price": str(round(book.old_price * (Decimal(book.discount/100)),2)),
        }
        for book in books
    ]

    # 构建分类数据（当前子分类作为唯一分类）
    categories = [
        {
            "id": str(subcategory.id),
            "layer": 2,  # 假设这是第二层分类
            "name": subcategory.name,
            "parent": None,  # 无需嵌套子分类
        }
    ]

    # 假设品牌和销售属性在当前实现中为空
    brands = []
    sale_properties = []

    # 构建返回数据
    result = {
        "brands": brands,
        "categories": categories,
        "goods": goods,
        "id": str(subcategory.id),
        "name": subcategory.name,
        "parentId": str(parent_category.id) if parent_category else None,
        "parentName": parent_category.name if parent_category else None,
        "picture": subcategory.picture if subcategory.picture else None,
        "saleProperties": sale_properties,
    }

    response = {
        "code": "200",
        "msg": "Success",
        "result": result
    }
    return JsonResponse(response)
