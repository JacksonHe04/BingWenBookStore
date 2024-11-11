"""
URL configuration for BookStoreBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


class CustomRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = super().get_redirect_url(*args, **kwargs)
        return url

    def post(self, request, *args, **kwargs):
        self.url = self.get_redirect_url(*args, **kwargs)
        return HttpResponseRedirect(self.url, status=307)  # 使用307保持POST请求


def login_to_user_redirect(request, subpath=None):
    # 构建新的 URL
    target_url = f'/user/{subpath}' if subpath else '/user/'

    # 获取查询参数并附加到目标 URL
    query_string = request.META.get('QUERY_STRING', '')
    if query_string:
        target_url += f'?{query_string}' if '?' not in target_url else f'&{query_string}'

    # 保留 POST 请求的数据
    if request.method == 'POST':
        return HttpResponseRedirect(target_url, status=307)
    else:
        return redirect(target_url)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('home/category/', include('category.urls')),

    path('home/brand/', RedirectView.as_view(url='/product/', query_string=True)),
    path('product/', include('product.urls')),

    re_path(r'^login(?:/(.*))?$', login_to_user_redirect),
    path('user/', include('user.urls')),

    # path('login', CustomRedirectView.as_view(url='/user/', query_string=True)),
    # path('user/', include('user.urls')),

]
