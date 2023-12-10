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

    path("login/", views.login, name='login'),
    path("login/headicon/", views.getlogheadicon, name='getlogheadicon'),

    path("read/", views.read, name='read'),
    path("search/", views.search, name='search'),
    path("detail/", views.detail, name='detail'),
    path("list/", views.getlist, name='getlist'),

    path("setting/headIcon/", views.headicon_change, name='headicon_change'),
    path("setting/nickname/", views.nickname_change, name='nickname_change'),
    path("setting/timeline/", views.timeline_change, name='timeline_change'),
    path("setting/record/", views.record_change, name='record_change'),

    path("wb/create/", views.wb_create, name='wb_create'),
    path("wb/remove/", views.wb_remove, name='wb_remove'),
    path("wb/info/", views.wb_info_change, name='wb_info_change'),
    path("wb/image/get/", views.wb_image_get, name='wb_image_get'),
    path("wb/image/set/", views.wb_image_set, name='wb_image_set'),

    path("word/add/", views.word_add, name='word_add'),
    path("word/remove/", views.word_remove, name='word_remove'),

    path("friends/list/", views.friends_list, name="friends_list"),
    path("friends/uidsearch/", views.friends_uidsearch, name='friends_uidsearch'),
    path("friends/follow/", views.friends_follow, name='friends_follow'),
    path("friends/unfollow/", views.friends_unfollow, name='friends_unfollow'),
    path("friends/headicon/", views.friends_headicon, name='friends_headicon'),
    path("friends/namesearch/", views.friends_namesearch, name='friends_namesearch'),
]
