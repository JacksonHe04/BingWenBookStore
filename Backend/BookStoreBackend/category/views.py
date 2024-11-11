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
        books = Book.objects.filter(subcategory__parent=category)
        for book in books:
            good = {
                "id": str(book.id),
                "name": book.name,
                "desc": book.desc,
                "discount": book.discount,
                "orderNum": None,
                "picture": book.main_pictures[0] if book.main_pictures else "",  # 假设 main_pictures 是一个图片 URL 列表
                "price": str(book.old_price)
            }
            result["goods"].append(good)

        response_data["result"].append(result)

    return JsonResponse(response_data)
