import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from user.models import User  # 替换为您的 User 模型路径

def get_user_from_token(request):
    """
    从 JWT 令牌中解析用户信息
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise AuthenticationFailed("未提供有效的令牌")

    # 移除外部的 {{}}，如果存在
    if auth_header.startswith('{{') and auth_header.endswith('}}'):
        auth_header = auth_header[2:-2].strip()

    # 检查是否以 'Bearer ' 开头
    if not auth_header.startswith('Bearer '):
        raise AuthenticationFailed("未提供有效的令牌")

    # 提取令牌
    token = auth_header.split(' ')[1]

    try:
        # 解码令牌
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get("user_id")

        # 获取用户
        user = User.objects.get(id=user_id)
        return user
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("令牌已过期")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("令牌无效")
    except User.DoesNotExist:
        raise AuthenticationFailed("用户不存在")
