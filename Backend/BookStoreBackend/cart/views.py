import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from user.models import User  # 替换为您的 User 模型路径

from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem
from product.models import Book
import json
from util import get_user_from_token

# def get_user_from_token(request):
#     """
#     从 JWT 令牌中解析用户信息
#     """
#     auth_header = request.headers.get('Authorization')
#     if not auth_header:
#         raise AuthenticationFailed("未提供有效的令牌")
#
#     # 移除外部的 {{}}，如果存在
#     if auth_header.startswith('{{') and auth_header.endswith('}}'):
#         auth_header = auth_header[2:-2].strip()
#
#     # 检查是否以 'Bearer ' 开头
#     if not auth_header.startswith('Bearer '):
#         raise AuthenticationFailed("未提供有效的令牌")
#
#     # 提取令牌
#     token = auth_header.split(' ')[1]
#
#     try:
#         # 解码令牌
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#         user_id = payload.get("user_id")
#
#         # 获取用户
#         user = User.objects.get(id=user_id)
#         return user
#     except jwt.ExpiredSignatureError:
#         raise AuthenticationFailed("令牌已过期")
#     except jwt.InvalidTokenError:
#         raise AuthenticationFailed("令牌无效")
#     except User.DoesNotExist:
#         raise AuthenticationFailed("用户不存在")


from decimal import Decimal
from django.http import JsonResponse


def merge_cart(request):
    if request.method != 'POST':
        return JsonResponse({"code": "405", "msg": "请求方法不被允许，仅支持 POST", "result": None}, status=405)
    try:
        user = get_user_from_token(request)
        cart_items = json.loads(request.body)  # 使用 json.loads 解析 JSON 请求体
        print(cart_items)

        # 确保购物车存在
        cart, _ = Cart.objects.get_or_create(user=user)

        response_data = []  # 用于存储返回的格式化数据

        for item in cart_items:
            id = item.get("id")  # 确保键名为小写的 "id"
            print(id)
            count = int(item.get("count", 1))
            selected = item.get("selected", True)  # 直接作为布尔值处理
            book = Book.objects.filter(id=id).first()
            if not book:
                return JsonResponse({"code": "404", "msg": f"未找到 ID 为 {id} 的书籍", "result": None}, status=404)

            # 获取或创建购物车条目
            cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book,
                                                                defaults={'original_price': book.old_price,
                                                                          'current_price': round(Decimal(book.old_price) * (
                                                                                  Decimal(book.discount) / Decimal(100)),2),
                                                                          'stock': book.inventory,
                                                                          'count': count})

            if not created:
                cart_item.count += count
                cart_item.original_price += Decimal(book.old_price) * count
                cart_item.current_price += round(Decimal(book.old_price) * (Decimal(book.discount) / Decimal(100)) * count,2)
                cart_item.save()

            # 格式化响应数据
            response_data.append({
                "id": id,
                "count": cart_item.count,
                "selected": str(selected).lower(),
                "originalPrice": str(cart_item.original_price),
                "currentPrice": str(cart_item.current_price),
                "stock": cart_item.stock,
                "picture": cart_item.picture
            })

        return JsonResponse({"code": "200", "msg": "购物车合并成功", "result": response_data})
    except Exception as e:
        return JsonResponse({"code": "500", "msg": f"服务器内部错误: {str(e)}", "result": None}, status=500)




@csrf_exempt
def cart_view(request):
    if request.method == 'GET':
        return get_cart(request)
    elif request.method == 'POST':
        return add_to_cart(request)
    elif request.method == 'DELETE':
        return delete_from_cart(request)
    else:
        return JsonResponse({
            "code": "405",
            "msg": "请求方法不被允许",
            "result": None
        }, status=405)


def get_cart(request):
    """
    获取购物车列表
    """
    try:
        user = get_user_from_token(request)

        # 获取当前用户的购物车及其条目
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return JsonResponse({
                "code": "200",
                "msg": "购物车为空",
                "result": []
            })

        items = cart.items.all()
        result = []
        for item in items:
            print(item)
            result.append({
                "id": str(item.id),
                "name": item.book.name,
                "nowOriginalPrice": str(item.original_price),
                "nowPrice": str(item.current_price),
                "picture": item.book.picture,
                "postFee": 0,
                "price": str(item.original_price),
                "stock": item.stock,
                "selected": True,
                "count": item.count,
                "isEffective": True,
                "isCollect": False,
                "attrsText": "",
                "specs": []
            })

        return JsonResponse({
            "code": "200",
            "msg": "获取购物车列表成功",
            "result": result
        })

    except Exception as e:
        return JsonResponse({
            "code": "500",
            "msg": f"服务器内部错误: {str(e)}",
            "result": None
        }, status=500)


def add_to_cart(request):
    """
    新增购物车项并返回详细数据
    """
    try:
        user = get_user_from_token(request)  # 从令牌获取用户
        data = json.loads(request.body)  # 解析请求体
        print(data)
        # id = data.get("skuId")
        id = data.get("id")

        count = int(data.get("count", 1))

        # 查找书籍
        book = Book.objects.filter(id=id).first()
        if not book:
            return JsonResponse({
                "code": "404",
                "msg": f"未找到 id 为 {id} 的书籍",
                "result": None
            }, status=404)

        # 获取或创建购物车和条目
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book,
                                                            defaults={
                                                                "original_price": book.old_price,
                                                                "current_price": Decimal(book.old_price) * (
                                                                        Decimal(1) - Decimal(book.discount) / Decimal(
                                                                    100)),
                                                                "stock": book.inventory,
                                                                "count": count,
                                                                "picture": book.picture
                                                            })

        if not created:
            cart_item.count += count
            cart_item.save()

        # 构造返回的结果数据
        result = {
            "attrsText": "",
            "count": cart_item.count,
            "discount": None,
            "id": str(cart_item.id),
            "isCollect": False,
            "isEffective": True,
            "name": book.name,
            "nowOriginalPrice": str(cart_item.original_price),
            "nowPrice": str(cart_item.current_price),
            "picture": book.main_pictures[0] if book.main_pictures else "",
            "postFee": 0,
            "price": str(cart_item.original_price),
            "selected": True,
            "skuId": str(book.id),
            "specs": [],
            "stock": cart_item.stock
        }

        return JsonResponse({
            "code": "200",
            "msg": "添加到购物车成功",
            "result": result
        })

    except Exception as e:
        return JsonResponse({
            "code": "500",
            "msg": f"服务器内部错误: {str(e)}",
            "result": None
        }, status=500)


def delete_from_cart(request):
    """
    删除购物车中的多个商品
    """
    try:
        user = get_user_from_token(request)  # 获取用户
        data = json.loads(request.body)  # 解析请求体
        ids = data.get("ids", [])  # 获取要删除的商品 ID 列表

        if not ids:
            return JsonResponse({
                "code": "400",
                "msg": "未提供需要删除的商品 ID",
                "result": False
            }, status=400)

        # 获取用户的购物车
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return JsonResponse({
                "code": "404",
                "msg": "购物车不存在",
                "result": False
            }, status=404)

        # 删除购物车中的指定商品
        deleted_items = cart.items.filter(book__id__in=ids)
        if not deleted_items.exists():
            return JsonResponse({
                "code": "404",
                "msg": "未找到需要删除的商品",
                "result": False
            }, status=404)

        deleted_items.delete()  # 删除匹配的条目

        return JsonResponse({
            "code": "200",
            "msg": "成功删除了指定商品",
            "result": True
        })

    except Exception as e:
        return JsonResponse({
            "code": "500",
            "msg": f"服务器内部错误: {str(e)}",
            "result": False
        }, status=500)

