# Backend 开发说明

郑宇榕你好！欢迎使用 Django 框架开发此项目的后端。在进行开发时，请注意 **仅在本 Backend 目录内开发后端**，不要修改或影响目录外的前端内容。前端已经使用 Vue 框架开发完成，您可以通过 Django 与前端进行有效通信。

## 基本要求

- 本项目使用 **Django** 框架，请确保您的开发环境中已经正确安装。
- 开发过程中请使用 `django-admin` 或 `manage.py` 命令创建应用、管理数据库等。

## Django 基本教程

1. 安装 Django:
   ```bash
   pip install django
   ```

2. 创建 Django 项目:
   ```bash
   django-admin startproject myproject
   ```

3. 启动开发服务器:
   ```bash
   python manage.py runserver
   ```

4. 创建应用:
   ```bash
   python manage.py startapp myapp
   ```

详细教程可以参考 [Django 官方文档](https://docs.djangoproject.com/en/stable/intro/).

## 使用 `rest_framework` 和 `corsheaders` 进行前后端通信

为了使 Django 后端与 Vue 前端能够进行有效通信，您需要配置 `rest_framework` 和 `corsheaders` 库。下面是基本步骤：

### 1. 安装相关库

在项目环境中安装 `Django REST framework` 和 `django-cors-headers`：

```bash
pip install djangorestframework
pip install django-cors-headers
```

### 2. 在 `settings.py` 中配置

在 `INSTALLED_APPS` 中添加：

```python
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'corsheaders',
    ...
]
```

### 3. 配置 CORS

在 `MIDDLEWARE` 中添加 `corsheaders.middleware.CorsMiddleware`，并允许跨域请求：

```python
MIDDLEWARE = [
    ...,
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOW_ALL_ORIGINS = True  # 如果只允许特定域名，替换为对应的 Vue 前端地址
```

### 4. 设置 REST framework

在 `settings.py` 中添加 REST framework 的基本配置：

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
```

### 5. 编写 API 接口

在您的应用中，编写 Django REST framework 的 `views` 和 `serializers`，用于与前端通信。

### 6. 测试通信

使用 Vue 前端通过 `axios` 或其他 HTTP 客户端与 Django 后端 API 进行通信，确保 CORS 设置正确，数据可以正常传输。

## 总结

请确保在当前 Backend 目录中使用 Django 开发后端，并通过配置 `rest_framework` 和 `corsheaders` 实现与 Vue 前端的通信。前端文件已在目录外，请勿修改。

如有任何问题，请随时与我（何锦诚）沟通。Happy coding!