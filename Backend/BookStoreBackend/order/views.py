from datetime import timedelta
from decimal import Decimal
from cart.models import CartItem
from django.db import transaction
from django.http import JsonResponse
from .models import Order, OrderItem, Address
from util import get_user_from_token


def create_order_summary_and_save(request):
    try:
        # 从请求中获取用户
        user = get_user_from_token(request)

        # 获取用户购物车的商品
        cart_items = CartItem.objects.filter(cart__user=user)
        if not cart_items.exists():
            return JsonResponse({"code": "400", "msg": "购物车为空，无法创建订单"}, status=400)

        goods = []
        total_price = Decimal(0)
        total_pay_price = Decimal(0)
        total_goods_count = 0

        for item in cart_items:
            good_data = {
                "id": str(item.book.id),
                "name": item.book.name,
                "attrsText": "N/A",  # 如果需要添加商品属性信息，可以在此扩展
                "count": item.count,
                "price": str(item.original_price),
                "payPrice": str(item.current_price),
                "totalPrice": str(item.original_price * item.count),
                "totalPayPrice": str(item.current_price * item.count),
                "skuId": str(item.id),  # 使用 `item.id` 模拟 SKU ID
                "picture": item.book.main_pictures[0] if item.book.main_pictures else None,
            }
            goods.append(good_data)

            total_price += item.original_price * item.count
            total_pay_price += item.current_price * item.count
            total_goods_count += item.count

        # 固定邮费和折扣计算
        post_fee = Decimal("10.00")  # 使用 Decimal 定义邮费
        discount_price = total_price - total_pay_price

        # 获取用户地址信息
        addresses = Address.objects.filter(user=user)
        if not addresses.exists():
            return JsonResponse({"code": "400", "msg": "没有找到用户地址，请先添加收货地址"}, status=400)

        # 使用默认地址作为订单地址
        shipping_address = addresses.filter(is_default=True).first() or addresses.first()

        # 开始事务保存订单和订单商品
        with transaction.atomic():
            # 创建订单
            order = Order.objects.create(
                user=user,
                total_price=total_price,
                total_pay_price=total_pay_price + post_fee,
                discount_price=discount_price,
                post_fee=post_fee,
                shipping_address=shipping_address,
            )

            # 创建订单商品
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    count=item.count,
                    original_price=item.original_price,
                    current_price=item.current_price,
                    total_price=item.original_price * item.count,
                    total_pay_price=item.current_price * item.count,
                )

            # # 清空购物车
            # cart_items.delete()

        # 计算订单总结数据
        summary = {
            "totalPrice": str(total_price),
            "totalPayPrice": str(total_pay_price + post_fee),
            "goodsCount": total_goods_count,
            "postFee": str(post_fee),
            "discountPrice": str(discount_price),
        }

        # 构造地址响应
        user_addresses = [
            {
                "id": str(address.id),
                "receiver": address.receiver,
                "contact": address.contact,
                "address": address.address,
                "cityCode": address.city_code,
                "countyCode": address.county_code,
                "provinceCode": address.province_code,
                "fullLocation": address.full_location,
                "isDefault": int(address.is_default),
                "addressTags": address.address_tags,
                "postalCode": address.postal_code,
            }
            for address in addresses
        ]

        # 构造响应数据
        response_data = {
            "code": "200",
            "msg": "订单创建成功",
            "result": {
                "orderId": str(order.id),
                "goods": goods,
                "summary": summary,
                "userAddresses": user_addresses,
            },
        }
        return JsonResponse(response_data, status=200)

    except Exception as e:
        return JsonResponse({"code": "500", "msg": f"订单创建失败: {str(e)}"}, status=500)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from util import get_user_from_token

def get_order_detail(request, id):
    try:
        # 获取用户信息
        user = get_user_from_token(request)

        # 获取订单信息
        order = get_object_or_404(Order, id=id, user=user)

        # 获取订单商品信息
        order_items = OrderItem.objects.filter(order=order)

        # 构造商品详情列表
        skus = []
        for item in order_items:
            skus.append({
                "attrsText": "N/A",  # 如果有商品属性信息，可在此扩展
                "curPrice": float(item.current_price),
                "id": str(item.id),
                "image": item.book.main_pictures[0] if item.book.main_pictures else None,
                "name": item.book.name,
                "properties": [],  # 可扩展属性信息
                "quantity": item.count,
                "realPay": float(item.total_pay_price),
                "spuId": str(item.book.id),
                "totalMoney": float(item.total_price),
            })

        # 构造订单详情响应数据
        result = {
            "arrivalEstimatedTime": None,  # 假设无预计到达时间
            "cityCode": order.shipping_address.city_code,
            "closeTime": order.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "consignTime": None,  # 假设无发货时间
            "countdown": 1800,  # 假设付款倒计时为 30 分钟
            "countyCode": order.shipping_address.county_code,
            "createTime": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "deliveryTimeType": 0,  # 假设固定配送类型
            "endTime": None,  # 假设无结束时间
            "evaluationTime": None,  # 假设无评价时间
            "id": str(order.id),
            "orderState": 1,  # 假设订单状态为 "已创建"
            "payChannel": 0,  # 假设固定支付渠道
            "payLatestTime": (order.created_at + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"),
            "payMoney": float(order.total_pay_price),
            "payState": 0,  # 假设支付状态为未支付
            "payTime": None,  # 假设未支付
            "payType": 0,  # 假设固定支付类型
            "postFee": float(order.post_fee),
            "provinceCode": order.shipping_address.province_code,
            "receiverAddress": order.shipping_address.full_location,
            "receiverContact": order.shipping_address.receiver,
            "receiverMobile": order.shipping_address.contact,
            "skus": skus,
            "totalMoney": float(order.total_price),
            "totalNum": sum(item.count for item in order_items),
        }

        return JsonResponse({"code": "200", "msg": "成功", "result": result}, status=200)
    except Exception as e:
        return JsonResponse({"code": "500", "msg": f"获取订单详情失败: {str(e)}"}, status=500)
