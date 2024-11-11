from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from user.models import User
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

@csrf_exempt  # 仅在开发中使用，生产环境应使用更安全的CSRF管理
def login_view(request):
    # 确保请求方法为 POST
    if request.method != 'POST':
        return JsonResponse({
            "code": "400",
            "msg": "请求方法不正确，仅支持 POST",
            "result": {}
        })

    # 从请求体中获取用户名和密码
    account = request.POST.get('account') or request.GET.get('account')
    password = request.POST.get('password') or request.GET.get('password')

    user = authenticate(username=account, password=password)
    if user is None:
        return JsonResponse({
            "code": "401",
            "msg": "用户名或密码错误",
            "result": {}
        })

    # 获取用户详细信息
    user_data = User.objects.get(account=account)
    result = {
        "account": user_data.account,
        "avatar": user_data.avatar.url if user_data.avatar else "",
        "birthday": user_data.birthday.isoformat() if user_data.birthday else "",
        "cityCode": user_data.city_code,
        "gender": user_data.gender,
        "id": str(user_data.id),
        "mobile": user_data.mobile,
        "nickname": user_data.nickname,
        "profession": user_data.profession,
        "provinceCode": user_data.province_code,
        "token": user_data.token,
    }

    # 构造成功响应
    response_data = {
        "code": "200",
        "msg": "登录成功",
        "result": result
    }
    return JsonResponse(response_data)


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
