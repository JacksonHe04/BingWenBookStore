from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from user.models import User
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User  # 替换为您的 User 模型路径

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user.models import User, Address  # 替换为您的 User 模型路径
from util import get_user_from_token




import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import jwt
from django.conf import settings

# /user/
@csrf_exempt  # 仅在开发中使用，生产环境应使用更安全的 CSRF 管理
def login_view(request):
    # 确保请求方法为 POST
    if request.method != 'POST':
        return JsonResponse({
            "code": "400",
            "msg": "请求方法不正确，仅支持 POST",
            "result": {}
        })

    try:
        # 解析 JSON 请求体
        data = json.loads(request.body)
        account = data.get('account')
        password = data.get('password')
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({
            "code": "400",
            "msg": "请求体格式不正确",
            "result": {}
        })

    if not account or not password:
        return JsonResponse({
            "code": "400",
            "msg": "账号和密码不能为空",
            "result": {}
        })

    try:
        # 查找用户
        user_data = User.objects.get(account=account)  # 假设使用 account 字段存储账号

        # 验证明文密码
        if user_data.password != password:  # 假设数据库中直接存储明文密码
            return JsonResponse({
                "code": "401",
                "msg": "用户名或密码错误",
                "result": {}
            })

        # 生成访问令牌（JWT）
        payload = {
            "user_id": user_data.id,
            "account": user_data.account,
            "exp": datetime.utcnow() + timedelta(minutes=720),  # 令牌有效期 15 分钟
            "iat": datetime.utcnow(),
        }
        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        # 构造返回的用户信息
        result = {
            "account": user_data.account,
            "avatar": user_data.profile.avatar.url if hasattr(user_data, 'profile') and user_data.profile.avatar else "",
            "birthday": user_data.profile.birthday.isoformat() if hasattr(user_data, 'profile') and user_data.profile.birthday else "",
            "cityCode": user_data.profile.city_code if hasattr(user_data, 'profile') else "",
            "gender": user_data.profile.gender if hasattr(user_data, 'profile') else "",
            "id": str(user_data.id),
            "mobile": user_data.profile.mobile if hasattr(user_data, 'profile') else "",
            "nickname": user_data.profile.nickname if hasattr(user_data, 'profile') else "",
            "profession": user_data.profile.profession if hasattr(user_data, 'profile') else "",
            "provinceCode": user_data.profile.province_code if hasattr(user_data, 'profile') else "",
            "token": access_token,  # 使用生成的 JWT 令牌
        }

        return JsonResponse({
            "code": "200",
            "msg": "登录成功",
            "result": result
        })

    except User.DoesNotExist:
        return JsonResponse({
            "code": "401",
            "msg": "用户名或密码错误",
            "result": {}
        })



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import random
from .models import User


