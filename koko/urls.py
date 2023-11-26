"""koko URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", views.helloView),

    path("login/", views.login),
    path("login/headicon/", views.getlogheadicon),

    path("read/", views.read),
    path("search/", views.search),
    path("detail/", views.detail),
    path("list/", views.getlist),

    path("setting/headIcon", views.headicon_change),
    path("setting/nickname/", views.nickname_change),
    path("setting/timeline/", views.timeline_change),
    path("setting/record", views.record_change),

    path("wb/create/", views.wb_create),
    path("wb/info/", views.wb_info_change),
    path("wb/image/get", views.wb_image_get),
    path("wb/image/set", views.wb_image_set),
]