class UserVerificationView(APIView):
    def get(self, request):
        # 处理 GET 请求：生成验证码
        mobile = request.query_params.get('mobile')

        # 验证手机号是否存在
        if not mobile:
            return Response({
                "code": "400",
                "msg": "手机号不能为空",
                "result": None
            }, status=status.HTTP_400_BAD_REQUEST)

        # 随机生成 6 位数字验证码
        verification_code = str(random.randint(100000, 999999))

        # 响应格式
        response_data = {
            "code": "200",
            "msg": "验证码生成成功",
            "result": None,
            "verification_code": verification_code  # 添加验证码信息，便于测试展示
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        # 处理 POST 请求：获取用户数据
        code = request.POST.get('code') or request.GET.get('code')
        mobile = request.POST.get('mobile') or request.GET.get('mobile')
        # code = request.data.get('code')
        # mobile = request.data.get('mobile')

        # 验证码验证（简单示例，生产环境应替换为实际的验证逻辑）
        if code != "123456":  # 模拟验证码匹配
            return Response({
                "code": "400",
                "msg": "验证码错误",
                "result": None
            }, status=status.HTTP_400_BAD_REQUEST)

        # 查找用户数据
        user = get_object_or_404(User, mobile=mobile)

        # 构造返回结果
        response_data = {
            "code": "200",
            "msg": "获取用户数据成功",
            "result": {
                "account": user.account,
                "avatar": user.avatar.url if user.avatar else None,
                "birthday": user.birthday,
                "cityCode": user.city_code,
                "gender": user.gender,
                "id": str(user.id),
                "mobile": user.mobile,
                "nickname": user.nickname,
                "profession": user.profession,
                "provinceCode": user.province_code,
                "token": user.token,
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)


from django.http import JsonResponse
import json

from django.http import JsonResponse
import json


def address_method(request):
    """
    添加收货地址（POST）或获取收货地址列表（GET）
    """
    try:
        user = get_user_from_token(request)  # 从令牌中获取用户信息

        if request.method == 'POST':
            # 添加收货地址
            data = json.loads(request.body)  # 解析请求体

            # 提取数据
            receiver = data.get("receiver")
            contact = data.get("contact")
            province_code = data.get("provinceCode")
            city_code = data.get("cityCode")
            county_code = data.get("countyCode")
            address = data.get("address")
            postal_code = data.get("postalCode")
            address_tags = data.get("addressTags", "")
            is_default = bool(data.get("isDefault", 0))
            full_location = data.get("fullLocation")

            # 验证必要字段
            if not all([receiver, contact, province_code, city_code, county_code, address, full_location]):
                return JsonResponse({
                    "code": "400",
                    "msg": "必要字段缺失",
                    "result": None
                }, status=400)

            # 如果是默认地址，取消其他地址的默认状态
            if is_default:
                Address.objects.filter(user=user, is_default=True).update(is_default=False)

            # 创建新地址
            new_address = Address.objects.create(
                user=user,
                receiver=receiver,
                contact=contact,
                province_code=province_code,
                city_code=city_code,
                county_code=county_code,
                address=address,
                postal_code=postal_code,
                address_tags=address_tags,
                is_default=is_default,
                full_location=full_location
            )

            return JsonResponse({
                "code": "200",
                "msg": "收货地址添加成功",
                "result": {
                    "id": new_address.id,
                    "receiver": new_address.receiver,
                    "contact": new_address.contact,
                    "fullLocation": new_address.full_location,
                    "address": new_address.address,
                    "postalCode": new_address.postal_code,
                    "addressTags": new_address.address_tags,
                    "isDefault": new_address.is_default
                }
            })

        elif request.method == 'GET':
            # 获取收货地址列表
            addresses = Address.objects.filter(user=user)

            # 格式化地址列表为符合接口要求的结构
            address_list = [{
                "id": str(address.id),  # 确保 ID 是字符串类型
                "receiver": address.receiver,
                "contact": address.contact,
                "fullLocation": address.full_location,
                "address": address.address,
                "postalCode": address.postal_code or None,  # 如果邮政编码为空，返回 None
                "addressTags": address.address_tags or None,  # 如果地址标签为空，返回 None
                "isDefault": address.is_default
            } for address in addresses]

            # 返回的响应格式
            return JsonResponse({
                "code": "200",
                "msg": "收货地址获取成功",
                "result": address_list
            })

        else:
            return JsonResponse({
                "code": "405",
                "msg": "请求方法不被允许，仅支持 GET 和 POST",
                "result": None
            }, status=405)

    except Exception as e:
        return JsonResponse({
            "code": "500",
            "msg": f"服务器内部错误: {str(e)}",
            "result": None
        }, status=500)


# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Address
from util import get_user_from_token

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Address
import json
from util import get_user_from_token


def address_edit_delete(request, id):
    """
    删除或更新收货地址
    """
    try:
        user = get_user_from_token(request)  # 从令牌中获取用户信息

        # 仅允许 DELETE 和 PUT 请求
        if request.method == 'DELETE':
            # 删除收货地址
            address = get_object_or_404(Address, id=id, user=user)
            address.delete()

            return JsonResponse({
                "code": "200",
                "msg": "收货地址删除成功",
                "result": None
            })

        elif request.method == 'PUT':
            # 更新收货地址
            data = json.loads(request.body)  # 解析请求体

            # 获取要更新的地址
            address = get_object_or_404(Address, id=id, user=user)

            # 提取数据
            receiver = data.get("receiver", address.receiver)
            contact = data.get("contact", address.contact)
            province_code = data.get("provinceCode", address.province_code)
            city_code = data.get("cityCode", address.city_code)
            county_code = data.get("countyCode", address.county_code)
            address_field = data.get("address", address.address)
            postal_code = data.get("postalCode", address.postal_code)
            address_tags = data.get("addressTags", address.address_tags)
            is_default = bool(data.get("isDefault", address.is_default))
            full_location = data.get("fullLocation", address.full_location)

            # 验证必要字段
            if not all([receiver, contact, province_code, city_code, county_code, address_field, full_location]):
                return JsonResponse({
                    "code": "400",
                    "msg": "必要字段缺失",
                    "result": None
                }, status=400)

            # 如果是默认地址，取消其他地址的默认状态
            if is_default:
                Address.objects.filter(user=user, is_default=True).update(is_default=False)

            # 更新地址
            address.receiver = receiver
            address.contact = contact
            address.province_code = province_code
            address.city_code = city_code
            address.county_code = county_code
            address.address = address_field
            address.postal_code = postal_code
            address.address_tags = address_tags
            address.is_default = is_default
            address.full_location = full_location
            address.save()

            return JsonResponse({
                "code": "200",
                "msg": "收货地址更新成功",
                "result": {
                    "id": address.id,
                    "receiver": address.receiver,
                    "contact": address.contact,
                    "fullLocation": address.full_location,
                    "address": address.address,
                    "postalCode": address.postal_code,
                    "addressTags": address.address_tags,
                    "isDefault": address.is_default
                }
            })

        else:
            return JsonResponse({"code": "405", "msg": "请求方法不被允许，仅支持 DELETE 和 PUT", "result": None},
                                status=405)

    except Exception as e:
        return JsonResponse({
            "code": "500",
            "msg": f"服务器内部错误: {str(e)}",
            "result": None
        }, status=500)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from user.models import User

@csrf_exempt
@require_POST
def register_user(request):
    """
    用户注册视图函数
    接收账号和密码，将用户信息存入数据库
    """
    try:
        # 从请求体中解析 JSON 数据
        body = json.loads(request.body.decode('utf-8'))
        account = body.get('account')
        password = body.get('password')

        # 校验必填字段
        if not account or not password:
            return JsonResponse({"error": "账号和密码是必填项"}, status=400)

        # 检查账号是否已存在
        if User.objects.filter(account=account).exists():
            return JsonResponse({"error": "该账号已被注册"}, status=400)

        # 创建新用户并保存到数据库
        user = User.objects.create_user(account=account, password=password)
        user.save()

        return JsonResponse({"message": "注册成功", "user_id": user.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "无效的 JSON 数据"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"注册失败: {str(e)}"}, status=500)

